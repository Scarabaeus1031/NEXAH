# Orientation Language Specification — OLS-4

## Derivations and Semantic Transitions

| Metadata field | Value |
| --- | --- |
| Document ID | `OLS-4` |
| Edition | 1 |
| Suite version | `1.0.0` |
| Document revision | `1.0.0` |
| Status | Version 1.0 publication candidate |
| Publication date | 17 July 2026 |
| Language | English |
| Normative scope | Derivation rules, semantic products, semantic transitions, outcome admission, recording eligibility, learning eligibility, and prohibited derivations |
| Replaces | Phase 2D derivation and validation/outcome summaries upon suite publication |
| Normative dependencies | `OLS-0`, `OLS-1`, `OLS-2`, `OLS-3` |
| Forward reference | `OLS-5` for conformance procedures and tests |
| Release manifest identifier | Pending assignment at suite publication |
| Persistent citation identifier | Unassigned |
| Architecture baseline | Phase 2D Canonical Architecture, frozen by ADR-0001 |

## Status of this document

OLS-4 is the authoritative Version 1.0 specification of derivations and semantic transitions. Clauses 1 through 15 and Annexes A, B, and C are **Normative**. Annexes D, E, and F are **Informative**.

OLS-4 does not redefine concepts, declarations, primitive operator contracts, profiles, or ownership established by OLS-1 through OLS-3. A semantic product is an output or status governed by existing semantics; registration as a product does not create a primitive concept or operator.

---

## 1 Scope

*Stable clause ID: `OLS4-CLS-0001` — Trace ID: `TRACE-000123` — Normative*

OLS-4 specifies:

- the common derivation model;
- eleven semantic products;
- eighteen accepted derivation rules;
- eighteen conditional derivation rules;
- legal product transitions;
- the cross-profile order for transformation, candidate outcome, validation, admission, recording, and learning;
- prohibited derivations and transition failures.

`[OLS4-REQ-0001]` OLS-4 shall preserve every semantic responsibility and boundary defined by OLS-1 through OLS-3.

`[OLS4-REQ-0002]` OLS-4 shall not introduce a universal concept, declaration, primitive operator, semantic profile, or semantic owner.

`[OLS4-REQ-0003]` A derivation or transition shall be valid only under its registered prerequisites, declarations, conditions, preservation rules, and non-implications.

`[OLS4-REQ-0004]` A semantic sequence shall not be interpreted as implementation scheduling, causality, external execution, or empirical proof.

## 2 Normative references

*Stable clause ID: `OLS4-CLS-0002` — Trace ID: `TRACE-000124` — Normative*

The following documents are normatively indispensable:

- `OLS-0`, *Specification Conventions and Suite Overview*, Edition 1;
- `OLS-1`, *Universal Base Language*, Edition 1;
- `OLS-2`, *Declarations and Operator Contracts*, Edition 1;
- `OLS-3`, *Semantic Profiles and Composition*, Edition 1.

`[OLS4-REQ-0005]` Terms, declarations, operators, profiles, activation, dependencies, and ownership shall resolve to their authoritative registries in OLS-1 through OLS-3.

## 3 Terms and derivation model

*Stable clause ID: `OLS4-CLS-0003` — Trace ID: `TRACE-000125` — Normative*

For OLS-4:

- **derivation** means a bounded semantic rule by which declared inputs and an identified operation or relation support a derived distinction;
- **accepted derivation** means one of the eighteen rules that applies when its registered prerequisites and declarations hold, without requiring an unregistered profile;
- **conditional derivation** means one of the eighteen rules that applies only when its registered profile, criteria, prerequisites, and declarations hold;
- **semantic product** means a declared output or status produced under existing concept, operator, or profile semantics;
- **semantic transition** means a permitted change from one declared product or status to another under a registered rule;
- **admission** means the Evidence/Validation-owned status transition from candidate outcome to admitted outcome after declared conditions are satisfied;
- **preservation** means retention of source, declarations, provenance, evidence class, uncertainty, and prior status wherever relevant to a derived product;
- **prohibited derivation** means a semantic implication that remains invalid regardless of composition or precedence.

A derivation record consists of: identified inputs; applicable operator or relation; applicable declarations; prerequisites; output distinction; preservation obligations; non-implications; status; and source trace.

`[OLS4-REQ-0006]` A derivation shall identify its source inputs and applicable operation or relation.

`[OLS4-REQ-0007]` A derivation shall preserve all applicable OLS-2 declarations and source statuses.

`[OLS4-REQ-0008]` Absence of a stated non-implication shall not authorize that implication.

`[OLS4-REQ-0009]` An accepted derivation shall not be treated as universal truth; its applicability remains bounded by its prerequisites.

`[OLS4-REQ-0010]` A conditional derivation shall not apply when any registered condition, profile, criterion, prerequisite, or declaration is absent.

`[OLS4-REQ-0011]` Historical labels that are not registered OLS-3 Profile IDs shall not activate a semantic profile.

`[OLS4-REQ-0012]` The labels `Research`, `Trajectory`, `Transition`, `Construction`, and `Culture`, where retained in Annex B as source conditions, shall be treated as recorded domain or criteria conditions, not as Version 1.0 semantic profiles.

## 4 Semantic product model

*Stable clause ID: `OLS4-CLS-0004` — Trace ID: `TRACE-000126` — Normative*

