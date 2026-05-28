#!/usr/bin/env python3
"""
YouTube Analyzer — one-command pipeline for Claude Code best-practices research.

Usage:
    python3 analyze.py <youtube_url> [--output-dir /path/to/dir]

Steps:
    1. Fetch metadata via yt-dlp
    2. Fetch transcript via youtube-transcript-api (with fallback to manual paste)
    3. Classify topic → choose target subfolder
    4. Deduplicate — skip if same URL already saved
    5. Save transcript + metadata
    6. Auto-update README.md index
    7. Print full transcript so Claude can analyze inline
"""

import sys
import re
import json
import time
import socket
import argparse
from datetime import datetime
from pathlib import Path

# ── Dependency checks ────────────────────────────────────────────────────────

try:
    import yt_dlp
except ImportError:
    sys.exit("yt-dlp not installed. Run: pip3 install yt-dlp")

try:
    from youtube_transcript_api import (
        YouTubeTranscriptApi,
        CouldNotRetrieveTranscript,
        NoTranscriptFound,
        TranscriptsDisabled,
        VideoUnavailable,
        YouTubeRequestFailed,
    )
except ImportError:
    sys.exit("youtube-transcript-api not installed. Run: pip3 install youtube-transcript-api")

# ── Constants ─────────────────────────────────────────────────────────────────

MAX_TRANSCRIPT_WORDS = 40_000   # truncate beyond this to avoid context overflow
MAX_RETRIES = 3
RETRY_DELAY = 5                 # seconds between retries

TOPIC_KEYWORDS = {
    "tips-tricks":       ["hack", "trick", "tip", "level up", "cheat", "shortcut", "workflow"],
    "agents":            ["agent", "sub-agent", "multi-agent", "agentic", "autonomous"],
    "mcp":               ["mcp", "model context protocol", "server", "tool use"],
    "prompting":         ["prompt", "prompting", "instruction", "system prompt", "context"],
    "cost-optimization": ["cost", "token", "cheap", "haiku", "budget", "optimize"],
    "setup":             ["install", "setup", "config", "getting started", "beginners"],
    "tools":             ["tool", "cli", "extension", "plugin", "integration"],
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def extract_video_id(url: str) -> str:
    """Extract 11-char video ID from any YouTube URL format."""
    patterns = [
        r"youtu\.be/([a-zA-Z0-9_-]{11})",
        r"[?&]v=([a-zA-Z0-9_-]{11})",
        r"embed/([a-zA-Z0-9_-]{11})",
        r"shorts/([a-zA-Z0-9_-]{11})",
    ]
    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1)
    die(f"Could not extract video ID from URL: {url}\n"
        "Supported formats: youtu.be/ID, youtube.com/watch?v=ID, /shorts/ID, /embed/ID")


