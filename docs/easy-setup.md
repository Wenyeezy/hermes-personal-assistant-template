# Codex Easy Setup

Easy Setup turns this public template into a private, local workspace without
mixing the two layers.

## What Success Means

At the end of Phase 1:

- the public template remains unchanged and safe to sync;
- a private markdown knowledge base exists under `private/` by default;
- `START_HERE.md`, indexes, policies, current state, projects, and logs have
  placeholder-only files;
- a localhost-only starter dashboard and local SQLite module store can be
  initialized without credentials;
- no provider, gateway, account, schedule, or background service is enabled;
- the setup checker passes.

This is enough for Codex to help the owner fill and evolve the framework.

## Codex Flow

Open the repository as a Codex project and say:

```text
Read AGENTS.md and help me start Easy Setup.
```

Codex should first run the read-only check, explain where private files will be
created, and ask before initialization. The deterministic commands are:

```text
python3 scripts/easy_setup.py check
python3 scripts/easy_setup.py init
python3 scripts/easy_setup.py check
python3 scripts/hermes.py init
python3 scripts/hermes.py doctor
```

Start the dashboard only after the owner approves local runtime creation:

```text
python3 scripts/hermes.py serve --open
```

Preview without writing:

```text
python3 scripts/easy_setup.py init --dry-run
```

Use another private location only when the owner explicitly chooses it:

```text
python3 scripts/easy_setup.py init --target /an/owner/selected/path
```

The script refuses to overwrite existing files unless `--force` is supplied.
Review any existing content before using that option.

## Phased Setup

### Phase 1 — Private Markdown Scaffold

Create the local knowledge base and fill only low-risk basics:

- response style;
- current priorities;
- active projects;
- memory write rules;
- do-not-save rules.

### Phase 2 — One Provider

Configure one provider outside the public repository. Keep credentials in a
secret manager or ignored local environment file. Test only non-sensitive
prompts first. The runtime supports owner-configured OpenAI Responses API,
Codex CLI, Ollama, and OpenAI-compatible adapters. See
[Runtime Edition](runtime-edition.md).

### Phase 3 — Local-First Privacy Routing

Define local-only, redacted/aggregate, and ordinary-cloud zones. Verify the
privacy decision happens before provider selection.

### Phase 4 — Optional Interfaces and Tools

Add dashboards, messaging adapters, task tools, health or finance workflows one
at a time. Each integration needs its own owner authorization, data boundary,
health check, and uninstall path.

### Phase 5 — Bounded Automation

Only after manual flows work, add schedules with explicit time and mutation
ceilings. Report dispatch, queue delay, execution, durable changes, delivery,
and owner confirmation as separate facts.

## Privacy Model

```text
tracked public template
  architecture + instructions + empty examples

ignored private workspace
  owner profile + project state + local logs + generated indexes

external secret storage
  provider keys + account tokens + private credentials
```

Do not turn `private/` into a nested public repository. Do not remove its
ignore rule. Before publishing template changes, run:

```text
python3 scripts/privacy_check.py
python3 -m unittest discover -s tests -p 'test_*.py'
```