Annex A registers exactly eleven products. A Product ID identifies a product without changing the underlying OLS-1 concept, OLS-2 operator output, or OLS-3 profile ownership.

`[OLS4-REQ-0013]` Every product shall have exactly one semantic owner.

`[OLS4-REQ-0014]` Every product shall retain its originating inputs, applicable declarations, provenance, evidence class, uncertainty, and status.

`[OLS4-REQ-0015]` A product shall not acquire the status of another product except through a legal transition in Annex B.

`[OLS4-REQ-0016]` An explanation produced by EXPLAIN remains governed by OLS-2 and is not an additional OLS-4 semantic product.

### 4.1 Observation

*Stable clause ID: `OLS4-CLS-0005` — Product ID: `PRODUCT-OBSERVATION` — Trace ID: `TRACE-000127` — Normative*

An observation product is an OLS-1 observation produced by `OP-OBSERVE`. It is owned by the Universal Base Language, is admissible when OLS-2 OBSERVE preconditions hold, and preserves source, provenance, context, time, evidence class where assigned, uncertainty, and unsupported status. It does not imply truth, evidence, causality, recommendation, validation, or outcome.

`[OLS4-REQ-0017]` Observation product status shall not be promoted solely because the product enters a later derivation.

### 4.2 Representation

*Stable clause ID: `OLS4-CLS-0006` — Product ID: `PRODUCT-REPRESENTATION` — Trace ID: `TRACE-000128` — Normative*

A representation product is an OLS-1 representation produced by `OP-REPRESENT`. It is owned by the Universal Base Language, depends on declared inputs, context, construction perspective, representation type, and applicable status, and preserves its source relation. It does not imply reality, completeness, causal mechanism, or validation.

`[OLS4-REQ-0018]` A representation product shall remain distinguishable from its source and from reality.

### 4.3 Comparison finding

*Stable clause ID: `OLS4-CLS-0007` — Product ID: `PRODUCT-COMPARISON-FINDING` — Trace ID: `TRACE-000129` — Normative*

A comparison finding is the output of `OP-COMPARE`: recorded differences, agreements, or mismatches among compatible declared items relative to a declared basis. It is owned by the Universal Base Language and preserves item identities, basis, declarations, evidence, provenance, uncertainty, and disagreement. It does not imply cause, preference, selection, validation, prediction, or universal law.

`[OLS4-REQ-0019]` A comparison finding shall identify every compared item and the comparison basis.

### 4.4 Orientation finding

*Stable clause ID: `OLS4-CLS-0008` — Product ID: `PRODUCT-ORIENTATION-FINDING` — Trace ID: `TRACE-000130` — Normative*

An orientation finding is a bounded finding contained in an orientation produced by `OP-ORIENT`. It is owned by the Universal Base Language and depends on declared representation, context, perspective, applicable position, evidence, provenance, uncertainty, and limitations. It does not imply recommendation, authorization, execution, outcome, learning, control, or certainty.

`[OLS4-REQ-0020]` An orientation finding shall preserve supported, unsupported, disputed, uncertain, and limited status as distinct.

### 4.5 Selection result

*Stable clause ID: `OLS4-CLS-0009` — Product ID: `PRODUCT-SELECTION-RESULT` — Trace ID: `TRACE-000131` — Normative*

A selection result is the output of `OP-SELECT`: one or more alternatives selected under a declared basis or constraint. It is owned by the Navigation Profile, depends on that active profile and its Representation dependency, and preserves alternatives, basis, constraint, declarations, evidence, provenance, uncertainty, and relevant unselected alternatives. It does not imply recommendation, authority, execution, or optimality.

`[OLS4-REQ-0021]` Selection result status shall remain selection status unless a separately owned operation establishes another status.

### 4.6 Transformation result

*Stable clause ID: `OLS4-CLS-0010` — Product ID: `PRODUCT-TRANSFORMATION-RESULT` — Trace ID: `TRACE-000132` — Normative*

A transformation result is the resulting form or state produced by `OP-TRANSFORM`. It is owned by the Transformation Profile and preserves the distinction between input and result, transformation description, identity criterion, time order, scale, representation type, provenance, evidence class, uncertainty, and constraint as applicable. It does not imply improvement, stability, validation, outcome admission, authorization, or execution success.

`[OLS4-REQ-0022]` A transformation result shall not be treated as a candidate outcome until the conditions of Clause 8 are satisfied.

### 4.7 Validation result

*Stable clause ID: `OLS4-CLS-0011` — Product ID: `PRODUCT-VALIDATION-RESULT` — Trace ID: `TRACE-000133` — Normative*

A validation result is the status produced by `OP-VALIDATE` for a declared subject tested against declared criteria and evidence. It is owned by the Evidence/Validation Profile and preserves subject, criteria, scope, evidence class, provenance, uncertainty, and applicable declarations. It does not imply causality, universality, authority, canonical status, publication, truth, or outcome admission.

`[OLS4-REQ-0023]` A validation result shall remain linked to its subject, criteria, evidence, and declared scope.

### 4.8 Candidate outcome

*Stable clause ID: `OLS4-CLS-0012` — Product ID: `PRODUCT-CANDIDATE-OUTCOME` — Trace ID: `TRACE-000134` — Normative*

