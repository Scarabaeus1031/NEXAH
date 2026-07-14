# Observed-Evidence Bridge

Status: Phase V Work Package H — documented admission path, no external dataset
admitted

## Purpose

This bridge defines how a later licensed, timestamped measurement source may
enter the existing NEXAH contracts without being confused with a benchmark,
scenario, computation, or model output.

It is an admission protocol, not evidence that such a source is already
available.

## Admission sequence

```text
source registration and license
→ immutable raw capture and checksum
→ entity, topology, unit, and time alignment
→ typed observations plus provenance and uncertainty
→ frozen development/evaluation split
→ orientation using evidence available at the cutoff
→ independently acquired later outcome
→ six-check outcome firewall
→ authorized episode write or explicit rejection/indeterminate result
```

## 1. Acquire and preserve

Before any representation or method selection, record:

- source owner and stable source identifier;
- acquisition method and timezone-aware acquisition timestamp;
- license, redistribution permission, and access restrictions;
- immutable raw checksum and storage location;
- dataset version and correction policy;
- privacy, security, and redaction requirements.

If redistribution is forbidden, publish only permitted derived evidence and a
verification procedure. Never copy restricted raw records into the repository.

## 2. Align semantics

Every admitted observation must identify:

- observation and source record IDs;
- event time and recording time;
- topology or schema identity valid at that time;
- entity identity and alignment procedure;
- variable name, unit, reference convention, and scale;
- missingness, quality flags, exclusions, and transformations;
- provenance and claim-specific uncertainty.

Unknown alignment or uncertainty remains unknown. It is not repaired with a
silent default.

## 3. Freeze evaluation before inspection

The case manifest must predeclare:

- the research question and admissible claims;
- development interval or entities;
- locked evaluation interval or entities;
- representation and method-selection cutoff;
- outcome definition and observation window;
- exclusions and stopping rules;
- metrics and insufficiency policy.

Evaluation outcomes cannot be used to choose methods or parameters. A revised
method requires a new manifest version and a new evaluation record.

## 4. Map into NEXAH

| External record | NEXAH contract | Required boundary |
|---|---|---|
| timestamped measurement | `Observation` plus `Evidence` | source, time, entity, unit, provenance, uncertainty |
| representation context | `OrientationState` | representation and topology scope remain explicit |
| generated report | `OrientationReport` | references only evidence available at orientation time |
| authored change | `ScenarioRecord` | never relabeled as observation |
| model or solver output | `ComputationResultRecord` | never relabeled as observed outcome |
| independently recorded later result | `ObservedOutcomeRecord` | source relation and method-selection relation declared |
| admitted history | `Episode` | only through `put_episode_if_authorized(...)` |

## 5. Outcome admission

An observed outcome is eligible only when all firewall checks pass:

1. explicit `observed_outcome` type;
2. observation time later than the orientation cutoff;
3. independently declared source with recorded basis;
4. matching orientation identity and scope;
5. no evidence unavailable at orientation time in the report;
6. no outcome leakage into method or parameter selection.

Unknown source independence or selection history produces `indeterminate`, not
acceptance. A failed condition produces `rejected`.

> **NO OBSERVED OUTCOME → NO EPISODIC MEMORY UPDATE**

The firewall checks declared and linked records. It cannot prove that an
external source is truthful or genuinely independent; that requires audit and
domain governance.

## 6. Privacy and redaction

- minimize collected fields before ingestion;
- separate direct identifiers from analytical records;
- document aggregation, pseudonymization, and redaction;
- preserve access roles and retention rules;
- never expose protected source data through reports, logs, fixtures, or
  episodic memory;
- require domain and legal review for sensitive human or infrastructure data.

## Repository materials

- [Admission checklist](ADMISSION_CHECKLIST.md)
- [Observed-case manifest template](templates/observed_case_manifest.template.json)
- [Outcome-firewall fixtures](fixtures/)
- [Outcome-firewall implementation](../../nexah/orientation/outcome_firewall.py)

Completing this bridge closes Phase V documentation. Admitting a real source is
the next evidence plateau and must receive its own versioned case protocol.
