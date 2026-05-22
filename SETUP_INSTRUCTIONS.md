# YouTube Analyzer — Full Setup Instructions
## Recreate on any PC with Antigravity + Claude Code

---

## What This System Does

You give it a YouTube URL. It:
1. Fetches metadata (title, channel, views, duration) via `yt-dlp`
2. Fetches the full transcript via `youtube-transcript-api`
3. Auto-classifies the topic → saves to the right subfolder
4. You drop the output back to Claude Code for analysis
5. Claude extracts best practices, anti-patterns, tool tips
6. Tasks are written to `tasks/backlog.md`
7. Infrastructure tasks get executed immediately (settings changes, installs, etc.)
8. A full report is generated per video

---

## Prerequisites

### 1. Python 3 + pip
```bash
python3 --version   # must be 3.8+
pip3 --version
```

### 2. Install the two core libraries
```bash
pip3 install yt-dlp youtube-transcript-api
```

Verify:
```bash
python3 -c "import yt_dlp; print('yt-dlp OK')"
python3 -c "from youtube_transcript_api import YouTubeTranscriptApi; print('transcript API OK')"
```

### 3. Claude Code CLI
Must be installed and authenticated. Test with:
```bash
claude --version
```

---

## Folder Structure to Create

Run this block in your terminal from inside `antigravity/`:

```bash
mkdir -p research/youtube_analyzer/{transcripts,analysis,tasks,reports,templates}
```

This gives you:
```
antigravity/
└── research/
    └── youtube_analyzer/
        ├── CLAUDE.md              ← tells Claude how to run the workflow
        ├── README.md              ← index of all analyzed videos
        ├── analyze.py             ← CLI tool: paste URL → get transcript
        ├── transcripts/           ← raw transcripts (auto-subfoldered by topic)
        ├── analysis/              ← extracted insights per video
        ├── tasks/
        │   └── backlog.md         ← all actionable tasks from all videos
        ├── reports/               ← final report per video
        └── templates/
            ├── analysis_template.md
            └── report_template.md
```

---

## File 1: `analyze.py`

Save this as `research/youtube_analyzer/analyze.py`:

```python
#!/usr/bin/env python3
"""
YouTube Analyzer — one-command pipeline.
Usage: python3 analyze.py <youtube_url>
"""

import sys
import re
import json
from datetime import datetime
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    sys.exit("Run: pip3 install yt-dlp")

try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    sys.exit("Run: pip3 install youtube-transcript-api")

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


def extract_video_id(url):
    for p in [r"youtu\.be/([a-zA-Z0-9_-]{11})", r"v=([a-zA-Z0-9_-]{11})"]:
        m = re.search(p, url)
        if m:
            return m.group(1)
    sys.exit(f"Could not extract video ID from: {url}")


def get_metadata(url):
    with yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True}) as ydl:
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


def get_transcript(video_id):
    api = YouTubeTranscriptApi()
    snippets = list(api.fetch(video_id))
    return " ".join(s.text.replace("\n", " ") for s in snippets)


def classify_topic(title, description):
    text = (title + " " + description).lower()
    scores = {t: sum(1 for kw in kws if kw in text) for t, kws in TOPIC_KEYWORDS.items()}
    best = max(scores, key=lambda t: scores[t])
    return best if scores[best] > 0 else "general"


def slugify(text):
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[\s_-]+", "-", text).strip("-")[:60]


def save_transcript(meta, transcript, topic):
    date = datetime.now().strftime("%Y-%m-%d")
    slug = slugify(meta["title"])
    folder = BASE / "transcripts" / topic
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{date}_{slug}.txt"
    path.write_text(
        f"Title: {meta['title']}\nChannel: {meta['channel']}\nURL: {meta['url']}\n"
        f"Views: {meta['views']:,}\nDuration: {meta['duration']}s\n"
        f"Upload date: {meta['upload_date']}\nTopic folder: {topic}\n"
        f"Analyzed: {date}\n\n{'='*60}\nTRANSCRIPT\n{'='*60}\n\n" + transcript
    )
    return path


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 analyze.py <youtube_url>")
        sys.exit(1)
    url = sys.argv[1]
    print("[1/4] Fetching metadata...")
    meta = get_metadata(url)
    print(f"      Title   : {meta['title']}")
    print(f"      Channel : {meta['channel']}")
    print(f"      Views   : {meta['views']:,}")
    print("[2/4] Fetching transcript...")
    transcript = get_transcript(meta["video_id"])
    print(f"      Words   : {len(transcript.split()):,}")
    print("[3/4] Classifying topic...")
    topic = classify_topic(meta["title"], meta["description"])
    print(f"      Topic   : {topic}")
    print("[4/4] Saving transcript...")
    path = save_transcript(meta, transcript, topic)
    print(f"      Saved   : {path.relative_to(BASE)}")
    print("\n" + "="*60 + "\nMETADATA JSON\n" + "="*60)
    print(json.dumps(meta, indent=2))
    print("\n" + "="*60 + "\nFULL TRANSCRIPT\n" + "="*60)
    print(transcript)


if __name__ == "__main__":
    main()
```

