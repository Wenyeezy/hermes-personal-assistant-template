# Sanitized Project Handoff Example

_This is an example handoff file. Replace placeholders with non-sensitive project details._

---

## Current Status

Hermes is installed and connected to a messaging gateway. A portable markdown memory layer has been created. The current cloud provider is used only for non-sensitive tasks.

---

## Important Paths

```text
AI_Knowledge_Base/
  START_HERE.md
  Profile/
  Current_State/
  Decision_Logs/
  Projects/
  Workflows/
  Life_Updates/
  Index/
```

Do not include real API keys, account IDs, or private local paths in a public handoff.

---

## Current Architecture

```text
Messaging App
  -> Hermes Gateway
  -> Hermes Agent
  -> Model Provider
  -> Markdown Memory Layer
```

---

## Current Provider Policy

```text
Local model:
  private memory and sensitive documents

Trusted cloud model:
  high-quality reasoning and writing when acceptable

Low-cost cloud model:
  non-sensitive, reviewable, low-cost tasks
```

---

## Known Issues

- Gateway requires the host machine to stay awake.
- Messaging APIs may be rate-limited or unstable.
- Low-cost provider routes may have wrapper prompts or inconsistent behavior.
- Tool calls may occasionally produce empty final responses.

---

## Next Steps

1. Test gateway reliability.
2. Improve memory triage workflow.
3. Move private tasks to a local model host.
4. Keep public templates separate from private memory.
