# Orientation Language Specification — OLS-3

## Semantic Profiles and Composition

| Metadata field | Value |
| --- | --- |
| Document ID | `OLS-3` |
| Edition | 1 |
| Suite version | `1.0.0` |
| Document revision | `1.0.0` |
| Status | Version 1.0 publication candidate |
| Publication date | 17 July 2026 |
| Language | English |
| Normative scope | Seven semantic profiles, activation, dependency resolution, composition, conflicts, reporting, and primitive concept ownership |
| Semantic scope | Representation; Navigation; Transformation; Evidence/Validation; Memory/Learning; Editorial Governance; Education |
| Replaces | Phase 2D profile architecture and composition summaries upon suite publication |
| Normative dependencies | `OLS-0`, `OLS-1`, `OLS-2` |
| Forward references | `OLS-4` for derivations and cross-profile validation/outcome order; `OLS-5` for conformance procedures |
| Release manifest identifier | Pending assignment at suite publication |
| Persistent citation identifier | Unassigned |
| Architecture baseline | Phase 2D Canonical Architecture, frozen by ADR-0001 |

## Status of this document

OLS-3 is the authoritative Version 1.0 specification of semantic profiles and their composition. Except for Annexes D, E, and F, all clauses and annexes in this document are **Normative**.

OLS-3 extends the Universal Base Language only through the seven frozen profiles. It references OLS-2 declarations and primitive operator contracts without redefining them.

---

## 1 Scope

*Stable clause ID: `OLS3-CLS-0001` — Trace ID: `TRACE-000096` — Normative*

OLS-3 specifies:

- a common semantic profile model;
- exactly seven semantic profiles;
- profile inheritance and activation;
- mandatory and conditional dependencies;
- legal profile composition and conflict detection;
- active-profile reporting;
- unique ownership of four profile primitive concepts;
- profile boundaries and prohibited modifications.

`[OLS3-REQ-0001]` OLS-3 shall contain exactly the seven profiles registered in Annex A.

`[OLS3-REQ-0002]` OLS-3 shall preserve OLS-1 universal semantics and OLS-2 declarations, primitive operator contracts, and ownership.

`[OLS3-REQ-0003]` OLS-3 shall not define derivations, conformance procedures, governance changes, or implementation architecture.

`[OLS3-REQ-0004]` A need for a new profile or changed profile responsibility shall be referred to an Architecture Revision Process.

## 2 Normative references

*Stable clause ID: `OLS3-CLS-0002` — Trace ID: `TRACE-000097` — Normative*

The following documents are normatively indispensable to OLS-3:

- `OLS-0`, *Specification Conventions and Suite Overview*, Edition 1, suite version `1.0.0`;
- `OLS-1`, *Universal Base Language*, Edition 1, suite version `1.0.0`;
- `OLS-2`, *Declarations and Operator Contracts*, Edition 1, suite version `1.0.0`.

`[OLS3-REQ-0005]` OLS-3 shall apply OLS-0 conventions, inherit OLS-1 without modification, and reference OLS-2 declarations and operator contracts by stable identifier.

## 3 Terms and definitions

*Stable clause ID: `OLS3-CLS-0003` — Trace ID: `TRACE-000098` — Normative*

For OLS-3:

- **semantic profile** means an explicitly active extension of the mandatory Universal Base Language with one frozen purpose, owned semantics, dependencies, declarations, references, and prohibited modifications;
- **active profile** means a profile activated under Clause 5;
- **dependency** means a profile that is active before or together with a dependent profile under the condition specified by OLS-3;
- **mandatory dependency** means a dependency present whenever the dependent profile is active;
- **conditional dependency** means a dependency present only when the stated profile capability, primitive, operator, or status is invoked;
- **profile composition** means one Universal Base Language combined with one or more active profiles under Clause 7;
- **profile conflict** means an unresolved incompatibility described by Clause 8;
- **profile primitive concept** means one of the four profile-owned concepts registered in Annex C.

`[OLS3-REQ-0006]` Profile terminology shall not add a universal concept or alter an OLS-1 definition.

`[OLS3-REQ-0007]` Profile operator names shall resolve to OLS-2 contracts and shall not be redefined in OLS-3.

`[OLS3-REQ-0008]` Declaration names shall resolve to OLS-2 and shall not acquire new value domains, defaults, or omission rules in OLS-3.

`[OLS3-REQ-0009]` A conditional dependency shall become active only under its stated condition and shall otherwise remain inactive.

## 4 Common profile model

*Stable clause ID: `OLS3-CLS-0004` — Trace ID: `TRACE-000099` — Normative*

Every Version 1.0 semantic profile has:

- a stable Profile ID, canonical name, and normative status;
- one purpose and architectural role;
- mandatory inheritance from OLS-1;
- zero or more uniquely owned primitive concepts;
- zero or more references to primitive concepts owned by another active profile;
- zero or more uniquely owned primitive operators whose contracts remain in OLS-2;
- references to operators owned elsewhere where frozen by the architecture;
- applicable declarations referenced from OLS-2;
- mandatory and conditional dependencies;
- permitted composition and conflict conditions;
- prohibited semantic modifications;
- active-profile reporting obligations.

`[OLS3-REQ-0010]` Every profile shall inherit the complete Universal Base Language.

`[OLS3-REQ-0011]` A profile shall add only semantics assigned to it by its authoritative profile clause.

`[OLS3-REQ-0012]` A profile shall not replace, weaken, or redefine inherited semantics.

`[OLS3-REQ-0013]` A profile shall have one Profile ID and one purpose.

`[OLS3-REQ-0014]` A primitive concept or primitive operator shall have exactly one semantic owner.

`[OLS3-REQ-0015]` Referencing owned semantics shall not transfer ownership.

`[OLS3-REQ-0016]` A profile shall identify every applicable OLS-2 declaration without reproducing its definition.

`[OLS3-REQ-0017]` A profile shall identify mandatory dependencies and the conditions of every conditional dependency.

`[OLS3-REQ-0018]` Profile composition shall add semantics and shall not silently remove inherited or concurrently active semantics.

`[OLS3-REQ-0019]` Profile status shall not be inferred from similar words, metaphors, visual forms, implementation technologies, or historical usage.

`[OLS3-REQ-0020]` A profile shall identify its active state and unresolved conflicts in every profile-based orientation artifact.

