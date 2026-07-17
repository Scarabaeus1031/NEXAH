# Orientation Language Specification — OLS-I

## Informative Companion

| Metadata field | Value |
| --- | --- |
| Document ID | `OLS-I` |
| Edition | 1 |
| Suite version | `1.0.0` |
| Document revision | `1.0.0` |
| Status | Version 1.0 informative publication candidate |
| Publication date | 17 July 2026 |
| Language | English |
| Normative scope | None |
| Semantic scope | None |
| Classification | Informative companion; historical material; implementation guidance |
| Controlling documents | `OLS-0`, `OLS-1`, `OLS-2`, `OLS-3`, `OLS-4`, `OLS-5`, `OLS-6` |
| Replaces | None |
| Release manifest identifier | Pending assignment at suite publication |
| Persistent citation identifier | Unassigned |
| Architecture baseline | Phase 2D Canonical Architecture, frozen by ADR-0001 |

## Status of this document

This document is informative in its entirety. It introduces no requirement, semantic authority, primitive, operator, profile, declaration, derivation, conformance rule, or extension. Normative keywords appearing in quotations, identifiers, examples, or descriptions of controlling clauses retain only the force assigned by those controlling clauses.

If this companion conflicts with any normative part of the suite, the normative part controls. OLS-0 Clause 6 governs the normative/informative distinction; OLS-0 Clause 22 governs the role of OLS-I.

---

## 1 Scope

*Stable clause ID: `OLSI-CLS-0001` — Trace ID: `TRACE-000203` — Informative*

OLS-I helps readers navigate, interpret, teach, and realize the normative Orientation Language Specification. It provides reading aids, explanatory mappings, examples, counterexamples, historical context, and implementation guidance without replacing any controlling definition or rule.

This document does not determine conformance. Conformance remains controlled by OLS-5.

**Controlling references:** OLS-0 Clauses 5, 6, and 22; OLS-5 Clauses 3 and 12.

## 2 Purpose and publication role

*Stable clause ID: `OLSI-CLS-0002` — Trace ID: `TRACE-000204` — Informative*

The companion has three practical roles:

1. navigation across the seven normative parts;
2. illustration of already specified semantics and boundaries;
3. translation from normative abstractions to human and implementation contexts.

It is intentionally outside the chain of semantic ownership. A reader can use it to find an authoritative clause, but cannot cite it instead of that clause when asserting semantics or conformance.

**Controlling references:** OLS-0 Clauses 12, 16, 21, and 22; OLS-6 Clause 10.

## 3 Specification suite map

*Stable clause ID: `OLSI-CLS-0003` — Trace ID: `TRACE-000205` — Informative*

| Part | Reader question | Controlling subject |
| --- | --- | --- |
| `OLS-0` | How is the suite read and cited? | Suite conventions, identifiers, references, registries, metadata |
| `OLS-1` | What is universally meant? | Universal Base Language, concepts, boundaries, canonical process |
| `OLS-2` | What is declared and how are operators invoked? | Ten declarations and ten primitive operator contracts |
| `OLS-3` | Which optional capabilities are active? | Seven semantic profiles, dependencies, composition, ownership |
| `OLS-4` | Which products, derivations, and transitions are legal? | Products, accepted and conditional derivations, outcome and learning sequence |
| `OLS-5` | How is a claim tested? | Conformance classes, tests, evidence, reports, certification boundaries |
| `OLS-6` | How may the suite evolve? | Extensions, versioning, governance, publication lifecycle |
| `OLS-I` | How can the suite be understood and approached? | Informative explanation and navigation only |

The dependency direction is `OLS-0` → `OLS-1` → `OLS-2` → `OLS-3` → `OLS-4` → `OLS-5` → `OLS-6`. OLS-I references the chain but does not extend it.

**Controlling references:** OLS-0 Clause 5 and Annex A; OLS-6 Clauses 4 and 12.

## 4 Reading guide

*Stable clause ID: `OLSI-CLS-0004` — Trace ID: `TRACE-000206` — Informative*

| Reader | Suggested path |
| --- | --- |
| First-time reader | OLS-I Clauses 3–5 → OLS-1 → OLS-2 |
| Human practitioner | OLS-1 → applicable OLS-2 declarations → OLS-I Clauses 13 and 15 |
| Implementer | OLS-0 → OLS-1 → OLS-2 → applicable OLS-3/OLS-4 material → OLS-I Clauses 16–18 → OLS-5 |
| Profile user | OLS-3 → OLS-2 owner contracts → OLS-4 transitions → OLS-5 |
| Assessor | OLS-5 → all normative parts named by the selected conformance class |
| Extension author | OLS-6 → OLS-0 through OLS-5 as referenced by the proposed extension |
| Historian or researcher | OLS-I Clauses 20–22 and Annexes A and C, then the cited sources |

The suggested paths do not change document dependencies or normative status.

**Controlling references:** OLS-0 Clauses 4 and 21; OLS-5 Clause 5; OLS-6 Clauses 5–13.

## 5 Orientation Language overview

*Stable clause ID: `OLSI-CLS-0005` — Trace ID: `TRACE-000207` — Informative*

The Orientation Language provides a bounded way to work from observation through representation and comparison toward orientation and explanation. Its universal layer preserves the observer, context, perspective, position, evidence, provenance, uncertainty, and difference relevant to the construction. Optional profiles add separately owned capabilities without changing universal meanings.

The language is representation-dependent, perspective-dependent, situated in context, and bounded by evidence and uncertainty. Representation remains distinct from reality. Orientation remains distinct from recommendation, authorization, execution, outcome, learning, control, and certainty.

This paragraph is a navigation summary, not an authoritative definition. The fourteen authoritative concept definitions are in OLS-1 Clause 7 and Annex A; universal non-implications are in OLS-1 Clause 10 and Annex B.

**Controlling references:** OLS-1 Clauses 4–12 and Annexes A–B; OLS-3 Clauses 4 and 12.

## 6 Terminology navigation

*Stable clause ID: `OLSI-CLS-0006` — Trace ID: `TRACE-000208` — Informative*

