# Hermes Life · Public Preview

[English](README.md) · [简体中文](README.zh-CN.md)

A local-first workspace for reviewed meal records, activity summaries, a simple
ledger, and career next steps.

**Preview, not the maintainer's private assistant.** This download includes a
working Python dashboard and manual local stores. It does not include personal
data, production gateways, automatic memory adoption, or connected accounts.

[Browser walkthrough](site/README.md) ·
[Live fictional demo](https://hermes-preview.wenyeezy.com/) ·
[Download](https://github.com/Wenyeezy/hermes-personal-assistant-template/releases) ·
[Installation help](INSTALL_FOR_FRIEND.md) · [Feedback](COMMUNITY.md)

## Start in one command

The fictional browser demo is hosted on AWS at a fixed HTTPS address. It is a
separate static walkthrough, not a hosted version of the local runtime.

Download and extract the repository, open a terminal **inside that folder**, and
run this with Python 3.10 or newer:

```sh
python3 scripts/hermes.py start --demo --open
```

No Git, Codex, API key, account, or third-party Python package is required.
This localhost walkthrough uses **made-up samples** in a separate, Git-ignored
`private/Hermes_Demo/` directory. Keep the terminal open; Ctrl-C stops it.
On Windows, use `py -3` instead of `python3`.

1. Open **Career** and save a sample opportunity and next step.
2. Open **Nutrition** and compare confirmed entries with an unconfirmed sample.
3. Notice the receipt after saving; records stay in your local SQLite store.

Default chat is an **offline echo, not an AI model**. Model setup is a separate
opt-in using your own account or local model.

Ready for an empty private workspace instead?

```sh
python3 scripts/hermes.py start --open
```

This initializes or checks the private Markdown scaffold and starts an empty
runtime. Existing configuration and records are preserved. Demo seeding refuses
nonempty, unmarked databases. See [Start Here](START_HERE.md) for troubleshooting
and [provider configuration](docs/runtime-edition.md) for optional AI chat.

## What works in this download?

| Capability | Public preview |
| --- | --- |
| Local dashboard and manual Nutrition, Health, Finance, Career records | Working |
| Confirmed nutrition totals, goals, and export format | Working; no automatic iPhone write |
| Private Markdown scaffold and local SQLite state | Working; not encrypted by this starter |
| OpenAI, Codex CLI, Ollama, compatible-provider adapters | Included, disabled until configured |
| Automatic memory review, owner-wide recall, production MCP gateways | Private system; not included |
| Bank sync, job applications, messaging, scheduled automation | Not enabled by this starter |
| HIIS and Crypto + RWA Research Labs | Separate research documentation; in development |

The browser demo is a **scripted simulation** of review workflows using
fictional data. It is not a hosted AI assistant or a connection to the
maintainer's records. No demo input is sent to a model or account gateway.

## Privacy boundaries

- Config, databases and knowledge files live under Git-ignored `private/` by
  default. Never publish that directory.
- First-run setup connects no model, bank, email or messaging account.
  Raw chat logging is off by default.
- The dashboard listens on `127.0.0.1`. **Do not expose it to the internet.**
  The public website is an independent static browser demo.
- Optional cloud adapters send requests to the provider you explicitly enable.
  Text checks are a backstop, not a guarantee of redaction.
- Use fictional data first. Read [Safety](docs/safety-and-privacy.md) before
  connecting real records.

## Understandable structure

```text
hermes_lite/  Python runtime, local stores and localhost UI
site/         Static landing page and fictional browser walkthrough
scripts/      Safe first run, privacy checks and preview build/deployment
tests/        Runtime, setup and preview regression checks
templates/    Placeholder-only private knowledge scaffold
docs/         Optional integrations, architecture and Research Labs
```

## Development checks

```sh
python3 scripts/privacy_check.py
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/build_preview.py
```

[Architecture](docs/architecture.md) · [Product areas](docs/product-areas.md) ·
[Roadmap](ROADMAP.md) · [Contributing](CONTRIBUTING.md).

## License

No open-source license has been granted yet. Public visibility is not an
open-source license; the owner retains rights while licensing is decided.
This is an early preview, with no medical, financial or employment guarantee.
Feedback and bug reports are welcome through the repository's issue templates.