A candidate outcome is an observed post-transformation state associated with the declared subject under compatible identity and later time and marked with candidate status. It is owned by the Evidence/Validation Profile. No new primitive operator originates it: `OP-OBSERVE` supplies the post-transformation observation and the profile supplies candidate status. It preserves pre- and post-transformation references, identity criterion, time, provenance, evidence class, uncertainty, and candidate status. It does not imply validation, admission, improvement, causality, or learning.

`[OLS4-REQ-0024]` A transformation result alone shall not constitute a candidate outcome.

`[OLS4-REQ-0025]` Candidate status shall require a post-transformation observation with identity, later time, provenance, evidence class, and uncertainty status.

### 4.9 Admitted outcome

*Stable clause ID: `OLS4-CLS-0013` — Product ID: `PRODUCT-ADMITTED-OUTCOME` — Trace ID: `TRACE-000135` — Normative*

An admitted outcome is a candidate outcome assigned admitted status after it satisfies declared validation and admission conditions. It is owned by the Evidence/Validation Profile. Admission is a status transition, not an operator. It preserves the candidate observation, validation result, criteria, identity, time, provenance, evidence class, uncertainty, and remaining limitations. It does not imply improvement, authority, publication, universal proof, or learning.

`[OLS4-REQ-0026]` Outcome admission shall not occur solely from observation, transformation, validation status, approval, or persistence.

### 4.10 Recorded experience

*Stable clause ID: `OLS4-CLS-0014` — Product ID: `PRODUCT-RECORDED-EXPERIENCE` — Trace ID: `TRACE-000136` — Normative*

A recorded experience is an admitted outcome stored by `OP-RECORD` with its declarations and statuses intact. It is owned by the Memory/Learning Profile and depends conditionally on the Evidence/Validation Profile because admitted outcome semantics are used. It preserves admission and validation status, identity, time, provenance, evidence class, uncertainty, context, and representation type as applicable. It does not imply learning, canonical status, publication, or universal truth.

`[OLS4-REQ-0027]` A record of an unvalidated observation shall not be identified as recorded experience.

### 4.11 Learned knowledge

*Stable clause ID: `OLS4-CLS-0015` — Product ID: `PRODUCT-LEARNED-KNOWLEDGE` — Trace ID: `TRACE-000137` — Normative*

Learned knowledge is the derived change produced in the Memory/Learning Profile by comparing admitted recorded experience with prior memory or knowledge and recording the resulting change. It has no additional primitive operator; its derivation references `OP-COMPARE` and `OP-RECORD`. It preserves the admitted source experience, prior state, comparison basis, resulting change, identity, time, provenance, evidence class, uncertainty, and limitations. It does not imply certainty, universality, transfer to another context, or truth beyond its evidence and scope.

`[OLS4-REQ-0028]` Learned knowledge shall require admitted outcome, recorded experience, prior memory or knowledge, an explicit comparison, and a recorded resulting change.

`[OLS4-REQ-0029]` Persistence alone shall not establish learned knowledge.

## 5 Accepted derivations

*Stable clause ID: `OLS4-CLS-0016` — Trace ID: `TRACE-000138` — Normative*

Annex B.2 registers exactly eighteen accepted derivations: comparison, signal, perception, coordinate, slice, model, map, structure, system, direction, change, motion, transformation, block, route, navigation, journey, and operator.

`[OLS4-REQ-0030]` An accepted derivation shall apply only when every input, declaration, operator or relation, and prerequisite in its registry row is present.

`[OLS4-REQ-0031]` The output distinction of an accepted derivation shall not imply any status listed in that row’s non-implications.

`[OLS4-REQ-0032]` An accepted derivation shall preserve its source terms and shall not redefine them.

## 6 Conditional derivations

*Stable clause ID: `OLS4-CLS-0017` — Trace ID: `TRACE-000139` — Normative*

Annex B.3 registers exactly eighteen conditional derivations: information, interpretation, meaning, knowledge, layer, continuity, stability, emergence, flow, potential, possibility, recurrence, pattern, boundary, threshold, path, bridge, and composition.

`[OLS4-REQ-0033]` A conditional derivation shall be unavailable unless all registered conditions are explicit.

`[OLS4-REQ-0034]` Where a registry row names an OLS-3 profile, that profile shall be active and its dependencies resolved.

`[OLS4-REQ-0035]` Where a registry row preserves a historical domain label not registered by OLS-3, that label shall supply no profile semantics or activation.

`[OLS4-REQ-0036]` A conditional derivation shall report the criteria by which its derived distinction was recognized.

## 7 Semantic transition model

*Stable clause ID: `OLS4-CLS-0018` — Trace ID: `TRACE-000140` — Normative*

A legal semantic transition connects compatible products through an existing operator, derivation, or profile-owned status rule. Annex B.1 is the authoritative transition matrix.

`[OLS4-REQ-0037]` Transition order shall matter whenever identity, time, validation, admission, or learning status depends on order.

`[OLS4-REQ-0038]` A transition shall preserve the source product and shall not overwrite prior status.

`[OLS4-REQ-0039]` A product may enter a later operation only when its type, status, declarations, context, perspective, identity, time, scale, and representation basis are compatible as applicable.

`[OLS4-REQ-0040]` Optional transitions shall not be inferred from adjacency in an example chain.