| Term family | Authoritative location |
| --- | --- |
| Fourteen universal concepts | OLS-1 Clause 7; OLS-1 Annex A |
| Ten declarations | OLS-2 Clause 5; OLS-2 Annex A |
| Ten primitive operators | OLS-2 Clauses 7–8; OLS-2 Annex B |
| Seven semantic profiles | OLS-3 Clause 10; OLS-3 Annex A |
| Profile primitive concepts | OLS-3 Clause 11; OLS-3 Annex C |
| Semantic products | OLS-4 Clause 4; OLS-4 Annex A |
| Accepted and conditional derivations | OLS-4 Clauses 5–6; OLS-4 Annex B |
| Conformance terms and statuses | OLS-5 Clauses 3 and 9; OLS-5 Annex C |
| Governance and version terms | OLS-6 Clauses 3 and 14–19 |
| Historical and cultural terms | OLS-I Clause 20 and Annex A, informative only |

An alias, historical label, visual motif, or implementation name does not become canonical terminology by appearing here. OLS-0 Clause 8 controls vocabulary and aliases.

**Controlling references:** OLS-0 Clause 8 and Annex D; the owning clauses listed in the table.

## 7 Concepts and declarations explained

*Stable clause ID: `OLSI-CLS-0007` — Trace ID: `TRACE-000209` — Informative*

Concepts and declarations answer different questions. A concept supplies a semantic distinction; a declaration supplies a scoped value or status needed to apply that distinction. For example, context and perspective are universal concepts, while `DECL-CONTEXT` and `DECL-PERSPECTIVE` identify the applicable values in an expression. A declared value is not a second definition of the concept.

The ten declarations are time, identity, scale, context, perspective, position, representation type, evidence class, uncertainty status, and authority scope. Omission is not a default: OLS-2 determines when each declaration applies and how omission, incompatibility, preservation, and reference are handled.

**Controlling references:** OLS-1 Clause 12; OLS-2 Clauses 4–5 and Annex A.

## 8 Operators and the canonical process explained

*Stable clause ID: `OLSI-CLS-0008` — Trace ID: `TRACE-000210` — Informative*

The universal process is:

`OBSERVE` → `REPRESENT` → `COMPARE` → `ORIENT` → `EXPLAIN`

This order describes the complete universal process. OLS-1 controls permitted omissions and boundaries; OLS-2 controls each invocation and contract. The profile operators `SELECT`, `TRANSFORM`, `VALIDATE`, `RECORD`, and `APPROVE` are not hidden universal stages. They become available only through their owning profiles and applicable dependencies.

Operator order does not manufacture truth, evidence, authority, outcome, or learning. Each output retains the status and limitations established by its controlling contract.

**Controlling references:** OLS-1 Clauses 8–10; OLS-2 Clauses 6–12 and Annexes B–C.

## 9 Profiles and composition explained

*Stable clause ID: `OLSI-CLS-0009` — Trace ID: `TRACE-000211` — Informative*

Version 1.0 contains Representation, Navigation, Transformation, Evidence/Validation, Memory/Learning, Editorial Governance, and Education profiles. A profile inherits OLS-1 and adds only its registered responsibility. Activation can introduce dependencies: Navigation depends on Representation; Education depends on Navigation; other dependencies arise under the conditions stated in OLS-3.

Composition means that active profiles coexist while retaining their identities, owners, declarations, dependencies, and prohibited modifications. It is not permission to blend definitions or transfer ownership.

**Controlling references:** OLS-3 Clauses 4–12 and Annexes A–C.

## 10 Derivations, transitions, outcomes, and learning explained

*Stable clause ID: `OLSI-CLS-0010` — Trace ID: `TRACE-000212` — Informative*

OLS-4 distinguishes primitive operator outputs from derived products and status transitions. Its registries contain eleven products, eighteen accepted derivations, eighteen conditional derivations, and prohibited derivations. Conditional derivations depend on every registered condition; examples do not remove those conditions.

The experiential sequence separates transformation, post-transformation observation, candidate outcome, validation, admission, recording, and learning. A transformation result is not an admitted outcome. Validation alone does not admit an outcome. Recording alone does not establish learning.

**Controlling references:** OLS-4 Clauses 3–15 and Annexes A–C.

## 11 Conformance explained

*Stable clause ID: `OLSI-CLS-0011` — Trace ID: `TRACE-000213` — Informative*

Conformance is a claim about compliance with identified normative requirements, not a claim that a construction is true, useful, scientifically valid, or well implemented. OLS-5 defines six conformance classes, the test model, evidence, statuses, aggregation, reporting, and certification boundaries.

An example in OLS-I may illustrate a conforming shape, but it cannot establish conformance. A formal claim uses the applicable OLS-5 class, release manifest, requirement-to-test mappings, evidence, and report.

**Controlling references:** OLS-5 Clauses 3–13 and Annexes A–C.

## 12 Evolution and governance explained

*Stable clause ID: `OLSI-CLS-0012` — Trace ID: `TRACE-000214` — Informative*

Version 1.0 can receive compatible registered extensions and editorial maintenance without silent semantic change. OLS-6 separates extensions, releases, deprecations, errata, and architecture revisions. Stable identifiers remain governed identities; reuse or reassignment is not a shortcut for change.

An issue that would add or remove a frozen primitive, change responsibility or ownership, alter profile semantics or composition, or change an accepted derivation crosses the architecture-revision boundary.

**Controlling references:** OLS-6 Clauses 4–24 and Annexes A–D; OLS-0 Clauses 10 and 23.

## 13 Worked examples

*Stable clause ID: `OLSI-CLS-0013` — Trace ID: `TRACE-000215` — Informative*

All examples are abbreviated. They illustrate already specified distinctions and do not replace applicable declarations, contracts, dependencies, or tests.

### 13.1 Bounded personal orientation

**Question:** What is currently observable about a professional situation, and which uncertainties prevent a bounded orientation?

**Illustrative sequence:** record sourced observations; represent the relevant roles, constraints, and events; compare the present state with a declared earlier state and stated alternatives; orient within the declared perspective and context; explain findings and limitations.

**Stopping boundary:** the result remains an orientation. It is not advice, recommendation, authority, action, or outcome.

**Controlling references:** OLS-1 Clauses 7–10; OLS-2 universal contracts; OLS-3 Navigation only if alternatives are selected.

### 13.2 Incompatible public perspectives

