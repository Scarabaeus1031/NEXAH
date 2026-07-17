# Orientation Language Specification — OLS-0

## Specification Conventions and Suite Overview

| Metadata field | Value |
| --- | --- |
| Document ID | `OLS-0` |
| Edition | 1 |
| Suite version | `1.0.0` |
| Document revision | `1.0.0` |
| Status | Version 1.0 publication candidate |
| Publication date | 17 July 2026 |
| Language | English |
| Normative scope | Specification-wide editorial, identification, reference, maintenance, and citation conventions |
| Semantic scope | None |
| Replaces | None |
| Required by | `OLS-1`, `OLS-2`, `OLS-3`, `OLS-4`, `OLS-5`, `OLS-6`, `OLS-I` |
| Release manifest identifier | Pending assignment at suite publication |
| Persistent citation identifier | Unassigned |
| Architecture baseline | Phase 2D Canonical Architecture, frozen by ADR-0001 |

## Status of this document

This document is the constitutional entry point to the Orientation Language Specification suite. It governs how the suite is organized, read, identified, referenced, cited, versioned, traced, and editorially maintained.

OLS-0 does not define Orientation Language concepts, declarations, operators, profiles, derivations, conformance semantics, or implementation behavior. Those subjects belong to the owning specification parts identified in Annex A.

Except where a clause or annex is explicitly marked **Informative**, the main clauses of OLS-0 are **Normative**.

---

## 1 Scope

*Stable clause ID: `OLS0-CLS-0001` — Trace ID: `TRACE-000001` — Normative*

OLS-0 specifies:

- the organization of the Orientation Language Specification suite;
- the distinction between normative and non-normative material;
- the interpretation of specification-wide normative keywords;
- terminology and semantic-ownership policies;
- clause, identifier, registry, cross-reference, manifest, version, citation, conformance-reference, traceability, and maintenance conventions;
- the relationship between the suite, its architectural baseline, its decision record, its normative parts, and its informative companion.

`[OLS0-REQ-0001]` Every document claiming membership in the Orientation Language Specification suite shall apply the applicable conventions of OLS-0.

`[OLS0-REQ-0002]` OLS-0 shall not be cited as the authoritative definition of an Orientation Language semantic element.

OLS-0 does not specify the content of the Universal Base Language, declaration semantics, operator contracts, semantic profiles, derivation rules, conformance criteria, implementation mappings, or application behavior.

## 2 Purpose

*Stable clause ID: `OLS0-CLS-0002` — Informative*

The purpose of OLS-0 is to give independent readers, authors, implementers, assessors, maintainers, and standards bodies one stable method for navigating and interpreting the suite. Its conventions reduce ambiguity caused by duplicated definitions, changing clause numbers, mixed normative status, unqualified version references, and unclear semantic ownership.

OLS-0 governs the specification as a publication system. It does not assert that the architecture is empirically true or universally applicable.

## 3 Intended audience

*Stable clause ID: `OLS0-CLS-0003` — Informative*

The intended audience includes:

- people applying the Orientation Language;
- authors of Orientation Language expressions and artifacts;
- implementers of human or computational procedures;
- authors and maintainers of semantic profiles;
- conformance assessors and test-suite authors;
- educators, editors, and researchers;
- custodians of the specification and its registries;
- reviewers evaluating extensions or future architecture revisions.

No particular software platform, data format, academic discipline, organizational role, or implementation technology is assumed.

## 4 Reading paths

*Stable clause ID: `OLS0-CLS-0004` — Informative*

| Reader purpose | Recommended path |
| --- | --- |
| Understand the suite | OLS-0 → OLS-1 → relevant informative overview in OLS-I |
| Apply the base language | OLS-0 → OLS-1 → applicable declaration clauses in OLS-2 |
| Invoke or implement operators | OLS-0 → OLS-1 → OLS-2 → applicable profile in OLS-3 → OLS-5 |
| Use one or more profiles | OLS-0 → OLS-1 → OLS-2 → OLS-3 → applicable OLS-4 rules |
| Assess conformance | OLS-0 → OLS-1 through OLS-5 → applicable registered extensions in OLS-6 |
| Author an extension | OLS-0 → OLS-1 → OLS-2 → OLS-3 → OLS-5 → OLS-6 |
| Study examples or implementation mappings | controlling normative parts → OLS-I |
| Review architectural rationale | OLS-0 → ADR-0001 → informative traceability material in OLS-I |

The normative status of a clause does not depend on the reading path used to reach it.

