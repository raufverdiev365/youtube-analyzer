# Task Backlog

All actionable tasks extracted from analyzed YouTube videos.

## Format
`- [x] done` / `- [ ] todo` — `[SOURCE: slug]` `<task>`

---

## From: 32-tricks-nate-herk (2026-05-20)

### Infrastructure (implement now)
- [x] [SOURCE: 32-tricks-nate-herk] Add macOS notification Stop hook to ~/.claude/settings.json so a sound fires when any Claude session finishes
- [x] [SOURCE: 32-tricks-nate-herk] Add explicit deny list for destructive bash commands to settings.json (rm -rf, git reset --hard, git push --force, DROP TABLE, truncate)

### CLAUDE.md Habits (add to global CLAUDE.md)
- [ ] [SOURCE: 32-tricks-nate-herk] Add reminder: run /init on every new project before starting work
- [ ] [SOURCE: 32-tricks-nate-herk] Add reminder: compact at 60% context — use `/compact but keep <key decisions>`
- [ ] [SOURCE: 32-tricks-nate-herk] Add reminder: exit early + re-ask if Claude goes wrong path (don't let it finish)
- [ ] [SOURCE: 32-tricks-nate-herk] Add reminder: after each session, log new patterns/gotchas back into project CLAUDE.md
- [ ] [SOURCE: 32-tricks-nate-herk] Add reminder: use ultrathink for architecture decisions and when 2 tries haven't worked

### Documentation / Reference
- [ ] [SOURCE: 32-tricks-nate-herk] Document API-endpoint-vs-MCP principle: when only 1 endpoint needed, hardcode it instead of loading full MCP
- [ ] [SOURCE: 32-tricks-nate-herk] Document sub-agent model selection pattern: Haiku for bulk reads/scrapes, Sonnet/Opus for main thread
- [ ] [SOURCE: 32-tricks-nate-herk] Document screenshot loop pattern for frontend: design → screenshot → revise → 3 passes before V1

### Already Done (tracked for reference)
- [x] [SOURCE: 32-tricks-nate-herk] Custom skills library (hack #12) — extensive library in ~/.claude/skills/
- [x] [SOURCE: 32-tricks-nate-herk] Sub-agents for parallel work (hack #11) — dispatching-parallel-agents.md skill
- [x] [SOURCE: 32-tricks-nate-herk] Haiku for sub-agents (hack #13) — subagent-driven-development.md skill
- [x] [SOURCE: 32-tricks-nate-herk] Chrome DevTools via Playwright MCP (hack #21)
- [x] [SOURCE: 32-tricks-nate-herk] Git worktrees skill (hack #23) — using-git-worktrees.md
- [x] [SOURCE: 32-tricks-nate-herk] Context7 MCP active by default (hack #32)
- [x] [SOURCE: 32-tricks-nate-herk] Verification before completion (hack #10) — verification-before-completion.md skill
