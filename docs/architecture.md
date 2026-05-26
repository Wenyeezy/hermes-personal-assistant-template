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
Hermes Agent
  ├── Gateway layer
  ├── Tool layer
  ├── Provider layer
  └── Memory policy layer
        |
        v
Portable Markdown Memory
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

### 2. Hermes Agent

Hermes coordinates:

- model calls;
- tool use;
- file operations;
- memory triage;
- gateway messages;
- workflow execution.

### 3. Model Providers

Use providers by sensitivity and task type:

- local model for private or personal memory tasks;
- standard cloud provider for high-quality reasoning or writing;
- low-cost cloud provider for non-sensitive batch work.

### 4. Portable Memory Layer

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