`[OLS3-REQ-0021]` A profile shall not claim empirical validation, authorization, successful execution, or implementation compatibility merely because it is active.

`[OLS3-REQ-0022]` A profile shall remain implementation independent.

## 5 Profile activation

*Stable clause ID: `OLS3-CLS-0005` — Trace ID: `TRACE-000100` — Normative*

A profile becomes active when:

1. the construction explicitly declares that Profile ID; or
2. the construction invokes a primitive concept or primitive operator owned by that profile.

The Universal Base Language is inherited implicitly and is not activated as a profile.

`[OLS3-REQ-0023]` Every active profile shall inherit OLS-1 before its own semantics are applied.

`[OLS3-REQ-0024]` Invoking an owned primitive concept or operator shall activate its owner profile.

`[OLS3-REQ-0025]` Activating a profile shall activate every mandatory dependency in Annex B.

`[OLS3-REQ-0026]` A conditional dependency shall activate when its stated condition becomes true.

`[OLS3-REQ-0027]` A profile with no owned primitive concept or primitive operator shall be activated explicitly by Profile ID.

`[OLS3-REQ-0028]` An inactive profile shall contribute no profile-specific semantics to the construction.

`[OLS3-REQ-0029]` Reference to an operator owned by another profile shall activate that operator’s owner and its mandatory dependencies.

`[OLS3-REQ-0030]` Reference to a profile primitive concept shall activate that concept’s owner and its mandatory dependencies.

`[OLS3-REQ-0031]` Activation shall not modify any universal or previously owned semantic responsibility.

`[OLS3-REQ-0032]` A construction shall report explicit activation separately from dependency activation.

`[OLS3-REQ-0033]` A profile shall not be inferred solely because an implementation supports its Operator ID.

`[OLS3-REQ-0034]` An unresolved activation condition shall make the affected profile composition incomplete.

## 6 Dependency resolution

*Stable clause ID: `OLS3-CLS-0006` — Trace ID: `TRACE-000101` — Normative*

Dependencies are resolved in this semantic order:

1. Universal Base Language;
2. Representation where it is mandatory or conditionally required;
3. Navigation, Transformation, and Evidence/Validation according to the active operation;
4. Memory/Learning after Evidence/Validation when experiential learning or outcome admission is involved;
5. Editorial Governance after persistence and any required validation;
6. Education after Navigation and, where recorded learning is claimed, Memory/Learning.

This order does not prescribe implementation scheduling.

`[OLS3-REQ-0035]` Every dependency shall resolve before the dependent profile operation is treated as complete.

`[OLS3-REQ-0036]` Mandatory dependencies shall be active whenever their dependent profile is active.

`[OLS3-REQ-0037]` Conditional dependencies shall identify their activation condition in the profile report.

`[OLS3-REQ-0038]` A profile at the same dependency level may compose with another only when declarations, ownership, representations, and operator contracts are compatible.

`[OLS3-REQ-0039]` An absent mandatory dependency shall make the composition incomplete.

`[OLS3-REQ-0040]` An absent conditional dependency after its condition is met shall make the affected composition incomplete.

`[OLS3-REQ-0041]` A dependency shall not redefine its dependent profile, and a dependent profile shall not redefine its dependency.

`[OLS3-REQ-0042]` Dependency activation shall not transfer primitive concept or operator ownership.

`[OLS3-REQ-0043]` A dependency cycle shall make the composition malformed.

`[OLS3-REQ-0044]` No dependency precedence shall override incompatible declarations or semantic ownership.

`[OLS3-REQ-0045]` Conditional dependencies not triggered by the active construction shall remain inactive and need not be reported as active.

`[OLS3-REQ-0046]` Every activated dependency shall appear in the active-profile report.

`[OLS3-REQ-0047]` Annex B shall control Version 1.0 dependency classification.

## 7 Legal composition

*Stable clause ID: `OLS3-CLS-0007` — Trace ID: `TRACE-000102` — Normative*

A profile composition is legal only when:

1. the complete Universal Base Language is inherited;
2. every active profile and activated dependency is identified;
3. every primitive concept and primitive operator resolves to exactly one owner;
4. every OLS-2 declaration applicable to the claims is present;
5. declaration values and scopes are mutually compatible;
6. representation types and comparison bases are compatible;
7. no profile modifies an inherited prohibited implication;
8. historical or cultural metaphor is not treated as a mechanical profile operation;
9. implementation behavior is not used as semantic authority.

`[OLS3-REQ-0048]` Every legal composition shall satisfy all nine conditions in Clause 7.

`[OLS3-REQ-0049]` Profiles shall compose additively through inherited and owned semantics, not by override.

`[OLS3-REQ-0050]` Every referenced primitive operator shall retain its OLS-2 contract and owner.

`[OLS3-REQ-0051]` Every referenced profile primitive concept shall retain its Annex C definition and owner.

`[OLS3-REQ-0052]` Applicable OLS-2 declarations shall retain their values, scopes, source, and unsupported status through composition.

`[OLS3-REQ-0053]` Composition shall preserve OLS-1 evidence class, provenance, uncertainty, disagreement, unsupported conclusions, and limitations.

`[OLS3-REQ-0054]` Representation compatibility shall be explicit and shall not be inferred from visual or implementation similarity.

`[OLS3-REQ-0055]` A composition shall identify every conditional dependency whose activation condition is met.

`[OLS3-REQ-0056]` A profile may reference another profile’s operator or primitive concept only through the authoritative owner.

`[OLS3-REQ-0057]` Composition shall not imply implementation compatibility, empirical validation, authorization, or successful execution.

`[OLS3-REQ-0058]` A legal composition need not activate profiles not required by its claims, owned semantics, or dependencies.

`[OLS3-REQ-0059]` No profile shall acquire universal status through frequent composition.

`[OLS3-REQ-0060]` OLS-3 composition shall not add an operator to the OLS-1 canonical universal process.

## 8 Conflict detection

*Stable clause ID: `OLS3-CLS-0008` — Trace ID: `TRACE-000103` — Normative*

A profile conflict exists when one or more legal-composition conditions fail and the failure cannot be represented merely as an explicit supported difference, disagreement, or uncertainty.