---

## File 2: `CLAUDE.md`

Save as `research/youtube_analyzer/CLAUDE.md`:

```markdown
# YouTube Analyzer — Claude Code Best Practices

## Project Purpose
Analyze YouTube videos about Claude Code best practices. For each video:
1. Accept the transcript (user pastes or provides it)
2. Extract actionable best practices, tips, and patterns
3. Break findings into discrete tasks
4. Generate a structured report
5. Execute infrastructure tasks immediately (settings changes, installs, etc.)

## Workflow

### Step 1 — Ingest
Save raw transcripts to `transcripts/<topic>/<date>_<slug>.txt`.

### Step 2 — Analysis
Save to `analysis/<topic>/<date>_<slug>.md`.
Extract: key practices, anti-patterns, tool tips, quotes.
Cross-check against what's already configured in ~/.claude/settings.json and ~/.claude/skills/.

### Step 3 — Tasks
Append to `tasks/backlog.md`:
`- [ ] [SOURCE: slug] <actionable task>`

### Step 4 — Execute
For tasks that are infrastructure (settings, installs, config):
execute them immediately in this same session.
Mark as `[x]` when done.

### Step 5 — Report
Save to `reports/<topic>/<date>_<slug>_report.md`.
Include: what was already set up, what was fixed this session,
what needs behavioral change, recommended follow-up.

## Focus Areas
- Claude Code CLI patterns and commands
- Prompt engineering for coding tasks
- Agent workflows and sub-agent patterns
- Tool use and MCP configuration
- Memory and context management
- Cost and token optimization
- Permissions and safety configuration
```

---

## File 3: `tasks/backlog.md`

Create `research/youtube_analyzer/tasks/backlog.md`:

```markdown
# Task Backlog

All actionable tasks extracted from analyzed YouTube videos.

## Format
`- [x] done` / `- [ ] todo` — `[SOURCE: slug]` `<task>`

---
<!-- Tasks appended here as videos are analyzed -->
```

---

## File 4: `templates/analysis_template.md`

```markdown
# Analysis: {VIDEO_TITLE}

**URL:** {URL}
**Date Analyzed:** {DATE}
**Transcript:** `transcripts/{TOPIC}/{SLUG}.txt`

---

## Summary

## Status Against Current Setup
### ✅ Already Implemented
### ❌ Not Implemented — High Priority
### ⚠️ Partially Done / Behavioral

## Key Practices
1.
2.

## Anti-Patterns / Mistakes to Avoid
-

## Tool & Workflow Tips
-

## Notable Quotes
>

## Priority Rating
**Signal strength:** High / Medium / Low
**Reason:**
```

---

## File 5: `templates/report_template.md`

```markdown
# Report: {VIDEO_TITLE}

**Date:** {DATE}
**Video URL:** {URL}

---

## Executive Summary

## What Was Already Set Up
| Hack | Feature |
|------|---------|

## What Was Fixed This Session
### [Change name]
Description of what was changed and why.

## Practices to Internalize
| # | Practice | Why |

## Tasks Generated
N tasks added to `tasks/backlog.md`. N done, N remaining.

## Recommended Follow-Up
- [ ]
```

---

## Claude Code Settings Changes

These go in `~/.claude/settings.json`. Open it and add:

### A) Notification Hook (fires macOS sound when Claude session ends)

Add inside the top-level JSON object:

```json
"hooks": {
  "Stop": [
    {
      "hooks": [
        {
          "type": "command",
          "command": "osascript -e 'display notification \"Claude session finished\" with title \"Claude Code\" sound name \"Glass\"'"
        }
      ]
    }
  ]
}
```

**Why:** Lets you run 15 sessions in parallel. The Glass chime tells you which one needs input without babysitting every terminal.

### B) Destructive Command Deny List

Add inside `"permissions"`:

```json
"deny": [
  "Bash(rm -rf /*)",
  "Bash(rm -rf ~/*)",
  "Bash(git reset --hard *)",
  "Bash(git push --force *)",
  "Bash(git push -f *)",
  "Bash(git branch -D *)"
]
```

**Why:** You're running with `bypassPermissions` for speed, but deny list intercepts catastrophic commands. Deny always overrides allow — same autonomy, zero blast radius.

> **Note for Linux/Windows:** Replace the `osascript` notification command with:
> - Linux: `notify-send "Claude Code" "Session finished"`
> - Windows: `powershell -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show('Done')"`

---

## The Full Workflow (Day-to-Day Use)

