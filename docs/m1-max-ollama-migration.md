# M1 Max + Ollama Migration Checklist

Use this checklist when moving a Hermes personal assistant from a daily-use machine to an always-on local model host.

The goal is to make the local host the private/default runtime while keeping cloud providers available only for non-sensitive fallback work.

---

## Target Architecture

```text
Phone / chat app / terminal
  -> Hermes gateway
  -> Hermes Agent on always-on Mac
  -> Ollama local model for private/default tasks
  -> Cloud provider only for non-sensitive fallback
  -> Portable markdown memory layer
```

---

## Before Migration

Confirm the current setup is healthy before changing hosts:

1. Hermes runs on the current machine.
2. The gateway can receive and reply to test messages.
3. The portable markdown memory folder is synced and readable.
4. The public sharing repo contains only sanitized files.
5. There is a current private handoff note outside the public repo.

Do not migrate by copying raw logs, real `.env` files, provider keys, or gateway tokens into a public repository.

---

## Prepare The New Host

On the always-on Mac:

1. Install or update Hermes.
2. Install Ollama.
3. Pull at least one local model suitable for private tasks.
4. Confirm the portable markdown memory folder has synced.
5. Confirm terminal access to both Hermes and Ollama.
6. Run a simple local model test before changing the gateway.

Example checks:

```bash
hermes --version
ollama list
ollama run <model-name> "Reply with OK"
```

---

## Switch Provider Strategy

Use a staged switch:

```text
Stage 1: Keep existing cloud provider as default.
Stage 2: Add Ollama as a manually selectable provider.
Stage 3: Test private memory and document tasks on Ollama.
Stage 4: Make Ollama the default provider.
Stage 5: Keep cloud providers as explicit fallback only.
```

Avoid full automatic routing during the first migration pass. Manual switching is easier to inspect and less likely to leak sensitive context.

---

## Move The Gateway

Only one host should actively run the same messaging gateway account at a time.

Recommended sequence:

1. Stop the gateway on the old machine.
2. Start the gateway on the new host in foreground test mode.
3. Send a simple non-sensitive test message.
4. Send a small image or file test if the gateway supports it.
5. Check logs for polling, login, or provider errors.
6. Only then consider a persistent service setup.

Example foreground command:

```bash
hermes gateway run --replace -v
```

Keep the old host available until the new gateway has survived a few normal usage sessions.

---

## Memory Safety Checks

Before using the migrated setup for private work:

1. Re-read the memory policy.
2. Confirm sensitive content defaults to the local provider.
3. Confirm cloud fallback requires an explicit choice.
4. Keep long-term memory in markdown, not only inside Hermes internal memory.
5. Do a test memory triage with non-sensitive content.

If provider routing is uncertain, pause and ask before saving or processing private content.

---

## Rollback Plan

Keep a simple rollback path:

1. Stop the gateway on the new host.
2. Restart the gateway on the old machine.
3. Restore the previous default provider if needed.
4. Record what failed in the private setup log.
5. Add only sanitized lessons learned to the public template.

Migration is complete only when normal daily use works from the new host and the old host is no longer needed for gateway availability.
