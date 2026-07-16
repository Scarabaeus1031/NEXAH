# Living Concepts — Concept Model Proposal

**Status:** X0 proposal · non-canonical · does not amend Architecture v1.0

## Finding

The existing Registry already models its 17 Operators as
`object_family: concept`, but production validation intentionally accepts only
`type: operator`. A future broader Concept layer is structurally plausible,
but must not be enabled until human review approves an identity policy,
relationship vocabulary, and claim-provenance contract.

## Proposed objects

### Concept candidate

A named idea with a recognizable NEXAH-specific meaning. During X0 it has only
a local `concept:<slug>` review key.

Minimum future fields:

```yaml
candidate_key: concept:example
preferred_name: Example
review_state: candidate
editorial_maturity: developing
existing_operator:
  value: false
  operator_ref: null
summary: ...
nexah_specificity:
  value: moderate
  rationale: ...
```

### Concept Occurrence

An evidence link between a source and a Concept candidate. It records what the
source does with the term, not whether its substantive claim is true.

```yaml
source: RESEARCH/example.md
locator: section "Working Definition"
occurrence_role: defines
occurrence_verification: verified
assertion_origin: human_authored
claim_support:
  value: exploratory
  scope: RESEARCH/example.md
  rationale: ...
```

### Definition candidate

X0 shows that a single inline `definition` will not be sufficient. Research
usage can differ from an Operator's controlled editorial definition, and terms
can change through time. X1 should test separate, versioned Definition
candidates with source, scope, assertion origin, status, and supersession.

### Open Question

Open Questions should remain embedded evidence records during X1. First-class
identity is unnecessary until questions must be cited, related, closed, or
reopened across multiple Concepts.

### Concept relation proposal

Concept-to-Concept relations remain proposals and require source provenance:

```text
depends_on · contrasts_with · specializes
transforms_into · develops_from · related_to
```

The X0 sample suggests adding `part_of` for compositional structures only if
X1 demonstrates that `depends_on` cannot express the needed distinction.

## Separate occurrence vocabulary

Source-to-Concept roles are not Concept relations:

```text
mentions · discusses · defines · develops · visualizes
applies · questions · tests · contrasts · revises
```

`observed_in`, `tested_in`, and `defined_in` should not become Concept-to-
Concept edges. Their meaning belongs to an Occurrence or claim-provenance
record.

## Status axes

Three axes must remain independent:

| Axis | Proposed values | Meaning |
|---|---|---|
| Editorial review | candidate · reviewed · established · deprecated | Human editorial decision |
| Concept maturity | emerging · developing · coherent · historical · unclear | Review aid, not scientific validation |
| Claim support | not_assessed · speculative · exploratory · supported_within_scope · validated_within_scope · not_supported | Support for a scoped assertion |

Existing Operator `vocabulary_status` remains authoritative and is not mapped
automatically onto broader Concept status.

## Work-title collision

A Work and a Concept may share a name without sharing identity. The Living
Equation sample demonstrates the required distinction:

```text
Work candidate: THE LIVING EQUATION — An Atlas of Orientation
Concept candidate: Living Equation
```

The Work is documented. A separate Concept meaning is not yet sufficiently
defined. No Concept identity should be inferred from the title.

## Earliest occurrence

Use `earliest_verified_occurrence`, never `origin`, unless a dedicated
historical review establishes authorship and chronology. File modification
times are insufficient. Git history can narrow the reviewed repository record,
but cannot prove an idea's absolute origin in books, private notes, or earlier
visual work.

## Kernel compatibility

The current Kernel can list Work–Operator usage and curated Work relations. It
cannot represent Definition candidates, Occurrences, Concept timelines, Open
Questions, or non-Operator Concept relations.

The smallest future addition is a read-only proposal overlay with:

```text
Concept candidate nodes
Occurrence evidence edges
typed Concept relation proposals
Definition candidates
Open Questions
```

No Kernel modification is authorized by X0. Any later overlay must preserve
canonical/proposal separation and return provenance with every Concept answer.

## Architecture decision deferred

X0 does not decide:

- permanent Concept ID syntax;
- production Registry placement;
- whether Operator and broader Concept records share identity;
- final relation vocabulary;
- Definition or Open Question identity;
- automated candidate extraction in production.

These are X1/X2 architecture candidates requiring explicit human approval.
