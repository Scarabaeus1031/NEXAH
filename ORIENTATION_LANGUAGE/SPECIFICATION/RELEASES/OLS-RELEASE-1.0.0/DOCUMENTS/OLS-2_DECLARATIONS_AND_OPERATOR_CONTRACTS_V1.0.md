# Orientation Language Specification — OLS-2

## Declarations and Operator Contracts

| Metadata field | Value |
| --- | --- |
| Document ID | `OLS-2` |
| Edition | 1 |
| Suite version | `1.0.0` |
| Document revision | `1.0.0` |
| Status | Version 1.0 publication candidate |
| Publication date | 17 July 2026 |
| Language | English |
| Normative scope | Declaration system and complete primitive operator contracts |
| Semantic scope | Ten frozen declarations; contracts for ten frozen primitive operators; ownership, invocation, sequencing, and failure structure |
| Replaces | Phase 2D declaration and primitive-operator contract summaries upon suite publication |
| Normative dependencies | `OLS-0`, `OLS-1` |
| Forward references | `OLS-3` for profile activation and composition; `OLS-5` for conformance procedures |
| Release manifest identifier | Pending assignment at suite publication |
| Persistent citation identifier | Unassigned |
| Architecture baseline | Phase 2D Canonical Architecture, frozen by ADR-0001 |

## Status of this document

OLS-2 is the authoritative specification of Orientation Language declarations and primitive operator contracts. Except for Annexes D and E, all clauses and annexes in this document are **Normative**.

OLS-2 adds operational precision to semantic responsibilities frozen by Phase 2D and specified by OLS-1. It does not add concepts, declarations, operators, profiles, derivations, or implementation requirements.

---

## 1 Scope

*Stable clause ID: `OLS2-CLS-0001` — Trace ID: `TRACE-000060` — Normative*

OLS-2 specifies:

- a common declaration model;
- exactly ten declarations;
- a common primitive operator contract model;
- complete contracts for five universal and five profile primitive operators;
- primitive operator ownership;
- operator invocation, composition, and sequencing structure;
- incomplete and malformed invocation conditions.

`[OLS2-REQ-0001]` OLS-2 shall preserve every universal concept and primitive operator responsibility specified by OLS-1.

`[OLS2-REQ-0002]` OLS-2 shall contain exactly the ten declarations and ten primitive operator contracts registered in Annexes A and B.

`[OLS2-REQ-0003]` OLS-2 shall not define profile activation, profile composition, derivations, conformance procedures, governance, or implementation architecture.

## 2 Normative references

*Stable clause ID: `OLS2-CLS-0002` — Trace ID: `TRACE-000061` — Normative*

The following documents are normatively indispensable to OLS-2:

- Orientation Language Specification, `OLS-0`, *Specification Conventions and Suite Overview*, Edition 1, suite version `1.0.0`;
- Orientation Language Specification, `OLS-1`, *Universal Base Language*, Edition 1, suite version `1.0.0`.

`[OLS2-REQ-0004]` OLS-2 shall use OLS-0 conventions and shall not change an OLS-1 definition, boundary, inventory, process, or operator responsibility.

## 3 Terms and definitions

*Stable clause ID: `OLS2-CLS-0003` — Trace ID: `TRACE-000062` — Normative*

OLS-1 controls universal semantic terms. OLS-2 controls the declarations registered in Annex A, the primitive Operator IDs registered in Annex B, and the contract fields registered in Annex C.

For OLS-2:

- **declaration** means an explicit instance-level value or status supplied for a semantic distinction;
- **declaration scope** means the construction, invocation, assertion, or artifact to which a declaration value applies;
- **operator contract** means the normative record of one primitive operator’s owner, inputs, declarations, preconditions, operation, outputs, preserved status, failures, prohibited implications, and traceability;
- **invocation** means a declared application of one operator contract to specified inputs under specified declarations;
- **unsupported declaration** means an explicit declaration whose value or status lacks the support needed for the claim that depends on it.

`[OLS2-REQ-0005]` OLS-2 terms shall be interpreted consistently with OLS-1 and shall not create additional universal primitives.

`[OLS2-REQ-0006]` An unsupported declaration shall remain explicit and speculative and shall not satisfy a requirement that depends on supported status.

`[OLS2-REQ-0007]` Ordinary implementation terms shall not acquire semantic authority through use in an invocation or contract mapping.

## 4 Declaration model

*Stable clause ID: `OLS2-CLS-0004` — Trace ID: `TRACE-000063` — Normative*

### 4.1 Purpose and ownership

Declarations make instance-level assumptions, values, statuses, and boundaries explicit. Annex A owns the Version 1.0 declaration registry. OLS-2 owns declaration definitions; it does not own the universal concepts or profile semantics to which declarations may apply.

`[OLS2-REQ-0008]` A declaration shall supply an explicit value or status and shall not redefine the semantic distinction to which it applies.

`[OLS2-REQ-0009]` A declaration shall have one Declaration ID, one owner, one declared value or status, and an identifiable scope.

`[OLS2-REQ-0010]` No declaration shall acquire an inferred default.

### 4.2 Applicability

A declaration is applicable when the interpretation or validity of a claim or invocation depends on the distinction represented by that declaration.

`[OLS2-REQ-0011]` Every applicable declaration shall be present before the dependent claim or operator output is treated as complete.

`[OLS2-REQ-0012]` Applicability shall be determined by the claims made and the owning declaration clause, not by implementation convenience.

### 4.3 Omission

An omitted declaration is valid only when no claim in its scope depends on that distinction.

`[OLS2-REQ-0013]` Omission shall not authorize an inferred value.

`[OLS2-REQ-0014]` Omission of an applicable declaration shall make the dependent construction or invocation incomplete.

### 4.4 Incompatibility

Declarations are incompatible when their values, statuses, or scopes cannot simultaneously support the same claimed operation or interpretation.

`[OLS2-REQ-0015]` Incompatible declarations shall make the affected construction or invocation malformed.

`[OLS2-REQ-0016]` No precedence rule shall silently select one incompatible declaration over another.

### 4.5 Unsupported declarations

An unsupported declaration remains a declared proposal or speculative status. Explicitness alone does not make it valid.

`[OLS2-REQ-0017]` An unsupported declaration shall identify its unsupported status and the dependent claims it limits.

`[OLS2-REQ-0018]` An unsupported declaration shall not be silently promoted to observed, validated, canonical, or authoritative status.

### 4.6 Scope and preservation

Declaration scope identifies where a value or status applies. A declaration may be referenced by multiple invocations only when its scope covers them and its value remains compatible.

`[OLS2-REQ-0019]` An operator output shall preserve every input declaration whose distinction remains relevant to that output.

`[OLS2-REQ-0020]` Changing a declaration value or scope shall create an explicit new declaration state or reference and shall not overwrite the earlier value without trace.

`[OLS2-REQ-0021]` A declaration reference shall identify the Declaration ID, value or status, scope, and source or controlling record.

`[OLS2-REQ-0022]` Provenance shall be preserved as an OLS-1 universal status and shall not be introduced as an eleventh declaration.

## 5 Frozen declarations

*Stable clause ID: `OLS2-CLS-0005` — Trace ID: `TRACE-000064` — Normative*

The Version 1.0 declaration system contains exactly: time, identity, scale, context, perspective, position, representation type, evidence class, uncertainty status, and authority scope.

`[OLS2-REQ-0023]` Each declaration shall retain the definition, responsibility, applicability, omission, incompatibility, preservation, and dependency rules of its owning subsection.

`[OLS2-REQ-0024]` A term not listed in Annex A shall not be represented as a Version 1.0 declaration.

`[OLS2-REQ-0025]` The examples in Clause 5 and Annex D are informative and shall not constrain the permitted declaration value forms.

