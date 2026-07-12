# WeChat / Weixin Gateway Notes

This document describes the role of a WeChat/Weixin gateway in a Hermes personal assistant setup.

---

## What The Gateway Does

The gateway lets a messaging app act as a mobile interface to Hermes.

```text
WeChat message
  -> Gateway running on a host machine
  -> Hermes Agent
  -> Model provider
  -> Reply back to WeChat
```

The gateway is not the model. It is only the message bridge.

In a mature setup, it also performs lightweight routing before the model call:

```text
message
  -> command check
  -> privacy check
  -> memory snippet retrieval
  -> provider/tool route
```

---

## Host Requirement

The machine running the gateway must be:

- powered on;
- online;
- not asleep;
- running the gateway process or background service.

Foreground test mode:

```bash
hermes gateway run
```

Verbose replacement mode:

```bash
hermes gateway run --replace -v
```

If the gateway stops, WeChat messages will not be answered.

---

## Good Mobile Use Cases

WeChat/mobile gateway is good for:

- quick notes;
- quick questions;
- voice-to-text commands when the gateway or messaging app provides transcription;
- non-sensitive images;
- project updates;
- memory triage;
- lightweight summaries;
- personal assistant reminders or follow-up prompts.

Provider-control commands should be instant:

```text
/local or /qwen
  switch this session to a local provider

/cloud or /square
  switch this session to the normal cloud provider
```

These commands should not be sent through the full model pipeline.

---

## Better In Terminal

Use Terminal/Codex for:

- installing dependencies;
- editing config;
- updating API keys;
- debugging gateway logs;
- running long commands;
- handling sensitive local files.

Also prefer Terminal/Codex for large PDF batches, long-running web research, and
deep debugging. The mobile gateway can trigger those workflows, but the local
tool path should do the heavy lifting.

---

## Suggested Mobile Instruction

```text
Please do not always use short mobile replies.

For casual chat, be concise.
For images, files, study, technical, or decision questions, use detailed analysis:
1. direct answer first;
2. reasoning and evidence;
3. uncertainty;
4. risks or next steps when useful.
```

---

## Safety Note

The gateway sends user content to whichever model provider Hermes is configured to use.

If the current provider is a low-cost third-party route, avoid sending sensitive screenshots, private documents, credentials, or raw personal memory through the gateway.

Do not silently fallback to an aggregator or expensive provider. If the user has
not explicitly approved that route for the current turn, queue the request for
local handling or ask first.

---

## Speed Notes

Common reasons a gateway feels slower than a dashboard chat:

- it loads too much recent chat history;
- it injects a full tool catalog into simple turns;
- it asks a model to perform route-control commands;
- it sends web/PDF/file tasks to a model without giving it the proper tools;
- it retries provider failures without telling the user;
- it waits for image/PDF extraction on the critical reply path.

Practical fixes:

- keep only a small number of recent turns plus relevant memory snippets;
- use fast command handlers for provider switching;
- route web/PDF/file questions to a tool-enabled path;
- summarize long sessions periodically;
- show visible route notices when provider changes affect privacy, cost, or
  latency.

---

## Desktop Sync Caveat

Some gateway conversations may not sync into the platform's desktop app like ordinary human-to-human chats.

A practical workaround is a local desktop mirror:

```text
Gateway turn
  -> local markdown log
  -> desktop tail/viewer window
```

This gives the desktop machine a receive-only view and an archive, but it does not replace a true desktop chat input.

---

## Multi-Gateway Pattern

A second gateway can improve file, album, long-instruction, and voice workflows
without replacing the first one.

Recommended contract:

```text
Gateway A session ─┐
                   ├─> shared privacy router, tools, memory, and providers
Gateway B session ─┘
```

- keep platform sessions separate;
- use one owner allowlist per gateway;
- disable groups, guests, pairing, and open access by default;
- apply the same secret-file denylist everywhere;
- aggregate rapid album/caption messages before invoking the agent;
- set a clear inbound file ceiling and send larger files through an
  authenticated local dashboard;
- keep voice STT credentials separate from general inference credentials.

When a gateway supports owner-authorized personal file access, allow ordinary
documents only through the normal file-tool policy. Continue to deny credential
stores, OAuth/token files, SSH material, project environment files, and secret
directories on every surface.
