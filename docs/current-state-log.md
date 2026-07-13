# Current State Log

This is a sanitized engineering log for patterns that proved useful while
building a personal Hermes-style assistant. It intentionally omits private
hostnames, local paths, account names, raw health/finance records, screenshots,
tokens, and personal memory.

---

## Stage 8 Baseline

The current recommended architecture is:

```text
chat / dashboard / phone app
  -> gateway
  -> privacy router
  -> memory router
  -> provider router
  -> tools and local state
```

The important lesson is that the gateway should not merely forward every turn to
one large model. Some turns are routing commands, some need local tools, some
need cloud quality, and some should never leave the local machine.

---

## Provider Routing Lessons

- Use a fast local path for simple private turns.
- Use the full tool path for web, PDF, files, finance, health, reminders, and
  anything that needs local scripts or APIs.
- Handle provider-switch commands before the model call. A command such as
  `/local` or `/cloud` should update routing state immediately.
- Do not silently fall back to an aggregator or expensive provider. Require
  explicit same-turn authorization.
- Avoid injecting the entire tool catalog for simple local turns. It can add
  latency and confuse smaller local models.

---

## Memory Routing Lessons

The best working pattern is a hybrid:

```text
small always-on core profile
  + deterministic topic triggers
  + short retrieved snippets
  + explicit missing-fact queue
```

The model should not be expected to "remember to search memory" by itself.
The gateway should detect likely memory needs and attach a few relevant snippets.
For ambiguous cases, use a small classifier or local heuristic first, then fall
back to a deeper route only when needed.

Keep local-sensitive memory gated. A public template should explain the layer,
not contain the user's private facts.

For official account exports, use incremental review rather than repeatedly
resynthesizing the entire archive:

```text
package hash and dedup
  -> compare conversation IDs + stable content hashes
  -> process only new/changed conversations
  -> local candidate extraction
  -> direct-evidence/conflict/privacy review
  -> ordinary pack or explicit local-sensitive source
  -> golden/card/stale/leak tests
```

Model confidence is not approval. A locally generated candidate can still mix
people, copy an assistant recommendation as a user preference, or revive an old
identity artifact. Promotion needs direct user evidence and canonical conflict
review.

---

## Health and Food Lessons

For HealthKit-style sync, a small native app is cleaner than a hand-edited
Shortcut once the project becomes long-term. Shortcuts remain useful for
prototyping and fallback diagnostics, but they are easy to misconfigure.

For food logging, avoid "vision guess first" behavior:

1. Read visible text, brand, restaurant, menu item, and quantity.
2. Search or resolve official nutrition data when available.
3. Use user observation over image/menu guesses.
4. Estimate only after evidence is exhausted.
5. Ask before writing uncertain rows.
6. Detect same-day duplicates and correction/replacement language.

If activity values are calibrated, label adjusted estimates separately from raw
device or HealthKit values.

The stronger lesson is to make calibration end to end. A raw day card combined
with an adjusted weekly report is a semantic bug even if each calculation is
individually valid. Keep raw values for private audit, but route every primary
display/report through one versioned derived-metric contract.

Generated frontend assets need their own regression gate. A later build can
silently restore stale behavior even when the source test remains green. Verify
the final production bundle and authenticated runtime routes after build and
restart.

---

## Finance Lessons

Finance should stay local by default. A useful dashboard can still expose:

- aggregate daily/weekly/monthly/yearly totals;
- local review counts;
- account aliases or short redacted labels;
- categories and notes;
- statement-audit status.

Do not send raw transactions, account masks, statement PDFs/text, or Plaid-style
secrets to cloud providers by default.

Two date modes are useful:

- spend-feel or authorized date for personal behavior review;
- posted or statement date for reconciliation.

Both modes should read the same local transaction table. Reviewing a transaction
should update category/status/notes, not duplicate or mutate the raw row.

A large backlog needs a review workflow, not just a long list:

- preserve manual approved/unsure/rejected decisions across classifier refresh;
- remove a row from Needs review only after the local server confirms the write;
- keep the inspector open and advance continuously;
- make Enter/Shift+Enter and IME behavior explicit;
- provide one bounded atomic Undo;
- treat smart queues as views, not new ledger states;
- generate repeated groups server-side with exact direction/category/channel
  boundaries, opaque fingerprints, stale-count rejection, explicit confirmation,
  and a strict batch ceiling;
- let remembered categories create suggestions, not unattended approval.