### 5.1 time

*Stable clause ID: `OLS2-CLS-0006` — Declaration ID: `DECL-TIME` — Trace ID: `TRACE-000065` — Normative*

| Field | Specification |
| --- | --- |
| Definition | Temporal position or order expressed as a declared reference, ordering, or interval. |
| Semantic responsibility | Makes temporal position, sequence, history, change, or recurrence explicit. |
| Applicability | Observations where sequence matters; states, transitions, trajectories, recurrence, records, outcomes, learning, and any before/after claim. |
| Valid omission | The scope makes no temporal, sequence, history, change, or recurrence claim. |
| Invalid omission | A transition, trajectory, provenance history, outcome, learning, or before/after relation is asserted. |
| Incompatibility | Temporal references, intervals, or orderings cannot support one asserted sequence or continuity. |
| Preservation | Outputs preserve the temporal reference or explicitly identify a new reference while retaining the earlier one. |
| Dependencies | Identity where same-subject continuity is claimed; context and scale where they affect temporal interpretation. |

`[OLS2-REQ-0026]` A time-dependent claim shall include `DECL-TIME`.

`[OLS2-REQ-0027]` A transition or before/after assertion without `DECL-TIME` shall be incomplete.

`[OLS2-REQ-0028]` Incompatible temporal orders for the same asserted sequence shall be malformed unless preserved as explicit disagreement or uncertainty.

`[OLS2-REQ-0029]` An operator shall preserve the applicable temporal reference through its output.

**Informative example:** “reading A precedes reading B during interval T” supplies an ordering and interval; “A changed” without temporal reference does not.

### 5.2 identity

*Stable clause ID: `OLS2-CLS-0007` — Declaration ID: `DECL-IDENTITY` — Trace ID: `TRACE-000066` — Normative*

| Field | Specification |
| --- | --- |
| Definition | Same-subject, work, or system continuity expressed by a declared identity criterion or referenced identity. |
| Semantic responsibility | Makes explicit why items across states, times, records, trajectories, outcomes, or editions are treated as the same continuing subject. |
| Applicability | Comparison across states or time; trajectory; provenance continuity; memory or outcome; editorial Work or edition continuity. |
| Valid omission | No same-subject continuity, persistence, or version relation is asserted. |
| Invalid omission | States, records, outcomes, trajectories, or editions are treated as belonging to the same subject. |
| Incompatibility | Identity criteria assign incompatible continuity or refer to different subjects within one continuity claim. |
| Preservation | Outputs preserve the identity criterion or explicitly state a changed identity relation. |
| Dependencies | Time for continuity across order; context and scale where identity depends on domain or level. |

`[OLS2-REQ-0030]` A continuity claim shall include `DECL-IDENTITY`.

`[OLS2-REQ-0031]` Identity shall not be inferred solely from naming, proximity, similarity, or sequence.

`[OLS2-REQ-0032]` Incompatible identity criteria within one continuity claim shall make that claim malformed.

`[OLS2-REQ-0033]` An operator shall preserve the applicable identity criterion when its output asserts continuity.

**Informative example:** two records cite one stable Work identifier; similar titles without an identity criterion do not establish continuity.

### 5.3 scale

*Stable clause ID: `OLS2-CLS-0008` — Declaration ID: `DECL-SCALE` — Trace ID: `TRACE-000067` — Normative*

| Field | Specification |
| --- | --- |
| Definition | Level or dimensionality of reading expressed as a declared level, dimensionality, or scale. |
| Semantic responsibility | Makes explicit the level at which representation, comparison, pattern, navigation, or transition meaning is asserted. |
| Applicability | Representations and comparisons where level affects meaning; maps, fields, geometry, navigation, patterns, transitions, and cross-scale claims. |
| Valid omission | Scale cannot alter the asserted interpretation and no cross-scale claim is made. |
| Invalid omission | Compatibility, cross-scale comparison, navigation, pattern, or transition depends on level. |
| Incompatibility | Scale values cannot support the claimed comparison or are combined without an explicit cross-scale basis. |
| Preservation | Outputs retain the applicable scale or explicitly record scale translation without erasing source scale. |
| Dependencies | Representation type; context; comparison basis where multiple scales are used. |

`[OLS2-REQ-0034]` A scale-dependent or cross-scale claim shall include `DECL-SCALE`.

`[OLS2-REQ-0035]` Items at incompatible scales shall not be treated as directly comparable without an explicit compatible basis.

`[OLS2-REQ-0036]` Scale omission shall be valid only under the omission condition in this clause.

`[OLS2-REQ-0037]` An operator shall preserve source scale when producing a result at another declared scale.

**Informative example:** a component-level reading and system-level reading identify both scales before comparison.

### 5.4 context

*Stable clause ID: `OLS2-CLS-0009` — Declaration ID: `DECL-CONTEXT` — Trace ID: `TRACE-000068` — Normative*

| Field | Specification |
| --- | --- |
| Definition | Situational conditions and scope expressed as declared applicable conditions, domain, and scope. |
| Semantic responsibility | Bounds interpretation of observations, relations, representations, comparisons, orientations, and explanations. |
| Applicability | Every orientation act and every representation reading; other semantic assertions where situation or scope affects interpretation. |
| Valid omission | Never for an orientation act or representation reading; a narrower non-orientation source record may omit context only when it makes no contextual interpretation. |
| Invalid omission | An observation, relation, representation, comparison, orientation, or explanation is interpreted without applicable situation or scope. |
| Incompatibility | Contexts assign mutually incompatible conditions, domains, or scopes to one asserted interpretation. |
| Preservation | Outputs retain the context of source assertions and identify any new context without replacing the source context silently. |
| Dependencies | Perspective for construction or reading; representation type; time, scale, identity, or position when contextual meaning depends on them. |

`[OLS2-REQ-0038]` Every orientation act and representation reading shall include `DECL-CONTEXT`.

`[OLS2-REQ-0039]` A claim shall not be generalized beyond its declared context without a separately declared and supported context.

`[OLS2-REQ-0040]` Incompatible contexts shall not be merged by omission or precedence.

`[OLS2-REQ-0041]` An operator shall preserve source context when its output introduces a different context.

**Informative example:** a reading declares the operating conditions and domain under which it applies.

### 5.5 perspective

*Stable clause ID: `OLS2-CLS-0010` — Declaration ID: `DECL-PERSPECTIVE` — Trace ID: `TRACE-000069` — Normative*

| Field | Specification |
| --- | --- |
| Definition | Condition or view of construction or reading expressed as a declared construction perspective or reading perspective. |
| Semantic responsibility | Makes the standpoint or view governing representation construction and interpretation explicit. |
| Applicability | Representation construction and reading; orientation; multi-perspective comparison. |
| Valid omission | Never where a representation or orientation claim is made. |
| Invalid omission | A viewpoint is presented as perspective-free or construction and reading perspectives are conflated. |
| Incompatibility | Perspectives are treated as one view despite incompatible construction or reading conditions. |
| Preservation | Outputs retain each applicable perspective and keep disagreements distinct. |
| Dependencies | Context; representation type; position where the view is location-dependent. |

`[OLS2-REQ-0042]` Every representation and orientation claim shall include `DECL-PERSPECTIVE`.

`[OLS2-REQ-0043]` Construction and reading perspectives shall be distinguished when both apply.

`[OLS2-REQ-0044]` Incompatible perspectives shall remain separately identified unless an explicit compatible relation is supported.

`[OLS2-REQ-0045]` An operator shall preserve perspective-specific agreements, disagreements, evidence, and uncertainty.

**Informative example:** one representation declares the view used to construct it and a reader declares a different view used to interpret it.

### 5.6 position

*Stable clause ID: `OLS2-CLS-0011` — Declaration ID: `DECL-POSITION` — Trace ID: `TRACE-000070` — Normative*

