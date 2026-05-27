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

---

## Better In Terminal

Use Terminal/Codex for:

- installing dependencies;
- editing config;
- updating API keys;
- debugging gateway logs;
- running long commands;
- handling sensitive local files.

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