| Conflict category | Condition |
| --- | --- |
| Ownership conflict | A primitive concept or operator has no owner, more than one owner, or a second definition. |
| Declaration conflict | OLS-2 declarations assign incompatible values or scopes to the same operation or claim. |
| Dependency conflict | A mandatory or triggered conditional dependency is absent, circular, or incompatible. |
| Profile conflict | A profile grammar or responsibility contradicts another active profile or inherited semantics. |
| Prohibited modification | A profile changes a universal definition, operator contract, declaration responsibility, ownership, boundary, or process. |
| Representation conflict | Representation types, identity criteria, time, scale, perspective, or comparison bases are incompatible. |
| Non-semantic authority conflict | Historical, cultural, informative, or implementation material is used to claim semantic conformance. |

`[OLS3-REQ-0061]` An unresolved conflict shall make the profile composition malformed.

`[OLS3-REQ-0062]` No profile, document order, operator order, declaration order, or implementation behavior shall override a conflict.

`[OLS3-REQ-0063]` Ownership conflict shall be evaluated against OLS-2 Annex B and OLS-3 Annex C.

`[OLS3-REQ-0064]` Declaration conflict shall be evaluated against OLS-2 without redefining declaration semantics.

`[OLS3-REQ-0065]` Dependency conflict shall identify the missing, circular, or incompatible dependency.

`[OLS3-REQ-0066]` Prohibited modification shall identify the inherited or owned semantic element affected.

`[OLS3-REQ-0067]` Representation conflict shall identify the incompatible declarations, types, or bases.

`[OLS3-REQ-0068]` A conflict shall remain visible in the active-profile report.

`[OLS3-REQ-0069]` Explicit disagreement or uncertainty shall not be classified as conflict when all active semantics and declarations remain compatible.

`[OLS3-REQ-0070]` Rewording an owned semantic element shall not resolve a substantive ownership conflict.

`[OLS3-REQ-0071]` An incomplete dependency state shall become malformed if the construction claims completion despite the unresolved dependency.

`[OLS3-REQ-0072]` Conflict repair shall use the controlling owner or declaration and shall not invent missing semantics.

## 9 Active-profile reporting

*Stable clause ID: `OLS3-CLS-0009` — Trace ID: `TRACE-000104` — Normative*

Every profile-based orientation artifact reports:

- the Universal Base Language;
- each explicitly active profile;
- each dependency-activated profile;
- the activation basis for each profile;
- mandatory and triggered conditional dependencies;
- each owned primitive concept used;
- each owned or referenced primitive operator and its owner;
- applicable OLS-2 declarations and their references;
- unresolved dependencies, conflicts, unsupported statuses, and missing information.

`[OLS3-REQ-0073]` A profile report shall identify the suite version and every active Profile ID.

`[OLS3-REQ-0074]` The Universal Base Language shall be reported as inherited and shall not be reported as a profile.

`[OLS3-REQ-0075]` Explicit activation and dependency activation shall remain distinguishable.

`[OLS3-REQ-0076]` Referenced operators shall identify their OLS-2 Operator IDs and owners.

`[OLS3-REQ-0077]` Owned primitive concepts shall identify their Annex C Term IDs and owners.

`[OLS3-REQ-0078]` Declaration references shall use OLS-2 Declaration IDs without duplicating declaration values outside their declared scope.

`[OLS3-REQ-0079]` Unresolved conflicts and missing dependencies shall not be omitted from a report that claims the affected composition.

`[OLS3-REQ-0080]` If no extension profile is active, the artifact shall report only the Universal Base Language and applicable OLS-2 declarations.

`[OLS3-REQ-0081]` Reporting shall not itself activate a profile or change semantic status.

## 10 Version 1.0 semantic profiles

*Stable clause ID: `OLS3-CLS-0010` — Trace ID: `TRACE-000105` — Normative*

The Version 1.0 semantic profiles are Representation, Navigation, Transformation, Evidence/Validation, Memory/Learning, Editorial Governance, and Education.

`[OLS3-REQ-0082]` Every profile shall use the Profile ID and canonical name in Annex A.

`[OLS3-REQ-0083]` Each profile shall retain the fields and boundaries in its owning subsection.

`[OLS3-REQ-0084]` No other component shall claim Version 1.0 semantic profile status.

### 10.1 Representation

*Stable clause ID: `OLS3-CLS-0011` — Profile ID: `PROFILE-REPRESENTATION` — Trace ID: `TRACE-000106` — Normative*

| Profile field | Specification |
| --- | --- |
| Identity | Representation; Normative Profile; `PROFILE-REPRESENTATION`. |
| Purpose | Type and construct structured forms while preserving the representation/reality boundary. |
| Architectural role | Supplies profile-specific representation typing and construction without changing universal representation or REPRESENT. |
| Inherited universal semantics | Complete OLS-1; primarily references `OP-REPRESENT`. |
| Owned primitive concepts | None. |
| Referenced primitive concepts | None. |
| Owned primitive operators | None. |
| Referenced primitive operators | `OP-REPRESENT`; other primitive operators only when independently invoked under their owners. |
| Required declarations | `DECL-REPRESENTATION-TYPE`, `DECL-PERSPECTIVE`, `DECL-CONTEXT`, and `DECL-SCALE` where applicable; provenance remains preserved OLS-1 status. |
| Mandatory dependencies | Universal Base Language only; no semantic profile dependency. |
| Conditional dependencies | Owner profile of any additionally referenced profile primitive. |
| Permitted composition | Any profile whose representations, declarations, ownership, and contracts remain compatible. |
| Conflict conditions | Missing or incompatible representation type, construction perspective, context, scale, or provenance; representation/reality collapse. |
| Prohibited modifications | Shall not present a representation as reality, proof, mechanism, or validation; shall not redefine representation or `OP-REPRESENT`. |

`[OLS3-REQ-0085]` Representation shall be activated explicitly because it owns no primitive concept or primitive operator.

`[OLS3-REQ-0086]` Representation shall preserve the OLS-1 representation/reality boundary.

`[OLS3-REQ-0087]` Representation shall not acquire ownership of `OP-REPRESENT` or another universal operator.

`[OLS3-REQ-0088]` Representation shall not infer compatibility from visual form or implementation type.

`[OLS3-REQ-0089]` Representation composition shall retain all source representation types, perspectives, provenance, and applicable scales.

### 10.2 Navigation

*Stable clause ID: `OLS3-CLS-0012` — Profile ID: `PROFILE-NAVIGATION` — Trace ID: `TRACE-000107` — Normative*

