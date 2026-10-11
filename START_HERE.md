# Start Here · Meals + Fitness

## Start your own workspace

Install Python 3.10+, download and unpack the latest preview, then open a
terminal in the extracted folder:

```sh
python3 scripts/hermes.py start --open
```

Windows: `py -3 scripts/hermes.py start --open`.
Convenience launchers: `Start-Hermes.command` (macOS) and `Start-Hermes.bat`
(Windows). Use the terminal command if your OS blocks a downloaded launcher.
No Git, GPT, Codex, account, API key or extra Python dependency is required.

The browser opens an empty **Nutrition + Fitness** dashboard.
Save a meal, log a workout, then check the daily totals.
Finance is off until you explicitly enable it under **Optional modules**.
Career is a separate, disabled extension.

State is written only under Git-ignored `private/` by default and is not
encrypted. Existing configuration and records are preserved. Keep the terminal
open; Ctrl-C stops the runtime. No account or background service is connected.

## Try fictional samples instead

```sh
python3 scripts/hermes.py start --demo --open
```

Made-up meals, activity and a workout go into separate `private/Hermes_Demo/`.
No model is called. Confirm the pending meal and explore Fitness.

## Optional models / gateway

Start manually first. Models are optional, with your own credentials or local
service. Chat is an offline Echo unless separately configured, and does not
automatically save records. See [model setup](docs/runtime-edition.md).

## Troubleshooting

| Symptom | Next step |
| --- | --- |
| Python missing or too old | Install Python 3.10+; Windows can use `py -3` |
| Script not found | Run inside the extracted repository folder |
| Launcher blocked | Use the terminal command above |
| Browser did not open | Open the printed localhost URL |
| Port in use | Add `--port 8766` |
| Chat repeats your message | Expected Echo; models are separate opt-ins |
| Finance or Career absent | Explicitly enable under Optional modules |
| Old config has no module flags | Optional modules default off; existing data is kept |
| Demo refuses existing data | Choose a fresh `--root`; do not overwrite |
| Partial knowledge scaffold | Run `python3 scripts/easy_setup.py check` and inspect files |

Isolated demo location:

```sh
python3 scripts/hermes.py --root ./private/My_Demo start --demo --open
```

Prefer Codex-guided onboarding? Open this folder and ask it to read
`AGENTS.md` and start Easy Setup.
[Full installation](INSTALL_FOR_FRIEND.md) · [Safety](docs/safety-and-privacy.md)