A shared category catalog with localized labels, contextual Emoji, and a Custom
fallback is faster and safer than free-text categories duplicated across views.

---

## Local-First Career OS Lessons

A personal Career OS should not imitate a job board or rely on unattended
scraping. The safer acquisition contract is one explicit Save/Share or archive
export from the owner, followed by local normalization, deduplication, ranking,
deadline tracking, material versioning, and action planning.

Important boundaries:

- do not store authenticated platform cookies or sessions;
- use official account archives and selected alerts as offline inputs;
- treat fuzzy company/title/location matches as duplicate candidates, not
  automatic merges;
- rank against one canonical local profile and save evidence, gaps, confidence,
  next action, and ranker version;
- distinguish deterministic daily maintenance from bounded local-model
  intelligence over new or changed items;
- keep ATS assistance current-page-only, confirmed field by field, and never
  click final submit;
- render planned and current components with visibly different styles in system
  maps and status views.

Operational lessons from the first live slice:

- make Quick Add an Inbox receipt, then let a bounded deterministic lane perform
  later canonicalization;
- keep acquisition state separate from application state: every future
  canonical opportunity enters bounded enrichment automatically, while only an
  owner decision can put it in Active Pipeline;
- try the original public page first, then a small official company/ATS search;
  treat rate limits as retry, generic link failure as review, and archive only
  with authoritative closure evidence;
- project Inbox, Recommended, Active Pipeline, Deadlines, and Review Queue as
  separate views, with evidence-backed counts and no invisible intermediate
  state;
- teach the workflow in the page with hover/focus/touch help and a replayable
  tour generated from the same value-free guide source as the offline PDF;
- expose strict profile completeness separately from an exact, versioned
  ranking-readiness gate;
- activate local schedules only through an owner authorization bound to the
  exact jobs, ceilings, local route, and no-submit contract;
- use an owner-only multi-day evidence pilot that derives ledger facts and asks
  only for correctness, time, and incident confirmation;
- treat missing-denominator pilot metrics as not exercised, never as a pass;
- restart the dashboard backend after adding plugin API routes; refreshing a
  static plugin bundle alone does not register new server routes.

See [Local-First Career OS](local-first-career-os.md) for the reusable pipeline.

---

## Multi-Adapter Gateway And Voice Lessons

It is practical to run lightweight and richer messaging adapters inside one
Hermes Gateway service. Share tool, memory, privacy, provider, skill, and
file-access policy, but isolate platform sessions, owner allowlists, media
transport, acknowledgements, delivery errors, and rate limits.

Do not infer that two chat platforms require two gateway processes. Separate
daemons make policy drift and duplicate schedulers more likely unless process
isolation is a deliberate requirement.

For voice, benchmark both speed and multilingual accuracy. A local model may be
fast after warm-up yet inaccurate for mixed-language speech. If cloud STT is
explicitly approved, use a dedicated restricted key and keep that permission
separate from general agent inference.

---

## Scheduled Briefing Reliability Lessons

Preparation and delivery must agree on the same freshness contract. A prep job
cannot run before a delivery job if the delivery prompt accepts only drafts
created later in the day.

Reliable pattern:

```text
bounded prep
  -> timestamped local draft
  -> freshness check
  -> small volatile refresh
  -> fail-soft delivery
```

Do not put unbounded webpage extraction or auxiliary LLM summarization on the
final delivery path. Keep the global watchdog intact, make optional source
failures section-local, update only the intended scheduled jobs through an
idempotent scoped command, and verify both successful content generation and
actual gateway delivery. A job marked successful before checking its delivery
log is incomplete evidence.

---

## Cloud Lite Lessons

A small cloud relay can keep the assistant useful while the main machine is
offline, but its job should be narrow:

- hold sanitized context snapshots;
- queue ordinary-safe events;
- receive whitelisted health/food summaries if the user policy allows it;
- store redacted local-request markers for the main machine;
- never store raw finance or local-sensitive memory by default.

Cloud chat should degrade gracefully. If a request needs local files, raw
finance, private health exports, or credentials, queue it for the local machine
instead of pretending the cloud node can handle it.

---

## Public Documentation Routine

After a private setup change:

1. Append the private maintenance log.
2. Decide whether a sanitized lesson belongs in this repository.
3. Update the relevant public doc or this log.
4. Run a leak scan for paths, tokens, account labels, hostnames, and private
   names.
5. Commit and publish only after reviewing the diff.