| Profile field | Specification |
| --- | --- |
| Identity | Navigation; Normative Profile; `PROFILE-NAVIGATION`. |
| Purpose | Locate positions and construct or select paths or routes under constraints. |
| Architectural role | Adds constrained position, path, route, and selection semantics to declared representations. |
| Inherited universal semantics | Complete OLS-1. |
| Owned primitive concepts | `TERM-CONSTRAINT`. |
| Referenced primitive concepts | None. |
| Owned primitive operators | `OP-SELECT`; complete contract remains OLS-2 `OLS2-CLS-0024`. |
| Referenced primitive operators | `OP-TRANSFORM` only when navigation changes a represented state; `OP-RECORD` only when a path or route is persisted. |
| Required declarations | `DECL-POSITION`, `DECL-REPRESENTATION-TYPE`, `DECL-SCALE`, and `DECL-TIME` where dynamic; applicable inherited context, perspective, identity, evidence class, and uncertainty status. Target or question and constraint or selection basis remain profile inputs, not declarations. |
| Mandatory dependencies | Representation. |
| Conditional dependencies | Transformation when `OP-TRANSFORM` is invoked; Memory/Learning when `OP-RECORD` is invoked. |
| Permitted composition | Representation plus Transformation or Memory/Learning under the stated conditions, and other compatible profiles under Clause 7. |
| Conflict conditions | Missing representation or position where required; incompatible constraints, selection basis, scale, time, representation, or owner reference. |
| Prohibited modifications | Shall not convert possibility, path, route, or selection into recommendation, authority, execution, or optimality. |

`[OLS3-REQ-0090]` Navigation shall own `TERM-CONSTRAINT` and `OP-SELECT` exclusively.

`[OLS3-REQ-0091]` Navigation shall activate Representation as a mandatory dependency.

`[OLS3-REQ-0092]` Referencing `OP-TRANSFORM` or `OP-RECORD` shall activate the owning profile under its stated condition.

`[OLS3-REQ-0093]` Navigation shall preserve the difference between a possible, selected, recommended, authorized, and executed path.

`[OLS3-REQ-0094]` Navigation shall not claim optimality solely from selection.

### 10.3 Transformation

*Stable clause ID: `OLS3-CLS-0013` — Profile ID: `PROFILE-TRANSFORMATION` — Trace ID: `TRACE-000108` — Normative*

| Profile field | Specification |
| --- | --- |
| Identity | Transformation; Normative Profile; `PROFILE-TRANSFORMATION`. |
| Purpose | Change a declared form or state while preserving input and output distinctions. |
| Architectural role | Adds declared change capability without assigning improvement, validation, admission, authority, or success. |
| Inherited universal semantics | Complete OLS-1. |
| Owned primitive concepts | None. |
| Referenced primitive concepts | `TERM-CONSTRAINT` when change is bounded by a Navigation-owned constraint. |
| Owned primitive operators | `OP-TRANSFORM`; complete contract remains OLS-2 `OLS2-CLS-0025`. |
| Referenced primitive operators | `OP-VALIDATE` where transformed results are tested. |
| Required declarations | `DECL-IDENTITY`, `DECL-TIME`, `DECL-SCALE`, `DECL-REPRESENTATION-TYPE`, and applicable context, perspective, evidence class, and uncertainty status. Input/output form or state and transformation description remain operator inputs. |
| Mandatory dependencies | Representation. |
| Conditional dependencies | Navigation when `TERM-CONSTRAINT` is referenced; Evidence/Validation when `OP-VALIDATE` is invoked. |
| Permitted composition | Representation; Navigation for bounded change; Evidence/Validation for tested change; other compatible profiles under Clause 7. |
| Conflict conditions | Collapsed input/output identity, incompatible time or scale, missing transformation input, incompatible constraint, or missing operator owner. |
| Prohibited modifications | Shall not imply improvement, stability, validation, outcome admission, authorization, or execution success. |

`[OLS3-REQ-0095]` Transformation shall own `OP-TRANSFORM` exclusively and shall own no profile primitive concept.

`[OLS3-REQ-0096]` Transformation shall activate Representation as a mandatory dependency.

`[OLS3-REQ-0097]` Referencing `TERM-CONSTRAINT` or `OP-VALIDATE` shall activate its owner profile.

`[OLS3-REQ-0098]` Transformation shall preserve distinct input and resulting form or state references.

`[OLS3-REQ-0099]` Transformation shall not establish an admitted outcome, validation, improvement, authorization, or execution success.

### 10.4 Evidence/Validation

*Stable clause ID: `OLS3-CLS-0014` — Profile ID: `PROFILE-EVIDENCE-VALIDATION` — Trace ID: `TRACE-000109` — Normative*

| Profile field | Specification |
| --- | --- |
| Identity | Evidence/Validation; Normative Profile; `PROFILE-EVIDENCE-VALIDATION`. |
| Purpose | Test a claim, model, transformation result, or candidate outcome against declared criteria and evidence. |
| Architectural role | Adds validation and governed outcome status without assigning authority, universality, or publication. |
| Inherited universal semantics | Complete OLS-1. |
| Owned primitive concepts | `TERM-OUTCOME`. |
| Referenced primitive concepts | `TERM-CONSTRAINT` where a Navigation-owned constraint forms part of the tested conditions. |
| Owned primitive operators | `OP-VALIDATE`; complete contract remains OLS-2 `OLS2-CLS-0026`. |
| Referenced primitive operators | `OP-TRANSFORM` for changed-state candidates; `OP-RECORD` after outcome admission. |
| Required declarations | `DECL-EVIDENCE-CLASS`, `DECL-UNCERTAINTY-STATUS`, and `DECL-TIME` plus `DECL-IDENTITY` for candidate outcomes; `DECL-REPRESENTATION-TYPE`, context, perspective, and scale where applicable. Criteria remain operator inputs. |
| Mandatory dependencies | Universal Base Language only. |
| Conditional dependencies | Representation when represented material is tested; Navigation when `TERM-CONSTRAINT` is referenced; Transformation when `OP-TRANSFORM` is invoked; Memory/Learning when `OP-RECORD` is invoked. |
| Permitted composition | Representation for represented subjects; Navigation for declared constraints; Transformation for changed candidates; Memory/Learning after admission; other compatible profiles under Clause 7. |
| Conflict conditions | Missing criteria or evidence status, incompatible candidate identity/time, incompatible representation, or conflated candidate, validation, and admission status. |
| Prohibited modifications | Shall not imply causality, universality, authority, canonical status, or publication. |

