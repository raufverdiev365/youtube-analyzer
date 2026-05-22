# Report: 32 Tricks to Level Up Claude Code in 16 Mins

**Date:** 2026-05-20
**Video URL:** https://youtu.be/jqoFP9QapXI
**Channel:** Nate Herk | AI Automation
**Views:** 252,738 | **Duration:** 16 min
**Analysis file:** `analysis/tips-tricks/2026-05-20_32-tricks-nate-herk.md`

---

## Executive Summary
Nate Herk presents 32 Claude Code hacks organized beginner → intermediate → advanced. The video is highly practical: every tip includes a specific command, rationale, and workflow example. 7 of the 32 hacks were already implemented in this setup. 2 infrastructure gaps were fixed immediately during this session. The remaining gaps are behavioral habits that need to be internalized, not installed.

---

## What Was Already Set Up (7/32)

| Hack | Feature |
|------|---------|
| #10 | Verification before completion (`verification-before-completion.md` skill) |
| #11 | Sub-agents for parallel work (`dispatching-parallel-agents.md`) |
| #12 | Custom skills (extensive library in `~/.claude/skills/`) |
| #13 | Haiku for sub-agents (`subagent-driven-development.md`) |
| #21 | Chrome DevTools via Playwright MCP |
| #23 | Git worktrees (`using-git-worktrees.md`) |
| #32 | Context7 MCP active by default |

---

## What Was Fixed This Session (2/32)

### Hack #19 — Notification Hook
Added `Stop` hook to `~/.claude/settings.json` that fires a macOS Glass sound + notification when any Claude session finishes. Enables running 15 sessions in parallel — the chime tells you which one needs input without babysitting terminals.

### Hack #30 — Destructive Command Deny List
Added explicit `deny` rules to `~/.claude/settings.json` for:
- `rm -rf /*` and `rm -rf ~/*`
- `git reset --hard *`
- `git push --force *` / `git push -f *`
- `git branch -D *`

`bypassPermissions` default is kept for speed, but the deny list intercepts anything catastrophic. Deny always overrides allow.

---

## Top Practices to Internalize (Behavioral)

| # | Practice | Why |
|---|----------|-----|
| 6 | `/compact` at 60% context | Prevents context rot; use `/compact but keep <decisions>` |
| 7 | Start in plan mode (Shift+Tab) | Claude reads/researches without changing anything; dramatically better quality |
| 14 | Update CLAUDE.md each session | Log new patterns, gotchas, conventions discovered during the session |
| 15 | Route CLAUDE.md to other files | Keep it under 150 lines; point to style guides / reference docs instead of embedding them |
| 16 | Exit early + re-ask | Don't wait for Claude to finish going the wrong way |
| 17 | Challenge outputs aggressively | "Scrap that. More elegant approach." — second try is often dramatically better |
| 29 | `ultrathink` for hard problems | 32k token thinking budget; use for architecture, complex debug, when 2 tries fail |

---

## Tasks Generated
9 tasks added to `tasks/backlog.md`. 2 marked done (infrastructure). 7 remain as behavioral/documentation work.

---

## Key Insight for This Setup
The setup is already at an advanced level (skills, worktrees, sub-agents, Context7). The main unlocks from this video are:
1. **Notification hook** (done) — enables true parallel multi-session work
2. **Deny list** (done) — removes the only real risk of `bypassPermissions`
3. **CLAUDE.md discipline** — keeping it lean and routing to files is the highest-leverage behavioral change

---

## Recommended Follow-Up
- [ ] Add 3-line habit reminder to global CLAUDE.md: compact at 60%, plan mode first, update CLAUDE.md after session
- [ ] Test the notification hook by finishing a session — should hear Glass chime
- [ ] Watch the follow-up video from same channel on agent teams (hack #31 deep-dive)
