# Orientation Language Specification — OLS-6

## Extensions, Versioning, and Governance

| Metadata field | Value |
| --- | --- |
| Document ID | `OLS-6` |
| Edition | 1 |
| Suite version | `1.0.0` |
| Document revision | `1.0.0` |
| Status | Version 1.0 publication candidate |
| Publication date | 17 July 2026 |
| Language | English |
| Normative scope | Compatible extensions, versioning, change classification, deprecation, publication lifecycle, release management, registry governance, and architecture-revision referral |
| Semantic scope | None; OLS-6 governs specification evolution and does not define Orientation Language semantics |
| Replaces | Phase 3A extension and versioning framework upon suite publication |
| Normative dependencies | `OLS-0`, `OLS-1`, `OLS-3`, `OLS-5` |
| Informative dependency | ADR-0001 architecture rationale and freeze record |
| Forward reference | `OLS-I` for informative history, rationale, examples, and implementation guidance |
| Release manifest identifier | Pending assignment at suite publication |
| Persistent citation identifier | Unassigned |
| Architecture baseline | Phase 2D Canonical Architecture, frozen by ADR-0001 |

## Status of this document

OLS-6 is the authoritative Version 1.0 specification-governance part. Clauses 1 through 24 and Annexes A and B are **Normative**. Annexes C and D are **Informative**.

OLS-6 governs future evolution. It does not add a semantic primitive, operator, declaration, profile, derivation, product, transition, or conformance meaning. An extension registered under OLS-6 remains subordinate to the semantic owners and conformance model of the compatible suite release.

---

## 1 Scope

*Stable clause ID: `OLS6-CLS-0001` — Trace ID: `TRACE-000175` — Normative*

OLS-6 specifies:

- compatibility principles and extension categories;
- registration of future profiles, profile-owned operators, profile-scoped declarations, and informative components;
- namespace, identifier, ownership, dependency, and conflict rules;
- application of OLS-5 conformance to extensions;
- suite and part versioning;
- change classification, backward compatibility, deprecation, and preservation;
- architecture-revision referral;
- change control, publication lifecycle, release manifests, and registry governance.

`[OLS6-REQ-0001]` OLS-6 shall govern future specification evolution without modifying Version 1.0 semantic architecture.

`[OLS6-REQ-0002]` OLS-6 shall not add, remove, redefine, or reassign an OLS-1 through OLS-4 semantic element or responsibility.

`[OLS6-REQ-0003]` A governance record, version number, registration, approval, publication, or deprecation shall not create semantic truth, evidence, authority outside its declared governance scope, or implementation behavior.

`[OLS6-REQ-0004]` A proposal requiring an architectural change shall leave the compatible-extension process and follow Clause 18.

## 2 Normative references

*Stable clause ID: `OLS6-CLS-0002` — Trace ID: `TRACE-000176` — Normative*

The following documents are normatively indispensable:

- `OLS-0`, *Specification Conventions and Suite Overview*, Edition 1;
- `OLS-1`, *Universal Base Language*, Edition 1;
- `OLS-3`, *Semantic Profiles and Composition*, Edition 1;
- `OLS-5`, *Conformance and Testing*, Edition 1.

OLS-2 and OLS-4 are controlling references whenever an extension references declarations, primitive operator contracts, derivations, products, or transitions owned there.

`[OLS6-REQ-0005]` OLS-6 shall apply OLS-0 conventions, OLS-1 inheritance and boundaries, OLS-3 profile composition, and OLS-5 conformance without redefining them.

`[OLS6-REQ-0006]` An extension shall cite every owning normative part whose semantics or conformance requirements it references.

`[OLS6-REQ-0007]` A reference to a compatible suite element shall preserve its stable identifier, owner, version, status, and prohibited implications.

## 3 Terms and governance model

*Stable clause ID: `OLS6-CLS-0003` — Trace ID: `TRACE-000177` — Normative*

For OLS-6:

- **extension** means a registered addition that remains outside the frozen Version 1.0 inventories unless activated under its compatible release;
- **compatible extension** means an optional extension that preserves every applicable prior semantic and conformance obligation;
- **extension package** means the complete registration, normative or informative content, tests, traceability, compatibility declaration, and change record for one extension;
- **architecture revision** means the separate process required before frozen semantic architecture may change;
- **release** means the exact set of parts and controlled artifacts fixed by one release manifest;
- **suite version** means the `MAJOR.MINOR.REVISION` identifier of a release;
- **document revision** means the revision of one suite part selected by a release manifest;
- **deprecation** means an explicit non-destructive status warning that preserves identity and history;
- **tombstone** means a reserved identifier record that prevents reassignment after retirement or correction;
- **change record** means the auditable record of classification, impact, review, approval, publication, and supersession;
- **release authority** means the recorded governance function that approves a manifest after all gates pass;
- **architecture authority** means the recorded governance function empowered by a separate architecture-revision process, not by OLS-6 alone.

These are specification-governance terms, not Orientation Language concepts.

`[OLS6-REQ-0008]` A governance term shall not be interpreted as a universal or profile semantic primitive.

`[OLS6-REQ-0009]` Every governance decision shall identify the acting function, decision scope, date, affected identifiers, and supporting record.

`[OLS6-REQ-0010]` Organizational implementation of governance roles may vary, but required separation of proposal, review, architecture referral, and release approval shall remain auditable.

## 4 Compatibility principles

*Stable clause ID: `OLS6-CLS-0004` — Trace ID: `TRACE-000178` — Normative*

A compatible extension inherits the published Universal Base Language and all applicable active-profile semantics. It adds only optional, explicitly activated, uniquely owned capability.

`[OLS6-REQ-0011]` A compatible extension shall preserve the Version 1.0 universal primitive inventory, universal operator responsibilities, declarations, ownership, profile composition, derivation rules, semantic transitions, and prohibited implications.

`[OLS6-REQ-0012]` A compatible extension shall not make a previously conforming Version 1.0 construction nonconforming when that extension is not activated.

`[OLS6-REQ-0013]` A compatible extension shall be explicitly identifiable, versioned, activated, and reported.

`[OLS6-REQ-0014]` No extension precedence rule shall override a definition, owner, boundary, conflict, or failure condition in the compatible base release.

`[OLS6-REQ-0015]` An extension shall preserve unsupported and unresolved status and shall not infer support from parseability, storage, similarity, or implementation presence.

`[OLS6-REQ-0016]` Compatibility shall be established by the completed Annex B declaration, applicable OLS-5 tests, and a release manifest; matching version numbers alone shall not establish it.

## 5 Extension categories

*Stable clause ID: `OLS6-CLS-0005` — Trace ID: `TRACE-000179` — Normative*

Every proposal receives exactly one category before normative review:

| Category | Meaning | Permitted release impact |
| --- | --- | --- |
| Compatible optional extension | New optional capability preserving the compatible base | MINOR |
| Compatible extension revision | Backward-compatible revision to an already registered extension without changing existing owner responsibilities | MINOR or REVISION according to impact |
| Editorial or informative addition | No normative interpretation, applicability, test, or conformance change | REVISION |
| Deprecated extension | Registered extension retained with explicit deprecated status | MINOR or REVISION when no requirement is removed |
| Incompatible architectural proposal | Requires frozen semantic change | No compatible release; Clause 18 referral |

`[OLS6-REQ-0017]` A proposal shall not enter registration until its category and rationale are recorded.

`[OLS6-REQ-0018]` Category shall be determined by semantic and conformance impact, not by document size, naming, implementation popularity, or claimed importance.

`[OLS6-REQ-0019]` Uncertain classification shall not be treated as editorial or compatible until the uncertainty is resolved.

`[OLS6-REQ-0020]` Reclassification shall preserve the earlier classification record and reason for change.

## 6 Extension registration lifecycle

*Stable clause ID: `OLS6-CLS-0006` — Trace ID: `TRACE-000180` — Normative*

The registration lifecycle is:

1. submission;
2. completeness review;
3. ownership and architecture screening;
4. dependency and conflict review;
5. conformance and negative testing;
6. traceability review;
7. compatibility and version classification;
8. approval or referral;
9. registry assignment;
10. inclusion in a release manifest.

`[OLS6-REQ-0021]` Every extension submission shall use Annex A.

`[OLS6-REQ-0022]` An incomplete submission shall not receive a registered extension identifier or publication status.

`[OLS6-REQ-0023]` Registration approval shall occur only after every applicable lifecycle stage passes.