`[OLS3-REQ-0100]` Evidence/Validation shall own `TERM-OUTCOME` and `OP-VALIDATE` exclusively.

`[OLS3-REQ-0101]` Representation shall activate when represented material is validated.

`[OLS3-REQ-0102]` Referencing `TERM-CONSTRAINT`, `OP-TRANSFORM`, or `OP-RECORD` shall activate the owning profile.

`[OLS3-REQ-0103]` Evidence/Validation shall preserve candidate, validation, and admission statuses as distinct.

`[OLS3-REQ-0104]` Evidence/Validation shall not convert validation into authority, canonical status, universality, or publication.

### 10.5 Memory/Learning

*Stable clause ID: `OLS3-CLS-0015` — Profile ID: `PROFILE-MEMORY-LEARNING` — Trace ID: `TRACE-000110` — Normative*

| Profile field | Specification |
| --- | --- |
| Identity | Memory/Learning; Normative Profile; `PROFILE-MEMORY-LEARNING`. |
| Purpose | Persist observations or admitted outcomes and support learning only from admitted experience. |
| Architectural role | Adds retained semantic memory and recording while preserving observation, validation, admission, and learning distinctions. |
| Inherited universal semantics | Complete OLS-1. |
| Owned primitive concepts | `TERM-MEMORY`. |
| Referenced primitive concepts | `TERM-OUTCOME` when admitted outcomes or experiential learning are claimed. |
| Owned primitive operators | `OP-RECORD`; complete contract remains OLS-2 `OLS2-CLS-0027`. |
| Referenced primitive operators | `OP-VALIDATE` when experiential learning or outcome admission is involved. |
| Required declarations | `DECL-IDENTITY`, `DECL-TIME`, `DECL-EVIDENCE-CLASS`, `DECL-UNCERTAINTY-STATUS`, and applicable context and representation type; provenance and outcome-admission status remain preserved semantic statuses. |
| Mandatory dependencies | Universal Base Language only for recording observations. |
| Conditional dependencies | Evidence/Validation for experiential learning or admitted outcomes. |
| Permitted composition | Evidence/Validation for admitted experience; Editorial Governance when records support governed work; Education when recorded learning is claimed; other compatible profiles under Clause 7. |
| Conflict conditions | Missing identity/time/provenance/status, treating an unadmitted result as admitted experience, or treating recording as learning. |
| Prohibited modifications | Shall not treat every record as validated, canonical, experiential, or learned. |

`[OLS3-REQ-0105]` Memory/Learning shall own `TERM-MEMORY` and `OP-RECORD` exclusively.

`[OLS3-REQ-0106]` Evidence/Validation shall activate when experiential learning or an admitted outcome is claimed.

`[OLS3-REQ-0107]` Recording an observation without validation shall preserve its evidence and admission status.

`[OLS3-REQ-0108]` Memory/Learning shall preserve identity, time, provenance, evidence class, uncertainty, and admission status.

`[OLS3-REQ-0109]` Memory/Learning shall not treat persistence alone as validation, admission, or learning.

### 10.6 Editorial Governance

*Stable clause ID: `OLS3-CLS-0016` — Profile ID: `PROFILE-EDITORIAL-GOVERNANCE` — Trace ID: `TRACE-000111` — Normative*

| Profile field | Specification |
| --- | --- |
| Identity | Editorial Governance; Normative Profile; `PROFILE-EDITORIAL-GOVERNANCE`. |
| Purpose | Govern stable editorial identity, proposal, review, approval, publication, and human authority. |
| Architectural role | Adds governed status and authority without converting editorial decisions into empirical truth. |
| Inherited universal semantics | Complete OLS-1. |
| Owned primitive concepts | `TERM-AUTHORITY`. |
| Referenced primitive concepts | `TERM-MEMORY` when persisted records are used; `TERM-OUTCOME` where outcomes support claims. |
| Owned primitive operators | `OP-APPROVE`; complete contract remains OLS-2 `OLS2-CLS-0028`. |
| Referenced primitive operators | `OP-RECORD`; `OP-VALIDATE` where claims or results require verification. |
| Required declarations | `DECL-AUTHORITY-SCOPE`, `DECL-IDENTITY`, and applicable context, time, evidence class, and uncertainty status. Proposal or canonical status, publication target, and provenance remain inputs or preserved statuses rather than new declarations. |
| Mandatory dependencies | Universal Base Language only. |
| Conditional dependencies | Memory/Learning when `OP-RECORD` or persistence is used; Evidence/Validation where claims or results require verification. |
| Permitted composition | Memory/Learning for persistence; Evidence/Validation for required verification; other compatible profiles under Clause 7. |
| Conflict conditions | Missing or incompatible authority scope, identity, status, or target; software or evidence replacing human authority; approval conflated with truth. |
| Prohibited modifications | Shall not convert proposal, approval, or publication into empirical truth and shall not replace human authority with software. |

`[OLS3-REQ-0110]` Editorial Governance shall own `TERM-AUTHORITY` and `OP-APPROVE` exclusively.

`[OLS3-REQ-0111]` Referencing `OP-RECORD` or required `OP-VALIDATE` shall activate its owner profile.

`[OLS3-REQ-0112]` Editorial Governance shall preserve proposal, approval, canonical, publication, evidence, and validation statuses as distinct where they occur.

`[OLS3-REQ-0113]` Editorial Governance shall require OLS-2 authority scope for governed status change.

`[OLS3-REQ-0114]` Editorial Governance shall not treat approval or publication as empirical truth or permit software to replace declared human authority.

### 10.7 Education

*Stable clause ID: `OLS3-CLS-0017` — Profile ID: `PROFILE-EDUCATION` — Trace ID: `TRACE-000112` — Normative*

