# Orientation Language Specification — OLS-1

## Universal Base Language

| Metadata field | Value |
| --- | --- |
| Document ID | `OLS-1` |
| Edition | 1 |
| Suite version | `1.0.0` |
| Document revision | `1.0.0` |
| Status | Version 1.0 publication candidate |
| Publication date | 17 July 2026 |
| Language | English |
| Normative scope | Universal Base Language |
| Semantic scope | Fourteen universal concepts, five universal operator responsibilities, canonical process, universal boundaries, inheritance, concept/declaration distinction, base-expression boundaries |
| Replaces | Phase 2D architectural summaries for the Universal Base Language upon suite publication |
| Normative dependency | `OLS-0` |
| Forward references | `OLS-2` for declarations and complete operator contracts; `OLS-5` for conformance assessment |
| Release manifest identifier | Pending assignment at suite publication |
| Persistent citation identifier | Unassigned |
| Architecture baseline | Phase 2D Canonical Architecture, frozen by ADR-0001 |

## Status of this document

OLS-1 is the single authoritative specification of the Universal Base Language. Except for Annexes C and D, all clauses and annexes in this document are **Normative**.

OLS-1 defines universal semantic responsibilities only. It does not define declaration applicability, complete operator contracts, profile semantics, derivations, detailed conformance procedures, governance, or implementation guidance.

---

## 1 Scope

*Stable clause ID: `OLS1-CLS-0001` — Trace ID: `TRACE-000024` — Normative*

OLS-1 specifies:

- the status and architectural position of the Universal Base Language;
- fourteen universal concept primitives;
- five universal primitive operators at responsibility level;
- the canonical universal process;
- universal boundary conditions;
- universal inheritance;
- the concept/declaration distinction;
- the base-language expression model and universal error conditions.

`[OLS1-REQ-0001]` The Universal Base Language shall contain exactly the concepts and primitive operator responsibilities specified by OLS-1.

`[OLS1-REQ-0002]` OLS-1 shall not define instance-level declaration semantics, complete operator contracts, profile-owned semantics, derivation rules, conformance procedures, governance, or implementation behavior.

`[OLS1-REQ-0003]` A reference from OLS-1 to a later suite part shall not transfer that part’s ownership to OLS-1.

## 2 Normative references

*Stable clause ID: `OLS1-CLS-0002` — Trace ID: `TRACE-000025` — Normative*

The following document is normatively indispensable to the application of OLS-1:

- Orientation Language Specification, `OLS-0`, *Specification Conventions and Suite Overview*, Edition 1, suite version `1.0.0`.

`[OLS1-REQ-0004]` OLS-1 shall be read using the normative keywords, identifier policy, cross-reference policy, semantic-ownership policy, and status conventions defined by OLS-0.

OLS-2 and OLS-5 are forward references. OLS-2 supplies declaration rules and complete primitive operator contracts. OLS-5 supplies conformance targets, tests, and result requirements. Neither forward reference changes the semantic definitions in OLS-1.

## 3 Terms and definitions

*Stable clause ID: `OLS1-CLS-0003` — Trace ID: `TRACE-000026` — Normative*

For OLS-1, the terms defined in Clause 7 and registered in Annex A are authoritative. Specification-governance terms are defined by OLS-0.

`[OLS1-REQ-0005]` Each universal concept shall have exactly one authoritative Term ID and definition in OLS-1.

`[OLS1-REQ-0006]` An alias, historical use, implementation label, or profile-specific term shall not replace an OLS-1 definition.

`[OLS1-REQ-0007]` Ordinary words used inside a definition shall not be interpreted as additional universal concept primitives unless Annex A registers them as such.

## 4 Universal Base Language status

*Stable clause ID: `OLS1-CLS-0004` — Trace ID: `TRACE-000027` — Normative*

The Universal Base Language is the mandatory semantic foundation of the Orientation Language. It is not an extension profile.

`[OLS1-REQ-0008]` The Universal Base Language shall be present in every Orientation Language construction that claims semantic conformance.

`[OLS1-REQ-0009]` The Universal Base Language shall not be deactivated, replaced, weakened, or redefined by a profile, implementation, application, example, or informative component.

`[OLS1-REQ-0010]` A construction using no extension profile shall remain a Universal Base Language construction when it satisfies the applicable requirements of OLS-1 and later owning parts.

`[OLS1-REQ-0011]` Use of the Universal Base Language shall not imply activation of a semantic profile.

## 5 Architectural position

*Stable clause ID: `OLS1-CLS-0005` — Trace ID: `TRACE-000028` — Normative*

The Universal Base Language establishes evidence-bounded orientation through universal concepts, operator responsibilities, process order, and boundary conditions.

`[OLS1-REQ-0012]` OLS-1 shall remain the semantic owner of the fourteen universal concepts and the responsibility-level meanings of OBSERVE, REPRESENT, COMPARE, ORIENT, and EXPLAIN.

`[OLS1-REQ-0013]` Transformation, persistence, selection, validation, authority, navigation, learning, publication, cultural interpretation, and implementation realization shall remain outside the universal primitive operator inventory.

`[OLS1-REQ-0014]` OLS-1 shall not present the Universal Base Language as a universal ontology or as a complete account of reality.

`[OLS1-REQ-0015]` Semantic profiles may extend the Universal Base Language only under OLS-3 and shall not modify OLS-1 semantics.

## 6 Universal semantic model

*Stable clause ID: `OLS1-CLS-0006` — Trace ID: `TRACE-000029` — Normative*

The universal semantic model is situated, representation-dependent, perspective-dependent, context-bound, and evidence-bounded. It preserves provenance and uncertainty while separating representation from reality and orientation from downstream acts or outcomes.

The model contains:

