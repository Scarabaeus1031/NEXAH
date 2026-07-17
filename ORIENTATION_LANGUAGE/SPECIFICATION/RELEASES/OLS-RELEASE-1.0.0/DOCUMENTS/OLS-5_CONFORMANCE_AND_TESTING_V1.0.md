# Orientation Language Specification — OLS-5

## Conformance and Testing

| Metadata field | Value |
| --- | --- |
| Document ID | `OLS-5` |
| Edition | 1 |
| Suite version | `1.0.0` |
| Document revision | `1.0.0` |
| Status | Version 1.0 publication candidate |
| Publication date | 17 July 2026 |
| Language | English |
| Normative scope | Conformance classes, targets, applicability, tests, evidence, reports, status aggregation, and certification boundaries |
| Normative dependencies | `OLS-0`, `OLS-1`, `OLS-2`, `OLS-3`, `OLS-4` |
| Forward reference | `OLS-6` for extension, version, and governance conformance |
| Release manifest identifier | Pending assignment at suite publication |
| Persistent citation identifier | Unassigned |
| Architecture baseline | Phase 2D Canonical Architecture, frozen by ADR-0001 |

## Status of this document

OLS-5 is the authoritative Version 1.0 conformance and testing specification. Clauses 1 through 14 and Annexes A, B, and C are **Normative**. Annexes D, E, and F are **Informative**.

OLS-5 verifies requirements defined by OLS-0 through OLS-4 and its own conformance requirements. It does not create, complete, validate, or modify the semantics being assessed.

---

## 1 Scope

*Stable clause ID: `OLS5-CLS-0001` — Trace ID: `TRACE-000155` — Normative*

OLS-5 specifies:

- six conformance classes;
- conformance targets and units;
- requirement applicability and coverage;
- normative test records and methods;
- PASS, FAIL, INCOMPLETE, UNSUPPORTED, and NOT APPLICABLE statuses;
- acceptable evidence and evidence boundaries;
- conformance report contents and aggregate results;
- certification boundaries and implementation neutrality.

`[OLS5-REQ-0001]` Conformance shall verify the applicable normative requirements of the declared suite version and claim scope.

`[OLS5-REQ-0002]` Conformance shall not introduce, remove, reinterpret, complete, or transfer semantic responsibility.

`[OLS5-REQ-0003]` A conformance claim shall identify one target, one Conformance ID, the suite version, and the tested scope.

`[OLS5-REQ-0004]` Informative text, examples, rationale, historical material, and implementation guidance shall not create a conformance obligation.

## 2 Normative references

*Stable clause ID: `OLS5-CLS-0002` — Trace ID: `TRACE-000156` — Normative*

The following documents are normatively indispensable:

- `OLS-0`, *Specification Conventions and Suite Overview*, Edition 1;
- `OLS-1`, *Universal Base Language*, Edition 1;
- `OLS-2`, *Declarations and Operator Contracts*, Edition 1;
- `OLS-3`, *Semantic Profiles and Composition*, Edition 1;
- `OLS-4`, *Derivations and Semantic Transitions*, Edition 1.

`[OLS5-REQ-0005]` A test shall use the controlling requirement text from the compatible release identified by the claim.

`[OLS5-REQ-0006]` An informative paraphrase shall not replace a controlling normative requirement as a test oracle.

## 3 Terms and conformance philosophy

*Stable clause ID: `OLS5-CLS-0003` — Trace ID: `TRACE-000157` — Normative*

For OLS-5:

- **conformance target** means the identified artifact, expression, composition, procedure, implementation, or specification being assessed;
- **conformance class** means a registered cumulative scope of normative parts;
- **conformance unit** means one identified clause, requirement, registry entry, normative annex, identifier, or cross-reference subject to assessment;
- **test** means a repeatable semantic or structural assessment identified by a Test ID;
- **test oracle** means the controlling normative requirement and referenced registries against which evidence is assessed;
- **applicability** means whether a requirement governs the declared target and claim scope;
- **evidence** means inspectable material sufficient to determine a test status;
- **conformance report** means the controlled record of scope, tests, evidence, statuses, failures, limitations, and aggregate result;
- **certification** means an attestation limited to the conformance scope and evidence identified by the report.

Conformance is semantic and structural verification. It is independent of implementation technology and does not confer truth, authority, usefulness, scientific validity, safety, performance, or successful execution.

`[OLS5-REQ-0007]` Every test shall preserve the normative/informative status of its source material.

`[OLS5-REQ-0008]` Passing evidence shall support only the tested requirement within the declared scope.

`[OLS5-REQ-0009]` The assessor shall not infer unclaimed capabilities or unreported semantic status.

`[OLS5-REQ-0010]` Human and software realizations shall be assessed against the same applicable semantic requirements.

## 4 Conformance targets

*Stable clause ID: `OLS5-CLS-0004` — Trace ID: `TRACE-000158` — Normative*

A target may be:

1. a language expression or orientation artifact;
2. a profile composition;
3. a repeatable human procedure;
4. a software implementation;
5. a profile specification or extension, when OLS-6 applies;
6. a specification document or suite release.

`[OLS5-REQ-0011]` The target shall have a stable identifier or an unambiguous report-local identifier.

`[OLS5-REQ-0012]` The claim shall identify the target type and the exact material included in assessment.

`[OLS5-REQ-0013]` A target shall claim only capabilities present in the declared scope.

`[OLS5-REQ-0014]` An implementation shall identify implemented profiles, operators, declarations, representation types, unsupported capabilities, and implementation mappings relevant to its claim.

`[OLS5-REQ-0015]` A human procedure shall provide repeatable evidence for the same semantic obligations as another realization of the claimed class.

`[OLS5-REQ-0016]` A profile composition shall identify all active profiles, activated dependencies, declarations, conflicts, and unsupported features.

## 5 Conformance classes

*Stable clause ID: `OLS5-CLS-0005` — Trace ID: `TRACE-000159` — Normative*

Annex A registers exactly six cumulative conformance classes.

`[OLS5-REQ-0017]` A class claim shall include every normative dependency registered for that class.

`[OLS5-REQ-0018]` A dependent class shall not mask a failure, incomplete result, or unsupported requirement in a dependency class.

`[OLS5-REQ-0019]` No profile-only conformance class shall exist in Version 1.0.

`[OLS5-REQ-0020]` Every semantic class from OLS-1 through OLS-4 shall include the complete OLS-1 Universal Base Language scope.

`[OLS5-REQ-0021]` `CONFORMANCE-OLS0` shall assess OLS-0 conventions and shall have no suite-internal dependency.

`[OLS5-REQ-0022]` `CONFORMANCE-OLS1` shall assess OLS-0 and OLS-1.

`[OLS5-REQ-0023]` `CONFORMANCE-OLS2` shall assess OLS-0 through OLS-2.

`[OLS5-REQ-0024]` `CONFORMANCE-OLS3` shall assess OLS-0 through OLS-3.

`[OLS5-REQ-0025]` `CONFORMANCE-OLS4` shall assess OLS-0 through OLS-4.

`[OLS5-REQ-0026]` `CONFORMANCE-FULL-SUITE` shall assess every applicable requirement in OLS-0 through OLS-5.

`[OLS5-REQ-0027]` A narrower class shall not be described as Full Suite conformance.

## 6 Conformance units and applicability

*Stable clause ID: `OLS5-CLS-0006` — Trace ID: `TRACE-000160` — Normative*

| Unit | Testability |
| --- | --- |
| Normative clause | Tested through its Requirement IDs and normative registry effects. |
| Requirement | Always mapped to at least one normative test. |
| Normative registry entry | Tested for presence, identity, uniqueness, ownership, values, and internal consistency as applicable. |
| Normative annex | Tested through its requirements and registry entries. |
| Stable identifier | Tested for syntax, uniqueness, resolution, preservation, and registry assignment as applicable. |
| Normative cross-reference | Tested for target resolution, compatible version, status, and ownership preservation. |
| Informative clause or annex | Not a conformance unit; may supply non-controlling test material. |

Applicability categories are: always applicable within class; conditionally applicable by declaration; active-profile applicable; invoked-operator applicable; used-derivation applicable; target-type applicable; and not applicable.

`[OLS5-REQ-0028]` Every normative Requirement ID in the claimed class shall receive one test status.

`[OLS5-REQ-0029]` Applicability shall be determined from the target type, class, active profiles, invoked operators, used derivations, declarations, and explicit claim scope.

`[OLS5-REQ-0030]` Undeclared scope shall not make a requirement not applicable.

`[OLS5-REQ-0031]` Conditional requirements shall be tested when their stated condition is true.

`[OLS5-REQ-0032]` A NOT APPLICABLE result shall identify the controlling condition and evidence that the condition is false.

`[OLS5-REQ-0033]` Informative material shall not receive a required PASS/FAIL test status.

`[OLS5-REQ-0034]` A normative registry entry referenced by an applicable requirement shall be included in that requirement’s test scope.

## 7 Requirement-to-test coverage

*Stable clause ID: `OLS5-CLS-0007` — Trace ID: `TRACE-000161` — Normative*

Annex B is the authoritative requirement-to-test matrix. The Version 1.0 mapping is one-to-one: `OLSx-REQ-nnnn` maps to `TEST-OLSx-nnnn`.

`[OLS5-REQ-0035]` Every normative Requirement ID in OLS-0 through OLS-5 shall map to at least one Test ID.

`[OLS5-REQ-0036]` Every Test ID shall map to at least one normative Requirement ID.

`[OLS5-REQ-0037]` A test mapping shall identify the controlling requirement, method, applicability basis, and expected condition.

`[OLS5-REQ-0038]` A requirement shall not be declared untestable; absence of sufficient evidence shall produce INCOMPLETE rather than remove the mapping.

`[OLS5-REQ-0039]` Changing a controlling requirement shall require review of every mapped test.

`[OLS5-REQ-0040]` A test shall not expand or narrow the semantic responsibility of its controlling requirement.

## 8 Normative test model

*Stable clause ID: `OLS5-CLS-0008` — Trace ID: `TRACE-000162` — Normative*

Every test record contains:

- Test ID;
- controlling Requirement ID;
- applicable Conformance IDs and target types;
- preconditions and applicability condition;
- test input and evidence references;
- test method;
- procedure;
- expected semantic or structural condition;
- prohibited outcomes;
- observed result;
- test status;
- assessor and date;
- suite and test-registry versions.

Normative methods are:

| Method ID | Purpose |
| --- | --- |
| `METHOD-DOCUMENT-INSPECTION` | Verify normative status, wording, structure, identifiers, citations, manifests, and editorial conventions. |
| `METHOD-IDENTIFIER-VERIFICATION` | Verify identifier syntax, uniqueness, registry ownership, preservation, and resolution. |
| `METHOD-REGISTRY-VERIFICATION` | Verify registry count, entries, ownership, dependencies, allowed values, and cross-registry consistency. |
| `METHOD-SEMANTIC-VERIFICATION` | Verify a semantic assertion, boundary, non-implication, declaration, or preserved status against declared evidence. |
| `METHOD-OPERATOR-VERIFICATION` | Verify inputs, declarations, preconditions, outputs, preservation, failure conditions, and prohibited implications. |
| `METHOD-PROFILE-VERIFICATION` | Verify activation, inheritance, dependencies, ownership, composition, conflicts, and reporting. |
| `METHOD-DERIVATION-VERIFICATION` | Verify prerequisites, conditions, products, transitions, non-implications, and forbidden jumps. |
| `METHOD-TRACE-VERIFICATION` | Verify forward and reverse trace resolution and compatible source status. |
| `METHOD-NEGATIVE-VERIFICATION` | Present or inspect an invalid case and verify its required rejection/status. |
| `METHOD-CONFORMANCE-VERIFICATION` | Verify class, applicability, test, evidence, report, status, and certification rules in OLS-5. |

`[OLS5-REQ-0041]` A test shall use one or more registered Method IDs.

`[OLS5-REQ-0042]` Test inputs shall declare every condition necessary to determine applicability and expected status.

`[OLS5-REQ-0043]` Expected output shall be expressed semantically or structurally and shall not prescribe implementation technology.

`[OLS5-REQ-0044]` A boundary requirement shall include a negative or prohibited-outcome check.

`[OLS5-REQ-0045]` An operator test shall assess the complete applicable OLS-2 contract, including failures and prohibited implications.

`[OLS5-REQ-0046]` A profile test shall assess the profile independently and its composition obligations collectively.

`[OLS5-REQ-0047]` A derivation test shall assess every registered prerequisite, condition, preservation rule, and non-implication.

`[OLS5-REQ-0048]` A test shall be repeatable from the evidence and procedure identified by its record.

`[OLS5-REQ-0049]` Equivalent evidence may be used across targets when it establishes the same normative condition without changing the oracle.

`[OLS5-REQ-0050]` An example or reference implementation may provide input but shall not define the expected result.

## 9 Conformance statuses and aggregation

*Stable clause ID: `OLS5-CLS-0009` — Trace ID: `TRACE-000163` — Normative*

Annex C is the authoritative status registry.

`[OLS5-REQ-0051]` PASS shall mean that sufficient evidence demonstrates satisfaction of the applicable requirement and no prohibited outcome occurred.

`[OLS5-REQ-0052]` FAIL shall mean that evidence demonstrates violation of an applicable requirement or occurrence of a prohibited outcome.

`[OLS5-REQ-0053]` INCOMPLETE shall mean that applicability is established but required evidence, execution, scope, or result is missing or indeterminate.

`[OLS5-REQ-0054]` UNSUPPORTED shall mean that the target explicitly lacks a capability required by the claimed scope.

`[OLS5-REQ-0055]` NOT APPLICABLE shall mean that the requirement’s controlling condition is demonstrably false for the declared target and scope.

`[OLS5-REQ-0056]` A test shall receive exactly one registered status.

`[OLS5-REQ-0057]` NOT APPLICABLE shall not be counted as PASS.

`[OLS5-REQ-0058]` A class shall receive PASS only when every applicable test receives PASS and no applicable test receives FAIL, INCOMPLETE, or UNSUPPORTED.

`[OLS5-REQ-0059]` Aggregate precedence shall be FAIL, then INCOMPLETE, then UNSUPPORTED, then PASS; NOT APPLICABLE results shall be excluded from precedence.

`[OLS5-REQ-0060]` A dependency class result shall be included in aggregate status.

`[OLS5-REQ-0061]` Retesting shall preserve earlier result records and identify supersession without erasing history.

## 10 Conformance evidence

*Stable clause ID: `OLS5-CLS-0010` — Trace ID: `TRACE-000164` — Normative*

Acceptable evidence includes document inspection, identifier verification, registry verification, semantic verification, operator/profile/derivation verification, trace verification, controlled test records, and inspectable realization mappings.

`[OLS5-REQ-0062]` Evidence shall be identifiable, inspectable, relevant to the requirement, and linked to the tested target and version.

`[OLS5-REQ-0063]` Evidence shall preserve provenance, date, assessor or producing system, and status.

`[OLS5-REQ-0064]` Evidence shall be sufficient for an independent assessor to repeat or audit the determination.

`[OLS5-REQ-0065]` Unsupported, disputed, partial, simulated, inferred, or implementation-generated evidence shall retain that status.

`[OLS5-REQ-0066]` Implementation technology, programming language, storage model, runtime, vendor, or platform shall not be mandatory evidence.

`[OLS5-REQ-0067]` Absence of mandatory evidence shall produce INCOMPLETE, not inferred PASS.

`[OLS5-REQ-0068]` Evidence for one requirement may support another only through an explicit second mapping and determination.

`[OLS5-REQ-0069]` Passing evidence shall not alter the evidence class or uncertainty status of the assessed semantic material.

## 11 Conformance reporting

*Stable clause ID: `OLS5-CLS-0011` — Trace ID: `TRACE-000165` — Normative*

A conformance report contains:

1. report identifier and date;
2. claimant and assessor;
3. target identifier, type, and version;
4. suite version and release manifest;
5. Conformance ID and dependencies;
6. tested clauses, Requirement IDs, Test IDs, registries, and annexes;
7. active profiles, declarations, invoked operators, and used derivations as applicable;
8. test applicability and evidence summary;
9. per-test status;
10. failures, incomplete tests, unsupported items, and not-applicable reasons;
11. conflicts, limitations, exclusions, and deviations;
12. aggregate status and certification boundary;
13. test-registry version and supersession history.

`[OLS5-REQ-0070]` Every report shall include all thirteen report fields.

`[OLS5-REQ-0071]` The report shall list every Requirement ID in the claimed class or provide an unambiguous complete reference to Annex B plus per-test results.

`[OLS5-REQ-0072]` Every non-PASS status shall include a reason and evidence reference.

`[OLS5-REQ-0073]` Every NOT APPLICABLE status shall identify the controlling applicability condition.

`[OLS5-REQ-0074]` The report shall distinguish claimant assertions from assessor determinations.

`[OLS5-REQ-0075]` The report shall disclose unsupported and partial capabilities without representing them as conforming.

`[OLS5-REQ-0076]` The aggregate status shall be reproducible from per-test statuses and Clause 9.

`[OLS5-REQ-0077]` A changed target, suite version, class scope, or controlling requirement shall require a new or superseding report.

`[OLS5-REQ-0078]` Reports shall preserve stable identifiers exactly as published.

## 12 Certification boundaries

*Stable clause ID: `OLS5-CLS-0012` — Trace ID: `TRACE-000166` — Normative*

Conformance certifies only that the assessed target satisfied the identified applicable normative requirements under the declared scope, suite version, test version, evidence, and date.

`[OLS5-REQ-0079]` Conformance shall not certify correctness, truth, usefulness, scientific validity, implementation quality, runtime behavior, safety, performance, recommendation quality, authority, successful execution, or outcome validity.

`[OLS5-REQ-0080]` Certification wording shall state its target, Conformance ID, suite version, report identifier, date, and aggregate status.

`[OLS5-REQ-0081]` Certification shall not extend to an untested target, version, profile, operator, declaration, derivation, or capability.

`[OLS5-REQ-0082]` PASS shall not erase uncertainty, validate source evidence, authorize action, or guarantee outcome or learning.

`[OLS5-REQ-0083]` A third-party certification process may add procedural controls but shall not modify OLS semantics, tests, or status meanings.

## 13 Implementation independence and partial capability

*Stable clause ID: `OLS5-CLS-0013` — Trace ID: `TRACE-000167` — Normative*

`[OLS5-REQ-0084]` A test shall assess observable semantic or structural obligations rather than internal implementation design.

`[OLS5-REQ-0085]` Different implementations shall be eligible for the same class when they provide equivalent evidence for the same requirements.

`[OLS5-REQ-0086]` An implementation may support fewer than all profiles but shall not claim a profile whose applicable requirements receive UNSUPPORTED.

`[OLS5-REQ-0087]` A general Orientation Language claim shall not declare partial Universal Base Language conformance.

`[OLS5-REQ-0088]` Unsupported optional profiles shall be reported and shall be NOT APPLICABLE only when excluded from the declared class scope and not activated or invoked.

`[OLS5-REQ-0089]` Implementation mappings shall preserve semantic ownership, identifiers, declarations, status, provenance, uncertainty, and prohibited implications.

## 14 Summary

*Stable clause ID: `OLS5-CLS-0014` — Trace ID: `TRACE-000168` — Normative*

`[OLS5-REQ-0090]` Version 1.0 conformance shall use Annex A classes, Annex B tests, and Annex C statuses.

`[OLS5-REQ-0091]` Every claimed applicable requirement shall receive a repeatable evidence-backed status.

`[OLS5-REQ-0092]` No passing test, class, report, or certification shall create semantic status beyond its controlling requirement.

---

# Annex A — Conformance Class Registry

*Annex ID: `OLS5-ANNEX-A` — Trace ID: `TRACE-000169` — Normative*

| Conformance ID | Name | Normative scope | Dependencies | PASS boundary |
| --- | --- | --- | --- | --- |
| `CONFORMANCE-OLS0` | OLS-0 Conformance | Applicable OLS-0 requirements | None | All applicable OLS-0 tests PASS. |
| `CONFORMANCE-OLS1` | OLS-1 Conformance | Applicable OLS-0 and OLS-1 requirements | `CONFORMANCE-OLS0` | Dependency and all applicable OLS-1 tests PASS. |
| `CONFORMANCE-OLS2` | OLS-2 Conformance | Applicable OLS-0 through OLS-2 requirements | `CONFORMANCE-OLS1` | Dependency and all applicable OLS-2 tests PASS. |
| `CONFORMANCE-OLS3` | OLS-3 Conformance | Applicable OLS-0 through OLS-3 requirements | `CONFORMANCE-OLS2` | Dependency and all applicable OLS-3 tests PASS. |
| `CONFORMANCE-OLS4` | OLS-4 Conformance | Applicable OLS-0 through OLS-4 requirements | `CONFORMANCE-OLS3` | Dependency and all applicable OLS-4 tests PASS. |
| `CONFORMANCE-FULL-SUITE` | Full Suite Conformance | Applicable OLS-0 through OLS-5 requirements | `CONFORMANCE-OLS4` | Dependency and all applicable OLS-5 tests PASS. |