| Profile field | Specification |
| --- | --- |
| Identity | Education; Normative Profile; `PROFILE-EDUCATION`. |
| Purpose | Organize learner or reader entry, selection, practice, reflection, navigation, and fluency. |
| Architectural role | Applies Orientation Language semantics to teaching and reader progression without asserting a universal cognitive law. |
| Inherited universal semantics | Complete OLS-1. |
| Owned primitive concepts | None. |
| Referenced primitive concepts | `TERM-MEMORY` where recorded learning or progression is claimed. |
| Owned primitive operators | None. |
| Referenced primitive operators | `OP-SELECT`; `OP-RECORD` where learning or reader progression is recorded. |
| Required declarations | `DECL-CONTEXT` and applicable perspective, position, representation type, identity, time, evidence class, and uncertainty status. Learner or reader, entry point, path, and purpose remain profile inputs. |
| Mandatory dependencies | Navigation. |
| Conditional dependencies | Memory/Learning when recorded or admitted learning is claimed. |
| Permitted composition | Navigation; Memory/Learning under the stated condition; other compatible profiles under Clause 7. |
| Conflict conditions | Missing Navigation, undeclared learner/reader context or path, treating completion as validation, or treating a teaching sequence as universal law. |
| Prohibited modifications | Shall not present pedagogical progression as a universal cognitive law or treat completion as validation. |

`[OLS3-REQ-0115]` Education shall be activated explicitly because it owns no primitive concept or primitive operator.

`[OLS3-REQ-0116]` Education shall activate Navigation as a mandatory dependency.

`[OLS3-REQ-0117]` Referencing `OP-RECORD` or claiming recorded learning shall activate Memory/Learning.

`[OLS3-REQ-0118]` Education shall preserve the difference between participation, completion, recording, admission, validation, and learning.

`[OLS3-REQ-0119]` Education shall not present its progression as universal cognitive law or completion as validation.

## 11 Primitive concept ownership

*Stable clause ID: `OLS3-CLS-0018` — Trace ID: `TRACE-000113` — Normative*

Version 1.0 contains exactly four profile primitive concepts: constraint, outcome, memory, and authority.

`[OLS3-REQ-0120]` Each profile primitive concept shall have exactly one owner in Annex C.

`[OLS3-REQ-0121]` A referencing profile shall use the owning definition and shall not redefine it.

`[OLS3-REQ-0122]` Invoking a profile primitive concept shall activate its owner profile.

`[OLS3-REQ-0123]` No additional profile primitive concept shall be introduced in Version 1.0.

### 11.1 constraint

*Stable clause ID: `OLS3-CLS-0019` — Term ID: `TERM-CONSTRAINT` — Trace ID: `TRACE-000114` — Normative*

**Definition:** a declared condition limiting admissible alternatives, paths, selections, or a bounded change within the active representation and context.

**Owner:** Navigation.

**Referencing profiles:** Transformation; Evidence/Validation where a constraint forms part of the tested conditions.

**Boundary:** constraint does not imply recommendation, optimality, authority, execution, or validation.

`[OLS3-REQ-0124]` Navigation shall remain the sole owner of `TERM-CONSTRAINT`.

`[OLS3-REQ-0125]` A profile referencing constraint shall activate Navigation and preserve the declared constraint basis.

`[OLS3-REQ-0126]` Constraint shall not be converted into selection, validation, or authority without the separately owned operator and conditions.

### 11.2 outcome

*Stable clause ID: `OLS3-CLS-0020` — Term ID: `TERM-OUTCOME` — Trace ID: `TRACE-000115` — Normative*

**Definition:** a declared observed result whose candidate, validation, and admission status is governed by Evidence/Validation.

**Owner:** Evidence/Validation.

**Referencing profiles:** Memory/Learning; Editorial Governance where outcomes support claims.

**Boundary:** a transformed state, candidate result, or validation status is not thereby an admitted outcome.

`[OLS3-REQ-0127]` Evidence/Validation shall remain the sole owner of `TERM-OUTCOME`.

`[OLS3-REQ-0128]` A profile referencing outcome shall activate Evidence/Validation and preserve candidate, validation, and admission status.

`[OLS3-REQ-0129]` Outcome shall not imply improvement, authority, publication, or learning.

### 11.3 memory

*Stable clause ID: `OLS3-CLS-0021` — Term ID: `TERM-MEMORY` — Trace ID: `TRACE-000116` — Normative*

**Definition:** a declared retained record of an observation or admitted outcome with identity, time, provenance, evidence class, and status.

**Owner:** Memory/Learning.

**Referencing profiles:** Editorial Governance; Education when recorded learning is claimed.

**Boundary:** a record is not thereby validated, canonical, experiential, or learned.

`[OLS3-REQ-0130]` Memory/Learning shall remain the sole owner of `TERM-MEMORY`.

`[OLS3-REQ-0131]` A profile referencing memory shall activate Memory/Learning and preserve identity, time, provenance, evidence class, uncertainty, and admission status.

`[OLS3-REQ-0132]` Memory shall not be treated as learning solely because material is retained.

### 11.4 authority

*Stable clause ID: `OLS3-CLS-0022` — Term ID: `TERM-AUTHORITY` — Trace ID: `TRACE-000117` — Normative*

**Definition:** declared permission held by an actor or role to perform a governed operation on a target within a declared authority scope.

**Owner:** Editorial Governance.

**Referencing profiles:** none as an independent Version 1.0 semantic owner; governed handoffs reference the Editorial Governance owner.

**Boundary:** evidence, validation, orientation, explanation, selection, or software capability is not authority.

`[OLS3-REQ-0133]` Editorial Governance shall remain the sole owner of `TERM-AUTHORITY`.

`[OLS3-REQ-0134]` A construction referencing authority shall activate Editorial Governance and identify `DECL-AUTHORITY-SCOPE`.

`[OLS3-REQ-0135]` Authority shall not be inferred from evidence, validation, orientation, explanation, selection, implementation capability, or operator order.

## 12 Profile boundaries

*Stable clause ID: `OLS3-CLS-0023` — Trace ID: `TRACE-000118` — Normative*

Profiles extend the Universal Base Language. They never redefine:

- an OLS-1 universal concept;
- an OLS-2 declaration or declaration responsibility;
- OLS-2 primitive operator ownership or contract;
- an OLS-1 universal boundary condition;
- the OLS-1 canonical universal process;
- another profile’s owned primitive concept, purpose, or prohibited modifications.

`[OLS3-REQ-0136]` A profile shall inherit all fourteen universal concepts without modification.

`[OLS3-REQ-0137]` A profile shall retain all five universal operator responsibilities and the OLS-1 canonical order.

