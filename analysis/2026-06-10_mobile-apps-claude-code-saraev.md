# Analysis — How to Build Mobile Apps with Claude Code: Full Course (2026), Nick Saraev
URL: https://youtu.be/BMMcmmnjrM8 · Analyzed: 2026-06-10
Lens: what is useful for the **Apex Sales native iOS buildout** that we are **not already doing**.

## Course shape
~4h course building three Expo/React-Native apps (habit tracker, calorie tracker, pomodoro)
end-to-end with Claude Code: ideation framework → scaffold → design loops → 3-tier testing →
Supabase backend → security audit → EAS build → App Store/Play submission → post-launch.

## Already covered by our buildout (no action)
- CLAUDE.md/AGENTS.md project instructions; error-logs-into-Claude debugging; git discipline
- Physical-device-only checks (haptics, push, mic) — our DEVICE_VALIDATION_RUNBOOK covers these
- Screenshot automation (ComprehensiveUIAudit ≈ his Chrome screenshot loop, but stronger)
- .env/secrets hygiene; contract-first backend; local-first caching w/ revalidate (CacheStore)
- App Store metadata/review-notes/privacy package; TestFlight-before-launch; demo reviewer account
- /clear, /compact, queued parallel work, subagents — session practices we already use

## USEFUL AND NOT YET USED (the delta)

### 1. Pre-submission security audit, run 2–3× with fresh context  [HIGH]
He treats a structured security audit (tiered severity, CWE labels) as a mandatory release
gate, re-run in a *fresh* Claude instance after fixes to catch fix-introduced regressions.
We never ran one on the iOS app. Known candidates worth checking: WebSocket auth token in
the URL path, keychain/token-refresh handling, PII in logs, ATS exceptions.

### 2. Hidden in-app dev/QA menu  [MEDIUM-HIGH]
Dev-only screen with "reset onboarding / clear all data / simulate states / trigger all
animation-states". We have UI-test launch args (--uitesting-*) but nothing usable during
manual device validation — would cut the 30-min device runbook time materially.

### 3. AI-output sample-review loop before shipping prompts  [MEDIUM]
Generate 10+ sample outputs of every LLM feature (our SmartReplyBar, DailyBriefing,
AskAISheet), review, tune the prompt (e.g. strip em-dash "AI tells"), regenerate — before
hardcoding. Our FoundationModels prompts were never sample-audited.

### 4. Autonomous performance audit loop  [MEDIUM]
"Measure each screen's load time → identify N+1 / serial fetches → batch → re-measure."
Direct hit in our code: TasksStore fetches communication detail **sequentially in a loop**
(one request per task-bearing conversation). Also no Instruments pass was ever done.

### 5. Screenshot-driven design-consistency audit  [MEDIUM]
Feed the 23 ComprehensiveUIAudit PNGs back through Claude to enumerate cross-screen
inconsistencies (borders, spacing, radius, typography) and fix as one batch. We capture
the screenshots already; we never close the loop automatically.

### 6. Post-launch ASO toolkit  [LOW, post-v1]
App Store Connect analytics, custom product pages, promo codes as deliberate post-launch
steps. Not in any of our docs yet — belongs in APP_STORE_CHECKLIST as a post-launch section.

### 7. Design-reference workflow (Dribbble screenshot → emulate)  [LOW]
Cheap technique for future redesign passes; not needed for v1.

### 8. Core-loop/retention framing  [LOW for a B2B CRM]
His 5-step framework (core function → <30s core loop → accessories → ≤5-7 screens →
retention hook) is consumer-app shaped, but "instant visual+haptic reward on the core
action" is worth borrowing for disposition-submit and task-complete moments.

## Explicitly NOT applicable
Expo Go / EAS build+submit pipeline, AsyncStorage versioning, Reanimated confetti,
Chrome-localhost testing tier, app.json/eas.json generation, Play Console setup —
all RN/Expo-specific; we are native SwiftUI with xcodebuild + fastlane.

## Anti-patterns he warns about that we already avoid
Mock-success states, skipping device testing, pasting API keys into chat, shipping
without security review (we now have it as a task), optimizing everything at once.