1. universal concepts that establish the distinctions used by the language;
2. universal primitive operators that act on declared material at responsibility level;
3. one canonical process ordering those operators;
4. boundary conditions restricting what their products imply;
5. declarations, specified in OLS-2, that supply applicable instance-level values or statuses.

`[OLS1-REQ-0016]` An orientation claim shall identify the context, perspective, representation, evidence, provenance, and uncertainty relevant to that claim through the applicable declaration rules of OLS-2.

`[OLS1-REQ-0017]` A representation shall remain distinguishable from the source material and reality it represents.

`[OLS1-REQ-0018]` An orientation shall remain distinguishable from recommendation, authorization, execution, outcome, learning, control, and certainty.

`[OLS1-REQ-0019]` A universal semantic assertion shall preserve the declared status of observations, evidence, provenance, and uncertainty through every universal operator that uses or communicates it.

## 7 Universal concept inventory

*Stable clause ID: `OLS1-CLS-0007` — Trace ID: `TRACE-000030` — Normative*

The Universal Base Language contains exactly fourteen concept primitives: observation, observer, context, perspective, representation, position, relation, state, transition, evidence, provenance, uncertainty, orientation, and difference.

`[OLS1-REQ-0020]` No additional concept shall be represented as a Version 1.0 universal primitive.

`[OLS1-REQ-0021]` A universal concept shall retain the definition, responsibility, and boundaries assigned by its owning subsection.

`[OLS1-REQ-0022]` The absence of an instance of a concept from a particular expression shall be evaluated by the claims made and the applicable OLS-2 declaration rules; it shall not remove the concept from the universal inventory.

### 7.1 observation

*Stable clause ID: `OLS1-CLS-0008` — Term ID: `TERM-OBSERVATION` — Trace ID: `TRACE-000031` — Normative*

**Definition:** noticed or captured source material admitted as an observation while retaining its declared source status.

**Semantic responsibility:** observation distinguishes source material available to the language from representations, findings, evidence claims, and outcomes derived or asserted later.

**Boundaries and non-implications:** an observation does not imply truth, completeness, neutrality, evidence, causality, or outcome.

**Relationships:** an observer notices or captures an observation; REPRESENT may use observations; provenance identifies their source; evidence may support a claim but is not created merely by observing; uncertainty records unresolved limits relevant to the observation.

**Declaration reference:** see OLS-2 for context, time where sequence matters, evidence class, provenance, and uncertainty-status declarations.

`[OLS1-REQ-0023]` A source item shall not acquire evidence, validation, or outcome status solely because it is an observation.

`[OLS1-REQ-0024]` An observation used by another universal operator shall preserve its declared source and epistemic status.

### 7.2 observer

*Stable clause ID: `OLS1-CLS-0009` — Term ID: `TERM-OBSERVER` — Trace ID: `TRACE-000032` — Normative*

**Definition:** the situated role associated with noticing or capturing observations and with constructing or reading a representation under a perspective and context.

**Semantic responsibility:** observer distinguishes the situated source or locus of observing from the observed material and from the representation used to interpret it.

**Boundaries and non-implications:** an observer is not perspective-free; the presence of an observer does not imply neutrality, authority, completeness, or correctness.

**Relationships:** an observer is situated by context, perspective, and, where applicable, position; the observer relates to observations and representations without becoming identical to either.

**Declaration reference:** see OLS-2 for context, perspective, and position declarations applicable to the claim.

`[OLS1-REQ-0025]` A construction shall keep the observer distinct from the observation and representation unless it explicitly asserts a relation among them.

`[OLS1-REQ-0026]` A construction shall not present an observer’s view as perspective-free.

### 7.3 context

*Stable clause ID: `OLS1-CLS-0010` — Term ID: `TERM-CONTEXT` — Trace ID: `TRACE-000033` — Normative*

**Definition:** the situational conditions, domain, and scope under which an observation, relation, representation, comparison, orientation, or explanation is interpreted.

**Semantic responsibility:** context bounds the applicability and interpretation of universal semantic assertions.

**Boundaries and non-implications:** context does not itself establish evidence, causality, universality, or truth.

**Relationships:** context situates observer, perspective, position, representation, state, transition, relation, difference, evidence, uncertainty, and orientation.

**Declaration reference:** OLS-2 owns the context declaration and its applicability and omission rules.

`[OLS1-REQ-0027]` An orientation act shall be interpreted within an explicitly declared context under OLS-2.

`[OLS1-REQ-0028]` A semantic assertion shall not be generalized beyond its declared context without a separately supported assertion.

### 7.4 perspective

*Stable clause ID: `OLS1-CLS-0011` — Term ID: `TERM-PERSPECTIVE` — Trace ID: `TRACE-000034` — Normative*

**Definition:** the condition or view under which a representation is constructed or read.

**Semantic responsibility:** perspective distinguishes how construction or reading conditions shape what a representation presents and how it is interpreted.

**Boundaries and non-implications:** perspective does not imply perspective-free truth, neutrality, completeness, consensus, or authority.

**Relationships:** perspective conditions observation, representation, comparison, difference, and orientation; multiple perspectives may be compared without being merged.

**Declaration reference:** OLS-2 owns construction-perspective and reading-perspective declaration requirements.

`[OLS1-REQ-0029]` A representation or orientation claim shall identify its applicable perspective under OLS-2.

`[OLS1-REQ-0030]` A construction shall not silently conflate a construction perspective with a reading perspective.

### 7.5 representation

*Stable clause ID: `OLS1-CLS-0012` — Term ID: `TERM-REPRESENTATION` — Trace ID: `TRACE-000035` — Normative*

**Definition:** a structured, analyzable form constructed from declared observations or data while preserving their provenance and status.

**Semantic responsibility:** representation makes declared material available for location, comparison, orientation, and explanation without identifying the structured form with reality.

**Boundaries and non-implications:** a representation does not imply reality, completeness, causal mechanism, or validation.