## 5 Structure of the Orientation Language Specification suite

*Stable clause ID: `OLS0-CLS-0005` — Trace ID: `TRACE-000002` — Normative*

The suite consists of seven normative parts and one informative companion:

- `OLS-0` — Specification Conventions and Suite Overview;
- `OLS-1` — Universal Base Language;
- `OLS-2` — Declarations and Operator Contracts;
- `OLS-3` — Semantic Profiles and Composition;
- `OLS-4` — Derivations, Validation, Outcome, and Learning;
- `OLS-5` — Conformance and Test Requirements;
- `OLS-6` — Extensions, Versioning, and Governance;
- `OLS-I` — Informative Companion.

Annex A is the authoritative specification document registry for Version 1.0.

`[OLS0-REQ-0003]` A suite part shall define only material assigned to it by the document registry and the frozen architectural ownership model.

`[OLS0-REQ-0004]` A later-numbered part may reference an earlier part but shall not replace or redefine the earlier part’s authoritative content.

`[OLS0-REQ-0005]` OLS-I shall not supply semantic or conformance requirements absent from the normative suite.

## 6 Normative and informative material

*Stable clause ID: `OLS0-CLS-0006` — Trace ID: `TRACE-000003` — Normative*

### 6.1 Normative material

Normative material states requirements, prohibitions, recommendations, permissions, definitions, registries, or conditions used to determine interpretation or conformance.

`[OLS0-REQ-0006]` Every normative clause and normative annex shall be explicitly identifiable as normative through document structure, clause metadata, or annex title.

`[OLS0-REQ-0007]` Normative tables and figures shall identify their controlling clause or state their normative status directly.

### 6.2 Informative material

Informative material supports understanding but does not establish conformance. It includes explanations, notes, examples, diagrams, rationale, historical material, analytical material, and implementation guidance unless explicitly classified otherwise by a normative part.

`[OLS0-REQ-0008]` Informative material shall be marked **Informative** at the clause, section, annex, or document level.

`[OLS0-REQ-0009]` Informative material shall not override, narrow, broaden, or create a normative requirement.

### 6.3 Conflict

`[OLS0-REQ-0010]` If informative material conflicts with normative material, the normative material shall control and the conflict shall be recorded for editorial correction.

`[OLS0-REQ-0011]` Visual emphasis, physical proximity, repetition, implementation prevalence, or historical frequency shall not change the declared status of material.

## 7 Normative keywords

*Stable clause ID: `OLS0-CLS-0007` — Trace ID: `TRACE-000004` — Normative*

The following lowercase keywords have specification-wide meanings when used in normative text. Inflected capitalization at the beginning of a sentence has the same effect.

| Keyword | Meaning |
| --- | --- |
| **shall** | Expresses a requirement necessary for conformance. |
| **shall not** | Expresses a prohibition necessary for conformance. |
| **should** | Expresses a recommendation. A departure is permitted only when its implications are understood and documented where the applicable clause requires documentation. |
| **should not** | Expresses a practice that is not recommended. A departure is permitted only when its implications are understood and documented where the applicable clause requires documentation. |
| **may** | Expresses permission or an allowed option. It does not express a requirement. |
| **need not** | Expresses absence of a requirement. The stated action or property is optional unless another applicable clause requires it. |

`[OLS0-REQ-0012]` Normative obligations shall use the keywords defined in this clause.

`[OLS0-REQ-0013]` The words “must”, “must not”, “required”, “recommended”, “optional”, and similar prose shall not be used as substitutes for the normative keywords in normative clauses.

`[OLS0-REQ-0014]` Keywords appearing in quotations, examples, code, identifiers, document titles, or explicitly informative text shall not create normative obligations.

The keywords describe specification force only. They do not define Orientation Language semantics.

## 8 Terminology policy

*Stable clause ID: `OLS0-CLS-0008` — Trace ID: `TRACE-000005` — Normative*

### 8.1 Controlled vocabulary

The controlled terminology registry indexes terms used by the suite. Each controlled entry identifies one authoritative definition, one owning part, a status, and stable identifiers for relevant clauses.

`[OLS0-REQ-0015]` A controlled term shall have exactly one authoritative definition within a given compatible suite release.

`[OLS0-REQ-0016]` A controlled term shall be defined in the normative part that owns its responsibility.

`[OLS0-REQ-0017]` OLS-0 and the central terminology registry shall point to authoritative definitions rather than duplicate them.

### 8.2 Aliases

