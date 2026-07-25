# NEXAH Evidence Atlas

## Status and authority

This page is a **non-authoritative navigation layer** over 28 bounded claim
units reviewed in Discovery Atlas Review 01.

The Atlas:

- links to evidence where it is owned;
- preserves status, scope, reproducibility, and limits;
- gives negative results, limitations, and blocked chains equal visibility;
- does not define Architecture, OLS, Research, validation, application, or
  Library authority;
- does not copy result payloads or promote a completed experiment into a
  stronger finding.

Every linked source remains authoritative within its own responsibility. The
reviewed source register is the
[Discovery Candidate Register](../../ARCHITECTURE/reviews/discovery_atlas_01/DISCOVERY_CANDIDATE_REGISTER.md);
status terms follow the
[Discovery Taxonomy](../../ARCHITECTURE/reviews/discovery_atlas_01/DISCOVERY_TAXONOMY.md).

## How to read an entry

| Field | Meaning |
|---|---|
| ID | Stable identifier assigned by Discovery Atlas Review 01 |
| Claim | Reviewed bounded wording; not an expanded interpretation |
| Status | Controlled evidence status from the Discovery Taxonomy |
| Scope | The domain in which the wording applies |
| Source | Authoritative owning source, or the audit record when primary evidence is unavailable |
| Replay | Current reproducibility and declared dependencies |
| Limit | What the entry does not establish |

## 1. Exact constructions

| ID | Claim | Status | Scope | Source | Replay | Limit |
|---|---|---|---|---|---|---|
| E-013 | Every prime greater than 3 lies in residue class 1 or 5 modulo 6. | `MATHEMATICALLY_EXACT` | Integer arithmetic | Wheel/product [SPEC](../../RESEARCH/VALIDATION/wheel_product_reference_spaces_01/SPEC.md) and [RESULTS](../../RESEARCH/VALIDATION/wheel_product_reference_spaces_01/RESULTS.md) | Exact and offline; integer arithmetic | Says nothing by itself about transition predictability or stability |
| E-015 | The mapping between `Z/42Z` and `Z/6Z × Z/7Z` is exact and invertible. | `MATHEMATICALLY_EXACT` | Finite coordinate systems | CRT construction in the wheel/product [SPEC](../../RESEARCH/VALIDATION/wheel_product_reference_spaces_01/SPEC.md) | Exact, fully replayable offline | Coordinate equivalence does not establish independence of transition dynamics |

## 2. Architectural validations

| ID | Claim | Status | Scope | Source | Replay | Limit |
|---|---|---|---|---|---|---|
| E-001 | OLS 1.0.0 is the first complete canonical OLS publication and its declared release package has integrity manifests and independent release review. | `ARCHITECTURALLY_VALIDATED` | OLS semantic release | OLS [Publication Summary](../../ORIENTATION_LANGUAGE/SPECIFICATION/RELEASES/OLS-RELEASE-1.0.0/PUBLICATION_SUMMARY.md) and [independent review](../../ORIENTATION_LANGUAGE/SPECIFICATION/RELEASES/OLS-RELEASE-1.0.0/REVIEW/INDEPENDENT_RELEASE_REVIEW.md) | Fully inspectable offline; Git and SHA-256 | Does not validate every implementation or domain |
| E-002 | NEXAH currently separates Research, OLS, Implementations, Applications, Library, and Editorial Operating System responsibilities rather than assigning them one authority. | `ARCHITECTURALLY_VALIDATED` | Repository Architecture | Maintained [Architecture README](../../ARCHITECTURE/README.md) subordinate to the Constitution | Fully inspectable offline | Diagrams do not prove an integrated runtime |
| E-024 | The Living Library curates Works and reader journeys while code, evidence, and specifications retain authority in their responsible repository areas. | `ARCHITECTURALLY_VALIDATED` | Repository editorial architecture | Maintained [Library README](../../LIBRARY/README.md) | Documentary and inspectable offline | Does not validate the claims inside a Work |

