# Task App Integrations

This document outlines a conservative path for connecting Hermes to task apps such as Things, Apple Reminders, or similar local task managers.

The goal is to let a mobile gateway become a practical command surface:

```text
Mobile text or voice
  -> Hermes
  -> Parse task intent
  -> Add task or reminder
  -> Confirm back to the user
```

---

## Start Write-Only

Begin with write-only actions before reading a user's entire task database.

Good first actions:

- add a task title;
- add a due date;
- add a short note;
- add a source label such as "from mobile assistant";
- confirm what was created.

Avoid starting with:

- full task database reads;
- automatic task prioritization;
- automatic rescheduling;
- private project inference from task history.

---

## Example Commands

```text
Add task: submit the homework tomorrow at 10 AM.
Remind me at 4 PM to call the dentist.
Put "review migration checklist" into my task app.
```

For ambiguous commands, ask a short clarification before writing.

---

## Things-Style Integration

Many local task apps support one or more automation surfaces:

- URL schemes;
- AppleScript;
- Shortcuts;
- command-line helper scripts.

A safe first milestone:

```text
Hermes command
  -> local helper script
  -> task app automation
  -> confirmation message
```

Keep the helper script small and explicit. It should create a task only from structured input, not from arbitrary shell text.

---

## Apple Reminders-Style Integration

For system reminder apps, a practical first path is:

```text
Hermes command
  -> AppleScript or Shortcuts
  -> create reminder
  -> confirmation message
```

Use a fixed default list at first, then add list selection later.

---

## Privacy Boundary

Task data often contains private information even when it looks mundane.

Recommended rule:

```text
Write-only task creation can be automated after clear user intent.
Reading private task lists should wait for local/private model handling or explicit user consent.
```

Do not automatically save task commands into long-term memory. If a task reveals a stable preference, decision, or project update, run memory triage first.

---

## Suggested Milestones

1. Add a single task through a local helper.
2. Add a dated reminder through a local helper.
3. Trigger both helpers from a mobile gateway command.
4. Add confirmation messages.
5. Add ambiguity handling.
6. Add read-only task summary after privacy rules are clear.
7. Move deeper task-list reading to a local/private model host when available.