| Field | Specification |
| --- | --- |
| Definition | Located observer, focus, or system expressed as a declared focus or location relative to a representation and context. |
| Semantic responsibility | Makes the location from which a position-dependent assertion is made explicit. |
| Applicability | Locating, reachability, blocked-region, navigation, or other position-dependent orientation claims. |
| Valid omission | No position-dependent or reachability claim is made. |
| Invalid omission | A claim states where something is, what is reachable, or how to navigate without a located focus. |
| Incompatibility | Positions cannot simultaneously locate the same identified focus under the same context, time, scale, and representation basis. |
| Preservation | Outputs retain source position or explicitly identify relocation without erasing the earlier position. |
| Dependencies | Representation type and context; scale and time where location depends on them; identity where the positioned focus persists. |

`[OLS2-REQ-0046]` A position-dependent assertion shall include `DECL-POSITION`.

`[OLS2-REQ-0047]` Position omission shall not authorize an inferred location.

`[OLS2-REQ-0048]` Incompatible positions for the same declared basis shall be malformed unless represented as distinct perspectives, times, or uncertainty.

`[OLS2-REQ-0049]` An operator changing the relevant location shall preserve both source and resulting position references.

**Informative example:** a focus is located relative to a declared graph node or map region without implying a route or recommendation.

### 5.7 representation type

*Stable clause ID: `OLS2-CLS-0012` — Declaration ID: `DECL-REPRESENTATION-TYPE` — Trace ID: `TRACE-000071` — Normative*

| Field | Specification |
| --- | --- |
| Definition | Kind of structured form used to represent declared material. |
| Semantic responsibility | Makes representation semantics and compatibility inspectable without treating the representation as reality. |
| Applicability | Every REPRESENT output and every ORIENT input using a representation. |
| Valid omission | Never for a representation used in orientation. |
| Invalid omission | Representation semantics or compatibility are left implicit. |
| Incompatibility | Representation types cannot support the claimed operation or are combined without a declared compatible basis. |
| Preservation | Outputs retain the source representation type and identify any newly constructed type. |
| Dependencies | Context and perspective; scale where type interpretation depends on level; provenance as universal status. |

`[OLS2-REQ-0050]` Every REPRESENT output and represented ORIENT input shall include `DECL-REPRESENTATION-TYPE`.

`[OLS2-REQ-0051]` A representation type shall not be inferred from visual appearance, file format, or implementation technology alone.

`[OLS2-REQ-0052]` Incompatible representation types shall not be combined or compared without an explicit compatible basis.

`[OLS2-REQ-0053]` Type conversion shall preserve the source type, provenance, status, and uncertainty.

**Informative example:** a construction labels its structured form as a graph, field, map, model, slice, or editorial form; the label does not validate it.

### 5.8 evidence class

*Stable clause ID: `OLS2-CLS-0013` — Declaration ID: `DECL-EVIDENCE-CLASS` — Trace ID: `TRACE-000072` — Normative*

| Field | Specification |
| --- | --- |
| Definition | Epistemic status of supporting material. |
| Semantic responsibility | Keeps observed, simulated, inferred, proposed, validated, and other declared evidence statuses distinguishable. |
| Applicability | Claims admitted to orientation, validation, explanation, or report. |
| Valid omission | No claim is admitted as evidence. |
| Invalid omission | Observation, simulation, inference, proposal, and validated result could be conflated. |
| Incompatibility | One item is assigned mutually exclusive evidence statuses under the same basis without explicit status history or disagreement. |
| Preservation | Outputs retain each evidence class and record any governed status change without overwriting the earlier class. |
| Dependencies | Provenance and uncertainty as universal statuses; time and identity where evidence status changes or persists. |

`[OLS2-REQ-0054]` Material used as evidence shall include `DECL-EVIDENCE-CLASS`.

`[OLS2-REQ-0055]` Model output, simulation, inference, proposal, or validation status shall not be represented as observed solely by relabeling its evidence class.

`[OLS2-REQ-0056]` Incompatible evidence classes shall remain visible as conflict, history, or uncertainty and shall not be silently collapsed.

`[OLS2-REQ-0057]` An operator shall preserve evidence class through every output that uses or communicates the material.

**Informative example:** a simulated result remains “simulated” when included in an orientation and explanation.

### 5.9 uncertainty status

*Stable clause ID: `OLS2-CLS-0014` — Declaration ID: `DECL-UNCERTAINTY-STATUS` — Trace ID: `TRACE-000073` — Normative*

| Field | Specification |
| --- | --- |
| Definition | Status of unresolved or bounded lack of knowledge. |
| Semantic responsibility | Makes known limitations, missing information, disagreements, and unresolved status explicit. |
| Applicability | Comparison, orientation, explanation, validation, and reporting whenever a finding is produced. |
| Valid omission | No finding is produced and no unresolved status affects the asserted material. |
| Invalid omission | Uncertainty is relevant to a finding but omitted or silently converted into confidence. |
| Incompatibility | Statuses claim both resolved and unresolved treatment of the same issue under the same basis without history or scope distinction. |
| Preservation | Outputs retain unresolved status and identify an explicit supported change without erasing prior uncertainty. |
| Dependencies | Evidence class and provenance; context, perspective, time, identity, or scale where uncertainty is scoped by them. |

`[OLS2-REQ-0058]` Every comparison, orientation, explanation, validation, or report finding shall include `DECL-UNCERTAINTY-STATUS`.

`[OLS2-REQ-0059]` Uncertainty shall not be silently replaced by confidence or certainty.

`[OLS2-REQ-0060]` Incompatible uncertainty statuses shall be preserved as explicit conflict or scoped difference.

`[OLS2-REQ-0061]` An operator shall preserve known limitations, missing information, disagreement, and unresolved status relevant to its output.

**Informative example:** a finding identifies missing source coverage rather than assigning an unsupported confidence value.

### 5.10 authority scope

*Stable clause ID: `OLS2-CLS-0015` — Declaration ID: `DECL-AUTHORITY-SCOPE` — Trace ID: `TRACE-000074` — Normative*

| Field | Specification |
| --- | --- |
| Definition | Permission boundary for a governed act expressed by a declared actor or role, governed operation, target, and applicable scope. |
| Semantic responsibility | Keeps evidence, orientation, and validation distinct from permission to perform or approve a governed act. |
| Applicability | Approval, recommendation, publication, execution, and AI pre-action handoff. |
| Valid omission | No governed act or authority claim occurs. |
| Invalid omission | Evidence, orientation, or validation is used as permission, or a governed status changes. |
| Incompatibility | Actors, operations, targets, or scopes assign conflicting permission for the same governed act without an explicit governing resolution. |
| Preservation | Outputs retain the authority source, scope, target, and status transition; narrower or changed authority is separately declared. |
| Dependencies | Identity of governed subject or Work; context; time where authority is time-bounded; provenance of the authority record. |

`[OLS2-REQ-0062]` A governed act or authority claim shall include `DECL-AUTHORITY-SCOPE`.

`[OLS2-REQ-0063]` Orientation, evidence, validation, or explanation shall not be treated as authority.

`[OLS2-REQ-0064]` Incompatible authority scopes shall not be resolved by operator order or implementation precedence.

`[OLS2-REQ-0065]` An authority-bearing output shall preserve actor or role, governed operation, target, scope, and authority status.

**Informative example:** an approval identifies who may approve which change for which publication target; a favorable orientation alone grants no permission.

## 6 Primitive Operator Contract Model

*Stable clause ID: `OLS2-CLS-0016` — Trace ID: `TRACE-000075` — Normative*

Every primitive operator contract uses the fields in Annex C.

