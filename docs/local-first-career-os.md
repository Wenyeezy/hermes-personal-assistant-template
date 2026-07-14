# Local-First Career OS

This pattern turns explicitly saved opportunities into a private, explainable
career workflow without crawling authenticated job platforms.

---

## Product Boundary

The owner performs one deliberate Save/Share, imports an official account
archive, or provides an allowed alert. After that, the local system owns:

- normalization and source history;
- bounded public-page evidence recovery and safe retry;
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
  -> acquisition state (enrich / retry / review / archive)
  -> bounded official-source recovery
  -> explainable rank vector
  -> five-view board and action queue
  -> truthful material workspace
  -> confirmed current-page ATS assistance
  -> human submission
  -> outcome event
```

Each adapter should declare allowed hosts, parser version, input/output
contract, fixtures, refresh policy, rate limit, and structured errors. Company-
specific parsing should not live inside the gateway or dashboard.

### Make Acquisition State Explicit

A saved opportunity is not yet an application. Give every canonical
opportunity a separate acquisition record with explicit states such as:

```text
enrichment_pending
  -> evidence_ready
  -> enrichment_retry
  -> review_required
  -> archived_tombstone
```

Try the original unauthenticated public page first. If it is broken, search a
small bounded set of official company or ATS alternatives and require
title/company agreement before repairing the authoritative URL. Third-party
copies are discovery hints, not authoritative Apply destinations.

Do not interpret a generic 404, login wall, timeout, or empty search as proof
that a role is closed. Archive only after explicit official closure evidence;
otherwise keep the item visible for retry or owner review. Tombstones should
retain only stable hashes, requisition identity when available, closure reason,
and timestamps—not JD bodies or private file pointers.

Every future canonical opportunity should enter this lifecycle automatically.
The recovery lane should be bounded by item count, total runtime, redirects,
response size, retries, and per-item failure isolation.

### Keep Intake And Canonicalization Separate

An explicit Quick Add should make only the narrow claim it can prove: the
owner's link or copied text was saved to a private Inbox. It should not claim
that an opportunity was identified, scored, or added to an application
pipeline in the same response.

A later deterministic lane can process a bounded number of pending Inbox
observations through the canonicalization engine. This separation gives the
system a stable place for incomplete input:

```text
Quick Add
  -> owner-only Inbox receipt

bounded Daily lane
  -> canonicalize when identity is sufficient
  -> keep incomplete observations visibly reviewable
  -> never guess the missing identity
```

### Treat Job-Digest Email As A Verified, Bounded Source

A read-only mailbox connection can turn selected job-alert or digest email into
Career Inbox observations without granting the career system a job-platform
login. Keep this adapter narrower than a general email reader:

- require the exact sender and return path plus passing DKIM, SPF, and DMARC;
- decode MIME locally, refuse attachment downloads, and never load remote
  images or tracking pixels;
- preserve useful plain text while extracting only allowlisted evidence links
  from the HTML alternative;
- split a multi-job digest into individual, versioned observations;
- cap messages, cards per message, and total Daily mutations independently;
- save owner-only continuation state so overflow is retried rather than lost;
- make replay idempotent and expose only aggregate counts in status surfaces.

The mailbox grant should stay exact and read-only. It can be shared by several
approved Career selectors, but it must not become permission to scan arbitrary
senders, modify mail, reuse platform cookies, or crawl an authenticated job
site.

Real-sample validation should retain only aggregate evidence: authentication
passed or failed, cards parsed, attachments fetched, and remote images loaded.
Do not copy subject lines, bodies, message identifiers, job identities, or
private links into tests or public logs.

Adding a source changes the automation contract. A Doctor should reject the
previous source-count shape as legacy evidence until one new-contract run is
recorded. This temporary `invalid` state is safer than treating an older run as
proof that the expanded pipeline is healthy.

### Isolate Multiple Mailboxes And Design For Reauthorization

A multi-mailbox Career connector should remain one bounded workflow, not one
duplicated scheduler per account. Keep a value-free registry and isolate each
mailbox's OAuth client material, token, cursor, selector state, and health. One
account may be the default processing priority, but it must not become a silent
fallback identity for another account.

After authorization, verify the actual mailbox profile against the selected
registry entry. If it does not match, refuse to save the token. A refresh or
administrator-policy failure should pause only that mailbox and expose a clear
`reauthorization_required` or `administrator_blocked` state while other approved
accounts continue within the same global mutation/runtime ceiling.

Do not design scheduled work around repeated MFA prompts. Interactive MFA may be
required for initial consent or after an organization revokes a refresh grant;
the connector must never automate passwords, MFA codes, or consent retries.
Google OAuth projects left in Testing expire non-basic-scope test-user grants
and offline refresh tokens after seven days. Durable unattended use therefore
needs an appropriate production publishing state, while each managed Workspace
may still require an administrator to allow high-risk Gmail scopes.

The account registry and public status should use opaque local aliases. Email
addresses, OAuth client identifiers, tokens, and organization policy details do
not belong in public docs, logs, metrics, or cross-gateway messages.

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

Do not collapse profile completeness and ranking eligibility into one boolean.
A profile may contain explicitly accepted follow-ups that do not prevent a
bounded rank. Publish both states:

```text
profile_ready
  strict completeness for the full profile contract