`[OLS5-REQ-0093]` Annex A shall contain exactly six Conformance IDs.

`[OLS5-REQ-0094]` A Conformance ID shall not be reassigned to another scope.

# Annex B — Requirement-to-Test Matrix

*Annex ID: `OLS5-ANNEX-B` — Trace ID: `TRACE-000170` — Normative*

## B.1 Mapping rule

For every published Requirement ID `OLSx-REQ-nnnn`, the corresponding Test ID is `TEST-OLSx-nnnn`. The controlling requirement text is the test oracle. The test establishes applicability, inspects admissible evidence through the registered method, verifies the full normative assertion and referenced registries, checks prohibited outcomes where applicable, and assigns exactly one Annex C status.

`[OLS5-REQ-0095]` The one-to-one mapping shall preserve the numeric component and owning part of every Requirement ID.

`[OLS5-REQ-0096]` Each matrix row shall identify one Requirement ID, one Test ID, one primary method, and the expected condition.

## B.2 Complete Version 1.0 matrix

| Requirement ID | Test ID | Primary method | Expected condition |
| --- | --- | --- | --- |
| `OLS0-REQ-0001` | `TEST-OLS0-0001` | `METHOD-DOCUMENT-INSPECTION` | Every document claiming membership in the Orientation Language Specification suite shall apply the applicable conventions of OLS-0. |
| `OLS0-REQ-0002` | `TEST-OLS0-0002` | `METHOD-DOCUMENT-INSPECTION` | OLS-0 shall not be cited as the authoritative definition of an Orientation Language semantic element. |
| `OLS0-REQ-0003` | `TEST-OLS0-0003` | `METHOD-REGISTRY-VERIFICATION` | A suite part shall define only material assigned to it by the document registry and the frozen architectural ownership model. |
| `OLS0-REQ-0004` | `TEST-OLS0-0004` | `METHOD-DOCUMENT-INSPECTION` | A later-numbered part may reference an earlier part but shall not replace or redefine the earlier part’s authoritative content. |
| `OLS0-REQ-0005` | `TEST-OLS0-0005` | `METHOD-DOCUMENT-INSPECTION` | OLS-I shall not supply semantic or conformance requirements absent from the normative suite. |
| `OLS0-REQ-0006` | `TEST-OLS0-0006` | `METHOD-DOCUMENT-INSPECTION` | Every normative clause and normative annex shall be explicitly identifiable as normative through document structure, clause metadata, or annex title. |
| `OLS0-REQ-0007` | `TEST-OLS0-0007` | `METHOD-DOCUMENT-INSPECTION` | Normative tables and figures shall identify their controlling clause or state their normative status directly. |
| `OLS0-REQ-0008` | `TEST-OLS0-0008` | `METHOD-DOCUMENT-INSPECTION` | Informative material shall be marked **Informative** at the clause, section, annex, or document level. |
| `OLS0-REQ-0009` | `TEST-OLS0-0009` | `METHOD-DOCUMENT-INSPECTION` | Informative material shall not override, narrow, broaden, or create a normative requirement. |
| `OLS0-REQ-0010` | `TEST-OLS0-0010` | `METHOD-DOCUMENT-INSPECTION` | If informative material conflicts with normative material, the normative material shall control and the conflict shall be recorded for editorial correction. |
| `OLS0-REQ-0011` | `TEST-OLS0-0011` | `METHOD-DOCUMENT-INSPECTION` | Visual emphasis, physical proximity, repetition, implementation prevalence, or historical frequency shall not change the declared status of material. |
| `OLS0-REQ-0012` | `TEST-OLS0-0012` | `METHOD-DOCUMENT-INSPECTION` | Normative obligations shall use the keywords defined in this clause. |
| `OLS0-REQ-0013` | `TEST-OLS0-0013` | `METHOD-DOCUMENT-INSPECTION` | The words “must”, “must not”, “required”, “recommended”, “optional”, and similar prose shall not be used as substitutes for the normative keywords in normative clauses. |
| `OLS0-REQ-0014` | `TEST-OLS0-0014` | `METHOD-IDENTIFIER-VERIFICATION` | Keywords appearing in quotations, examples, code, identifiers, document titles, or explicitly informative text shall not create normative obligations. |
| `OLS0-REQ-0015` | `TEST-OLS0-0015` | `METHOD-DOCUMENT-INSPECTION` | A controlled term shall have exactly one authoritative definition within a given compatible suite release. |
| `OLS0-REQ-0016` | `TEST-OLS0-0016` | `METHOD-DOCUMENT-INSPECTION` | A controlled term shall be defined in the normative part that owns its responsibility. |
| `OLS0-REQ-0017` | `TEST-OLS0-0017` | `METHOD-REGISTRY-VERIFICATION` | OLS-0 and the central terminology registry shall point to authoritative definitions rather than duplicate them. |
| `OLS0-REQ-0018` | `TEST-OLS0-0018` | `METHOD-DOCUMENT-INSPECTION` | An alias shall identify its target Term ID and shall not introduce an independent definition or transfer semantic ownership. |
| `OLS0-REQ-0019` | `TEST-OLS0-0019` | `METHOD-DOCUMENT-INSPECTION` | Historical occurrence shall not confer normative status. |
| `OLS0-REQ-0020` | `TEST-OLS0-0020` | `METHOD-DOCUMENT-INSPECTION` | A historical term used in normative text shall either refer to an existing controlled term or be introduced through the applicable normative change process before it carries normative meaning. |
| `OLS0-REQ-0021` | `TEST-OLS0-0021` | `METHOD-DOCUMENT-INSPECTION` | A deprecation record shall identify the affected Term ID, deprecation version, status, rationale, replacement if any, conformance impact, and retained historical reference. |
| `OLS0-REQ-0022` | `TEST-OLS0-0022` | `METHOD-DOCUMENT-INSPECTION` | Deprecation shall not silently change an authoritative definition. |
| `OLS0-REQ-0023` | `TEST-OLS0-0023` | `METHOD-DOCUMENT-INSPECTION` | Main clauses shall use decimal numbering beginning with 1 in each part. |
| `OLS0-REQ-0024` | `TEST-OLS0-0024` | `METHOD-DOCUMENT-INSPECTION` | Subclauses shall extend the parent number using decimal components. |
| `OLS0-REQ-0025` | `TEST-OLS0-0025` | `METHOD-DOCUMENT-INSPECTION` | Annexes shall use uppercase letters assigned in publication order and shall state their normative or informative status in the annex title. |
| `OLS0-REQ-0026` | `TEST-OLS0-0026` | `METHOD-DOCUMENT-INSPECTION` | Figures and tables shall be numbered within their document or annex and shall be cited together with their document ID. |
| `OLS0-REQ-0027` | `TEST-OLS0-0027` | `METHOD-DOCUMENT-INSPECTION` | Renumbering shall not change a stable Clause ID or Requirement ID. |
| `OLS0-REQ-0028` | `TEST-OLS0-0028` | `METHOD-IDENTIFIER-VERIFICATION` | Every identifier shall be unique within its identifier class and assigned registry scope. |
| `OLS0-REQ-0029` | `TEST-OLS0-0029` | `METHOD-IDENTIFIER-VERIFICATION` | A published identifier shall not be reassigned to a different object. |
| `OLS0-REQ-0030` | `TEST-OLS0-0030` | `METHOD-IDENTIFIER-VERIFICATION` | A retired identifier shall remain reserved and traceable. |
| `OLS0-REQ-0031` | `TEST-OLS0-0031` | `METHOD-DOCUMENT-INSPECTION` | Clause and Requirement IDs shall remain independent of visible clause numbering. |
| `OLS0-REQ-0032` | `TEST-OLS0-0032` | `METHOD-DOCUMENT-INSPECTION` | A normative requirement shall have exactly one Requirement ID, even when explanatory text or tables repeat its human-readable wording. |
| `OLS0-REQ-0033` | `TEST-OLS0-0033` | `METHOD-DOCUMENT-INSPECTION` | Multiple requirements shall not be combined under one Requirement ID when they can produce independent conformance outcomes. |
| `OLS0-REQ-0034` | `TEST-OLS0-0034` | `METHOD-IDENTIFIER-VERIFICATION` | Machine-readable exports shall preserve identifiers exactly as published. |
| `OLS0-REQ-0035` | `TEST-OLS0-0035` | `METHOD-IDENTIFIER-VERIFICATION` | A normative cross-reference shall identify the target Document ID and stable Clause ID, Requirement ID, registry identifier, or annex identifier as applicable. |
| `OLS0-REQ-0036` | `TEST-OLS0-0036` | `METHOD-IDENTIFIER-VERIFICATION` | A visible clause number or title may accompany a stable identifier for readability but shall not be the sole target of a normative cross-reference. |
| `OLS0-REQ-0037` | `TEST-OLS0-0037` | `METHOD-DOCUMENT-INSPECTION` | Cross-document references shall identify a compatible suite version directly or through the release manifest. |
| `OLS0-REQ-0038` | `TEST-OLS0-0038` | `METHOD-DOCUMENT-INSPECTION` | A reference to an informative source shall be labeled informative when its status is not evident from the source Document ID or citation. |
| `OLS0-REQ-0039` | `TEST-OLS0-0039` | `METHOD-DOCUMENT-INSPECTION` | Broken, ambiguous, or version-incompatible normative references shall be treated as publication defects and shall not be resolved by inferred intent. |
| `OLS0-REQ-0040` | `TEST-OLS0-0040` | `METHOD-REGISTRY-VERIFICATION` | Each primitive concept and primitive operator shall resolve to exactly one semantic owner identified by the applicable normative registry. |
| `OLS0-REQ-0041` | `TEST-OLS0-0041` | `METHOD-DOCUMENT-INSPECTION` | A referencing part, profile, annex, implementation, example, or extension shall not redefine an owned semantic element. |
| `OLS0-REQ-0042` | `TEST-OLS0-0042` | `METHOD-DOCUMENT-INSPECTION` | Referencing an owned semantic element shall not transfer ownership. |
| `OLS0-REQ-0043` | `TEST-OLS0-0043` | `METHOD-DOCUMENT-INSPECTION` | If two normative texts appear to define the same owned responsibility differently, publication shall stop for the affected text until the ownership conflict is corrected or referred to an Architecture Revision Process. |
| `OLS0-REQ-0044` | `TEST-OLS0-0044` | `METHOD-IDENTIFIER-VERIFICATION` | Each registry entry shall have a stable identifier, status, owner, version of introduction, and controlling normative reference. |
| `OLS0-REQ-0045` | `TEST-OLS0-0045` | `METHOD-REGISTRY-VERIFICATION` | A registry shall not contain a second authoritative definition when the controlling clause already supplies one. |
| `OLS0-REQ-0046` | `TEST-OLS0-0046` | `METHOD-REGISTRY-VERIFICATION` | A normative registry shall be published as a normative annex or normative clause of its owning part. |
| `OLS0-REQ-0047` | `TEST-OLS0-0047` | `METHOD-REGISTRY-VERIFICATION` | A machine-readable registry export shall be treated as an implementation artifact unless a normative clause explicitly establishes its precedence and equivalence rules. |
| `OLS0-REQ-0048` | `TEST-OLS0-0048` | `METHOD-REGISTRY-VERIFICATION` | Registry changes shall be included in the release manifest and change record. |
| `OLS0-REQ-0049` | `TEST-OLS0-0049` | `METHOD-DOCUMENT-INSPECTION` | Every published suite release shall include one release manifest. |
| `OLS0-REQ-0050` | `TEST-OLS0-0050` | `METHOD-DOCUMENT-INSPECTION` | The release manifest shall identify: |
| `OLS0-REQ-0051` | `TEST-OLS0-0051` | `METHOD-DOCUMENT-INSPECTION` | A release manifest shall not claim compatibility for a set of parts whose declared dependencies conflict. |
| `OLS0-REQ-0052` | `TEST-OLS0-0052` | `METHOD-DOCUMENT-INSPECTION` | File names and repository locations shall not substitute for the release manifest. |
| `OLS0-REQ-0053` | `TEST-OLS0-0053` | `METHOD-DOCUMENT-INSPECTION` | A citation or conformance claim shall identify the suite version against which it is made. |
| `OLS0-REQ-0054` | `TEST-OLS0-0054` | `METHOD-DOCUMENT-INSPECTION` | Compatibility among independently revised parts shall be established by a release manifest, not inferred from matching major numbers alone. |
| `OLS0-REQ-0055` | `TEST-OLS0-0055` | `METHOD-DOCUMENT-INSPECTION` | An editorial revision shall not change normative meaning, requirement applicability, semantic ownership, or conformance outcome. |
| `OLS0-REQ-0056` | `TEST-OLS0-0056` | `METHOD-DOCUMENT-INSPECTION` | A version reference lacking a revision number may be used only when the intended release manifest unambiguously resolves the revision. |
| `OLS0-REQ-0057` | `TEST-OLS0-0057` | `METHOD-REGISTRY-VERIFICATION` | A citation intended to support a normative claim shall cite the controlling normative clause or registry entry rather than an informative paraphrase. |
| `OLS0-REQ-0058` | `TEST-OLS0-0058` | `METHOD-IDENTIFIER-VERIFICATION` | A citation shall preserve the target identifier and suite version exactly. |
| `OLS0-REQ-0059` | `TEST-OLS0-0059` | `METHOD-DOCUMENT-INSPECTION` | A citation to superseded or deprecated material shall state that status. |
| `OLS0-REQ-0060` | `TEST-OLS0-0060` | `METHOD-IDENTIFIER-VERIFICATION` | External sources shall be cited with sufficient bibliographic or persistent-identifier information to locate the cited edition. |
| `OLS0-REQ-0061` | `TEST-OLS0-0061` | `METHOD-DOCUMENT-INSPECTION` | A conformance claim shall identify its target, suite version, applicable normative parts, Requirement IDs, active profiles where applicable, and test evidence required by OLS-5. |
| `OLS0-REQ-0062` | `TEST-OLS0-0062` | `METHOD-DOCUMENT-INSPECTION` | A conformance claim shall not rely solely on a document title, informal phrase, implementation label, or informative example. |
| `OLS0-REQ-0063` | `TEST-OLS0-0063` | `METHOD-DOCUMENT-INSPECTION` | A claim of profile conformance shall cite the Profile ID and the release manifest that establishes the compatible profile specification. |
| `OLS0-REQ-0064` | `TEST-OLS0-0064` | `METHOD-DOCUMENT-INSPECTION` | Passing test evidence shall not be cited as proof of claims beyond the declared conformance scope. |
| `OLS0-REQ-0065` | `TEST-OLS0-0065` | `METHOD-TRACE-VERIFICATION` | Every normative clause shall have a Trace ID mapping it to its architectural source, architectural classification, semantic owner where applicable, and relevant ADR decision. |
| `OLS0-REQ-0066` | `TEST-OLS0-0066` | `METHOD-DOCUMENT-INSPECTION` | Every Requirement ID shall map to a Test ID or to a recorded explanation that direct testing is not applicable. |
| `OLS0-REQ-0067` | `TEST-OLS0-0067` | `METHOD-TRACE-VERIFICATION` | Reverse traceability shall identify every specification clause that realizes a frozen normative architectural artifact. |
| `OLS0-REQ-0068` | `TEST-OLS0-0068` | `METHOD-TRACE-VERIFICATION` | Earlier research evidence may support traceability but shall not override the Phase 2D Canonical Architecture. |
| `OLS0-REQ-0069` | `TEST-OLS0-0069` | `METHOD-DOCUMENT-INSPECTION` | Phase 3 specification text shall remain consistent with the architecture frozen by ADR-0001. |
| `OLS0-REQ-0070` | `TEST-OLS0-0070` | `METHOD-DOCUMENT-INSPECTION` | ADR-0001 may be cited as architectural rationale but shall not be used as a substitute for a controlling normative clause after that clause is published. |
| `OLS0-REQ-0071` | `TEST-OLS0-0071` | `METHOD-DOCUMENT-INSPECTION` | Version 1.0 specification drafting shall describe the frozen Phase 2D architecture without adding, removing, or reallocating semantic responsibilities. |
| `OLS0-REQ-0072` | `TEST-OLS0-0072` | `METHOD-TRACE-VERIFICATION` | Earlier phases may be cited for historical or research traceability but shall not override the Phase 2D baseline. |
| `OLS0-REQ-0073` | `TEST-OLS0-0073` | `METHOD-DOCUMENT-INSPECTION` | An apparent need to change a frozen semantic inventory, responsibility, ownership, composition rule, or accepted derivation shall be treated as an architecture-revision question rather than an editorial correction. |
| `OLS0-REQ-0074` | `TEST-OLS0-0074` | `METHOD-DOCUMENT-INSPECTION` | A definition, contract, profile rule, derivation, or conformance requirement shall be cited from its owning normative part. |
| `OLS0-REQ-0075` | `TEST-OLS0-0075` | `METHOD-DOCUMENT-INSPECTION` | OLS-0 shall control suite-wide editorial interpretation where it does not conflict with the semantic ownership of OLS-1 through OLS-6. |
| `OLS0-REQ-0076` | `TEST-OLS0-0076` | `METHOD-DOCUMENT-INSPECTION` | If a suite-wide convention and a semantic clause appear to conflict, publication or maintenance shall stop for the affected text until the conflict is classified and corrected; neither clause shall be silently ignored. |
| `OLS0-REQ-0077` | `TEST-OLS0-0077` | `METHOD-DOCUMENT-INSPECTION` | OLS-I shall identify the suite release it explains. |
| `OLS0-REQ-0078` | `TEST-OLS0-0078` | `METHOD-DOCUMENT-INSPECTION` | OLS-I shall cite the controlling normative clauses for any normative behavior it illustrates. |
| `OLS0-REQ-0079` | `TEST-OLS0-0079` | `METHOD-DOCUMENT-INSPECTION` | Revision of OLS-I alone shall not change conformance to a fixed normative release. |
| `OLS0-REQ-0080` | `TEST-OLS0-0080` | `METHOD-DOCUMENT-INSPECTION` | Work on an affected specification clause shall stop when completing it requires a new universal primitive, removal of an accepted primitive, changed responsibility, changed ownership, changed profile composition, changed accepted derivation, or changed normative status for informative or implementation material. |
| `OLS0-REQ-0081` | `TEST-OLS0-0081` | `METHOD-DOCUMENT-INSPECTION` | An architecture-revision proposal shall remain outside the current normative release until approved through an explicit future Architecture Revision Process and decision record. |
| `OLS0-REQ-0082` | `TEST-OLS0-0082` | `METHOD-TRACE-VERIFICATION` | Rejected, deferred, or unresolved proposals shall remain traceable and shall not be represented as current semantics. |
| `OLS0-REQ-0083` | `TEST-OLS0-0083` | `METHOD-DOCUMENT-INSPECTION` | Every proposed maintenance change shall be classified as editorial, backward-compatible normative, deprecation, or architectural before publication. |
| `OLS0-REQ-0084` | `TEST-OLS0-0084` | `METHOD-DOCUMENT-INSPECTION` | A change that affects interpretation, applicability, ownership, requirement force, or conformance outcome shall not be classified as editorial. |
| `OLS0-REQ-0085` | `TEST-OLS0-0085` | `METHOD-DOCUMENT-INSPECTION` | Published errata shall identify affected stable IDs, affected versions, correction text, classification, approval record, and release incorporation status. |
| `OLS0-REQ-0086` | `TEST-OLS0-0086` | `METHOD-IDENTIFIER-VERIFICATION` | A correction to a duplicated or malformed identifier shall preserve the erroneous identifier as a traceable alias or tombstone and shall not reassign it. |
| `OLS0-REQ-0087` | `TEST-OLS0-0087` | `METHOD-DOCUMENT-INSPECTION` | Normative definitions and requirements shall appear once in their owning location; other occurrences shall be cross-references or clearly informative summaries. |
| `OLS0-REQ-0088` | `TEST-OLS0-0088` | `METHOD-REGISTRY-VERIFICATION` | Generated indexes and registry exports shall identify their controlling source and generation version. |
| `OLS0-REQ-0089` | `TEST-OLS0-0089` | `METHOD-IDENTIFIER-VERIFICATION` | A normative publication shall complete editorial, cross-reference, traceability, identifier-uniqueness, dependency, normative-status, and conformance-impact review. |
| `OLS0-REQ-0090` | `TEST-OLS0-0090` | `METHOD-DOCUMENT-INSPECTION` | Unresolved ownership, architecture, or normative-status conflicts shall block publication of the affected release. |
| `OLS0-REQ-0091` | `TEST-OLS0-0091` | `METHOD-DOCUMENT-INSPECTION` | Every suite document shall publish the following metadata: |
| `OLS0-REQ-0092` | `TEST-OLS0-0092` | `METHOD-REGISTRY-VERIFICATION` | Metadata shall not be used to imply semantic scope that the document registry does not assign. |
| `OLS0-REQ-0093` | `TEST-OLS0-0093` | `METHOD-DOCUMENT-INSPECTION` | A metadata change affecting version compatibility, status, dependency, or supersession shall be recorded in the release manifest and change history. |
| `OLS0-REQ-0094` | `TEST-OLS0-0094` | `METHOD-IDENTIFIER-VERIFICATION` | A document shall claim membership in the Version 1.0 suite only under an identifier and role listed in this registry or added through the OLS-6 extension and release process. |
| `OLS0-REQ-0095` | `TEST-OLS0-0095` | `METHOD-DOCUMENT-INSPECTION` | A Document ID shall not be reused for a different allocated responsibility within Version 1.0. |
| `OLS0-REQ-0096` | `TEST-OLS0-0096` | `METHOD-DOCUMENT-INSPECTION` | A document dependency shall not authorize the dependent document to redefine the dependency. |
| `OLS1-REQ-0001` | `TEST-OLS1-0001` | `METHOD-SEMANTIC-VERIFICATION` | The Universal Base Language shall contain exactly the concepts and primitive operator responsibilities specified by OLS-1. |
| `OLS1-REQ-0002` | `TEST-OLS1-0002` | `METHOD-SEMANTIC-VERIFICATION` | OLS-1 shall not define instance-level declaration semantics, complete operator contracts, profile-owned semantics, derivation rules, conformance procedures, governance, or implementation behavior. |
| `OLS1-REQ-0003` | `TEST-OLS1-0003` | `METHOD-SEMANTIC-VERIFICATION` | A reference from OLS-1 to a later suite part shall not transfer that part’s ownership to OLS-1. |
| `OLS1-REQ-0004` | `TEST-OLS1-0004` | `METHOD-SEMANTIC-VERIFICATION` | OLS-1 shall be read using the normative keywords, identifier policy, cross-reference policy, semantic-ownership policy, and status conventions defined by OLS-0. |
| `OLS1-REQ-0005` | `TEST-OLS1-0005` | `METHOD-SEMANTIC-VERIFICATION` | Each universal concept shall have exactly one authoritative Term ID and definition in OLS-1. |
| `OLS1-REQ-0006` | `TEST-OLS1-0006` | `METHOD-SEMANTIC-VERIFICATION` | An alias, historical use, implementation label, or profile-specific term shall not replace an OLS-1 definition. |
| `OLS1-REQ-0007` | `TEST-OLS1-0007` | `METHOD-SEMANTIC-VERIFICATION` | Ordinary words used inside a definition shall not be interpreted as additional universal concept primitives unless Annex A registers them as such. |
| `OLS1-REQ-0008` | `TEST-OLS1-0008` | `METHOD-SEMANTIC-VERIFICATION` | The Universal Base Language shall be present in every Orientation Language construction that claims semantic conformance. |
| `OLS1-REQ-0009` | `TEST-OLS1-0009` | `METHOD-SEMANTIC-VERIFICATION` | The Universal Base Language shall not be deactivated, replaced, weakened, or redefined by a profile, implementation, application, example, or informative component. |
| `OLS1-REQ-0010` | `TEST-OLS1-0010` | `METHOD-SEMANTIC-VERIFICATION` | A construction using no extension profile shall remain a Universal Base Language construction when it satisfies the applicable requirements of OLS-1 and later owning parts. |
| `OLS1-REQ-0011` | `TEST-OLS1-0011` | `METHOD-SEMANTIC-VERIFICATION` | Use of the Universal Base Language shall not imply activation of a semantic profile. |
| `OLS1-REQ-0012` | `TEST-OLS1-0012` | `METHOD-SEMANTIC-VERIFICATION` | OLS-1 shall remain the semantic owner of the fourteen universal concepts and the responsibility-level meanings of OBSERVE, REPRESENT, COMPARE, ORIENT, and EXPLAIN. |
| `OLS1-REQ-0013` | `TEST-OLS1-0013` | `METHOD-SEMANTIC-VERIFICATION` | Transformation, persistence, selection, validation, authority, navigation, learning, publication, cultural interpretation, and implementation realization shall remain outside the universal primitive operator inventory. |
| `OLS1-REQ-0014` | `TEST-OLS1-0014` | `METHOD-SEMANTIC-VERIFICATION` | OLS-1 shall not present the Universal Base Language as a universal ontology or as a complete account of reality. |
| `OLS1-REQ-0015` | `TEST-OLS1-0015` | `METHOD-SEMANTIC-VERIFICATION` | Semantic profiles may extend the Universal Base Language only under OLS-3 and shall not modify OLS-1 semantics. |
| `OLS1-REQ-0016` | `TEST-OLS1-0016` | `METHOD-SEMANTIC-VERIFICATION` | An orientation claim shall identify the context, perspective, representation, evidence, provenance, and uncertainty relevant to that claim through the applicable declaration rules of OLS-2. |
| `OLS1-REQ-0017` | `TEST-OLS1-0017` | `METHOD-SEMANTIC-VERIFICATION` | A representation shall remain distinguishable from the source material and reality it represents. |
| `OLS1-REQ-0018` | `TEST-OLS1-0018` | `METHOD-SEMANTIC-VERIFICATION` | An orientation shall remain distinguishable from recommendation, authorization, execution, outcome, learning, control, and certainty. |
| `OLS1-REQ-0019` | `TEST-OLS1-0019` | `METHOD-SEMANTIC-VERIFICATION` | A universal semantic assertion shall preserve the declared status of observations, evidence, provenance, and uncertainty through every universal operator that uses or communicates it. |
| `OLS1-REQ-0020` | `TEST-OLS1-0020` | `METHOD-SEMANTIC-VERIFICATION` | No additional concept shall be represented as a Version 1.0 universal primitive. |
| `OLS1-REQ-0021` | `TEST-OLS1-0021` | `METHOD-SEMANTIC-VERIFICATION` | A universal concept shall retain the definition, responsibility, and boundaries assigned by its owning subsection. |
| `OLS1-REQ-0022` | `TEST-OLS1-0022` | `METHOD-SEMANTIC-VERIFICATION` | The absence of an instance of a concept from a particular expression shall be evaluated by the claims made and the applicable OLS-2 declaration rules; it shall not remove the concept from the universal inventory. |
| `OLS1-REQ-0023` | `TEST-OLS1-0023` | `METHOD-SEMANTIC-VERIFICATION` | A source item shall not acquire evidence, validation, or outcome status solely because it is an observation. |
| `OLS1-REQ-0024` | `TEST-OLS1-0024` | `METHOD-SEMANTIC-VERIFICATION` | An observation used by another universal operator shall preserve its declared source and epistemic status. |
| `OLS1-REQ-0025` | `TEST-OLS1-0025` | `METHOD-SEMANTIC-VERIFICATION` | A construction shall keep the observer distinct from the observation and representation unless it explicitly asserts a relation among them. |
| `OLS1-REQ-0026` | `TEST-OLS1-0026` | `METHOD-SEMANTIC-VERIFICATION` | A construction shall not present an observer’s view as perspective-free. |
| `OLS1-REQ-0027` | `TEST-OLS1-0027` | `METHOD-SEMANTIC-VERIFICATION` | An orientation act shall be interpreted within an explicitly declared context under OLS-2. |
| `OLS1-REQ-0028` | `TEST-OLS1-0028` | `METHOD-SEMANTIC-VERIFICATION` | A semantic assertion shall not be generalized beyond its declared context without a separately supported assertion. |
| `OLS1-REQ-0029` | `TEST-OLS1-0029` | `METHOD-SEMANTIC-VERIFICATION` | A representation or orientation claim shall identify its applicable perspective under OLS-2. |
| `OLS1-REQ-0030` | `TEST-OLS1-0030` | `METHOD-SEMANTIC-VERIFICATION` | A construction shall not silently conflate a construction perspective with a reading perspective. |
| `OLS1-REQ-0031` | `TEST-OLS1-0031` | `METHOD-SEMANTIC-VERIFICATION` | A representation shall remain explicitly distinguishable from the reality or source material it represents. |
| `OLS1-REQ-0032` | `TEST-OLS1-0032` | `METHOD-SEMANTIC-VERIFICATION` | A representation used for orientation shall identify its representation type under OLS-2. |
| `OLS1-REQ-0033` | `TEST-OLS1-0033` | `METHOD-SEMANTIC-VERIFICATION` | Representation compatibility shall not be assumed when the comparison basis or applicable declarations are absent or incompatible. |
| `OLS1-REQ-0034` | `TEST-OLS1-0034` | `METHOD-SEMANTIC-VERIFICATION` | A position-dependent assertion shall identify the applicable position under OLS-2. |
| `OLS1-REQ-0035` | `TEST-OLS1-0035` | `METHOD-SEMANTIC-VERIFICATION` | A position shall not be interpreted as a path or selection. |
| `OLS1-REQ-0036` | `TEST-OLS1-0036` | `METHOD-SEMANTIC-VERIFICATION` | A relation shall identify the items related and the context or representation in which the relation is asserted. |
| `OLS1-REQ-0037` | `TEST-OLS1-0037` | `METHOD-SEMANTIC-VERIFICATION` | A relation shall not be presented as a causal mechanism without separately governed support. |
| `OLS1-REQ-0038` | `TEST-OLS1-0038` | `METHOD-SEMANTIC-VERIFICATION` | A state assertion shall preserve the identity, time, and scale distinctions on which the assertion depends under OLS-2. |
| `OLS1-REQ-0039` | `TEST-OLS1-0039` | `METHOD-SEMANTIC-VERIFICATION` | A state shall not be treated as an admitted outcome solely because it occurs after another state. |
| `OLS1-REQ-0040` | `TEST-OLS1-0040` | `METHOD-SEMANTIC-VERIFICATION` | A transition assertion shall identify the source and resulting states and preserve the applicable identity and temporal order under OLS-2. |
| `OLS1-REQ-0041` | `TEST-OLS1-0041` | `METHOD-SEMANTIC-VERIFICATION` | A transition shall not be treated as a TRANSFORM invocation or validated outcome solely because a change is represented. |
| `OLS1-REQ-0042` | `TEST-OLS1-0042` | `METHOD-SEMANTIC-VERIFICATION` | Material used as evidence shall retain its declared evidence class, provenance, and uncertainty under OLS-2. |
| `OLS1-REQ-0043` | `TEST-OLS1-0043` | `METHOD-SEMANTIC-VERIFICATION` | An observation shall not be treated as evidence for a claim without an explicit evidence assertion and applicable declaration. |
| `OLS1-REQ-0044` | `TEST-OLS1-0044` | `METHOD-SEMANTIC-VERIFICATION` | Evidence shall not be interpreted as validation or authority. |
| `OLS1-REQ-0045` | `TEST-OLS1-0045` | `METHOD-SEMANTIC-VERIFICATION` | A universal operator shall preserve provenance for material whose source or status affects the resulting claim. |
| `OLS1-REQ-0046` | `TEST-OLS1-0046` | `METHOD-SEMANTIC-VERIFICATION` | Provenance shall not be used as a substitute for evidence evaluation or validation. |
| `OLS1-REQ-0047` | `TEST-OLS1-0047` | `METHOD-SEMANTIC-VERIFICATION` | A universal operation producing a finding shall preserve relevant known uncertainty. |
| `OLS1-REQ-0048` | `TEST-OLS1-0048` | `METHOD-SEMANTIC-VERIFICATION` | A construction shall not silently replace uncertainty with confidence or certainty. |
| `OLS1-REQ-0049` | `TEST-OLS1-0049` | `METHOD-SEMANTIC-VERIFICATION` | An orientation shall identify the representation, context, perspective, evidence, provenance, and uncertainty on which it depends under OLS-2. |
| `OLS1-REQ-0050` | `TEST-OLS1-0050` | `METHOD-SEMANTIC-VERIFICATION` | An orientation shall not be presented as recommendation, authorization, execution, outcome, learning, control, or certainty. |
| `OLS1-REQ-0051` | `TEST-OLS1-0051` | `METHOD-SEMANTIC-VERIFICATION` | An orientation shall preserve disagreement and unsupported conclusions as distinct from supported findings. |
| `OLS1-REQ-0052` | `TEST-OLS1-0052` | `METHOD-SEMANTIC-VERIFICATION` | Difference shall remain a universal primitive on which COMPARE depends. |
| `OLS1-REQ-0053` | `TEST-OLS1-0053` | `METHOD-SEMANTIC-VERIFICATION` | A difference shall identify its items and basis and shall not be treated as causal or preferential without separately governed support. |
| `OLS1-REQ-0054` | `TEST-OLS1-0054` | `METHOD-SEMANTIC-VERIFICATION` | OLS-1 operator clauses shall state responsibility and universal boundary only; complete inputs, outputs, preconditions, postconditions, failure behavior, and invocation syntax shall remain in OLS-2. |
| `OLS1-REQ-0055` | `TEST-OLS1-0055` | `METHOD-SEMANTIC-VERIFICATION` | An implementation, profile, application, or historical operator label shall not redefine a universal primitive operator. |
| `OLS1-REQ-0056` | `TEST-OLS1-0056` | `METHOD-SEMANTIC-VERIFICATION` | OBSERVE shall preserve the declared source status of admitted observations. |
| `OLS1-REQ-0057` | `TEST-OLS1-0057` | `METHOD-SEMANTIC-VERIFICATION` | A complete OBSERVE contract shall be taken from OLS-2. |
| `OLS1-REQ-0058` | `TEST-OLS1-0058` | `METHOD-SEMANTIC-VERIFICATION` | REPRESENT shall preserve the representation/reality distinction and the source status of represented material. |
| `OLS1-REQ-0059` | `TEST-OLS1-0059` | `METHOD-SEMANTIC-VERIFICATION` | A complete REPRESENT contract shall be taken from OLS-2. |
| `OLS1-REQ-0060` | `TEST-OLS1-0060` | `METHOD-SEMANTIC-VERIFICATION` | COMPARE shall use declared compatible items and a declared comparison basis under OLS-2. |
| `OLS1-REQ-0061` | `TEST-OLS1-0061` | `METHOD-SEMANTIC-VERIFICATION` | COMPARE shall depend on difference and shall not define difference. |
| `OLS1-REQ-0062` | `TEST-OLS1-0062` | `METHOD-SEMANTIC-VERIFICATION` | A complete COMPARE contract shall be taken from OLS-2. |
| `OLS1-REQ-0063` | `TEST-OLS1-0063` | `METHOD-SEMANTIC-VERIFICATION` | ORIENT shall preserve the declared basis, evidence, provenance, uncertainty, disagreement, unsupported conclusions, and limitations relevant to its result. |
| `OLS1-REQ-0064` | `TEST-OLS1-0064` | `METHOD-SEMANTIC-VERIFICATION` | A complete ORIENT contract shall be taken from OLS-2. |
| `OLS1-REQ-0065` | `TEST-OLS1-0065` | `METHOD-SEMANTIC-VERIFICATION` | EXPLAIN shall not increase the epistemic or authority status of the material it communicates. |
| `OLS1-REQ-0066` | `TEST-OLS1-0066` | `METHOD-SEMANTIC-VERIFICATION` | A complete EXPLAIN contract shall be taken from OLS-2. |
| `OLS1-REQ-0067` | `TEST-OLS1-0067` | `METHOD-SEMANTIC-VERIFICATION` | A construction claiming the complete canonical universal process shall include the five operators in the specified order. |
| `OLS1-REQ-0068` | `TEST-OLS1-0068` | `METHOD-SEMANTIC-VERIFICATION` | A partial construction shall identify the stages present and shall not claim completion of the canonical universal process. |
| `OLS1-REQ-0069` | `TEST-OLS1-0069` | `METHOD-SEMANTIC-VERIFICATION` | Repetition or return to an earlier stage may occur when new observations, representations, comparisons, or uncertainties arise, but each completed pass shall preserve the canonical order. |
| `OLS1-REQ-0070` | `TEST-OLS1-0070` | `METHOD-SEMANTIC-VERIFICATION` | The canonical process shall not be represented as including a profile-owned operator unless the applicable profile is explicitly active under OLS-3. |
| `OLS1-REQ-0071` | `TEST-OLS1-0071` | `METHOD-SEMANTIC-VERIFICATION` | Completion of the canonical process shall not imply recommendation, authorization, execution, validation, outcome, learning, control, certainty, or empirical truth. |
| `OLS1-REQ-0072` | `TEST-OLS1-0072` | `METHOD-SEMANTIC-VERIFICATION` | A downstream clause, profile, implementation, application, example, or explanatory text shall not weaken a universal non-implication. |
| `OLS1-REQ-0073` | `TEST-OLS1-0073` | `METHOD-SEMANTIC-VERIFICATION` | A construction shall preserve the distinction between representation and reality. |
| `OLS1-REQ-0074` | `TEST-OLS1-0074` | `METHOD-SEMANTIC-VERIFICATION` | A construction shall preserve the distinction between orientation and recommendation, authorization, execution, outcome, learning, control, and certainty. |
| `OLS1-REQ-0075` | `TEST-OLS1-0075` | `METHOD-SEMANTIC-VERIFICATION` | A claim crossing a universal boundary shall require separately owned semantics and shall not be inferred from the Universal Base Language alone. |
| `OLS1-REQ-0076` | `TEST-OLS1-0076` | `METHOD-SEMANTIC-VERIFICATION` | A profile shall inherit the Universal Base Language as a complete unit. |
| `OLS1-REQ-0077` | `TEST-OLS1-0077` | `METHOD-SEMANTIC-VERIFICATION` | A profile shall not override, narrow, broaden, replace, or deactivate an inherited universal definition, responsibility, process boundary, or non-implication. |
| `OLS1-REQ-0078` | `TEST-OLS1-0078` | `METHOD-SEMANTIC-VERIFICATION` | Referencing a universal concept or operator from a profile shall not transfer semantic ownership. |
| `OLS1-REQ-0079` | `TEST-OLS1-0079` | `METHOD-SEMANTIC-VERIFICATION` | Historical, cultural, implementation, or application material shall not participate in universal inheritance unless a normative suite part assigns it semantics through the applicable architecture process. |
| `OLS1-REQ-0080` | `TEST-OLS1-0080` | `METHOD-SEMANTIC-VERIFICATION` | A declaration shall not create a new universal concept. |
| `OLS1-REQ-0081` | `TEST-OLS1-0081` | `METHOD-SEMANTIC-VERIFICATION` | The presence of a declaration shall not by itself supply evidence, validation, authority, or truth. |
| `OLS1-REQ-0082` | `TEST-OLS1-0082` | `METHOD-SEMANTIC-VERIFICATION` | A declaration value shall not replace the authoritative definition of the concept to which it applies. |
| `OLS1-REQ-0083` | `TEST-OLS1-0083` | `METHOD-SEMANTIC-VERIFICATION` | OLS-1 shall not determine declaration syntax, value domains, applicability, omission, incompatibility, or default behavior; OLS-2 owns those rules. |
| `OLS1-REQ-0084` | `TEST-OLS1-0084` | `METHOD-SEMANTIC-VERIFICATION` | No declaration value shall be inferred merely from the presence of a universal concept. |
| `OLS1-REQ-0085` | `TEST-OLS1-0085` | `METHOD-SEMANTIC-VERIFICATION` | A valid Universal Base Language expression shall use universal terms according to their OLS-1 definitions. |
| `OLS1-REQ-0086` | `TEST-OLS1-0086` | `METHOD-SEMANTIC-VERIFICATION` | A valid expression shall preserve all applicable universal boundary conditions. |
| `OLS1-REQ-0087` | `TEST-OLS1-0087` | `METHOD-SEMANTIC-VERIFICATION` | A valid expression shall identify every declaration required by its claims under OLS-2. |
| `OLS1-REQ-0088` | `TEST-OLS1-0088` | `METHOD-SEMANTIC-VERIFICATION` | A complete universal orientation expression shall identify the five canonical stages and their semantic products without claiming profile-owned capability. |
| `OLS1-REQ-0089` | `TEST-OLS1-0089` | `METHOD-SEMANTIC-VERIFICATION` | A partial universal construction may be valid within its declared scope but shall not claim a complete orientation process or a downstream implication excluded by OLS-1. |
| `OLS1-REQ-0090` | `TEST-OLS1-0090` | `METHOD-SEMANTIC-VERIFICATION` | A Universal Base Language expression need not activate or identify a semantic profile. |
| `OLS1-REQ-0091` | `TEST-OLS1-0091` | `METHOD-SEMANTIC-VERIFICATION` | A construction claiming the complete canonical process with one or more missing stages shall be incomplete. |
| `OLS1-REQ-0092` | `TEST-OLS1-0092` | `METHOD-SEMANTIC-VERIFICATION` | A construction missing a universal concept or declaration on which its actual claim depends shall be incomplete. |
| `OLS1-REQ-0093` | `TEST-OLS1-0093` | `METHOD-SEMANTIC-VERIFICATION` | A construction containing contradictory assertions about the same identified semantic item under the same declared basis shall be malformed unless the contradiction is explicitly preserved as disagreement or uncertainty. |
| `OLS1-REQ-0094` | `TEST-OLS1-0094` | `METHOD-SEMANTIC-VERIFICATION` | A construction treating a concept as an operator, an operator as a concept definition, a declaration as evidence, or an implementation as semantic authority shall be malformed. |
| `OLS1-REQ-0095` | `TEST-OLS1-0095` | `METHOD-SEMANTIC-VERIFICATION` | A construction that treats representation as reality or orientation as recommendation, authorization, execution, outcome, learning, control, or certainty shall be malformed. |
| `OLS1-REQ-0096` | `TEST-OLS1-0096` | `METHOD-SEMANTIC-VERIFICATION` | A construction that redefines a universal concept or primitive operator responsibility shall be malformed. |
| `OLS1-REQ-0097` | `TEST-OLS1-0097` | `METHOD-SEMANTIC-VERIFICATION` | An incomplete construction may be completed only by supplying supported missing material under the owning specification part; missing semantics shall not be invented or inferred. |
| `OLS1-REQ-0098` | `TEST-OLS1-0098` | `METHOD-SEMANTIC-VERIFICATION` | A Version 1.0 claim to the Universal Base Language shall resolve to the fourteen concepts, five operator responsibilities, canonical process, boundaries, inheritance, and concept/declaration distinction specified by OLS-1. |
| `OLS1-REQ-0099` | `TEST-OLS1-0099` | `METHOD-SEMANTIC-VERIFICATION` | OLS-1 semantics shall remain independent of implementation technology and shall not acquire profile, derivation, governance, or implementation meaning by implication. |
| `OLS1-REQ-0100` | `TEST-OLS1-0100` | `METHOD-SEMANTIC-VERIFICATION` | The universal concept inventory shall contain exactly the fourteen entries in Table A.1. |
| `OLS1-REQ-0101` | `TEST-OLS1-0101` | `METHOD-SEMANTIC-VERIFICATION` | An entry shall not be added to or removed from Table A.1 without an approved Architecture Revision Process. |
| `OLS1-REQ-0102` | `TEST-OLS1-0102` | `METHOD-SEMANTIC-VERIFICATION` | Every Universal Base Language construction shall preserve every applicable non-implication in Table B.1. |
| `OLS1-REQ-0103` | `TEST-OLS1-0103` | `METHOD-SEMANTIC-VERIFICATION` | A later specification part may add separately owned semantics but shall not erase a non-implication in Table B.1. |
| `OLS2-REQ-0001` | `TEST-OLS2-0001` | `METHOD-OPERATOR-VERIFICATION` | OLS-2 shall preserve every universal concept and primitive operator responsibility specified by OLS-1. |
| `OLS2-REQ-0002` | `TEST-OLS2-0002` | `METHOD-OPERATOR-VERIFICATION` | OLS-2 shall contain exactly the ten declarations and ten primitive operator contracts registered in Annexes A and B. |
| `OLS2-REQ-0003` | `TEST-OLS2-0003` | `METHOD-SEMANTIC-VERIFICATION` | OLS-2 shall not define profile activation, profile composition, derivations, conformance procedures, governance, or implementation architecture. |
| `OLS2-REQ-0004` | `TEST-OLS2-0004` | `METHOD-OPERATOR-VERIFICATION` | OLS-2 shall use OLS-0 conventions and shall not change an OLS-1 definition, boundary, inventory, process, or operator responsibility. |
| `OLS2-REQ-0005` | `TEST-OLS2-0005` | `METHOD-SEMANTIC-VERIFICATION` | OLS-2 terms shall be interpreted consistently with OLS-1 and shall not create additional universal primitives. |
| `OLS2-REQ-0006` | `TEST-OLS2-0006` | `METHOD-SEMANTIC-VERIFICATION` | An unsupported declaration shall remain explicit and speculative and shall not satisfy a requirement that depends on supported status. |
| `OLS2-REQ-0007` | `TEST-OLS2-0007` | `METHOD-OPERATOR-VERIFICATION` | Ordinary implementation terms shall not acquire semantic authority through use in an invocation or contract mapping. |
| `OLS2-REQ-0008` | `TEST-OLS2-0008` | `METHOD-SEMANTIC-VERIFICATION` | A declaration shall supply an explicit value or status and shall not redefine the semantic distinction to which it applies. |
| `OLS2-REQ-0009` | `TEST-OLS2-0009` | `METHOD-REGISTRY-VERIFICATION` | A declaration shall have one Declaration ID, one owner, one declared value or status, and an identifiable scope. |
| `OLS2-REQ-0010` | `TEST-OLS2-0010` | `METHOD-SEMANTIC-VERIFICATION` | No declaration shall acquire an inferred default. |
| `OLS2-REQ-0011` | `TEST-OLS2-0011` | `METHOD-OPERATOR-VERIFICATION` | Every applicable declaration shall be present before the dependent claim or operator output is treated as complete. |
| `OLS2-REQ-0012` | `TEST-OLS2-0012` | `METHOD-SEMANTIC-VERIFICATION` | Applicability shall be determined by the claims made and the owning declaration clause, not by implementation convenience. |
| `OLS2-REQ-0013` | `TEST-OLS2-0013` | `METHOD-SEMANTIC-VERIFICATION` | Omission shall not authorize an inferred value. |
| `OLS2-REQ-0014` | `TEST-OLS2-0014` | `METHOD-OPERATOR-VERIFICATION` | Omission of an applicable declaration shall make the dependent construction or invocation incomplete. |
| `OLS2-REQ-0015` | `TEST-OLS2-0015` | `METHOD-OPERATOR-VERIFICATION` | Incompatible declarations shall make the affected construction or invocation malformed. |
| `OLS2-REQ-0016` | `TEST-OLS2-0016` | `METHOD-SEMANTIC-VERIFICATION` | No precedence rule shall silently select one incompatible declaration over another. |
| `OLS2-REQ-0017` | `TEST-OLS2-0017` | `METHOD-SEMANTIC-VERIFICATION` | An unsupported declaration shall identify its unsupported status and the dependent claims it limits. |
| `OLS2-REQ-0018` | `TEST-OLS2-0018` | `METHOD-SEMANTIC-VERIFICATION` | An unsupported declaration shall not be silently promoted to observed, validated, canonical, or authoritative status. |
| `OLS2-REQ-0019` | `TEST-OLS2-0019` | `METHOD-OPERATOR-VERIFICATION` | An operator output shall preserve every input declaration whose distinction remains relevant to that output. |
| `OLS2-REQ-0020` | `TEST-OLS2-0020` | `METHOD-SEMANTIC-VERIFICATION` | Changing a declaration value or scope shall create an explicit new declaration state or reference and shall not overwrite the earlier value without trace. |
| `OLS2-REQ-0021` | `TEST-OLS2-0021` | `METHOD-SEMANTIC-VERIFICATION` | A declaration reference shall identify the Declaration ID, value or status, scope, and source or controlling record. |
| `OLS2-REQ-0022` | `TEST-OLS2-0022` | `METHOD-SEMANTIC-VERIFICATION` | Provenance shall be preserved as an OLS-1 universal status and shall not be introduced as an eleventh declaration. |
| `OLS2-REQ-0023` | `TEST-OLS2-0023` | `METHOD-SEMANTIC-VERIFICATION` | Each declaration shall retain the definition, responsibility, applicability, omission, incompatibility, preservation, and dependency rules of its owning subsection. |
| `OLS2-REQ-0024` | `TEST-OLS2-0024` | `METHOD-SEMANTIC-VERIFICATION` | A term not listed in Annex A shall not be represented as a Version 1.0 declaration. |
| `OLS2-REQ-0025` | `TEST-OLS2-0025` | `METHOD-SEMANTIC-VERIFICATION` | The examples in Clause 5 and Annex D are informative and shall not constrain the permitted declaration value forms. |
| `OLS2-REQ-0026` | `TEST-OLS2-0026` | `METHOD-SEMANTIC-VERIFICATION` | A time-dependent claim shall include `DECL-TIME`. |
| `OLS2-REQ-0027` | `TEST-OLS2-0027` | `METHOD-SEMANTIC-VERIFICATION` | A transition or before/after assertion without `DECL-TIME` shall be incomplete. |
| `OLS2-REQ-0028` | `TEST-OLS2-0028` | `METHOD-SEMANTIC-VERIFICATION` | Incompatible temporal orders for the same asserted sequence shall be malformed unless preserved as explicit disagreement or uncertainty. |
| `OLS2-REQ-0029` | `TEST-OLS2-0029` | `METHOD-OPERATOR-VERIFICATION` | An operator shall preserve the applicable temporal reference through its output. |
| `OLS2-REQ-0030` | `TEST-OLS2-0030` | `METHOD-SEMANTIC-VERIFICATION` | A continuity claim shall include `DECL-IDENTITY`. |
| `OLS2-REQ-0031` | `TEST-OLS2-0031` | `METHOD-SEMANTIC-VERIFICATION` | Identity shall not be inferred solely from naming, proximity, similarity, or sequence. |
| `OLS2-REQ-0032` | `TEST-OLS2-0032` | `METHOD-SEMANTIC-VERIFICATION` | Incompatible identity criteria within one continuity claim shall make that claim malformed. |
| `OLS2-REQ-0033` | `TEST-OLS2-0033` | `METHOD-OPERATOR-VERIFICATION` | An operator shall preserve the applicable identity criterion when its output asserts continuity. |
| `OLS2-REQ-0034` | `TEST-OLS2-0034` | `METHOD-SEMANTIC-VERIFICATION` | A scale-dependent or cross-scale claim shall include `DECL-SCALE`. |
| `OLS2-REQ-0035` | `TEST-OLS2-0035` | `METHOD-SEMANTIC-VERIFICATION` | Items at incompatible scales shall not be treated as directly comparable without an explicit compatible basis. |
| `OLS2-REQ-0036` | `TEST-OLS2-0036` | `METHOD-SEMANTIC-VERIFICATION` | Scale omission shall be valid only under the omission condition in this clause. |
| `OLS2-REQ-0037` | `TEST-OLS2-0037` | `METHOD-OPERATOR-VERIFICATION` | An operator shall preserve source scale when producing a result at another declared scale. |
| `OLS2-REQ-0038` | `TEST-OLS2-0038` | `METHOD-SEMANTIC-VERIFICATION` | Every orientation act and representation reading shall include `DECL-CONTEXT`. |
| `OLS2-REQ-0039` | `TEST-OLS2-0039` | `METHOD-SEMANTIC-VERIFICATION` | A claim shall not be generalized beyond its declared context without a separately declared and supported context. |
| `OLS2-REQ-0040` | `TEST-OLS2-0040` | `METHOD-SEMANTIC-VERIFICATION` | Incompatible contexts shall not be merged by omission or precedence. |
| `OLS2-REQ-0041` | `TEST-OLS2-0041` | `METHOD-OPERATOR-VERIFICATION` | An operator shall preserve source context when its output introduces a different context. |
| `OLS2-REQ-0042` | `TEST-OLS2-0042` | `METHOD-SEMANTIC-VERIFICATION` | Every representation and orientation claim shall include `DECL-PERSPECTIVE`. |
| `OLS2-REQ-0043` | `TEST-OLS2-0043` | `METHOD-SEMANTIC-VERIFICATION` | Construction and reading perspectives shall be distinguished when both apply. |
| `OLS2-REQ-0044` | `TEST-OLS2-0044` | `METHOD-SEMANTIC-VERIFICATION` | Incompatible perspectives shall remain separately identified unless an explicit compatible relation is supported. |
| `OLS2-REQ-0045` | `TEST-OLS2-0045` | `METHOD-OPERATOR-VERIFICATION` | An operator shall preserve perspective-specific agreements, disagreements, evidence, and uncertainty. |
| `OLS2-REQ-0046` | `TEST-OLS2-0046` | `METHOD-SEMANTIC-VERIFICATION` | A position-dependent assertion shall include `DECL-POSITION`. |
| `OLS2-REQ-0047` | `TEST-OLS2-0047` | `METHOD-SEMANTIC-VERIFICATION` | Position omission shall not authorize an inferred location. |
| `OLS2-REQ-0048` | `TEST-OLS2-0048` | `METHOD-SEMANTIC-VERIFICATION` | Incompatible positions for the same declared basis shall be malformed unless represented as distinct perspectives, times, or uncertainty. |
| `OLS2-REQ-0049` | `TEST-OLS2-0049` | `METHOD-OPERATOR-VERIFICATION` | An operator changing the relevant location shall preserve both source and resulting position references. |
| `OLS2-REQ-0050` | `TEST-OLS2-0050` | `METHOD-SEMANTIC-VERIFICATION` | Every REPRESENT output and represented ORIENT input shall include `DECL-REPRESENTATION-TYPE`. |
| `OLS2-REQ-0051` | `TEST-OLS2-0051` | `METHOD-SEMANTIC-VERIFICATION` | A representation type shall not be inferred from visual appearance, file format, or implementation technology alone. |
| `OLS2-REQ-0052` | `TEST-OLS2-0052` | `METHOD-SEMANTIC-VERIFICATION` | Incompatible representation types shall not be combined or compared without an explicit compatible basis. |
| `OLS2-REQ-0053` | `TEST-OLS2-0053` | `METHOD-SEMANTIC-VERIFICATION` | Type conversion shall preserve the source type, provenance, status, and uncertainty. |
| `OLS2-REQ-0054` | `TEST-OLS2-0054` | `METHOD-SEMANTIC-VERIFICATION` | Material used as evidence shall include `DECL-EVIDENCE-CLASS`. |
| `OLS2-REQ-0055` | `TEST-OLS2-0055` | `METHOD-SEMANTIC-VERIFICATION` | Model output, simulation, inference, proposal, or validation status shall not be represented as observed solely by relabeling its evidence class. |
| `OLS2-REQ-0056` | `TEST-OLS2-0056` | `METHOD-SEMANTIC-VERIFICATION` | Incompatible evidence classes shall remain visible as conflict, history, or uncertainty and shall not be silently collapsed. |
| `OLS2-REQ-0057` | `TEST-OLS2-0057` | `METHOD-OPERATOR-VERIFICATION` | An operator shall preserve evidence class through every output that uses or communicates the material. |
| `OLS2-REQ-0058` | `TEST-OLS2-0058` | `METHOD-SEMANTIC-VERIFICATION` | Every comparison, orientation, explanation, validation, or report finding shall include `DECL-UNCERTAINTY-STATUS`. |
| `OLS2-REQ-0059` | `TEST-OLS2-0059` | `METHOD-SEMANTIC-VERIFICATION` | Uncertainty shall not be silently replaced by confidence or certainty. |
| `OLS2-REQ-0060` | `TEST-OLS2-0060` | `METHOD-SEMANTIC-VERIFICATION` | Incompatible uncertainty statuses shall be preserved as explicit conflict or scoped difference. |
| `OLS2-REQ-0061` | `TEST-OLS2-0061` | `METHOD-OPERATOR-VERIFICATION` | An operator shall preserve known limitations, missing information, disagreement, and unresolved status relevant to its output. |
| `OLS2-REQ-0062` | `TEST-OLS2-0062` | `METHOD-SEMANTIC-VERIFICATION` | A governed act or authority claim shall include `DECL-AUTHORITY-SCOPE`. |
| `OLS2-REQ-0063` | `TEST-OLS2-0063` | `METHOD-SEMANTIC-VERIFICATION` | Orientation, evidence, validation, or explanation shall not be treated as authority. |
| `OLS2-REQ-0064` | `TEST-OLS2-0064` | `METHOD-OPERATOR-VERIFICATION` | Incompatible authority scopes shall not be resolved by operator order or implementation precedence. |
| `OLS2-REQ-0065` | `TEST-OLS2-0065` | `METHOD-SEMANTIC-VERIFICATION` | An authority-bearing output shall preserve actor or role, governed operation, target, scope, and authority status. |
| `OLS2-REQ-0066` | `TEST-OLS2-0066` | `METHOD-OPERATOR-VERIFICATION` | A primitive operator contract shall identify purpose, semantic owner, inputs, required declarations, preconditions, operation, outputs, preserved status, failure conditions, prohibited implications, and traceability. |
| `OLS2-REQ-0067` | `TEST-OLS2-0067` | `METHOD-OPERATOR-VERIFICATION` | Contract fields shall describe semantic obligations independently of software, data format, interface, storage, or execution technology. |
| `OLS2-REQ-0068` | `TEST-OLS2-0068` | `METHOD-OPERATOR-VERIFICATION` | A contract shall not change its owner’s frozen semantic responsibility. |
| `OLS2-REQ-0069` | `TEST-OLS2-0069` | `METHOD-OPERATOR-VERIFICATION` | Inputs shall identify the semantic material accepted by the operator without implying implementation types. |
| `OLS2-REQ-0070` | `TEST-OLS2-0070` | `METHOD-OPERATOR-VERIFICATION` | Required declarations shall include every Annex A distinction on which the invocation or output depends. |
| `OLS2-REQ-0071` | `TEST-OLS2-0071` | `METHOD-OPERATOR-VERIFICATION` | Preconditions shall be satisfied before an invocation is treated as complete. |
| `OLS2-REQ-0072` | `TEST-OLS2-0072` | `METHOD-SEMANTIC-VERIFICATION` | Outputs shall identify semantic products and preserved statuses without implying successful external execution. |
| `OLS2-REQ-0073` | `TEST-OLS2-0073` | `METHOD-SEMANTIC-VERIFICATION` | Preserved status shall include applicable provenance, evidence class, uncertainty, declarations, disagreements, and limitations. |
| `OLS2-REQ-0074` | `TEST-OLS2-0074` | `METHOD-SEMANTIC-VERIFICATION` | Failure conditions shall classify missing requirements as incomplete and incompatible or boundary-violating assertions as malformed under Clause 12. |
| `OLS2-REQ-0075` | `TEST-OLS2-0075` | `METHOD-OPERATOR-VERIFICATION` | Prohibited implications shall remain valid regardless of implementation behavior or operator composition. |
| `OLS2-REQ-0076` | `TEST-OLS2-0076` | `METHOD-OPERATOR-VERIFICATION` | Every universal primitive invocation shall preserve the OLS-1 Universal Boundary Matrix. |
| `OLS2-REQ-0077` | `TEST-OLS2-0077` | `METHOD-OPERATOR-VERIFICATION` | Operational detail in Clause 7 shall not broaden a universal operator responsibility. |
| `OLS2-REQ-0078` | `TEST-OLS2-0078` | `METHOD-SEMANTIC-VERIFICATION` | OBSERVE shall not create evidence, validation, or outcome status solely by admission. |
| `OLS2-REQ-0079` | `TEST-OLS2-0079` | `METHOD-SEMANTIC-VERIFICATION` | OBSERVE shall preserve the source and epistemic status of every output observation. |
| `OLS2-REQ-0080` | `TEST-OLS2-0080` | `METHOD-SEMANTIC-VERIFICATION` | REPRESENT shall identify its output as a representation and shall preserve the representation/reality distinction. |
| `OLS2-REQ-0081` | `TEST-OLS2-0081` | `METHOD-SEMANTIC-VERIFICATION` | REPRESENT shall not change the evidence or uncertainty status of input material unless a separately owned operation supports that change. |
| `OLS2-REQ-0082` | `TEST-OLS2-0082` | `METHOD-SEMANTIC-VERIFICATION` | COMPARE shall identify every compared item and the comparison basis. |
| `OLS2-REQ-0083` | `TEST-OLS2-0083` | `METHOD-SEMANTIC-VERIFICATION` | COMPARE shall depend on the universal primitive difference and shall not define or generate its semantic responsibility. |
| `OLS2-REQ-0084` | `TEST-OLS2-0084` | `METHOD-SEMANTIC-VERIFICATION` | ORIENT shall identify the declared basis and limits of its situated understanding. |
| `OLS2-REQ-0085` | `TEST-OLS2-0085` | `METHOD-SEMANTIC-VERIFICATION` | ORIENT shall preserve supported findings, disagreements, unsupported conclusions, and uncertainty as distinct statuses. |
| `OLS2-REQ-0086` | `TEST-OLS2-0086` | `METHOD-SEMANTIC-VERIFICATION` | EXPLAIN shall preserve the status of every finding it communicates. |
| `OLS2-REQ-0087` | `TEST-OLS2-0087` | `METHOD-SEMANTIC-VERIFICATION` | EXPLAIN shall not convert communication into proof, consensus, authority, recommendation, or approval. |
| `OLS2-REQ-0088` | `TEST-OLS2-0088` | `METHOD-OPERATOR-VERIFICATION` | Invocation of a profile primitive operator shall refer to its owner and applicable profile rules in OLS-3. |
| `OLS2-REQ-0089` | `TEST-OLS2-0089` | `METHOD-OPERATOR-VERIFICATION` | A profile primitive operator shall not modify a universal concept, operator responsibility, or boundary. |
| `OLS2-REQ-0090` | `TEST-OLS2-0090` | `METHOD-SEMANTIC-VERIFICATION` | Clause 8 shall not be interpreted as profile activation or profile composition semantics. |
| `OLS2-REQ-0091` | `TEST-OLS2-0091` | `METHOD-SEMANTIC-VERIFICATION` | SELECT shall report the alternatives and declared basis under which selection occurred. |
| `OLS2-REQ-0092` | `TEST-OLS2-0092` | `METHOD-SEMANTIC-VERIFICATION` | SELECT shall not convert possibility or selection into recommendation, authority, execution, or optimality. |
| `OLS2-REQ-0093` | `TEST-OLS2-0093` | `METHOD-SEMANTIC-VERIFICATION` | TRANSFORM shall preserve distinct input and resulting form or state references. |
| `OLS2-REQ-0094` | `TEST-OLS2-0094` | `METHOD-SEMANTIC-VERIFICATION` | TRANSFORM shall not establish validation, admitted outcome, improvement, authorization, or execution success. |
| `OLS2-REQ-0095` | `TEST-OLS2-0095` | `METHOD-SEMANTIC-VERIFICATION` | VALIDATE shall report its subject, criteria, evidence, and validation status within one declared scope. |
| `OLS2-REQ-0096` | `TEST-OLS2-0096` | `METHOD-SEMANTIC-VERIFICATION` | VALIDATE shall not establish authority, publication, universal proof, or admitted outcome solely by producing validation status. |
| `OLS2-REQ-0097` | `TEST-OLS2-0097` | `METHOD-SEMANTIC-VERIFICATION` | RECORD shall preserve the declared status of recorded material and shall not upgrade that status. |
| `OLS2-REQ-0098` | `TEST-OLS2-0098` | `METHOD-SEMANTIC-VERIFICATION` | RECORD shall not establish experiential learning solely by persistence. |
| `OLS2-REQ-0099` | `TEST-OLS2-0099` | `METHOD-OPERATOR-VERIFICATION` | APPROVE shall limit its output to the governed status and authority scope declared for the invocation. |
| `OLS2-REQ-0100` | `TEST-OLS2-0100` | `METHOD-SEMANTIC-VERIFICATION` | APPROVE shall not convert editorial or governed approval into empirical truth or validation. |
| `OLS2-REQ-0101` | `TEST-OLS2-0101` | `METHOD-OPERATOR-VERIFICATION` | Every primitive operator shall resolve to exactly one semantic owner. |
| `OLS2-REQ-0102` | `TEST-OLS2-0102` | `METHOD-OPERATOR-VERIFICATION` | An owner shall control the operator’s semantic responsibility, contract, boundaries, and prohibited implications. |
| `OLS2-REQ-0103` | `TEST-OLS2-0103` | `METHOD-OPERATOR-VERIFICATION` | A reference to an operator shall use its Operator ID and shall retain the owner’s contract. |
| `OLS2-REQ-0104` | `TEST-OLS2-0104` | `METHOD-OPERATOR-VERIFICATION` | Referencing an operator shall not transfer ownership. |
| `OLS2-REQ-0105` | `TEST-OLS2-0105` | `METHOD-OPERATOR-VERIFICATION` | A downstream profile, implementation, application, example, or extension shall not supply a second definition for a Version 1.0 primitive operator. |
| `OLS2-REQ-0106` | `TEST-OLS2-0106` | `METHOD-OPERATOR-VERIFICATION` | A derived or specialized operator shall identify the primitive capability and owner from which it derives under the owning profile specification. |
| `OLS2-REQ-0107` | `TEST-OLS2-0107` | `METHOD-OPERATOR-VERIFICATION` | An implementation function, visual operator, human role, or historical operator name shall not acquire primitive ownership. |
| `OLS2-REQ-0108` | `TEST-OLS2-0108` | `METHOD-OPERATOR-VERIFICATION` | An ownership conflict shall make the affected invocation malformed. |
| `OLS2-REQ-0109` | `TEST-OLS2-0109` | `METHOD-OPERATOR-VERIFICATION` | An invocation shall identify exactly one primitive Operator ID. |
| `OLS2-REQ-0110` | `TEST-OLS2-0110` | `METHOD-OPERATOR-VERIFICATION` | An invocation shall satisfy every applicable contract precondition before its output is treated as complete. |
| `OLS2-REQ-0111` | `TEST-OLS2-0111` | `METHOD-OPERATOR-VERIFICATION` | An invocation shall include every declaration required by its contract and actual claims. |
| `OLS2-REQ-0112` | `TEST-OLS2-0112` | `METHOD-OPERATOR-VERIFICATION` | An invocation shall preserve input status required by its contract. |
| `OLS2-REQ-0113` | `TEST-OLS2-0113` | `METHOD-OPERATOR-VERIFICATION` | An invocation shall identify unsupported inputs or declarations and shall limit dependent output accordingly. |
| `OLS2-REQ-0114` | `TEST-OLS2-0114` | `METHOD-OPERATOR-VERIFICATION` | An invocation shall not claim semantic effects outside its operator contract. |
| `OLS2-REQ-0115` | `TEST-OLS2-0115` | `METHOD-OPERATOR-VERIFICATION` | A human procedure and a computational realization shall be evaluated against the same semantic invocation fields. |
| `OLS2-REQ-0116` | `TEST-OLS2-0116` | `METHOD-OPERATOR-VERIFICATION` | Invocation order shall not create authority, validation, outcome, or learning absent the separately owned operator and conditions. |
| `OLS2-REQ-0117` | `TEST-OLS2-0117` | `METHOD-OPERATOR-VERIFICATION` | A profile primitive invocation shall reference its active owner under OLS-3 without redefining that profile. |
| `OLS2-REQ-0118` | `TEST-OLS2-0118` | `METHOD-OPERATOR-VERIFICATION` | Invocation syntax and serialization may vary by implementation, but their semantic mapping shall remain explicit. |
| `OLS2-REQ-0119` | `TEST-OLS2-0119` | `METHOD-OPERATOR-VERIFICATION` | An invocation record need not prescribe scheduling, storage, transport, user interface, or runtime architecture. |
| `OLS2-REQ-0120` | `TEST-OLS2-0120` | `METHOD-OPERATOR-VERIFICATION` | Every composed invocation shall remain independently attributable to its Operator ID and owner. |
| `OLS2-REQ-0121` | `TEST-OLS2-0121` | `METHOD-SEMANTIC-VERIFICATION` | An output shall be used as a later input only when semantic type, status, declarations, context, perspective, identity, time, scale, and representation basis are compatible as applicable. |
| `OLS2-REQ-0122` | `TEST-OLS2-0122` | `METHOD-OPERATOR-VERIFICATION` | Composition shall preserve provenance from each source invocation. |
| `OLS2-REQ-0123` | `TEST-OLS2-0123` | `METHOD-SEMANTIC-VERIFICATION` | Composition shall not erase an unsupported, incomplete, malformed, uncertain, or conflicting status. |
| `OLS2-REQ-0124` | `TEST-OLS2-0124` | `METHOD-OPERATOR-VERIFICATION` | The universal operators shall follow the OLS-1 canonical order when a complete universal process is claimed. |
| `OLS2-REQ-0125` | `TEST-OLS2-0125` | `METHOD-OPERATOR-VERIFICATION` | A profile primitive operator shall compose only under OLS-3 profile activation and dependency rules. |
| `OLS2-REQ-0126` | `TEST-OLS2-0126` | `METHOD-OPERATOR-VERIFICATION` | Operator order shall not act as a precedence rule for incompatible declarations or ownership conflicts. |
| `OLS2-REQ-0127` | `TEST-OLS2-0127` | `METHOD-OPERATOR-VERIFICATION` | Composition shall not be interpreted as external execution architecture, causality, validation, authority, outcome, or learning unless the applicable owned contracts and conditions establish that status. |
| `OLS2-REQ-0128` | `TEST-OLS2-0128` | `METHOD-OPERATOR-VERIFICATION` | A composed sequence shall identify its semantic invocation order without prescribing implementation scheduling. |
| `OLS2-REQ-0129` | `TEST-OLS2-0129` | `METHOD-OPERATOR-VERIFICATION` | Missing required declarations shall make an invocation incomplete. |
| `OLS2-REQ-0130` | `TEST-OLS2-0130` | `METHOD-OPERATOR-VERIFICATION` | Incompatible declarations shall make an invocation malformed. |
| `OLS2-REQ-0131` | `TEST-OLS2-0131` | `METHOD-SEMANTIC-VERIFICATION` | Unsupported declarations shall remain explicit and shall not be treated as satisfying supported preconditions. |
| `OLS2-REQ-0132` | `TEST-OLS2-0132` | `METHOD-OPERATOR-VERIFICATION` | A missing operator owner or active owner-profile reference shall make a profile primitive invocation incomplete. |
| `OLS2-REQ-0133` | `TEST-OLS2-0133` | `METHOD-OPERATOR-VERIFICATION` | A second or conflicting operator owner shall make an invocation malformed. |
| `OLS2-REQ-0134` | `TEST-OLS2-0134` | `METHOD-OPERATOR-VERIFICATION` | Omission of provenance or source status required by a contract shall make an invocation incomplete even though provenance is not an Annex A declaration. |
| `OLS2-REQ-0135` | `TEST-OLS2-0135` | `METHOD-OPERATOR-VERIFICATION` | Silent evidence-class promotion, uncertainty removal, authority expansion, or input/output collapse shall make an invocation malformed. |
| `OLS2-REQ-0136` | `TEST-OLS2-0136` | `METHOD-OPERATOR-VERIFICATION` | Failure of one invocation shall remain visible to every dependent invocation. |
| `OLS2-REQ-0137` | `TEST-OLS2-0137` | `METHOD-OPERATOR-VERIFICATION` | An incomplete invocation may be completed only with supported missing material under the owning contract. |
| `OLS2-REQ-0138` | `TEST-OLS2-0138` | `METHOD-OPERATOR-VERIFICATION` | A malformed invocation shall not be repaired by inferred declarations, operator precedence, implementation behavior, or informative examples. |
| `OLS2-REQ-0139` | `TEST-OLS2-0139` | `METHOD-SEMANTIC-VERIFICATION` | OLS-2 failure states shall not be represented as OLS-5 conformance results until evaluated under OLS-5. |
| `OLS2-REQ-0140` | `TEST-OLS2-0140` | `METHOD-OPERATOR-VERIFICATION` | A Version 1.0 declaration or primitive operator invocation shall resolve to the applicable OLS-2 registry and owning clause. |
| `OLS2-REQ-0141` | `TEST-OLS2-0141` | `METHOD-REGISTRY-VERIFICATION` | OLS-2 shall add operational precision without changing OLS-1 semantics or Phase 2D ownership. |
| `OLS2-REQ-0142` | `TEST-OLS2-0142` | `METHOD-SEMANTIC-VERIFICATION` | OLS-2 semantics shall remain independent of implementation technology and downstream profile, derivation, conformance, and governance specifications. |
| `OLS2-REQ-0143` | `TEST-OLS2-0143` | `METHOD-SEMANTIC-VERIFICATION` | Annex A shall contain exactly ten Version 1.0 declaration entries. |
| `OLS2-REQ-0144` | `TEST-OLS2-0144` | `METHOD-SEMANTIC-VERIFICATION` | A declaration shall not be added, removed, or assigned a new responsibility without the applicable Architecture Revision Process. |
| `OLS2-REQ-0145` | `TEST-OLS2-0145` | `METHOD-SEMANTIC-VERIFICATION` | A declaration reference shall use the registered Declaration ID. |
| `OLS2-REQ-0146` | `TEST-OLS2-0146` | `METHOD-OPERATOR-VERIFICATION` | Annex B shall contain exactly ten Version 1.0 primitive operators with exactly one owner each. |
| `OLS2-REQ-0147` | `TEST-OLS2-0147` | `METHOD-OPERATOR-VERIFICATION` | A registered Operator ID shall not be reassigned or given a second contract. |
| `OLS2-REQ-0148` | `TEST-OLS2-0148` | `METHOD-OPERATOR-VERIFICATION` | Every primitive operator reference shall resolve to the contract and owner in Annex B. |
| `OLS2-REQ-0149` | `TEST-OLS2-0149` | `METHOD-OPERATOR-VERIFICATION` | Every primitive operator contract shall contain all eleven fields in Annex C. |
| `OLS2-REQ-0150` | `TEST-OLS2-0150` | `METHOD-SEMANTIC-VERIFICATION` | An empty or inapplicable field shall state why it is inapplicable and shall not be silently omitted. |
| `OLS3-REQ-0001` | `TEST-OLS3-0001` | `METHOD-PROFILE-VERIFICATION` | OLS-3 shall contain exactly the seven profiles registered in Annex A. |
| `OLS3-REQ-0002` | `TEST-OLS3-0002` | `METHOD-PROFILE-VERIFICATION` | OLS-3 shall preserve OLS-1 universal semantics and OLS-2 declarations, primitive operator contracts, and ownership. |
| `OLS3-REQ-0003` | `TEST-OLS3-0003` | `METHOD-PROFILE-VERIFICATION` | OLS-3 shall not define derivations, conformance procedures, governance changes, or implementation architecture. |
| `OLS3-REQ-0004` | `TEST-OLS3-0004` | `METHOD-PROFILE-VERIFICATION` | A need for a new profile or changed profile responsibility shall be referred to an Architecture Revision Process. |
| `OLS3-REQ-0005` | `TEST-OLS3-0005` | `METHOD-PROFILE-VERIFICATION` | OLS-3 shall apply OLS-0 conventions, inherit OLS-1 without modification, and reference OLS-2 declarations and operator contracts by stable identifier. |
| `OLS3-REQ-0006` | `TEST-OLS3-0006` | `METHOD-PROFILE-VERIFICATION` | Profile terminology shall not add a universal concept or alter an OLS-1 definition. |
| `OLS3-REQ-0007` | `TEST-OLS3-0007` | `METHOD-PROFILE-VERIFICATION` | Profile operator names shall resolve to OLS-2 contracts and shall not be redefined in OLS-3. |
| `OLS3-REQ-0008` | `TEST-OLS3-0008` | `METHOD-PROFILE-VERIFICATION` | Declaration names shall resolve to OLS-2 and shall not acquire new value domains, defaults, or omission rules in OLS-3. |
| `OLS3-REQ-0009` | `TEST-OLS3-0009` | `METHOD-PROFILE-VERIFICATION` | A conditional dependency shall become active only under its stated condition and shall otherwise remain inactive. |
| `OLS3-REQ-0010` | `TEST-OLS3-0010` | `METHOD-PROFILE-VERIFICATION` | Every profile shall inherit the complete Universal Base Language. |
| `OLS3-REQ-0011` | `TEST-OLS3-0011` | `METHOD-PROFILE-VERIFICATION` | A profile shall add only semantics assigned to it by its authoritative profile clause. |
| `OLS3-REQ-0012` | `TEST-OLS3-0012` | `METHOD-PROFILE-VERIFICATION` | A profile shall not replace, weaken, or redefine inherited semantics. |
| `OLS3-REQ-0013` | `TEST-OLS3-0013` | `METHOD-PROFILE-VERIFICATION` | A profile shall have one Profile ID and one purpose. |
| `OLS3-REQ-0014` | `TEST-OLS3-0014` | `METHOD-PROFILE-VERIFICATION` | A primitive concept or primitive operator shall have exactly one semantic owner. |
| `OLS3-REQ-0015` | `TEST-OLS3-0015` | `METHOD-PROFILE-VERIFICATION` | Referencing owned semantics shall not transfer ownership. |
| `OLS3-REQ-0016` | `TEST-OLS3-0016` | `METHOD-PROFILE-VERIFICATION` | A profile shall identify every applicable OLS-2 declaration without reproducing its definition. |
| `OLS3-REQ-0017` | `TEST-OLS3-0017` | `METHOD-PROFILE-VERIFICATION` | A profile shall identify mandatory dependencies and the conditions of every conditional dependency. |
| `OLS3-REQ-0018` | `TEST-OLS3-0018` | `METHOD-PROFILE-VERIFICATION` | Profile composition shall add semantics and shall not silently remove inherited or concurrently active semantics. |
| `OLS3-REQ-0019` | `TEST-OLS3-0019` | `METHOD-PROFILE-VERIFICATION` | Profile status shall not be inferred from similar words, metaphors, visual forms, implementation technologies, or historical usage. |
| `OLS3-REQ-0020` | `TEST-OLS3-0020` | `METHOD-PROFILE-VERIFICATION` | A profile shall identify its active state and unresolved conflicts in every profile-based orientation artifact. |
| `OLS3-REQ-0021` | `TEST-OLS3-0021` | `METHOD-PROFILE-VERIFICATION` | A profile shall not claim empirical validation, authorization, successful execution, or implementation compatibility merely because it is active. |
| `OLS3-REQ-0022` | `TEST-OLS3-0022` | `METHOD-PROFILE-VERIFICATION` | A profile shall remain implementation independent. |
| `OLS3-REQ-0023` | `TEST-OLS3-0023` | `METHOD-PROFILE-VERIFICATION` | Every active profile shall inherit OLS-1 before its own semantics are applied. |
| `OLS3-REQ-0024` | `TEST-OLS3-0024` | `METHOD-PROFILE-VERIFICATION` | Invoking an owned primitive concept or operator shall activate its owner profile. |
| `OLS3-REQ-0025` | `TEST-OLS3-0025` | `METHOD-PROFILE-VERIFICATION` | Activating a profile shall activate every mandatory dependency in Annex B. |
| `OLS3-REQ-0026` | `TEST-OLS3-0026` | `METHOD-PROFILE-VERIFICATION` | A conditional dependency shall activate when its stated condition becomes true. |
| `OLS3-REQ-0027` | `TEST-OLS3-0027` | `METHOD-PROFILE-VERIFICATION` | A profile with no owned primitive concept or primitive operator shall be activated explicitly by Profile ID. |
| `OLS3-REQ-0028` | `TEST-OLS3-0028` | `METHOD-PROFILE-VERIFICATION` | An inactive profile shall contribute no profile-specific semantics to the construction. |
| `OLS3-REQ-0029` | `TEST-OLS3-0029` | `METHOD-PROFILE-VERIFICATION` | Reference to an operator owned by another profile shall activate that operator’s owner and its mandatory dependencies. |
| `OLS3-REQ-0030` | `TEST-OLS3-0030` | `METHOD-PROFILE-VERIFICATION` | Reference to a profile primitive concept shall activate that concept’s owner and its mandatory dependencies. |
| `OLS3-REQ-0031` | `TEST-OLS3-0031` | `METHOD-PROFILE-VERIFICATION` | Activation shall not modify any universal or previously owned semantic responsibility. |
| `OLS3-REQ-0032` | `TEST-OLS3-0032` | `METHOD-PROFILE-VERIFICATION` | A construction shall report explicit activation separately from dependency activation. |
| `OLS3-REQ-0033` | `TEST-OLS3-0033` | `METHOD-PROFILE-VERIFICATION` | A profile shall not be inferred solely because an implementation supports its Operator ID. |
| `OLS3-REQ-0034` | `TEST-OLS3-0034` | `METHOD-PROFILE-VERIFICATION` | An unresolved activation condition shall make the affected profile composition incomplete. |
| `OLS3-REQ-0035` | `TEST-OLS3-0035` | `METHOD-PROFILE-VERIFICATION` | Every dependency shall resolve before the dependent profile operation is treated as complete. |
| `OLS3-REQ-0036` | `TEST-OLS3-0036` | `METHOD-PROFILE-VERIFICATION` | Mandatory dependencies shall be active whenever their dependent profile is active. |
| `OLS3-REQ-0037` | `TEST-OLS3-0037` | `METHOD-PROFILE-VERIFICATION` | Conditional dependencies shall identify their activation condition in the profile report. |
| `OLS3-REQ-0038` | `TEST-OLS3-0038` | `METHOD-PROFILE-VERIFICATION` | A profile at the same dependency level may compose with another only when declarations, ownership, representations, and operator contracts are compatible. |
| `OLS3-REQ-0039` | `TEST-OLS3-0039` | `METHOD-PROFILE-VERIFICATION` | An absent mandatory dependency shall make the composition incomplete. |
| `OLS3-REQ-0040` | `TEST-OLS3-0040` | `METHOD-PROFILE-VERIFICATION` | An absent conditional dependency after its condition is met shall make the affected composition incomplete. |
| `OLS3-REQ-0041` | `TEST-OLS3-0041` | `METHOD-PROFILE-VERIFICATION` | A dependency shall not redefine its dependent profile, and a dependent profile shall not redefine its dependency. |
| `OLS3-REQ-0042` | `TEST-OLS3-0042` | `METHOD-PROFILE-VERIFICATION` | Dependency activation shall not transfer primitive concept or operator ownership. |
| `OLS3-REQ-0043` | `TEST-OLS3-0043` | `METHOD-PROFILE-VERIFICATION` | A dependency cycle shall make the composition malformed. |
| `OLS3-REQ-0044` | `TEST-OLS3-0044` | `METHOD-PROFILE-VERIFICATION` | No dependency precedence shall override incompatible declarations or semantic ownership. |
| `OLS3-REQ-0045` | `TEST-OLS3-0045` | `METHOD-PROFILE-VERIFICATION` | Conditional dependencies not triggered by the active construction shall remain inactive and need not be reported as active. |
| `OLS3-REQ-0046` | `TEST-OLS3-0046` | `METHOD-PROFILE-VERIFICATION` | Every activated dependency shall appear in the active-profile report. |
| `OLS3-REQ-0047` | `TEST-OLS3-0047` | `METHOD-PROFILE-VERIFICATION` | Annex B shall control Version 1.0 dependency classification. |
| `OLS3-REQ-0048` | `TEST-OLS3-0048` | `METHOD-PROFILE-VERIFICATION` | Every legal composition shall satisfy all nine conditions in Clause 7. |
| `OLS3-REQ-0049` | `TEST-OLS3-0049` | `METHOD-PROFILE-VERIFICATION` | Profiles shall compose additively through inherited and owned semantics, not by override. |
| `OLS3-REQ-0050` | `TEST-OLS3-0050` | `METHOD-PROFILE-VERIFICATION` | Every referenced primitive operator shall retain its OLS-2 contract and owner. |
| `OLS3-REQ-0051` | `TEST-OLS3-0051` | `METHOD-PROFILE-VERIFICATION` | Every referenced profile primitive concept shall retain its Annex C definition and owner. |
| `OLS3-REQ-0052` | `TEST-OLS3-0052` | `METHOD-PROFILE-VERIFICATION` | Applicable OLS-2 declarations shall retain their values, scopes, source, and unsupported status through composition. |
| `OLS3-REQ-0053` | `TEST-OLS3-0053` | `METHOD-PROFILE-VERIFICATION` | Composition shall preserve OLS-1 evidence class, provenance, uncertainty, disagreement, unsupported conclusions, and limitations. |
| `OLS3-REQ-0054` | `TEST-OLS3-0054` | `METHOD-PROFILE-VERIFICATION` | Representation compatibility shall be explicit and shall not be inferred from visual or implementation similarity. |
| `OLS3-REQ-0055` | `TEST-OLS3-0055` | `METHOD-PROFILE-VERIFICATION` | A composition shall identify every conditional dependency whose activation condition is met. |
| `OLS3-REQ-0056` | `TEST-OLS3-0056` | `METHOD-PROFILE-VERIFICATION` | A profile may reference another profile’s operator or primitive concept only through the authoritative owner. |
| `OLS3-REQ-0057` | `TEST-OLS3-0057` | `METHOD-PROFILE-VERIFICATION` | Composition shall not imply implementation compatibility, empirical validation, authorization, or successful execution. |
| `OLS3-REQ-0058` | `TEST-OLS3-0058` | `METHOD-PROFILE-VERIFICATION` | A legal composition need not activate profiles not required by its claims, owned semantics, or dependencies. |
| `OLS3-REQ-0059` | `TEST-OLS3-0059` | `METHOD-PROFILE-VERIFICATION` | No profile shall acquire universal status through frequent composition. |
| `OLS3-REQ-0060` | `TEST-OLS3-0060` | `METHOD-PROFILE-VERIFICATION` | OLS-3 composition shall not add an operator to the OLS-1 canonical universal process. |
| `OLS3-REQ-0061` | `TEST-OLS3-0061` | `METHOD-PROFILE-VERIFICATION` | An unresolved conflict shall make the profile composition malformed. |
| `OLS3-REQ-0062` | `TEST-OLS3-0062` | `METHOD-PROFILE-VERIFICATION` | No profile, document order, operator order, declaration order, or implementation behavior shall override a conflict. |
| `OLS3-REQ-0063` | `TEST-OLS3-0063` | `METHOD-PROFILE-VERIFICATION` | Ownership conflict shall be evaluated against OLS-2 Annex B and OLS-3 Annex C. |
| `OLS3-REQ-0064` | `TEST-OLS3-0064` | `METHOD-PROFILE-VERIFICATION` | Declaration conflict shall be evaluated against OLS-2 without redefining declaration semantics. |
| `OLS3-REQ-0065` | `TEST-OLS3-0065` | `METHOD-PROFILE-VERIFICATION` | Dependency conflict shall identify the missing, circular, or incompatible dependency. |
| `OLS3-REQ-0066` | `TEST-OLS3-0066` | `METHOD-PROFILE-VERIFICATION` | Prohibited modification shall identify the inherited or owned semantic element affected. |
| `OLS3-REQ-0067` | `TEST-OLS3-0067` | `METHOD-PROFILE-VERIFICATION` | Representation conflict shall identify the incompatible declarations, types, or bases. |
| `OLS3-REQ-0068` | `TEST-OLS3-0068` | `METHOD-PROFILE-VERIFICATION` | A conflict shall remain visible in the active-profile report. |
| `OLS3-REQ-0069` | `TEST-OLS3-0069` | `METHOD-PROFILE-VERIFICATION` | Explicit disagreement or uncertainty shall not be classified as conflict when all active semantics and declarations remain compatible. |
| `OLS3-REQ-0070` | `TEST-OLS3-0070` | `METHOD-PROFILE-VERIFICATION` | Rewording an owned semantic element shall not resolve a substantive ownership conflict. |
| `OLS3-REQ-0071` | `TEST-OLS3-0071` | `METHOD-PROFILE-VERIFICATION` | An incomplete dependency state shall become malformed if the construction claims completion despite the unresolved dependency. |
| `OLS3-REQ-0072` | `TEST-OLS3-0072` | `METHOD-PROFILE-VERIFICATION` | Conflict repair shall use the controlling owner or declaration and shall not invent missing semantics. |
| `OLS3-REQ-0073` | `TEST-OLS3-0073` | `METHOD-PROFILE-VERIFICATION` | A profile report shall identify the suite version and every active Profile ID. |
| `OLS3-REQ-0074` | `TEST-OLS3-0074` | `METHOD-PROFILE-VERIFICATION` | The Universal Base Language shall be reported as inherited and shall not be reported as a profile. |
| `OLS3-REQ-0075` | `TEST-OLS3-0075` | `METHOD-PROFILE-VERIFICATION` | Explicit activation and dependency activation shall remain distinguishable. |
| `OLS3-REQ-0076` | `TEST-OLS3-0076` | `METHOD-PROFILE-VERIFICATION` | Referenced operators shall identify their OLS-2 Operator IDs and owners. |
| `OLS3-REQ-0077` | `TEST-OLS3-0077` | `METHOD-PROFILE-VERIFICATION` | Owned primitive concepts shall identify their Annex C Term IDs and owners. |
| `OLS3-REQ-0078` | `TEST-OLS3-0078` | `METHOD-PROFILE-VERIFICATION` | Declaration references shall use OLS-2 Declaration IDs without duplicating declaration values outside their declared scope. |
| `OLS3-REQ-0079` | `TEST-OLS3-0079` | `METHOD-PROFILE-VERIFICATION` | Unresolved conflicts and missing dependencies shall not be omitted from a report that claims the affected composition. |
| `OLS3-REQ-0080` | `TEST-OLS3-0080` | `METHOD-PROFILE-VERIFICATION` | If no extension profile is active, the artifact shall report only the Universal Base Language and applicable OLS-2 declarations. |
| `OLS3-REQ-0081` | `TEST-OLS3-0081` | `METHOD-PROFILE-VERIFICATION` | Reporting shall not itself activate a profile or change semantic status. |
| `OLS3-REQ-0082` | `TEST-OLS3-0082` | `METHOD-PROFILE-VERIFICATION` | Every profile shall use the Profile ID and canonical name in Annex A. |
| `OLS3-REQ-0083` | `TEST-OLS3-0083` | `METHOD-PROFILE-VERIFICATION` | Each profile shall retain the fields and boundaries in its owning subsection. |
| `OLS3-REQ-0084` | `TEST-OLS3-0084` | `METHOD-PROFILE-VERIFICATION` | No other component shall claim Version 1.0 semantic profile status. |
| `OLS3-REQ-0085` | `TEST-OLS3-0085` | `METHOD-PROFILE-VERIFICATION` | Representation shall be activated explicitly because it owns no primitive concept or primitive operator. |
| `OLS3-REQ-0086` | `TEST-OLS3-0086` | `METHOD-PROFILE-VERIFICATION` | Representation shall preserve the OLS-1 representation/reality boundary. |
| `OLS3-REQ-0087` | `TEST-OLS3-0087` | `METHOD-PROFILE-VERIFICATION` | Representation shall not acquire ownership of `OP-REPRESENT` or another universal operator. |
| `OLS3-REQ-0088` | `TEST-OLS3-0088` | `METHOD-PROFILE-VERIFICATION` | Representation shall not infer compatibility from visual form or implementation type. |
| `OLS3-REQ-0089` | `TEST-OLS3-0089` | `METHOD-PROFILE-VERIFICATION` | Representation composition shall retain all source representation types, perspectives, provenance, and applicable scales. |
| `OLS3-REQ-0090` | `TEST-OLS3-0090` | `METHOD-PROFILE-VERIFICATION` | Navigation shall own `TERM-CONSTRAINT` and `OP-SELECT` exclusively. |
| `OLS3-REQ-0091` | `TEST-OLS3-0091` | `METHOD-PROFILE-VERIFICATION` | Navigation shall activate Representation as a mandatory dependency. |
| `OLS3-REQ-0092` | `TEST-OLS3-0092` | `METHOD-PROFILE-VERIFICATION` | Referencing `OP-TRANSFORM` or `OP-RECORD` shall activate the owning profile under its stated condition. |
| `OLS3-REQ-0093` | `TEST-OLS3-0093` | `METHOD-PROFILE-VERIFICATION` | Navigation shall preserve the difference between a possible, selected, recommended, authorized, and executed path. |
| `OLS3-REQ-0094` | `TEST-OLS3-0094` | `METHOD-PROFILE-VERIFICATION` | Navigation shall not claim optimality solely from selection. |
| `OLS3-REQ-0095` | `TEST-OLS3-0095` | `METHOD-PROFILE-VERIFICATION` | Transformation shall own `OP-TRANSFORM` exclusively and shall own no profile primitive concept. |
| `OLS3-REQ-0096` | `TEST-OLS3-0096` | `METHOD-PROFILE-VERIFICATION` | Transformation shall activate Representation as a mandatory dependency. |
| `OLS3-REQ-0097` | `TEST-OLS3-0097` | `METHOD-PROFILE-VERIFICATION` | Referencing `TERM-CONSTRAINT` or `OP-VALIDATE` shall activate its owner profile. |
| `OLS3-REQ-0098` | `TEST-OLS3-0098` | `METHOD-PROFILE-VERIFICATION` | Transformation shall preserve distinct input and resulting form or state references. |
| `OLS3-REQ-0099` | `TEST-OLS3-0099` | `METHOD-PROFILE-VERIFICATION` | Transformation shall not establish an admitted outcome, validation, improvement, authorization, or execution success. |
| `OLS3-REQ-0100` | `TEST-OLS3-0100` | `METHOD-PROFILE-VERIFICATION` | Evidence/Validation shall own `TERM-OUTCOME` and `OP-VALIDATE` exclusively. |
| `OLS3-REQ-0101` | `TEST-OLS3-0101` | `METHOD-PROFILE-VERIFICATION` | Representation shall activate when represented material is validated. |
| `OLS3-REQ-0102` | `TEST-OLS3-0102` | `METHOD-PROFILE-VERIFICATION` | Referencing `TERM-CONSTRAINT`, `OP-TRANSFORM`, or `OP-RECORD` shall activate the owning profile. |
| `OLS3-REQ-0103` | `TEST-OLS3-0103` | `METHOD-PROFILE-VERIFICATION` | Evidence/Validation shall preserve candidate, validation, and admission statuses as distinct. |
| `OLS3-REQ-0104` | `TEST-OLS3-0104` | `METHOD-PROFILE-VERIFICATION` | Evidence/Validation shall not convert validation into authority, canonical status, universality, or publication. |
| `OLS3-REQ-0105` | `TEST-OLS3-0105` | `METHOD-PROFILE-VERIFICATION` | Memory/Learning shall own `TERM-MEMORY` and `OP-RECORD` exclusively. |
| `OLS3-REQ-0106` | `TEST-OLS3-0106` | `METHOD-PROFILE-VERIFICATION` | Evidence/Validation shall activate when experiential learning or an admitted outcome is claimed. |
| `OLS3-REQ-0107` | `TEST-OLS3-0107` | `METHOD-PROFILE-VERIFICATION` | Recording an observation without validation shall preserve its evidence and admission status. |
| `OLS3-REQ-0108` | `TEST-OLS3-0108` | `METHOD-PROFILE-VERIFICATION` | Memory/Learning shall preserve identity, time, provenance, evidence class, uncertainty, and admission status. |
| `OLS3-REQ-0109` | `TEST-OLS3-0109` | `METHOD-PROFILE-VERIFICATION` | Memory/Learning shall not treat persistence alone as validation, admission, or learning. |
| `OLS3-REQ-0110` | `TEST-OLS3-0110` | `METHOD-PROFILE-VERIFICATION` | Editorial Governance shall own `TERM-AUTHORITY` and `OP-APPROVE` exclusively. |
| `OLS3-REQ-0111` | `TEST-OLS3-0111` | `METHOD-PROFILE-VERIFICATION` | Referencing `OP-RECORD` or required `OP-VALIDATE` shall activate its owner profile. |
| `OLS3-REQ-0112` | `TEST-OLS3-0112` | `METHOD-PROFILE-VERIFICATION` | Editorial Governance shall preserve proposal, approval, canonical, publication, evidence, and validation statuses as distinct where they occur. |
| `OLS3-REQ-0113` | `TEST-OLS3-0113` | `METHOD-PROFILE-VERIFICATION` | Editorial Governance shall require OLS-2 authority scope for governed status change. |
| `OLS3-REQ-0114` | `TEST-OLS3-0114` | `METHOD-PROFILE-VERIFICATION` | Editorial Governance shall not treat approval or publication as empirical truth or permit software to replace declared human authority. |
| `OLS3-REQ-0115` | `TEST-OLS3-0115` | `METHOD-PROFILE-VERIFICATION` | Education shall be activated explicitly because it owns no primitive concept or primitive operator. |
| `OLS3-REQ-0116` | `TEST-OLS3-0116` | `METHOD-PROFILE-VERIFICATION` | Education shall activate Navigation as a mandatory dependency. |
| `OLS3-REQ-0117` | `TEST-OLS3-0117` | `METHOD-PROFILE-VERIFICATION` | Referencing `OP-RECORD` or claiming recorded learning shall activate Memory/Learning. |
| `OLS3-REQ-0118` | `TEST-OLS3-0118` | `METHOD-PROFILE-VERIFICATION` | Education shall preserve the difference between participation, completion, recording, admission, validation, and learning. |
| `OLS3-REQ-0119` | `TEST-OLS3-0119` | `METHOD-PROFILE-VERIFICATION` | Education shall not present its progression as universal cognitive law or completion as validation. |
| `OLS3-REQ-0120` | `TEST-OLS3-0120` | `METHOD-PROFILE-VERIFICATION` | Each profile primitive concept shall have exactly one owner in Annex C. |
| `OLS3-REQ-0121` | `TEST-OLS3-0121` | `METHOD-PROFILE-VERIFICATION` | A referencing profile shall use the owning definition and shall not redefine it. |
| `OLS3-REQ-0122` | `TEST-OLS3-0122` | `METHOD-PROFILE-VERIFICATION` | Invoking a profile primitive concept shall activate its owner profile. |
| `OLS3-REQ-0123` | `TEST-OLS3-0123` | `METHOD-PROFILE-VERIFICATION` | No additional profile primitive concept shall be introduced in Version 1.0. |
| `OLS3-REQ-0124` | `TEST-OLS3-0124` | `METHOD-PROFILE-VERIFICATION` | Navigation shall remain the sole owner of `TERM-CONSTRAINT`. |
| `OLS3-REQ-0125` | `TEST-OLS3-0125` | `METHOD-PROFILE-VERIFICATION` | A profile referencing constraint shall activate Navigation and preserve the declared constraint basis. |
| `OLS3-REQ-0126` | `TEST-OLS3-0126` | `METHOD-PROFILE-VERIFICATION` | Constraint shall not be converted into selection, validation, or authority without the separately owned operator and conditions. |
| `OLS3-REQ-0127` | `TEST-OLS3-0127` | `METHOD-PROFILE-VERIFICATION` | Evidence/Validation shall remain the sole owner of `TERM-OUTCOME`. |
| `OLS3-REQ-0128` | `TEST-OLS3-0128` | `METHOD-PROFILE-VERIFICATION` | A profile referencing outcome shall activate Evidence/Validation and preserve candidate, validation, and admission status. |
| `OLS3-REQ-0129` | `TEST-OLS3-0129` | `METHOD-PROFILE-VERIFICATION` | Outcome shall not imply improvement, authority, publication, or learning. |
| `OLS3-REQ-0130` | `TEST-OLS3-0130` | `METHOD-PROFILE-VERIFICATION` | Memory/Learning shall remain the sole owner of `TERM-MEMORY`. |
| `OLS3-REQ-0131` | `TEST-OLS3-0131` | `METHOD-PROFILE-VERIFICATION` | A profile referencing memory shall activate Memory/Learning and preserve identity, time, provenance, evidence class, uncertainty, and admission status. |
| `OLS3-REQ-0132` | `TEST-OLS3-0132` | `METHOD-PROFILE-VERIFICATION` | Memory shall not be treated as learning solely because material is retained. |
| `OLS3-REQ-0133` | `TEST-OLS3-0133` | `METHOD-PROFILE-VERIFICATION` | Editorial Governance shall remain the sole owner of `TERM-AUTHORITY`. |
| `OLS3-REQ-0134` | `TEST-OLS3-0134` | `METHOD-PROFILE-VERIFICATION` | A construction referencing authority shall activate Editorial Governance and identify `DECL-AUTHORITY-SCOPE`. |
| `OLS3-REQ-0135` | `TEST-OLS3-0135` | `METHOD-PROFILE-VERIFICATION` | Authority shall not be inferred from evidence, validation, orientation, explanation, selection, implementation capability, or operator order. |
| `OLS3-REQ-0136` | `TEST-OLS3-0136` | `METHOD-PROFILE-VERIFICATION` | A profile shall inherit all fourteen universal concepts without modification. |
| `OLS3-REQ-0137` | `TEST-OLS3-0137` | `METHOD-PROFILE-VERIFICATION` | A profile shall retain all five universal operator responsibilities and the OLS-1 canonical order. |
| `OLS3-REQ-0138` | `TEST-OLS3-0138` | `METHOD-PROFILE-VERIFICATION` | A profile shall not add an operator to or remove an operator from the canonical universal process. |
| `OLS3-REQ-0139` | `TEST-OLS3-0139` | `METHOD-PROFILE-VERIFICATION` | A profile shall not change an OLS-2 declaration definition, default, applicability, omission, incompatibility, or preservation rule. |
| `OLS3-REQ-0140` | `TEST-OLS3-0140` | `METHOD-PROFILE-VERIFICATION` | A profile shall not redefine an OLS-2 primitive operator contract or owner. |
| `OLS3-REQ-0141` | `TEST-OLS3-0141` | `METHOD-PROFILE-VERIFICATION` | A profile shall not convert metaphor, historical recurrence, implementation support, or visual similarity into semantic authority. |
| `OLS3-REQ-0142` | `TEST-OLS3-0142` | `METHOD-PROFILE-VERIFICATION` | Profile activation shall not imply empirical truth, implementation correctness, safety, performance, recommendation, authorization, execution, or outcome. |
| `OLS3-REQ-0143` | `TEST-OLS3-0143` | `METHOD-PROFILE-VERIFICATION` | A profile violating a boundary in Clause 12 shall make the affected composition malformed. |
| `OLS3-REQ-0144` | `TEST-OLS3-0144` | `METHOD-PROFILE-VERIFICATION` | A Version 1.0 profile composition shall resolve to Annexes A, B, and C and the applicable profile clauses. |
| `OLS3-REQ-0145` | `TEST-OLS3-0145` | `METHOD-PROFILE-VERIFICATION` | OLS-3 shall preserve unique ownership, explicit activation, dependency resolution, and universal boundaries in every profile composition. |
| `OLS3-REQ-0146` | `TEST-OLS3-0146` | `METHOD-PROFILE-VERIFICATION` | OLS-3 shall remain independent of implementation technology and shall not define derivations or conformance procedures. |
| `OLS3-REQ-0147` | `TEST-OLS3-0147` | `METHOD-PROFILE-VERIFICATION` | Annex A shall contain exactly seven Version 1.0 profiles. |
| `OLS3-REQ-0148` | `TEST-OLS3-0148` | `METHOD-PROFILE-VERIFICATION` | A Profile ID shall not be reassigned to another purpose or owner. |
| `OLS3-REQ-0149` | `TEST-OLS3-0149` | `METHOD-PROFILE-VERIFICATION` | A profile shall not be added, removed, or given a changed responsibility without the applicable Architecture Revision Process. |
| `OLS3-REQ-0150` | `TEST-OLS3-0150` | `METHOD-PROFILE-VERIFICATION` | Annex B shall control Version 1.0 mandatory and conditional profile dependencies. |
| `OLS3-REQ-0151` | `TEST-OLS3-0151` | `METHOD-PROFILE-VERIFICATION` | A conditional dependency shall activate exactly when its registered trigger applies. |
| `OLS3-REQ-0152` | `TEST-OLS3-0152` | `METHOD-PROFILE-VERIFICATION` | An activation route shall not change the semantics of the activated profile. |
| `OLS3-REQ-0153` | `TEST-OLS3-0153` | `METHOD-PROFILE-VERIFICATION` | The Universal Base Language shall be inherited by every row and shall not be represented as a profile dependency. |
| `OLS3-REQ-0154` | `TEST-OLS3-0154` | `METHOD-PROFILE-VERIFICATION` | Annex C shall contain exactly four Version 1.0 profile primitive concepts. |
| `OLS3-REQ-0155` | `TEST-OLS3-0155` | `METHOD-PROFILE-VERIFICATION` | Each Annex C concept shall have exactly one semantic owner. |
| `OLS3-REQ-0156` | `TEST-OLS3-0156` | `METHOD-PROFILE-VERIFICATION` | A referencing profile shall preserve the owner, definition, boundaries, and activation rule. |
| `OLS3-REQ-0157` | `TEST-OLS3-0157` | `METHOD-PROFILE-VERIFICATION` | An Annex C Term ID shall not be reassigned or given a second normative definition. |
| `OLS4-REQ-0001` | `TEST-OLS4-0001` | `METHOD-DERIVATION-VERIFICATION` | OLS-4 shall preserve every semantic responsibility and boundary defined by OLS-1 through OLS-3. |
| `OLS4-REQ-0002` | `TEST-OLS4-0002` | `METHOD-DERIVATION-VERIFICATION` | OLS-4 shall not introduce a universal concept, declaration, primitive operator, semantic profile, or semantic owner. |
| `OLS4-REQ-0003` | `TEST-OLS4-0003` | `METHOD-DERIVATION-VERIFICATION` | A derivation or transition shall be valid only under its registered prerequisites, declarations, conditions, preservation rules, and non-implications. |
| `OLS4-REQ-0004` | `TEST-OLS4-0004` | `METHOD-DERIVATION-VERIFICATION` | A semantic sequence shall not be interpreted as implementation scheduling, causality, external execution, or empirical proof. |
| `OLS4-REQ-0005` | `TEST-OLS4-0005` | `METHOD-DERIVATION-VERIFICATION` | Terms, declarations, operators, profiles, activation, dependencies, and ownership shall resolve to their authoritative registries in OLS-1 through OLS-3. |
| `OLS4-REQ-0006` | `TEST-OLS4-0006` | `METHOD-DERIVATION-VERIFICATION` | A derivation shall identify its source inputs and applicable operation or relation. |
| `OLS4-REQ-0007` | `TEST-OLS4-0007` | `METHOD-DERIVATION-VERIFICATION` | A derivation shall preserve all applicable OLS-2 declarations and source statuses. |
| `OLS4-REQ-0008` | `TEST-OLS4-0008` | `METHOD-DERIVATION-VERIFICATION` | Absence of a stated non-implication shall not authorize that implication. |
| `OLS4-REQ-0009` | `TEST-OLS4-0009` | `METHOD-DERIVATION-VERIFICATION` | An accepted derivation shall not be treated as universal truth; its applicability remains bounded by its prerequisites. |
| `OLS4-REQ-0010` | `TEST-OLS4-0010` | `METHOD-DERIVATION-VERIFICATION` | A conditional derivation shall not apply when any registered condition, profile, criterion, prerequisite, or declaration is absent. |
| `OLS4-REQ-0011` | `TEST-OLS4-0011` | `METHOD-DERIVATION-VERIFICATION` | Historical labels that are not registered OLS-3 Profile IDs shall not activate a semantic profile. |
| `OLS4-REQ-0012` | `TEST-OLS4-0012` | `METHOD-DERIVATION-VERIFICATION` | The labels `Research`, `Trajectory`, `Transition`, `Construction`, and `Culture`, where retained in Annex B as source conditions, shall be treated as recorded domain or criteria conditions, not as Version 1.0 semantic profiles. |
| `OLS4-REQ-0013` | `TEST-OLS4-0013` | `METHOD-DERIVATION-VERIFICATION` | Every product shall have exactly one semantic owner. |
| `OLS4-REQ-0014` | `TEST-OLS4-0014` | `METHOD-DERIVATION-VERIFICATION` | Every product shall retain its originating inputs, applicable declarations, provenance, evidence class, uncertainty, and status. |
| `OLS4-REQ-0015` | `TEST-OLS4-0015` | `METHOD-DERIVATION-VERIFICATION` | A product shall not acquire the status of another product except through a legal transition in Annex B. |
| `OLS4-REQ-0016` | `TEST-OLS4-0016` | `METHOD-DERIVATION-VERIFICATION` | An explanation produced by EXPLAIN remains governed by OLS-2 and is not an additional OLS-4 semantic product. |
| `OLS4-REQ-0017` | `TEST-OLS4-0017` | `METHOD-DERIVATION-VERIFICATION` | Observation product status shall not be promoted solely because the product enters a later derivation. |
| `OLS4-REQ-0018` | `TEST-OLS4-0018` | `METHOD-DERIVATION-VERIFICATION` | A representation product shall remain distinguishable from its source and from reality. |
| `OLS4-REQ-0019` | `TEST-OLS4-0019` | `METHOD-DERIVATION-VERIFICATION` | A comparison finding shall identify every compared item and the comparison basis. |
| `OLS4-REQ-0020` | `TEST-OLS4-0020` | `METHOD-DERIVATION-VERIFICATION` | An orientation finding shall preserve supported, unsupported, disputed, uncertain, and limited status as distinct. |
| `OLS4-REQ-0021` | `TEST-OLS4-0021` | `METHOD-DERIVATION-VERIFICATION` | Selection result status shall remain selection status unless a separately owned operation establishes another status. |
| `OLS4-REQ-0022` | `TEST-OLS4-0022` | `METHOD-DERIVATION-VERIFICATION` | A transformation result shall not be treated as a candidate outcome until the conditions of Clause 8 are satisfied. |
| `OLS4-REQ-0023` | `TEST-OLS4-0023` | `METHOD-DERIVATION-VERIFICATION` | A validation result shall remain linked to its subject, criteria, evidence, and declared scope. |
| `OLS4-REQ-0024` | `TEST-OLS4-0024` | `METHOD-DERIVATION-VERIFICATION` | A transformation result alone shall not constitute a candidate outcome. |
| `OLS4-REQ-0025` | `TEST-OLS4-0025` | `METHOD-DERIVATION-VERIFICATION` | Candidate status shall require a post-transformation observation with identity, later time, provenance, evidence class, and uncertainty status. |
| `OLS4-REQ-0026` | `TEST-OLS4-0026` | `METHOD-DERIVATION-VERIFICATION` | Outcome admission shall not occur solely from observation, transformation, validation status, approval, or persistence. |
| `OLS4-REQ-0027` | `TEST-OLS4-0027` | `METHOD-DERIVATION-VERIFICATION` | A record of an unvalidated observation shall not be identified as recorded experience. |
| `OLS4-REQ-0028` | `TEST-OLS4-0028` | `METHOD-DERIVATION-VERIFICATION` | Learned knowledge shall require admitted outcome, recorded experience, prior memory or knowledge, an explicit comparison, and a recorded resulting change. |
| `OLS4-REQ-0029` | `TEST-OLS4-0029` | `METHOD-DERIVATION-VERIFICATION` | Persistence alone shall not establish learned knowledge. |
| `OLS4-REQ-0030` | `TEST-OLS4-0030` | `METHOD-DERIVATION-VERIFICATION` | An accepted derivation shall apply only when every input, declaration, operator or relation, and prerequisite in its registry row is present. |
| `OLS4-REQ-0031` | `TEST-OLS4-0031` | `METHOD-DERIVATION-VERIFICATION` | The output distinction of an accepted derivation shall not imply any status listed in that row’s non-implications. |
| `OLS4-REQ-0032` | `TEST-OLS4-0032` | `METHOD-DERIVATION-VERIFICATION` | An accepted derivation shall preserve its source terms and shall not redefine them. |
| `OLS4-REQ-0033` | `TEST-OLS4-0033` | `METHOD-DERIVATION-VERIFICATION` | A conditional derivation shall be unavailable unless all registered conditions are explicit. |
| `OLS4-REQ-0034` | `TEST-OLS4-0034` | `METHOD-DERIVATION-VERIFICATION` | Where a registry row names an OLS-3 profile, that profile shall be active and its dependencies resolved. |
| `OLS4-REQ-0035` | `TEST-OLS4-0035` | `METHOD-DERIVATION-VERIFICATION` | Where a registry row preserves a historical domain label not registered by OLS-3, that label shall supply no profile semantics or activation. |
| `OLS4-REQ-0036` | `TEST-OLS4-0036` | `METHOD-DERIVATION-VERIFICATION` | A conditional derivation shall report the criteria by which its derived distinction was recognized. |
| `OLS4-REQ-0037` | `TEST-OLS4-0037` | `METHOD-DERIVATION-VERIFICATION` | Transition order shall matter whenever identity, time, validation, admission, or learning status depends on order. |
| `OLS4-REQ-0038` | `TEST-OLS4-0038` | `METHOD-DERIVATION-VERIFICATION` | A transition shall preserve the source product and shall not overwrite prior status. |
| `OLS4-REQ-0039` | `TEST-OLS4-0039` | `METHOD-DERIVATION-VERIFICATION` | A product may enter a later operation only when its type, status, declarations, context, perspective, identity, time, scale, and representation basis are compatible as applicable. |
| `OLS4-REQ-0040` | `TEST-OLS4-0040` | `METHOD-DERIVATION-VERIFICATION` | Optional transitions shall not be inferred from adjacency in an example chain. |
| `OLS4-REQ-0041` | `TEST-OLS4-0041` | `METHOD-DERIVATION-VERIFICATION` | `PRODUCT-VALIDATION-RESULT` shall not transition to `PRODUCT-CANDIDATE-OUTCOME`; candidate status precedes outcome validation in the experiential sequence. |
| `OLS4-REQ-0042` | `TEST-OLS4-0042` | `METHOD-DERIVATION-VERIFICATION` | Candidate outcome and admitted outcome shall be owned by `PROFILE-EVIDENCE-VALIDATION`. |
| `OLS4-REQ-0043` | `TEST-OLS4-0043` | `METHOD-DERIVATION-VERIFICATION` | Candidate outcome shall be an observed post-transformation state with compatible identity and later time. |
| `OLS4-REQ-0044` | `TEST-OLS4-0044` | `METHOD-DERIVATION-VERIFICATION` | Admission shall require an identifiable candidate outcome, applicable validation result, declared validation and admission conditions, supporting evidence with provenance, and preserved uncertainty. |
| `OLS4-REQ-0045` | `TEST-OLS4-0045` | `METHOD-DERIVATION-VERIFICATION` | Admission shall be a status transition and shall not invoke or imply an additional primitive operator. |
| `OLS4-REQ-0046` | `TEST-OLS4-0046` | `METHOD-DERIVATION-VERIFICATION` | Admission shall preserve both candidate and validation status rather than replacing their history. |
| `OLS4-REQ-0047` | `TEST-OLS4-0047` | `METHOD-DERIVATION-VERIFICATION` | `OP-APPROVE` shall not perform outcome admission. |
| `OLS4-REQ-0048` | `TEST-OLS4-0048` | `METHOD-DERIVATION-VERIFICATION` | Admitted status shall not imply improvement, desired effect, authority, publication, or universal proof. |
| `OLS4-REQ-0049` | `TEST-OLS4-0049` | `METHOD-DERIVATION-VERIFICATION` | Recording shall require identifiable material, identity, time, provenance and status, and all applicable declarations. |
| `OLS4-REQ-0050` | `TEST-OLS4-0050` | `METHOD-DERIVATION-VERIFICATION` | Recording shall preserve the recorded material’s validation, admission, evidence, provenance, and uncertainty status. |
| `OLS4-REQ-0051` | `TEST-OLS4-0051` | `METHOD-DERIVATION-VERIFICATION` | Recording shall not upgrade an observation to evidence, a candidate to an admitted outcome, a record to canonical status, or persistence to learning. |
| `OLS4-REQ-0052` | `TEST-OLS4-0052` | `METHOD-DERIVATION-VERIFICATION` | An observation may be recorded without validation, but the record shall retain its unvalidated status and shall not become recorded experience by default. |
| `OLS4-REQ-0053` | `TEST-OLS4-0053` | `METHOD-DERIVATION-VERIFICATION` | Experiential learning shall require a validated and admitted outcome. |
| `OLS4-REQ-0054` | `TEST-OLS4-0054` | `METHOD-DERIVATION-VERIFICATION` | Experiential learning shall require recording of the admitted outcome, explicit comparison with prior memory or knowledge, and recording of the resulting change. |
| `OLS4-REQ-0055` | `TEST-OLS4-0055` | `METHOD-DERIVATION-VERIFICATION` | Learning shall preserve evidence class, provenance, uncertainty, disagreements, limitations, identity, time, and the prior state. |
| `OLS4-REQ-0056` | `TEST-OLS4-0056` | `METHOD-DERIVATION-VERIFICATION` | A simulated, inferred, proposed, or merely persisted result shall not be presented as observed experiential learning. |
| `OLS4-REQ-0057` | `TEST-OLS4-0057` | `METHOD-DERIVATION-VERIFICATION` | Learned knowledge shall remain bounded to the declared context, perspective, representation, evidence, identity, time, scale, and uncertainty. |
| `OLS4-REQ-0058` | `TEST-OLS4-0058` | `METHOD-DERIVATION-VERIFICATION` | No prohibited derivation shall become legal through sequencing, profile composition, explanation, repetition, approval, implementation output, or precedence. |
| `OLS4-REQ-0059` | `TEST-OLS4-0059` | `METHOD-DERIVATION-VERIFICATION` | A prohibited derivation shall remain prohibited even when its source product is complete or its originating operator succeeds. |
| `OLS4-REQ-0060` | `TEST-OLS4-0060` | `METHOD-DERIVATION-VERIFICATION` | A separately governed operation may establish only the status within its own contract and shall not retroactively legalize an earlier prohibited implication. |
| `OLS4-REQ-0061` | `TEST-OLS4-0061` | `METHOD-DERIVATION-VERIFICATION` | Failure shall be reported at the earliest unsupported or invalid transition. |
| `OLS4-REQ-0062` | `TEST-OLS4-0062` | `METHOD-DERIVATION-VERIFICATION` | A later valid operation shall not erase an earlier failure or missing state. |
| `OLS4-REQ-0063` | `TEST-OLS4-0063` | `METHOD-DERIVATION-VERIFICATION` | No precedence rule shall repair an illegal transition. |
| `OLS4-REQ-0064` | `TEST-OLS4-0064` | `METHOD-DERIVATION-VERIFICATION` | OLS-5 shall define conformance procedures; OLS-4 defines only semantic failure conditions. |
| `OLS4-REQ-0065` | `TEST-OLS4-0065` | `METHOD-DERIVATION-VERIFICATION` | `space` and `balance` shall not receive one generic Version 1.0 derivation. |
| `OLS4-REQ-0066` | `TEST-OLS4-0066` | `METHOD-DERIVATION-VERIFICATION` | Reclassification records shall not be used to derive the reclassified element. |
| `OLS4-REQ-0067` | `TEST-OLS4-0067` | `METHOD-DERIVATION-VERIFICATION` | `difference`, `constraint`, `outcome`, `scale`, and `time` shall resolve to their OLS-1, OLS-2, or OLS-3 classifications. |
| `OLS4-REQ-0068` | `TEST-OLS4-0068` | `METHOD-DERIVATION-VERIFICATION` | Non-transformation validation shall retain subject, criteria, evidence class, provenance, uncertainty, and validation scope. |
| `OLS4-REQ-0069` | `TEST-OLS4-0069` | `METHOD-DERIVATION-VERIFICATION` | Absence of transformation shall not remove validation prerequisites. |
| `OLS4-REQ-0070` | `TEST-OLS4-0070` | `METHOD-DERIVATION-VERIFICATION` | A non-transformation validation result shall not become an admitted outcome unless the separately required candidate-outcome and admission conditions hold. |
| `OLS4-REQ-0071` | `TEST-OLS4-0071` | `METHOD-DERIVATION-VERIFICATION` | A recorded but unvalidated observation shall retain observation status and shall not become experiential learning. |
| `OLS4-REQ-0072` | `TEST-OLS4-0072` | `METHOD-DERIVATION-VERIFICATION` | Cross-profile transition shall not transfer semantic ownership. |
| `OLS4-REQ-0073` | `TEST-OLS4-0073` | `METHOD-DERIVATION-VERIFICATION` | The Evidence/Validation Profile shall be active when candidate, validation, or admitted outcome status is used. |
| `OLS4-REQ-0074` | `TEST-OLS4-0074` | `METHOD-DERIVATION-VERIFICATION` | The Memory/Learning Profile shall be active when recorded experience or learned knowledge is claimed. |
| `OLS4-REQ-0075` | `TEST-OLS4-0075` | `METHOD-DERIVATION-VERIFICATION` | The complete Version 1.0 derivation architecture consists of the registries and rules in OLS-4; examples shall not add transitions. |
| `OLS4-REQ-0076` | `TEST-OLS4-0076` | `METHOD-DERIVATION-VERIFICATION` | Annex A shall contain exactly eleven Product IDs and one owner for each. |
| `OLS4-REQ-0077` | `TEST-OLS4-0077` | `METHOD-DERIVATION-VERIFICATION` | Annex B shall contain exactly eighteen accepted and eighteen conditional derivation records. |
| `OLS4-REQ-0078` | `TEST-OLS4-0078` | `METHOD-DERIVATION-VERIFICATION` | Every prohibition in Annex C shall apply to direct and composed derivations. |
| `OLS5-REQ-0001` | `TEST-OLS5-0001` | `METHOD-CONFORMANCE-VERIFICATION` | Conformance shall verify the applicable normative requirements of the declared suite version and claim scope. |
| `OLS5-REQ-0002` | `TEST-OLS5-0002` | `METHOD-CONFORMANCE-VERIFICATION` | Conformance shall not introduce, remove, reinterpret, complete, or transfer semantic responsibility. |
| `OLS5-REQ-0003` | `TEST-OLS5-0003` | `METHOD-CONFORMANCE-VERIFICATION` | A conformance claim shall identify one target, one Conformance ID, the suite version, and the tested scope. |
| `OLS5-REQ-0004` | `TEST-OLS5-0004` | `METHOD-CONFORMANCE-VERIFICATION` | Informative text, examples, rationale, historical material, and implementation guidance shall not create a conformance obligation. |
| `OLS5-REQ-0005` | `TEST-OLS5-0005` | `METHOD-CONFORMANCE-VERIFICATION` | A test shall use the controlling requirement text from the compatible release identified by the claim. |
| `OLS5-REQ-0006` | `TEST-OLS5-0006` | `METHOD-CONFORMANCE-VERIFICATION` | An informative paraphrase shall not replace a controlling normative requirement as a test oracle. |
| `OLS5-REQ-0007` | `TEST-OLS5-0007` | `METHOD-CONFORMANCE-VERIFICATION` | Every test shall preserve the normative/informative status of its source material. |
| `OLS5-REQ-0008` | `TEST-OLS5-0008` | `METHOD-CONFORMANCE-VERIFICATION` | Passing evidence shall support only the tested requirement within the declared scope. |
| `OLS5-REQ-0009` | `TEST-OLS5-0009` | `METHOD-CONFORMANCE-VERIFICATION` | The assessor shall not infer unclaimed capabilities or unreported semantic status. |
| `OLS5-REQ-0010` | `TEST-OLS5-0010` | `METHOD-CONFORMANCE-VERIFICATION` | Human and software realizations shall be assessed against the same applicable semantic requirements. |
| `OLS5-REQ-0011` | `TEST-OLS5-0011` | `METHOD-CONFORMANCE-VERIFICATION` | The target shall have a stable identifier or an unambiguous report-local identifier. |
| `OLS5-REQ-0012` | `TEST-OLS5-0012` | `METHOD-CONFORMANCE-VERIFICATION` | The claim shall identify the target type and the exact material included in assessment. |
| `OLS5-REQ-0013` | `TEST-OLS5-0013` | `METHOD-CONFORMANCE-VERIFICATION` | A target shall claim only capabilities present in the declared scope. |
| `OLS5-REQ-0014` | `TEST-OLS5-0014` | `METHOD-CONFORMANCE-VERIFICATION` | An implementation shall identify implemented profiles, operators, declarations, representation types, unsupported capabilities, and implementation mappings relevant to its claim. |
| `OLS5-REQ-0015` | `TEST-OLS5-0015` | `METHOD-CONFORMANCE-VERIFICATION` | A human procedure shall provide repeatable evidence for the same semantic obligations as another realization of the claimed class. |
| `OLS5-REQ-0016` | `TEST-OLS5-0016` | `METHOD-CONFORMANCE-VERIFICATION` | A profile composition shall identify all active profiles, activated dependencies, declarations, conflicts, and unsupported features. |
| `OLS5-REQ-0017` | `TEST-OLS5-0017` | `METHOD-CONFORMANCE-VERIFICATION` | A class claim shall include every normative dependency registered for that class. |
| `OLS5-REQ-0018` | `TEST-OLS5-0018` | `METHOD-CONFORMANCE-VERIFICATION` | A dependent class shall not mask a failure, incomplete result, or unsupported requirement in a dependency class. |
| `OLS5-REQ-0019` | `TEST-OLS5-0019` | `METHOD-CONFORMANCE-VERIFICATION` | No profile-only conformance class shall exist in Version 1.0. |
| `OLS5-REQ-0020` | `TEST-OLS5-0020` | `METHOD-CONFORMANCE-VERIFICATION` | Every semantic class from OLS-1 through OLS-4 shall include the complete OLS-1 Universal Base Language scope. |
| `OLS5-REQ-0021` | `TEST-OLS5-0021` | `METHOD-CONFORMANCE-VERIFICATION` | `CONFORMANCE-OLS0` shall assess OLS-0 conventions and shall have no suite-internal dependency. |
| `OLS5-REQ-0022` | `TEST-OLS5-0022` | `METHOD-CONFORMANCE-VERIFICATION` | `CONFORMANCE-OLS1` shall assess OLS-0 and OLS-1. |
| `OLS5-REQ-0023` | `TEST-OLS5-0023` | `METHOD-CONFORMANCE-VERIFICATION` | `CONFORMANCE-OLS2` shall assess OLS-0 through OLS-2. |
| `OLS5-REQ-0024` | `TEST-OLS5-0024` | `METHOD-CONFORMANCE-VERIFICATION` | `CONFORMANCE-OLS3` shall assess OLS-0 through OLS-3. |
| `OLS5-REQ-0025` | `TEST-OLS5-0025` | `METHOD-CONFORMANCE-VERIFICATION` | `CONFORMANCE-OLS4` shall assess OLS-0 through OLS-4. |
| `OLS5-REQ-0026` | `TEST-OLS5-0026` | `METHOD-CONFORMANCE-VERIFICATION` | `CONFORMANCE-FULL-SUITE` shall assess every applicable requirement in OLS-0 through OLS-5. |
| `OLS5-REQ-0027` | `TEST-OLS5-0027` | `METHOD-CONFORMANCE-VERIFICATION` | A narrower class shall not be described as Full Suite conformance. |
| `OLS5-REQ-0028` | `TEST-OLS5-0028` | `METHOD-CONFORMANCE-VERIFICATION` | Every normative Requirement ID in the claimed class shall receive one test status. |
| `OLS5-REQ-0029` | `TEST-OLS5-0029` | `METHOD-CONFORMANCE-VERIFICATION` | Applicability shall be determined from the target type, class, active profiles, invoked operators, used derivations, declarations, and explicit claim scope. |
| `OLS5-REQ-0030` | `TEST-OLS5-0030` | `METHOD-CONFORMANCE-VERIFICATION` | Undeclared scope shall not make a requirement not applicable. |
| `OLS5-REQ-0031` | `TEST-OLS5-0031` | `METHOD-CONFORMANCE-VERIFICATION` | Conditional requirements shall be tested when their stated condition is true. |
| `OLS5-REQ-0032` | `TEST-OLS5-0032` | `METHOD-CONFORMANCE-VERIFICATION` | A NOT APPLICABLE result shall identify the controlling condition and evidence that the condition is false. |
| `OLS5-REQ-0033` | `TEST-OLS5-0033` | `METHOD-CONFORMANCE-VERIFICATION` | Informative material shall not receive a required PASS/FAIL test status. |
| `OLS5-REQ-0034` | `TEST-OLS5-0034` | `METHOD-CONFORMANCE-VERIFICATION` | A normative registry entry referenced by an applicable requirement shall be included in that requirement’s test scope. |
| `OLS5-REQ-0035` | `TEST-OLS5-0035` | `METHOD-CONFORMANCE-VERIFICATION` | Every normative Requirement ID in OLS-0 through OLS-5 shall map to at least one Test ID. |
| `OLS5-REQ-0036` | `TEST-OLS5-0036` | `METHOD-CONFORMANCE-VERIFICATION` | Every Test ID shall map to at least one normative Requirement ID. |
| `OLS5-REQ-0037` | `TEST-OLS5-0037` | `METHOD-CONFORMANCE-VERIFICATION` | A test mapping shall identify the controlling requirement, method, applicability basis, and expected condition. |
| `OLS5-REQ-0038` | `TEST-OLS5-0038` | `METHOD-CONFORMANCE-VERIFICATION` | A requirement shall not be declared untestable; absence of sufficient evidence shall produce INCOMPLETE rather than remove the mapping. |
| `OLS5-REQ-0039` | `TEST-OLS5-0039` | `METHOD-CONFORMANCE-VERIFICATION` | Changing a controlling requirement shall require review of every mapped test. |
| `OLS5-REQ-0040` | `TEST-OLS5-0040` | `METHOD-CONFORMANCE-VERIFICATION` | A test shall not expand or narrow the semantic responsibility of its controlling requirement. |
| `OLS5-REQ-0041` | `TEST-OLS5-0041` | `METHOD-CONFORMANCE-VERIFICATION` | A test shall use one or more registered Method IDs. |
| `OLS5-REQ-0042` | `TEST-OLS5-0042` | `METHOD-CONFORMANCE-VERIFICATION` | Test inputs shall declare every condition necessary to determine applicability and expected status. |
| `OLS5-REQ-0043` | `TEST-OLS5-0043` | `METHOD-CONFORMANCE-VERIFICATION` | Expected output shall be expressed semantically or structurally and shall not prescribe implementation technology. |
| `OLS5-REQ-0044` | `TEST-OLS5-0044` | `METHOD-CONFORMANCE-VERIFICATION` | A boundary requirement shall include a negative or prohibited-outcome check. |
| `OLS5-REQ-0045` | `TEST-OLS5-0045` | `METHOD-CONFORMANCE-VERIFICATION` | An operator test shall assess the complete applicable OLS-2 contract, including failures and prohibited implications. |
| `OLS5-REQ-0046` | `TEST-OLS5-0046` | `METHOD-CONFORMANCE-VERIFICATION` | A profile test shall assess the profile independently and its composition obligations collectively. |
| `OLS5-REQ-0047` | `TEST-OLS5-0047` | `METHOD-CONFORMANCE-VERIFICATION` | A derivation test shall assess every registered prerequisite, condition, preservation rule, and non-implication. |
| `OLS5-REQ-0048` | `TEST-OLS5-0048` | `METHOD-CONFORMANCE-VERIFICATION` | A test shall be repeatable from the evidence and procedure identified by its record. |
| `OLS5-REQ-0049` | `TEST-OLS5-0049` | `METHOD-CONFORMANCE-VERIFICATION` | Equivalent evidence may be used across targets when it establishes the same normative condition without changing the oracle. |
| `OLS5-REQ-0050` | `TEST-OLS5-0050` | `METHOD-CONFORMANCE-VERIFICATION` | An example or reference implementation may provide input but shall not define the expected result. |
| `OLS5-REQ-0051` | `TEST-OLS5-0051` | `METHOD-CONFORMANCE-VERIFICATION` | PASS shall mean that sufficient evidence demonstrates satisfaction of the applicable requirement and no prohibited outcome occurred. |
| `OLS5-REQ-0052` | `TEST-OLS5-0052` | `METHOD-CONFORMANCE-VERIFICATION` | FAIL shall mean that evidence demonstrates violation of an applicable requirement or occurrence of a prohibited outcome. |
| `OLS5-REQ-0053` | `TEST-OLS5-0053` | `METHOD-CONFORMANCE-VERIFICATION` | INCOMPLETE shall mean that applicability is established but required evidence, execution, scope, or result is missing or indeterminate. |
| `OLS5-REQ-0054` | `TEST-OLS5-0054` | `METHOD-CONFORMANCE-VERIFICATION` | UNSUPPORTED shall mean that the target explicitly lacks a capability required by the claimed scope. |
| `OLS5-REQ-0055` | `TEST-OLS5-0055` | `METHOD-CONFORMANCE-VERIFICATION` | NOT APPLICABLE shall mean that the requirement’s controlling condition is demonstrably false for the declared target and scope. |
| `OLS5-REQ-0056` | `TEST-OLS5-0056` | `METHOD-CONFORMANCE-VERIFICATION` | A test shall receive exactly one registered status. |
| `OLS5-REQ-0057` | `TEST-OLS5-0057` | `METHOD-CONFORMANCE-VERIFICATION` | NOT APPLICABLE shall not be counted as PASS. |
| `OLS5-REQ-0058` | `TEST-OLS5-0058` | `METHOD-CONFORMANCE-VERIFICATION` | A class shall receive PASS only when every applicable test receives PASS and no applicable test receives FAIL, INCOMPLETE, or UNSUPPORTED. |
| `OLS5-REQ-0059` | `TEST-OLS5-0059` | `METHOD-CONFORMANCE-VERIFICATION` | Aggregate precedence shall be FAIL, then INCOMPLETE, then UNSUPPORTED, then PASS; NOT APPLICABLE results shall be excluded from precedence. |
| `OLS5-REQ-0060` | `TEST-OLS5-0060` | `METHOD-CONFORMANCE-VERIFICATION` | A dependency class result shall be included in aggregate status. |
| `OLS5-REQ-0061` | `TEST-OLS5-0061` | `METHOD-CONFORMANCE-VERIFICATION` | Retesting shall preserve earlier result records and identify supersession without erasing history. |
| `OLS5-REQ-0062` | `TEST-OLS5-0062` | `METHOD-CONFORMANCE-VERIFICATION` | Evidence shall be identifiable, inspectable, relevant to the requirement, and linked to the tested target and version. |
| `OLS5-REQ-0063` | `TEST-OLS5-0063` | `METHOD-CONFORMANCE-VERIFICATION` | Evidence shall preserve provenance, date, assessor or producing system, and status. |
| `OLS5-REQ-0064` | `TEST-OLS5-0064` | `METHOD-CONFORMANCE-VERIFICATION` | Evidence shall be sufficient for an independent assessor to repeat or audit the determination. |
| `OLS5-REQ-0065` | `TEST-OLS5-0065` | `METHOD-CONFORMANCE-VERIFICATION` | Unsupported, disputed, partial, simulated, inferred, or implementation-generated evidence shall retain that status. |
| `OLS5-REQ-0066` | `TEST-OLS5-0066` | `METHOD-CONFORMANCE-VERIFICATION` | Implementation technology, programming language, storage model, runtime, vendor, or platform shall not be mandatory evidence. |
| `OLS5-REQ-0067` | `TEST-OLS5-0067` | `METHOD-CONFORMANCE-VERIFICATION` | Absence of mandatory evidence shall produce INCOMPLETE, not inferred PASS. |
| `OLS5-REQ-0068` | `TEST-OLS5-0068` | `METHOD-CONFORMANCE-VERIFICATION` | Evidence for one requirement may support another only through an explicit second mapping and determination. |
| `OLS5-REQ-0069` | `TEST-OLS5-0069` | `METHOD-CONFORMANCE-VERIFICATION` | Passing evidence shall not alter the evidence class or uncertainty status of the assessed semantic material. |
| `OLS5-REQ-0070` | `TEST-OLS5-0070` | `METHOD-CONFORMANCE-VERIFICATION` | Every report shall include all thirteen report fields. |
| `OLS5-REQ-0071` | `TEST-OLS5-0071` | `METHOD-CONFORMANCE-VERIFICATION` | The report shall list every Requirement ID in the claimed class or provide an unambiguous complete reference to Annex B plus per-test results. |
| `OLS5-REQ-0072` | `TEST-OLS5-0072` | `METHOD-CONFORMANCE-VERIFICATION` | Every non-PASS status shall include a reason and evidence reference. |
| `OLS5-REQ-0073` | `TEST-OLS5-0073` | `METHOD-CONFORMANCE-VERIFICATION` | Every NOT APPLICABLE status shall identify the controlling applicability condition. |
| `OLS5-REQ-0074` | `TEST-OLS5-0074` | `METHOD-CONFORMANCE-VERIFICATION` | The report shall distinguish claimant assertions from assessor determinations. |
| `OLS5-REQ-0075` | `TEST-OLS5-0075` | `METHOD-CONFORMANCE-VERIFICATION` | The report shall disclose unsupported and partial capabilities without representing them as conforming. |
| `OLS5-REQ-0076` | `TEST-OLS5-0076` | `METHOD-CONFORMANCE-VERIFICATION` | The aggregate status shall be reproducible from per-test statuses and Clause 9. |
| `OLS5-REQ-0077` | `TEST-OLS5-0077` | `METHOD-CONFORMANCE-VERIFICATION` | A changed target, suite version, class scope, or controlling requirement shall require a new or superseding report. |
| `OLS5-REQ-0078` | `TEST-OLS5-0078` | `METHOD-CONFORMANCE-VERIFICATION` | Reports shall preserve stable identifiers exactly as published. |
| `OLS5-REQ-0079` | `TEST-OLS5-0079` | `METHOD-CONFORMANCE-VERIFICATION` | Conformance shall not certify correctness, truth, usefulness, scientific validity, implementation quality, runtime behavior, safety, performance, recommendation quality, authority, successful execution, or outcome validity. |
| `OLS5-REQ-0080` | `TEST-OLS5-0080` | `METHOD-CONFORMANCE-VERIFICATION` | Certification wording shall state its target, Conformance ID, suite version, report identifier, date, and aggregate status. |
| `OLS5-REQ-0081` | `TEST-OLS5-0081` | `METHOD-CONFORMANCE-VERIFICATION` | Certification shall not extend to an untested target, version, profile, operator, declaration, derivation, or capability. |
| `OLS5-REQ-0082` | `TEST-OLS5-0082` | `METHOD-CONFORMANCE-VERIFICATION` | PASS shall not erase uncertainty, validate source evidence, authorize action, or guarantee outcome or learning. |
| `OLS5-REQ-0083` | `TEST-OLS5-0083` | `METHOD-CONFORMANCE-VERIFICATION` | A third-party certification process may add procedural controls but shall not modify OLS semantics, tests, or status meanings. |
| `OLS5-REQ-0084` | `TEST-OLS5-0084` | `METHOD-CONFORMANCE-VERIFICATION` | A test shall assess observable semantic or structural obligations rather than internal implementation design. |
| `OLS5-REQ-0085` | `TEST-OLS5-0085` | `METHOD-CONFORMANCE-VERIFICATION` | Different implementations shall be eligible for the same class when they provide equivalent evidence for the same requirements. |
| `OLS5-REQ-0086` | `TEST-OLS5-0086` | `METHOD-CONFORMANCE-VERIFICATION` | An implementation may support fewer than all profiles but shall not claim a profile whose applicable requirements receive UNSUPPORTED. |
| `OLS5-REQ-0087` | `TEST-OLS5-0087` | `METHOD-CONFORMANCE-VERIFICATION` | A general Orientation Language claim shall not declare partial Universal Base Language conformance. |
| `OLS5-REQ-0088` | `TEST-OLS5-0088` | `METHOD-CONFORMANCE-VERIFICATION` | Unsupported optional profiles shall be reported and shall be NOT APPLICABLE only when excluded from the declared class scope and not activated or invoked. |
| `OLS5-REQ-0089` | `TEST-OLS5-0089` | `METHOD-CONFORMANCE-VERIFICATION` | Implementation mappings shall preserve semantic ownership, identifiers, declarations, status, provenance, uncertainty, and prohibited implications. |
| `OLS5-REQ-0090` | `TEST-OLS5-0090` | `METHOD-CONFORMANCE-VERIFICATION` | Version 1.0 conformance shall use Annex A classes, Annex B tests, and Annex C statuses. |
| `OLS5-REQ-0091` | `TEST-OLS5-0091` | `METHOD-CONFORMANCE-VERIFICATION` | Every claimed applicable requirement shall receive a repeatable evidence-backed status. |
| `OLS5-REQ-0092` | `TEST-OLS5-0092` | `METHOD-CONFORMANCE-VERIFICATION` | No passing test, class, report, or certification shall create semantic status beyond its controlling requirement. |
| `OLS5-REQ-0093` | `TEST-OLS5-0093` | `METHOD-CONFORMANCE-VERIFICATION` | Annex A shall contain exactly six Conformance IDs. |
| `OLS5-REQ-0094` | `TEST-OLS5-0094` | `METHOD-CONFORMANCE-VERIFICATION` | A Conformance ID shall not be reassigned to another scope. |
| `OLS5-REQ-0095` | `TEST-OLS5-0095` | `METHOD-CONFORMANCE-VERIFICATION` | The one-to-one mapping shall preserve the numeric component and owning part of every Requirement ID. |
| `OLS5-REQ-0096` | `TEST-OLS5-0096` | `METHOD-CONFORMANCE-VERIFICATION` | Each matrix row shall identify one Requirement ID, one Test ID, one primary method, and the expected condition. |
| `OLS5-REQ-0097` | `TEST-OLS5-0097` | `METHOD-CONFORMANCE-VERIFICATION` | Annex C shall contain exactly five statuses. |
| `OLS5-REQ-0098` | `TEST-OLS5-0098` | `METHOD-CONFORMANCE-VERIFICATION` | Status labels and meanings shall not be extended by an individual report. |

