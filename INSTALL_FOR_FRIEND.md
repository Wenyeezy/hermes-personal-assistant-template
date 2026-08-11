# Install Hermes From a Fork

This guide is for a new owner installing the sanitized Hermes starter on their
own Mac and iPhone. Your accounts, credentials, Health data, and private memory
remain separate from the template maintainer.

## 1. Fork and Open in Codex

Prerequisites:

- macOS with Python 3.10 or newer;
- a GitHub account;
- Codex Desktop, or another Codex environment that can open the whole folder.

Fork this repository into your own GitHub account, clone or download your fork,
then open the entire repository folder in Codex. Tell Codex:

```text
Read AGENTS.md and help me start Easy Setup.
```

Codex should explain the privacy boundary before creating local state. The
generated `private/` directory is ignored by Git.

## 2. Manual Setup Equivalent

If you prefer Terminal:

```text
python3 scripts/easy_setup.py check
python3 scripts/easy_setup.py init
python3 scripts/easy_setup.py check
python3 scripts/hermes.py init
python3 scripts/hermes.py doctor
python3 scripts/hermes.py serve --open
```

The last command opens the local Hermes Dashboard. Keep that Terminal window
open while using it; press Control-C to stop.

Working without an account:

- Dashboard;
- private knowledge scaffold;
- Nutrition records, goals, summaries, and review flow;
- manual Health summaries and workouts;
- Finance review ledger;
- Career opportunity tracker;
- offline echo provider.

## 3. Optional GPT/Codex Connection

Install Codex CLI separately and sign in with your own ChatGPT account. Verify:

```text
codex --version
codex
```

Then enable it for Hermes:

```text
python3 scripts/hermes.py provider enable codex_cli --default
python3 scripts/hermes.py doctor
```

Dashboard chat can now use `/gpt` or `/codex`. This does not use the template
maintainer's ChatGPT account.

## 4. Optional OpenAI Food-Photo Estimates

Food-photo estimation is a separate explicit cloud action and requires your own
OpenAI API key:

```text
export OPENAI_API_KEY="your-own-key"
export HERMES_OPENAI_MODEL="gpt-5.6-luna"
python3 scripts/hermes.py provider enable openai
python3 scripts/hermes.py serve --open
```

Hermes does not store the selected image. The returned estimate is always marked
`needs_review`; inspect portions and values before confirming it.

## 5. Optional Apple Health Companion

The maintainer may invite you by email to a private TestFlight group. On iPhone:

1. Install Apple's TestFlight app.
2. Open the invitation using the same Apple Account.
3. Install Hermes Health.
4. Grant only the Apple Health permissions you want Hermes to use.

On the Mac, create a unique password and start the authenticated ingest service:

```text
export HERMES_HEALTH_USERNAME="hermes"
export HERMES_HEALTH_PASSWORD="create-your-own-long-password"
python3 scripts/hermes.py health-ingest --host 0.0.0.0 --port 9121
```

Find the Mac Wi-Fi address:

```text
ipconfig getifaddr en0
```

While the iPhone and Mac are on the same trusted Wi-Fi, configure Hermes Health:

```text
Endpoint: http://MAC_WIFI_ADDRESS:9121/health/import
Username: hermes
Password: the unique password created above
```

Allow the incoming connection if macOS asks. Test authorization in the app,
then sync today or recent days. Do not expose port 9121 directly to the public
internet.

## Privacy Rules

- Never commit `private/`, `.env`, SQLite databases, raw Health exports, photos,
  statements, or chat exports.
- Never reuse or request the maintainer's API keys, Health password, Apple
  account, signing certificate, or developer credentials.
- Use fictional or low-risk test data first.
- Keep the Dashboard on `127.0.0.1`; only the authenticated Health ingest service
  should listen on the private LAN.
- Add bank, messaging, browser, and scheduled automation only as separate opt-ins.

For details, read [Runtime Edition](docs/runtime-edition.md),
[HealthKit Companion](docs/healthkit-companion.md), and
[Safety and Privacy](docs/safety-and-privacy.md).
