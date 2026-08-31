# Research Tree Inventory

## Complete census

The recursive tree contains 1,543 files in 227 directories, approximately 869 MB. Principal file types are: 880 PNG, 237 Python, 138 Markdown, 107 CSV, 80 JSON, 31 TXT, 23 NPY, 14 GIF, 5 HTML, and supporting metadata or archive formats.

Every object is covered by an owning-path row below. Binary, data, and source artifacts inherit the currentness and paper action of their owning package unless a later closed decision gives a specific artifact higher authority. The major documentary files are then listed individually.

## Owning-path inventory

| path | purpose | currentness | authority | claim level | paper relevance | action |
|---|---|---|---|---|---|---|
| `RESEARCH/` | Research corpus and navigation | PARTIALLY_CURRENT | Mixed | Mixed | Context and evidence archive | UPDATE |
| `RESEARCH/FOUNDATION/` | Formal and pre-formal foundations | PARTIALLY_CURRENT | Mixed | Level 1–3 | Main candidate source, with pruning | REWRITE |
| `RESEARCH/CORE_CONCEPTS/` | Concepts and simulations | HISTORICAL | Superseded working research | Level 1–3 | Background only | REMOVE_FROM_PAPER_PATH |
| `RESEARCH/CORE_CONCEPTS/JANUS/` | Janus/Rope experiments and claims | OVERCLAIMED | Historical experiment package | Level 1–3 | Selected local results only | ARCHIVE |
| `RESEARCH/VALIDATION/` | Experimental artifacts and validation records | PARTIALLY_CURRENT | Evidence archive | Level 1–3 | Bounded support after reclassification | KEEP |
| `RESEARCH/VALIDATION/BLIND_VALIDATION/` | Blind/predictive controls | USEFUL_SUPPORT | Local result packages | Level 2–3 | Supplementary evidence | KEEP |
| `RESEARCH/VALIDATION/CROSS_SYSTEM/` | Cross-system comparisons | PARTIALLY_CURRENT | Local result packages | Level 2–3 | Supporting cases, not universality | REWRITE |
| `RESEARCH/VALIDATION/PHASE2_CONTROLLED/` | Controlled cases | USEFUL_SUPPORT | Local result packages | Level 2–3 | Supporting evidence | KEEP |
| `RESEARCH/VALIDATION/PHASE3_PREDICTION/` | Prediction-oriented runs | PARTIALLY_CURRENT | Local result packages | Level 2–3 | Requires claim-by-claim audit | REWRITE |
| `RESEARCH/VALIDATION/PHASE4_CROSS_SYSTEM/` | Transfer attempts | PARTIALLY_CURRENT | Local result packages | Level 2–3 | Negative and mixed evidence useful | REWRITE |
| `RESEARCH/FINDINGS/` | Syntheses of experimental findings | OVERCLAIMED | Historical synthesis | Level 2–3 | Evidence leads, not paper authority | REWRITE |
| `RESEARCH/FINDINGS/PRIME_STRUCTURE/` | Prime/numeric structure findings | HISTORICAL | Closed or superseded exploration | Level 1–3 | Not central | ARCHIVE |
| `RESEARCH/FINDINGS/TRANSITIONS/` | Transition findings | PARTIALLY_CURRENT | Local experimental synthesis | Level 2–3 | Selected cases only | REWRITE |
| `RESEARCH/APPLIED_CASES/` | Applied demonstrations | HISTORICAL | Case-specific | Level 1–2 | Optional examples | ARCHIVE |
| `RESEARCH/FIGURES/` | Explanatory and result graphics | EXPRESSION_ONLY | Non-authoritative unless source-bound | Level 0–2 | Curated figures only | REMOVE_FROM_PAPER_PATH |
| `RESEARCH/NOTES/` | Working notes | HISTORICAL | Non-authoritative | Level 0–2 | No direct paper role | ARCHIVE |
| `RESEARCH/HISTORY/` | Historical and custody record | HISTORICAL | Provenance only | Mixed | Audit trail, not central evidence | KEEP |
| `RESEARCH/HISTORY/ROUTED_CUSTODY_2026-08-25/` | Routed incomplete custody packages | HISTORICAL | Custody record | Mixed | Excluded from paper core | KEEP |
| `RESEARCH/NEXAH_DEVELOPMENT/` | Legacy developmental work | SUPERSEDED | Historical | Level 0–2 | Historical background only | ARCHIVE |
| `RESEARCH/NEXAH_TRANSLATIONS/` | Cross-domain interpretive translations | OVERCLAIMED | Interpretive | Level 0–3 | Remove from technical paper | REMOVE_FROM_PAPER_PATH |
| `RESEARCH/SYSTEM_MODELS/` | Intended model area | UNDERDEFINED | None | None | No paper support | REMOVE_FROM_PAPER_PATH |
| `RESEARCH/THEORETICAL_EXTENSIONS/` | Explicitly exploratory extensions | HISTORICAL | Non-proved exploration | Level 0–2 | Future discussion at most | ARCHIVE |
| `RESEARCH/translations/` | Language translations | PARTIALLY_CURRENT | Derived text | Mirrors source authority | Publication support only | UPDATE |