## 3. Experimental findings

| ID | Claim | Status | Scope | Source | Replay | Limit |
|---|---|---|---|---|---|---|
| E-009 | Under the frozen prime comparison protocol, tested modular residue sequences contain held-out predictive transition information beyond their training-only baselines. | `EXPERIMENTALLY_SUPPORTED` | Declared sequences, folds, and metrics | Prime comparison [SPEC](../../RESEARCH/VALIDATION/prime_modular_residue_comparison_01/SPEC.md) and [RESULTS](../../RESEARCH/VALIDATION/prime_modular_residue_comparison_01/RESULTS.md) | Fully replayable offline with repository Python dependencies | Sequence description, not continuous dynamics or physical law |
| E-010 | Mod 23, not Mod 17, had the highest held-out gain among the declared tested moduli under both prime policies. | `EXPERIMENTALLY_SUPPORTED` | One frozen experiment | Prime comparison [RESULTS](../../RESEARCH/VALIDATION/prime_modular_residue_comparison_01/RESULTS.md) | Fully replayable offline | Does not mean optimal outside the tested set, data, metric, or policy |
| E-014 | Mod-6 residue transitions carried positive held-out information relative to the frozen null under both declared prime policies. | `EXPERIMENTALLY_SUPPORTED` | Specific sequence and metric | Wheel/product [RESULTS](../../RESEARCH/VALIDATION/wheel_product_reference_spaces_01/RESULTS.md) | Fully replayable offline | Distinct from the exact residue-class fact and not evidence of stabilization |
| E-016 | On the frozen dataset, independently factorized Mod-6 and Mod-7 transition models did not reproduce the joint Mod-42 transition kernel. | `EXPERIMENTALLY_SUPPORTED` | One dataset and model comparison | Wheel/product [RESULTS](../../RESEARCH/VALIDATION/wheel_product_reference_spaces_01/RESULTS.md) | Fully replayable offline | Does not prove universal coupling or non-factorization under every model |
| E-017 | Despite equal Euler totients, Mod 280 and Mod 360 differed under the frozen normalized-gain metric. | `EXPERIMENTALLY_SUPPORTED` | One metric and prime dataset | Wheel/product [RESULTS](../../RESEARCH/VALIDATION/wheel_product_reference_spaces_01/RESULTS.md) | Fully replayable offline | Does not rank either modulus universally or infer geometric stability |
| E-020 | In the Demonstrator experiments, high gate-field values neither guaranteed transitions nor captured many transitions, supporting an instability-field rather than event-detector interpretation. | `EXPERIMENTALLY_SUPPORTED` | Demonstrator behavior | [Demonstrator README](../../PROTO_CORE/NEXAH_DEMONSTRATOR/README.md) | Replayable with repository dependencies | Not a universal theorem about dynamical systems |
| E-022 | The frozen IEEE-9 development / IEEE-14 evaluation method ran without evaluation retuning and preserved its declared provenance, insufficiency, and claim boundaries. | `EXPERIMENTALLY_SUPPORTED` | Benchmark application | IEEE protocol [README](../../APPLICATIONS/power_systems/ieee_geometry_v1/README.md) and [validation test](../../tests/validation/test_ieee_geometry_v1.py) | Replayable with locked repository dependencies | Benchmark result, not operational-grid validity |

## 4. Negative and inconclusive results