An alias is a non-authoritative label that points to a controlled term.

`[OLS0-REQ-0018]` An alias shall identify its target Term ID and shall not introduce an independent definition or transfer semantic ownership.

### 8.3 Historical terminology

Historical terminology records earlier, cultural, metaphorical, or non-mechanical usage. It belongs in OLS-I or an explicitly Historical registry entry.

`[OLS0-REQ-0019]` Historical occurrence shall not confer normative status.

`[OLS0-REQ-0020]` A historical term used in normative text shall either refer to an existing controlled term or be introduced through the applicable normative change process before it carries normative meaning.

### 8.4 Deprecated terminology

A deprecated term remains identifiable but is discouraged for new use.

`[OLS0-REQ-0021]` A deprecation record shall identify the affected Term ID, deprecation version, status, rationale, replacement if any, conformance impact, and retained historical reference.

`[OLS0-REQ-0022]` Deprecation shall not silently change an authoritative definition.

### 8.5 Typography

Primitive operator names are written in uppercase when used as controlled operator identifiers or semantic operator names. Controlled concept, declaration, and profile typography is governed by the owning part and indexed by Term ID.

## 9 Clause numbering policy

*Stable clause ID: `OLS0-CLS-0009` — Trace ID: `TRACE-000006` — Normative*

Visible clause numbers communicate reading order and hierarchy. They are not permanent identity.

`[OLS0-REQ-0023]` Main clauses shall use decimal numbering beginning with 1 in each part.

`[OLS0-REQ-0024]` Subclauses shall extend the parent number using decimal components.

`[OLS0-REQ-0025]` Annexes shall use uppercase letters assigned in publication order and shall state their normative or informative status in the annex title.

`[OLS0-REQ-0026]` Figures and tables shall be numbered within their document or annex and shall be cited together with their document ID.

`[OLS0-REQ-0027]` Renumbering shall not change a stable Clause ID or Requirement ID.

## 10 Stable identifier policy

*Stable clause ID: `OLS0-CLS-0010` — Trace ID: `TRACE-000007` — Normative*

### 10.1 General syntax

Stable identifiers use uppercase ASCII letters, digits, and hyphens. They are case-sensitive and contain no spaces. Human-readable labels may change; stable identifiers remain unchanged except under the correction process in Clause 24.

`[OLS0-REQ-0028]` Every identifier shall be unique within its identifier class and assigned registry scope.

`[OLS0-REQ-0029]` A published identifier shall not be reassigned to a different object.

`[OLS0-REQ-0030]` A retired identifier shall remain reserved and traceable.

### 10.2 Identifier classes

| Class | Pattern | Example | Registry owner |
| --- | --- | --- | --- |
| Document ID | `OLS-[0–6]` or `OLS-I` | `OLS-3` | OLS-0 Annex A |
| Clause ID | `OLS<part>-CLS-<four digits>` | `OLS3-CLS-0012` | Owning document |
| Requirement ID | `OLS<part>-REQ-<four digits>` | `OLS3-REQ-0042` | Owning document |
| Operator ID | `OP-<canonical name>` | `OP-VALIDATE` | OLS-2 |
| Profile ID | `PROFILE-<canonical name>` | `PROFILE-EVIDENCE-VALIDATION` | OLS-3 or registered extension |
| Declaration ID | `DECL-<canonical name>` | `DECL-EVIDENCE-CLASS` | OLS-2 or registered extension |
| Term ID | `TERM-<canonical name>` | `TERM-ORIENTATION` | Controlled terminology registry |
| Trace ID | `TRACE-<six digits>` | `TRACE-000142` | Traceability registry |
| Test ID | `TEST-OLS<part>-<four digits>` | `TEST-OLS3-0042` | OLS-5 test registry |

For identifier patterns, `<canonical name>` is an uppercase hyphen-separated registry key. The exact semantic names and inventories are supplied only by their owning parts.

`[OLS0-REQ-0031]` Clause and Requirement IDs shall remain independent of visible clause numbering.

`[OLS0-REQ-0032]` A normative requirement shall have exactly one Requirement ID, even when explanatory text or tables repeat its human-readable wording.

`[OLS0-REQ-0033]` Multiple requirements shall not be combined under one Requirement ID when they can produce independent conformance outcomes.

`[OLS0-REQ-0034]` Machine-readable exports shall preserve identifiers exactly as published.

## 11 Cross-reference policy

*Stable clause ID: `OLS0-CLS-0011` — Trace ID: `TRACE-000008` — Normative*