def slugify(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[\s_-]+", "-", text).strip("-")[:60]


def die(msg: str) -> None:
    print(f"\n[ERROR] {msg}", file=sys.stderr)
    sys.exit(1)


def warn(msg: str) -> None:
    print(f"[WARN]  {msg}", file=sys.stderr)


def truncate_transcript(text: str) -> tuple[str, bool]:
    """Truncate to MAX_TRANSCRIPT_WORDS; return (text, was_truncated)."""
    words = text.split()
    if len(words) <= MAX_TRANSCRIPT_WORDS:
        return text, False
    truncated = " ".join(words[:MAX_TRANSCRIPT_WORDS])
    return truncated, True


def find_existing_transcript(base: Path, video_id: str) -> Path | None:
    """Return path to an already-saved transcript for this video_id, if any."""
    for f in base.glob("transcripts/**/*.txt"):
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
            first_lines = content[:500]
            if video_id in first_lines:
                return f
        except OSError:
            continue
    return None

# ── Core steps ────────────────────────────────────────────────────────────────

def get_metadata(url: str) -> dict:
    """Fetch video metadata via yt-dlp with error handling."""
    if "list=" in url and "v=" not in url and "youtu.be" not in url:
        die("URL looks like a playlist. Pass an individual video URL instead.")

    opts = {
        "quiet": True,
        "no_warnings": True,
        "socket_timeout": 20,
        "logtostderr": False,
        "logger": type("NullLogger", (), {
            "debug":     lambda s, m: None,
            "info":      lambda s, m: None,
            "warning":   lambda s, m: None,
            "error":     lambda s, m: None,
            "stdout":    lambda s, m: None,
            "trace":     lambda s, m: None,
            "log_level": None,
            "prefix":    "",
        })(),
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=False)

            if info is None:
                die("yt-dlp returned no data. The video may be unavailable.")

            return {
                "title":       info.get("title") or "Unknown Title",
                "channel":     info.get("channel") or info.get("uploader") or "Unknown Channel",
                "duration":    info.get("duration") or 0,
                "views":       info.get("view_count") or 0,
                "upload_date": info.get("upload_date") or "",
                "url":         url,
                "video_id":    info.get("id") or extract_video_id(url),
                "description": (info.get("description") or "")[:600],
                "is_live":     bool(info.get("is_live")),
            }

        except yt_dlp.utils.DownloadError as e:
            err = str(e).lower()
            if "private" in err:
                die("Video is private. Provide the transcript text manually.")
            if "unavailable" in err or "not available" in err or "removed" in err or "404" in err or "does not exist" in err:
                die("Video is unavailable or has been deleted.")
            if "age" in err or "sign in" in err:
                die("Video is age-restricted. Provide the transcript text manually.")
            if "members only" in err:
                die("Video is members-only. Provide the transcript text manually.")
            if attempt < MAX_RETRIES:
                warn(f"Metadata fetch failed (attempt {attempt}/{MAX_RETRIES}): {e}. Retrying in {RETRY_DELAY}s...")
                time.sleep(RETRY_DELAY)
            else:
                die(f"Failed to fetch metadata after {MAX_RETRIES} attempts: {e}")

        except socket.timeout:
            if attempt < MAX_RETRIES:
                warn(f"Network timeout (attempt {attempt}/{MAX_RETRIES}). Retrying...")
                time.sleep(RETRY_DELAY)
            else:
                die("Network timeout fetching video metadata. Check your connection.")

        except Exception as e:
            die(f"Unexpected error fetching metadata: {type(e).__name__}: {e}")

    die("Metadata fetch exhausted all retries.")  # unreachable but satisfies type checker


def get_transcript(video_id: str) -> tuple[str, str]:
    """
    Fetch transcript text. Returns (transcript_text, source_label).
    source_label is one of: 'manual' | 'english' | 'auto-generated' | 'translated:<lang>'
    Falls back through: English → auto-generated → first available → manual paste.
    """
    api = YouTubeTranscriptApi()

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            transcript_list = api.list(video_id)

            # Priority 1: manually created English transcript
            try:
                t = transcript_list.find_manually_created_transcript(["en", "en-US", "en-GB"])
                snippets = list(t.fetch())
                text = " ".join(s.text.replace("\n", " ") for s in snippets)
                return text, "english"
            except NoTranscriptFound:
                pass

            # Priority 2: auto-generated English transcript
            try:
                t = transcript_list.find_generated_transcript(["en", "en-US", "en-GB"])
                snippets = list(t.fetch())
                text = " ".join(s.text.replace("\n", " ") for s in snippets)
                return text, "auto-generated"
            except NoTranscriptFound:
                pass

            # Priority 3: translate first available transcript to English
            available = list(transcript_list)
            if available:
                lang = available[0].language_code
                warn(f"No English transcript. Translating from '{lang}'...")
                t = available[0].translate("en")
                snippets = list(t.fetch())
                text = " ".join(s.text.replace("\n", " ") for s in snippets)
                return text, f"translated:{lang}"

            # Priority 4: manual fallback
            return _manual_transcript_input(video_id), "manual"

        except TranscriptsDisabled:
            warn("Transcripts are disabled for this video.")
            return _manual_transcript_input(video_id), "manual"

        except VideoUnavailable:
            die("Video is unavailable. Cannot fetch transcript.")

        except YouTubeRequestFailed as e:
            if attempt < MAX_RETRIES:
                warn(f"YouTube API error (attempt {attempt}/{MAX_RETRIES}): {e}. Retrying in {RETRY_DELAY}s...")
                time.sleep(RETRY_DELAY * attempt)  # exponential-ish backoff
            else:
                warn(f"YouTube API failed after {MAX_RETRIES} attempts: {e}")
                return _manual_transcript_input(video_id), "manual"

        except CouldNotRetrieveTranscript as e:
            if attempt < MAX_RETRIES:
                warn(f"Could not retrieve transcript (attempt {attempt}/{MAX_RETRIES}): {e}. Retrying in {RETRY_DELAY}s...")
                time.sleep(RETRY_DELAY * attempt)
            else:
                warn(f"Failed to retrieve transcript: {e}")
                return _manual_transcript_input(video_id), "manual"

        except socket.timeout:
            if attempt < MAX_RETRIES:
                warn(f"Network timeout fetching transcript (attempt {attempt}/{MAX_RETRIES}). Retrying...")
                time.sleep(RETRY_DELAY)
            else:
                warn("Network timeout. Falling back to manual transcript.")
                return _manual_transcript_input(video_id), "manual"

        except Exception as e:
            warn(f"Unexpected transcript error: {type(e).__name__}: {e}")
            return _manual_transcript_input(video_id), "manual"

    return _manual_transcript_input(video_id), "manual"


def _manual_transcript_input(video_id: str) -> str:
    """Prompt user to paste transcript text manually."""
    print(f"\n[ACTION NEEDED] Could not fetch transcript automatically for video: {video_id}")
    print("Paste the transcript text below, then press Enter twice + Ctrl+D (Mac/Linux) or Ctrl+Z Enter (Windows):")
    print("-" * 60)
    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass
    text = "\n".join(lines).strip()
    if not text:
        die("No transcript provided. Cannot continue.")
    return text


def classify_topic(title: str, description: str) -> str:
    """Score title + description against topic keyword lists; return best match."""
    text = (title + " " + description).lower()
    scores = {
        topic: sum(1 for kw in keywords if kw in text)
        for topic, keywords in TOPIC_KEYWORDS.items()
    }
    best = max(scores, key=lambda t: scores[t])
    return best if scores[best] > 0 else "general"


def save_transcript(base: Path, meta: dict, transcript: str, topic: str, source: str, truncated: bool) -> Path:
    """Save transcript + metadata header to the right topic subfolder."""
    date = datetime.now().strftime("%Y-%m-%d")
    slug = slugify(meta["title"])
    folder = base / "transcripts" / topic
    try:
        folder.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        die(f"Could not create transcript folder '{folder}': {e}")

    path = folder / f"{date}_{slug}.txt"

    warnings = []
    if truncated:
        warnings.append(f"TRUNCATED to {MAX_TRANSCRIPT_WORDS:,} words (original was longer)")
    if source.startswith("translated:"):
        warnings.append(f"Transcript auto-translated from {source.split(':')[1]}")
    if source == "auto-generated":
        warnings.append("Auto-generated captions — may contain errors")
    if source == "manual":
        warnings.append("Transcript provided manually by user")
    if meta.get("is_live"):
        warnings.append("This was a live stream — transcript may be incomplete")

    warning_block = ""
    if warnings:
        warning_block = "\nWARNINGS:\n" + "\n".join(f"  ! {w}" for w in warnings) + "\n"

    try:
        path.write_text(
            f"Title:        {meta['title']}\n"
            f"Channel:      {meta['channel']}\n"
            f"URL:          {meta['url']}\n"
            f"Video ID:     {meta['video_id']}\n"
            f"Views:        {meta['views']:,}\n"
            f"Duration:     {meta['duration']}s\n"
            f"Upload date:  {meta['upload_date']}\n"
            f"Topic folder: {topic}\n"
            f"Transcript:   {source}\n"
            f"Analyzed:     {date}\n"
            + warning_block
            + f"\n{'='*60}\nTRANSCRIPT\n{'='*60}\n\n"
            + transcript,
            encoding="utf-8",
        )
    except OSError as e:
        die(f"Could not write transcript file '{path}': {e}")

    return path


def update_readme(base: Path, meta: dict, topic: str, task_count: int) -> None:
    """Append a row to the Videos Analyzed table in README.md."""
    readme = base / "README.md"
    if not readme.exists():
        return

    content = readme.read_text(encoding="utf-8")

    date = datetime.now().strftime("%Y-%m-%d")
    title_md = f"[{meta['title']}]({meta['url']})"
    report_path = f"`reports/{topic}/{date}_{slugify(meta['title'])}_report.md`"
    new_row = f"| {date} | {title_md} | {meta['channel']} | {report_path} | {task_count} pending |\n"

    # Find the table separator line and insert after the last row
    if "| —" in content:
        # Replace the empty placeholder row
        content = content.replace(
            "| —    | —     | —      | —     |\n",
            new_row,
        )
    else:
        # Append after last row in the table
        lines = content.splitlines(keepends=True)
        table_end = None
        in_table = False
        for i, line in enumerate(lines):
            if "| Date |" in line:
                in_table = True
            if in_table and line.strip() == "":
                table_end = i
                break
        if table_end:
            lines.insert(table_end, new_row)
            content = "".join(lines)

    try:
        readme.write_text(content, encoding="utf-8")
    except OSError as e:
        warn(f"Could not update README.md: {e}")

# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="YouTube Analyzer — fetch transcript and metadata for Claude Code analysis"
    )
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Base output directory (default: same folder as this script)",
    )
    parser.add_argument(
        "--no-readme-update",
        action="store_true",
        help="Skip updating README.md",
    )
    args = parser.parse_args()

    base = (args.output_dir or Path(__file__).parent).resolve()
    url = args.url

    # ── Validate URL ──────────────────────────────────────────────────────────
    if not re.search(r"(youtube\.com|youtu\.be)", url):
        die(f"Not a YouTube URL: {url}")

    video_id = extract_video_id(url)

    # ── Deduplication ─────────────────────────────────────────────────────────
    existing = find_existing_transcript(base, video_id)
    if existing:
        print(f"[SKIP] Already analyzed: {existing.relative_to(base)}")
        print("       Delete that file or use a different --output-dir to re-analyze.")
        sys.exit(0)

    # ── Step 1: Metadata ──────────────────────────────────────────────────────
    print("[1/5] Fetching metadata...", flush=True)
    meta = get_metadata(url)
    print(f"      Title   : {meta['title']}")
    print(f"      Channel : {meta['channel']}")
    print(f"      Views   : {meta['views']:,}")
    print(f"      Duration: {meta['duration']}s")
    if meta.get("is_live"):
        warn("This is a live stream — transcript may be incomplete or unavailable.")

    # ── Step 2: Transcript ────────────────────────────────────────────────────
    print("[2/5] Fetching transcript...", flush=True)
    transcript, source = get_transcript(meta["video_id"])
    transcript, was_truncated = truncate_transcript(transcript)
    word_count = len(transcript.split())
    print(f"      Words   : {word_count:,}  (source: {source})")
    if was_truncated:
        warn(f"Transcript truncated to {MAX_TRANSCRIPT_WORDS:,} words to avoid context overflow.")

    # ── Step 3: Classify ──────────────────────────────────────────────────────
    print("[3/5] Classifying topic...", flush=True)
    topic = classify_topic(meta["title"], meta["description"])
    print(f"      Topic   : {topic}")

    # ── Step 4: Save ──────────────────────────────────────────────────────────
    print("[4/5] Saving transcript...", flush=True)
    path = save_transcript(base, meta, transcript, topic, source, was_truncated)
    print(f"      Saved   : {path.relative_to(base)}")

    # ── Step 5: Update README ─────────────────────────────────────────────────
    if not args.no_readme_update:
        print("[5/5] Updating README.md index...", flush=True)
        update_readme(base, meta, topic, task_count=0)
        print("      Done.")

    # ── Output for Claude ─────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("METADATA (for Claude analysis)")
    print("=" * 60)
    print(json.dumps({k: v for k, v in meta.items() if k != "description"}, indent=2))
    print(f'\n  "description_preview": {json.dumps(meta["description"][:200])}')

    print("\n" + "=" * 60)
    print(f"FULL TRANSCRIPT ({word_count:,} words | source: {source})")
    if was_truncated:
        print(f"  ⚠ Truncated at {MAX_TRANSCRIPT_WORDS:,} words")
    print("=" * 60)
    print(transcript)


if __name__ == "__main__":
    main()
