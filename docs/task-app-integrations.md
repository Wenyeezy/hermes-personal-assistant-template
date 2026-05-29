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

## Recommended Routing Policy

A practical split is:

```text
Task/project manager = primary task inbox.
System reminders app = strong time-based alerts.
```

Example routing:

- "Add this task", "put this into my to-do list", or project/study planning -> task manager.
- "Remind me at...", "alert me when...", or anything with a hard notification time -> system reminders.
- If something needs both planning context and a hard alert, create both after the user's intent is clear.

This keeps the task manager useful for organizing work while reserving system reminders for moments where the operating system notification layer matters.

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

For shopping lists, errands, route-based lists, or checklists, prefer one parent task with native checklist items when the task app supports it:

```text
Shopping list request
  -> one parent task
  -> native checklist items
  -> one confirmation message
```

Do not create one task per grocery item unless the user explicitly asks for that. On chat gateways with rate limits, repeated per-item writes and progress replies can create unnecessary API calls and failed sends.

If the app does not expose native checklist creation through its stable automation API, fall back to a single task note with visual checkbox markers such as `[ ]` or `☐`.

---

## Apple Reminders-Style Integration

For system reminder apps, a practical first path is:

```text
Hermes command
  -> CLI helper, AppleScript, or Shortcuts
  -> create reminder
  -> confirmation message
```

Use a fixed default list at first, then add list selection later.

If a stable command-line tool exists for the system reminder app, prefer that over ad hoc scripts. Keep script-based automation as a fallback.

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