**Relationships:** REPRESENT constructs a representation; an observer constructs or reads it under context and perspective; position is located relative to it; COMPARE uses compatible represented items; ORIENT depends on it; provenance and uncertainty remain attached to relevant claims.

**Declaration reference:** OLS-2 owns representation-type, construction-perspective, context, provenance, and scale-where-applicable declarations.

`[OLS1-REQ-0031]` A representation shall remain explicitly distinguishable from the reality or source material it represents.

`[OLS1-REQ-0032]` A representation used for orientation shall identify its representation type under OLS-2.

`[OLS1-REQ-0033]` Representation compatibility shall not be assumed when the comparison basis or applicable declarations are absent or incompatible.

### 7.6 position

*Stable clause ID: `OLS1-CLS-0013` — Term ID: `TERM-POSITION` — Trace ID: `TRACE-000036` — Normative*

**Definition:** the location of an observer, focus, or system relative to a declared representation and context.

**Semantic responsibility:** position distinguishes where the focus of an orientation claim is located within the terms of the representation.

**Boundaries and non-implications:** position does not imply a target, path, reachability, navigation, preference, recommendation, or authority.

**Relationships:** position is interpreted within context and representation and may locate an observer, focus, state, or other represented item.

**Declaration reference:** OLS-2 owns the position declaration and its conditional applicability.

`[OLS1-REQ-0034]` A position-dependent assertion shall identify the applicable position under OLS-2.

`[OLS1-REQ-0035]` A position shall not be interpreted as a path or selection.

### 7.7 relation

*Stable clause ID: `OLS1-CLS-0014` — Term ID: `TERM-RELATION` — Trace ID: `TRACE-000037` — Normative*

**Definition:** a declared association between two or more items within a context or representation.

**Semantic responsibility:** relation distinguishes an asserted association from the items it connects and from any mechanism proposed to explain that association.

**Boundaries and non-implications:** a relation does not by itself imply causality, mechanism, direction, transformation, evidence, or universal applicability.

**Relationships:** relations may connect observations, representations, positions, states, transitions, evidence, perspectives, or other represented items; differences may be identified among related or unrelated compatible items.

**Declaration reference:** see OLS-2 for context and for time, scale, identity, perspective, or representation type where the asserted relation depends on them.

`[OLS1-REQ-0036]` A relation shall identify the items related and the context or representation in which the relation is asserted.

`[OLS1-REQ-0037]` A relation shall not be presented as a causal mechanism without separately governed support.

### 7.8 state

*Stable clause ID: `OLS1-CLS-0015` — Term ID: `TERM-STATE` — Trace ID: `TRACE-000038` — Normative*

**Definition:** a declared condition of an identified subject or represented item within a context and, where applicable, at a time.

**Semantic responsibility:** state distinguishes a condition represented as holding from a transition between conditions or an operation that changes them.

**Boundaries and non-implications:** a state does not imply stability, permanence, validation, outcome, desirability, or cause.

**Relationships:** a representation may contain states; a difference may distinguish states; a transition relates a source state and a resulting state; provenance and evidence support claims made about a state.

**Declaration reference:** see OLS-2 for context and for time, identity, scale, representation type, evidence class, and uncertainty status where applicable.

`[OLS1-REQ-0038]` A state assertion shall preserve the identity, time, and scale distinctions on which the assertion depends under OLS-2.

`[OLS1-REQ-0039]` A state shall not be treated as an admitted outcome solely because it occurs after another state.

### 7.9 transition

*Stable clause ID: `OLS1-CLS-0016` — Term ID: `TERM-TRANSITION` — Trace ID: `TRACE-000039` — Normative*

**Definition:** a declared change from one state to another under an applicable context, identity, and temporal order.

**Semantic responsibility:** transition distinguishes represented change between states from the states themselves and from any operator, cause, or mechanism associated with that change.

**Boundaries and non-implications:** a transition does not by itself imply causality, intentional transformation, execution, success, validation, outcome admission, or improvement.

**Relationships:** transition relates states and depends on difference between them; observations and representations may support a transition claim; provenance, evidence, and uncertainty qualify the claim.

**Declaration reference:** see OLS-2 for time, identity, context, scale, representation type, evidence class, and uncertainty-status declarations.

`[OLS1-REQ-0040]` A transition assertion shall identify the source and resulting states and preserve the applicable identity and temporal order under OLS-2.

`[OLS1-REQ-0041]` A transition shall not be treated as a TRANSFORM invocation or validated outcome solely because a change is represented.

### 7.10 evidence

*Stable clause ID: `OLS1-CLS-0017` — Term ID: `TERM-EVIDENCE` — Trace ID: `TRACE-000040` — Normative*

**Definition:** declared material used to support a claim while retaining its provenance, epistemic status, and uncertainty.

**Semantic responsibility:** evidence distinguishes material used in support of a claim from observation alone, from the claim itself, and from validation status.

**Boundaries and non-implications:** evidence does not by itself imply truth, proof, completeness, causality, validation, consensus, authority, recommendation, or outcome.

**Relationships:** evidence may consist of or refer to observations and representations; provenance identifies its origin; uncertainty limits its interpretation; ORIENT and EXPLAIN preserve its status.

**Declaration reference:** OLS-2 owns evidence-class, provenance, and uncertainty-status declarations.

`[OLS1-REQ-0042]` Material used as evidence shall retain its declared evidence class, provenance, and uncertainty under OLS-2.

`[OLS1-REQ-0043]` An observation shall not be treated as evidence for a claim without an explicit evidence assertion and applicable declaration.

`[OLS1-REQ-0044]` Evidence shall not be interpreted as validation or authority.

### 7.11 provenance

*Stable clause ID: `OLS1-CLS-0018` — Term ID: `TERM-PROVENANCE` — Trace ID: `TRACE-000041` — Normative*

