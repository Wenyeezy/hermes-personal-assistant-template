# Digital Assets Lab: crypto and RWA research

Digital Assets Lab is an early research workstream inside HIIS. Its intended
value is to make evidence comparable and uncertainty visible before drawing
a conclusion about a stablecoin or a tokenized real-world asset (RWA).

## Start with two questions

**Stablecoins:** do two observations describe the same asset, chain, time
window and supply definition? A difference is not automatically a depeg,
growth signal or reconciliation failure.

**RWA products:** what do the source documents actually say about the product,
eligibility, transfer restrictions, redemption process and disclosure date?
Missing terms should remain unknown rather than being filled in by a model.

## What is available

| Layer | Status |
| --- | --- |
| Public explanation | This brief and the [HIIS workflow](hiis.md) |
| Public example | [Fictional evidence walkthrough](../examples/digital-assets-evidence-demo.md); readable without an account or API |
| Development implementation | Private work includes registries, timestamped evidence, reconciliation, disclosure revisions, incident records and dashboard read/export paths |
| Public executable replay | Planned; not included in the documentation example |
| Live provider coverage | Not established by this public repository |
| Public plugin distribution | Pending packaging, verification and licensing decisions |

Private implementation evidence does not establish an externally usable
product. The public example intentionally makes no claims about current
market data, issuer quality, trading returns or adoption.

## Shared research model

```text
source and rights metadata
  -> dated observation with explicit scope
  -> comparable evidence, or an unresolved mismatch
  -> reviewed claim and conflicting evidence
  -> incident/change record and later review
```

Reuse HIIS's source registry, evidence handling and research interface.
Development defaults prioritize free/public-source research and local
computation. Paid providers and live integrations require separate decisions;
an existing consumer subscription is not evidence of programmatic API access.

## First reproducible milestone

Convert the fictional walkthrough into an executable replay that accepts
comparable observations, flags different timestamps, keeps native and bridged
supply distinct, and leaves unverified product terms unresolved. Include
expected outputs and a correction/review path.

Readers can already review the example and report a counterexample through
[Community and feedback](../COMMUNITY.md). Execution, wallets and live
financial recommendations are outside this public example's scope.
