# Living Concepts — Minimal Concept Overlay v0.1

**Status:** editorial baseline accepted · non-canonical
**Load policy:** manual evaluation only  
**Kernel integration:** not implemented

The Minimal Concept Overlay records the accepted editorial baseline for
whether reviewed Concept-family knowledge can
be represented in a small, machine-readable form without turning editorial
synthesis into canonical graph truth.

Acceptance covers the schema, seven reviewed handles, documentary
occurrences, review-only relations, curated paths, Reader and Explain answer
contracts, and the six-question baseline evaluation. It does not approve
permanent identities, Registry integration, graph truth, inference, general
Kernel loading, or Are.na mutation.

The overlay is deliberately not placed in the Registry and is not loaded by
the Orientation Kernel. It has no writer and no Are.na mutation path.

## What it contains

```text
reviewed handle
    ├── reader profile or authority reference
    ├── evidence occurrences
    ├── review-only relation proposals
    ├── human-curated paths
    └── Reader / Explain answer contracts
```

Version 0.1 is limited to seven handles:

- Transition Geometry;
- JANUS;
- Aperture;
- Inbetween;
- Boundary;
- Transition;
- Balance.

Aperture, Boundary, and Transition bind to existing controlled Operators. The
binding does not create broader Concept identities. The other handles are
local review keys only.

## Authority order

The overlay preserves source authority rather than flattening it:

1. existing controlled Operator records remain authoritative for Operator
   definitions;
2. accepted Architecture constrains identity and claim boundaries;
3. reviewed dossiers and family reviews provide editorial synthesis;
4. Works provide authored definitions, examples, and visual language;
5. Research and Validation provide only their explicitly scoped support;
6. historical sources provide lineage, not current authority.

## Relation and path boundary

Relations use `status: review_only`. Paths use `status: curated`. Neither is a
canonical graph edge.

An occurrence proves that a source contains a statement or visual
formulation. It does not validate the substantive claim. Every occurrence
therefore records its assertion origin and claim-support boundary.

## Reader and Explain contracts

Question bindings do not contain a general inference engine. They identify the
smallest reviewed evidence bundle needed to reproduce the six accepted
Concept-family answers.

- Reader Mode uses the short `reader_answer` and an optional curated route.
- Explain Mode adds provenance, identity separation, and uncertainty through
  `explain_disclosures`.

The contract is successful only if it reproduces the human baseline without
allocating identities, inventing relations, or hiding uncertainty.

## Files

- [Concept Overlay v0.1](concept_overlay_v0_1.yaml)
- [Evaluation Report](../review/transition_geometry/CONCEPT_OVERLAY_V0_1_EVALUATION.md)
- Structural validator: `tests/living_concepts/test_concept_overlay_v0_1.py`

## Explicit exclusions

Version 0.1 does not:

- allocate `NX-C-...` identities;
- amend the Canonical Registry or controlled Operator vocabulary;
- implement a production Concept Graph;
- add Kernel commands or runtime loading;
- infer relations from co-occurrence;
- extract text from Works automatically;
- write to Are.na;
- promote Balance into one Concept;
- promote `Region → Boundary → Transition → Closure` into an invariant.

## Current system state

```text
Overlay v0.1                 Editorial baseline accepted
Read-only Answer Adapter     Pilot implemented for six accepted questions
Production Concept Graph     Not implemented
General Kernel integration   Deferred
```

The distinctions are explicit:

```text
Concept Overlay              ≠ Concept Graph
Concept Answer Adapter       ≠ General Reasoning Engine
Accepted Editorial Baseline  ≠ Canonical Knowledge
```

## Read-only Concept Answer Adapter

The Phase X2 pilot resolves only `CFQ-01` through `CFQ-06` from the accepted
question contracts. It does not interpret arbitrary questions.

```bash
python -m nexah.living_concepts answer CFQ-01 --mode reader
python -m nexah.living_concepts answer CFQ-01 --mode explain
```

An accepted Overlay path may also be supplied explicitly:

```bash
python -m nexah.living_concepts answer CFQ-01 \
  --overlay EDITORIAL_OPERATING_SYSTEM/living_concepts/overlay/concept_overlay_v0_1.yaml \
  --mode explain
```

There are no write options. Unknown questions return `state: unsupported`.

Additional artifacts:

- [Accepted Answer Baseline](concept_overlay_v0_1_expected_answers.yaml)
- [Adapter Evaluation](../review/transition_geometry/CONCEPT_OVERLAY_ADAPTER_V0_1_EVALUATION.md)