**Definition:** declared information identifying the origin and relevant history or status of an observation, representation, or item of evidence.

**Semantic responsibility:** provenance preserves the trace from semantic material to its declared source and status.

**Boundaries and non-implications:** provenance does not imply truth, reliability, completeness, validation, authority, or correctness.

**Relationships:** provenance qualifies observations, representations, evidence, states, transitions, orientations, and explanations; time and identity may be needed when provenance includes history or continuity.

**Declaration reference:** OLS-2 owns the provenance-related requirements attached to representation, evidence, records, and relevant time/identity assertions.

`[OLS1-REQ-0045]` A universal operator shall preserve provenance for material whose source or status affects the resulting claim.

`[OLS1-REQ-0046]` Provenance shall not be used as a substitute for evidence evaluation or validation.

### 7.12 uncertainty

*Stable clause ID: `OLS1-CLS-0019` — Term ID: `TERM-UNCERTAINTY` — Trace ID: `TRACE-000042` — Normative*

**Definition:** unresolved or bounded lack of knowledge, including known limitation, missing information, disagreement, or unresolved status relevant to a claim.

**Semantic responsibility:** uncertainty preserves what remains unresolved rather than silently converting absence, limitation, or disagreement into confidence or certainty.

**Boundaries and non-implications:** uncertainty is not confidence, certainty, proof, validation, or permission to omit a known limitation.

**Relationships:** uncertainty qualifies observations, representations, comparisons, evidence, states, transitions, orientation, and explanation; disagreements between perspectives remain expressible as uncertainty or disagreement without forced resolution.

**Declaration reference:** OLS-2 owns the uncertainty-status declaration and its applicability.

`[OLS1-REQ-0047]` A universal operation producing a finding shall preserve relevant known uncertainty.

`[OLS1-REQ-0048]` A construction shall not silently replace uncertainty with confidence or certainty.

### 7.13 orientation

*Stable clause ID: `OLS1-CLS-0020` — Term ID: `TERM-ORIENTATION` — Trace ID: `TRACE-000043` — Normative*

**Definition:** situated understanding produced from declared observations, representation, context, perspective, position or focus, evidence, provenance, and uncertainty.

**Semantic responsibility:** orientation identifies what can be understood about a subject or focus relative to declared conditions and limits, before downstream recommendation, authorization, execution, or outcome.

**Boundaries and non-implications:** orientation does not imply recommendation, authorization, execution, outcome, learning, control, or certainty.

**Relationships:** ORIENT produces orientation after OBSERVE, REPRESENT, and COMPARE in the canonical process; EXPLAIN communicates it while preserving evidence, provenance, uncertainty, disagreement, unsupported conclusions, and limitations.

**Declaration reference:** see OLS-2 for context, perspective, position where applicable, representation type, evidence class, uncertainty status, and any time, scale, or identity distinctions on which the orientation depends.

`[OLS1-REQ-0049]` An orientation shall identify the representation, context, perspective, evidence, provenance, and uncertainty on which it depends under OLS-2.

`[OLS1-REQ-0050]` An orientation shall not be presented as recommendation, authorization, execution, outcome, learning, control, or certainty.

`[OLS1-REQ-0051]` An orientation shall preserve disagreement and unsupported conclusions as distinct from supported findings.

### 7.14 difference

*Stable clause ID: `OLS1-CLS-0021` — Term ID: `TERM-DIFFERENCE` — Trace ID: `TRACE-000044` — Normative*

**Definition:** a declared distinction between items, states, perspectives, or representations relative to a basis.

**Semantic responsibility:** difference makes non-equivalence available to comparison without being generated by, or reduced to, the COMPARE operator.

**Boundaries and non-implications:** difference does not by itself imply causality, preference, selection, validation, prediction, or universal law.

**Relationships:** COMPARE identifies differences among compatible declared items; differences may distinguish observations, representations, perspectives, relations, positions, states, transitions, evidence, or orientations.

**Declaration reference:** see OLS-2 for the comparison basis and for context, perspective, representation type, scale, time, and identity where they affect the distinction.

`[OLS1-REQ-0052]` Difference shall remain a universal primitive on which COMPARE depends.

`[OLS1-REQ-0053]` A difference shall identify its items and basis and shall not be treated as causal or preferential without separately governed support.

## 8 Universal primitive operators

*Stable clause ID: `OLS1-CLS-0022` — Trace ID: `TRACE-000045` — Normative*

The Universal Base Language owns exactly five primitive operator responsibilities: OBSERVE, REPRESENT, COMPARE, ORIENT, and EXPLAIN.

`[OLS1-REQ-0054]` OLS-1 operator clauses shall state responsibility and universal boundary only; complete inputs, outputs, preconditions, postconditions, failure behavior, and invocation syntax shall remain in OLS-2.

`[OLS1-REQ-0055]` An implementation, profile, application, or historical operator label shall not redefine a universal primitive operator.

### 8.1 OBSERVE

*Stable clause ID: `OLS1-CLS-0023` — Trace ID: `TRACE-000046` — Normative*

**Responsibility:** OBSERVE notices or captures declared signals, events, measurements, or context as observations.

**Universal boundary:** OBSERVE does not establish truth, completeness, neutrality, evidence, causality, or outcome.

`[OLS1-REQ-0056]` OBSERVE shall preserve the declared source status of admitted observations.

`[OLS1-REQ-0057]` A complete OBSERVE contract shall be taken from OLS-2.

### 8.2 REPRESENT

*Stable clause ID: `OLS1-CLS-0024` — Trace ID: `TRACE-000047` — Normative*

**Responsibility:** REPRESENT transforms declared observations or data into a structured, analyzable form while preserving provenance and status.

**Universal boundary:** REPRESENT does not establish reality, completeness, causal mechanism, or validation.

`[OLS1-REQ-0058]` REPRESENT shall preserve the representation/reality distinction and the source status of represented material.

