# Product areas and package model

Reviewed: 2026-09-22.

Hermes has two product areas with different maturity and release paths.

## 1. Hermes Life

Hermes Life is the primary product. The maintainer's private system is used
daily across personal context, decisions and bounded workflows. That repeated
owner use makes Life the most mature part of the project.

The public repository currently provides a sanitized Life starter:

- portable Markdown memory templates;
- a deterministic, Git-ignored private workspace scaffold;
- architecture and privacy guidance;
- setup and privacy checks.

The starter is publicly reproducible, but it is not a packaged copy of the
complete private runtime. Features documented from private daily use should be
published one bounded module at a time with their own installation and tests.

## 2. Hermes Research Labs

Research Labs is in development and contains:

- **HIIS**, the evidence and research layer;
- **Crypto + RWA Lab**, a focused HIIS application for digital-asset and
  tokenized-product evidence.

Current public materials explain the method and provide fictional examples.
They do not establish a finished installer, live data coverage, investment
performance or execution capability.

## Separate installs, shared foundation

The target distribution model is:

```text
Hermes foundation
  ├── Life package
  │     └── personal memory and daily workflows
  └── Research Labs package
        ├── HIIS evidence layer
        └── Crypto + RWA module
```

Life should work by itself. Research Labs should also have an explicit
standalone installation path. When combined, both may share the Hermes gateway,
provider routing and tool framework, while preserving separate storage and
privacy policy for personal memory and research evidence.

## Release labels

| Label | Meaning |
| --- | --- |
| Available | A public reader can follow the repository instructions and reproduce the stated result |
| Daily-tested privately | The maintainer uses it repeatedly, but the full implementation is not necessarily public |
| In development | Design or implementation exists, but public installation and independent reproduction are incomplete |
| Planned | Direction only; no current implementation promise |

These labels keep private maturity, public packaging and external validation
from being treated as the same fact.