`[OLS4-REQ-0041]` `PRODUCT-VALIDATION-RESULT` shall not transition to `PRODUCT-CANDIDATE-OUTCOME`; candidate status precedes outcome validation in the experiential sequence.

## 8 Outcome admission

*Stable clause ID: `OLS4-CLS-0019` — Trace ID: `TRACE-000141` — Normative*

The canonical experiential order is:

`PRODUCT-OBSERVATION` → optional `PRODUCT-TRANSFORMATION-RESULT` → `PRODUCT-CANDIDATE-OUTCOME` → `PRODUCT-VALIDATION-RESULT` → `PRODUCT-ADMITTED-OUTCOME` → `PRODUCT-RECORDED-EXPERIENCE` → `PRODUCT-LEARNED-KNOWLEDGE`.

`[OLS4-REQ-0042]` Candidate outcome and admitted outcome shall be owned by `PROFILE-EVIDENCE-VALIDATION`.

`[OLS4-REQ-0043]` Candidate outcome shall be an observed post-transformation state with compatible identity and later time.

`[OLS4-REQ-0044]` Admission shall require an identifiable candidate outcome, applicable validation result, declared validation and admission conditions, supporting evidence with provenance, and preserved uncertainty.

`[OLS4-REQ-0045]` Admission shall be a status transition and shall not invoke or imply an additional primitive operator.

`[OLS4-REQ-0046]` Admission shall preserve both candidate and validation status rather than replacing their history.

`[OLS4-REQ-0047]` `OP-APPROVE` shall not perform outcome admission.

`[OLS4-REQ-0048]` Admitted status shall not imply improvement, desired effect, authority, publication, or universal proof.

## 9 Recording eligibility

*Stable clause ID: `OLS4-CLS-0020` — Trace ID: `TRACE-000142` — Normative*

`OP-RECORD` may store a declared observation or admitted outcome under OLS-2. Only a stored admitted outcome constitutes `PRODUCT-RECORDED-EXPERIENCE`.

`[OLS4-REQ-0049]` Recording shall require identifiable material, identity, time, provenance and status, and all applicable declarations.

`[OLS4-REQ-0050]` Recording shall preserve the recorded material’s validation, admission, evidence, provenance, and uncertainty status.

`[OLS4-REQ-0051]` Recording shall not upgrade an observation to evidence, a candidate to an admitted outcome, a record to canonical status, or persistence to learning.

`[OLS4-REQ-0052]` An observation may be recorded without validation, but the record shall retain its unvalidated status and shall not become recorded experience by default.

## 10 Learning eligibility

*Stable clause ID: `OLS4-CLS-0021` — Trace ID: `TRACE-000143` — Normative*

Learning is a derived Memory/Learning Profile process, not a primitive operator. Its eligible inputs are admitted recorded experience and prior memory or knowledge.

`[OLS4-REQ-0053]` Experiential learning shall require a validated and admitted outcome.

`[OLS4-REQ-0054]` Experiential learning shall require recording of the admitted outcome, explicit comparison with prior memory or knowledge, and recording of the resulting change.

`[OLS4-REQ-0055]` Learning shall preserve evidence class, provenance, uncertainty, disagreements, limitations, identity, time, and the prior state.

`[OLS4-REQ-0056]` A simulated, inferred, proposed, or merely persisted result shall not be presented as observed experiential learning.

`[OLS4-REQ-0057]` Learned knowledge shall remain bounded to the declared context, perspective, representation, evidence, identity, time, scale, and uncertainty.

## 11 Prohibited derivations

*Stable clause ID: `OLS4-CLS-0022` — Trace ID: `TRACE-000144` — Normative*

Annex C is the authoritative prohibited derivation registry.

`[OLS4-REQ-0058]` No prohibited derivation shall become legal through sequencing, profile composition, explanation, repetition, approval, implementation output, or precedence.

`[OLS4-REQ-0059]` A prohibited derivation shall remain prohibited even when its source product is complete or its originating operator succeeds.

`[OLS4-REQ-0060]` A separately governed operation may establish only the status within its own contract and shall not retroactively legalize an earlier prohibited implication.

## 12 Transition failure model

*Stable clause ID: `OLS4-CLS-0023` — Trace ID: `TRACE-000145` — Normative*

| Failure class | Condition | Consequence |
| --- | --- | --- |
| Incomplete transition | A required input, declaration, criterion, profile, dependency, preserved status, or prerequisite is missing. | The target product or status may not be claimed complete. |
| Malformed transition | Types, declarations, identity, time, scale, ownership, or statuses are incompatible or silently collapsed. | The target claim is invalid. |
| Unsupported transition | The transition is explicit but evidence or criteria do not support the target status. | Unsupported status and uncertainty remain explicit; no status promotion occurs. |
| Invalid semantic jump | No Annex B transition or registered derivation supports the asserted source-to-target change. | The target status shall not be claimed. |
| Skipped mandatory state | A sequence requiring candidate, validation, admission, recording, or comparison bypasses that state. | Every dependent later state is incomplete or malformed as applicable. |
| Prohibited derivation | Annex C forbids the implication. | The implication is invalid and cannot be repaired by precedence. |

`[OLS4-REQ-0061]` Failure shall be reported at the earliest unsupported or invalid transition.