# Annex C — Conformance Status Registry

*Annex ID: `OLS5-ANNEX-C` — Trace ID: `TRACE-000171` — Normative*

| Status | Meaning | Required evidence | Aggregate effect |
| --- | --- | --- | --- |
| `PASS` | Applicable requirement satisfied; no prohibited outcome observed. | Sufficient positive and applicable negative evidence. | Supports class PASS. |
| `FAIL` | Applicable requirement violated or prohibited outcome observed. | Evidence of violation. | Aggregate FAIL. |
| `INCOMPLETE` | Applicable, but evidence, execution, scope, or result is missing or indeterminate. | Evidence of gap or indeterminacy. | Aggregate INCOMPLETE unless FAIL exists. |
| `UNSUPPORTED` | Required claimed capability is explicitly absent. | Capability statement or observed absence. | Aggregate UNSUPPORTED unless FAIL or INCOMPLETE exists. |
| `NOT APPLICABLE` | Controlling condition demonstrably false. | Applicability rationale and evidence. | Excluded from aggregate precedence. |

`[OLS5-REQ-0097]` Annex C shall contain exactly five statuses.

`[OLS5-REQ-0098]` Status labels and meanings shall not be extended by an individual report.

# Annex D — Example Test Reports

*Annex ID: `OLS5-ANNEX-D` — Trace ID: `TRACE-000172` — Informative*

