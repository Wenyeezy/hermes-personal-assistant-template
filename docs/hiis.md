# HIIS: Hermes Investment Intelligence System

HIIS is the project's investment research application. Its job is to preserve
the connection between a research conclusion and the evidence behind it.
This page describes the workflow; the public repository does not currently
ship the HIIS plugin implementation or an installer.

## A concrete research problem

Imagine reading a persuasive thesis on Monday, saving several supporting
charts, then seeing a contradictory disclosure on Friday. A useful research
system should help answer: what did the original thesis rely on, which facts
were available at the time, and what now needs to change?

The workflow is:

1. **Collect:** preserve the source, acquisition time and usage restrictions.
2. **Normalize:** distinguish publication time, observation time, scope and units.
3. **Extract:** record a claim without treating ingestion as verification.
4. **Challenge:** attach both supporting and conflicting evidence.
5. **Review:** state the conclusion, uncertainty and invalidation conditions.
6. **Revisit:** record what changed and why.

This creates a research trail rather than a collection of disconnected
summaries. Research evidence remains separate from personal memory and the
personal-finance ledger.

## Development scope

The private development work includes a reference library, source registry,
evidence storage, research relationships, replay components and dashboard
integration. These are maintainer-reported implementation areas, not public
installation promises or independently reproduced benchmarks.

The first public implementation milestone should be a small, fictional-data
replay with inspectable inputs, expected outputs and a clear failure case.
The [roadmap](../ROADMAP.md) keeps that milestone separate from this
documentation release.

## Why Digital Assets Lab belongs here

Crypto and RWA research needs the same source, time, scope and review controls.
The Lab therefore extends HIIS's evidence workflow rather than introducing
another unrelated memory store or research dashboard.

Start with the [Lab brief](digital-assets-lab.md) and
[fictional walkthrough](../examples/digital-assets-evidence-demo.md).
Feedback is especially useful when it identifies a claim the workflow might
mistakenly accept, an ambiguous status, or a missing piece of provenance.

## Publication boundary

This repository presents research methods and development progress. It does
not provide an installed brokerage connection, trade execution, live
recommendation service or validated investment performance. Any future
public implementation will need its own reproducible acceptance evidence.
