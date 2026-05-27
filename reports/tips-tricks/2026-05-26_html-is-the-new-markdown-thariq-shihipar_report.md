# Report: Why this Claude Code engineer uses HTML files as AI specs

**Date:** 2026-05-26
**Video URL:** https://youtu.be/Qrpm7E80wQ0
**Channel:** How I AI | **Speaker:** Thariq Shihipar (Anthropic, Claude Code team)
**Views:** 71,355 | **Duration:** 36 min
**Analysis file:** `analysis/tips-tricks/2026-05-26_html-is-the-new-markdown-thariq-shihipar.md`

---

## Executive Summary
First-party signal from inside Anthropic's Claude Code team. Thariq Shihipar makes the case that HTML has replaced Markdown as the right format for specs, plans, and any document you want to meaningfully engage with alongside Claude. The insight is not just aesthetic — it's about staying in the loop as agents run longer and plans grow larger. When plans are unreadable, you stop editing them, and output quality collapses.

---

## Top Practices Extracted

| # | Practice | Why |
|---|----------|-----|
| 1 | HTML over Markdown for all planning artifacts | Plans get unreadable at scale; HTML keeps you in the loop |
| 2 | Brainstorm in HTML — visual grid, not bullet list | "I won't read output longer than one screen" — HTML forces scannable density |
| 3 | Interview yourself before writing the plan | Surfaces unknown unknowns before they become bugs |
| 4 | HTML plan = max context doc (types, mockups, file structure, code excerpts) | One artifact with everything Claude needs to implement |
| 5 | Micro-apps for editing plan sections | Build throwaway HTML UI for a single table/section → edit visually → copy back |
| 6 | Type interfaces + validation criteria as spec bookends | Two anchors that make everything in between executable |
| 7 | Verification ≠ Testing — synthetic data CLI, rubrics, recorded video | More robust than unit tests for agent-built code |
| 8 | Living design system as `design.html` | Shareable, referenced by Claude on any new project |
| 9 | Always give Claude an out: "whatever is needed" | Prevents over-constraining; activates Claude's judgment |
| 10 | Clear context → pass HTML plan as artifact → implement | Clean handoff from planning to execution |

---

## Anti-Patterns Identified

| Anti-Pattern | Better Alternative |
|---|---|
| Markdown plans >1 screen | HTML with visual structure |
| Over-built skills ("You are an expert planner who must...") | Lean instructions + trust signal ("whatever is needed") |
| Yelling at or being stern with Claude | Friendly tone → reasoning traces stay healthy |
| "Where is the source of truth for this spec?" | Just-in-time HTML docs; Claude can find any context it needs |

---

## What Was Executed This Session

### ✅ Global CLAUDE.md updated — 2 rules added
1. **HTML planning rule:** "For any plan, spec, or PRD longer than one screen: generate HTML, not Markdown."
2. **Compute allocator mindset:** "Every long-running task is a spend decision. Spec quality = output quality."

These are now active in every Claude session globally.

---

## Tasks Created
10 tasks added to `tasks/backlog.md`. 2 executed immediately. 8 remaining.

| Task | Priority |
|------|----------|
| Create `templates/plan_template.html` | High |
| Generate `.html` reports alongside `.md` in pipeline | High |
| Create `html-spec.md` skill | High |
| Living `design.html` for antigravity frontend work | High |
| Add brainstorm step to youtube_analyzer CLAUDE.md | Medium |
| Document micro-app editing pattern | Medium |
| Add verification step to pipeline | Medium |
| Try weekly HTML status update pattern | Low |

---

## How This Applies to Our Workflow

**Immediately:** Every plan Claude generates from now on should be HTML if it's longer than one screen. The youtube_analyzer reports are a natural candidate — switch `reports/` from `.md` to `.html` to actually engage with findings visually.

**Next:** The `html-spec.md` skill will standardize the full workflow: brainstorm HTML → interview → HTML plan → micro-app editing → clear context → implement. This is the most valuable skill to build from this video.

**Mindset shift:** We're spending compute to build things. The quality of the planning HTML directly determines the quality of what gets built. Treat specs as the most important artifact in the pipeline, not as overhead.

---

## Recommended Follow-Up
- [ ] Build `templates/plan_template.html` before the next implementation task
- [ ] Schedule part 2 of this interview (testing/verification deep-dive)
- [ ] Try the brainstorm-in-HTML approach on the next youtube_analyzer feature