| ID | Claim | Status | Scope | Source | Replay | Limit |
|---|---|---|---|---|---|---|
| E-003 | Publication integrity and semantic authority of OLS 1.0 do not by themselves establish conformance of every implementation or validity in any application domain. | `DOCUMENTED_LIMITATION` | OLS semantic release | OLS [Publication Summary](../../ORIENTATION_LANGUAGE/SPECIFICATION/RELEASES/OLS-RELEASE-1.0.0/PUBLICATION_SUMMARY.md) and [Architecture boundary](../../ARCHITECTURE/README.md) | Documentary | Does not evaluate a particular implementation |
| E-006 | The reviewed editorial corpus does not establish a provisional cross-domain grammar or candidate formal system. | `NOT_SUPPORTED` | Independent editorial review | [Candidate Grammar Assessment](../../APPLICATIONS/orientation_translation/studies/editorial_grammar_of_orientation_01/CANDIDATE_GRAMMAR_ASSESSMENT.md) | Replayable by source inspection | Does not prove that no future grammar can exist |
| E-008 | Current Orientation Translation material does not establish that its practices improve reader orientation, navigation, or learning. | `INCONCLUSIVE` | Application research program | [Program Reflection disposition](../../APPLICATIONS/orientation_translation/reviews/program_reflection_01/FINAL_DISPOSITION.md) | No reader experiment available | Production and inspectability are not causal reader effect |
| E-011 | The frozen specificity rule did not support a uniquely privileged predictive status for Mod 17. | `NOT_SUPPORTED` | One frozen experiment | Prime comparison [RESULTS](../../RESEARCH/VALIDATION/prime_modular_residue_comparison_01/RESULTS.md) | Fully replayable offline | Does not show Mod 17 is uninteresting under every question |
| E-012 | The predefined mapping `(7*r7+8) mod 17` did not outperform the training-only majority baseline on held-out residues. | `NOT_SUPPORTED` | Fixed mapping and dataset | Prime comparison [RESULTS](../../RESEARCH/VALIDATION/prime_modular_residue_comparison_01/RESULTS.md) | Fully replayable offline | Rejects this mapping and test, not every possible relation between the spaces |
| E-018 | The predefined 31/32/33 boundary did not reach the top-5% local curvature threshold. | `NOT_SUPPORTED` | One predeclared anomaly test | Wheel/product [RESULTS](../../RESEARCH/VALIDATION/wheel_product_reference_spaces_01/RESULTS.md) | Fully replayable offline | Does not prove that the numbers have no other relevant relation |
| E-023 | Pandapower non-convergence and sampled geometric change in the frozen IEEE protocol do not establish certified voltage stability, causal prediction, operational generalization, or control advice. | `NOT_SUPPORTED` | Benchmark application | Prohibited claims in the IEEE [manifest](../../APPLICATIONS/power_systems/ieee_geometry_v1/case_manifest.json) and [README](../../APPLICATIONS/power_systems/ieee_geometry_v1/README.md) | Replayable benchmark; real observed input absent | Independent observed outcome remains open |

## 5. Open hypotheses and blocked chains

| ID | Claim | Status | Scope | Source | Replay | Limit |
|---|---|---|---|---|---|---|
| E-004 | The Foundation document named Structural Theorems contains testable, semi-formal propositions and explicitly does not establish mathematical proof, universality, or physical fundamentality. | `OPEN_HYPOTHESIS` | Historical and cross-system Research | [Structural Theorems](../../RESEARCH/FOUNDATION/structural_theorems.md) | Partially reproducible; heterogeneous sources | No formal proof or universal validation is supplied |
| E-019 | No current frozen prime bundle establishes dynamical damping, recovery, attraction, error correction, or stabilization by Mod 17. | `OPEN_HYPOTHESIS` | Prime Research | Prime comparison [interpretation boundary](../../RESEARCH/VALIDATION/prime_modular_residue_comparison_01/RESULTS.md) | No adequate dynamical test exists | Current experiments test sequence description and coordinate reconstruction, not dynamics |
| E-025 | No POA experiment, freeze report, or synthesis document requested by this audit was found in the current checkout or any inspected Git history. | `BLOCKED` | Repository evidence chain | [Evidence Chain Audit](../../ARCHITECTURE/reviews/discovery_atlas_01/EVIDENCE_CHAIN_AUDIT.md); no primary source | Repository search is reproducible | Absence here is not evidence that the work never existed elsewhere |
| E-026 | No NTO formal specification, reference-space review, or dependency graph was found in the current checkout or inspected Git history. | `BLOCKED` | Proposed reference-space review | [Evidence Chain Audit](../../ARCHITECTURE/reviews/discovery_atlas_01/EVIDENCE_CHAIN_AUDIT.md); no primary source | Repository search is reproducible | Conversation or visuals cannot substitute for a repository artifact |
| E-027 | No controlled DERIS/HYDRA evidence bundle matching the requested intake was found in the current checkout or inspected Git history. | `BLOCKED` | Research intake | [Evidence Chain Audit](../../ARCHITECTURE/reviews/discovery_atlas_01/EVIDENCE_CHAIN_AUDIT.md); no primary source | Blocked by missing repository materials | Incidental names or external images are not a controlled evidence bundle |