`[OLS0-REQ-0035]` A normative cross-reference shall identify the target Document ID and stable Clause ID, Requirement ID, registry identifier, or annex identifier as applicable.

`[OLS0-REQ-0036]` A visible clause number or title may accompany a stable identifier for readability but shall not be the sole target of a normative cross-reference.

`[OLS0-REQ-0037]` Cross-document references shall identify a compatible suite version directly or through the release manifest.

`[OLS0-REQ-0038]` A reference to an informative source shall be labeled informative when its status is not evident from the source Document ID or citation.

`[OLS0-REQ-0039]` Broken, ambiguous, or version-incompatible normative references shall be treated as publication defects and shall not be resolved by inferred intent.

References do not copy the target’s definition or transfer its ownership.

## 12 Semantic ownership policy

*Stable clause ID: `OLS0-CLS-0012` — Trace ID: `TRACE-000009` — Normative*

Semantic ownership identifies the single specification location authorized to define a semantic responsibility. OLS-0 governs how ownership is respected; it does not assign or define semantic elements beyond the document allocation recorded in Annex A.

`[OLS0-REQ-0040]` Each primitive concept and primitive operator shall resolve to exactly one semantic owner identified by the applicable normative registry.

`[OLS0-REQ-0041]` A referencing part, profile, annex, implementation, example, or extension shall not redefine an owned semantic element.

`[OLS0-REQ-0042]` Referencing an owned semantic element shall not transfer ownership.

`[OLS0-REQ-0043]` If two normative texts appear to define the same owned responsibility differently, publication shall stop for the affected text until the ownership conflict is corrected or referred to an Architecture Revision Process.

## 13 Registry policy

*Stable clause ID: `OLS0-CLS-0013` — Trace ID: `TRACE-000010` — Normative*

The suite uses controlled registries for documents, clauses, requirements, terminology, declarations, operators, profiles, derivations, traceability records, conformance tests, extensions, versions, and deprecations.

`[OLS0-REQ-0044]` Each registry entry shall have a stable identifier, status, owner, version of introduction, and controlling normative reference.

`[OLS0-REQ-0045]` A registry shall not contain a second authoritative definition when the controlling clause already supplies one.

`[OLS0-REQ-0046]` A normative registry shall be published as a normative annex or normative clause of its owning part.

`[OLS0-REQ-0047]` A machine-readable registry export shall be treated as an implementation artifact unless a normative clause explicitly establishes its precedence and equivalence rules.

`[OLS0-REQ-0048]` Registry changes shall be included in the release manifest and change record.

If a machine-readable export and its controlling human-readable normative registry differ, the human-readable normative registry controls unless that registry explicitly states otherwise.

## 14 Release manifest policy

*Stable clause ID: `OLS0-CLS-0014` — Trace ID: `TRACE-000011` — Normative*

A release manifest fixes the exact set of compatible suite parts and associated controlled artifacts for one release.

`[OLS0-REQ-0049]` Every published suite release shall include one release manifest.

`[OLS0-REQ-0050]` The release manifest shall identify:

- suite version and release date;
- each Document ID, title, edition, revision, status, and content digest;
- normative and informative parts included in the release;
- required dependency versions;
- normative registry versions;
- conformance test-suite version;
- traceability export version;
- applicable errata and deprecations;
- superseded release, if any.

`[OLS0-REQ-0051]` A release manifest shall not claim compatibility for a set of parts whose declared dependencies conflict.

`[OLS0-REQ-0052]` File names and repository locations shall not substitute for the release manifest.

## 15 Version compatibility

*Stable clause ID: `OLS0-CLS-0015` — Trace ID: `TRACE-000012` — Normative*

The suite version has the form `MAJOR.MINOR.REVISION`. OLS-6 defines the complete versioning and change-control model.

`[OLS0-REQ-0053]` A citation or conformance claim shall identify the suite version against which it is made.

`[OLS0-REQ-0054]` Compatibility among independently revised parts shall be established by a release manifest, not inferred from matching major numbers alone.

`[OLS0-REQ-0055]` An editorial revision shall not change normative meaning, requirement applicability, semantic ownership, or conformance outcome.

`[OLS0-REQ-0056]` A version reference lacking a revision number may be used only when the intended release manifest unambiguously resolves the revision.

The Version 1.0 suite corresponds to suite version `1.0.0` unless a later compatible release manifest states otherwise.

## 16 Citation rules