Two perspectives can be represented and compared without being merged. Agreements, differences, incompatible premises, evidence status, and unresolved uncertainty remain visible. A derived boundary can function as a separation or interface under its declared criteria; this does not prove a causal mechanism or create consensus.

**Controlling references:** OLS-1 concepts perspective, representation, relation, difference, evidence, and uncertainty; OLS-4 `DERIVATION-C14`; OLS-1 Annex B.

### 13.3 Cross-disciplinary research comparison

Claims from two disciplines are represented with distinct provenance, scale, representation type, evidence class, and uncertainty status. COMPARE identifies agreements and mismatches under a declared basis. Similarity can support a comparison finding but not a mechanism, causal claim, or universal law.

**Controlling references:** OLS-2 `OP-REPRESENT` and `OP-COMPARE`; OLS-4 `PRODUCT-COMPARISON-FINDING`; OLS-4 Annex C.

### 13.4 Dependency network

A graph realization represents identified components and relations at a declared scale. Navigation can locate a position, apply constraints, and select a route; derivations can describe a block or route when their registered inputs are present. Missing edges, stale observations, or incompatible scales remain limitations rather than silently absent dependencies.

**Controlling references:** OLS-3 Representation and Navigation; OLS-4 `DERIVATION-A14`, `DERIVATION-A15`, and `DERIVATION-C16`; OLS-2 declaration clauses.

### 13.5 AI before action

An AI implementation can produce observations, representations, comparisons, orientation findings, and explanations while preserving evidence, provenance, uncertainty, and authority scope. A selection is not a recommendation. Orientation is not authorization. Implementation capability is not authority. Execution, observed outcome, validation, admission, recording, and learning remain separately governed.

**Controlling references:** OLS-1 Annex B; OLS-3 Navigation, Evidence/Validation, Memory/Learning, and Editorial Governance; OLS-4 Clauses 8–10.

## 14 Counterexamples and common misunderstandings

*Stable clause ID: `OLSI-CLS-0014` — Trace ID: `TRACE-000216` — Informative*

| Misreading | Why it fails | Controlling source |
| --- | --- | --- |
| A polished map is reality. | Representation/reality boundary is collapsed. | OLS-1 Annex B |
| Two visually similar structures share a cause. | Comparison does not imply causality. | OLS-1 Annex B; OLS-4 Annex C |
| A model output is an observation. | Product and provenance status are changed without OBSERVE. | OLS-2 `OP-OBSERVE`; OLS-4 Clause 4 |
| A possible path is recommended. | Path, selection, recommendation, and authority remain distinct. | OLS-3 Navigation; OLS-4 `DERIVATION-C16` |
| A transformation result proves improvement. | TRANSFORM does not imply improvement or validation. | OLS-2 `OP-TRANSFORM`; OLS-4 Clause 4.6 |
| A validation result is an admitted outcome. | Validation and admission are separate statuses. | OLS-4 Clauses 7–8 |
| A stored record is learned knowledge. | Persistence alone does not establish learning. | OLS-3 Memory/Learning; OLS-4 Clause 10 |
| Software capability supplies authority. | Authority belongs to Editorial Governance and requires authority scope. | OLS-3 Clause 11.4; OLS-2 `DECL-AUTHORITY-SCOPE` |
| A teaching path is a universal cognitive law. | Education preserves this boundary. | OLS-3 Education |
| Passing conformance proves truth or usefulness. | Certification is semantic compliance only. | OLS-5 Clause 12 |

## 15 Human-use guidance

*Stable clause ID: `OLSI-CLS-0015` — Trace ID: `TRACE-000217` — Informative*

A human application can begin with six prompts:

- What is the question and focus?
- What was observed, by whom, when, and from which source?
- Which context, perspective, position, scale, and representation apply?
- Which differences and relations are visible under that basis?
- Which evidence, uncertainty, disagreement, and limits remain?
- What can be explained without crossing into recommendation, authority, or action?

These prompts are a reading aid, not alternate syntax. Applicable declarations and operator contracts remain controlled by OLS-2.

**Controlling references:** OLS-1 Clauses 6–13; OLS-2 Clauses 4–12.

## 16 Implementation realization guidance

*Stable clause ID: `OLSI-CLS-0016` — Trace ID: `TRACE-000218` — Informative*

An implementation can use forms, documents, diagrams, graphs, databases, software services, AI systems, or manual procedures. Technology does not determine semantics. A realization is easier to audit when it exposes:

- the suite and profile versions it applies;
- the concepts, declarations, operators, products, and derivations it supports;
- source and provenance links;
- preserved evidence and uncertainty statuses;
- unsupported capabilities and incomplete inputs;
- ownership and authority boundaries;
- the distinction between computed output and observed fact.

These are implementation considerations derived from existing normative responsibilities. OLS-5, not this clause, controls conformance evidence and reports.

**Controlling references:** OLS-1 Clause 4; OLS-2 Clause 10; OLS-3 Clause 9; OLS-5 Clauses 4, 10, 11, and 13.

## 17 Reference representation mappings

*Stable clause ID: `OLSI-CLS-0017` — Trace ID: `TRACE-000219` — Informative*

| Realization form | Possible OLS use | Boundary to preserve |
| --- | --- | --- |
| Graph | Represent entities/relations; compare structures; support Navigation | A graph is not reality, mechanism, or proof |
| Field or state space | Represent states, positions, differences, or transitions | Representation type and scale remain declared |
| Timeline or trajectory | Order observations/states under identity and time | A represented sequence is not thereby causal |
| Map or atlas | Arrange positions and relations; collect representations | Map is a derived distinction, not territory or complete model |
| Table or report | Preserve declarations, findings, evidence, and uncertainty | Format does not change semantic status |
| Registry or store | Persist identities, statuses, and records | Persistence is not validation, admission, or learning |
| AI-generated explanation | Render an explanation from declared inputs | Explanation is not truth, authority, or approval |

No row registers a new representation type or implementation requirement.

**Controlling references:** OLS-1 representation and boundary clauses; OLS-2 `DECL-REPRESENTATION-TYPE`; OLS-3 Representation; OLS-4 map/path/flow derivations.

## 18 Report and schema examples

*Stable clause ID: `OLSI-CLS-0018` — Trace ID: `TRACE-000220` — Informative*

