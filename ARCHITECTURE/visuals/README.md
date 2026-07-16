# NEXAH Architecture Visuals

These visuals are orientation artifacts. They help readers understand the
repository, but they do not replace specifications, validation records, or the
current **[System State](../SYSTEM_STATE.md)**.

## Evidence Classes

### `current/`

Visuals describing the reviewed repository state or its present architectural
organization.

- `orientation-laboratory.png` — current repository-wide architecture overview
- `what-is-nexah-2026-07-16.png` — immutable, dated status snapshot

Counts and maturity statements in dated snapshots must not be silently updated.
A later review should create a new dated file.

### `research-models/`

Conceptual lenses and bounded research hypotheses.

- `orientation-layer-concave-mirror.png` — comparison, reflection, and
  reorientation across bounded representations

Research-model visuals are not canonical ontologies, proofs of universality, or
evidence that every depicted relation has been implemented.

## Reading Rule

Use the labels in this order:

```text
CURRENT / IMPLEMENTED
→ supported by repository state and evidence

RESEARCH MODEL
→ investigated conceptual structure

EDITORIAL INTERPRETATION
→ human or philosophical reading

VISION
→ possible future direction, not current capability
```

Only the first two classes belong in this Architecture directory today.
Editorial and visionary Plates remain with the Library or Editorial Operating
System so that interpretation is not mistaken for implementation.