*Stable clause ID: `OLS0-CLS-0016` — Trace ID: `TRACE-000013` — Normative*

### 16.1 Whole-document citation

A whole-document citation uses:

> Orientation Language Specification, `OLS-<part>`, *Title*, Edition, document revision, suite version, publication date.

### 16.2 Clause and requirement citation

A precise citation uses the Document ID and stable identifier:

> `OLS-3`, `OLS3-CLS-0012`, suite version `1.0.0`.

or:

> `OLS-3`, `OLS3-REQ-0042`, suite version `1.0.0`.

### 16.3 Registry citation

A registry citation uses the Document ID, registry or annex identifier, entry ID, and suite version.

`[OLS0-REQ-0057]` A citation intended to support a normative claim shall cite the controlling normative clause or registry entry rather than an informative paraphrase.

`[OLS0-REQ-0058]` A citation shall preserve the target identifier and suite version exactly.

`[OLS0-REQ-0059]` A citation to superseded or deprecated material shall state that status.

`[OLS0-REQ-0060]` External sources shall be cited with sufficient bibliographic or persistent-identifier information to locate the cited edition.

## 17 Conformance reference policy

*Stable clause ID: `OLS0-CLS-0017` — Trace ID: `TRACE-000014` — Normative*

OLS-5 defines conformance targets, claims, requirements, and test evidence. OLS-0 defines only how they are referenced.

`[OLS0-REQ-0061]` A conformance claim shall identify its target, suite version, applicable normative parts, Requirement IDs, active profiles where applicable, and test evidence required by OLS-5.

`[OLS0-REQ-0062]` A conformance claim shall not rely solely on a document title, informal phrase, implementation label, or informative example.

`[OLS0-REQ-0063]` A claim of profile conformance shall cite the Profile ID and the release manifest that establishes the compatible profile specification.

`[OLS0-REQ-0064]` Passing test evidence shall not be cited as proof of claims beyond the declared conformance scope.

## 18 Traceability overview

*Stable clause ID: `OLS0-CLS-0018` — Trace ID: `TRACE-000015` — Normative*

Traceability connects specification clauses to the frozen architecture, architecture elements to specification clauses, requirements to tests, and published changes to affected identifiers.

`[OLS0-REQ-0065]` Every normative clause shall have a Trace ID mapping it to its architectural source, architectural classification, semantic owner where applicable, and relevant ADR decision.

`[OLS0-REQ-0066]` Every Requirement ID shall map to a Test ID or to a recorded explanation that direct testing is not applicable.

`[OLS0-REQ-0067]` Reverse traceability shall identify every specification clause that realizes a frozen normative architectural artifact.

`[OLS0-REQ-0068]` Earlier research evidence may support traceability but shall not override the Phase 2D Canonical Architecture.

The complete human-readable traceability index belongs in OLS-I. Machine-readable exports remain subject to Clause 13.

## 19 Relationship to ADR-0001

*Stable clause ID: `OLS0-CLS-0019` — Trace ID: `TRACE-000016` — Normative*

ADR-0001 records the accepted architectural rationale and the Architecture Freeze dated 17 July 2026. It is not part of the normative language specification and does not replace normative clauses in OLS-1 through OLS-6.

`[OLS0-REQ-0069]` Phase 3 specification text shall remain consistent with the architecture frozen by ADR-0001.

`[OLS0-REQ-0070]` ADR-0001 may be cited as architectural rationale but shall not be used as a substitute for a controlling normative clause after that clause is published.

## 20 Relationship to the Phase 2D Architecture

*Stable clause ID: `OLS0-CLS-0020` — Trace ID: `TRACE-000017` — Normative*

The Phase 2D Canonical Architecture is the sole active semantic source for drafting Version 1.0. Phase 2D artifacts retain their assigned architectural classifications.

`[OLS0-REQ-0071]` Version 1.0 specification drafting shall describe the frozen Phase 2D architecture without adding, removing, or reallocating semantic responsibilities.

`[OLS0-REQ-0072]` Earlier phases may be cited for historical or research traceability but shall not override the Phase 2D baseline.

`[OLS0-REQ-0073]` An apparent need to change a frozen semantic inventory, responsibility, ownership, composition rule, or accepted derivation shall be treated as an architecture-revision question rather than an editorial correction.

## 21 Relationship to OLS-1 through OLS-6

*Stable clause ID: `OLS0-CLS-0021` — Trace ID: `TRACE-000018` — Normative*

OLS-1 through OLS-6 contain the normative language, conformance, extension, and governance clauses allocated by Annex A.