The following YAML is an illustrative carrier. It is not a normative schema and its field names are not registered identifiers.

```yaml
suite_version: 1.0.0
question: "What can be oriented from the declared material?"
declarations:
  context: "declared case boundary"
  perspective: "declared analytical view"
  representation_type: "graph"
  evidence_class: "declared by the application"
  uncertainty_status: "partially unresolved"
operator_sequence:
  - OP-OBSERVE
  - OP-REPRESENT
  - OP-COMPARE
  - OP-ORIENT
  - OP-EXPLAIN
findings:
  supported: []
  disputed: []
  unsupported: []
limitations: []
authority_scope: "orientation and explanation only"
outcome_status: "not claimed"
learning_status: "not claimed"
```

A real expression supplies all declarations applicable to its claims, uses the authoritative contracts, and does not infer a default from this example.

**Controlling references:** OLS-2 Clauses 4–12; OLS-3 Clause 9; OLS-4 product/status clauses; OLS-5 Clause 11 for conformance reports.

## 19 Learning pathways

*Stable clause ID: `OLSI-CLS-0019` — Trace ID: `TRACE-000221` — Informative*

| Path | Sequence | Intended outcome |
| --- | --- | --- |
| Foundation | OLS-0 → OLS-1 → OLS-2 | Navigate the suite and form base expressions |
| Application | Foundation → OLS-3 → OLS-4 → worked examples | Apply profiles and interpret products/transitions |
| Assessment | Foundation → OLS-3/4 → OLS-5 | Evaluate a declared conformance claim |
| Stewardship | Complete normative suite → OLS-6 | Maintain or extend the publication under governance |
| Historical study | OLS-I Clauses 20–22 → cited research record | Understand provenance without importing historical semantics |

These pathways are editorial sequences. They are not semantic derivations or universal cognitive laws.

**Controlling references:** OLS-0 Clauses 4 and 6; OLS-3 Education; OLS-6 governance clauses.

## 20 Historical and cultural component

*Stable clause ID: `OLSI-CLS-0020` — Trace ID: `TRACE-000222` — Informative*

NEXAH’s source corpus includes books, atlases, visual research, metaphors, cultural interpretations, and recurring terms such as wonder, attention, awareness, becoming, inbetween, and meaning-oriented or embodied orientation. These materials preserve the context from which the formal architecture was reconstructed.

They do not become universal concepts, declarations, operators, profiles, derivations, evidence, mechanisms, or conformance criteria by inclusion in this companion. Their role is historical and interpretive. Annex A provides navigation labels, not canonical definitions.

**Controlling references:** OLS-0 Clauses 6 and 8; OLS-6 Clauses 10 and 19; Phase 2D informative-component classification as cited in Annex C.

## 21 Research and architectural rationale

*Stable clause ID: `OLSI-CLS-0021` — Trace ID: `TRACE-000223` — Informative*

The published architecture resulted from corpus extraction, review, distillation, falsification, semantic reconstruction, architectural review, and consolidation. ADR-0001 records the frozen decisions: minimal universal kernel; difference as primitive; time, identity, and scale as declarations; profile extension; unique ownership; historical preservation; implementation/semantics separation; validation before admitted experience; unresolved space and balance; and architecture freeze.

The rationale explains why the suite has its structure. It does not replace the normative clauses produced from that baseline.

**Controlling references:** OLS-0 Clauses 19–20; OLS-6 Clause 18; ADR-0001.

## 22 ADR and review index

*Stable clause ID: `OLSI-CLS-0022` — Trace ID: `TRACE-000224` — Informative*

| Record | Role | Authority boundary |
| --- | --- | --- |
| ADR-0001 | Records the accepted architectural baseline and rationale | Not part of the normative specification |
| Phase 2D Canonical Architecture | Frozen semantic source used to write the suite | Superseded for publication interpretation by owning normative clauses, while retained for traceability |
| Phase 3 Specification Charter | Governs transformation from architecture to specification | Does not redefine semantics |
| Phase 3A framework | Allocates suite structure and deliverables | Does not add semantic authority |
| OLS-0 through OLS-6 editorial reviews | Record publication-readiness checks | Do not replace reviewed documents |

**Controlling references:** OLS-0 Clauses 18–20; OLS-6 Clauses 20–24.

## 23 Editorial and citation conventions

*Stable clause ID: `OLSI-CLS-0023` — Trace ID: `TRACE-000225` — Informative*

When citing semantics, use the owning normative document and stable element identifier. When citing an OLS-I explanation, identify OLS-I, edition, revision, and clause ID, and make its informative status clear. Clause numbers are navigation aids; stable IDs are the durable references.

Examples can abbreviate material for readability. An abbreviation does not waive declarations, dependencies, boundaries, or tests in the controlling documents.

**Controlling references:** OLS-0 Clauses 9–11, 16, 18, and 25.

## 24 Publication package navigation

*Stable clause ID: `OLSI-CLS-0024` — Trace ID: `TRACE-000226` — Informative*

The Version 1.0 publication package consists of OLS-0 through OLS-6 and OLS-I. Release identity, checksums, registry versions, compatibility, publication state, and canonical locations belong in the OLS-6 release manifest. OLS-I is complete only as a companion to the exact normative suite version named in that manifest.

The traceability export in Annex D supports review but does not supersede source metadata or the normative registries.

**Controlling references:** OLS-0 Annex A; OLS-6 Clauses 21–23.

---

# Annex A — Historical and Cultural Glossary

*Annex ID: `OLSI-ANNEX-A` — Trace ID: `TRACE-000227` — Informative*

The labels below navigate preserved source material. They are neither canonical definitions nor semantic registrations.

| Historical label or family | Informative corpus role | Normative boundary |
| --- | --- | --- |
| wonder | Cultural/philosophical entry and orientation motif | Not a universal concept or operator |
| attention | Human/cultural orientation theme | Not a declaration or perceptual contract |
| awareness | Human/cultural orientation theme | Not a validated cognitive mechanism |
| becoming | Change and transition motif | Not a synonym for the registered transition or transformation semantics |
| inbetween | Transitional and cultural motif | Not a registered universal region or profile primitive |
| meaning-oriented orientation | Interpretive/cultural framing | Meaning remains a conditional derivation under OLS-4 |
| embodied orientation | Human/cultural framing | Does not supply empirical or implementation semantics |
| books, atlases, and visual systems | Source and teaching forms | Do not define semantic authority |
| space | Preserved unresolved historical concept | No universal derivation in Version 1.0 |
| balance | Preserved unresolved historical concept | No universal derivation in Version 1.0 |