`[OLS4-REQ-0062]` A later valid operation shall not erase an earlier failure or missing state.

`[OLS4-REQ-0063]` No precedence rule shall repair an illegal transition.

`[OLS4-REQ-0064]` OLS-5 shall define conformance procedures; OLS-4 defines only semantic failure conditions.

## 13 Rejected and analytical derivations

*Stable clause ID: `OLS4-CLS-0024` — Trace ID: `TRACE-000146` — Normative status boundary; records informative*

The generic derivations of `space` and `balance` remain rejected. The records for `difference`, `constraint`, `outcome`, `scale`, and `time` remain analytical reclassifications. They are not normative derivation rules.

`[OLS4-REQ-0065]` `space` and `balance` shall not receive one generic Version 1.0 derivation.

`[OLS4-REQ-0066]` Reclassification records shall not be used to derive the reclassified element.

`[OLS4-REQ-0067]` `difference`, `constraint`, `outcome`, `scale`, and `time` shall resolve to their OLS-1, OLS-2, or OLS-3 classifications.

## 14 Non-transformation cases

*Stable clause ID: `OLS4-CLS-0025` — Trace ID: `TRACE-000147` — Normative*

Validation may test an observation, representation, claim, model, change, or record without preceding transformation. Recording may preserve an observation without validation.

`[OLS4-REQ-0068]` Non-transformation validation shall retain subject, criteria, evidence class, provenance, uncertainty, and validation scope.

`[OLS4-REQ-0069]` Absence of transformation shall not remove validation prerequisites.

`[OLS4-REQ-0070]` A non-transformation validation result shall not become an admitted outcome unless the separately required candidate-outcome and admission conditions hold.

`[OLS4-REQ-0071]` A recorded but unvalidated observation shall retain observation status and shall not become experiential learning.

## 15 Cross-profile responsibility and summary

*Stable clause ID: `OLS4-CLS-0026` — Trace ID: `TRACE-000148` — Normative*

| Responsibility | Sole owner |
| --- | --- |
| Observation, representation, comparison finding, orientation finding | Universal Base Language |
| Selection result | Navigation Profile |
| Transformation result | Transformation Profile |
| Validation result, candidate outcome, admitted outcome | Evidence/Validation Profile |
| Recorded experience, learned knowledge | Memory/Learning Profile |
| Editorial approval | Editorial Governance Profile; separate from outcome admission |

`[OLS4-REQ-0072]` Cross-profile transition shall not transfer semantic ownership.

`[OLS4-REQ-0073]` The Evidence/Validation Profile shall be active when candidate, validation, or admitted outcome status is used.

`[OLS4-REQ-0074]` The Memory/Learning Profile shall be active when recorded experience or learned knowledge is claimed.

`[OLS4-REQ-0075]` The complete Version 1.0 derivation architecture consists of the registries and rules in OLS-4; examples shall not add transitions.

---

# Annex A — Semantic Product Registry

*Annex ID: `OLS4-ANNEX-A` — Trace ID: `TRACE-000149` — Normative*

| Product ID | Product | Owner | Origin | Dependencies | Principal prohibited implications |
| --- | --- | --- | --- | --- | --- |
| `PRODUCT-OBSERVATION` | observation | Universal Base Language | `OP-OBSERVE` | OLS-1/OLS-2 | truth; evidence; causality; outcome |
| `PRODUCT-REPRESENTATION` | representation | Universal Base Language | `OP-REPRESENT` | observation/data; declarations | reality; completeness; validation |
| `PRODUCT-COMPARISON-FINDING` | comparison finding | Universal Base Language | `OP-COMPARE` | compatible items; basis | causality; preference; validation |
| `PRODUCT-ORIENTATION-FINDING` | orientation finding | Universal Base Language | `OP-ORIENT` | representation; evidence/status | recommendation; authority; execution; outcome |
| `PRODUCT-SELECTION-RESULT` | selection result | Navigation | `OP-SELECT` | active Navigation and Representation | recommendation; authority; optimality |
| `PRODUCT-TRANSFORMATION-RESULT` | transformation result | Transformation | `OP-TRANSFORM` | active Transformation | improvement; validation; admitted outcome |
| `PRODUCT-VALIDATION-RESULT` | validation result | Evidence/Validation | `OP-VALIDATE` | subject; criteria; evidence/status | truth; authority; admission |
| `PRODUCT-CANDIDATE-OUTCOME` | candidate outcome | Evidence/Validation | post-transformation `OP-OBSERVE` plus candidate status | observed later state; identity/time | validation; admission; improvement |
| `PRODUCT-ADMITTED-OUTCOME` | admitted outcome | Evidence/Validation | admission status transition | candidate plus validation/admission conditions | improvement; authority; learning |
| `PRODUCT-RECORDED-EXPERIENCE` | recorded experience | Memory/Learning | `OP-RECORD` | admitted outcome | learning; canonical status; truth |
| `PRODUCT-LEARNED-KNOWLEDGE` | learned knowledge | Memory/Learning | derived `OP-COMPARE` plus `OP-RECORD` | admitted recorded experience; prior memory/knowledge | certainty; universality; transfer |

`[OLS4-REQ-0076]` Annex A shall contain exactly eleven Product IDs and one owner for each.

# Annex B — Semantic Transition Matrix