## D.1 Passing semantic target

Report `REPORT-EXAMPLE-001` assesses an orientation artifact under `CONFORMANCE-OLS2`, suite `1.0.0`. It identifies all OLS-0 through OLS-2 requirements, marks operator- and declaration-conditional tests according to the artifact’s actual content, links inspectable evidence, and reports PASS only because every applicable test passes. The report explicitly excludes scientific validity and usefulness.

## D.2 Partial implementation

Report `REPORT-EXAMPLE-002` assesses an implementation under `CONFORMANCE-OLS3`. Navigation is supported; Transformation is outside the declared scope and never activated. Transformation-conditional requirements receive NOT APPLICABLE with evidence. A required Navigation conflict test lacks evidence and receives INCOMPLETE; the class result is INCOMPLETE.

# Annex E — Example Failure Reports

*Annex ID: `OLS5-ANNEX-E` — Trace ID: `TRACE-000173` — Informative*

1. A target labels a representation as reality. The applicable OLS-1/OLS-2 boundary test receives FAIL; later correct explanation does not repair it.
2. A profile composition omits a mandatory dependency. The relevant OLS-3 test receives FAIL or INCOMPLETE according to the available evidence; the profile class cannot pass.
3. An implementation claims Full Suite conformance while declaring VALIDATE unsupported. The relevant tests receive UNSUPPORTED; Full Suite does not pass.
4. Evidence is not supplied for an applicable requirement. The test receives INCOMPLETE, not PASS.
5. A report marks a requirement NOT APPLICABLE without identifying its false condition. The OLS-5 applicability/reporting tests receive FAIL.

