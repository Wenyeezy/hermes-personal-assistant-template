# Conversation Preprocessing Workflow

This document describes a conservative workflow for turning exported AI conversations into durable personal-assistant memory.

The goal is not to train a model directly. The goal is to transform messy exports into reviewed, portable Markdown files that an assistant can read later.

---

## Roles

```text
Preprocessing agent
  -> cleans exports and prepares structured files

Strong synthesis model
  -> performs a second-pass review or condensation

Proctor/auditor agent
  -> checks the synthesis before anything becomes long-term memory

Markdown knowledge base
  -> stores the durable result

Assistant runtime
  -> reads the knowledge base when needed
```

This separation makes the system easier to debug. The assistant runtime should not be the only place where memory exists.

---

## First Pass: Local Preprocessing

Good first-pass tasks:

- preserve raw exports untouched;
- remove embedded base64 images from model-facing Markdown;
- save cleaned Markdown separately;
- extract embedded images into a local archive if visual fallback may be useful;
- create an inventory of files, sizes, turns, and removed images;
- identify obvious contradictions or user corrections;
- create a domain-specific mapping file for names, aliases, and definitions.

For domains where naming matters, such as wardrobe, tools, projects, or people, keep the user's original names as canonical handles. Translations or English descriptors should clarify the handle, not replace it.

---

## Second Pass: Strong-Model Review

Use a stronger model for review and synthesis only after the first pass has reduced the noise.

Suggested inputs:

- cleaned project inventory;
- domain memory guide;
- name/alias mapping;
- correction log;
- selected excerpts from cleaned conversations;
- visual fallback protocol, if relevant.

Suggested outputs:

- proposed long-term memory file;
- short assistant index;
- uncertainty list;
- corrections or conflicts to review;
- items that should stay in archive only.

Do not treat this as model training. It is document synthesis and memory curation.

---

## Proctoring

Before writing to long-term memory, a proctor/auditor should check:

- Did the synthesis invent facts?
- Did it preserve user-corrected terminology?
- Did it over-compress important details?
- Did it mix up similarly named items?
- Did it include sensitive details that should remain archived only?
- Did it write to the correct private paths?
- Can the result be repaired later from the raw archive and intermediate files?

If a second-pass model runs outside the proctor's terminal, save the prompt, terminal output, and generated files so they can be reviewed.

---

## Visual Fallback

When exported conversations contain embedded base64 images:

- remove base64 from regular model-facing Markdown;
- optionally extract images into a local archive;
- create an index that maps image ids to likely items or source turns;
- inspect only the smallest relevant image set when text is ambiguous.

Avoid sending images to cloud vision models unless the user accepts that provider/privacy tradeoff. Prefer local vision for sensitive material when available.

---

## Durable Memory

The final write should be a normal Markdown file in the private knowledge base.

Keep runtime assistant memory short:

```text
Detailed project/profile memory exists at: /path/to/private/knowledge-base/file.md
```

This keeps the assistant lightweight while preserving the full source of truth in files that can be synced, inspected, backed up, and repaired.