`[OLS6-REQ-0024]` Rejection, deferral, withdrawal, or architecture referral shall preserve the proposal, evidence, review findings, and stable proposal identity.

`[OLS6-REQ-0025]` Registry assignment shall precede release-manifest inclusion.

`[OLS6-REQ-0026]` Release-manifest inclusion shall not repair an incomplete or incompatible registration.

## 7 Future profile registration

*Stable clause ID: `OLS6-CLS-0007` — Trace ID: `TRACE-000181` — Normative*

A future profile is a compatible optional extension governed by OLS-3 inheritance, activation, dependency, composition, conflict, and reporting rules.

`[OLS6-REQ-0027]` A future profile shall inherit the complete compatible Universal Base Language without modification.

`[OLS6-REQ-0028]` A future profile shall declare purpose, scope, unique Profile ID, dependencies, applicable declarations, referenced owners, composition rules, conflicts, prohibited modifications, and conformance obligations.

`[OLS6-REQ-0029]` A future profile shall not redefine any Version 1.0 profile or silently activate another profile.

`[OLS6-REQ-0030]` New profile primitive concepts, if proposed, shall be profile-scoped, uniquely owned, traceable, and absent from the universal inventory.

`[OLS6-REQ-0031]` A future profile shall remain optional for constructions and implementations that do not activate it.

`[OLS6-REQ-0032]` A change to an existing Version 1.0 profile purpose, ownership, required declarations, dependencies, composition, or prohibited implications shall follow Clause 18.

## 8 Future operator registration

*Stable clause ID: `OLS6-CLS-0008` — Trace ID: `TRACE-000182` — Normative*

A future primitive operator may be registered only as a capability owned by one registered future profile. Its contract remains governed by the OLS-2 contract model.

`[OLS6-REQ-0033]` A future primitive operator shall have one unique Operator ID and exactly one registered profile owner.

`[OLS6-REQ-0034]` Its contract shall identify purpose, inputs, declarations, preconditions, operation, outputs, preservation, failures, prohibited implications, owner, and traceability.

`[OLS6-REQ-0035]` A future operator shall not redefine, overload, alias as equivalent to, or transfer ownership from a Version 1.0 primitive operator.

`[OLS6-REQ-0036]` A universal primitive operator addition or reassignment shall follow Clause 18.

`[OLS6-REQ-0037]` A derived or specialized operator shall identify its generating owner and shall not acquire primitive status through implementation use.

`[OLS6-REQ-0038]` Operator registration shall include positive, boundary, failure, and prohibited-implication tests under OLS-5.

## 9 Future declaration registration

*Stable clause ID: `OLS6-CLS-0009` — Trace ID: `TRACE-000183` — Normative*

A future declaration may be registered only as a profile-scoped instance distinction required by a compatible future profile.

`[OLS6-REQ-0039]` A future declaration shall have one unique Declaration ID and one registered profile scope.

`[OLS6-REQ-0040]` It shall specify responsibility, applicability, omission, incompatibility, scope, preservation, dependencies, and explicit default behavior.

`[OLS6-REQ-0041]` No inferred default shall exist unless the compatible extension explicitly registers and tests it within its profile scope.

`[OLS6-REQ-0042]` A future declaration shall not change the meaning, omission, incompatibility, preservation, or responsibility of a Version 1.0 declaration.

`[OLS6-REQ-0043]` A declaration proposed as universal or independent of profile scope shall follow Clause 18.

## 10 Future informative components

*Stable clause ID: `OLS6-CLS-0010` — Trace ID: `TRACE-000184` — Normative*

Informative, historical, analytical, educational, visual, and implementation material may be added without semantic effect when its status and controlling references are explicit.

`[OLS6-REQ-0044]` An informative addition shall identify its status, compatible suite release, controlling normative references where applicable, provenance, and maintainer.

`[OLS6-REQ-0045]` Informative material shall not supply missing normative semantics, requirements, ownership, validation, authority, or conformance.

`[OLS6-REQ-0046]` A conflict between informative material and normative text shall be resolved in favor of the normative text and recorded for correction.

`[OLS6-REQ-0047]` Promotion of informative or implementation material into semantic architecture shall follow Clause 18.

## 11 Identifier, namespace, and ownership governance