`[OLS1-REQ-0059]` A complete REPRESENT contract shall be taken from OLS-2.

### 8.3 COMPARE

*Stable clause ID: `OLS1-CLS-0025` — Trace ID: `TRACE-000048` — Normative*

**Responsibility:** COMPARE identifies differences, agreements, or mismatches among declared compatible items relative to a declared basis.

**Universal boundary:** COMPARE does not establish causality, preference, selection, validation, prediction, or universal law.

`[OLS1-REQ-0060]` COMPARE shall use declared compatible items and a declared comparison basis under OLS-2.

`[OLS1-REQ-0061]` COMPARE shall depend on difference and shall not define difference.

`[OLS1-REQ-0062]` A complete COMPARE contract shall be taken from OLS-2.

### 8.4 ORIENT

*Stable clause ID: `OLS1-CLS-0026` — Trace ID: `TRACE-000049` — Normative*

**Responsibility:** ORIENT produces situated understanding from declared observations, representation, context, perspective, position or focus, evidence, provenance, and uncertainty.

**Universal boundary:** ORIENT does not establish recommendation, authorization, execution, outcome, learning, control, or certainty.

`[OLS1-REQ-0063]` ORIENT shall preserve the declared basis, evidence, provenance, uncertainty, disagreement, unsupported conclusions, and limitations relevant to its result.

`[OLS1-REQ-0064]` A complete ORIENT contract shall be taken from OLS-2.

### 8.5 EXPLAIN

*Stable clause ID: `OLS1-CLS-0027` — Trace ID: `TRACE-000050` — Normative*

**Responsibility:** EXPLAIN communicates structured findings while preserving evidence, uncertainty, disagreement, unsupported conclusions, and limitations.

**Universal boundary:** EXPLAIN does not establish truth, proof, consensus, authority, recommendation, or publication approval.

`[OLS1-REQ-0065]` EXPLAIN shall not increase the epistemic or authority status of the material it communicates.

`[OLS1-REQ-0066]` A complete EXPLAIN contract shall be taken from OLS-2.

## 9 Canonical universal process

*Stable clause ID: `OLS1-CLS-0028` — Trace ID: `TRACE-000051` — Normative*

The canonical universal process is:

```text
OBSERVE
↓
REPRESENT
↓
COMPARE
↓
ORIENT
↓
EXPLAIN
```

**Process intent:** the sequence produces and communicates evidence-bounded orientation while preserving declared source status, representation boundaries, comparison basis, context, perspective, evidence, provenance, uncertainty, disagreements, unsupported conclusions, and limits.

**Ordering:** each stage consumes or refers to material established by preceding stages. The process order is semantic order; it does not require a particular software execution architecture.

**Permitted omissions:** no stage may be omitted from a construction claiming the complete canonical universal process. A construction may invoke or describe fewer operators under their OLS-2 contracts, but it is then a partial universal construction rather than a complete canonical process.

**Prohibited interpretations:** the sequence is not a decision cycle, authorization chain, execution workflow, validation process, learning process, universal cognitive law, or guarantee of truth or outcome.

`[OLS1-REQ-0067]` A construction claiming the complete canonical universal process shall include the five operators in the specified order.

`[OLS1-REQ-0068]` A partial construction shall identify the stages present and shall not claim completion of the canonical universal process.

`[OLS1-REQ-0069]` Repetition or return to an earlier stage may occur when new observations, representations, comparisons, or uncertainties arise, but each completed pass shall preserve the canonical order.

`[OLS1-REQ-0070]` The canonical process shall not be represented as including a profile-owned operator unless the applicable profile is explicitly active under OLS-3.

`[OLS1-REQ-0071]` Completion of the canonical process shall not imply recommendation, authorization, execution, validation, outcome, learning, control, certainty, or empirical truth.

## 10 Universal boundary conditions

*Stable clause ID: `OLS1-CLS-0029` — Trace ID: `TRACE-000052` — Normative*

The universal boundary conditions in Annex B apply to every Universal Base Language construction and are inherited by every semantic profile.

`[OLS1-REQ-0072]` A downstream clause, profile, implementation, application, example, or explanatory text shall not weaken a universal non-implication.

`[OLS1-REQ-0073]` A construction shall preserve the distinction between representation and reality.

`[OLS1-REQ-0074]` A construction shall preserve the distinction between orientation and recommendation, authorization, execution, outcome, learning, control, and certainty.

`[OLS1-REQ-0075]` A claim crossing a universal boundary shall require separately owned semantics and shall not be inferred from the Universal Base Language alone.

## 11 Universal inheritance

*Stable clause ID: `OLS1-CLS-0030` — Trace ID: `TRACE-000053` — Normative*

Every semantic profile inherits:

1. all fourteen universal concepts;
2. all five universal primitive operator responsibilities;
3. all universal boundary conditions;
4. the concept/declaration distinction;
5. every universal declaration applicable to the operation under OLS-2;
6. the rule that profile semantics may extend but never redefine the Universal Base Language.

`[OLS1-REQ-0076]` A profile shall inherit the Universal Base Language as a complete unit.

`[OLS1-REQ-0077]` A profile shall not override, narrow, broaden, replace, or deactivate an inherited universal definition, responsibility, process boundary, or non-implication.

`[OLS1-REQ-0078]` Referencing a universal concept or operator from a profile shall not transfer semantic ownership.

`[OLS1-REQ-0079]` Historical, cultural, implementation, or application material shall not participate in universal inheritance unless a normative suite part assigns it semantics through the applicable architecture process.

## 12 Concept–declaration distinction

*Stable clause ID: `OLS1-CLS-0031` — Trace ID: `TRACE-000054` — Normative*

A concept defines a semantic distinction. A declaration supplies an instance-level value or status for a distinction in a particular construction.