`[OLS2-REQ-0066]` A primitive operator contract shall identify purpose, semantic owner, inputs, required declarations, preconditions, operation, outputs, preserved status, failure conditions, prohibited implications, and traceability.

`[OLS2-REQ-0067]` Contract fields shall describe semantic obligations independently of software, data format, interface, storage, or execution technology.

`[OLS2-REQ-0068]` A contract shall not change its owner’s frozen semantic responsibility.

`[OLS2-REQ-0069]` Inputs shall identify the semantic material accepted by the operator without implying implementation types.

`[OLS2-REQ-0070]` Required declarations shall include every Annex A distinction on which the invocation or output depends.

`[OLS2-REQ-0071]` Preconditions shall be satisfied before an invocation is treated as complete.

`[OLS2-REQ-0072]` Outputs shall identify semantic products and preserved statuses without implying successful external execution.

`[OLS2-REQ-0073]` Preserved status shall include applicable provenance, evidence class, uncertainty, declarations, disagreements, and limitations.

`[OLS2-REQ-0074]` Failure conditions shall classify missing requirements as incomplete and incompatible or boundary-violating assertions as malformed under Clause 12.

`[OLS2-REQ-0075]` Prohibited implications shall remain valid regardless of implementation behavior or operator composition.

## 7 Universal Primitive Operator Contracts

*Stable clause ID: `OLS2-CLS-0017` — Trace ID: `TRACE-000076` — Normative*

The Universal Base Language owns OBSERVE, REPRESENT, COMPARE, ORIENT, and EXPLAIN. Their responsibilities are identical to OLS-1.

`[OLS2-REQ-0076]` Every universal primitive invocation shall preserve the OLS-1 Universal Boundary Matrix.

`[OLS2-REQ-0077]` Operational detail in Clause 7 shall not broaden a universal operator responsibility.

### 7.1 OBSERVE

*Stable clause ID: `OLS2-CLS-0018` — Operator ID: `OP-OBSERVE` — Trace ID: `TRACE-000077` — Normative*

| Contract field | Specification |
| --- | --- |
| Purpose | Notice or capture declared signals, events, measurements, or context as observations. |
| Semantic owner | Universal Base Language. |
| Inputs | Declared source material and its identifiable source/provenance status. |
| Required declarations | Context when interpreted; time when sequence matters; evidence class when material is used as evidence; uncertainty status when unresolved status affects the observation or a finding. |
| Preconditions | Source material is identifiable; applicable declarations are present; source status is not silently promoted. |
| Operation | Admit or notice source material as observations while preserving source status. |
| Outputs | One or more observations linked to source/provenance and applicable declarations. |
| Preserved status | Source, provenance, time, context, evidence class where assigned, uncertainty, and unsupported status. |
| Failure conditions | Missing identifiable source or applicable declaration: incomplete; incompatible declarations or status promotion: malformed. |
| Prohibited implications | Truth, completeness, neutrality, evidence, causality, or outcome. |
| Traceability | OLS-1 `OLS1-CLS-0023`; Phase 2D Universal Base Language and operator ownership. |

`[OLS2-REQ-0078]` OBSERVE shall not create evidence, validation, or outcome status solely by admission.

`[OLS2-REQ-0079]` OBSERVE shall preserve the source and epistemic status of every output observation.

### 7.2 REPRESENT

*Stable clause ID: `OLS2-CLS-0019` — Operator ID: `OP-REPRESENT` — Trace ID: `TRACE-000078` — Normative*

| Contract field | Specification |
| --- | --- |
| Purpose | Transform declared observations or data into a structured, analyzable form while preserving provenance and status. |
| Semantic owner | Universal Base Language. |
| Inputs | Declared observations or data with source/provenance and status. |
| Required declarations | Context, perspective, representation type; scale when meaning depends on level; time and identity when continuity or sequence is represented; evidence class and uncertainty status when carried into claims. |
| Preconditions | Inputs and source status are identifiable; construction perspective and representation type are declared; applicable declarations are compatible. |
| Operation | Construct a representation without identifying it with its source or reality. |
| Outputs | A declared representation linked to its inputs, type, perspective, provenance, and applicable statuses. |
| Preserved status | Source, provenance, evidence class, uncertainty, context, perspective, time, identity, and scale as applicable. |
| Failure conditions | Missing type, construction perspective, context, or source status: incomplete; incompatible declarations or representation/reality collapse: malformed. |
| Prohibited implications | Reality, completeness, causal mechanism, or validation. |
| Traceability | OLS-1 `OLS1-CLS-0024`; Phase 2D Universal Base Language and operator ownership. |

`[OLS2-REQ-0080]` REPRESENT shall identify its output as a representation and shall preserve the representation/reality distinction.

`[OLS2-REQ-0081]` REPRESENT shall not change the evidence or uncertainty status of input material unless a separately owned operation supports that change.

### 7.3 COMPARE

*Stable clause ID: `OLS2-CLS-0020` — Operator ID: `OP-COMPARE` — Trace ID: `TRACE-000079` — Normative*

| Contract field | Specification |
| --- | --- |
| Purpose | Identify differences, agreements, or mismatches among declared compatible items relative to a declared basis. |
| Semantic owner | Universal Base Language. |
| Inputs | Two or more declared items and a declared comparison basis. |
| Required declarations | Context and perspective; representation type where represented items are used; scale, time, and identity where compatibility depends on them; evidence class and uncertainty status for findings. |
| Preconditions | Items and basis are identifiable; compatibility is supported; applicable declarations are present and compatible. |
| Operation | Identify differences, agreements, or mismatches without defining difference or assigning downstream status. |
| Outputs | Comparison findings linked to items, basis, declarations, evidence, provenance, and uncertainty. |
| Preserved status | Item identity, representation type, context, perspective, scale, time, evidence class, provenance, uncertainty, and disagreement as applicable. |
| Failure conditions | Missing item, basis, compatibility, or applicable declaration: incomplete; incompatible items treated as compatible or prohibited implication asserted: malformed. |
| Prohibited implications | Causality, preference, selection, validation, prediction, or universal law. |
| Traceability | OLS-1 `OLS1-CLS-0025`; ADR-0001 Decision 2; Phase 2D operator ownership. |

`[OLS2-REQ-0082]` COMPARE shall identify every compared item and the comparison basis.

`[OLS2-REQ-0083]` COMPARE shall depend on the universal primitive difference and shall not define or generate its semantic responsibility.

### 7.4 ORIENT

*Stable clause ID: `OLS2-CLS-0021` — Operator ID: `OP-ORIENT` — Trace ID: `TRACE-000080` — Normative*

| Contract field | Specification |
| --- | --- |
| Purpose | Produce situated understanding from declared observations, representation, context, perspective, position or focus, evidence, provenance, and uncertainty. |
| Semantic owner | Universal Base Language. |
| Inputs | Declared observations, representation, comparison findings, context, perspective, position or focus, evidence, provenance, uncertainty, and limitations. |
| Required declarations | Context, perspective, representation type, evidence class, uncertainty status; position for position-dependent claims; time, scale, and identity when the orientation depends on them. |
| Preconditions | Inputs and their statuses are identifiable; representation and comparison basis are declared; applicable declarations are present and compatible. |
| Operation | Produce situated understanding bounded by the declared material and conditions. |
| Outputs | An orientation identifying supported findings, disagreements, unsupported conclusions, uncertainty, limitations, and applicable declarations. |
| Preserved status | Observation/source status, representation type, context, perspective, position, evidence class, provenance, uncertainty, disagreement, unsupported conclusions, and limitations. |
| Failure conditions | Missing representation, context, perspective, evidence class, uncertainty status, source status, or applicable basis: incomplete; incompatible declarations or downstream implication asserted: malformed. |
| Prohibited implications | Recommendation, authorization, execution, outcome, learning, control, or certainty. |
| Traceability | OLS-1 `OLS1-CLS-0026`; Phase 2D Universal Base Language and operator ownership. |

