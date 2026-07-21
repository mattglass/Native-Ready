# Example Build Spec

## Purpose

Build a native onboarding flow for `[APP_NAME]` that:

- reduces confusion for first-time users
- captures a lightweight local profile for personalization
- keeps the app usable without required account creation
- reveals the app's value before the user lands in the main experience
- hands the user directly into the most important first action with momentum

This flow should feel:

- clear
- motivating
- fast
- credible

It should not feel:

- busy
- over-explained
- permission-heavy
- like a second app inside the app

## Product Intent

The onboarding should help users:

- focus on what they want from `[APP_NAME]`
- reflect briefly on their current habits, needs, or goals
- establish a foundation for behavior-aware personalization
- start with confidence instead of hesitation

## Core Product Decisions

- onboarding is a first-launch experience
- incomplete onboarding must be resumable later from `App Setup`
- answers are stored locally for now
- login is not required to start using the app
- any assistant, coach, or support feature is introduced as product value, not as a permission-like opt-in
- Siri / App Shortcuts are introduced later in the flow as a value-add, not a required setup step
- the strongest final handoff is into real app actions relevant to `[APP_NAME]`

## Source Inputs

### Stitch concepts to simplify

Use these as content and interaction references, not as layout replicas:

1. `[STITCH_SCREEN_1]`
2. `[STITCH_SCREEN_2]`
3. `[STITCH_SCREEN_3]`
4. `[STITCH_SCREEN_4]`
5. `[STITCH_SCREEN_5]`

### What to preserve from Stitch

- one question or decision per screen
- a clear sense of progress
- large direct answers
- at least one interaction pattern that feels distinct and native

### What to remove from Stitch

- oversized hero framing
- below-the-fold clutter
- secondary blocks competing with the main question
- anything that feels like web onboarding rather than native iOS flow

## Benchmark Patterns To Borrow

### Benchmark 1

- `[BENCHMARK_PATTERN_1]`
- `[BENCHMARK_PATTERN_2]`

### Benchmark 2

- `[BENCHMARK_PATTERN_3]`
- `[BENCHMARK_PATTERN_4]`

## UX Principles

### 1. Above-the-fold first

Each screen should fit the primary action without scroll on iPhone:

- progress / eyebrow
- one question or one promise
- one short support sentence
- answer controls or one primary value prop
- continue button

### 2. One decision per screen

No combined questions.

### 3. Friction is the enemy

If a screen does not help the app personalize better or help the user start more confidently, cut it.

### 4. Calm motion

Use:

- soft fade + slide transitions
- subtle selection animation
- smooth progress movement

Avoid:

- long hero animations
- bouncing
- noisy overlays

## Revised Screen Flow

### Screen 0: Welcome

- eyebrow: `[WELCOME_EYEBROW]`
- headline: `[WELCOME_HEADLINE]`
- body: `[WELCOME_BODY]`
- CTA: `[PRIMARY_WELCOME_CTA]`
- secondary: `[SECONDARY_WELCOME_CTA]`

### Screen 1: Primary Intent

Question:

- `[QUESTION_1]`

Options:

- `[OPTION_1A]`
- `[OPTION_1B]`
- `[OPTION_1C]`
- `[OPTION_1D]`

Storage:

- `[STORAGE_KEY_1]`

### Screen 2: Signal or Preference

Question:

- `[QUESTION_2]`

Control:

- `[CONTROL_TYPE_2]`

Storage:

- `[STORAGE_KEY_2]`

### Screen 3: Behavior Pattern

Question:

- `[QUESTION_3]`

Options:

- `[OPTION_3A]`
- `[OPTION_3B]`
- `[OPTION_3C]`
- `[OPTION_3D]`

Storage:

- `[STORAGE_KEY_3]`

### Screen 4: Starting Style or Mode

Purpose:

- reduce first-use confusion
- map users toward a better initial path

Question:

- `[QUESTION_4]`

Options:

- `[OPTION_4A]`
- `[OPTION_4B]`
- `[OPTION_4C]`

Storage:

- `[STORAGE_KEY_4]`

### Screen 5: Meet the Assistant or Guidance Layer

Purpose:

- introduce the app's coaching or support value
- reduce setup friction

Content:

- eyebrow: `[ASSISTANT_EYEBROW]`
- headline: `[ASSISTANT_HEADLINE]`
- body: `[ASSISTANT_BODY]`
- CTA: `[ASSISTANT_CTA]`

Notes:

- this screen is informational
- no binary opt-in required unless the product truly needs it
- the feature remains available later in the app

### Screen 6: Utility / Automation Value

Purpose:

- introduce hands-free or shortcut value without making it required

Content:

- eyebrow: `[AUTOMATION_EYEBROW]`
- headline: `[AUTOMATION_HEADLINE]`
- body: `[AUTOMATION_BODY]`
- CTA: `[AUTOMATION_CTA]`

## Final Handoff

The final onboarding state should hand the user into:

- `[PRIMARY_POST_ONBOARDING_ACTION]`
- `[SECONDARY_POST_ONBOARDING_ACTION]`

## Native Implementation Notes

- use a lightweight persisted profile model for onboarding answers
- keep screens modular and one responsibility per destination
- prefer native SwiftUI hierarchy over literal Stitch recreation
- preserve momentum and clarity over decorative complexity

## Validation Expectations

- onboarding builds and launches successfully
- first-run flow can be completed without dead ends
- primary selections persist across relaunch when intended
- the final handoff lands in a meaningful app destination
- the roadmap and baton reflect any newly unlocked follow-up work
