# Health Dashboard Workflow

This note documents a sanitized pattern for adding a private health and food
ledger to a personal Hermes-style assistant.

It intentionally avoids real hostnames, account IDs, screenshots, raw health
records, private memory, and production credentials.

---

## Goal

Build a local-first dashboard where a user can review:

- meals;
- macros;
- workouts;
- activity calories;
- resting calories;
- daily energy balance;
- current assistant engineering tasks.

The assistant can reason about food photos and text descriptions, but the
private ledger should remain local by default.

---

## Recommended Boundary

```text
User photo/text
  -> Hermes reasoning
  -> confirm or correct estimate
  -> local food/workout ledger
  -> dashboard summary

Phone HealthKit data
  -> small native bridge app, with Shortcut as fallback
  -> authenticated local ingest endpoint
  -> local ledger
  -> dashboard summary
```

Use cloud models only when the user's privacy policy allows it. Medical/private
HealthKit exports, unrelated private photos, and raw history should not be sent
to general cloud providers by default. A project may separately allow small
daily activity summaries or user-initiated food/activity uploads through a
limited cloud relay.

---

## Why Keep Meals In Hermes

Health platforms are good at clean numeric samples such as calories, steps, and
exercise minutes. They are usually less useful as a rich assistant diary.

Hermes can keep:

- restaurant context;
- user corrections;
- uncertainty notes;
- food photo references;
- final-vs-draft replacement logic;
- daily summaries and explanations.

If desired, a later bridge can write only confirmed numeric nutrition samples
back to HealthKit.

---

## Bridge Options

### Shortcut Bridge

Pros:

- quick to build;
- no app signing required;
- good for testing payload shape.

Cons:

- tedious to edit by hand;
- automation timing can be approximate;
- not ideal for long-term maintainability.
- Health sample queries can be easy to misconfigure, causing date or source
  mismatches.

### Native HealthKit Bridge App

Pros:

- cleaner authorization flow;
- can use HealthKit background delivery;
- easier to maintain once built;
- better long-term user experience.

Cons:

- requires Xcode;
- requires signing and HealthKit capability;
- background delivery is opportunistic, not exact wall-clock scheduling.

For a serious long-term setup, build the native app first and keep the Shortcut
as a diagnostic fallback. If using free personal-team signing, remember that
installed builds can expire quickly; paid developer signing or TestFlight is
cleaner for daily use.

### Third-Party Export App

Pros:

- faster than writing a bridge from scratch;
- may expose REST or file export options;
- useful for quick validation.

Cons:

- paid tiers may be required;
- debugging is limited to the vendor's behavior;
- the app may not expose the exact Apple Health summary semantics you expect.

Use this as an optional comparison tool, not as the only long-term architecture
if you intend to own the assistant stack.

---

## Dashboard Pattern

A good first dashboard does not need to be flashy. It should be readable:

- one row or card per meal;
- separate meal and workout sections;
- daily totals at the top;
- compact labels and soft typography;
- bilingual labels if the user works in multiple languages;
- a small workboard for current engineering tasks and completed-work archive.

Avoid exposing internal event IDs or replacement markers in the user-facing
view. Keep those in the raw ledger or debug view.

---

## Suggested Milestones

1. Create a local JSONL or SQLite ledger for meals, workouts, and daily health
   snapshots.
2. Add an authenticated local ingest endpoint.
3. Test with a phone Shortcut.
4. Add a dashboard summary endpoint.
5. Build a native HealthKit bridge app.
6. Keep the Shortcut as fallback until the app is verified.
7. Optionally add HealthKit nutrition write-back for confirmed numeric samples.
8. Make the dashboard workboard read from a structured task/log file.

## Calibrated Activity Contract

If activity calories are calibrated, treat the calibration as a system
contract rather than a per-card decoration:

- keep the raw device/HealthKit value unchanged in the private ledger for
  audit;
- store or deterministically derive the calibrated value alongside it;
- use one calibrated policy for day cards, workout details, total burn, net
  balance, rolling charts, exports, and scheduled reports;
- label the primary UI value with a quiet `Adjusted` or `Calibrated` badge;
- version the policy or record its factors so historical recomputation is
  explainable;
- migrate historical derived fields atomically, with a backup, and never invent
  a calibrated value when the source value is missing.

Do not mix a raw single-day number with a calibrated weekly number. The UI may
offer raw values in an audit/debug view, but the primary product surface should
have one consistent meaning.

### Preventing Build Regressions

A source-level test is not enough when a dashboard serves generated static
assets. Another build or worktree can overwrite a correct bundle with stale
behavior. Add a post-build contract test that:

1. checks the source uses calibrated fields;
2. resolves the generated JavaScript asset from the production index;
3. confirms the deployed bundle contains the calibrated-field contract and UI
   label;
4. probes the authenticated local and public summary routes after restart.

Run this gate after every production dashboard build, especially when multiple
branches or agents can rebuild the same shared runtime.