`[OLS2-REQ-0084]` ORIENT shall identify the declared basis and limits of its situated understanding.

`[OLS2-REQ-0085]` ORIENT shall preserve supported findings, disagreements, unsupported conclusions, and uncertainty as distinct statuses.

### 7.5 EXPLAIN

*Stable clause ID: `OLS2-CLS-0022` — Operator ID: `OP-EXPLAIN` — Trace ID: `TRACE-000081` — Normative*

| Contract field | Specification |
| --- | --- |
| Purpose | Communicate structured findings while preserving evidence, uncertainty, disagreement, unsupported conclusions, and limitations. |
| Semantic owner | Universal Base Language. |
| Inputs | Declared findings or orientation together with evidence, provenance, uncertainty, disagreements, unsupported conclusions, limitations, and applicable declarations. |
| Required declarations | Context, perspective, representation type where represented findings are explained, evidence class, uncertainty status, and any position, time, scale, or identity on which the explanation depends. |
| Preconditions | Communicated material and statuses are identifiable; applicable declarations are present and compatible. |
| Operation | Structure and communicate findings without increasing epistemic, authority, or publication status. |
| Outputs | An explanation retaining the declared findings, support, disagreement, unsupported status, uncertainty, and limitations. |
| Preserved status | Evidence class, provenance, uncertainty, context, perspective, representation type, disagreement, unsupported conclusions, and limitations. |
| Failure conditions | Missing source finding or status needed for interpretation: incomplete; status elevation, omission of known uncertainty, or prohibited implication: malformed. |
| Prohibited implications | Truth, proof, consensus, authority, recommendation, or publication approval. |
| Traceability | OLS-1 `OLS1-CLS-0027`; Phase 2D Universal Base Language and operator ownership. |

`[OLS2-REQ-0086]` EXPLAIN shall preserve the status of every finding it communicates.

`[OLS2-REQ-0087]` EXPLAIN shall not convert communication into proof, consensus, authority, recommendation, or approval.

## 8 Profile Primitive Operator Contracts

*Stable clause ID: `OLS2-CLS-0023` — Trace ID: `TRACE-000082` — Normative*

SELECT, TRANSFORM, VALIDATE, RECORD, and APPROVE are primitive operators owned by the profiles identified in Annex B. OLS-2 specifies their contracts but does not specify their owning profiles beyond ownership and contract reference.

`[OLS2-REQ-0088]` Invocation of a profile primitive operator shall refer to its owner and applicable profile rules in OLS-3.

`[OLS2-REQ-0089]` A profile primitive operator shall not modify a universal concept, operator responsibility, or boundary.

`[OLS2-REQ-0090]` Clause 8 shall not be interpreted as profile activation or profile composition semantics.

### 8.1 SELECT

*Stable clause ID: `OLS2-CLS-0024` — Operator ID: `OP-SELECT` — Trace ID: `TRACE-000083` — Normative*

| Contract field | Specification |
| --- | --- |
| Purpose | Choose among declared alternatives under a declared selection basis or constraint. |
| Semantic owner | Navigation Profile. |
| Inputs | Declared alternatives, selection basis or constraint, and the representation in which alternatives are identified. |
| Required declarations | Context, perspective, representation type, position where selection is position-dependent, scale, time where dynamic, identity where alternatives require continuity, evidence class and uncertainty status where the basis uses evidence. |
| Preconditions | Alternatives and basis are identifiable; applicable declarations are present and compatible; the owning profile is active under OLS-3. |
| Operation | Select one or more alternatives under the declared basis without assigning recommendation, authority, execution, or optimality. |
| Outputs | Selected alternative or alternatives with basis, constraint, applicable declarations, evidence, provenance, and uncertainty. |
| Preserved status | Alternative identity, representation, position, basis, constraint, evidence class, provenance, uncertainty, and unselected alternatives where relevant to the claim. |
| Failure conditions | Missing alternatives, basis, owner/profile reference, or applicable declaration: incomplete; incompatible basis or prohibited implication: malformed. |
| Prohibited implications | Recommendation, authority, execution, or optimality; a possible path or selected alternative is not thereby an authorized action. |
| Traceability | Phase 2D `05_OPERATOR_OWNERSHIP.md`; `03_PROFILE_ARCHITECTURE.md`, Navigation row. |

`[OLS2-REQ-0091]` SELECT shall report the alternatives and declared basis under which selection occurred.

`[OLS2-REQ-0092]` SELECT shall not convert possibility or selection into recommendation, authority, execution, or optimality.

### 8.2 TRANSFORM

*Stable clause ID: `OLS2-CLS-0025` — Operator ID: `OP-TRANSFORM` — Trace ID: `TRACE-000084` — Normative*

| Contract field | Specification |
| --- | --- |
| Purpose | Change a declared form or state into another declared form or state. |
| Semantic owner | Transformation Profile. |
| Inputs | Declared input form or state, transformation description, and constraint where applicable. |
| Required declarations | Context, perspective, representation type, identity, time, scale, evidence class and uncertainty status where claims about the change depend on them. The transformation description and constraint are operator inputs, not additional declarations. |
| Preconditions | Input is identifiable; source and resulting identity criteria are declared; applicable declarations are present and compatible; the owning profile is active under OLS-3. |
| Operation | Change the declared input form or state while preserving the input/output distinction. |
| Outputs | Declared resulting form or state linked to input, transformation description, declarations, provenance, evidence class, and uncertainty. |
| Preserved status | Input state/form, identity criterion, time order, scale, representation type, provenance, evidence class, uncertainty, and constraint as applicable. |
| Failure conditions | Missing input, transformation description, identity/time distinction, owner/profile reference, or applicable declaration: incomplete; input/output collapse, incompatible declarations, or prohibited implication: malformed. |
| Prohibited implications | Improvement, stability, validation, outcome admission, authorization, or execution success. |
| Traceability | Phase 2D `05_OPERATOR_OWNERSHIP.md`; `03_PROFILE_ARCHITECTURE.md`, Transformation row; `07_VALIDATION_AND_OUTCOME.md`. |

`[OLS2-REQ-0093]` TRANSFORM shall preserve distinct input and resulting form or state references.

`[OLS2-REQ-0094]` TRANSFORM shall not establish validation, admitted outcome, improvement, authorization, or execution success.

### 8.3 VALIDATE

*Stable clause ID: `OLS2-CLS-0026` — Operator ID: `OP-VALIDATE` — Trace ID: `TRACE-000085` — Normative*

| Contract field | Specification |
| --- | --- |
| Purpose | Test a declared claim, model, change, or candidate outcome against declared criteria and evidence and produce validation status. |
| Semantic owner | Evidence/Validation Profile. |
| Inputs | Declared claim, model, change, or candidate outcome; validation criteria; evidence with provenance and status. |
| Required declarations | Context, perspective, evidence class, uncertainty status; representation type when represented material is tested; time and identity for candidate outcomes; scale where criteria depend on level. Criteria are operator inputs, not an additional declaration. |
| Preconditions | Test subject, criteria, evidence, and statuses are identifiable; applicable declarations are present and compatible; the owning profile is active under OLS-3. |
| Operation | Test the subject against declared criteria and evidence and assign a validation status within the declared scope. |
| Outputs | Validation status linked to subject, criteria, evidence, provenance, uncertainty, and declarations. |
| Preserved status | Subject identity/status, evidence class, provenance, uncertainty, criteria, context, perspective, time, scale, and representation type as applicable. |
| Failure conditions | Missing subject, criteria, evidence/status, owner/profile reference, or applicable declaration: incomplete; incompatible criteria/declarations or prohibited implication: malformed. |
| Prohibited implications | Causality, universality, authority, canonical status, publication, or outcome admission without the separately governed admission conditions. |
| Traceability | Phase 2D `05_OPERATOR_OWNERSHIP.md`; `03_PROFILE_ARCHITECTURE.md`, Evidence/Validation row; `07_VALIDATION_AND_OUTCOME.md`. |