*Stable clause ID: `OLS6-CLS-0011` — Trace ID: `TRACE-000185` — Normative*

Extension identifiers use OLS-0 syntax and a registered namespace. An Extension ID has the form `EXT-<NAMESPACE>-<NAME>`. Profile, Operator, Declaration, and Term IDs belonging to an extension include the registered namespace within their canonical-name component.

`[OLS6-REQ-0048]` Every extension namespace shall be unique, stable, reserved after retirement, and owned by one registry entry.

`[OLS6-REQ-0049]` A stable identifier shall not be reassigned to another object, owner, or meaning.

`[OLS6-REQ-0050]` An alias shall point to one registered identifier and shall not create a second definition or owner.

`[OLS6-REQ-0051]` An ownership registry collision shall block registration and release.

`[OLS6-REQ-0052]` Referencing Version 1.0 semantics shall not transfer ownership to the extension namespace.

`[OLS6-REQ-0053]` Retired, corrected, or replaced identifiers shall remain as reserved traceable tombstones.

## 12 Dependencies, composition, and conflicts

*Stable clause ID: `OLS6-CLS-0012` — Trace ID: `TRACE-000186` — Normative*

Extensions compose only through explicit activation and resolved version-compatible dependencies. OLS-3 rules control profile composition.

`[OLS6-REQ-0054]` An extension shall declare mandatory and conditional dependencies by stable identifier and compatible version range.

`[OLS6-REQ-0055]` Every dependency shall resolve before extension capability is treated as available.

`[OLS6-REQ-0056]` An extension shall declare known ownership, declaration, representation, contract, profile, version, and non-semantic-authority conflicts.

`[OLS6-REQ-0057]` An unresolved conflict shall make the affected composition incomplete or malformed under the controlling OLS-3 rule and shall block a conforming extension claim.

`[OLS6-REQ-0058]` A dependency cycle, incompatible version range, or missing mandatory dependency shall block registration or release as applicable.

`[OLS6-REQ-0059]` Extension composition shall preserve every active profile, owner, declaration, provenance, evidence, uncertainty, and prohibited implication required by the compatible base.

## 13 Extension conformance and testing

*Stable clause ID: `OLS6-CLS-0013` — Trace ID: `TRACE-000187` — Normative*

OLS-5 controls conformance terminology, targets, methods, evidence, statuses, reports, and certification boundaries. OLS-6 adds no conformance status or method.

`[OLS6-REQ-0060]` A normative extension shall supply Requirement IDs and OLS-5-compatible Test IDs for every normative obligation.

`[OLS6-REQ-0061]` Every extension test shall identify the controlling requirement, applicability, method, evidence, expected condition, prohibited outcomes, and result status.

`[OLS6-REQ-0062]` Extension conformance shall include the compatible base class, every active extension profile, all dependencies, and composition tests.

`[OLS6-REQ-0063]` A base conformance result shall not imply support for an optional extension.

`[OLS6-REQ-0064]` Unsupported extension content shall remain unsupported and shall not be reported as conforming because it was stored, ignored, or parsed.

`[OLS6-REQ-0065]` Negative tests shall verify ownership, redefinition, dependency, conflict, prohibited implication, and architecture-boundary failures.

`[OLS6-REQ-0066]` An extension shall not enter a published release until its requirements and tests are included in the release’s controlled test registry.

`[OLS6-REQ-0067]` OLS-6 requirements shall be mapped into the OLS-5-owned test registry before Full Suite conformance to a release containing OLS-6 is claimed.

## 14 Version number model

*Stable clause ID: `OLS6-CLS-0014` — Trace ID: `TRACE-000188` — Normative*

The suite version is `MAJOR.MINOR.REVISION`.

- MAJOR identifies an architecture generation;
- MINOR identifies backward-compatible normative addition within one architecture generation;
- REVISION identifies editorial correction or clarification with no normative or conformance effect.

`[OLS6-REQ-0068]` Every release shall publish all three numeric components.

`[OLS6-REQ-0069]` Version `1.0.0` shall identify the first complete release based on the Phase 2D architecture frozen by ADR-0001.

`[OLS6-REQ-0070]` Every suite part shall state its document revision, compatible suite version, dependency revisions, and release-manifest identifier.

