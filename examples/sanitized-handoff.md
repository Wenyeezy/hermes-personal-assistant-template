# Sanitized Project Handoff Example

_This is an example handoff file. Replace placeholders with non-sensitive project details._

---

## Current Status

Hermes is installed and connected to a messaging gateway. A portable markdown memory layer has been created. The current cloud provider is used only for non-sensitive tasks.

The messaging gateway has been tested for voice-to-text style input, and a local desktop mirror can be used when the mobile gateway conversation does not sync cleanly to a desktop messaging client.

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
- Gateway/bot conversations may not appear in every desktop client.
- DNS failures can look like provider failures; test DNS and endpoint reachability before rotating API keys.

---

## Next Steps

1. Test gateway reliability.
2. Add task/reminder creation through a local task app integration.
3. Improve memory triage workflow.
4. Move private tasks to a local model host.
5. Keep public templates separate from private memory.
