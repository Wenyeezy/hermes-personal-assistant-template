# Hermes Personal Assistant Template

[English](README.md) | [简体中文](README.zh-CN.md)

A practical, local-first personal assistant project built around two product
areas: **Hermes Life**, the primary daily-use system, and **Hermes Research
Labs**, where HIIS and Crypto + RWA are still being developed.

This repository is intentionally **sanitized**. It is meant to show the architecture, rules, and templates without exposing private configuration, API keys, account IDs, or personal memory.

## Start With Hermes Life

Hermes Life is the main product. It organizes personal context, decisions and
daily workflows around portable memory, privacy-aware model routing and clear
action receipts. The maintainer uses the private Life system every day; it is
the most mature part of the wider project.

| Product area | Status | What you can do here |
| --- | --- | --- |
| **Hermes Life** | Primary; daily-tested in the maintainer's private system | Download or fork the public starter, then run [Easy Setup](START_HERE.md) |
| **Hermes Research Labs** | In development; not a finished public plugin | Review [HIIS](docs/hiis.md) and the [Crypto + RWA lab](docs/digital-assets-lab.md) |

The public Life download is currently a sanitized starter package: architecture,
memory templates, deterministic Easy Setup and setup tests. It does not contain
the maintainer's private data or the entire private runtime. Research Labs is a
separate optional area and is not installed by Life Easy Setup.

[Product and package model](docs/product-areas.md) · [Project map](docs/project-map.md) · [Roadmap](ROADMAP.md) ·
[Community and feedback](COMMUNITY.md) · [Contributing](CONTRIBUTING.md)

## Install the Hermes Life Starter

Fork or download the repository, open the whole folder as a Codex project, and
say:

```text
Read AGENTS.md and help me start Easy Setup.
```

Codex will use the repository-local guide and deterministic scaffold. By
default, personal files are generated only under Git-ignored `private/`; no
credential, provider, gateway, schedule, or background service is enabled.

Manual equivalent:

```text
python3 scripts/easy_setup.py check
python3 scripts/easy_setup.py init
python3 scripts/easy_setup.py check
```

See [Start Here](START_HERE.md) and [Codex Easy Setup](docs/easy-setup.md).

---

## Hermes Life: Primary Product

This setup treats Hermes as an assistant layer, not just a chatbot.

Hermes Life is designed to:

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
│   └── privacy_check.py
├── tests/
│   └── test_easy_setup.py
├── docs/
│   ├── easy-setup.md
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
2. Create the private markdown scaffold; do not add credentials yet.
3. Fill response preferences, current state, and one project.
4. Configure one model provider outside the public tracked tree.
5. Test with simple non-sensitive tasks.
6. Define local-only, redacted/aggregate, and cloud-capable zones.
7. Add a messaging gateway only after the core setup works.
8. Add bounded automation last, with explicit owner authorization.

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

For aggregator routes or expensive fallback providers, make opt-in explicit.
Silent fallback can leak context and spend budget before the user notices.

---

## Research Labs: HIIS + Crypto/RWA

Research Labs is the second product area. It contains two connected modules:

- **HIIS** — an evidence-first investment research system that keeps claims
  connected to sources, timestamps, counterevidence and later review;
- **Crypto + RWA Lab** — an early HIIS application for stablecoin evidence,
  digital-asset operations and tokenized real-world asset disclosures.

These modules are still being developed and tested. This repository currently
publishes their scope and a [fictional evidence walkthrough](examples/digital-assets-evidence-demo.md),
not a finished installer or live financial service.

The intended package model is modular:

```text
Hermes foundation
  ├── Hermes Life starter       available now
  └── Research Labs package     planned
        ├── HIIS
        └── Crypto + RWA Lab
```

People should be able to install Life by itself, install Research Labs later,
or combine both through the same Hermes foundation. Personal memory and
research evidence remain separate data domains even when both are installed.
See [Product areas and package model](docs/product-areas.md).

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

- [Product Areas and Package Model](docs/product-areas.md)
- [Codex Easy Setup](docs/easy-setup.md)
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