`[OLS6-REQ-0071]` Independently revised parts shall be compatible only when one release manifest selects them together.

`[OLS6-REQ-0072]` Version numbers shall classify change impact and shall not be used to imply empirical maturity, truth, or implementation quality.

## 15 Change classification

*Stable clause ID: `OLS6-CLS-0015` — Trace ID: `TRACE-000189` — Normative*

Classification is performed in this order:

1. Does the change modify frozen semantic meaning, responsibility, ownership, composition, accepted derivation, or normative status boundary? If yes: architecture revision and MAJOR.
2. Does it add optional backward-compatible normative capability or change conformance interpretation/outcome? If yes: MINOR.
3. Does it deprecate without removal? If yes: explicit deprecation in MINOR or REVISION according to normative impact.
4. Does it alter presentation only, with no interpretation, applicability, test, or outcome change? If yes: REVISION.

`[OLS6-REQ-0073]` Every proposed change shall have one recorded change class before approval.

`[OLS6-REQ-0074]` A change affecting interpretation, requirement force, applicability, test expectation, conformance outcome, ownership, or semantic boundary shall not be REVISION-only.

`[OLS6-REQ-0075]` Uncertain impact shall be classified at the higher applicable review level until resolved.

`[OLS6-REQ-0076]` Splitting one change into smaller edits shall not reduce its aggregate classification.

`[OLS6-REQ-0077]` Change classification shall be independently reviewed before release approval.

## 16 Major, minor, and editorial releases

*Stable clause ID: `OLS6-CLS-0016` — Trace ID: `TRACE-000190` — Normative*

`[OLS6-REQ-0078]` A MAJOR release shall require a completed Architecture Revision Process, approving decision record, impact analysis, migration guidance, and new architecture-generation declaration.

`[OLS6-REQ-0079]` A MINOR release shall preserve all conforming claims from earlier releases in the same MAJOR version for capabilities those claims declared.

`[OLS6-REQ-0080]` A MINOR release may add optional profiles, profile-owned primitives/operators, profile-scoped declarations, equivalent syntax, tests, registries, and mappings only under the compatible-extension rules.

`[OLS6-REQ-0081]` A REVISION release shall not change normative meaning, requirement applicability, expected test result, ownership, compatibility, or conformance status.

`[OLS6-REQ-0082]` A correction found to have normative impact shall be reclassified before publication.

`[OLS6-REQ-0083]` A part-only editorial revision shall not alter the suite version unless incorporated by a new release manifest; the manifest shall select the exact part revision.

## 17 Backward compatibility

*Stable clause ID: `OLS6-CLS-0017` — Trace ID: `TRACE-000191` — Normative*

Compatibility is evaluated against declared conformance targets, capabilities, and active extensions.

`[OLS6-REQ-0084]` A later REVISION release shall preserve conformance outcomes for the same target and evidence.

`[OLS6-REQ-0085]` A later MINOR release shall preserve earlier conforming constructions within the same MAJOR version when no newly optional extension is activated.

`[OLS6-REQ-0086]` Optional extension support shall be separately declared and shall not be inferred from base support.

`[OLS6-REQ-0087]` A MAJOR release shall make no automatic backward-compatibility claim.

`[OLS6-REQ-0088]` A compatibility claim shall identify source release, target release, tested conformance targets, supported extensions, limitations, and evidence using Annex B.

`[OLS6-REQ-0089]` A compatibility claim shall not hide a changed failure, prohibited implication, evidence requirement, or unsupported capability.

## 18 Architecture-revision boundary

*Stable clause ID: `OLS6-CLS-0018` — Trace ID: `TRACE-000192` — Normative*

OLS-6 stops when a proposal requires modification of frozen semantic architecture. It does not approve architecture revisions.

Architecture referral is mandatory for:

- adding or removing a universal primitive;
- changing universal or profile primitive responsibility;
- adding or reassigning a universal primitive operator;
- changing Version 1.0 declaration responsibility;
- changing primitive ownership;
- changing existing profile purpose, dependencies, composition, or prohibited implications;
- changing accepted derivation semantics or cross-profile semantic order;
- promoting informative or implementation material into semantic authority;
- removing a required capability in a way that makes prior conforming constructions architecturally nonconforming.

`[OLS6-REQ-0090]` Work on affected normative text shall stop at the first architecture-revision condition.

