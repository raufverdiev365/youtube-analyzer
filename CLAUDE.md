# YouTube Analyzer — Claude Code Best Practices

## Project Purpose
Analyze YouTube videos about Claude Code best practices. For each video:
1. Accept the transcript (user pastes or provides it)
2. Extract actionable best practices, tips, and patterns
3. Break findings into discrete tasks
4. Generate a structured report

## Workflow

### Step 1 — Ingest Transcript
Save raw transcripts to `transcripts/<video_id_or_slug>.txt`.
Include video title, URL, and date at the top of each file.

### Step 2 — Analysis
Run analysis → save to `analysis/<slug>.md`.
Extract: key practices, anti-patterns, tool tips, workflow patterns, quotes.

### Step 3 — Tasks
For each actionable insight, create a task entry in `tasks/backlog.md`.
Format: `- [ ] [SOURCE: slug] <actionable task>`

### Step 4 — Report
Compile findings → `reports/<date>_<slug>_report.md`.
Report must include: summary, key practices, tasks generated, priority rating.

## File Naming
- Transcripts: `transcripts/YYYY-MM-DD_<slug>.txt`
- Analysis: `analysis/YYYY-MM-DD_<slug>.md`
- Reports: `reports/YYYY-MM-DD_<slug>_report.md`
- Tasks: always appended to `tasks/backlog.md`

## Focus Areas
When analyzing videos, prioritize extracting insights about:
- Claude Code CLI usage patterns
- Prompt engineering for coding tasks
- Agent workflows and multi-step tasks
- Tool use and MCP configuration
- Memory and context management
- Cost/token optimization
- Common mistakes to avoid
