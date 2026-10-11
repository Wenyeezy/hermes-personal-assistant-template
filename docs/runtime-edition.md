# Sanitized Runtime Edition

The public repository includes a small, dependency-free runtime so a fork can
open a real local Hermes dashboard before any private integration is connected.

## What Runs Immediately

After Easy Setup approval:

```text
python3 scripts/easy_setup.py init
python3 scripts/hermes.py init
python3 scripts/hermes.py doctor
python3 scripts/hermes.py serve --open
```

The dashboard binds to `127.0.0.1:8765` by default and provides:

- a provider-routed chat surface;
- confirmed nutrition entries and daily totals;
- manual daily activity/health summaries;
- a local finance review ledger;
- a local career opportunity pipeline;
- safe provider readiness status.

Runtime state is stored under Git-ignored `private/Hermes_Runtime/`:

```text
private/Hermes_Runtime/
├── config.json
└── hermes.sqlite3
```

The starter does not install a background service. Closing the terminal stops
the dashboard.

Prerequisite: Python 3.10 or newer. The starter otherwise uses only Python's
standard library; there is no package installation step for the local runtime.

## Provider Router

The generated private configuration starts with only `echo` enabled. Echo is a
local readiness adapter, not an AI model.

### OpenAI Responses API

Enable the adapter, then keep the real key outside the private config:

```text
python3 scripts/hermes.py provider enable openai --default
export OPENAI_API_KEY="your own key"
export HERMES_OPENAI_MODEL="your chosen model"
python3 scripts/hermes.py doctor
```

The adapter calls the Responses API with `store: false`. The public template
does not include, request, or inherit the repository owner's key.

### Codex CLI / ChatGPT Sign-In

Install Codex CLI separately, run `codex`, and sign in with the fork owner's
own ChatGPT account. Then enable the adapter:

```text
python3 scripts/hermes.py provider enable codex_cli --default
```

Hermes invokes `codex exec` in an ephemeral, read-only session and reads only
the final response. It does not copy another person's Codex session, ChatGPT
cookies, API keys, or configuration.

Official references: [Codex CLI](https://learn.chatgpt.com/docs/codex/cli) and
[non-interactive `codex exec`](https://learn.chatgpt.com/docs/non-interactive-mode).

This route is useful for owner-initiated local chat, but it is not a substitute
for a production API service. Expect higher latency than a direct API call.

“ChatGPT connected to Hermes” in this starter means that the fork owner signs
in to their own Codex CLI account and enables `codex_cli`. It does not mean that
the original maintainer's ChatGPT login or developer application is shared.

### Ollama

Install and start Ollama separately, then run:

```text
python3 scripts/hermes.py provider enable ollama --default
export HERMES_OLLAMA_MODEL="your installed model"
```

The default endpoint is loopback-only `http://127.0.0.1:11434`.

### OpenAI-Compatible Provider

Enable `openai_compatible` and set the owner-selected values:

```text
python3 scripts/hermes.py provider enable openai_compatible --default
export HERMES_COMPAT_BASE_URL="your provider base URL"
export HERMES_COMPAT_MODEL="your provider model"
export HERMES_COMPAT_API_KEY="your own key when required"
```

No silent provider fallback is implemented. If a selected provider fails, the
turn fails visibly.

### Named Routes

The chat input recognizes owner-editable route mappings from the private
configuration:

```text
/gpt    -> codex_cli
/codex  -> codex_cli
/openai -> openai
/qwen   -> ollama
/local  -> ollama
```

For example: `/gpt summarize this project`. A route never enables its target
provider or supplies credentials; it only selects an adapter the owner already
configured. Change the private `providers.routes` mapping if `/gpt` should use
the OpenAI API instead of Codex CLI.

## Privacy Routing

Sensitive-looking prompts are refused before OpenAI, Codex CLI, or another
cloud-compatible provider is called unless the owner deliberately changes the
private policy. Private memory is not automatically injected into cloud
prompts, and raw chat history is not persisted by default.

Treat pattern matching as a guardrail, not a complete data-loss-prevention
system. Review prompts and choose a local provider for sensitive work.

## Module Boundaries

### Nutrition

Working now: confirmed/review meal entry; calories, protein, carbohydrates,
fat, fiber, sugar, and sodium; meal/source provenance; goals; date-range
summaries; recent entries; local SQLite; and confirmed-total export in a
HealthKit-compatible payload. The dashboard also implements explicit OpenAI
food-photo estimation as an optional provider action: it
sends the selected image only after the owner presses Estimate, does not store
the image, and returns a `needs_review` candidate that is never auto-confirmed.
Restaurant lookup remains an extension point.

### Health

Working now: manual and JSON daily summaries for steps, active/resting calories,
exercise/standing minutes, distance, sleep, and weight; workout deduplication;
7–90 day history; one canonical row per date; authenticated HealthKit ingest;
sync status; and Nutrition export for owner-approved HealthKit write-back.
HealthKit still requires an iPhone app installed through TestFlight or built
under the fork owner's Apple team. See [HealthKit Companion](healthkit-companion.md).
Do not send medical or raw Health exports to cloud providers by default.

### Finance

Working now: manual local entries, categories, review status, and aggregate
counts. Bank sync and statement import remain optional. Bank credentials,
tokens, account identifiers, raw statements, and transaction databases must
remain private.

### Career

Working now: company, role, status, URL, next-step tracking, pipeline counts,
and recent opportunities. Email import, browser companion, ranking, and bounded
schedules remain optional. The starter has no application submission primitive.

## Commands

```text
python3 scripts/hermes.py init
python3 scripts/hermes.py doctor
python3 scripts/hermes.py doctor --json
python3 scripts/hermes.py serve --open
python3 scripts/hermes.py chat "hello" --provider echo
python3 scripts/hermes.py provider enable codex_cli --default
```

Authenticated HealthKit/TestFlight ingest:

```text
export HERMES_HEALTH_USERNAME="hermes"
export HERMES_HEALTH_PASSWORD="generate-a-unique-password"
python3 scripts/hermes.py health-ingest
```

Use `--root /owner/chosen/private/path` before the subcommand to keep runtime
state elsewhere. Non-loopback dashboard binding requires the explicit
`--allow-network` flag and should be protected by a separate authenticated
proxy before use.
