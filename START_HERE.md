# Start Here

This repository is a privacy-safe framework, not a copy of somebody else's
personal assistant data.

## Easiest Path

1. Fork or download this repository.
2. Open the whole folder as a project in Codex.
3. Say:

   ```text
   Read AGENTS.md and help me start Easy Setup.
   ```

4. Codex will inspect the template, explain the privacy boundary, and—after
   your approval—create a local knowledge-base scaffold under `private/`.

You can also run the deterministic scaffold yourself:

```text
python3 scripts/easy_setup.py check
python3 scripts/easy_setup.py init
python3 scripts/easy_setup.py check
```

The generated `private/` directory is ignored by Git. The setup script does not
request credentials, install background services, connect accounts, or enable
cloud providers.

## After the Scaffold

Fill the generated files gradually. Start with response preferences, current
priorities, and one project. Add model providers, messaging gateways, imports,
and scheduled automation only as separate opt-in phases.

Read [Easy Setup](docs/easy-setup.md) for the full flow and
[Safety and Privacy](docs/safety-and-privacy.md) before connecting real data.