ranking_ready
  exact registered conditions sufficient for the current ranker
```

The exception list must be versioned and tested. A generic rule such as
"partial is good enough" silently weakens the evidence gate. The UI should say
that ranking is active while keeping the follow-ups visible.

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
  import, normalize, deduplicate, recover public evidence,
  retry safely, check deadlines/errors

bounded local-intelligence lane
  process only new/changed opportunities, explain ranking and gaps
```

Both lanes should be idempotent, isolate per-source failures, enforce item/time
ceilings, expose deferred backlog, and write status-only run reports. Keep
scheduling dormant until storage, adapters, migrations, privacy, and idempotency
tests pass.

Activate recurring jobs through a separate owner-authorization receipt rather
than turning a dry-run planner into an implicit installer. A safe activation
record binds the exact job IDs, schedules, local-only route, runtime/item
ceilings, and no-submit boundary. Activation should preserve unrelated jobs,
create an owner-only backup, write atomically, and replay idempotently. A Doctor
check should reject mismatched authorization hashes or drifted job contracts.

---

## Five-View Board Contract

Do not mix bookmarks, recommendations, and applications in one pipeline:

- **Inbox** — newly captured jobs being enriched or waiting for a bounded retry.
- **Recommended** — current, complete, ranked jobs that pass owner exclusions.
- **Active Pipeline** — only jobs the owner explicitly advanced to preparing,
  ready, applied, screening, interview, or offer.
- **Deadlines** — only evidence-backed deadlines; never guess a date.
- **Review Queue** — unresolved link/evidence/duplicate questions that still
  require human judgment.

Counts should represent distinct opportunities. If one opportunity has several
gaps, expose a separate attention-unit count rather than inflating the Review
Queue headline.

Teach this model inside the product. Each view should provide equivalent
hover, keyboard-focus, and touch help, plus a replayable first-use tour. The
same value-free canonical guide source can render an in-page guide and an
offline PDF so documentation does not drift from verified behavior.

---

## Evidence Pilot

Passing fixtures is necessary but not sufficient for a personal Career OS.
Before calling the stage complete, run a real multi-day evidence pilot that
tests the approved product claims in ordinary use.

Derive what the system can prove from local ledgers:

- Share/Save and canonicalization counts;
- duplicate-review decisions;
- confirmed ATS fields approved and written;
- Daily and due deep-run success;
- visible backlog.

Ask the owner only for facts the ledgers cannot prove, such as correctness,
manual minutes, and privacy/boundary incidents. Keep each local day's record
immutable and owner-only.

An idle pilot must not pass. Metrics with no denominator should remain `null`
or `not exercised`, not silently become 100%. The final report should require
both the intended duration and at least one real exercise of every required
workflow category.

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
