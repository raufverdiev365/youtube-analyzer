# YouTube Analyzer

Research project for extracting Claude Code best practices from YouTube videos.

## Structure

```
youtube_analyzer/
├── CLAUDE.md           ← Instructions for Claude on how to run the workflow
├── README.md           ← This file
├── transcripts/        ← Raw video transcripts (one file per video)
├── analysis/           ← Extracted insights per video
├── tasks/
│   └── backlog.md      ← All actionable tasks from all videos
├── reports/            ← Final report per video
└── templates/          ← Reusable templates for analysis and reports
```

## How to Use

1. Open a Claude Code session in this folder
2. Paste a YouTube transcript and say "analyze this"
3. Claude will follow the workflow in CLAUDE.md automatically
4. Check `reports/` for the output and `tasks/backlog.md` for action items

## Videos Analyzed

| Date | Video | Report | Tasks |
|------|-------|--------|-------|
| 2026-05-20 | [32 Tricks to Level Up Claude Code](https://youtu.be/jqoFP9QapXI) — Nate Herk | `reports/tips-tricks/2026-05-20_32-tricks-nate-herk_report.md` | 9 tasks (2 done) |
| 2026-06-10 | [How to Build Mobile Apps with Claude Code: Full Course](https://youtu.be/BMMcmmnjrM8) — Nick Saraev | `reports/2026-06-10_mobile-apps-claude-code-saraev_report.md` | 7 tasks (0 done) |