**Controlling references:** OLS-0 Clauses 6 and 8; OLS-4 Annex B for meaning; OLS-6 Clause 19; ADR-0001 Decisions 6 and 9.

# Annex B — Implementation Mapping Catalogue

*Annex ID: `OLSI-ANNEX-B` — Trace ID: `TRACE-000228` — Informative*

| Implementation component | Referenced normative owner | Informative mapping |
| --- | --- | --- |
| Input adapter or observation form | OLS-2 `OP-OBSERVE` | Captures declared source material and status |
| Graph/field/model builder | OLS-2 `OP-REPRESENT`; OLS-3 Representation | Constructs a declared representation type |
| Comparison routine | OLS-2 `OP-COMPARE` | Produces comparison findings under a declared basis |
| Orientation report generator | OLS-2 `OP-ORIENT` and `OP-EXPLAIN` | Renders bounded findings and explanation |
| Route or alternative selector | OLS-3 Navigation; OLS-2 `OP-SELECT` | Produces selection result without authority implication |
| Transformation service | OLS-3 Transformation; OLS-2 `OP-TRANSFORM` | Produces a distinct resulting form or state |
| Validator | OLS-3 Evidence/Validation; OLS-2 `OP-VALIDATE` | Tests a subject against declared criteria and evidence |
| Record store | OLS-3 Memory/Learning; OLS-2 `OP-RECORD` | Persists material while preserving status |
| Approval workflow | OLS-3 Editorial Governance; OLS-2 `OP-APPROVE` | Applies governed approval within declared authority scope |
| Test harness | OLS-5 | Executes normative tests and produces conformance evidence |
| Registry/release tooling | OLS-6 | Maintains registered identities and manifests under governance |

No component is required, and no mapping grants conformance by itself.

# Annex C — Research Evidence Index

*Annex ID: `OLSI-ANNEX-C` — Trace ID: `TRACE-000229` — Informative*

| Evidence layer | Principal retained artifacts | Use in Version 1.0 |
| --- | --- | --- |
| Architecture baseline | Phase 2D Canonical Architecture; ADR-0001 | Rationale and bidirectional traceability |
| Corpus archaeology | Phase 1 extraction inventories | Historical source evidence |
| Editorial landscape | Phase 1A review | Description of corpus state before compression |
| Distillation | Phase 2 candidate kernel and relocation records | Evidence for retention and relocation decisions |
| Falsification | Phase 2A validation | Evidence of primitive, sufficiency, circularity, and reconstruction tests |
| Semantic reconstruction | Phase 2B architecture | Reconstructed concepts, operators, declarations, profiles, and derivations |
| Architectural review | Phase 2C review | Recorded boundary, minimality, profile, and readiness findings |
| Consolidation | Phase 2D canonical artifacts | Frozen semantic input to Phase 3 |
| Specification framework | Phase 3 Charter and Phase 3A | Publication allocation and traceability model |
| Publication reviews | Phase 3B through Phase 3I reviews | Editorial and architecture-fidelity checks |

Research evidence explains provenance; authoritative interpretation remains with OLS-0 through OLS-6.

# Annex D — Complete Bidirectional Traceability Export

*Annex ID: `OLSI-ANNEX-D` — Trace ID: `TRACE-000230` — Informative*

This export indexes every stable clause and annex identity carrying a trace identifier in OLS-0 through OLS-6. Each row resolves specification element → Trace ID. Because Trace IDs are unique in the listed suite, lookup by Trace ID provides the reverse direction. Rows without a trace identifier in the source publication are intentionally absent; OLS-I does not manufacture identifiers for another document.