*Annex ID: `OLS4-ANNEX-B` — Trace ID: `TRACE-000150` — Normative*

## B.1 Product transitions

| Transition ID | Source input | Governing operation or rule | Target product | Conditions | Status |
| --- | --- | --- | --- | --- | --- |
| `TRANSITION-001` | source material | `OP-OBSERVE` | observation | OLS-2 contract | Legal |
| `TRANSITION-002` | observation/data | `OP-REPRESENT` | representation | type, context, perspective, provenance/status | Legal |
| `TRANSITION-003` | two or more compatible items, including representations | `OP-COMPARE` | comparison finding | declared basis and compatibility | Legal |
| `TRANSITION-004` | representation and comparison findings with orientation inputs | `OP-ORIENT` | orientation finding | context, perspective, evidence/status, uncertainty | Legal |
| `TRANSITION-005` | declared alternatives, optionally supported by orientation | `OP-SELECT` | selection result | active Navigation; basis/constraint; Representation dependency | Conditional legal |
| `TRANSITION-006` | declared form/state, optionally a selection result | `OP-TRANSFORM` | transformation result | active Transformation; description; input/output identity/time | Conditional legal |
| `TRANSITION-007` | transformation result | post-transformation `OP-OBSERVE` plus candidate status | candidate outcome | same declared identity, later time, provenance, evidence class, uncertainty | Conditional legal |
| `TRANSITION-008` | claim, model, change, observation, representation, record, or candidate outcome | `OP-VALIDATE` | validation result | active Evidence/Validation; criteria; evidence/status | Conditional legal |
| `TRANSITION-009` | candidate outcome plus applicable validation result | admission status transition | admitted outcome | declared validation and admission conditions satisfied | Conditional legal |
| `TRANSITION-010` | admitted outcome | `OP-RECORD` | recorded experience | active Memory/Learning; identity, time, provenance/status | Conditional legal |
| `TRANSITION-011` | recorded experience plus prior memory/knowledge | derived compare-and-record process | learned knowledge | admitted source; comparison basis; resulting change recorded | Conditional legal |
| `TRANSITION-012` | observation | `OP-RECORD` | recorded observation, not recorded experience | status preserved; no validation or learning implication | Legal outside Product Registry target set |
| `TRANSITION-013` | validation result | none | candidate outcome | candidate must precede outcome validation | Prohibited |

## B.2 Accepted derivation registry

| Derivation ID | Derived distinction | Inputs | Operator/relation and declarations | Output boundary / non-implications |
| --- | --- | --- | --- | --- |
| `DERIVATION-A01` | comparison | difference; two or more declared items | COMPARE; basis; compatible context/time/scale/type | differences, agreements, mismatches; not cause, preference, validation |
| `DERIVATION-A02` | signal | observation; context | OBSERVE; source/status and time where relevant | captured event/data as process input; not evidence, meaning, truth |
| `DERIVATION-A03` | perception | observer; observation; perspective; context | OBSERVE; observer and perspective declarations | reception/organization of observed; not objective reality or evidence |
| `DERIVATION-A04` | coordinate | position; representation | REPRESENT; position, representation type, scale | locator in declared representation; not physical location or cross-type equivalence |
| `DERIVATION-A05` | slice | representation; perspective; context | REPRESENT; type and scale | explicitly partial view/form; not complete map or reality |
| `DERIVATION-A06` | model | observation; representation; relation; state | REPRESENT; type, context, provenance | structured analytical/comparison form; not reality, mechanism, validation |
| `DERIVATION-A07` | map | representation; relation; position; coordinate | REPRESENT; relations/positions, map type, scale, perspective | arranged representation; not territory, complete model, valid route |
| `DERIVATION-A08` | structure | relation; representation; difference | REPRESENT/COMPARE; representation type | organized relations/form; not mechanism, stability, universality |
| `DERIVATION-A09` | system | structure; relation; state; context | REPRESENT; boundary/type and scale | organized interacting elements in context; not autonomy, control, completeness |
| `DERIVATION-A10` | direction | two or more positions; relation; time | COMPARE; identity, temporal order, scale | ordered heading/tendency; not route, intention, recommendation |
| `DERIVATION-A11` | change | two states; difference; transition | COMPARE; identity and time | difference between ordered states; not cause, improvement, mechanism |
| `DERIVATION-A12` | motion | change; position; direction; state | COMPARE; identity, time, scale, representation type | change of position/state over time; not agency, purpose, flow law |
| `DERIVATION-A13` | transformation | state/form; transition | TRANSFORM; input/output identity and time | process changing form/state/relation/representation; not improvement, validation, stability |
| `DERIVATION-A14` | block | constraint; path/transition; representation | COMPARE under constraint; reachability basis; Navigation active | prevented transition/unreachable region; not permanent impossibility or cause |
| `DERIVATION-A15` | route | path; possibility; constraint | SELECT; basis and authority where needed; Navigation active | selected/described path; not optimal path, recommendation, execution |
| `DERIVATION-A16` | navigation | map/representation; position; route/path; orientation | ORIENT + SELECT; target/question, constraints, scale; Navigation active | movement/selection through representation; not decision quality, authorization, success |
| `DERIVATION-A17` | journey | path; states; transition; perspective | EXPLAIN; human/reader identity and time; Education or Editorial use | human/editorial sequence; not universal path or measured trajectory |
| `DERIVATION-A18` | operator | named operation and its contract | typed distinction over evidenced operations | operation category; not human role, mathematical validity, universal mechanism |