`[OLS2-REQ-0095]` VALIDATE shall report its subject, criteria, evidence, and validation status within one declared scope.

`[OLS2-REQ-0096]` VALIDATE shall not establish authority, publication, universal proof, or admitted outcome solely by producing validation status.

### 8.4 RECORD

*Stable clause ID: `OLS2-CLS-0027` — Operator ID: `OP-RECORD` — Trace ID: `TRACE-000086` — Normative*

| Contract field | Specification |
| --- | --- |
| Purpose | Store declared observations or admitted outcomes with time, identity, provenance, and status. |
| Semantic owner | Memory/Learning Profile. |
| Inputs | Declared observation or admitted outcome and its evidence, validation/admission, provenance, uncertainty, time, and identity status. |
| Required declarations | Identity, time, evidence class, uncertainty status, context where interpretation depends on it; representation type where represented material is stored. Outcome-admission status is an input status, not an additional declaration. |
| Preconditions | Material and status are identifiable; applicable declarations are present and compatible; an admitted outcome is identified as such only under its owning rules; the owning profile is active under OLS-3. |
| Operation | Store the declared material and status without upgrading its epistemic, validation, admission, canonical, experiential, or learning status. |
| Outputs | A record reference or recorded state preserving material, declarations, provenance, time, identity, evidence class, admission status, and uncertainty. |
| Preserved status | Observation or outcome status, validation/admission status, identity, time, provenance, evidence class, uncertainty, context, and representation type as applicable. |
| Failure conditions | Missing material, identity, time, provenance/status, owner/profile reference, or applicable declaration: incomplete; incompatible identity/time or silent status upgrade: malformed. |
| Prohibited implications | Validation, canonical status, experiential status, or learning merely from recording. |
| Traceability | Phase 2D `05_OPERATOR_OWNERSHIP.md`; `03_PROFILE_ARCHITECTURE.md`, Memory/Learning row; `07_VALIDATION_AND_OUTCOME.md`. |

`[OLS2-REQ-0097]` RECORD shall preserve the declared status of recorded material and shall not upgrade that status.

`[OLS2-REQ-0098]` RECORD shall not establish experiential learning solely by persistence.

### 8.5 APPROVE

*Stable clause ID: `OLS2-CLS-0028` — Operator ID: `OP-APPROVE` — Trace ID: `TRACE-000087` — Normative*

| Contract field | Specification |
| --- | --- |
| Purpose | Change a declared proposal or change to an approved governed status under declared authority scope. |
| Semantic owner | Editorial Governance Profile. |
| Inputs | Declared proposal or change, current governed status, approval basis, authority record, and target. |
| Required declarations | Authority scope; identity of the governed subject or Work; context; time where authority/status is time-bounded; evidence class and uncertainty status where approval basis uses claims. Proposal status, approval basis, and target are inputs, not additional declarations. |
| Preconditions | Proposal/change, current status, authority actor or role, operation, target, and scope are identifiable; applicable declarations are present and compatible; the owning profile is active under OLS-3. |
| Operation | Assign approved governed status within the declared authority scope. |
| Outputs | Approved governed status linked to proposal/change, authority, scope, target, basis, provenance, and declarations. |
| Preserved status | Proposal/change identity, prior status, authority actor or role, operation, target, scope, evidence class, provenance, uncertainty, context, and time as applicable. |
| Failure conditions | Missing proposal/change, authority scope, target, current status, owner/profile reference, or applicable declaration: incomplete; incompatible authority or out-of-scope approval: malformed. |
| Prohibited implications | Empirical truth, validation, universal proof, recommendation, external execution, or publication outside the declared governed status and scope. |
| Traceability | Phase 2D `05_OPERATOR_OWNERSHIP.md`; `03_PROFILE_ARCHITECTURE.md`, Editorial Governance row; `07_VALIDATION_AND_OUTCOME.md`. |

`[OLS2-REQ-0099]` APPROVE shall limit its output to the governed status and authority scope declared for the invocation.

`[OLS2-REQ-0100]` APPROVE shall not convert editorial or governed approval into empirical truth or validation.

## 9 Primitive operator ownership

*Stable clause ID: `OLS2-CLS-0029` — Trace ID: `TRACE-000088` — Normative*

Annex B is the authoritative Version 1.0 primitive operator ownership registry.

`[OLS2-REQ-0101]` Every primitive operator shall resolve to exactly one semantic owner.

`[OLS2-REQ-0102]` An owner shall control the operator’s semantic responsibility, contract, boundaries, and prohibited implications.

`[OLS2-REQ-0103]` A reference to an operator shall use its Operator ID and shall retain the owner’s contract.

`[OLS2-REQ-0104]` Referencing an operator shall not transfer ownership.

`[OLS2-REQ-0105]` A downstream profile, implementation, application, example, or extension shall not supply a second definition for a Version 1.0 primitive operator.

`[OLS2-REQ-0106]` A derived or specialized operator shall identify the primitive capability and owner from which it derives under the owning profile specification.

`[OLS2-REQ-0107]` An implementation function, visual operator, human role, or historical operator name shall not acquire primitive ownership.

`[OLS2-REQ-0108]` An ownership conflict shall make the affected invocation malformed.

## 10 Operator invocation

*Stable clause ID: `OLS2-CLS-0030` — Trace ID: `TRACE-000089` — Normative*

An invocation is a specification-level application of one operator contract. It does not prescribe software execution.

Every invocation identifies:

- Operator ID and semantic owner;
- input references and their status;
- applicable Declaration IDs, values/statuses, scopes, and sources;
- precondition status;
- operation claimed;
- output reference and status;
- preserved provenance, evidence class, uncertainty, disagreements, and limitations;
- incomplete or malformed status, if present;
- Trace ID linking the invocation form to its contract.

`[OLS2-REQ-0109]` An invocation shall identify exactly one primitive Operator ID.

`[OLS2-REQ-0110]` An invocation shall satisfy every applicable contract precondition before its output is treated as complete.

`[OLS2-REQ-0111]` An invocation shall include every declaration required by its contract and actual claims.

`[OLS2-REQ-0112]` An invocation shall preserve input status required by its contract.

`[OLS2-REQ-0113]` An invocation shall identify unsupported inputs or declarations and shall limit dependent output accordingly.

`[OLS2-REQ-0114]` An invocation shall not claim semantic effects outside its operator contract.

`[OLS2-REQ-0115]` A human procedure and a computational realization shall be evaluated against the same semantic invocation fields.

`[OLS2-REQ-0116]` Invocation order shall not create authority, validation, outcome, or learning absent the separately owned operator and conditions.

`[OLS2-REQ-0117]` A profile primitive invocation shall reference its active owner under OLS-3 without redefining that profile.

`[OLS2-REQ-0118]` Invocation syntax and serialization may vary by implementation, but their semantic mapping shall remain explicit.

`[OLS2-REQ-0119]` An invocation record need not prescribe scheduling, storage, transport, user interface, or runtime architecture.

## 11 Operator composition and sequencing

*Stable clause ID: `OLS2-CLS-0031` — Trace ID: `TRACE-000090` — Normative*

Operator composition connects the declared output of one invocation to a compatible input of another while retaining both contracts and all applicable declarations and statuses.

`[OLS2-REQ-0120]` Every composed invocation shall remain independently attributable to its Operator ID and owner.

`[OLS2-REQ-0121]` An output shall be used as a later input only when semantic type, status, declarations, context, perspective, identity, time, scale, and representation basis are compatible as applicable.

