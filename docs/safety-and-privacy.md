# Safety and Privacy

This project is designed around one principle:

> Sensitive information should not be automatically sent to a model provider or saved into long-term memory.

---

## Sensitive Content Examples

Treat these as sensitive:

- API keys;
- passwords;
- tokens;
- private keys;
- identity documents;
- health information;
- financial information;
- private school/work documents;
- raw personal relationship details;
- precise addresses or private locations;
- any content the user labels as private.

---

## Triage Before Saving

Before saving a user update, classify it:

```text
short-term context
long-term memory candidate
project update
decision log update
action item
sensitive/private content
ignore
```

Then ask for confirmation before writing.

---

## Provider Safety Rule

```text
Local provider:
  Best for private/sensitive tasks.

Trusted cloud provider:
  Use when quality is more important and user accepts cloud processing.

Low-cost third-party provider:
  Use only for non-sensitive and reviewable tasks.
```

Aggregator or fallback provider:

```text
Use only after explicit same-turn authorization.
Do not silently switch sensitive/private content to this route.
```

---

## Data Zones

Use three practical zones:

```text
Zone A: local-only
  raw finance, statements, account details, tokens, credentials,
  private identity documents, medical/private health exports,
  local-sensitive memory, private screenshots

Zone B: redacted or aggregate
  review counts, account aliases, category totals, sanitized health summaries,
  status-only sync reports

Zone C: ordinary cloud-capable
  public research, drafting, non-sensitive planning, sanitized project notes
```

The gateway should route Zone A locally by default. Zone B can be shown on a
dashboard or sent to cloud only when the user policy allows it. Zone C may use
the normal high-quality route.

Health and food data need project-specific policy. Some users may allow daily
activity summaries or confirmed food rows through a small cloud relay, while
medical-grade exports and unrelated private photos remain local-first.

---

## What Not To Commit

Never commit:

```text
.env
*.key
*.pem
*.token
secrets/
private/
real-memory/
logs/
*.sqlite3
```

Also avoid committing raw screenshots, exported chat logs, provider response
logs, and runtime databases unless they are sanitized. The public runtime keeps
module rows in Git-ignored local SQLite and does not persist raw chat history by
default. Enabling local chat logging does not make that database safe to
publish.

---

## Redaction Checklist

Before publishing:

- remove API keys and tokens;
- remove real account IDs;
- remove personal names unless intentionally public;
- remove private file paths if they reveal personal data;
- remove real hostnames and callback URLs;
- replace real model endpoint keys with placeholders;
- sanitize logs;
- review images for private content.
