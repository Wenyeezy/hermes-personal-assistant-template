# Hermes Life · Meals + Fitness Preview

[English](README.md) · [简体中文](README.zh-CN.md)

Record a meal. Log a workout. Pick up your day.

A local-first daily journal you can **fork and run without GPT**. Nutrition and
Fitness are the core; **Finance is optional and off by default**. MIT licensed.

[Try the fictional demo](https://hermes-preview.wenyeezy.com/) ·
[Download the latest preview](https://github.com/Wenyeezy/hermes-personal-assistant-template/releases) ·
[Installation](START_HERE.md) · [Feedback](COMMUNITY.md)

![Fictional meals and fitness preview](https://hermes-preview.wenyeezy.com/media/hermes-preview-wide.png)

## Start recording

Install Python 3.10+, download and unpack the preview, and open a terminal
**inside that folder**:

```sh
python3 scripts/hermes.py start --open
```

That's it: no Git, GPT, Codex, API key, account, or extra Python packages.
On Windows, use `py -3` instead of `python3`. Included convenience launchers:
`Start-Hermes.command` on macOS and `Start-Hermes.bat` on Windows. If the OS
blocks a downloaded launcher, use the terminal command above.

1. **Nutrition:** save a meal and its calories/macros. Pending estimates stay
   out of confirmed totals; confirm a reviewed entry without duplicating it.
2. **Fitness:** save a workout or a daily activity summary. See recorded workout
   minutes, steps and nutrition totals in the dashboard.
3. **Optional modules:** explicitly enable Finance if you want a manual local
   ledger. Turning it off hides it, blocks the dashboard API and keeps records.

Keep the terminal open; Ctrl-C stops Hermes. No background service is installed.
Existing files and configuration are preserved. State stays in Git-ignored
`private/Hermes_Runtime/`; the local database is **not encrypted**.

Prefer fictional samples first?

```sh
python3 scripts/hermes.py start --demo --open
```

The offline sample is isolated in `private/Hermes_Demo/`. It never seeds an
unmarked database containing existing records. The public browser demo is a
separate static simulation, not a hosted personal-data service.

## Optional AI — later, not a setup requirement

The default Echo adapter is an offline test, **not AI**. You can independently
configure your own OpenAI API, Codex CLI sign-in, Ollama, or compatible chat
endpoint. Selected prompts/photos may leave your machine when you enable a
cloud provider. Chat does **not** automatically write meals or workouts.

A local Hermes Gateway can be used through the compatible chat adapter **only
if it exposes the required chat-completions protocol**. Production Hermes MCP,
owner-wide memory and write-tool/receipt bridging are not shipped in this
starter. See [model and endpoint setup](docs/runtime-edition.md).

## What's included?

| Capability | Preview |
| --- | --- |
| Manual meals, confirmation, macros, summaries and optional goals | Working without AI |
| Manual daily activity and workouts; daily workout totals | Working without wearable or iPhone |
| Finance ledger | Explicit opt-in; disabled by default |
| Career tracker | Optional extension; disabled by default |
| Local SQLite and private Markdown scaffold | Working; unencrypted |
| Model adapters and optional photo estimates | Included; disabled until you configure them |
| iOS companion, bank sync, production memory/gateway system | Not included |

## Privacy

- Never commit `private/`, real photos, exports, databases or credentials.
- First run connects no account or model. Raw chat logging is off.
- The dashboard binds to `127.0.0.1`. **Do not expose it to the internet.**
- Disabling an optional module is not deletion or encryption; records stay local.
- The AWS website contains only fictional data. It has no signup or analytics.
- Read [Safety](docs/safety-and-privacy.md) before using real records.

## Project structure

```text
hermes_lite/  Dependency-free Python runtime and localhost UI
site/         Static fictional demo and code-native launch layouts
scripts/      First run, checks, build and isolated static deployment
tests/        Runtime, opt-in, setup and privacy regression checks
templates/    Placeholder-only private knowledge scaffold
docs/         Optional models, integrations and architecture
```

Development checks:

```sh
python3 scripts/privacy_check.py
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/build_preview.py
```

[Architecture](docs/architecture.md) · [Roadmap](ROADMAP.md) ·
[Contributing](CONTRIBUTING.md)

## License

[MIT](LICENSE): fork, modify and reuse, including commercially, under its terms.
This early preview is provided as-is; it is not medical or financial advice.