## B.3 Conditional derivation registry

| Derivation ID | Derived distinction | Inputs | Operator/relation and conditions | Output boundary / non-implications |
| --- | --- | --- | --- | --- |
| `DERIVATION-C01` | information | signal; representation; difference; context | REPRESENT; type and provenance; organization criteria | organized signals/differences; not knowledge, meaning, causality |
| `DERIVATION-C02` | interpretation | information; context; perspective; relation | ORIENT; reading perspective and position | situated reading; not truth, consensus, evidence |
| `DERIVATION-C03` | meaning | interpretation; difference; relation; context | ORIENT/EXPLAIN; reader/cultural context; Education where active | attributed significance; not universal significance or proof |
| `DERIVATION-C04` | knowledge | information; meaning; evidence; provenance; orientation | ORIENT and optionally RECORD; evidence class | structured understanding or recorded editorial content; not certainty or canonical status |
| `DERIVATION-C05` | layer | representation/structure; relation; scale | REPRESENT; ordering or containment criterion | declared stratum; not ontological level or independence |
| `DERIVATION-C06` | continuity | identity; ordered states; relation; time | COMPARE across interval; observation coverage criterion | retained relation/form without observed break; not absence of gaps or stability |
| `DERIVATION-C07` | stability | continuity; state; transition; constraint | COMPARE/VALIDATE; interval, perturbation/test criteria; Evidence/Validation active for VALIDATE | persistence/order under declared change; not permanence, balance, safety |
| `DERIVATION-C08` | emergence | earlier/later states; structure; difference; transformation | COMPARE; identity, time, novelty criteria; `Research` retained as domain label only | later structure not admitted earlier; not spontaneous cause or universal law |
| `DERIVATION-C09` | flow | ordered transitions; direction; relation | COMPARE; identity, time, scale, type; `Trajectory/Research` retained as domain labels | ordered movement/change; not continuity, conserved quantity, causal transport |
| `DERIVATION-C10` | potential | state; transition; constraint; representation | ORIENT; candidate-state/reachability criteria; Navigation where active; `Research` domain label retained | unrealized capacity/candidate state; not probability, reachability, prediction |
| `DERIVATION-C11` | possibility | potential; constraint; representation | ORIENT; admissibility criteria; Navigation active | available candidate before selection; not feasibility, recommendation, outcome |
| `DERIVATION-C12` | recurrence | observations/states; comparison; identity; time; scale | repeated COMPARE; recurrence basis | repeated similarity/return; not same cause or universal law |
| `DERIVATION-C13` | pattern | recurrence; structure; comparison | COMPARE/REPRESENT; pattern criterion and scale | recurring arrangement; not law, cause, proof |
| `DERIVATION-C14` | boundary | difference; relation; representation; constraint | REPRESENT/COMPARE; classification or constraint rule; Representation or Navigation as applicable | separation/interface; not wall, mechanism, impermeability |
| `DERIVATION-C15` | threshold | boundary; transition; constraint | COMPARE; crossing condition, scale/time; `Transition` retained as domain label only | salient crossing condition/point; not gate, prediction, action |
| `DERIVATION-C16` | path | relation; position/state; transition | REPRESENT ordered relations; identity, order/time, type; Navigation where active; `Trajectory` domain label retained | possible/observed sequence; not selected route or recommendation |
| `DERIVATION-C17` | bridge | differentiated sides/boundary; relation; path | REPRESENT or TRANSFORM; connection/crossing criteria; Navigation where active; `Construction` domain label retained | connector/passage; not causal mechanism or safe crossing |
| `DERIVATION-C18` | composition | elements/operators; relation; time/order | REPRESENT; ordered relation and context | combined ordered meaning/structure; not valid grammar or causal process |

`[OLS4-REQ-0077]` Annex B shall contain exactly eighteen accepted and eighteen conditional derivation records.

# Annex C — Prohibited Derivation Registry

*Annex ID: `OLS4-ANNEX-C` — Trace ID: `TRACE-000151` — Normative*

| Prohibition ID | Source | Prohibited target | Basis |
| --- | --- | --- | --- |
| `PROHIBITION-001` | observation | truth | OBSERVE does not establish truth. |
| `PROHIBITION-002` | observation | recommendation | Observation has no recommendation or authority status. |
| `PROHIBITION-003` | representation | reality | Representation is not reality. |
| `PROHIBITION-004` | comparison finding | causality | COMPARE identifies difference/agreement, not cause. |
| `PROHIBITION-005` | orientation finding | authority | ORIENT does not grant authority. |
| `PROHIBITION-006` | selection result | recommendation | SELECT does not establish recommendation. |
| `PROHIBITION-007` | transformation result | improvement | TRANSFORM establishes change, not improvement. |
| `PROHIBITION-008` | validation result | truth | Validation is criterion- and scope-bounded. |
| `PROHIBITION-009` | validation result | authority | VALIDATE does not grant authority. |
| `PROHIBITION-010` | approval status | reality | APPROVE changes governed status only. |
| `PROHIBITION-011` | recording | learning | RECORD alone does not establish learning. |
| `PROHIBITION-012` | learned knowledge | universal truth | Learning remains bounded by evidence, context, and uncertainty. |
| `PROHIBITION-013` | candidate outcome | admitted outcome without conditions | Candidate status is not admission. |
| `PROHIBITION-014` | validation result | candidate outcome | Candidate observation precedes outcome validation. |
| `PROHIBITION-015` | admitted outcome | improvement | Admission does not establish desirability. |
| `PROHIBITION-016` | approval status | outcome admission | Editorial authority does not own empirical admission. |
| `PROHIBITION-017` | possible path | authorized action | Possibility, selection, recommendation, authority, and execution remain separate. |
| `PROHIBITION-018` | model or simulation output | observed fact | Evidence class cannot be promoted by relabeling. |

