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
```

Also avoid committing raw screenshots, exported chat logs, and provider response logs unless they are sanitized.

---

## Redaction Checklist

Before publishing:

- remove API keys and tokens;
- remove real account IDs;
- remove personal names unless intentionally public;
- remove private file paths if they reveal personal data;
- replace real model endpoint keys with placeholders;
- sanitize logs;
- review images for private content.