`[OLS2-REQ-0122]` Composition shall preserve provenance from each source invocation.

`[OLS2-REQ-0123]` Composition shall not erase an unsupported, incomplete, malformed, uncertain, or conflicting status.

`[OLS2-REQ-0124]` The universal operators shall follow the OLS-1 canonical order when a complete universal process is claimed.

`[OLS2-REQ-0125]` A profile primitive operator shall compose only under OLS-3 profile activation and dependency rules.

`[OLS2-REQ-0126]` Operator order shall not act as a precedence rule for incompatible declarations or ownership conflicts.

`[OLS2-REQ-0127]` Composition shall not be interpreted as external execution architecture, causality, validation, authority, outcome, or learning unless the applicable owned contracts and conditions establish that status.

`[OLS2-REQ-0128]` A composed sequence shall identify its semantic invocation order without prescribing implementation scheduling.

## 12 Failure model

*Stable clause ID: `OLS2-CLS-0032` — Trace ID: `TRACE-000091` — Normative*

OLS-2 distinguishes incomplete, malformed, and unsupported invocation states. OLS-5 owns test procedures and conformance reporting.

| State | Condition | Semantic consequence |
| --- | --- | --- |
| Incomplete invocation | A required input, applicable declaration, precondition, owner/profile reference, source status, or required preserved status is missing. | No complete operator output may be claimed. |
| Malformed invocation | Declarations or inputs are incompatible; ownership is violated; categories are conflated; a prohibited implication is asserted; or an unresolved conflict is silently overridden. | The claimed invocation is not a valid use of the identified contract. |
| Unsupported invocation | A declaration, input, basis, criterion, authority, or status is explicit but lacks support for a dependent claim. | The unsupported status and affected output remain explicit; unsupported material does not acquire supported status. |

`[OLS2-REQ-0129]` Missing required declarations shall make an invocation incomplete.

`[OLS2-REQ-0130]` Incompatible declarations shall make an invocation malformed.

`[OLS2-REQ-0131]` Unsupported declarations shall remain explicit and shall not be treated as satisfying supported preconditions.

`[OLS2-REQ-0132]` A missing operator owner or active owner-profile reference shall make a profile primitive invocation incomplete.

`[OLS2-REQ-0133]` A second or conflicting operator owner shall make an invocation malformed.

`[OLS2-REQ-0134]` Omission of provenance or source status required by a contract shall make an invocation incomplete even though provenance is not an Annex A declaration.

`[OLS2-REQ-0135]` Silent evidence-class promotion, uncertainty removal, authority expansion, or input/output collapse shall make an invocation malformed.

`[OLS2-REQ-0136]` Failure of one invocation shall remain visible to every dependent invocation.

`[OLS2-REQ-0137]` An incomplete invocation may be completed only with supported missing material under the owning contract.

`[OLS2-REQ-0138]` A malformed invocation shall not be repaired by inferred declarations, operator precedence, implementation behavior, or informative examples.

`[OLS2-REQ-0139]` OLS-2 failure states shall not be represented as OLS-5 conformance results until evaluated under OLS-5.

## 13 Normative summary

*Stable clause ID: `OLS2-CLS-0033` — Trace ID: `TRACE-000092` — Normative*

OLS-2 expresses the frozen Orientation Language through ten declarations and ten complete primitive operator contracts. Annex A controls the declaration inventory, Annex B controls operator identity and ownership, and Annex C controls contract structure.

`[OLS2-REQ-0140]` A Version 1.0 declaration or primitive operator invocation shall resolve to the applicable OLS-2 registry and owning clause.

`[OLS2-REQ-0141]` OLS-2 shall add operational precision without changing OLS-1 semantics or Phase 2D ownership.

`[OLS2-REQ-0142]` OLS-2 semantics shall remain independent of implementation technology and downstream profile, derivation, conformance, and governance specifications.

---

# Annex A — Declaration Registry

*Annex ID: `OLS2-ANN-A` — Trace ID: `TRACE-000093` — Normative*

## A.1 Registry authority

This annex is the Version 1.0 authoritative declaration registry. Detailed rules remain authoritative in the cited clauses.

## A.2 Declaration entries

| Declaration ID | Canonical declaration | Authoritative clause | Owner | Default |
| --- | --- | --- | --- | --- |
| `DECL-TIME` | time | `OLS2-CLS-0006` | OLS-2 | Prohibited |
| `DECL-IDENTITY` | identity | `OLS2-CLS-0007` | OLS-2 | Prohibited |
| `DECL-SCALE` | scale | `OLS2-CLS-0008` | OLS-2 | Prohibited |
| `DECL-CONTEXT` | context | `OLS2-CLS-0009` | OLS-2 | Prohibited |
| `DECL-PERSPECTIVE` | perspective | `OLS2-CLS-0010` | OLS-2 | Prohibited |
| `DECL-POSITION` | position | `OLS2-CLS-0011` | OLS-2 | Prohibited |
| `DECL-REPRESENTATION-TYPE` | representation type | `OLS2-CLS-0012` | OLS-2 | Prohibited |
| `DECL-EVIDENCE-CLASS` | evidence class | `OLS2-CLS-0013` | OLS-2 | Prohibited |
| `DECL-UNCERTAINTY-STATUS` | uncertainty status | `OLS2-CLS-0014` | OLS-2 | Prohibited |
| `DECL-AUTHORITY-SCOPE` | authority scope | `OLS2-CLS-0015` | OLS-2; applicability remains profile-bound where governed acts occur | Prohibited |

`[OLS2-REQ-0143]` Annex A shall contain exactly ten Version 1.0 declaration entries.

`[OLS2-REQ-0144]` A declaration shall not be added, removed, or assigned a new responsibility without the applicable Architecture Revision Process.

`[OLS2-REQ-0145]` A declaration reference shall use the registered Declaration ID.

---

# Annex B — Primitive Operator Ownership Registry

*Annex ID: `OLS2-ANN-B` — Trace ID: `TRACE-000094` — Normative*

## B.1 Registry authority

This annex is the Version 1.0 authoritative primitive operator identity and ownership registry.

## B.2 Operator entries

| Operator ID | Operator | Semantic owner | Authoritative contract |
| --- | --- | --- | --- |
| `OP-OBSERVE` | OBSERVE | Universal Base Language | `OLS2-CLS-0018` |
| `OP-REPRESENT` | REPRESENT | Universal Base Language | `OLS2-CLS-0019` |
| `OP-COMPARE` | COMPARE | Universal Base Language | `OLS2-CLS-0020` |
| `OP-ORIENT` | ORIENT | Universal Base Language | `OLS2-CLS-0021` |
| `OP-EXPLAIN` | EXPLAIN | Universal Base Language | `OLS2-CLS-0022` |
| `OP-SELECT` | SELECT | Navigation Profile | `OLS2-CLS-0024` |
| `OP-TRANSFORM` | TRANSFORM | Transformation Profile | `OLS2-CLS-0025` |
| `OP-VALIDATE` | VALIDATE | Evidence/Validation Profile | `OLS2-CLS-0026` |
| `OP-RECORD` | RECORD | Memory/Learning Profile | `OLS2-CLS-0027` |
| `OP-APPROVE` | APPROVE | Editorial Governance Profile | `OLS2-CLS-0028` |

`[OLS2-REQ-0146]` Annex B shall contain exactly ten Version 1.0 primitive operators with exactly one owner each.

`[OLS2-REQ-0147]` A registered Operator ID shall not be reassigned or given a second contract.

`[OLS2-REQ-0148]` Every primitive operator reference shall resolve to the contract and owner in Annex B.

---

# Annex C — Operator Contract Template

