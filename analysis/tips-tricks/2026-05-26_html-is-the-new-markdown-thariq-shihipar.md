# Analysis: Why this Claude Code engineer uses HTML files as AI specs

**URL:** https://youtu.be/Qrpm7E80wQ0
**Channel:** How I AI (interview with Thariq Shihipar, Anthropic Claude Code team)
**Date Analyzed:** 2026-05-26
**Views:** 71,355 | **Duration:** 36 min
**Transcript:** `transcripts/tips-tricks/2026-05-26_why-this-claude-code-engineer-uses-html-files-as-ai-specs-th.txt`

---

## Summary
Thariq Shihipar, an engineer on the Claude Code team at Anthropic, argues that HTML has replaced Markdown as the right format for specs, plans, PRDs, and any document you want to meaningfully interact with alongside Claude. The core thesis: as agents run longer and plans grow larger, Markdown becomes unreadable — and if you stop reading, you stop editing, and quality collapses. HTML forces you back into the loop. This is a first-party signal from inside Anthropic's Claude Code team, making it extremely high-value.

---

## Status Against Current Setup

### ❌ Not Implemented — High Priority
| Practice | Gap |
|----------|-----|
| HTML specs/plans instead of Markdown | All current reports, CLAUDE.md, backlog, templates are .md |
| Brainstorm in HTML | No brainstorm step in the current pipeline at all |
| Micro-apps for editing plan sections | Not in workflow |
| Living design system as HTML file | Not present anywhere in antigravity |
| HTML plans as context artifact passed to implementation | Using raw .md + transcript output |
| Verification ≠ testing (synthetic data CLI runs) | No verification step in pipeline |

### ✅ Already Implemented
| Practice | Evidence |
|----------|----------|
| Interview yourself / ask Claude questions before planning | `verification-before-completion.md` skill, plan mode |
| Clear context between plan and implementation | CLAUDE.md instructs `/clear` between tasks |
| Type interfaces as spec anchors | N/A (no frontend work currently in youtube_analyzer) |

### ⚠️ Partially Done
| Practice | Notes |
|----------|-------|
| You are a compute allocator | Not explicitly in CLAUDE.md; should be a mindset reminder |
| Don't over-constrain Claude | Our skills library is extensive — worth auditing for over-built prompts |

---

## Key Practices

1. **HTML over Markdown for all planning artifacts**
   Markdown plans get so long you stop reading them → you stop editing → you accept mediocre output. HTML forces engagement. Claude is equally good at both but HTML is much richer: scrollable, visual mockups, collapsible sections, real diagrams instead of ASCII art.

2. **Brainstorm in HTML, not bullet lists**
   Prompt: *"Brainstorm me some ideas in an HTML file."* You get a visual grid of options with mockups, risks, descriptions — all scannable at a glance. "I'm not going to read longer output than fits on screen in Claude Code." HTML fixes this.

3. **Interview yourself before writing the plan**
   Before generating an HTML plan, ask Claude to interview you until it understands the goal. This surfaces unknown unknowns before they become bugs.

4. **HTML plan = maximum context document**
   The plan should include: file structure, type interfaces, mock-ups, code excerpts, logic overview, component previews. Prompt pattern: *"Create an HTML file as a plan. Include excerpts, mock-ups, code, whatever is needed to give me maximum context."* — then add *"whatever is needed"* as an escape hatch so Claude doesn't over-interpret.

5. **Micro-apps for editing specific plan sections**
   If a table or section in the plan needs refinement, don't edit it in the terminal. Ask Claude to build a throwaway HTML UI for just that section. Edit visually, copy the output, bop it back into the plan. "This is micro-software on top of micro-software."

6. **Type interfaces as spec bookends**
   Define data model types and validation criteria as the two bookends of the spec. Everything in the middle is easier to execute when these are pinned.

7. **Verification ≠ Testing**
   Verification can be: a rubric, a recorded video of what Claude did, a CLI run through synthetic data. Keep a synthetic data set. Run it through the CLI after each session. If it handles old breakages, you've moved forward.

8. **Living design system as `design.html`**
   Store design system (colors, typography, spacing, core components) as a single HTML file. Pass `design.html` to new projects. Claude can auto-extract a design system from a repo and produce this file. "Design.md is dead. Long live design.html."

9. **Weekly status updates in HTML**
   Ask Claude to read your Slack messages → generate a weekly HTML status update for your manager. Actually gets read.

10. **Clear context → pass HTML plan as artifact**
    After plan approval: clear context, then "Here's a plan. Implement it." The HTML plan is the handoff document.

---

## Anti-Patterns / Mistakes to Avoid

- **Reading 1000-line Markdown files** — you stop reading, stop editing, stop caring about quality
- **Over-built skills** — "You're an expert planner and you must always..." constrains Claude and outsources judgment. Give Claude room + a trust signal ("whatever is needed")
- **Yelling at or being harsh with Claude** — activates different internal features; reasoning traces become "sad"; you get worse output
- **Spec format driven by tooling constraints** — historically teams asked "where is the source of truth?" instead of "is this a good plan?" HTML removes format friction so you can focus on content quality

---

## Notable Quotes

> "When you say Claude can run for 8 hours, what you're really saying is Claude can spend $500. All of us are becoming compute allocators now."

> "The amount of tokens I produce that go into production code is like 1%. But I'm generating so many more tokens like this — dashboards, custom interfaces — really trying to get a sense of what I want to do."

> "Verification is not testing."

> "Design.md is dead. Long live design.html."

> "This is micro-software on top of micro-software."

> "There's no trade-off between being nice and pretty for you and being nice for Claude — they're really the same."

> "I always give Claude an out — 'whatever is needed to give me maximum context' — my way of saying: I trust you here."

---

## Tasks Generated
See `tasks/backlog.md` — filter by `[SOURCE: html-markdown-thariq]`

---

## Priority Rating
**Signal strength:** Very High
**Reason:** First-party signal from an Anthropic Claude Code engineer about how the team internally uses the tool. The HTML-over-Markdown insight is immediately applicable, costs nothing to implement, and directly improves quality of every planning artifact. Multiple practices are zero-friction to adopt today.
