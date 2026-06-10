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

---

## From: html-markdown-thariq (2026-05-26)

### Implement Now — Zero Friction
- [x] [SOURCE: html-markdown-thariq] Add to global CLAUDE.md: "For plans longer than 1 screen, generate HTML not Markdown"
- [x] [SOURCE: html-markdown-thariq] Add to global CLAUDE.md: "You are a compute allocator — spec quality determines output quality"
- [ ] [SOURCE: html-markdown-thariq] Create `templates/plan_template.html` — reusable HTML plan scaffold (sections: overview, types, mockups, file structure, verification criteria)

### High Priority
- [ ] [SOURCE: html-markdown-thariq] Update youtube_analyzer reports to generate `.html` versions alongside `.md` (richer, actually readable)
- [ ] [SOURCE: html-markdown-thariq] Create `~/.claude/skills/html-spec.md` skill — guides Claude through: brainstorm → interview → HTML plan → micro-app editing → clear context → implement
- [ ] [SOURCE: html-markdown-thariq] Create a living `design.html` file for any frontend work in antigravity (colors, typography, spacing, core components)
- [ ] [SOURCE: html-markdown-thariq] Add brainstorm step to youtube_analyzer CLAUDE.md: before analyzing, brainstorm extraction angles in HTML

### Behavioral / Reference
- [ ] [SOURCE: html-markdown-thariq] Add to CLAUDE.md: "Always give Claude an out with 'whatever is needed' — don't over-constrain with rigid skill instructions"
- [ ] [SOURCE: html-markdown-thariq] Document micro-app editing pattern: when a plan section needs editing, build throwaway HTML UI → edit visually → copy back
- [ ] [SOURCE: html-markdown-thariq] Add verification step to youtube_analyzer pipeline: after analysis, confirm tasks were actually written to backlog
- [ ] [SOURCE: html-markdown-thariq] Try weekly HTML status update pattern: Claude reads recent session outputs → generates HTML summary

### Already Done (tracked for reference)
- [x] [SOURCE: 32-tricks-nate-herk] Custom skills library (hack #12) — extensive library in ~/.claude/skills/
- [x] [SOURCE: 32-tricks-nate-herk] Sub-agents for parallel work (hack #11) — dispatching-parallel-agents.md skill
- [x] [SOURCE: 32-tricks-nate-herk] Haiku for sub-agents (hack #13) — subagent-driven-development.md skill
- [x] [SOURCE: 32-tricks-nate-herk] Chrome DevTools via Playwright MCP (hack #21)
- [x] [SOURCE: 32-tricks-nate-herk] Git worktrees skill (hack #23) — using-git-worktrees.md
- [x] [SOURCE: 32-tricks-nate-herk] Context7 MCP active by default (hack #32)
- [x] [SOURCE: 32-tricks-nate-herk] Verification before completion (hack #10) — verification-before-completion.md skill

## From: 2026-06-10_mobile-apps-claude-code-saraev (Apex Sales iOS buildout)
- [ ] [SOURCE: mobile-apps-saraev] Run a structured pre-submission security audit on the iOS app (tiered severity, CWE labels); fix; then re-run the same audit in a FRESH session to catch fix-introduced regressions. Start with: WebSocket token in URL path, keychain/token-refresh handling, PII in logs, ATS config.
- [ ] [SOURCE: mobile-apps-saraev] Add a hidden DEBUG-only dev/QA menu (reset onboarding, clear keychain+caches, seed demo data, jump to any v1 screen) to speed manual device validation.
- [ ] [SOURCE: mobile-apps-saraev] Sample-audit every FoundationModels prompt (SmartReplyBar, DailyBriefingView, AskAISheet): generate 10+ outputs each, tune prompts, regenerate before App Review.
- [ ] [SOURCE: mobile-apps-saraev] Performance pass: parallelize TasksStore's sequential per-communication detail fetches (TaskGroup w/ small concurrency cap); measure screen load times before/after.
- [ ] [SOURCE: mobile-apps-saraev] Close the design loop: feed docs/screenshots/2026-06-09-appstore-6.9 PNGs through Claude to enumerate cross-screen inconsistencies; fix as one batch.
- [ ] [SOURCE: mobile-apps-saraev] Add a "Post-launch" section to APP_STORE_CHECKLIST.md: ASC analytics review cadence, custom product pages, promo codes for early users.
- [ ] [SOURCE: mobile-apps-saraev] Borrow the core-loop reward idea: add haptic + visual confirmation on disposition-submit and task-complete (the app's two highest-frequency actions).