*Annex ID: `OLS2-ANN-C` — Trace ID: `TRACE-000095` — Normative*

## C.1 Template

| Contract field | Required content |
| --- | --- |
| Purpose | One statement of the frozen operator responsibility. |
| Semantic owner | Exactly one owner from the ownership registry. |
| Inputs | Accepted semantic material and status. |
| Required declarations | Applicable Annex A declarations; non-declaration inputs remain identified separately. |
| Preconditions | Conditions that precede a complete invocation. |
| Operation | Operational precision within the frozen responsibility. |
| Outputs | Semantic product and status without implementation typing. |
| Preserved status | Provenance, evidence class, uncertainty, declarations, disagreement, unsupported conclusions, limitations, and other applicable status. |
| Failure conditions | Incomplete, malformed, and unsupported conditions. |
| Prohibited implications | Boundaries that the invocation and its composition cannot cross. |
| Traceability | OLS-1 responsibility where universal, Phase 2D owner, Clause ID, Requirement IDs, and Trace ID. |

`[OLS2-REQ-0149]` Every primitive operator contract shall contain all eleven fields in Annex C.

`[OLS2-REQ-0150]` An empty or inapplicable field shall state why it is inapplicable and shall not be silently omitted.

---

# Annex D — Informative Invocation Examples

*Annex ID: `OLS2-ANN-D` — Informative*

## D.1 Universal sequence

An OBSERVE invocation admits two source readings with context, time, source, and uncertainty status. REPRESENT constructs one declared table representation. COMPARE identifies a difference under a declared basis. ORIENT reports what that difference supports under the declared evidence and uncertainty. EXPLAIN communicates the finding without recommendation or authority. Each output retains the declarations and provenance needed by the next invocation.

## D.2 Incomplete invocation

A COMPARE invocation names two items but no comparison basis. The intended operator is recognizable, but the invocation is incomplete and produces no complete comparison finding.

## D.3 Malformed invocation

A REPRESENT invocation labels a model output as observed reality. The invocation collapses representation into reality and silently promotes evidence class. It is malformed.

## D.4 Unsupported declaration

An authority-scope declaration names an approver but provides no supported authority record. The declaration remains explicit and unsupported; an APPROVE invocation depending on it cannot claim approved status.

## D.5 Profile operator boundary

SELECT identifies one alternative under a declared constraint. The output remains a selection. It does not become a recommendation or authorized execution.

---

# Annex E — Architectural Traceability

*Annex ID: `OLS2-ANN-E` — Informative*

## E.1 Traceability rule

This annex maps OLS-2 clauses to the frozen architecture and controlling OLS-1 clauses. It does not add normative semantics.

## E.2 Clause traceability

| Trace ID | OLS-2 subject | Authoritative source |
| --- | --- | --- |
| `TRACE-000060` | Scope | Phase 2D `09_CANONICAL_ARCHITECTURE.md`; Phase 3 Charter; OLS-0 Annex A |
| `TRACE-000061` | Normative references | Phase 2D canonical baseline; OLS-0; OLS-1 |
| `TRACE-000062` | Terms | Phase 2D `02_CONCEPTS_AND_DECLARATIONS.md`; OLS-0 terminology policy; OLS-1 concept/declaration distinction |
| `TRACE-000063` | Declaration model | Phase 2D `02_CONCEPTS_AND_DECLARATIONS.md`, architectural and omission rules; `04_PROFILE_COMPOSITION.md`, conflicts |
| `TRACE-000064` | Frozen declarations | Phase 2D `02_CONCEPTS_AND_DECLARATIONS.md`, declaration inventory |
| `TRACE-000065` | time | Phase 2D declaration inventory, time row |
| `TRACE-000066` | identity | Phase 2D declaration inventory, identity row |
| `TRACE-000067` | scale | Phase 2D declaration inventory, scale row |
| `TRACE-000068` | context | Phase 2D declaration inventory, context row; OLS-1 `TERM-CONTEXT` |
| `TRACE-000069` | perspective | Phase 2D declaration inventory, perspective row; OLS-1 `TERM-PERSPECTIVE` |
| `TRACE-000070` | position | Phase 2D declaration inventory, position row; OLS-1 `TERM-POSITION` |
| `TRACE-000071` | representation type | Phase 2D declaration inventory, representation type row; OLS-1 representation boundary |
| `TRACE-000072` | evidence class | Phase 2D declaration inventory, evidence class row; OLS-1 `TERM-EVIDENCE` |
| `TRACE-000073` | uncertainty status | Phase 2D declaration inventory, uncertainty status row; OLS-1 `TERM-UNCERTAINTY` |
| `TRACE-000074` | authority scope | Phase 2D declaration inventory, authority scope row; `03_PROFILE_ARCHITECTURE.md`, Editorial Governance owner |
| `TRACE-000075` | Contract model | Phase 3A OLS-2 allocation; Phase 2D operator ownership; OLS-1 operator responsibility boundary |
| `TRACE-000076` | Universal contracts | Phase 2D `01_UNIVERSAL_BASE_LANGUAGE.md`; `05_OPERATOR_OWNERSHIP.md`; OLS-1 Clause 8 |
| `TRACE-000077` | OBSERVE | Phase 2D universal operator responsibility and boundary; OLS-1 `OLS1-CLS-0023` |
| `TRACE-000078` | REPRESENT | Phase 2D universal operator responsibility and boundary; OLS-1 `OLS1-CLS-0024` |
| `TRACE-000079` | COMPARE | Phase 2D universal operator responsibility and boundary; ADR-0001 Decision 2; OLS-1 `OLS1-CLS-0025` |
| `TRACE-000080` | ORIENT | Phase 2D universal operator responsibility and boundary; OLS-1 `OLS1-CLS-0026` |
| `TRACE-000081` | EXPLAIN | Phase 2D universal operator responsibility and boundary; OLS-1 `OLS1-CLS-0027` |
| `TRACE-000082` | Profile primitive contracts | Phase 2D `03_PROFILE_ARCHITECTURE.md`; `05_OPERATOR_OWNERSHIP.md` |
| `TRACE-000083` | SELECT | Phase 2D Navigation row and ownership table |
| `TRACE-000084` | TRANSFORM | Phase 2D Transformation row, ownership table, validation/outcome order |
| `TRACE-000085` | VALIDATE | Phase 2D Evidence/Validation row, ownership table, validation/outcome order |
| `TRACE-000086` | RECORD | Phase 2D Memory/Learning row, ownership table, validation/outcome order |
| `TRACE-000087` | APPROVE | Phase 2D Editorial Governance row, ownership table, validation/outcome boundary |
| `TRACE-000088` | Ownership | Phase 2D `05_OPERATOR_OWNERSHIP.md`; `04_PROFILE_COMPOSITION.md` |
| `TRACE-000089` | Invocation | Phase 2D operator ownership and declaration rules; Phase 3 Charter authorization for syntax |
| `TRACE-000090` | Composition | Phase 2D `04_PROFILE_COMPOSITION.md`; OLS-1 canonical process |
| `TRACE-000091` | Failure model | Phase 2D declaration omission rule and profile conflict detection; OLS-1 universal errors |
| `TRACE-000092` | Summary | Phase 2D canonical architecture; OLS-1 |
| `TRACE-000093` | Declaration Registry | Phase 2D declaration inventory and classification |
| `TRACE-000094` | Ownership Registry | Phase 2D primitive operator ownership table |
| `TRACE-000095` | Contract Template | Phase 3A OLS-2 structure; Phase 3 Charter; Phase 2D ownership boundaries |

## E.3 Requirement coverage

Requirement IDs `OLS2-REQ-0001` through `OLS2-REQ-0150` are governed by the Trace ID of their containing normative clause or annex. Requirement-to-test mappings belong to OLS-5.

---

## End of OLS-2
