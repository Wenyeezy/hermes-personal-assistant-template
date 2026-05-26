# Maintenance Routine

Use this routine whenever the private Hermes setup changes.

---

## Two-Layer Update Rule

Maintain two separate layers:

```text
Private setup layer
  Real logs, real paths, real environment notes

Public sharing layer
  Sanitized docs, templates, diagrams, reusable instructions
```

Do not automatically mirror private files into the public layer.

---

## After Each Major Setup Change

1. Update the private setup log or handoff file.
2. Decide whether the change is useful for public readers.
3. If yes, write a sanitized version into this folder.
4. Remove:
   - API keys;
   - tokens;
   - account IDs;
   - private paths;
   - personal memory;
   - raw logs;
   - identifying screenshots.
5. Re-read `.gitignore`.
6. Review the diff before publishing.

---

## What Belongs Here

Good public content:

- architecture explanations;
- setup principles;
- provider strategy;
- memory policy templates;
- triage workflow templates;
- sanitized troubleshooting notes;
- diagrams;
- examples with fake IDs.

Bad public content:

- real `.env`;
- real `config.yaml`;
- WeChat/iLink tokens;
- provider credentials;
- private memory files;
- raw assistant conversations;
- screenshots with personal information.

---

## Suggested Commit Style

```text
docs: add WeChat gateway notes
templates: add memory triage workflow
docs: document provider safety strategy
examples: add sanitized handoff
```

Keep commits boring and obvious.
