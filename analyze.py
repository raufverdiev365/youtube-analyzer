#!/usr/bin/env python3
"""
YouTube Analyzer — one-command pipeline for Claude Code best-practices research.

Usage:
    python3 analyze.py <youtube_url>

Steps:
    1. Fetch metadata via yt-dlp
    2. Fetch transcript via youtube-transcript-api
    3. Classify topic → choose target subfolder
    4. Save transcript + metadata
    5. Print full transcript so Claude can analyze inline
"""

import sys
import re
import json
import textwrap
from datetime import datetime
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    sys.exit("yt-dlp not installed. Run: pip3 install yt-dlp")

try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    sys.exit("youtube-transcript-api not installed. Run: pip3 install youtube-transcript-api")

BASE = Path(__file__).parent

TOPIC_KEYWORDS = {
    "tips-tricks": ["hack", "trick", "tip", "level up", "cheat", "shortcut", "workflow"],
    "agents": ["agent", "sub-agent", "multi-agent", "agentic", "autonomous"],
    "mcp": ["mcp", "model context protocol", "server", "tool use"],
    "prompting": ["prompt", "prompting", "instruction", "system prompt", "context"],
    "cost-optimization": ["cost", "token", "cheap", "haiku", "budget", "optimize"],
    "setup": ["install", "setup", "config", "getting started", "beginners"],
    "tools": ["tool", "cli", "extension", "plugin", "integration"],
}


def extract_video_id(url: str) -> str:
    patterns = [
        r"youtu\.be/([a-zA-Z0-9_-]{11})",
        r"v=([a-zA-Z0-9_-]{11})",
        r"embed/([a-zA-Z0-9_-]{11})",
    ]
    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1)
    sys.exit(f"Could not extract video ID from: {url}")


def get_metadata(url: str) -> dict:
    opts = {"quiet": True, "no_warnings": True}
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)
    return {
        "title": info.get("title", ""),
        "channel": info.get("channel", ""),
        "duration": info.get("duration", 0),
        "views": info.get("view_count", 0),
        "upload_date": info.get("upload_date", ""),
        "url": url,
        "video_id": info.get("id", ""),
        "description": info.get("description", "")[:600],
    }


def get_transcript(video_id: str) -> str:
    api = YouTubeTranscriptApi()
    snippets = list(api.fetch(video_id))
    return " ".join(s.text.replace("\n", " ") for s in snippets)


def classify_topic(title: str, description: str) -> str:
    text = (title + " " + description).lower()
    scores = {topic: 0 for topic in TOPIC_KEYWORDS}
    for topic, keywords in TOPIC_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                scores[topic] += 1
    best = max(scores, key=lambda t: scores[t])
    return best if scores[best] > 0 else "general"


def slugify(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[\s_-]+", "-", text).strip("-")[:60]


def save_transcript(meta: dict, transcript: str, topic: str) -> Path:
    date = datetime.now().strftime("%Y-%m-%d")
    slug = slugify(meta["title"])
    folder = BASE / "transcripts" / topic
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{date}_{slug}.txt"
    path.write_text(
        f"Title: {meta['title']}\n"
        f"Channel: {meta['channel']}\n"
        f"URL: {meta['url']}\n"
        f"Views: {meta['views']:,}\n"
        f"Duration: {meta['duration']}s\n"
        f"Upload date: {meta['upload_date']}\n"
        f"Topic folder: {topic}\n"
        f"Analyzed: {date}\n"
        f"\n{'='*60}\nTRANSCRIPT\n{'='*60}\n\n"
        + transcript
    )
    return path


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 analyze.py <youtube_url>")
        sys.exit(1)

    url = sys.argv[1]
    print(f"[1/4] Fetching metadata...")
    meta = get_metadata(url)
    print(f"      Title   : {meta['title']}")
    print(f"      Channel : {meta['channel']}")
    print(f"      Views   : {meta['views']:,}")

    print(f"[2/4] Fetching transcript...")
    transcript = get_transcript(meta["video_id"])
    print(f"      Words   : {len(transcript.split()):,}")

    print(f"[3/4] Classifying topic...")
    topic = classify_topic(meta["title"], meta["description"])
    print(f"      Topic   : {topic}")

    print(f"[4/4] Saving transcript...")
    path = save_transcript(meta, transcript, topic)
    print(f"      Saved   : {path.relative_to(BASE)}")

    print("\n" + "="*60)
    print("METADATA JSON (for analysis)")
    print("="*60)
    print(json.dumps(meta, indent=2))
    print("\n" + "="*60)
    print("FULL TRANSCRIPT")
    print("="*60)
    print(transcript)


if __name__ == "__main__":
    main()
