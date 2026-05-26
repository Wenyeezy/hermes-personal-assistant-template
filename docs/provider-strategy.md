# Provider Strategy

The provider strategy is intentionally simple at first.

Do not begin with full automatic model routing. It is harder to make reliable than it looks.

---

## Recommended Progression

```text
Level 1: Single provider
Level 2: Manual switching
Level 3: Rule-based switching
Level 4: Automatic routing with fallback
```

Start at Level 1 or Level 2.

---

## Provider Roles

### Local Provider

Best for:

- private memory;
- personal documents;
- sensitive project notes;
- repeated local workflows;
- offline or semi-private tasks.

Example:

```text
Hermes -> Ollama -> local model
```

### Standard Cloud Provider

Best for:

- high-quality writing;
- complex reasoning;
- coding assistance;
- tasks where reliability matters more than cost.

Examples:

- official OpenAI API;
- official Anthropic API;
- OpenRouter or similar aggregator platforms.

### Low-Cost Cloud Provider

Best for:

- non-sensitive batch work;
- casual chat;
- rough summaries;
- low-risk image or text analysis;
- drafts that will be reviewed.

These providers can be useful, but they should be chosen by the user based on price, reliability, privacy policy, and compatibility.

Avoid using low-cost third-party routes for sensitive memory or private raw documents.

---

## Example Routing Rules

```text
Default:
  Use local model for private/personal tasks.

Use cloud when:
  - user explicitly requests cloud;
  - task needs stronger reasoning;
  - local model fails;
  - task is non-sensitive and cost matters.

Pause and ask when:
  - content includes credentials;
  - content includes health/finance/school-private details;
  - content includes personal identity documents;
  - content should be saved into long-term memory.
```

---

## Why Not Full Auto-Routing First

Automatic routing has hidden complexity:

- providers differ in API behavior;
- models have different context limits;
- vision/tool support varies;
- prompt classification can be wrong;
- fallback logic can leak context unexpectedly;
- extra routing calls add cost and latency.

Semi-automatic rules are usually more reliable for a personal assistant.