### Step 1 — Run the pipeline script
```bash
cd /path/to/antigravity/research/youtube_analyzer
python3 analyze.py https://youtu.be/VIDEO_ID
```

This prints metadata + full transcript to stdout AND saves the transcript file.

### Step 2 — Open Claude Code in the youtube_analyzer folder
```bash
claude
```
The CLAUDE.md loads automatically, telling Claude exactly what to do.

### Step 3 — Paste the script output to Claude
Just say: **"analyze this"** and paste the transcript output.

Or for a direct URL workflow, just say:
> "Analyze this video: https://youtu.be/VIDEO_ID"

Claude will run the script, read the transcript, and execute the full pipeline.

### Step 4 — Claude delivers
- `analysis/<topic>/` — extracted insights, status against current setup
- `tasks/backlog.md` — new tasks appended
- Infrastructure tasks executed immediately in-session
- `reports/<topic>/` — final report

---

## Topic Auto-Classification

Videos are automatically sorted into subfolders:

| Folder | Trigger keywords |
|--------|-----------------|
| `tips-tricks` | hack, trick, tip, level up, shortcut, workflow |
| `agents` | agent, sub-agent, multi-agent, agentic, autonomous |
| `mcp` | mcp, model context protocol, tool use |
| `prompting` | prompt, prompting, system prompt, context |
| `cost-optimization` | cost, token, cheap, haiku, budget, optimize |
| `setup` | install, setup, config, getting started |
| `tools` | tool, cli, extension, plugin, integration |
| `general` | (fallback) |

---

## What Was Extracted From the First Video

**Video:** "32 Tricks to Level Up Claude Code in 16 Mins" — Nate Herk (252k views)
**Date:** 2026-05-20

### Top 10 practices extracted:
1. `/compact` at 60% context — use `/compact but keep <key decisions>`
2. Always start in plan mode (Shift+Tab) — reads/researches without modifying anything
3. Keep CLAUDE.md lean (150–200 lines max) — route to other files for detail
4. Sub-agents on Haiku for bulk reads, Sonnet/Opus on main thread
5. Notification hook — enables true parallel multi-session work
6. Explicit deny list — same speed as `dangerously-skip-permissions`, no blast radius
7. `ultrathink` — 32k token thinking budget for architecture decisions
8. Git worktrees for parallel features — `claude --worktree feature-name`
9. Context7 MCP — live library docs, prevents hallucinated/deprecated APIs
10. Screenshot loop for frontend — design → screenshot → revise → 3 passes before V1

### Tasks executed in session:
- ✅ Added macOS notification Stop hook to `~/.claude/settings.json`
- ✅ Added destructive command deny list to `~/.claude/settings.json`

---

## Existing Skills Already in Place (don't recreate)

If you're on the same Antigravity setup, these are already available in `~/.claude/skills/`:

| Skill file | What it does |
|-----------|-------------|
| `dispatching-parallel-agents.md` | Sub-agent orchestration |
| `subagent-driven-development.md` | Haiku for sub-agents pattern |
| `verification-before-completion.md` | Self-checking todos |
| `using-git-worktrees.md` | Parallel Claude sessions |
| `youtube-outliers.md` | YouTube research/transcript pipeline |
| `youtube-clipper.md` | Video download + subtitle extraction |
| `summarizing-youtube-videos.md` | Video summarization |

And these MCPs are active by default:
- `context7` — live library documentation
- `playwright` — Chrome DevTools / browser automation
- `github-mcp-server` — GitHub operations

---

## Quick Start Checklist

```
[ ] pip3 install yt-dlp youtube-transcript-api
[ ] mkdir -p antigravity/research/youtube_analyzer/{transcripts,analysis,tasks,reports,templates}
[ ] Create analyze.py (see File 1 above)
[ ] Create CLAUDE.md (see File 2 above)
[ ] Create tasks/backlog.md (see File 3 above)
[ ] Create templates/analysis_template.md (see File 4 above)
[ ] Create templates/report_template.md (see File 5 above)
[ ] Add hooks + deny list to ~/.claude/settings.json (see Settings section)
[ ] Test: python3 analyze.py https://youtu.be/jqoFP9QapXI
[ ] Open Claude Code in the folder: cd youtube_analyzer && claude
[ ] Say "analyze this" and paste the output
```

---

## File Path Reference (relative to antigravity/)

```
research/youtube_analyzer/
├── analyze.py
├── CLAUDE.md
├── README.md
├── tasks/backlog.md
├── transcripts/{topic}/{date}_{slug}.txt
├── analysis/{topic}/{date}_{slug}.md
├── reports/{topic}/{date}_{slug}_report.md
└── templates/
    ├── analysis_template.md
    └── report_template.md
```

---

*Generated: 2026-05-21 | Source machine: macOS (Darwin 25.5.0) | Claude Code: claude-sonnet-4-6*