`[OLS4-REQ-0078]` Every prohibition in Annex C shall apply to direct and composed derivations.

# Annex D — Example Derivation Chains

*Annex ID: `OLS4-ANNEX-D` — Trace ID: `TRACE-000152` — Informative*

## D.1 Universal orientation

Source readings are observed, represented, compared, oriented, and explained. The semantic products are observation, representation, comparison finding, and orientation finding; EXPLAIN communicates the orientation under OLS-2. No recommendation or authority follows.

## D.2 Selection and transformation

An orientation identifies alternatives. Navigation is activated, SELECT produces a selection result under a declared constraint, and Transformation is activated to produce a transformation result. Selection remains distinct from recommendation; transformation remains distinct from improvement and validation.

## D.3 Experiential outcome and learning

An initial state is observed. A transformation result is produced. A later observation of the same declared identity becomes a candidate outcome. VALIDATE produces a validation result. When declared admission conditions are satisfied, admitted status is assigned. RECORD produces recorded experience. Comparison with prior memory or knowledge and recording of the resulting change produces learned knowledge.

The candidate outcome occurs before the validation result. A chain placing validation before creation of the candidate outcome is not the canonical experiential sequence.

## D.4 Validation without transformation

A representation is tested against declared criteria and evidence. VALIDATE produces a validation result. No candidate outcome, admitted outcome, recorded experience, or learning follows merely from that result.

# Annex E — Illegal Transition Examples

*Annex ID: `OLS4-ANNEX-E` — Trace ID: `TRACE-000153` — Informative*

1. A sensor reading is called true because it was observed: `PROHIBITION-001`.
2. A diagram is treated as the territory it depicts: `PROHIBITION-003`.
3. A correlation found by COMPARE is asserted as a cause: `PROHIBITION-004`.
4. An orientation report is treated as permission to act: `PROHIBITION-005`.
5. SELECT chooses an option and labels it a recommendation: `PROHIBITION-006`.
6. A changed state is described as improved without criteria: `PROHIBITION-007`.
7. A passing validation status is presented as truth or authority: `PROHIBITION-008` and `PROHIBITION-009`.
8. Editorial approval is presented as empirical reality: `PROHIBITION-010`.
9. A stored record is called learned knowledge without admitted experience and comparison: `PROHIBITION-011`.
10. A local learning result is generalized as universal truth: `PROHIBITION-012`.
11. A validation result is used to create a candidate outcome retrospectively: `PROHIBITION-014`.
12. A simulated result is relabeled as an observed outcome: `PROHIBITION-018`.

# Annex F — Architectural Traceability

*Annex ID: `OLS4-ANNEX-F` — Trace ID: `TRACE-000154` — Informative*

| OLS-4 element | Frozen source | Incorporated evidence | Transformation |
| --- | --- | --- | --- |
| Common derivation model | Phase 2D `08_NORMATIVE_CLASSIFICATION.md`, `09_CANONICAL_ARCHITECTURE.md` | Phase 2B `07_DERIVATION_RULES.md` | Converted accepted/conditional status into normative registry form. |
| Eleven semantic products | Phase 2D universal, operator, profile, and validation/outcome architecture | OLS-1 concepts; OLS-2 outputs; OLS-3 owners | Added stable Product IDs as editorial identifiers; no primitive added. |
| Accepted derivations | Phase 2D canonical count and status | Phase 2B accepted rows 1–43 | Preserved 18 inputs, operations, declarations, outputs, and non-implications. |
| Conditional derivations | Phase 2D canonical count and status | Phase 2B conditional rows 1–43 | Preserved 18 conditions; non-OLS-3 historical labels were not converted to profiles. |
| Outcome and learning order | Phase 2D `07_VALIDATION_AND_OUTCOME.md` | Phase 2B typed dependencies and reconstruction graph | Formalized candidate-before-validation order and status transitions. |
| Recording and non-transformation cases | Phase 2D `07_VALIDATION_AND_OUTCOME.md` | OLS-2 RECORD and VALIDATE contracts | Preserved recording without learning and validation without transformation. |
| Prohibited derivations | Phase 2D boundaries; OLS-1/OLS-2 prohibited implications | Phase 2B derivation non-implications | Consolidated direct and composed prohibitions. |
| Rejected/reclassified boundary | Phase 2D `08_NORMATIVE_CLASSIFICATION.md` | Phase 2B rejected/reclassified rows | Retained outside normative derivation. |

The Product ID namespace and matrix presentation are specification-level editorial additions permitted by the Phase 3 Charter. They introduce no semantic owner, primitive, operator, declaration, profile, or derivation.