`[OLS0-REQ-0074]` A definition, contract, profile rule, derivation, or conformance requirement shall be cited from its owning normative part.

`[OLS0-REQ-0075]` OLS-0 shall control suite-wide editorial interpretation where it does not conflict with the semantic ownership of OLS-1 through OLS-6.

`[OLS0-REQ-0076]` If a suite-wide convention and a semantic clause appear to conflict, publication or maintenance shall stop for the affected text until the conflict is classified and corrected; neither clause shall be silently ignored.

## 22 Relationship to OLS-I

*Stable clause ID: `OLS0-CLS-0022` — Trace ID: `TRACE-000019` — Normative*

OLS-I is the Informative Companion. It may contain overviews, examples, counterexamples, implementation guidance, historical and cultural material, analytical rationale, mappings, traceability indexes, and bibliography.

`[OLS0-REQ-0077]` OLS-I shall identify the suite release it explains.

`[OLS0-REQ-0078]` OLS-I shall cite the controlling normative clauses for any normative behavior it illustrates.

`[OLS0-REQ-0079]` Revision of OLS-I alone shall not change conformance to a fixed normative release.

## 23 Future architecture revisions

*Stable clause ID: `OLS0-CLS-0023` — Trace ID: `TRACE-000020` — Normative*

An Architecture Revision Process applies when a proposal would change the frozen semantic architecture. OLS-6 defines extension and version governance; it does not authorize silent architectural change.

`[OLS0-REQ-0080]` Work on an affected specification clause shall stop when completing it requires a new universal primitive, removal of an accepted primitive, changed responsibility, changed ownership, changed profile composition, changed accepted derivation, or changed normative status for informative or implementation material.

`[OLS0-REQ-0081]` An architecture-revision proposal shall remain outside the current normative release until approved through an explicit future Architecture Revision Process and decision record.

`[OLS0-REQ-0082]` Rejected, deferred, or unresolved proposals shall remain traceable and shall not be represented as current semantics.

## 24 Editorial maintenance rules

*Stable clause ID: `OLS0-CLS-0024` — Trace ID: `TRACE-000021` — Normative*

### 24.1 Change classification

`[OLS0-REQ-0083]` Every proposed maintenance change shall be classified as editorial, backward-compatible normative, deprecation, or architectural before publication.

`[OLS0-REQ-0084]` A change that affects interpretation, applicability, ownership, requirement force, or conformance outcome shall not be classified as editorial.

### 24.2 Corrections and errata

`[OLS0-REQ-0085]` Published errata shall identify affected stable IDs, affected versions, correction text, classification, approval record, and release incorporation status.

`[OLS0-REQ-0086]` A correction to a duplicated or malformed identifier shall preserve the erroneous identifier as a traceable alias or tombstone and shall not reassign it.

### 24.3 Duplication control

`[OLS0-REQ-0087]` Normative definitions and requirements shall appear once in their owning location; other occurrences shall be cross-references or clearly informative summaries.

`[OLS0-REQ-0088]` Generated indexes and registry exports shall identify their controlling source and generation version.

### 24.4 Review gates

`[OLS0-REQ-0089]` A normative publication shall complete editorial, cross-reference, traceability, identifier-uniqueness, dependency, normative-status, and conformance-impact review.

`[OLS0-REQ-0090]` Unresolved ownership, architecture, or normative-status conflicts shall block publication of the affected release.

## 25 Document metadata

*Stable clause ID: `OLS0-CLS-0025` — Trace ID: `TRACE-000022` — Normative*

`[OLS0-REQ-0091]` Every suite document shall publish the following metadata:

- Document ID;
- title;
- edition;
- suite version;
- document revision;
- status;
- publication or revision date;
- language;
- normative or informative scope;
- semantic scope;
- supersession status;
- required dependencies;
- release-manifest identifier;
- architecture baseline or compatible architecture generation;
- persistent citation identifier when assigned.

`[OLS0-REQ-0092]` Metadata shall not be used to imply semantic scope that the document registry does not assign.

`[OLS0-REQ-0093]` A metadata change affecting version compatibility, status, dependency, or supersession shall be recorded in the release manifest and change history.

---

# Annex A — Specification document registry

*Annex ID: `OLS0-ANN-A` — Trace ID: `TRACE-000023` — Normative*

## A.1 Registry authority

This annex is the Version 1.0 normative registry of Orientation Language Specification documents.