`[OLS6-REQ-0091]` The proposal shall remain outside the current compatible release until an Architecture Revision Process and decision record approve it.

`[OLS6-REQ-0092]` Architecture referral shall preserve proposal identity, evidence, impact, alternatives, review findings, migration consequences, and unresolved questions.

`[OLS6-REQ-0093]` Rejected, deferred, or unresolved architecture proposals shall remain traceable and shall not be presented as current semantics.

`[OLS6-REQ-0094]` OLS-6 release authority shall not substitute for architecture authority.

## 19 Deprecation and historical preservation

*Stable clause ID: `OLS6-CLS-0019` — Trace ID: `TRACE-000193` — Normative*

Deprecation is explicit and non-destructive.

`[OLS6-REQ-0095]` A deprecation record shall identify affected stable ID, status, rationale, replacement or absence, first deprecated version, conformance impact, earliest eligible removal version, migration guidance, and retained source.

`[OLS6-REQ-0096]` Deprecation shall not remove or reassign the affected identifier.

`[OLS6-REQ-0097]` A requirement shall not be removed in the same MINOR release in which it is first deprecated.

`[OLS6-REQ-0098]` Normative removal shall occur only in a MAJOR release and shall require architecture review when frozen architecture is affected.

`[OLS6-REQ-0099]` Superseded and deprecated text, manifests, tests, traceability, and change records shall remain recoverable.

`[OLS6-REQ-0100]` A replacement shall not inherit the deprecated identifier unless it is the same governed object with unchanged identity.

## 20 Change control and review

*Stable clause ID: `OLS6-CLS-0020` — Trace ID: `TRACE-000194` — Normative*

Every change passes submission, classification, impact analysis, owner review, cross-reference and traceability review, conformance-impact review, approval, and release recording.

`[OLS6-REQ-0101]` A change record shall identify proposal ID, affected IDs, current and proposed versions, exact change, rationale, class, dependencies, compatibility impact, conformance/test impact, traceability, reviewers, decision, and release status.

`[OLS6-REQ-0102]` An affected semantic owner shall review every change referencing its owned material.

`[OLS6-REQ-0103]` No author or implementation shall acquire approval authority merely by proposing or using a change.

`[OLS6-REQ-0104]` Unresolved ownership, architecture, normative-status, dependency, identifier, or conformance conflict shall block approval.

`[OLS6-REQ-0105]` Approval shall apply only to the exact reviewed content and identified version.

`[OLS6-REQ-0106]` A post-approval content change shall invalidate approval unless separately classified and reviewed.

## 21 Publication lifecycle

*Stable clause ID: `OLS6-CLS-0021` — Trace ID: `TRACE-000195` — Normative*

Publication states are: Proposal, Draft, Publication Candidate, Approved, Published, Superseded, Deprecated, and Withdrawn. These are governance statuses only.

`[OLS6-REQ-0107]` Every controlled artifact shall identify exactly one current publication status.

`[OLS6-REQ-0108]` Proposal and Draft material shall not be cited as published normative authority.

`[OLS6-REQ-0109]` Publication Candidate status shall require completed content and pending final release gates; it shall not imply publication.

`[OLS6-REQ-0110]` Approved status shall identify the approving record and exact content digest.

`[OLS6-REQ-0111]` Published status shall require inclusion in one valid release manifest.

`[OLS6-REQ-0112]` Superseded, Deprecated, or Withdrawn status shall retain the last published identity, status history, replacement where any, and manifest references.

`[OLS6-REQ-0113]` Withdrawal shall not erase a published historical record.

## 22 Release management and manifest

*Stable clause ID: `OLS6-CLS-0022` — Trace ID: `TRACE-000196` — Normative*

The OLS-0 release-manifest fields remain controlling. OLS-6 governs assembly, review, approval, publication, and preservation of the manifest.

`[OLS6-REQ-0114]` Every published release shall have exactly one Release ID and one manifest.

`[OLS6-REQ-0115]` The manifest shall contain every field required by OLS0-REQ-0050 and shall additionally identify release approval, architecture generation, included extensions, compatibility declarations, change-record set, and registry digests.

`[OLS6-REQ-0116]` Every included document and normative registry shall have an exact version, status, dependency set, and content digest.