## Major file inventory

| path | purpose | currentness | authority | claim level | paper relevance | action |
|---|---|---|---|---|---|---|
| `RESEARCH/README.md` | Research overview and navigation | PARTIALLY_CURRENT | Working overview | Level 1–3 | Useful orientation after correction | UPDATE |
| `RESEARCH/ABSTRACT.md` | Historical working abstract | STALE, OVERCLAIMED | Explicitly historical synthesis | Level 2–3 | Not a current abstract | SUPERSEDE |
| `RESEARCH/PAPER_DRAFT.md` | Transition-geometry manuscript draft | STALE, OVERCLAIMED | Working historical draft | Level 2–3 | Wrong center for frozen framework | SUPERSEDE |
| `RESEARCH/RESEARCH_INDEX.md` | Detailed index | PARTIALLY_CURRENT | Working index | Mixed | Navigation only | UPDATE |
| `RESEARCH/RESEARCH_VISION.md` | Program vision | OVERCLAIMED | Historical vision | Level 1–3 | Not evidence | REMOVE_FROM_PAPER_PATH |
| `RESEARCH/CORE_CONCEPT_MAP.md` | Concept synthesis map | OVERCLAIMED | Historical synthesis | Level 1–3 | Background only | ARCHIVE |
| `RESEARCH/FOUNDATION/STATE_TRANSITION_ORIENTATION_FRAMEWORK_V0_1.md` | Typed representation and transition framework | PAPER_CORE_CANDIDATE, CURRENT | Non-normative formal proposal aligned with freeze | Level 1–2 | Strongest paper core | KEEP |
| `RESEARCH/FOUNDATION/README.md` | Foundation navigation | PARTIALLY_CURRENT | Mixed | Level 1–3 | Navigation after pruning | UPDATE |
| `RESEARCH/FOUNDATION/STRUCTURAL_AXIOMS.md` | Earlier axiomatic framing | OVERCLAIMED | Pre-freeze formalization | Level 2–3 | Historical comparison only | ARCHIVE |
| `RESEARCH/FOUNDATION/STRUCTURAL_THEOREMS.md` | Claimed structural theorems | OVERCLAIMED | Pre-freeze, not established as theorems | Level 3 | Exclude | REMOVE_FROM_PAPER_PATH |
| `RESEARCH/VALIDATION/README.md` | Validation archive boundaries | USEFUL_SUPPORT | Bounded evidence overview | Level 1–2 | Strong limitations source | KEEP |
| `RESEARCH/VALIDATION/VALIDATION_SUMMARY.md` | Older validation synthesis | OVERCLAIMED | Superseded summary | Level 2–3 | Do not cite as global validation | SUPERSEDE |
| `RESEARCH/NEXAH_TRANSLATIONS/00_core_claims_short.md` | Short cross-domain claims | OVERCLAIMED | Interpretive | Level 3 | Exclude | REMOVE_FROM_PAPER_PATH |
| `RESEARCH/THEORETICAL_EXTENSIONS/README.md` | Exploratory extension boundary | HISTORICAL | Explicitly non-proved | Level 0–1 | Archive only | ARCHIVE |

## Current paper-core candidates

1. The frozen typed framework and its representation/change/provenance boundaries.
2. RID-01 as a machine-readable formalization artifact, without runtime claims.
3. WNI-01 as a formal case study showing exact preservation conditions and fail-closed controls.
4. NOS-01 as a synthesis/destruction control showing that the core survives removal of metaphor.
5. TITAN-01 and IEEE Geometry as secondary transfer/control cases.
6. EXP-00 positive, negative, and non-citable outcomes as evidence-discipline examples.

The existing paper draft, universal transition claims, symbolic translations, and visual atlas are not paper-core candidates.

