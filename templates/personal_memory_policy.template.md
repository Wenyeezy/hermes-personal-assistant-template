# Personal Memory Policy

This file defines how AI assistants should handle long-term memory.

---

## Storage Layers

### 1. Internal Agent Memory

Use only for short, stable, non-sensitive index facts.

Examples:

- preferred language;
- location of the memory folder;
- stable workflow preferences.

### 2. Portable Markdown Memory

Use for:

- detailed user preferences;
- project state;
- decision logs;
- workflows;
- current priorities;
- reusable context.

### 3. Do Not Save

Do not save:

- random chat fragments;
- temporary context;
- sensitive raw content;
- credentials;
- private documents without explicit approval.

---

## Write Rules

1. Classify first.
2. Ask before writing.
3. Explain what will be saved and where.
4. Prefer summaries over raw transcripts.
5. Avoid duplicate entries.
6. Keep files small and focused.
7. Do not write sensitive information unless the user explicitly approves and chooses the storage location.

---

## Sensitive Content Handling

If sensitive content appears:

1. Pause.
2. Describe the type of sensitivity without repeating the secret.
3. Offer options:
   - redact and continue;
   - process locally;
   - save only a summary;
   - do not save;
   - continue only after explicit user confirmation.

---

## Provider Safety

Use local models for private memory whenever possible.

Use cloud providers only when the user accepts the tradeoff.

Use low-cost third-party providers only for non-sensitive, reviewable tasks.