`[OLS6-REQ-0117]` A manifest shall not include a Draft, unresolved, incompatible, checksum-mismatched, or untested normative artifact.

`[OLS6-REQ-0118]` Release assembly shall verify document identity, identifier uniqueness, ownership, dependencies, cross-references, normative status, traceability, tests, deprecations, and content digests.

`[OLS6-REQ-0119]` The release authority shall approve the complete manifest and exact artifact set, not individual paths by implication.

`[OLS6-REQ-0120]` A published manifest and its artifacts shall be immutable; correction shall create a new release or governed erratum.

`[OLS6-REQ-0121]` Repository location shall not substitute for manifest identity or digest verification.

## 23 Registry governance

*Stable clause ID: `OLS6-CLS-0023` — Trace ID: `TRACE-000197` — Normative*

OLS-6 owns governance registries for extensions, suite versions/releases, change records, and deprecations. Semantic and conformance registries remain owned by their existing parts.

`[OLS6-REQ-0122]` Every governance registry entry shall contain stable ID, status, owner, introduction version, controlling reference, change history, and current release relation.

`[OLS6-REQ-0123]` A governance registry shall point to an existing semantic or conformance owner and shall not duplicate its authoritative definition.

`[OLS6-REQ-0124]` Registry changes shall be reviewed, versioned, traceable, included in the manifest, and tested where normative.

`[OLS6-REQ-0125]` Machine-readable exports shall identify controlling human-readable sources and generation version and shall not supersede them unless a controlling normative registry explicitly says otherwise.

`[OLS6-REQ-0126]` A registry collision, orphaned owner, unresolved dependency, or broken controlling reference shall block release.

`[OLS6-REQ-0127]` Registry history and tombstones shall remain available across releases.

## 24 Errata, preservation, and summary

*Stable clause ID: `OLS6-CLS-0024` — Trace ID: `TRACE-000198` — Normative*

`[OLS6-REQ-0128]` An erratum shall identify affected release and stable IDs, original and corrected text, classification, impact determination, approval, incorporation status, and tests affected.

`[OLS6-REQ-0129]` An erratum with normative or conformance impact shall not be applied as an unversioned editorial replacement.

`[OLS6-REQ-0130]` Every release shall remain available with manifest, artifacts, registries, tests, traceability, change log, deprecations, and errata.

`[OLS6-REQ-0131]` Later releases shall not erase superseded content, identifiers, decisions, rejected proposals, or architectural rationale.

`[OLS6-REQ-0132]` Version 1.0 governance shall preserve the frozen architecture until a separately approved architecture generation supersedes it.

---

# Annex A — Extension Registration Template

*Annex ID: `OLS6-ANNEX-A` — Trace ID: `TRACE-000199` — Normative*

Every extension registration contains:

| Field | Required content |
| --- | --- |
| Proposal ID | Stable pre-registration identity |
| Proposed Extension ID and namespace | Unique requested identifiers |
| Name, category, status, and purpose | Governance identity and bounded purpose |
| Proposer and maintainer | Recorded governance functions |
| Compatible architecture generation and suite version | Exact base |
| Normative or informative classification | Status boundary |
| Inherited base semantics | OLS-1 references |
| Active/required profiles and dependencies | IDs and compatible versions |
| New profile-scoped primitives, operators, or declarations | IDs, owners, contracts, and scopes where applicable |
| Existing owners referenced | Stable IDs and controlling clauses |
| Activation, composition, and conflict rules | OLS-3-compatible behavior |
| Prohibited modifications and implications | Preserved base boundaries |
| Requirements and tests | OLS-5-compatible mappings |
| Backward-compatibility evidence | Annex B declaration |
| Traceability | Forward and reverse mappings |
| Change classification and intended release | MAJOR/MINOR/REVISION impact |
| Deprecation and migration impact | If applicable |
| Review and decision records | Findings, approvals, referrals, dates |
| Content and registry digests | Exact reviewed artifacts |

`[OLS6-REQ-0133]` Every field in Annex A shall be completed or marked not applicable with a reason.

`[OLS6-REQ-0134]` A not-applicable entry shall not bypass a condition that applies to the proposed extension.

`[OLS6-REQ-0135]` The published extension registry entry shall resolve to the approved registration, exact content, tests, and release manifest.