## 6. Application and editorial findings

| ID | Claim | Status | Scope | Source | Replay | Limit |
|---|---|---|---|---|---|---|
| E-005 | Thirteen distinguishable editorial operations recur across the reviewed Orientation Translation corpus. | `PARTIALLY_SUPPORTED` | Independent editorial review | [Candidate Grammar Assessment](../../APPLICATIONS/orientation_translation/studies/editorial_grammar_of_orientation_01/CANDIDATE_GRAMMAR_ASSESSMENT.md) | Inspectable corpus; not independently reproduced | Shared authorship, variable order, inconsistent visual semantics, and absent reader tests limit independence |
| E-007 | Across the reviewed program, source records, evidence boundaries, traceability, and bounded publication form a recurring source-bounded inspectability practice. | `PARTIALLY_SUPPORTED` | Application research program | [Program Reflection disposition](../../APPLICATIONS/orientation_translation/reviews/program_reflection_01/FINAL_DISPOSITION.md) | Inspectable; not independently reproduced | Comparison method, analyst independence, domain generality, and scalability remain unestablished |

## 7. Representations and implementation limitations

| ID | Claim | Status | Scope | Source | Replay | Limit |
|---|---|---|---|---|---|---|
| E-021 | Requesting six historical radial sheets currently yields seven observed labels because the maximum radius enters an additional digitization bin. | `DOCUMENTED_LIMITATION` | Demonstrator implementation | [Demonstrator replay notes](../../PROTO_CORE/NEXAH_DEMONSTRATOR/README.md) | Replayable with repository dependencies | Not an externally validated regime model |
| E-028 | Polar, wheel, architecture, and application figures can represent source records but do not independently establish common mathematics, capability, or physical truth. | `DOCUMENTED_LIMITATION` | Visual representation | Wheel [interpretation boundary](../../RESEARCH/VALIDATION/wheel_product_reference_spaces_01/RESULTS.md), [Architecture warning](../../ARCHITECTURE/README.md), and IEEE [authority statement](../../APPLICATIONS/power_systems/ieee_geometry_v1/README.md) | Varies by visual; source record required | A reproducibly generated figure can still be useful without becoming evidence authority |

## Status inventory

| Status | Count |
|---|---:|
| `MATHEMATICALLY_EXACT` | 2 |
| `ARCHITECTURALLY_VALIDATED` | 3 |
| `EXPERIMENTALLY_SUPPORTED` | 7 |
| `PARTIALLY_SUPPORTED` | 2 |
| `NOT_SUPPORTED` | 5 |
| `INCONCLUSIVE` | 1 |
| `OPEN_HYPOTHESIS` | 2 |
| `DOCUMENTED_LIMITATION` | 3 |
| `BLOCKED` | 3 |
| **Total** | **28** |

## Maintenance boundary

An Atlas entry may change only when its owning source changes or a new review
changes the bounded status. Adding a link does not validate a claim. Removing a
blocked status requires a repository-addressable primary source and a separate
evidence review. No automated promotion, ranking, claim inference, or
machine-readable registry is part of this first version.
