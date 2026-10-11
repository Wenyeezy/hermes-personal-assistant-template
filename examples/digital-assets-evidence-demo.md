# Fictional evidence walkthrough

Everything below is synthetic. DEMO Dollar and DEMO Treasury are invented
names. Values and terms do not describe any real issuer, asset, investment or
market. This is a reading exercise, not an executable service or live feed.

## Case 1: two numbers that should not be compared yet

| Observation | As-of time (UTC) | Definition | Units |
| --- | --- | --- | ---: |
| A | 2026-01-01 12:00 | DEMO Dollar native supply on Chain A | 1,000 |
| B | 2026-01-01 12:15 | DEMO Dollar native plus bridged supply on Chain A | 1,200 |

A naive summary might say native supply grew 20%. That interpretation compares
different supply definitions. The correct first result is **not comparable**.
Growth measurement normally uses different timestamps, but it still needs a
consistent definition at both times. A same-time reconciliation is a separate
question and requires observations aligned to the same time.

Expected research record:

```text
claim: "DEMO Dollar native supply grew 20%"
status: unresolved
reasons:
  - native and native-plus-bridged definitions differ
  - the native component of observation B has not been established
next evidence:
  - consistently defined native observations at both timestamps
  - a bridged-supply breakdown aligned with observation B
```

Now suppose a third fictional record describes 200 bridged units at 12:15.
Subtracting it from B yields 1,000. First verify that the records use compatible
scope and methodology and that the bridged component is actually included in
B. If those checks pass, the two native observations support zero change
between these timestamps, not the original 20% growth claim. Arithmetic alone
does not establish those comparability conditions.

## Case 2: a tokenized product with incomplete terms

| Field | Fictional source record |
| --- | --- |
| Product | DEMO Treasury |
| Source | Synthetic product note, revision 1 |
| Document date | 2026-01-01 |
| Redemption | Monthly window, according to the fictional note |
| Eligibility | Not provided |
| Transfer restrictions | Not provided |
| Independent corroboration | Not provided |

Expected conclusion: **partial product record; review required**. A token
label and a redemption window do not supply the missing eligibility or
transfer terms. Preserve the document revision and request the missing
evidence before making a stronger statement.

## Try it

Read the two cases and answer: which claim is unresolved, why, and what
specific evidence would change the result? Then change one field, such as the
timestamp or supply definition, and check whether your answer changes.

This exercise can be done by a human or with an assistant. No model-specific
capability is required. A useful feedback report includes the edited fictional
input, your expected conclusion, and the reasoning step that was unclear.
Use [Community and feedback](../COMMUNITY.md).