| Specification element | Trace ID | Heading | Status |
| --- | --- | --- | --- |
| `OLS0-CLS-0001` | `TRACE-000001` | 1 Scope | Normative |
| `OLS0-CLS-0005` | `TRACE-000002` | 5 Structure of the Orientation Language Specification suite | Normative |
| `OLS0-CLS-0006` | `TRACE-000003` | 6 Normative and informative material | Normative |
| `OLS0-CLS-0007` | `TRACE-000004` | 7 Normative keywords | Normative |
| `OLS0-CLS-0008` | `TRACE-000005` | 8 Terminology policy | Normative |
| `OLS0-CLS-0009` | `TRACE-000006` | 9 Clause numbering policy | Normative |
| `OLS0-CLS-0010` | `TRACE-000007` | 10 Stable identifier policy | Normative |
| `OLS0-CLS-0011` | `TRACE-000008` | 11 Cross-reference policy | Normative |
| `OLS0-CLS-0012` | `TRACE-000009` | 12 Semantic ownership policy | Normative |
| `OLS0-CLS-0013` | `TRACE-000010` | 13 Registry policy | Normative |
| `OLS0-CLS-0014` | `TRACE-000011` | 14 Release manifest policy | Normative |
| `OLS0-CLS-0015` | `TRACE-000012` | 15 Version compatibility | Normative |
| `OLS0-CLS-0016` | `TRACE-000013` | 16 Citation rules | Normative |
| `OLS0-CLS-0017` | `TRACE-000014` | 17 Conformance reference policy | Normative |
| `OLS0-CLS-0018` | `TRACE-000015` | 18 Traceability overview | Normative |
| `OLS0-CLS-0019` | `TRACE-000016` | 19 Relationship to ADR-0001 | Normative |
| `OLS0-CLS-0020` | `TRACE-000017` | 20 Relationship to the Phase 2D Architecture | Normative |
| `OLS0-CLS-0021` | `TRACE-000018` | 21 Relationship to OLS-1 through OLS-6 | Normative |
| `OLS0-CLS-0022` | `TRACE-000019` | 22 Relationship to OLS-I | Normative |
| `OLS0-CLS-0023` | `TRACE-000020` | 23 Future architecture revisions | Normative |
| `OLS0-CLS-0024` | `TRACE-000021` | 24 Editorial maintenance rules | Normative |
| `OLS0-CLS-0025` | `TRACE-000022` | 25 Document metadata | Normative |
| `OLS0-ANN-A` | `TRACE-000023` | Annex A — Specification document registry | Normative |
| `OLS1-CLS-0001` | `TRACE-000024` | 1 Scope | Normative |
| `OLS1-CLS-0002` | `TRACE-000025` | 2 Normative references | Normative |
| `OLS1-CLS-0003` | `TRACE-000026` | 3 Terms and definitions | Normative |
| `OLS1-CLS-0004` | `TRACE-000027` | 4 Universal Base Language status | Normative |
| `OLS1-CLS-0005` | `TRACE-000028` | 5 Architectural position | Normative |
| `OLS1-CLS-0006` | `TRACE-000029` | 6 Universal semantic model | Normative |
| `OLS1-CLS-0007` | `TRACE-000030` | 7 Universal concept inventory | Normative |
| `OLS1-CLS-0008` | `TRACE-000031` | 7.1 observation | Normative |
| `OLS1-CLS-0009` | `TRACE-000032` | 7.2 observer | Normative |
| `OLS1-CLS-0010` | `TRACE-000033` | 7.3 context | Normative |
| `OLS1-CLS-0011` | `TRACE-000034` | 7.4 perspective | Normative |
| `OLS1-CLS-0012` | `TRACE-000035` | 7.5 representation | Normative |
| `OLS1-CLS-0013` | `TRACE-000036` | 7.6 position | Normative |
| `OLS1-CLS-0014` | `TRACE-000037` | 7.7 relation | Normative |
| `OLS1-CLS-0015` | `TRACE-000038` | 7.8 state | Normative |
| `OLS1-CLS-0016` | `TRACE-000039` | 7.9 transition | Normative |
| `OLS1-CLS-0017` | `TRACE-000040` | 7.10 evidence | Normative |
| `OLS1-CLS-0018` | `TRACE-000041` | 7.11 provenance | Normative |
| `OLS1-CLS-0019` | `TRACE-000042` | 7.12 uncertainty | Normative |
| `OLS1-CLS-0020` | `TRACE-000043` | 7.13 orientation | Normative |
| `OLS1-CLS-0021` | `TRACE-000044` | 7.14 difference | Normative |
| `OLS1-CLS-0022` | `TRACE-000045` | 8 Universal primitive operators | Normative |
| `OLS1-CLS-0023` | `TRACE-000046` | 8.1 OBSERVE | Normative |
| `OLS1-CLS-0024` | `TRACE-000047` | 8.2 REPRESENT | Normative |
| `OLS1-CLS-0025` | `TRACE-000048` | 8.3 COMPARE | Normative |
| `OLS1-CLS-0026` | `TRACE-000049` | 8.4 ORIENT | Normative |
| `OLS1-CLS-0027` | `TRACE-000050` | 8.5 EXPLAIN | Normative |
| `OLS1-CLS-0028` | `TRACE-000051` | 9 Canonical universal process | Normative |
| `OLS1-CLS-0029` | `TRACE-000052` | 10 Universal boundary conditions | Normative |
| `OLS1-CLS-0030` | `TRACE-000053` | 11 Universal inheritance | Normative |
| `OLS1-CLS-0031` | `TRACE-000054` | 12 Concept–declaration distinction | Normative |
| `OLS1-CLS-0032` | `TRACE-000055` | 13 Base Language expression model | Normative |
| `OLS1-CLS-0033` | `TRACE-000056` | 14 Universal error conditions | Normative |
| `OLS1-CLS-0034` | `TRACE-000057` | 15 Normative summary | Normative |
| `OLS1-ANN-A` | `TRACE-000058` | Annex A — Universal Concept Registry | Normative |
| `OLS1-ANN-B` | `TRACE-000059` | Annex B — Universal Boundary Matrix | Normative |
| `OLS2-CLS-0001` | `TRACE-000060` | 1 Scope | Normative |
| `OLS2-CLS-0002` | `TRACE-000061` | 2 Normative references | Normative |
| `OLS2-CLS-0003` | `TRACE-000062` | 3 Terms and definitions | Normative |
| `OLS2-CLS-0004` | `TRACE-000063` | 4 Declaration model | Normative |
| `OLS2-CLS-0005` | `TRACE-000064` | 5 Frozen declarations | Normative |
| `OLS2-CLS-0006` | `TRACE-000065` | 5.1 time | Normative |
| `OLS2-CLS-0007` | `TRACE-000066` | 5.2 identity | Normative |
| `OLS2-CLS-0008` | `TRACE-000067` | 5.3 scale | Normative |
| `OLS2-CLS-0009` | `TRACE-000068` | 5.4 context | Normative |
| `OLS2-CLS-0010` | `TRACE-000069` | 5.5 perspective | Normative |
| `OLS2-CLS-0011` | `TRACE-000070` | 5.6 position | Normative |
| `OLS2-CLS-0012` | `TRACE-000071` | 5.7 representation type | Normative |
| `OLS2-CLS-0013` | `TRACE-000072` | 5.8 evidence class | Normative |
| `OLS2-CLS-0014` | `TRACE-000073` | 5.9 uncertainty status | Normative |
| `OLS2-CLS-0015` | `TRACE-000074` | 5.10 authority scope | Normative |
| `OLS2-CLS-0016` | `TRACE-000075` | 6 Primitive Operator Contract Model | Normative |
| `OLS2-CLS-0017` | `TRACE-000076` | 7 Universal Primitive Operator Contracts | Normative |
| `OLS2-CLS-0018` | `TRACE-000077` | 7.1 OBSERVE | Normative |
| `OLS2-CLS-0019` | `TRACE-000078` | 7.2 REPRESENT | Normative |
| `OLS2-CLS-0020` | `TRACE-000079` | 7.3 COMPARE | Normative |
| `OLS2-CLS-0021` | `TRACE-000080` | 7.4 ORIENT | Normative |
| `OLS2-CLS-0022` | `TRACE-000081` | 7.5 EXPLAIN | Normative |
| `OLS2-CLS-0023` | `TRACE-000082` | 8 Profile Primitive Operator Contracts | Normative |
| `OLS2-CLS-0024` | `TRACE-000083` | 8.1 SELECT | Normative |
| `OLS2-CLS-0025` | `TRACE-000084` | 8.2 TRANSFORM | Normative |
| `OLS2-CLS-0026` | `TRACE-000085` | 8.3 VALIDATE | Normative |
| `OLS2-CLS-0027` | `TRACE-000086` | 8.4 RECORD | Normative |
| `OLS2-CLS-0028` | `TRACE-000087` | 8.5 APPROVE | Normative |
| `OLS2-CLS-0029` | `TRACE-000088` | 9 Primitive operator ownership | Normative |
| `OLS2-CLS-0030` | `TRACE-000089` | 10 Operator invocation | Normative |
| `OLS2-CLS-0031` | `TRACE-000090` | 11 Operator composition and sequencing | Normative |
| `OLS2-CLS-0032` | `TRACE-000091` | 12 Failure model | Normative |
| `OLS2-CLS-0033` | `TRACE-000092` | 13 Normative summary | Normative |
| `OLS2-ANN-A` | `TRACE-000093` | Annex A — Declaration Registry | Normative |
| `OLS2-ANN-B` | `TRACE-000094` | Annex B — Primitive Operator Ownership Registry | Normative |
| `OLS2-ANN-C` | `TRACE-000095` | Annex C — Operator Contract Template | Normative |
| `OLS3-CLS-0001` | `TRACE-000096` | 1 Scope | Normative |
| `OLS3-CLS-0002` | `TRACE-000097` | 2 Normative references | Normative |
| `OLS3-CLS-0003` | `TRACE-000098` | 3 Terms and definitions | Normative |
| `OLS3-CLS-0004` | `TRACE-000099` | 4 Common profile model | Normative |
| `OLS3-CLS-0005` | `TRACE-000100` | 5 Profile activation | Normative |
| `OLS3-CLS-0006` | `TRACE-000101` | 6 Dependency resolution | Normative |
| `OLS3-CLS-0007` | `TRACE-000102` | 7 Legal composition | Normative |
| `OLS3-CLS-0008` | `TRACE-000103` | 8 Conflict detection | Normative |
| `OLS3-CLS-0009` | `TRACE-000104` | 9 Active-profile reporting | Normative |
| `OLS3-CLS-0010` | `TRACE-000105` | 10 Version 1.0 semantic profiles | Normative |
| `OLS3-CLS-0011` | `TRACE-000106` | 10.1 Representation | Normative |
| `OLS3-CLS-0012` | `TRACE-000107` | 10.2 Navigation | Normative |
| `OLS3-CLS-0013` | `TRACE-000108` | 10.3 Transformation | Normative |
| `OLS3-CLS-0014` | `TRACE-000109` | 10.4 Evidence/Validation | Normative |
| `OLS3-CLS-0015` | `TRACE-000110` | 10.5 Memory/Learning | Normative |
| `OLS3-CLS-0016` | `TRACE-000111` | 10.6 Editorial Governance | Normative |
| `OLS3-CLS-0017` | `TRACE-000112` | 10.7 Education | Normative |
| `OLS3-CLS-0018` | `TRACE-000113` | 11 Primitive concept ownership | Normative |
| `OLS3-CLS-0019` | `TRACE-000114` | 11.1 constraint | Normative |
| `OLS3-CLS-0020` | `TRACE-000115` | 11.2 outcome | Normative |
| `OLS3-CLS-0021` | `TRACE-000116` | 11.3 memory | Normative |
| `OLS3-CLS-0022` | `TRACE-000117` | 11.4 authority | Normative |
| `OLS3-CLS-0023` | `TRACE-000118` | 12 Profile boundaries | Normative |
| `OLS3-CLS-0024` | `TRACE-000119` | 13 Normative summary | Normative |
| `OLS3-ANN-A` | `TRACE-000120` | Annex A — Profile Registry | Normative |
| `OLS3-ANN-B` | `TRACE-000121` | Annex B — Dependency and Activation Matrix | Normative |
| `OLS3-ANN-C` | `TRACE-000122` | Annex C — Primitive Concept Ownership Registry | Normative |
| `OLS4-CLS-0001` | `TRACE-000123` | 1 Scope | Normative |
| `OLS4-CLS-0002` | `TRACE-000124` | 2 Normative references | Normative |
| `OLS4-CLS-0003` | `TRACE-000125` | 3 Terms and derivation model | Normative |
| `OLS4-CLS-0004` | `TRACE-000126` | 4 Semantic product model | Normative |
| `OLS4-CLS-0005` | `TRACE-000127` | 4.1 Observation | Normative |
| `OLS4-CLS-0006` | `TRACE-000128` | 4.2 Representation | Normative |
| `OLS4-CLS-0007` | `TRACE-000129` | 4.3 Comparison finding | Normative |
| `OLS4-CLS-0008` | `TRACE-000130` | 4.4 Orientation finding | Normative |
| `OLS4-CLS-0009` | `TRACE-000131` | 4.5 Selection result | Normative |
| `OLS4-CLS-0010` | `TRACE-000132` | 4.6 Transformation result | Normative |
| `OLS4-CLS-0011` | `TRACE-000133` | 4.7 Validation result | Normative |
| `OLS4-CLS-0012` | `TRACE-000134` | 4.8 Candidate outcome | Normative |
| `OLS4-CLS-0013` | `TRACE-000135` | 4.9 Admitted outcome | Normative |
| `OLS4-CLS-0014` | `TRACE-000136` | 4.10 Recorded experience | Normative |
| `OLS4-CLS-0015` | `TRACE-000137` | 4.11 Learned knowledge | Normative |
| `OLS4-CLS-0016` | `TRACE-000138` | 5 Accepted derivations | Normative |
| `OLS4-CLS-0017` | `TRACE-000139` | 6 Conditional derivations | Normative |
| `OLS4-CLS-0018` | `TRACE-000140` | 7 Semantic transition model | Normative |
| `OLS4-CLS-0019` | `TRACE-000141` | 8 Outcome admission | Normative |
| `OLS4-CLS-0020` | `TRACE-000142` | 9 Recording eligibility | Normative |
| `OLS4-CLS-0021` | `TRACE-000143` | 10 Learning eligibility | Normative |
| `OLS4-CLS-0022` | `TRACE-000144` | 11 Prohibited derivations | Normative |
| `OLS4-CLS-0023` | `TRACE-000145` | 12 Transition failure model | Normative |
| `OLS4-CLS-0024` | `TRACE-000146` | 13 Rejected and analytical derivations | Normative |
| `OLS4-CLS-0025` | `TRACE-000147` | 14 Non-transformation cases | Normative |
| `OLS4-CLS-0026` | `TRACE-000148` | 15 Cross-profile responsibility and summary | Normative |
| `OLS4-ANNEX-A` | `TRACE-000149` | Annex A — Semantic Product Registry | Normative |
| `OLS4-ANNEX-B` | `TRACE-000150` | Annex B — Semantic Transition Matrix | Normative |
| `OLS4-ANNEX-C` | `TRACE-000151` | Annex C — Prohibited Derivation Registry | Normative |
| `OLS4-ANNEX-D` | `TRACE-000152` | Annex D — Example Derivation Chains | Informative |
| `OLS4-ANNEX-E` | `TRACE-000153` | Annex E — Illegal Transition Examples | Informative |
| `OLS4-ANNEX-F` | `TRACE-000154` | Annex F — Architectural Traceability | Informative |
| `OLS5-CLS-0001` | `TRACE-000155` | 1 Scope | Normative |
| `OLS5-CLS-0002` | `TRACE-000156` | 2 Normative references | Normative |
| `OLS5-CLS-0003` | `TRACE-000157` | 3 Terms and conformance philosophy | Normative |
| `OLS5-CLS-0004` | `TRACE-000158` | 4 Conformance targets | Normative |
| `OLS5-CLS-0005` | `TRACE-000159` | 5 Conformance classes | Normative |
| `OLS5-CLS-0006` | `TRACE-000160` | 6 Conformance units and applicability | Normative |
| `OLS5-CLS-0007` | `TRACE-000161` | 7 Requirement-to-test coverage | Normative |
| `OLS5-CLS-0008` | `TRACE-000162` | 8 Normative test model | Normative |
| `OLS5-CLS-0009` | `TRACE-000163` | 9 Conformance statuses and aggregation | Normative |
| `OLS5-CLS-0010` | `TRACE-000164` | 10 Conformance evidence | Normative |
| `OLS5-CLS-0011` | `TRACE-000165` | 11 Conformance reporting | Normative |
| `OLS5-CLS-0012` | `TRACE-000166` | 12 Certification boundaries | Normative |
| `OLS5-CLS-0013` | `TRACE-000167` | 13 Implementation independence and partial capability | Normative |
| `OLS5-CLS-0014` | `TRACE-000168` | 14 Summary | Normative |
| `OLS5-ANNEX-A` | `TRACE-000169` | Annex A — Conformance Class Registry | Normative |
| `OLS5-ANNEX-B` | `TRACE-000170` | Annex B — Requirement-to-Test Matrix | Normative |
| `OLS5-ANNEX-C` | `TRACE-000171` | Annex C — Conformance Status Registry | Normative |
| `OLS5-ANNEX-D` | `TRACE-000172` | Annex D — Example Test Reports | Informative |
| `OLS5-ANNEX-E` | `TRACE-000173` | Annex E — Example Failure Reports | Informative |
| `OLS5-ANNEX-F` | `TRACE-000174` | Annex F — Architectural Traceability | Informative |
| `OLS6-CLS-0001` | `TRACE-000175` | 1 Scope | Normative |
| `OLS6-CLS-0002` | `TRACE-000176` | 2 Normative references | Normative |
| `OLS6-CLS-0003` | `TRACE-000177` | 3 Terms and governance model | Normative |
| `OLS6-CLS-0004` | `TRACE-000178` | 4 Compatibility principles | Normative |
| `OLS6-CLS-0005` | `TRACE-000179` | 5 Extension categories | Normative |
| `OLS6-CLS-0006` | `TRACE-000180` | 6 Extension registration lifecycle | Normative |
| `OLS6-CLS-0007` | `TRACE-000181` | 7 Future profile registration | Normative |
| `OLS6-CLS-0008` | `TRACE-000182` | 8 Future operator registration | Normative |
| `OLS6-CLS-0009` | `TRACE-000183` | 9 Future declaration registration | Normative |
| `OLS6-CLS-0010` | `TRACE-000184` | 10 Future informative components | Normative |
| `OLS6-CLS-0011` | `TRACE-000185` | 11 Identifier, namespace, and ownership governance | Normative |
| `OLS6-CLS-0012` | `TRACE-000186` | 12 Dependencies, composition, and conflicts | Normative |
| `OLS6-CLS-0013` | `TRACE-000187` | 13 Extension conformance and testing | Normative |
| `OLS6-CLS-0014` | `TRACE-000188` | 14 Version number model | Normative |
| `OLS6-CLS-0015` | `TRACE-000189` | 15 Change classification | Normative |
| `OLS6-CLS-0016` | `TRACE-000190` | 16 Major, minor, and editorial releases | Normative |
| `OLS6-CLS-0017` | `TRACE-000191` | 17 Backward compatibility | Normative |
| `OLS6-CLS-0018` | `TRACE-000192` | 18 Architecture-revision boundary | Normative |
| `OLS6-CLS-0019` | `TRACE-000193` | 19 Deprecation and historical preservation | Normative |
| `OLS6-CLS-0020` | `TRACE-000194` | 20 Change control and review | Normative |
| `OLS6-CLS-0021` | `TRACE-000195` | 21 Publication lifecycle | Normative |
| `OLS6-CLS-0022` | `TRACE-000196` | 22 Release management and manifest | Normative |
| `OLS6-CLS-0023` | `TRACE-000197` | 23 Registry governance | Normative |
| `OLS6-CLS-0024` | `TRACE-000198` | 24 Errata, preservation, and summary | Normative |
| `OLS6-ANNEX-A` | `TRACE-000199` | Annex A — Extension Registration Template | Normative |
| `OLS6-ANNEX-B` | `TRACE-000200` | Annex B — Version Compatibility Declaration | Normative |
| `OLS6-ANNEX-C` | `TRACE-000201` | Annex C — Change Examples | Informative |
| `OLS6-ANNEX-D` | `TRACE-000202` | Annex D — Architecture-Revision Referral Guide | Informative |

---

## End of OLS-I

OLS-I is informative in its entirety. OLS-0 through OLS-6 remain controlling.
