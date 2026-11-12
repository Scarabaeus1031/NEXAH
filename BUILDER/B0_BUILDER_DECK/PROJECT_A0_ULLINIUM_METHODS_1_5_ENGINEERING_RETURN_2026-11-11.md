# B0 Builder Return — A0 Ullinium Methods 1–5

Date: `2026-11-11`
Status: `COMPLETE_LOCAL_ENGINEERING_CLASSIFICATION / HOLD / NO_NEW_BUILD`
Owning source: A0 Science package
Builder role: capability classification, architecture consequence and return

## Goal

Translate the preregistered Methods 1–5 comparator into an exact Builder
statement: what the current A0/NEXAH machinery can do, what it does not do and
which architectural consequence may guide later bounded assemblies.

## Received evidence

The frozen population contains `10,000` deterministic labelled gluing cases
across five graph families and three overlap selectors. The result is:

| Method | Exact labelled Return | Corruption / false-seam detection |
|---|---:|---:|
| adjacency-only | `0 / 10,000` | not sufficient |
| property graph | `10,000 / 10,000` | `10,000 / 10,000` |
| incidence graph | `10,000 / 10,000` | `10,000 / 10,000` |
| cospan / pushout | `10,000 / 10,000` | `10,000 / 10,000` |
| NEXAH receipt | `10,000 / 10,000` | `10,000 / 10,000` |

The NEXAH representation uses `2.0363×` the mean payload of the best standard
cospan representation in this bench. It is neither more exact nor more robust
than that comparator.

## Capability statement

### Demonstrated bounded Engineering capability

NEXAH can package a labelled Return with explicit layer, seam, loss, Return
status and claim boundary; replay the declared reconstruction; and fail closed
on the injected corruption and false-seam cases.

This is a **governance-envelope capability** around a reconstruction core. It
is useful when the engineering object must preserve not only the returned
graph but also the declared cut, loss and decision boundary.

### Explicit non-capability

The result does not establish:

- a new graph algorithm;
- superior reconstruction or corruption detection;
- a universal data format or runtime;
- lower storage or transport cost;
- external Human utility, production readiness or scientific novelty.

## Architecture consequence

The smallest defensible Builder architecture is not a proprietary replacement
for property graphs, incidence graphs or cospans. It is a replaceable-core
assembly:

```text
DECLARED SOURCE + SELECTOR
  → STANDARD RECONSTRUCTION CORE
  → NEXAH GOVERNANCE ENVELOPE
       layer · seam · loss · Return status · claim boundary
  → RECEIPT + REPLAY + FAIL-CLOSED CHECK
  → HUMAN RETURN / ABSTAIN / STOP
```

The core remains substitutable. The envelope must expose overhead and cannot
claim algorithmic privilege. A later real case may test whether the explicit
receipt improves review, audit or Human decision quality; that later test is
not activated here.

## Builder disposition

- existing A0/B0 identity reused;
- new Build, Capability ID, Runtime, Family or product: `0`;
- active-build effect: `0`;
- Engineering Assembly: add one bounded, non-privileged governance-envelope
  row;
- Builder Vision: retain the envelope as an architectural principle;
- next permitted action: `HOLD` until a separately authorized real case names
  task, baseline, Human outcome and STOP.

## NSNavigator return

Reused identity: `NEXAH_AX0_QMODE_FOUNDATION_PACKAGE` and existing A0
orientation evidence binder. The Builder return changes only source
currentness and descriptive projections. New nodes `0`; relations `0`;
aliases `0`; canonical counts remain `329/29` base and `332/32` composed.

## Verification sources

- [Frozen preregistration](../../../../30%20SCIENCE%20LAB/NEXAH-Science-Lab/RESEARCH_PROGRAM_B_MATHEMATICAL_FOUNDATIONS/AXIOM0_QMODE_ORIENTATION_TO_MEASUREMENT_FOUNDATION_PACKAGE_2026-10-01/A0_BOOK/results/A0_ULLINIUM_METHODS_1_5_PREREGISTRATION_2026-11-11.md)
- [Machine result](../../../../30%20SCIENCE%20LAB/NEXAH-Science-Lab/RESEARCH_PROGRAM_B_MATHEMATICAL_FOUNDATIONS/AXIOM0_QMODE_ORIENTATION_TO_MEASUREMENT_FOUNDATION_PACKAGE_2026-10-01/A0_BOOK/results/a0-ullinium-methods-1-5-result-2026-11-11.json)
- [Scientific position](../../../../30%20SCIENCE%20LAB/NEXAH-Science-Lab/RESEARCH_PROGRAM_B_MATHEMATICAL_FOUNDATIONS/AXIOM0_QMODE_ORIENTATION_TO_MEASUREMENT_FOUNDATION_PACKAGE_2026-10-01/A0_BOOK/A0_SCIENTIFIC_POSITION_REPORT.html#ullinium-methods-1-5-benchmark-20261111)

## Boundary

This return records an Engineering capability and its limit. It creates no
Study, Finding, scientific claim promotion, build activation, commit, push,
deployment, publication or outreach authority.
