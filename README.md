# Hermes Personal Assistant Template

A practical template for building a portable personal AI assistant with Hermes Agent, a messaging gateway, cloud/local model providers, and a markdown-based long-term memory layer.

This repository is intentionally **sanitized**. It is meant to show the architecture, rules, and templates without exposing private configuration, API keys, account IDs, or personal memory.

---

## What This Is

This setup treats Hermes as an assistant layer, not just a chatbot.

The goal is to build a system that can:

- remember stable preferences and project state;
- classify life/project/decision updates before saving them;
- keep long-term memory in portable markdown files;
- use local models for private tasks;
- use cloud providers for non-sensitive or high-quality work;
- connect through a mobile messaging gateway such as WeChat/Weixin.

```text
Phone / Chat App
  -> Hermes Gateway
  -> Hermes Agent
  -> Model Provider
      -> Local model for private tasks
      -> Cloud model for non-sensitive tasks
  -> Portable Markdown Memory Layer
```

---

## Folder Layout

```text
.
├── README.md
├── docs/
│   ├── architecture.md
│   ├── desktop-mirror-and-voice.md
│   ├── m1-max-ollama-migration.md
│   ├── provider-strategy.md
│   ├── safety-and-privacy.md
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

1. Install Hermes Agent.
2. Configure one model provider first.
3. Create a portable markdown memory folder.
4. Add `START_HERE.md`.
5. Add a memory policy and triage workflow.
6. Test with simple non-sensitive tasks.
7. Add a messaging gateway after the core setup works.
8. Move private workflows to a local model host when available.

Do not start with full automatic multi-model routing. Start with:

```text
single provider -> manual switching -> rule-based switching -> automation
```

Common provider options include:

- official APIs, such as OpenAI or Anthropic;
- aggregator platforms, such as OpenRouter;
- local providers, such as Ollama;
- other third-party API gateways, only for non-sensitive and reviewable tasks.

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

- [Architecture](docs/architecture.md)
- [Desktop Mirror and Voice Input](docs/desktop-mirror-and-voice.md)
- [M1 Max + Ollama Migration Checklist](docs/m1-max-ollama-migration.md)
- [Provider Strategy](docs/provider-strategy.md)
- [Safety and Privacy](docs/safety-and-privacy.md)
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

Use whichever license fits your public repo. If unsure, MIT is a simple default for templates and documentation.