# Annex F — Architectural Traceability

*Annex ID: `OLS5-ANNEX-F` — Trace ID: `TRACE-000174` — Informative*

| OLS-5 element | Frozen or specification source | Specification transformation |
| --- | --- | --- |
| Conformance purpose and targets | Phase 2D implementation boundary; Phase 3A Conformance Model | Converted declared targets into testable claim scopes without semantic authority. |
| Six classes | Phase 3G charter; OLS-0 suite dependency order | Registered cumulative conformance scopes. |
| Units and applicability | Phase 3A Conformance Model; OLS-0 normative/informative policy | Defined what is tested and when. |
| Requirement/test mapping | OLS-0 stable Test ID and traceability policies; Phase 3G charter | Assigned one stable normative test to every Version 1.0 requirement. |
| Test methods | Phase 3A test organization | Formalized implementation-neutral semantic and structural methods. |
| Status registry | Phase 3G charter | Defined five specification-level assessment results without semantic effect. |
| Evidence and reporting | Phase 3A claim structure and implementation conformance | Formalized inspectable evidence and complete report fields. |
| Certification boundaries | Phase 2D boundaries; OLS-1 through OLS-4 non-implications | Prevented conformance from certifying truth, quality, authority, behavior, or outcome. |

Conformance IDs, Method IDs, report fields, status aggregation, and the one-to-one Test ID mapping are conformance-level specification decisions authorized by the Phase 3 Charter. They introduce no language semantics.