A universal concept may also require a declaration value without duplication. For example, the universal concept perspective distinguishes the responsibility of perspective, while a perspective declaration identifies the construction or reading perspective used by an expression.

`[OLS1-REQ-0080]` A declaration shall not create a new universal concept.

`[OLS1-REQ-0081]` The presence of a declaration shall not by itself supply evidence, validation, authority, or truth.

`[OLS1-REQ-0082]` A declaration value shall not replace the authoritative definition of the concept to which it applies.

`[OLS1-REQ-0083]` OLS-1 shall not determine declaration syntax, value domains, applicability, omission, incompatibility, or default behavior; OLS-2 owns those rules.

`[OLS1-REQ-0084]` No declaration value shall be inferred merely from the presence of a universal concept.

## 13 Base Language expression model

*Stable clause ID: `OLS1-CLS-0032` — Trace ID: `TRACE-000055` — Normative*

A Universal Base Language expression is a structured semantic assertion or record that uses one or more universal concepts or operators while preserving their definitions, ownership, applicable declarations, and universal boundaries.

A **complete universal orientation expression** is a Universal Base Language expression that realizes the five-stage canonical process. A **partial universal construction** uses fewer stages or expresses only a subset of applicable universal semantics and does not claim a complete orientation process.

A complete universal orientation expression contains or identifies:

- declared source material and observations;
- the observer or situated focus relevant to the act;
- context and perspective;
- a declared representation and its type through OLS-2;
- compatible comparison items and basis;
- relevant differences, agreements, or mismatches;
- the resulting orientation;
- evidence, provenance, and uncertainty relevant to findings;
- an explanation preserving disagreements, unsupported conclusions, and limitations;
- every additional universal concept and declaration on which its actual claims depend.

`[OLS1-REQ-0085]` A valid Universal Base Language expression shall use universal terms according to their OLS-1 definitions.

`[OLS1-REQ-0086]` A valid expression shall preserve all applicable universal boundary conditions.

`[OLS1-REQ-0087]` A valid expression shall identify every declaration required by its claims under OLS-2.

`[OLS1-REQ-0088]` A complete universal orientation expression shall identify the five canonical stages and their semantic products without claiming profile-owned capability.

`[OLS1-REQ-0089]` A partial universal construction may be valid within its declared scope but shall not claim a complete orientation process or a downstream implication excluded by OLS-1.

`[OLS1-REQ-0090]` A Universal Base Language expression need not activate or identify a semantic profile.

## 14 Universal error conditions

*Stable clause ID: `OLS1-CLS-0033` — Trace ID: `TRACE-000056` — Normative*

Universal Base Language constructions are classified at semantic level as valid, incomplete, or malformed. OLS-5 owns the complete conformance error taxonomy and test procedures.

**Incomplete construction:** a construction whose intended claim is recognizable but lacks an applicable concept, canonical stage, declaration, source/status distinction, or preserved limitation needed to support that claim.

**Malformed construction:** a construction that contradicts an authoritative definition, combines incompatible semantic assertions, violates a category or ownership boundary, asserts a prohibited implication, or claims completion despite an unresolved semantic conflict.

`[OLS1-REQ-0091]` A construction claiming the complete canonical process with one or more missing stages shall be incomplete.

`[OLS1-REQ-0092]` A construction missing a universal concept or declaration on which its actual claim depends shall be incomplete.

`[OLS1-REQ-0093]` A construction containing contradictory assertions about the same identified semantic item under the same declared basis shall be malformed unless the contradiction is explicitly preserved as disagreement or uncertainty.

`[OLS1-REQ-0094]` A construction treating a concept as an operator, an operator as a concept definition, a declaration as evidence, or an implementation as semantic authority shall be malformed.

`[OLS1-REQ-0095]` A construction that treats representation as reality or orientation as recommendation, authorization, execution, outcome, learning, control, or certainty shall be malformed.

`[OLS1-REQ-0096]` A construction that redefines a universal concept or primitive operator responsibility shall be malformed.

`[OLS1-REQ-0097]` An incomplete construction may be completed only by supplying supported missing material under the owning specification part; missing semantics shall not be invented or inferred.

## 15 Normative summary

*Stable clause ID: `OLS1-CLS-0034` — Trace ID: `TRACE-000057` — Normative*

The Universal Base Language is the mandatory, minimal semantic foundation of the Orientation Language. Its authoritative inventory is Annex A. Its universal non-implications are Annex B. Its five primitive operators form the canonical process in Clause 9. All profiles inherit these semantics without modification.

`[OLS1-REQ-0098]` A Version 1.0 claim to the Universal Base Language shall resolve to the fourteen concepts, five operator responsibilities, canonical process, boundaries, inheritance, and concept/declaration distinction specified by OLS-1.

`[OLS1-REQ-0099]` OLS-1 semantics shall remain independent of implementation technology and shall not acquire profile, derivation, governance, or implementation meaning by implication.

---

# Annex A — Universal Concept Registry

*Annex ID: `OLS1-ANN-A` — Trace ID: `TRACE-000058` — Normative*

## A.1 Registry authority

This annex is the Version 1.0 normative registry of universal concepts. Definitions remain authoritative in the cited clauses.

`[OLS1-REQ-0100]` The universal concept inventory shall contain exactly the fourteen entries in Table A.1.

## A.2 Table A.1 — Universal concepts

