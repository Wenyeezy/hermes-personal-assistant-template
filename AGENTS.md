# Codex Workspace Guide

This repository is a sanitized, Codex-first template for a local-first personal
assistant. Treat the public repository as documentation and scaffolding, never
as a live user-data store.

## First-Run Protocol

When the user asks to set up, onboard, initialize, or continue this template:

1. Read `START_HERE.md`, `docs/easy-setup.md`, and
   `docs/safety-and-privacy.md`.
2. Run `python3 scripts/easy_setup.py check` before changing anything.
3. Explain that the default generated workspace is `private/`, which Git
   ignores.
4. Ask only for choices needed for the current phase. Do not ask for API keys,
   tokens, account identifiers, raw exports, or private documents during the
   scaffold phase.
5. With the user's approval, run `python3 scripts/easy_setup.py init`.
6. Run `python3 scripts/easy_setup.py check` again and report the next smallest
   useful step.

If the user has an explicit non-setup task, do that task instead of forcing
onboarding.

## Safety Rules

- Keep personal memory, generated state, credentials, raw logs, exports, and
  screenshots out of tracked files.
- Write personal setup content only under `private/` by default, or to another
  path explicitly chosen by the user.
- Never copy a real `.env`, runtime config, database, browser profile, keychain
  value, session, or account export into this repository.
- Use placeholders in public examples. Do not infer personal facts.
- Before any commit or push, run:

  ```text
  python3 scripts/privacy_check.py
  python3 -m unittest discover -s tests -p 'test_*.py'
  ```

- Review the exact staged diff. Do not use broad staging in a private runtime
  repository.
- Installing Hermes, enabling gateways, adding providers, scheduling jobs, or
  connecting accounts are separate opt-in phases. Scaffold success does not
  authorize them.

## Source of Truth

- `START_HERE.md`: human entry point.
- `docs/easy-setup.md`: Codex-guided setup contract.
- `docs/architecture.md`: reusable system design.
- `docs/current-state-log.md`: sanitized lessons and current template state.
- `templates/`: files copied into the private workspace.
- `scripts/easy_setup.py`: deterministic local scaffold and check.
- `scripts/privacy_check.py`: public-tree privacy backstop.
