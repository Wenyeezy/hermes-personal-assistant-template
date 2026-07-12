# Local-First Career OS

This pattern turns explicitly saved opportunities into a private, explainable
career workflow without crawling authenticated job platforms.

---

## Product Boundary

The owner performs one deliberate Save/Share, imports an official account
archive, or provides an allowed alert. After that, the local system owns:

- normalization and source history;
- duplicate/repost review;
- profile-aware ranking;
- deadlines and application state;
- truthful versioned materials;
- reminders and action queues;
- confirmed current-page form assistance;
- later outcome calibration.

It does not store platform cookies, run a headless authenticated crawler, send
outreach automatically, or submit an application.

---

## Pipeline

```text
explicit Share / selected alert / official archive
  -> versioned source adapter
  -> immutable source observation
  -> canonicalization
  -> duplicate-candidate review
  -> canonical opportunity
  -> explainable rank vector
  -> board and action queue
  -> truthful material workspace
  -> confirmed current-page ATS assistance
  -> human submission
  -> outcome event
```

Each adapter should declare allowed hosts, parser version, input/output
contract, fixtures, refresh policy, rate limit, and structured errors. Company-
specific parsing should not live inside the gateway or dashboard.

### Rehearsing Official Archives

Official exports can change a column label or timestamp format without changing
the meaning of the category. Treat that as schema drift, not permission to make
the parser permissive:

1. Rehearse the real archive against an owner-only temporary database and inbox.
2. On failure, inspect only member names, headers, format shapes, and aggregate
   status codes; do not print or copy row values into logs.
3. Add only the exact observed alias or format behind a failing regression test.
   Unknown headers and unsupported categories must continue to fail closed.
4. Replay the rehearsal to prove idempotency, file permissions, and database
   integrity before touching live state.
5. Back up the live database, run the bounded import, replay it once more, and
   record only aggregate status in the maintenance log.

An official profile export is evidence, not automatically the canonical
profile. When a newer structured memory or owner-confirmed profile exists, keep
that source authoritative and import only the explicitly approved categories.

---

## Ranking Contract

Do not save only one opaque score. Store a versioned vector that can explain:

- role and skill fit;
- evidence strength;
- career direction;
- location/work mode/eligibility;
- urgency and application effort;
- networking opportunity;
- risk and source freshness;
- confidence and next action.

The canonical profile is the ranking fact source. Retrieval memory can help
with conversation and drafting, but it should not silently override structured
profile facts. Models may improve wording; they must not invent scores or
experience.

---

## Duplicate Safety

Prefer exact identities in this order:

1. ATS host plus requisition ID;
2. canonical external apply URL;
3. source-platform opportunity ID.

Company/title/location fingerprints are useful only for creating a review
candidate. Never silently hard-merge on a fuzzy fingerprint.

---

## Automation

Use two separate lanes:

```text
daily deterministic lane
  import, normalize, deduplicate, check deadlines/errors

bounded local-intelligence lane
  process only new/changed opportunities, explain ranking and gaps
```

Both lanes should be idempotent, isolate per-source failures, enforce item/time
ceilings, expose deferred backlog, and write status-only run reports. Keep
scheduling dormant until storage, adapters, migrations, privacy, and idempotency
tests pass.

---

## Human Control

- Every external form field requires an explicit confirmation.
- Navigation changes or low-confidence mappings stop the helper.
- The system never clicks final submit.
- Outreach and status changes remain human actions.
- Private profile, resume, draft, form values, and application notes remain
  local by default.

A system map should use different visual language for current and planned
components and should show handoffs between sources, local processing, board,
materials, and human submission.