# Annex B — Version Compatibility Declaration

*Annex ID: `OLS6-ANNEX-B` — Trace ID: `TRACE-000200` — Normative*

| Field | Required content |
| --- | --- |
| Declaration ID | Stable compatibility-record identity |
| Claimant and date | Responsible function and date |
| Source release | Release ID, suite version, manifest digest |
| Target release | Release ID, suite version, manifest digest |
| Compared parts and revisions | Exact Document IDs and digests |
| Compared registries and tests | Exact versions and digests |
| Conformance targets | Targets and prior claims assessed |
| Extensions | Supported, unsupported, activated, and excluded IDs |
| Change classification | MAJOR, MINOR, or REVISION |
| Preserved constructions and claims | Evidence-backed scope |
| Known incompatibilities and limitations | Explicit exclusions |
| Test evidence | OLS-5 reports and statuses |
| Deprecations and migration guidance | Applicable records |
| Decision and approval | Result, reviewers, authority, date |

`[OLS6-REQ-0136]` A compatibility declaration shall include every Annex B field.

`[OLS6-REQ-0137]` A compatible result shall be limited to the tested targets, capabilities, extensions, releases, and evidence.

`[OLS6-REQ-0138]` Missing evidence shall produce an incomplete compatibility determination rather than inferred compatibility.

# Annex C — Change Examples

*Annex ID: `OLS6-ANNEX-C` — Trace ID: `TRACE-000201` — Informative*

| Example | Likely class | Reason |
| --- | --- | --- |
| Correct a broken informative link without changing interpretation | REVISION | Presentation only |
| Add an optional profile inheriting the base and owning new profile-scoped capability | MINOR | Compatible optional normative addition |
| Add tests exposing an existing requirement without changing expected semantics | MINOR or REVISION after impact review | Classification depends on conformance impact |
| Mark an extension deprecated while retaining requirements and identity | MINOR or REVISION | Explicit status; no removal |
| Rename visible heading while stable IDs and meaning remain unchanged | REVISION | Editorial only |
| Change the universal primitive inventory | Architecture revision / MAJOR | Frozen architecture changes |
| Reassign a primitive operator owner | Architecture revision / MAJOR | Ownership changes |
| Treat an implementation mapping as a normative definition | Architecture revision referral | Normative-status boundary changes |

These examples do not replace impact analysis.

# Annex D — Architecture-Revision Referral Guide

*Annex ID: `OLS6-ANNEX-D` — Trace ID: `TRACE-000202` — Informative*

## D.1 Referral questions

1. Does the proposal change a universal primitive or operator?
2. Does it change an existing primitive responsibility or owner?
3. Does it change a Version 1.0 declaration responsibility?
4. Does it alter an existing profile’s purpose, dependencies, composition, or prohibited implications?
5. Does it alter an accepted derivation or validation/outcome order?
6. Does it promote informative or implementation material into semantic authority?
7. Does it remove a required capability so prior conforming constructions become nonconforming?

Any affirmative answer invokes Clause 18.

## D.2 Minimum referral record

Preserve the proposal, evidence, affected stable IDs, architectural impact, compatibility and migration effects, alternatives, review findings, unresolved questions, and requested decision scope. OLS-6 does not decide the architectural merits.

## D.3 Architectural traceability

| OLS-6 area | Governing source |
| --- | --- |
| Scope and freeze boundary | Phase 3 Charter; ADR-0001; OLS-0 Clause 23 |
| Compatibility and extension categories | Phase 3A Extension Model |
| Profile/operator/declaration registration | Phase 3A Extension Model; OLS-1/OLS-2/OLS-3 ownership boundaries |
| Extension conformance | Phase 3A Conformance Model; OLS-5 |
| Version classification and compatibility | Phase 3A Versioning Model; OLS-0 Clause 15 |
| Deprecation and preservation | Phase 3A Versioning Model; OLS-0 terminology and maintenance policies |
| Manifest and registries | OLS-0 Clauses 13–15 |
| Change control and publication gates | OLS-0 Clauses 23–25; Phase 3 Charter |

The Extension ID namespace, governance lifecycle statuses, templates, and decision-record fields are specification-level governance additions authorized by the Phase 3 Charter. They add no Orientation Language semantics.

