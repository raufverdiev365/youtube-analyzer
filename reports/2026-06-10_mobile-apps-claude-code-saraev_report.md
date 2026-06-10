# Report — How to Build Mobile Apps with Claude Code: Full Course (2026)
Author: Nick Saraev · https://youtu.be/BMMcmmnjrM8 · Analyzed 2026-06-10

## Summary
4-hour Expo/React-Native course building three apps end-to-end with Claude Code. Roughly
60% of its concrete techniques are Expo-pipeline-specific or things the Apex Sales iOS
buildout already does better (scripted xcodebuild testing, screenshot audits, contract
verification, fastlane metadata). The transferable value concentrates in **release-gate
practices** and **closing loops we already half-built**.

## Key practices adopted into backlog (7 tasks)
1. Security audit as a mandatory release gate, run 2–3× with fresh context — **top gap**;
   never run on the iOS app, and it ships auth tokens/keychain/WebSocket auth.
2. Hidden dev/QA menu for manual device validation speed.
3. Sample-review loop for LLM feature prompts before shipping them.
4. Autonomous performance audit (we have a known N+1 in TasksStore).
5. Screenshot-driven design-consistency batch fix (artifacts already exist).
6. Post-launch ASO section (ASC analytics, custom product pages, promo codes).
7. Core-action reward polish (haptics on disposition/task-complete).

## Priority
HIGH: #1 (pre-submission gate) · MEDIUM: #2–#5 · LOW/post-v1: #6–#7

## Not applicable
Expo Go/EAS build+submit, AsyncStorage, Reanimated, Chrome-tier testing, app.json/eas.json,
Play Console flow — RN/Expo-specific; the buildout is native SwiftUI + xcodebuild + fastlane.
