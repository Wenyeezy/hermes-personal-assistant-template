# Architecture

This template uses Hermes as the orchestration layer between user interfaces, model providers, tools, and long-term memory.

---

## High-Level Diagram

```text
User
  ├── Terminal
  ├── Mobile messaging app
  └── Other AI tools
        |
        v
Hermes Gateway
  -> Privacy Router
  -> Memory Router
  -> Provider Router
  -> Tool Layer
  -> Local State + Portable Markdown Memory
```

## Setup and Control Plane

The public template and private runtime are separate trust zones from the first
minute:

```text
public fork opened in Codex
  -> AGENTS.md + START_HERE.md
  -> deterministic knowledge scaffold
  -> optional localhost starter runtime
  -> ignored private markdown + SQLite workspace
  -> optional provider / gateway / tools / schedules, each separately approved
```

The public starter is intentionally useful before any gateway is installed.
Codex can help the owner fill portable markdown files, and the dependency-free
runtime can display empty local modules with an offline echo provider.
Credentials, account connections, device/bank/browser adapters, data imports,
and background jobs are later opt-in phases rather than hidden side effects of
opening the repository.

Keep three ownership zones:

```text
tracked public template: architecture, empty templates, runtime code, validation
ignored private workspace: owner memory, SQLite state, local logs
external secret storage: keys, tokens, account credentials
```

---

## Runtime Layers

### 1. User Interfaces

Possible interfaces:

- terminal;
- WeChat/Weixin gateway;
- Telegram/Discord/Slack-style gateway;
- Codex or other coding agents;
- local model UI such as Open WebUI.

The interface should be treated as an input/output layer. It should not own the long-term memory.

### 2. Gateway Layer

The gateway normalizes messages from chat apps, dashboards, voice input, file
uploads, and phone bridge apps. It should also handle obvious control commands
before invoking a model.

One long-running Gateway service can host multiple platform adapters. Those
adapters should share the same privacy, tool, memory, provider, skill, and file
access policies without sharing one conversation session. Keep each platform
owner-allowlisted, give it a separate session namespace, and disable group/open
access until that surface has its own threat model. A richer adapter can handle
albums, documents, and voice while a lighter adapter remains convenient for
short daily turns.

```text
Weixin adapter ----\
                    -> one Gateway service -> shared routers/tools/state
Telegram adapter --/

Shared: policy, tools, models, memory sources
Isolated: sessions, media transport, delivery, rate limits, allowlists
```

Examples:

```text
/local -> switch to local route
/cloud -> switch to cloud route
/reset -> clear a bad session
```

### 3. Privacy Router

The privacy router decides whether the turn can use a cloud provider, should use
a local model, should ask the user, or should be queued for a local machine.

It should detect:

- raw finance;
- credentials and tokens;
- private IDs or addresses;
- medical/private health exports;
- local-sensitive memory;
- ordinary cloud-capable work.

### 4. Memory Router

Long-term memory should not be pasted wholesale into every turn. A better
pattern is:

```text
small core profile
  + topic triggers
  + top relevant snippets
  + missing-fact queue
```

The gateway retrieves the likely memory snippets before model reasoning. This is
more stable than hoping the model will remember to search.

A mature router benefits from explicit layers:

```text
always-resident core
  -> identity, response style, privacy and routing rules

short Memory Cards
  -> bounded context for local/fast model routes

ordinary topic packs
  -> reviewed academic, career, device, health-summary, lifestyle, or project context

source registry
  -> metadata and paths for deeper reviewed sources

local-sensitive sources
  -> excluded by default; explicit local route only

audit / do-not-store controls
  -> maintenance visibility, never normal answer context
```

Reserve context space for matched source documents. If a large topic pack can
consume the entire prompt budget before source-registry entries are appended,
the registry may look healthy in an inventory test while failing to influence
real answers.

### 5. Hermes Agent

Hermes coordinates:

- model calls;
- tool use;
- file operations;
- memory triage;
- gateway messages;
- workflow execution.

### 6. Model Providers

Use providers by sensitivity and task type:

- local model for private, personal memory, or simple low-latency tasks;
- standard cloud provider for high-quality reasoning or writing;
- low-cost or aggregator provider for non-sensitive batch work, only when the
  user policy allows it.

Avoid silent fallback to aggregators or expensive providers. Fallback can leak
context and spend budget without the user noticing.

### 7. Tool Layer and Local State

The tool layer should own real-world side effects:

- web and PDF extraction;
- task/reminder creation;
- dashboard summary endpoints;
- local file indexing;
- health/food ledgers;
- local-only finance ledgers.

Keep raw finance, private health exports, statements, and secrets out of cloud
tools by default.

For long workflows, split deterministic preparation from user-facing delivery.
The preparation step can build a timestamped local cache; the delivery step
should validate cache freshness, refresh only volatile fields, and fail optional
sections soft. Avoid expensive webpage extraction or auxiliary summarization on
the final delivery path.

### 8. Portable Memory Layer

Long-term memory should live in markdown files, not only inside one agent's internal memory.

Recommended path:

```text
~/AI_Knowledge_Base/
```

or any synced folder you control.

---

## Why Markdown Memory

Markdown is:

- portable;
- human-readable;
- easy to diff;
- easy to back up;
- usable by many agents and editors;
- not tied to one model provider.

---

## Practical Rule

If losing one app would destroy the memory, the memory is in the wrong place.

Use internal memory for quick lookup, and markdown files for durable knowledge.

For cloud/offline continuity, use a small relay only for sanitized context and
queued events. The cloud node should not pretend to be the full local assistant
when a request needs local files, raw finance, or private memory.
