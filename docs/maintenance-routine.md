# Maintenance Routine

Use this routine whenever the private Hermes setup changes.

---

## Two-Layer Update Rule

Maintain two separate layers:

```text
Private setup layer
  Real logs, real paths, real environment notes

Public sharing layer
  Sanitized docs, templates, diagrams, reusable instructions
```

Do not automatically mirror private files into the public layer.

---

## After Each Major Setup Change

1. Update the private setup log or handoff file.
2. Decide whether the change is useful for public readers.
3. If yes, write a sanitized version into this folder.
4. Remove:
   - API keys;
   - tokens;
   - account IDs;
   - private paths;
   - personal memory;
   - raw logs;
   - identifying screenshots.
5. Re-read `.gitignore`.
6. Run a leak scan for private paths, hostnames, API-key names, account labels,
   real people, screenshots, and raw logs.
7. Review the diff before publishing.
8. Commit and push only the sanitized public layer.

For this repository, the minimum automated gate is:

```text
python3 scripts/privacy_check.py
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/easy_setup.py init --dry-run
```

CI repeats the privacy scan and setup tests. Automated checks are a backstop,
not permission to skip a staged-diff review.

When inspecting a private runtime, prefer metadata-only discovery, explicit
allowlisted directories, and filename-only matches before reading content. Do
not run broad content searches across credential, token, session, keychain,
browser-profile, or environment-file stores. If credential-like material is
rendered in a terminal, agent trace, or log, stop, avoid repeating the value,
check tracked/public copies, and rotate the credential through a verify-then-
disable sequence.

## Runtime Consistency Checks

After memory or messaging changes, verify behavior rather than file presence:

- the Gateway process is alive and every configured platform adapter connects;
- platform adapters share policy but return distinct session identifiers;
- ordinary memory queries never return local-sensitive sources;
- an explicit local-only test can retrieve the expected local-sensitive source;
- matched source-registry content reaches the final prompt instead of being
  crowded out by a large topic pack;
- scheduled generation success and platform delivery success are reported as
  separate states;
- official-export promotion leaves a zero-item human approval queue or clearly
  records what is still pending.

After Career workflow changes, also verify:

- Inbox receipts do not overclaim canonicalization, ranking, or application
  creation;
- bounded Daily processing advances only eligible observations and leaves
  incomplete items visible;
- strict profile completeness and ranking eligibility are reported separately;
- every active recurring job matches one owner-authorization hash and preserves
  the local-only/no-submit contract;
- the Doctor reports schedule drift, stale runs, failures, and backlog without
  exposing job or profile content;
- a real evidence pilot cannot pass with unexercised denominator categories;
- scheduler dispatch, queue delay, execution, committed changes, downstream
  delivery, and owner confirmation remain separately observable;
- the outer script timeout matches the documented bounded runtime without
  relaxing per-request, per-item, or per-mutation ceilings;
- authorized source/account registries match the owner-approved baseline;
- acquisition throughput is not reported as enrichment, ranking, or production
  acceptance when required evidence is absent;
- plugin API additions are tested after restarting the dashboard backend, not
  only after reloading static assets.

For multi-platform setups, document one Gateway service and each adapter
separately. This prevents a healthy Telegram connection from masking a Weixin
delivery failure, or vice versa.

---

## What Belongs Here

Good public content:

- architecture explanations;
- setup principles;
- provider strategy;
- memory policy templates;
- triage workflow templates;
- sanitized troubleshooting notes;
- current-state lessons without private implementation details;
- diagrams;
- examples with fake IDs.

Bad public content:

- real `.env`;
- real `config.yaml`;
- WeChat/iLink tokens;
- provider credentials;
- private memory files;
- raw assistant conversations;
- screenshots with personal information.

---

## Suggested Public Log Pattern

Use `docs/current-state-log.md` for reusable lessons:

```text
Private log:
  exact incident, commands, real paths, runtime details

Public log:
  sanitized pattern, root-cause category, reusable mitigation
```

Never copy private maintenance-log entries verbatim into the public repository.

---

## Suggested Commit Style

```text
docs: add WeChat gateway notes
templates: add memory triage workflow
docs: document provider safety strategy
examples: add sanitized handoff
```

Keep commits boring and obvious.