`[OLS3-REQ-0138]` A profile shall not add an operator to or remove an operator from the canonical universal process.

`[OLS3-REQ-0139]` A profile shall not change an OLS-2 declaration definition, default, applicability, omission, incompatibility, or preservation rule.

`[OLS3-REQ-0140]` A profile shall not redefine an OLS-2 primitive operator contract or owner.

`[OLS3-REQ-0141]` A profile shall not convert metaphor, historical recurrence, implementation support, or visual similarity into semantic authority.

`[OLS3-REQ-0142]` Profile activation shall not imply empirical truth, implementation correctness, safety, performance, recommendation, authorization, execution, or outcome.

`[OLS3-REQ-0143]` A profile violating a boundary in Clause 12 shall make the affected composition malformed.

## 13 Normative summary

*Stable clause ID: `OLS3-CLS-0024` — Trace ID: `TRACE-000119` — Normative*

Version 1.0 consists of one mandatory Universal Base Language and the seven optional semantic profiles registered in Annex A. Active profiles extend inherited semantics through uniquely owned concepts and operators, resolved dependencies, compatible declarations, legal composition, conflict detection, and explicit reporting.

`[OLS3-REQ-0144]` A Version 1.0 profile composition shall resolve to Annexes A, B, and C and the applicable profile clauses.

`[OLS3-REQ-0145]` OLS-3 shall preserve unique ownership, explicit activation, dependency resolution, and universal boundaries in every profile composition.

`[OLS3-REQ-0146]` OLS-3 shall remain independent of implementation technology and shall not define derivations or conformance procedures.

---

# Annex A — Profile Registry

*Annex ID: `OLS3-ANN-A` — Trace ID: `TRACE-000120` — Normative*

## A.1 Version 1.0 profiles

| Profile ID | Canonical name | Authoritative clause | Owned primitive concepts | Owned primitive operators |
| --- | --- | --- | --- | --- |
| `PROFILE-REPRESENTATION` | Representation | `OLS3-CLS-0011` | None | None |
| `PROFILE-NAVIGATION` | Navigation | `OLS3-CLS-0012` | `TERM-CONSTRAINT` | `OP-SELECT` |
| `PROFILE-TRANSFORMATION` | Transformation | `OLS3-CLS-0013` | None | `OP-TRANSFORM` |
| `PROFILE-EVIDENCE-VALIDATION` | Evidence/Validation | `OLS3-CLS-0014` | `TERM-OUTCOME` | `OP-VALIDATE` |
| `PROFILE-MEMORY-LEARNING` | Memory/Learning | `OLS3-CLS-0015` | `TERM-MEMORY` | `OP-RECORD` |
| `PROFILE-EDITORIAL-GOVERNANCE` | Editorial Governance | `OLS3-CLS-0016` | `TERM-AUTHORITY` | `OP-APPROVE` |
| `PROFILE-EDUCATION` | Education | `OLS3-CLS-0017` | None | None |

`[OLS3-REQ-0147]` Annex A shall contain exactly seven Version 1.0 profiles.

`[OLS3-REQ-0148]` A Profile ID shall not be reassigned to another purpose or owner.

`[OLS3-REQ-0149]` A profile shall not be added, removed, or given a changed responsibility without the applicable Architecture Revision Process.

---

# Annex B — Dependency and Activation Matrix

*Annex ID: `OLS3-ANN-B` — Trace ID: `TRACE-000121` — Normative*

| Active profile | Explicit activation required | Mandatory profile dependencies | Conditional dependencies and trigger |
| --- | --- | --- | --- |
| Representation | Yes; no owned primitive activation | None | Owner profile of any additionally referenced profile primitive |
| Navigation | No when `TERM-CONSTRAINT` or `OP-SELECT` is invoked; otherwise yes | Representation | Transformation when `OP-TRANSFORM` is invoked; Memory/Learning when `OP-RECORD` is invoked |
| Transformation | No when `OP-TRANSFORM` is invoked; otherwise yes | Representation | Navigation when `TERM-CONSTRAINT` is referenced; Evidence/Validation when `OP-VALIDATE` is invoked |
| Evidence/Validation | No when `TERM-OUTCOME` or `OP-VALIDATE` is invoked; otherwise yes | None | Representation for represented material; Navigation when `TERM-CONSTRAINT` is referenced; Transformation when `OP-TRANSFORM` is invoked; Memory/Learning when `OP-RECORD` is invoked |
| Memory/Learning | No when `TERM-MEMORY` or `OP-RECORD` is invoked; otherwise yes | None for observation recording | Evidence/Validation for experiential learning or admitted outcomes |
| Editorial Governance | No when `TERM-AUTHORITY` or `OP-APPROVE` is invoked; otherwise yes | None | Memory/Learning for persistence or `OP-RECORD`; Evidence/Validation where claims/results require verification |
| Education | Yes; no owned primitive activation | Navigation | Memory/Learning when recorded or admitted learning is claimed |

`[OLS3-REQ-0150]` Annex B shall control Version 1.0 mandatory and conditional profile dependencies.

`[OLS3-REQ-0151]` A conditional dependency shall activate exactly when its registered trigger applies.

`[OLS3-REQ-0152]` An activation route shall not change the semantics of the activated profile.

`[OLS3-REQ-0153]` The Universal Base Language shall be inherited by every row and shall not be represented as a profile dependency.

---

# Annex C — Primitive Concept Ownership Registry

*Annex ID: `OLS3-ANN-C` — Trace ID: `TRACE-000122` — Normative*

| Term ID | Primitive concept | Semantic owner | Referencing profiles or components | Authoritative clause |
| --- | --- | --- | --- | --- |
| `TERM-CONSTRAINT` | constraint | Navigation | Transformation; Evidence/Validation | `OLS3-CLS-0019` |
| `TERM-OUTCOME` | outcome | Evidence/Validation | Memory/Learning; Editorial Governance where outcomes support claims | `OLS3-CLS-0020` |
| `TERM-MEMORY` | memory | Memory/Learning | Editorial Governance; Education where recorded learning is claimed | `OLS3-CLS-0021` |
| `TERM-AUTHORITY` | authority | Editorial Governance | Governed handoffs through the owning profile | `OLS3-CLS-0022` |

`[OLS3-REQ-0154]` Annex C shall contain exactly four Version 1.0 profile primitive concepts.

