# Hermes Personal Assistant Template

A practical template for building a portable personal AI assistant with Hermes Agent, a messaging gateway, cloud/local model providers, and a markdown-based long-term memory layer.

This repository is intentionally **sanitized**. It is meant to show the architecture, rules, and templates without exposing private configuration, API keys, account IDs, or personal memory.

## Fork-to-Codex Easy Setup

Fork or download the repository, open the whole folder as a Codex project, and
say:

```text
Read AGENTS.md and help me start Easy Setup.
```

Codex will use the repository-local guide and deterministic scaffold. By
default, personal files and runtime state are generated only under Git-ignored
`private/`; no credential, cloud provider, gateway, schedule, or background
service is enabled.

Manual equivalent:

```text
python3 scripts/easy_setup.py check
python3 scripts/easy_setup.py init
python3 scripts/easy_setup.py check
python3 scripts/hermes.py init
python3 scripts/hermes.py doctor
python3 scripts/hermes.py serve --open
```

Prerequisite: Python 3.10 or newer. The local starter has no third-party Python
package installation step. Model providers are optional and configured later
with the fork owner's own account, API key, or local model.

This opens a real localhost dashboard with an offline provider and working local
Nutrition, Health, Finance, and Career stores. See [Start Here](START_HERE.md),
[Codex Easy Setup](docs/easy-setup.md), and
[Sanitized Runtime Edition](docs/runtime-edition.md). For Apple Health, see the
[HealthKit Companion guide](docs/healthkit-companion.md).

---

## What This Is

This setup treats Hermes as an assistant layer, not just a chatbot.

The goal is to build a system that can:

- remember stable preferences and project state;
- classify life/project/decision updates before saving them;
- keep long-term memory in portable markdown files;
- use local models for private tasks;
- use cloud providers for non-sensitive or high-quality work;
- connect through owner-gated mobile messaging gateways such as WeChat/Weixin
  and Telegram;
- keep private implementation logs separate from sanitized public instructions.
- keep derived-metric policy in one canonical contract and verify the deployed
  artifact after every dashboard build, not only the source tree.
- prove local-first Career automation with explicit schedule authorization,
  separate completeness/ranking-readiness states, and a real evidence pilot
  that cannot pass by remaining idle.

```text
Weixin / Telegram / Dashboard
  -> one Hermes Gateway service
      -> platform adapter + platform-scoped session
  -> Hermes Agent
  -> Privacy + Memory + Provider Router
      -> Local model for private/simple tasks
      -> Cloud model for non-sensitive or high-quality tasks
      -> Tools for web/files/tasks/health/finance
  -> Portable Markdown Memory Layer
```

---

## Folder Layout

```text
.
├── AGENTS.md
├── START_HERE.md
├── README.md
├── scripts/
│   ├── easy_setup.py
│   ├── hermes.py
│   └── privacy_check.py
├── hermes_lite/
│   ├── config.py
│   ├── providers.py
│   ├── server.py
│   ├── store.py
│   └── static/
├── tests/
│   ├── test_easy_setup.py
│   └── test_runtime.py
├── docs/
│   ├── easy-setup.md
│   ├── runtime-edition.md
│   ├── healthkit-companion.md
│   ├── architecture.md
│   ├── current-state-log.md
│   ├── desktop-mirror-and-voice.md
│   ├── m1-max-ollama-migration.md
│   ├── provider-strategy.md
│   ├── safety-and-privacy.md
│   ├── conversation-preprocessing.md
│   ├── final-write-package.md
│   ├── health-dashboard-workflow.md
│   ├── local-first-career-os.md
│   ├── task-app-integrations.md
│   └── wechat-gateway-notes.md
├── templates/
│   ├── START_HERE.template.md
│   ├── personal_memory_policy.template.md
│   └── personal_memory_triage.template.md
├── examples/
│   └── sanitized-handoff.md
├── config.example.yaml
├── runtime.example.json
├── env.example
└── .gitignore
```

---

## Core Idea

The most important design choice is separating **agent runtime memory** from **portable long-term memory**.

```text
Agent internal memory
  Short, stable, non-sensitive index facts only

Markdown memory layer
  Detailed preferences, project state, decision logs, workflows

No-save zone
  Random chat fragments, sensitive raw data, temporary context
```