| Term ID | Canonical term | Authoritative clause | Semantic owner | Status |
| --- | --- | --- | --- | --- |
| `TERM-OBSERVATION` | observation | `OLS1-CLS-0008` | Universal Base Language | Universal primitive |
| `TERM-OBSERVER` | observer | `OLS1-CLS-0009` | Universal Base Language | Universal primitive |
| `TERM-CONTEXT` | context | `OLS1-CLS-0010` | Universal Base Language | Universal primitive |
| `TERM-PERSPECTIVE` | perspective | `OLS1-CLS-0011` | Universal Base Language | Universal primitive |
| `TERM-REPRESENTATION` | representation | `OLS1-CLS-0012` | Universal Base Language | Universal primitive |
| `TERM-POSITION` | position | `OLS1-CLS-0013` | Universal Base Language | Universal primitive |
| `TERM-RELATION` | relation | `OLS1-CLS-0014` | Universal Base Language | Universal primitive |
| `TERM-STATE` | state | `OLS1-CLS-0015` | Universal Base Language | Universal primitive |
| `TERM-TRANSITION` | transition | `OLS1-CLS-0016` | Universal Base Language | Universal primitive |
| `TERM-EVIDENCE` | evidence | `OLS1-CLS-0017` | Universal Base Language | Universal primitive |
| `TERM-PROVENANCE` | provenance | `OLS1-CLS-0018` | Universal Base Language | Universal primitive |
| `TERM-UNCERTAINTY` | uncertainty | `OLS1-CLS-0019` | Universal Base Language | Universal primitive |
| `TERM-ORIENTATION` | orientation | `OLS1-CLS-0020` | Universal Base Language | Universal primitive |
| `TERM-DIFFERENCE` | difference | `OLS1-CLS-0021` | Universal Base Language | Universal primitive |

`[OLS1-REQ-0101]` An entry shall not be added to or removed from Table A.1 without an approved Architecture Revision Process.

---

# Annex B — Universal Boundary Matrix

*Annex ID: `OLS1-ANN-B` — Trace ID: `TRACE-000059` — Normative*

## B.1 Matrix authority

Table B.1 is the Version 1.0 normative matrix of universal non-implications.

## B.2 Table B.1 — Universal non-implications

| Semantic product or operation | Does not imply |
| --- | --- |
| observation / OBSERVE | truth; completeness; neutrality; evidence; causality; outcome |
| representation / REPRESENT | reality; completeness; causal mechanism; validation |
| comparison / COMPARE | causality; preference; selection; validation; prediction; universal law |
| orientation / ORIENT | recommendation; authorization; execution; outcome; learning; control; certainty |
| explanation / EXPLAIN | truth; proof; consensus; authority; recommendation; publication approval |

`[OLS1-REQ-0102]` Every Universal Base Language construction shall preserve every applicable non-implication in Table B.1.

`[OLS1-REQ-0103]` A later specification part may add separately owned semantics but shall not erase a non-implication in Table B.1.

---

# Annex C — Minimal Orientation Examples

*Annex ID: `OLS1-ANN-C` — Informative*

The examples illustrate OLS-1 only. They do not define operator contracts, declaration syntax, profile semantics, conformance tests, or implementation formats.

## C.1 Minimal complete process

**OBSERVE:** A declared source provides two readings, each retained as an observation with source status and known uncertainty.

**REPRESENT:** The readings are placed in one declared structured form. The form is identified as a representation, not reality.

**COMPARE:** The readings are compared under one declared basis. A difference is recorded; no causal explanation is inferred.

**ORIENT:** The difference is interpreted relative to the declared context, perspective, focus, evidence, provenance, and uncertainty. The result states what is supported and what remains unknown.

**EXPLAIN:** The orientation is communicated with its evidence, disagreement if any, unsupported conclusions, and limitations. No recommendation or authorization is issued.

## C.2 Two perspectives without forced agreement

One source is represented under two declared perspectives. COMPARE identifies an agreement and a disagreement between the represented readings. ORIENT preserves both, together with the evidence and uncertainty relevant to each perspective. EXPLAIN reports the disagreement without converting it into consensus or a false middle.

## C.3 Partial universal construction

A source is observed and represented, but no comparison, orientation, or explanation is produced. The construction may accurately report those two stages. It is not a complete canonical universal process and does not claim orientation.

## C.4 Invalid boundary crossing

A representation shows a possible difference, and the author labels one downstream action “authorized.” OLS-1 provides neither recommendation nor authority semantics. The authorization claim therefore cannot follow from the Universal Base Language.

---

# Annex D — Architectural Traceability to Phase 2D

*Annex ID: `OLS1-ANN-D` — Informative*

## D.1 Traceability rule

This annex maps OLS-1 normative clauses to the frozen architecture. It does not add normative semantics. Phase 2D filenames identify artifacts in the architecture baseline.

## D.2 Table D.1 — Clause traceability

