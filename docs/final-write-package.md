# Final Write Package Workflow

This document describes a sanitized workflow for turning reviewed conversation exports into a portable memory package for a personal assistant.

It intentionally omits real paths, real people, account data, private memories, and raw logs.

---

## Goal

The final write package is the last checkpoint before long-term memory is loaded into an assistant runtime.

It should separate:

```text
ordinary memory
  -> safe for general assistant retrieval

local-sensitive memory
  -> only loaded through explicit local/private routing

do-not-store policy
  -> exclusions and redaction rules

audit controls
  -> source map, path registry, open questions, leak scan

handoff note
  -> how another machine or assistant session continues the work
```

---

## Recommended Package Layout

```text
final_write_package/
├── README.md
├── ordinary_memory/
│   └── 00_INDEX.md
├── local_sensitive_memory/
│   └── 00_INDEX.md
├── do_not_store/
│   └── 00_INDEX.md
├── audit_controls/
│   ├── 00_INDEX.md
│   ├── path_registry.md
│   ├── path_registry.json
│   ├── entity_resolution.md
│   ├── open_questions.md
│   └── ordinary_leak_scan.md
└── HANDOFF_TO_NEW_HOST.md
```

---

## Audit Rules

Before loading memory into the assistant:

1. Confirm the identity anchor and discard known bad artifacts.
2. Confirm ordinary memory does not contain do-not-store items.
3. Keep sensitive files out of ordinary embeddings.
4. Preserve source traceability without exposing private paths in public docs.
5. Keep unresolved facts marked as `needs_human_review`.
6. Use a path registry so a new host can resolve synced files.

---

## Path Registry

Use aliases instead of hard-coding machine-specific paths:

```text
AI_ROOT=/path/to/private/AI/root
MEMORY_ROOT=${AI_ROOT}/AI_Knowledge_Base
PACKAGE_ROOT=${AI_ROOT}/conversation_migration/final_write_package
LOCAL_SENSITIVE_ROOT=${PACKAGE_ROOT}/local_sensitive_memory
```

When migrating to a new machine, update the path registry first. Do not rewrite every memory file by hand.

---

## Migration Handoff

A handoff note should tell the next machine/session:

- which files to read first;
- where ordinary memory lives;
- where local-sensitive memory lives;
- which files must not be loaded;
- how to verify path aliases;
- which open questions remain;
- the intended ingestion order.

Recommended ingestion order:

```text
ordinary memory
  -> retrieval test
  -> local-sensitive routing setup
  -> local-sensitive memory
  -> cross-contamination test
```

---

## Public Sharing Rule

Public repositories should contain only the workflow and templates.

Do not publish:

- private memories;
- real source paths;
- raw conversation exports;
- account details;
- private object/person profiles;
- screenshots or logs with identifying data.