This keeps the system easier to migrate across machines, agents, and model providers.

---

## Recommended Memory Structure

```text
AI_Knowledge_Base/
├── START_HERE.md
├── Profile/
│   ├── user_core_profile.md
│   └── response_preferences.md
├── Current_State/
│   └── current_state.md
├── Decision_Logs/
│   └── decision_log_index.md
├── Projects/
│   └── local_ai_system.md
├── Workflows/
│   ├── personal_memory_policy.md
│   └── personal_memory_triage.md
├── Life_Updates/
│   ├── daily_logs/
│   └── weekly_reviews/
└── Index/
    └── master_index.md
```

The user only needs to remember one file:

```text
START_HERE.md
```

Every new assistant should read that file first.

---

## Quick Start

1. Open the fork as a Codex project and start Easy Setup.
2. Create the private markdown scaffold and localhost runtime; do not add
   credentials yet.
3. Open the dashboard and verify local Nutrition, Health, Finance, and Career
   entries with fictional or low-risk test data.
4. Fill response preferences, current state, and one project.
5. Configure one model provider outside the public tracked tree.
6. Test with simple non-sensitive tasks.
7. Define local-only, redacted/aggregate, and cloud-capable zones.
8. Add device, bank, browser, or messaging adapters one at a time.
9. Add bounded automation last, with explicit owner authorization.

When adding more than one chat platform, prefer one long-running Gateway
service with isolated adapters rather than separate daemons that each invent
their own policy. Share privacy, memory, provider, tool, and file-access rules;
keep sessions, media transport, acknowledgements, rate limits, and owner
allowlists platform-scoped.

Do not start with full automatic multi-model routing. Start with:

```text
single provider -> manual switching -> rule-based switching -> automation
```

Common provider options include:

- official APIs, such as OpenAI or Anthropic;
- aggregator platforms, such as OpenRouter;
- local providers, such as Ollama;
- other third-party API gateways, only for non-sensitive and reviewable tasks.

The runnable starter includes disabled-by-default adapters for OpenAI Responses,
Codex CLI, Ollama, and OpenAI-compatible endpoints. Its private route map
supports `/gpt`, `/codex`, `/openai`, `/qwen`, and `/local` after the fork owner
enables the corresponding adapter with their own account or local model.

For aggregator routes or expensive fallback providers, make opt-in explicit.
Silent fallback can leak context and spend budget before the user notices.

---

## Safety Boundary

Do not commit:

- `.env` files;
- API keys;
- provider tokens;
- WeChat/Weixin account IDs or iLink tokens;
- personal memory files;
- raw logs;
- private screenshots/documents;
- real `~/.hermes/config.yaml` if it contains private details.

Use this repository as a template, not as a dump of a live assistant environment.

---

## Docs

- [Codex Easy Setup](docs/easy-setup.md)
- [Sanitized Runtime Edition](docs/runtime-edition.md)
- [HealthKit Companion](docs/healthkit-companion.md)
- [Architecture](docs/architecture.md)
- [Current State Log](docs/current-state-log.md)
- [Desktop Mirror and Voice Input](docs/desktop-mirror-and-voice.md)
- [M1 Max + Ollama Migration Checklist](docs/m1-max-ollama-migration.md)
- [Provider Strategy](docs/provider-strategy.md)
- [Safety and Privacy](docs/safety-and-privacy.md)
- [Conversation Preprocessing Workflow](docs/conversation-preprocessing.md)
- [Final Write Package Workflow](docs/final-write-package.md)
- [Health Dashboard Workflow](docs/health-dashboard-workflow.md)
- [Local-First Career OS](docs/local-first-career-os.md)
- [Task App Integrations](docs/task-app-integrations.md)
- [WeChat Gateway Notes](docs/wechat-gateway-notes.md)
- [Maintenance Routine](docs/maintenance-routine.md)

---

## Templates

- [START_HERE.template.md](templates/START_HERE.template.md)
- [personal_memory_policy.template.md](templates/personal_memory_policy.template.md)
- [personal_memory_triage.template.md](templates/personal_memory_triage.template.md)

---

## License

No open-source license has been granted yet. Copyright remains with the
repository owner while the licensing and intellectual-property strategy is
being reviewed. Contact the owner before redistribution or commercial use.