`[OLS3-REQ-0155]` Each Annex C concept shall have exactly one semantic owner.

`[OLS3-REQ-0156]` A referencing profile shall preserve the owner, definition, boundaries, and activation rule.

`[OLS3-REQ-0157]` An Annex C Term ID shall not be reassigned or given a second normative definition.

---

# Annex D — Composition Examples

*Annex ID: `OLS3-ANN-D` — Informative*

## D.1 Base plus Representation

A construction explicitly activates Representation, inherits OLS-1, declares its representation type, construction perspective, context, and applicable scale, and invokes `OP-REPRESENT`. No other profile becomes active merely because the representation is implemented as a graph.

## D.2 Navigation with persisted path

Invoking `OP-SELECT` activates Navigation and its mandatory Representation dependency. Persisting the selected path invokes `OP-RECORD`, conditionally activating Memory/Learning. The selection remains distinct from recommendation and authority.

## D.3 Tested transformation

Invoking `OP-TRANSFORM` activates Transformation and Representation. Testing its resulting state with `OP-VALIDATE` activates Evidence/Validation. The transformed state, validation status, and admitted outcome remain distinct.

## D.4 Recorded educational progression

Education is activated explicitly and activates Navigation. If learner progression is recorded with `OP-RECORD`, Memory/Learning becomes active. Completion does not become validation or learning merely through recording.

---

# Annex E — Conflict Examples

*Annex ID: `OLS3-ANN-E` — Informative*

## E.1 Ownership conflict

A Transformation construction supplies a second definition of `TERM-CONSTRAINT`. Navigation already owns that concept. The composition is malformed.

## E.2 Declaration conflict

Two active profiles use incompatible identity criteria for one claimed continuing subject without preserving the difference as uncertainty. The composition is malformed.

## E.3 Missing dependency

Education is active while Navigation is absent. The mandatory dependency is unresolved, so the composition is incomplete; a claim of completed composition makes it malformed.

## E.4 Incompatible representation

Navigation selects alternatives from two representation types without a compatible basis. The composition is malformed.

## E.5 Prohibited modification

Evidence/Validation treats validation status as publication authority. This changes a universal and profile boundary. The composition is malformed.

## E.6 Non-conflicting disagreement

Two compatible perspectives disagree while retaining their declarations, evidence, and uncertainty. The disagreement is reported but is not itself a profile conflict.

---

# Annex F — Architectural Traceability to Phase 2D

*Annex ID: `OLS3-ANN-F` — Informative*

## F.1 Traceability rule

This annex maps OLS-3 normative clauses to the frozen architecture and controlling OLS clauses. It does not add normative semantics.

## F.2 Clause traceability

| Trace ID | OLS-3 subject | Authoritative source |
| --- | --- | --- |
| `TRACE-000096` | Scope | Phase 2D `09_CANONICAL_ARCHITECTURE.md`; Phase 3 Charter; OLS-0 Annex A |
| `TRACE-000097` | Normative references | Phase 2D canonical baseline; OLS-0; OLS-1; OLS-2 |
| `TRACE-000098` | Terms | Phase 2D `03_PROFILE_ARCHITECTURE.md`; `04_PROFILE_COMPOSITION.md` |
| `TRACE-000099` | Common profile model | Phase 2D consolidated profile architecture and composition model |
| `TRACE-000100` | Activation | Phase 2D `04_PROFILE_COMPOSITION.md`, Profile activation |
| `TRACE-000101` | Dependencies | Phase 2D profile table, dependency ordering, and consolidated graph |
| `TRACE-000102` | Legal composition | Phase 2D `04_PROFILE_COMPOSITION.md`, Legal composition |
| `TRACE-000103` | Conflicts | Phase 2D `04_PROFILE_COMPOSITION.md`, Conflict detection |
| `TRACE-000104` | Reporting | Phase 2D `04_PROFILE_COMPOSITION.md`, Active-profile reporting |
| `TRACE-000105` | Profile inventory | Phase 2D `03_PROFILE_ARCHITECTURE.md`; `09_CANONICAL_ARCHITECTURE.md` |
| `TRACE-000106` | Representation | Phase 2D profile table, Representation row; OLS-1 representation boundary; OLS-2 declarations/contracts |
| `TRACE-000107` | Navigation | Phase 2D profile table, Navigation row; OLS-2 `OP-SELECT` |
| `TRACE-000108` | Transformation | Phase 2D profile table, Transformation row; OLS-2 `OP-TRANSFORM` |
| `TRACE-000109` | Evidence/Validation | Phase 2D profile table, Evidence/Validation row; OLS-2 `OP-VALIDATE`; Phase 2D validation/outcome order |
| `TRACE-000110` | Memory/Learning | Phase 2D profile table, Memory/Learning row; OLS-2 `OP-RECORD`; Phase 2D validation/outcome order |
| `TRACE-000111` | Editorial Governance | Phase 2D profile table, Editorial Governance row; OLS-2 `OP-APPROVE` |
| `TRACE-000112` | Education | Phase 2D profile table, Education row |
| `TRACE-000113` | Primitive concept ownership | Phase 2D profile primitive ownership table |
| `TRACE-000114` | constraint | Phase 2D owner/reference table; Navigation and Transformation profile rows |
| `TRACE-000115` | outcome | Phase 2D owner/reference table; validation/outcome architecture |
| `TRACE-000116` | memory | Phase 2D owner/reference table; Memory/Learning profile row |
| `TRACE-000117` | authority | Phase 2D owner/reference table; Editorial Governance profile row; OLS-2 authority scope |
| `TRACE-000118` | Profile boundaries | Phase 2D universal inheritance, prohibited modifications, and non-profile boundaries |
| `TRACE-000119` | Summary | Phase 2D canonical architecture and profile composition |
| `TRACE-000120` | Profile Registry | Phase 2D consolidated profile table |
| `TRACE-000121` | Dependency Matrix | Phase 2D dependency ordering, profile rows, and dependency graph |
| `TRACE-000122` | Concept Ownership Registry | Phase 2D profile primitive ownership table |

## F.3 Requirement coverage

Requirement IDs `OLS3-REQ-0001` through `OLS3-REQ-0157` are governed by the Trace ID of their containing normative clause or annex. Requirement-to-test mappings belong to OLS-5.

---

## End of OLS-3