`[OLS0-REQ-0094]` A document shall claim membership in the Version 1.0 suite only under an identifier and role listed in this registry or added through the OLS-6 extension and release process.

## A.2 Document registry

| Document ID | Title | Primary status | Allocated responsibility | Normative dependencies |
| --- | --- | --- | --- | --- |
| `OLS-0` | Specification Conventions and Suite Overview | Normative conventions; informative overview where marked | Suite organization, normative language, identifiers, references, registries, manifests, citation, maintenance | None within the suite |
| `OLS-1` | Universal Base Language | Normative Universal and universal operator responsibility | Universal semantic foundation and boundaries | `OLS-0` |
| `OLS-2` | Declarations and Operator Contracts | Normative Declaration and Normative Operator Contract | Declaration rules, complete primitive contracts, primitive operator ownership | `OLS-0`, `OLS-1` |
| `OLS-3` | Semantic Profiles and Composition | Normative Profile | Frozen profiles, activation, dependencies, ownership, legal composition, conflicts, reporting | `OLS-0`, `OLS-1`, `OLS-2` |
| `OLS-4` | Derivations, Validation, Outcome, and Learning | Normative Derivation Rule, Conditional Derivation, and Normative Profile | Derivation registries and cross-profile validation/outcome order | `OLS-0`, `OLS-1`, `OLS-2`, `OLS-3` |
| `OLS-5` | Conformance and Test Requirements | Normative conformance | Conformance targets, claims, applicability, errors, tests, and result boundaries | `OLS-0` through `OLS-4` |
| `OLS-6` | Extensions, Versioning, and Governance | Normative specification governance | Compatible extensions, registration, change classes, versions, deprecation, architecture-revision boundary | `OLS-0`, `OLS-1`, `OLS-3`, `OLS-5` |
| `OLS-I` | Informative Companion | Informative, Historical, Implementation Guidance, and Analytical | Explanations, examples, mappings, history, rationale, traceability, bibliography | Applicable normative parts |

## A.3 Registry boundaries

`[OLS0-REQ-0095]` A Document ID shall not be reused for a different allocated responsibility within Version 1.0.

`[OLS0-REQ-0096]` A document dependency shall not authorize the dependent document to redefine the dependency.

---

# Annex B — Architecture-to-specification mapping

*Annex ID: `OLS0-ANN-B` — Informative*

| Frozen architectural category | Specification location | Notes |
| --- | --- | --- |
| Universal Base Language | OLS-1 | Mandatory semantic foundation |
| Universal concepts | OLS-1 | Authoritative definitions remain there |
| Universal primitive operators | OLS-1 for responsibility; OLS-2 for complete contracts | Ownership is not duplicated |
| Required declarations | OLS-2 | Includes omission and incompatibility rules |
| Semantic profiles | OLS-3 | Includes profile-owned primitives and dependencies |
| Profile composition | OLS-3 | Includes activation, conflicts, and reporting |
| Primitive operator ownership | OLS-2 | Profile references do not transfer ownership |
| Accepted and conditional derivations | OLS-4 | Status remains distinct |
| Validation and outcome order | OLS-4 | Cross-profile sequence |
| Conformance | OLS-5 | Evaluates semantics without creating them |
| Compatible extension and version governance | OLS-6 | Bound by the Architecture Freeze |
| Informative Historical Component | OLS-I | No semantic conformance effect |
| Implementation Realization Layer | OLS-I | Guidance; no semantic authority |
| Analytical rationale and research trace | OLS-I | Audit support only |

The mapping describes publication placement. It does not change the architectural classification of any source artifact.

## B.2 OLS-0 trace summary

