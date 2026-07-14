# Orientation Brief Contract

Status: implemented as a backend-independent typed contract

## Purpose

An Orientation Brief is the compact human-facing product of an orientation
cycle. It helps a reader see the question, the available perspectives, their
evidence, their disagreements, and the boundary of the current map.

It is not a recommendation, prediction, command, or automatic decision. Its
job is to make a system easier to inspect and to improve the next question.

```text
Orientation Report + read-only perspectives
→ transparent synthesis
→ Orientation Brief
→ human reflection, discussion, and next inquiry
```

## Required content

Every brief records:

1. the question and declared scope
2. the current position and observed or computed changes
3. at least two named perspectives with their full findings
4. agreements and contradictions without majority-vote truth
5. evidence classes, references, assumptions, and provenance
6. boundaries and missing information
7. next questions and a reproduction command

The machine-readable implementation is `nexah.orientation.OrientationBrief`.
The stable Markdown renderer is
`nexah.orientation.render_orientation_brief_markdown`.

## Evidence classes

The brief distinguishes:

| Class | Meaning |
|---|---|
| `declared_input` | explicitly supplied data or scenario |
| `benchmark_model` | published or standard reference model |
| `computed_result` | output of a recorded method |
| `observed_measurement` | independently acquired measurement |
| `observed_outcome` | independently recorded later outcome |
| `assumption` | declared premise used by the report |
| `unknown` | information not established |
| `not_supported` | claim or update excluded by current evidence |

These are provenance roles, not quality scores. A benchmark computation can be
excellent evidence for software behavior without being observed operational
evidence.

## Outcome firewall

The contract rejects an episode reference unless the outcome status is
`observed`. An `observed` status is itself rejected unless the evidence contains
an explicit `observed_outcome` statement with an independent reference.
Conversely, observed-outcome evidence cannot appear under a non-observed
status.

Therefore:

> **NO OBSERVED OUTCOME → NO EPISODIC MEMORY UPDATE**

The contract makes this rule machine-checkable, not merely editorial.

## Perspective synthesis

Each perspective retains its findings, limitations, missing information, and
evidence references. Synthesis may identify agreement or contradiction, but it
does not discard minority findings or convert a vote into truth.

The first reference implementation uses the five Phase IV network probes. The
Phase V IEEE probes will populate the same brief contract after the geometry
frame and operators are implemented.

## Reproduction

Every brief includes:

- one runnable command
- the expected artifacts
- whether the path is intended to be deterministic
- timestamped provenance inherited from the Orientation Report

For Network Orientation, a human-readable brief is available with:

```bash
nexah orient-network APPLICATIONS/datasets/supply_chain.json \
  --focus normal_operation \
  --target system_disruption \
  --recorded-at 2026-07-13T22:45:00+00:00 \
  --format brief
```

## Acceptance evidence

- JSON-compatible typed round-trip
- at least two unique perspectives
- preserved agreements, contradictions, and limitations
- explicit input, computation, assumption, and outcome evidence roles
- enforced outcome-to-episode invariant
- stable Markdown output
- CLI reference path and tests

The brief answers: **What can we currently see, where does the evidence stop,
and what should we ask next?**
