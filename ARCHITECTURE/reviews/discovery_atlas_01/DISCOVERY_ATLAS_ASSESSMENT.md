# NEXAH Discovery Atlas Assessment

Status: informative repository review  
Decision: **D — create a structured Evidence Atlas**

## Executive summary

NEXAH already has strong local portals: Architecture, System State, Research,
Validation, Findings, Applications, OLS, Library, and the Editorial Operating
System. What it lacks is a repository-level, claim-oriented view that answers
three questions together: what is claimed, what is its present status, and
where is its authoritative evidence.

The gap is not another architecture and not another evidence store. It is
navigation plus conservative classification. The smallest justified response
is a documentation-only **NEXAH Evidence Atlas** whose entries link to original
specifications, results, machine-readable summaries, tests, reviews, and
limitations. It must not become semantic authority.

This review identifies 28 candidate claim units. They span exact arithmetic,
released semantics, bounded experiments, negative results, limitations, open
hypotheses, applications, and three requested but repository-unavailable
evidence chains. That diversity and the distance between their sources justify
more than a few root links, while the quality of existing local bundles means
the repository does not need reorganization.

## Repository areas inspected

- root README, repository map, documentation and navigation pages;
- Architecture, System State, governance, review conventions, current and
  historical visuals;
- OLS specification, release 1.0.0, manifests, checksums, and release review;
- maintained implementation and tests;
- Research Foundation, Core Concepts, Findings, Validation, and historical
  experimental material;
- Prime Modular Resonance and both current prime validation bundles;
- Orientation Translation studies and independent reviews;
- NEXAH Demonstrator and validation tests;
- IEEE Geometry V1 application, manifest, artifacts, validation, and showcase;
- Library authority and catalog distinctions;
- Git-tracked history for the requested POA, structural-review, NTO, and
  DERIS/HYDRA materials.

The Architecture index itself states that six responsibilities remain distinct
and that its diagrams are not capability or conformance claims
([Architecture README](../../README.md#L12-L28)). System State separately
records implemented maturity and warns that the framework is not
comprehensively validated or unified into a stable runtime
([System State](../../SYSTEM_STATE.md#L34-L74)).

## Existing consolidation mechanisms

| Mechanism | What it does well | What it does not do |
|---|---|---|
| Root README | Separates subsystem authorities and routes readers | Does not enumerate independently meaningful claims |
| `REPOSITORY_MAP.md` | Maps directory responsibilities | Is directory-oriented, not evidence-chain-oriented |
| Architecture and System State | State boundaries and current implementation maturity | Do not consolidate research and application results |
| Research Index | Routes within Research | Does not include OLS, applications, Library, or architecture proofs |
| Findings portal | Preserves thematic research narratives | Contains historical and current claims at different strengths |
| Validation portal | Links modern frozen bundles | Does not surface reviewed application or architectural claims |
| Application READMEs | Give domain-local evidence boundaries | Are invisible as a cross-repository result landscape |
| OLS release package | Provides excellent local authority and integrity | Is deliberately not a repository findings index |
| Library | Curates human-facing Works | Explicitly does not replace repository evidence authority |

## The identified gap

The missing object is a **claim-level navigation layer**. A new reader can
usually find a subsystem, but cannot reliably discover:

1. which statements are exact, architectural, experimental, negative, open, or
   historical;
2. which summary has authority when historical prose is stronger than a later
   frozen result;
3. whether a plot is a representation or evidence;
4. whether an evidence chain is complete;
5. which important hypotheses failed;
6. which referenced programs are absent from the repository.

The Prime Modular Resonance README, for example, explicitly says that
non-uniform transition evidence exists while entropy and drift scaling remain
unresolved ([source](../../../RESEARCH/FINDINGS/PRIME_MODULAR_RESONANCE/README.md#L4-L7)).
The newer frozen comparison then rejects special Mod-17 status and the proposed
7-to-17 bridge ([results](../../../RESEARCH/VALIDATION/prime_modular_residue_comparison_01/RESULTS.md#L7-L11)).
Both are valuable, but no repository-level page currently shows their
relationship.

## Reasons for a central atlas

- At least 28 independently addressable claims or status records were found.
- Exact constructions, experiments, reviews, implementations, and applications
  use different local conventions.
- Important negative results are deeply nested.
- Historical prose sometimes uses stronger language than current frozen tests.
- Modern bundles have excellent provenance but remain visible mainly through
  the Validation portal.
- Requested POA, NTO, and DERIS/HYDRA chains are not addressable in this
  repository; an atlas would expose this absence immediately.
- The IEEE application demonstrates why claims and prohibited implications
  should be navigated together
  ([manifest](../../../APPLICATIONS/power_systems/ieee_geometry_v1/case_manifest.json#L109-L134)).

## Reasons against a central atlas

- Existing local portals are already good and must not be duplicated.
- A new index can drift, become stale, or silently strengthen source wording.
- “Discovery” can imply novelty or success and underrepresent negative results.
- Machine-readable metadata would create maintenance cost before a manual
  editorial practice is proven.
- A large per-claim catalog would become another competing authority.

These objections constrain the implementation; they do not eliminate the
claim-level navigation gap.

## Architectural implications

None. The atlas would be informative documentation. Research continues to own
hypotheses and evidence; OLS owns released semantics; Architecture owns
responsibility boundaries; implementations own behavior; applications own
bounded domain use; Library owns curated encounter. The atlas owns none of
these. This follows the repository's existing separation
([Architecture README](../../README.md#L64-L113)) and the constitutional
distinction between OLS definition, Kernel execution, and ORION navigation
([Constitution](../../../GOVERNANCE/ECOSYSTEM_CONSTITUTION.md#L197-L217)).

## Why this is not merely another README

A normal README routes to folders. The proposed atlas routes from a stable
claim unit to:

`status → scope → authority → evidence chain → limits → source`

Its additional value is controlled status and provenance. It should still be
implemented as ordinary Markdown first.

## Duplication and semantic-centralization risks

The atlas must quote or paraphrase only the minimum claim, never copy results
tables, formulas, or evidence artifacts. Every entry must name one authoritative
source and may name supporting or limiting sources. Changes in status require
source changes first. An atlas entry can be stale or wrong; it cannot overrule
its source.

## Minimal recommended action

In a separately approved task, create one entry page at
`docs/evidence/README.md` and populate it with the 28 reviewed entries as a
compact table. Do not create claim subpages or metadata in the first iteration.
Link that page from the root README, Research index, Validation portal, and
Applications index. Review it after one maintenance cycle before adding JSON.

## Things that must not change

- frozen Architecture, governance, OLS releases, or semantic definitions;
- ORION, Kernel, Processor, or application responsibilities;
- POA contracts or results;
- experiment specifications, results, checksums, raw artifacts, or histories;
- original evidence locations or authority;
- negative, inconclusive, blocked, and historical status;
- Library/editorial authority boundaries;
- wording that prevents benchmark or visual results from becoming physical,
  universal, causal, or operational claims.
