# Personal Memory Triage Workflow

Use this workflow when the user provides a life, study, project, or decision update.

---

## Categories

Classify content into one or more categories:

| Category | Meaning | Save? |
|---|---|---|
| Short-term context | Useful only for the current conversation | Usually no |
| Long-term memory candidate | Stable preference, background, or pattern | Maybe |
| Project update | Changes project status or next steps | Yes, if relevant |
| Decision log update | Captures a meaningful decision and rationale | Yes |
| Action item | Something the user should do later | Maybe |
| Sensitive/private content | Requires caution | Ask first |
| Ignore | No future value | No |

---

## Output Format

```text
[Triage Result]
- Category:
- Summary:
- Suggested file:
- Reason:
- Sensitive content:
- Recommended action:
```

---

## Write Flow

1. Classify.
2. Check sensitivity.
3. Suggest save location.
4. Wait for user confirmation.
5. Write only the confirmed content.
6. Update index files if needed.

---

## Example

User:

```text
I decided to use a local model for private memory and a cloud provider only for non-sensitive tasks.
```

Assistant:

```text
[Triage Result]
- Category: Decision log update + long-term memory candidate
- Summary: User prefers local models for private memory and cloud models for non-sensitive tasks.
- Suggested file: Decision_Logs/decision_log_index.md and Workflows/personal_memory_policy.md
- Reason: This affects provider routing and privacy policy.
- Sensitive content: No
- Recommended action: Save after confirmation.
```
