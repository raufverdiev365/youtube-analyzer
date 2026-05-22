# Analysis: 32 Tricks to Level Up Claude Code in 16 Mins

**URL:** https://youtu.be/jqoFP9QapXI
**Channel:** Nate Herk | AI Automation
**Date Analyzed:** 2026-05-20
**Views:** 252,738
**Transcript:** `transcripts/tips-tricks/2026-05-20_32-tricks-to-level-up-claude-code-in-16-mins.txt`

---

## Summary
Nate Herk covers 32 practical Claude Code hacks from beginner to advanced, organized by experience level. The video is highly practical with specific commands, rationale for each, and real workflow examples. Signal density is very high — almost every tip is immediately actionable.

---

## Status Against Current Setup

### ✅ Already Implemented
| # | Hack | Evidence |
|---|------|----------|
| 10 | Self-checking in todos | `verification-before-completion.md` skill exists |
| 11 | Sub-agents for parallel work | `dispatching-parallel-agents.md` + `subagent-driven-development.md` skills |
| 12 | Custom skills | Extensive skills library in `~/.claude/skills/` |
| 13 | Haiku for sub-agents | `subagent-driven-development.md` covers this |
| 21 | Chrome DevTools | `playwright` MCP is in default MCPs |
| 23 | Git worktrees | `using-git-worktrees.md` skill exists |
| 32 | Context7 MCP | `context7` is in the default MCPs list |

### ❌ Not Implemented — High Priority
| # | Hack | Gap |
|---|------|-----|
| 19 | Notification hook when Claude stops | `hooks: {}` — empty, no Stop hook |
| 30 | Explicit deny list for destructive commands | Using `bypassPermissions` + `skipDangerousModePermissionPrompt: true` with no deny list |

### ⚠️ Partially Done / Behavioral
| # | Hack | Notes |
|---|------|-------|
| 1 | /init on every project | No habit documented in CLAUDE.md — needs reminder |
| 6 | Compact at 60%, clear between tasks | Not enforced anywhere |
| 14 | Keep CLAUDE.md fresh per session | Not in global CLAUDE.md as an instruction |
| 15 | CLAUDE.md routes to other files | Global CLAUDE.md is lean but per-project CLAUDEs could use this pattern |
| 16 | Exit early + re-ask | Behavioral — worth adding to CLAUDE.md |
| 24 | API endpoints vs MCP servers | Good principle, not documented anywhere |
| 29 | ultrathink | Documented in Claude's training; no project-level reminder |

---

## Key Practices

1. **Plan before acting** — Use plan mode (Shift+Tab) for every non-trivial task. It reads/researches but doesn't modify. Switch to execute only after approving.
2. **Compact at 60%** — Don't let context bloat. `/compact` with selective preservation, e.g. `/compact but keep API decisions`.
3. **CLAUDE.md stays lean (150–200 lines)** — Anything beyond that bloats the system prompt. Route to other files instead.
4. **Sub-agents on Haiku for bulk reads** — Main session on Opus/Sonnet, sub-agents on Haiku when they're just reading/scraping/summarizing.
5. **Notification hooks** — Set a `Stop` hook to fire an OS notification. Enables running 15 sessions in parallel and knowing when each needs input.
6. **Explicit permissions > dangerously skip** — Add deny list for `rm -rf`, `git reset --hard`, `DROP TABLE`. Keeps speed, removes blast radius.
7. **ultrathink for hard decisions** — 32k token thinking budget. Use for architecture, complex debugging, when first 2 tries fail.
8. **Git worktrees for parallel features** — `claude --worktree feature-name` spawns isolated branch. Merge back when done.
9. **Context7 MCP** — Always active, pulls live library docs to prevent hallucinated/deprecated API usage.
10. **/loop for recurring checks** — Every N minutes, monitor a PR, deployment, logs. Self-pacing or interval-based.

## Anti-Patterns / Mistakes to Avoid

- **Dumping entire codebase into context** — Only give Claude what the current task needs.
- **Waiting for Claude to finish a wrong path** — Hit Escape early, correct, re-prompt.
- **Accepting mediocre first output** — Push back aggressively. "Scrap that. More elegant approach."
- **Using MCP servers when only 1 endpoint is needed** — Loads all tool definitions = token waste. Hardcode the endpoint.
- **dangerously-skip-permissions with no deny list** — Fast but risky. Add explicit denies for destructive commands.
- **Never updating CLAUDE.md** — Patterns, gotchas, new conventions discovered in session should be written back.

## Notable Quotes

> "Every token that it spends going the wrong direction is just wasted context. So steer tight and steer early."

> "You can actually get to the point where you have the same exact speed and autonomy of dangerously skip permissions without it being very dangerous."

> "The V1 that it gives me [after 3 screenshot passes] is so much better than a V1 that it used to give me."

## Priority Rating
**Signal strength:** High
**Reason:** 32 specific, command-level tips. 7 are already implemented here. 2 are infrastructure gaps that can be fixed right now (hook + permissions). The rest are behavioral habits worth encoding into CLAUDE.md.
