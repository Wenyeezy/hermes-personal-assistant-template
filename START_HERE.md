# Start Here

## Try a fictional local walkthrough

Install Python 3.10+, download and extract this repository, and open a terminal
in the extracted folder. Git and Codex are optional.

```sh
python3 scripts/hermes.py start --demo --open
```

Made-up entries go in a separate `private/Hermes_Demo/` directory. No model is
called. Try Career or Nutrition first. Keep the terminal open; Ctrl-C stops it.

## Start your own empty workspace

```sh
python3 scripts/hermes.py start --open
```

This initializes or checks the private knowledge scaffold and local runtime
without replacing existing files. State stays under Git-ignored `private/`.
Providers, gateways, schedules and account connections remain off by default.

Prefer Codex? Open this folder as a project and say:

```text
Read AGENTS.md and help me start Easy Setup.
```

## Troubleshooting

| Symptom | Next step |
| --- | --- |
| `python3` not found | Install Python 3.10+; on Windows try `py -3` |
| Script not found | Run inside the extracted repository folder |
| Browser did not open | Open the localhost URL printed in the terminal |
| Port in use | Add `--port 8766` to the start command |
| Chat repeats your message | Expected offline echo; configure a provider separately |
| Demo refuses existing data | Choose a fresh `--root` before the command; do not overwrite |
| Partial knowledge scaffold | Run `python3 scripts/easy_setup.py check`; inspect existing files |

Example isolated location:

```sh
python3 scripts/hermes.py --root ./private/My_Demo start --demo --open
```

[Full installation](INSTALL_FOR_FRIEND.md) · [Providers](docs/runtime-edition.md) ·
[Safety](docs/safety-and-privacy.md)