| Trace ID | OLS-0 subject | Governing source | Nature of specification text |
| --- | --- | --- | --- |
| `TRACE-000001` | Scope | Phase 3 Specification Charter; Phase 3A document structure | Editorial scope |
| `TRACE-000002` | Suite structure | Phase 3A specification overview and document structure | Editorial organization |
| `TRACE-000003` | Normative/informative status | Phase 2D normative classification; Phase 3A normative structure | Classification transcription and editorial marking |
| `TRACE-000004` | Normative keywords | Phase 3 Charter; Phase 3A OLS-0 allocation | Specification convention |
| `TRACE-000005` | Terminology policy | Phase 3A glossary and traceability strategies | Specification convention |
| `TRACE-000006` | Clause numbering | Phase 3A document and traceability structures | Publication convention |
| `TRACE-000007` | Stable identifiers | Phase 3A traceability model | Identifier convention |
| `TRACE-000008` | Cross-references | Phase 3A traceability model and dependency graph | Reference convention |
| `TRACE-000009` | Semantic ownership | Phase 2D operator ownership and profile architecture; Phase 3A normative structure | Ownership-preservation rule |
| `TRACE-000010` | Registries | Phase 3A overview, traceability model, and dependency graph | Publication-control convention |
| `TRACE-000011` | Release manifests | Phase 3A specification overview and versioning model | Release-control convention |
| `TRACE-000012` | Version compatibility | Phase 3A versioning model | Version convention |
| `TRACE-000013` | Citations | Phase 3A traceability model | Citation convention |
| `TRACE-000014` | Conformance references | Phase 3A conformance model | Reference convention |
| `TRACE-000015` | Traceability | Phase 3 Charter; Phase 3A traceability model | Traceability convention |
| `TRACE-000016` | ADR-0001 relationship | ADR-0001; Phase 3 Charter | Authority boundary |
| `TRACE-000017` | Phase 2D relationship | Phase 2D Canonical Architecture; Phase 3 Charter | Authority boundary |
| `TRACE-000018` | OLS-1 through OLS-6 relationship | Phase 3A overview and document structure | Document allocation |
| `TRACE-000019` | OLS-I relationship | Phase 2D informative components; Phase 3A normative structure | Status boundary |
| `TRACE-000020` | Architecture revisions | ADR-0001; Phase 3 Charter; Phase 3A extension model | Freeze boundary |
| `TRACE-000021` | Editorial maintenance | Phase 3A traceability and versioning models | Maintenance convention |
| `TRACE-000022` | Document metadata | Phase 3A overview and versioning model | Publication convention |
| `TRACE-000023` | Document registry | Phase 3A overview, document structure, and dependency graph | Normative document allocation |

These records establish Phase 3 source coverage. Detailed requirement-to-test mappings are added under OLS-5 without changing this architecture trace.

---

# Annex C — Reader guide

*Annex ID: `OLS0-ANN-C` — Informative*

## C.1 How to read a requirement

A normative requirement consists of its controlling clause, normative keyword, stable Requirement ID, applicable definitions, and referenced conditions. Examples and notes may clarify the requirement but do not replace it.

## C.2 How to find a definition

1. Locate the Term ID in the controlled terminology registry.
2. Follow the entry to the owning normative part and Clause ID.
3. Read the definition together with its applicable boundaries and references.
4. Treat aliases, examples, and historical uses as non-authoritative unless a normative clause states otherwise.

## C.3 How to cite the suite

For general discussion, cite the part, title, edition, revision, suite version, and date. For a precise claim, add the stable Clause ID, Requirement ID, or registry entry ID. Cite OLS-I only for informative material.

## C.4 How to assess a construction

Begin with OLS-1, identify applicable declarations and operators in OLS-2, identify active profiles and dependencies in OLS-3, apply relevant derivation or validation rules in OLS-4, and evaluate the resulting claim under OLS-5.

## C.5 How to report a problem

A useful issue report identifies the suite version, release manifest, Document ID, stable IDs, quoted text, observed ambiguity or conflict, proposed classification of the issue, and any conformance impact. An issue report does not itself modify the specification.

---

# Annex D — Glossary navigation

*Annex ID: `OLS0-ANN-D` — Informative*

## D.1 Terminology locations

| Terminology category | Authoritative or supporting location |
| --- | --- |
| Suite conventions, identifiers, citation, version references | OLS-0 |
| Universal semantic terms | OLS-1 |
| Declaration and primitive operator terms | OLS-2 |
| Profile names and profile-owned semantic terms | OLS-3 |
| Derivation, validation, outcome, recording, and learning terms | OLS-4 |
| Conformance and test terms | OLS-5 |
| Extension, change, version, and deprecation terms | OLS-6 |
| Historical, cultural, visual, analytical, and implementation vocabulary | OLS-I |

## D.2 Entry interpretation

A normative terminology entry contains a Term ID, preferred label, owning part, authoritative Clause ID, status, and applicable aliases. An informative entry identifies its non-normative category and any related controlled terms.

## D.3 Search order

When the same word appears in several contexts, readers should:

1. identify the status of the containing material;
2. consult the controlled terminology registry;
3. follow the owning-part reference;
4. apply any profile or declaration scope stated by the controlling clause;
5. avoid inferring equivalence from spelling, metaphor, or historical recurrence alone.

---

## End of OLS-0