| Trace ID | OLS-1 subject | Phase 2D source |
| --- | --- | --- |
| `TRACE-000024` | Scope | `01_UNIVERSAL_BASE_LANGUAGE.md`; `09_CANONICAL_ARCHITECTURE.md`; Phase 3 Charter |
| `TRACE-000025` | Normative references | `09_CANONICAL_ARCHITECTURE.md`, Phase 3 input boundary; OLS-0 Annex A; Phase 3 Charter |
| `TRACE-000026` | Terms and definitions | `08_NORMATIVE_CLASSIFICATION.md`; OLS-0 terminology policy |
| `TRACE-000027` | Base-language status | `01_UNIVERSAL_BASE_LANGUAGE.md`, Architectural status |
| `TRACE-000028` | Architectural position | `01_UNIVERSAL_BASE_LANGUAGE.md`, Architectural role; `09_CANONICAL_ARCHITECTURE.md` |
| `TRACE-000029` | Universal semantic model | `01_UNIVERSAL_BASE_LANGUAGE.md`; `02_CONCEPTS_AND_DECLARATIONS.md` |
| `TRACE-000030` | Universal inventory | `01_UNIVERSAL_BASE_LANGUAGE.md`, Universal concepts; `09_CANONICAL_ARCHITECTURE.md` |
| `TRACE-000031` | observation | `01_UNIVERSAL_BASE_LANGUAGE.md`, OBSERVE and universal boundaries; `05_OPERATOR_OWNERSHIP.md`; `07_VALIDATION_AND_OUTCOME.md` |
| `TRACE-000032` | observer | `01_UNIVERSAL_BASE_LANGUAGE.md`, universal inventory; `02_CONCEPTS_AND_DECLARATIONS.md`, position/perspective distinctions |
| `TRACE-000033` | context | `02_CONCEPTS_AND_DECLARATIONS.md`, context row and architectural rule |
| `TRACE-000034` | perspective | `02_CONCEPTS_AND_DECLARATIONS.md`, perspective row and example |
| `TRACE-000035` | representation | `01_UNIVERSAL_BASE_LANGUAGE.md`, REPRESENT and boundaries; `02_CONCEPTS_AND_DECLARATIONS.md`; `03_PROFILE_ARCHITECTURE.md` |
| `TRACE-000036` | position | `02_CONCEPTS_AND_DECLARATIONS.md`, position row |
| `TRACE-000037` | relation | `01_UNIVERSAL_BASE_LANGUAGE.md`, universal inventory; `02_CONCEPTS_AND_DECLARATIONS.md`, context omission boundary; `03_PROFILE_ARCHITECTURE.md`, representation/mechanism boundary |
| `TRACE-000038` | state | `01_UNIVERSAL_BASE_LANGUAGE.md`, universal inventory; `02_CONCEPTS_AND_DECLARATIONS.md`, time/identity rows; `07_VALIDATION_AND_OUTCOME.md` |
| `TRACE-000039` | transition | `01_UNIVERSAL_BASE_LANGUAGE.md`, universal inventory; `02_CONCEPTS_AND_DECLARATIONS.md`, time/identity rows; `07_VALIDATION_AND_OUTCOME.md` |
| `TRACE-000040` | evidence | `01_UNIVERSAL_BASE_LANGUAGE.md`, ORIENT/EXPLAIN and boundaries; `02_CONCEPTS_AND_DECLARATIONS.md`, evidence-class row; `07_VALIDATION_AND_OUTCOME.md` |
| `TRACE-000041` | provenance | `01_UNIVERSAL_BASE_LANGUAGE.md`, REPRESENT/ORIENT; `02_CONCEPTS_AND_DECLARATIONS.md`, provenance references; `07_VALIDATION_AND_OUTCOME.md` |
| `TRACE-000042` | uncertainty | `01_UNIVERSAL_BASE_LANGUAGE.md`, ORIENT/EXPLAIN; `02_CONCEPTS_AND_DECLARATIONS.md`, uncertainty-status row |
| `TRACE-000043` | orientation | `01_UNIVERSAL_BASE_LANGUAGE.md`, ORIENT responsibility and boundaries; `05_OPERATOR_OWNERSHIP.md` |
| `TRACE-000044` | difference | `01_UNIVERSAL_BASE_LANGUAGE.md`, universal inventory and COMPARE; ADR-0001, Decision 2 |
| `TRACE-000045` | Universal operators | `01_UNIVERSAL_BASE_LANGUAGE.md`, Universal operators; `05_OPERATOR_OWNERSHIP.md` |
| `TRACE-000046` | OBSERVE | `01_UNIVERSAL_BASE_LANGUAGE.md`; `05_OPERATOR_OWNERSHIP.md` |
| `TRACE-000047` | REPRESENT | `01_UNIVERSAL_BASE_LANGUAGE.md`; `05_OPERATOR_OWNERSHIP.md` |
| `TRACE-000048` | COMPARE | `01_UNIVERSAL_BASE_LANGUAGE.md`; `05_OPERATOR_OWNERSHIP.md`; ADR-0001, Decision 2 |
| `TRACE-000049` | ORIENT | `01_UNIVERSAL_BASE_LANGUAGE.md`; `05_OPERATOR_OWNERSHIP.md` |
| `TRACE-000050` | EXPLAIN | `01_UNIVERSAL_BASE_LANGUAGE.md`; `05_OPERATOR_OWNERSHIP.md` |
| `TRACE-000051` | Canonical process | `01_UNIVERSAL_BASE_LANGUAGE.md`, Canonical universal process |
| `TRACE-000052` | Universal boundaries | `01_UNIVERSAL_BASE_LANGUAGE.md`, Universal boundary conditions |
| `TRACE-000053` | Universal inheritance | `01_UNIVERSAL_BASE_LANGUAGE.md`, Universal inheritance; `04_PROFILE_COMPOSITION.md` |
| `TRACE-000054` | Concept/declaration distinction | `02_CONCEPTS_AND_DECLARATIONS.md`, Architectural rule and omission rule |
| `TRACE-000055` | Base expression | `01_UNIVERSAL_BASE_LANGUAGE.md`; `02_CONCEPTS_AND_DECLARATIONS.md`; `04_PROFILE_COMPOSITION.md`, active-profile reporting boundary |
| `TRACE-000056` | Universal errors | `02_CONCEPTS_AND_DECLARATIONS.md`, omission rule; `04_PROFILE_COMPOSITION.md`, conflict detection; `06_INFORMATIVE_COMPONENTS.md`, boundaries |
| `TRACE-000057` | Normative summary | `01_UNIVERSAL_BASE_LANGUAGE.md`; `09_CANONICAL_ARCHITECTURE.md` |
| `TRACE-000058` | Concept registry | `01_UNIVERSAL_BASE_LANGUAGE.md`, Universal concepts; `08_NORMATIVE_CLASSIFICATION.md` |
| `TRACE-000059` | Boundary matrix | `01_UNIVERSAL_BASE_LANGUAGE.md`, Universal boundary conditions |

## D.3 Requirement coverage

Requirement IDs `OLS1-REQ-0001` through `OLS1-REQ-0103` are governed by the Trace ID of their containing normative clause. Requirement-to-test mappings belong to OLS-5.

---

## End of OLS-1
