# Discovery Candidate Register

Status: curated review register; not a new source of authority

The 28 entries below are claim units, not document listings. “Public” means
suitable for a future evidence atlas with the stated conservative wording.
Source files remain authoritative.

## Architecture, language, and reviewed editorial structure

### E-001 — OLS 1.0 canonical release

- **Claim:** OLS 1.0.0 is the first complete canonical OLS publication and its
  declared release package has integrity manifests and independent release
  review.
- **Status / scope / kind:** `ARCHITECTURALLY_VALIDATED`; OLS semantic release;
  proof.
- **Evidence / authority:** release specification and integrity manifests;
  [Publication Summary](../../../ORIENTATION_LANGUAGE/SPECIFICATION/RELEASES/OLS-RELEASE-1.0.0/PUBLICATION_SUMMARY.md#L1-L33).
- **Support / limits:** release tree, checksums, and
  [independent review](../../../ORIENTATION_LANGUAGE/SPECIFICATION/RELEASES/OLS-RELEASE-1.0.0/REVIEW/INDEPENDENT_RELEASE_REVIEW.md);
  authority is limited to the canonical documents and does not validate every
  implementation or domain.
- **Reproducibility / dependencies:** fully inspectable offline; Git and SHA-256.
- **Open question / public:** implementation conformance is separate; yes.

### E-002 — Repository authority separation

- **Claim:** NEXAH currently separates Research, OLS, Implementations,
  Applications, Library, and Editorial Operating System responsibilities rather
  than assigning them one authority.
- **Status / scope / kind:** `ARCHITECTURALLY_VALIDATED`; repository
  architecture; proof.
- **Evidence / authority:** maintained [Architecture README](../../README.md#L12-L28)
  subordinate to the Constitution.
- **Support / limits:** [repository-wide responsibility map](../../README.md#L64-L113);
  diagrams are informative and do not prove an integrated runtime.
- **Reproducibility / dependencies:** fully inspectable offline; governance and
  current architecture documents.
- **Open question / public:** maintenance consistency across subsystem indexes;
  yes.

### E-003 — OLS release is not general implementation conformance

- **Claim:** Publication integrity and semantic authority of OLS 1.0 do not by
  themselves establish conformance of every implementation or validity in any
  application domain.
- **Status / scope / kind:** `DOCUMENTED_LIMITATION`; OLS semantic release;
  limitation.
- **Evidence / authority:** [Publication Summary](../../../ORIENTATION_LANGUAGE/SPECIFICATION/RELEASES/OLS-RELEASE-1.0.0/PUBLICATION_SUMMARY.md#L27-L33)
  and [Architecture boundary](../../README.md#L25-L28).
- **Support / limits:** OLS conformance remains governed by its own normative
  suite; this entry does not evaluate a particular implementation.
- **Reproducibility / dependencies:** documentary; OLS release.
- **Open question / public:** which implementations have separate conformance
  records; yes.

### E-004 — Structural “theorems” remain semi-formal propositions

- **Claim:** The Foundation document named Structural Theorems contains
  testable, semi-formal propositions and explicitly does not establish
  mathematical proof, universality, or physical fundamentality.
- **Status / scope / kind:** `OPEN_HYPOTHESIS`; historical/cross-system research;
  hypothesis.
- **Evidence / authority:** [Structural Theorems](../../../RESEARCH/FOUNDATION/structural_theorems.md#L1-L43).
- **Support / limits:** repository experiments and visuals are cited locally;
  no formal proof or universal validation is supplied.
- **Reproducibility / dependencies:** partially reproducible; heterogeneous
  research sources.
- **Open question / public:** which propositions survive modern frozen tests;
  yes, only as open hypotheses.

### E-005 — Recurring editorial operation family

- **Claim:** Thirteen distinguishable editorial operations recur across the
  reviewed Orientation Translation corpus.
- **Status / scope / kind:** `PARTIALLY_SUPPORTED`; independent editorial
  review; finding.
- **Evidence / authority:** [Candidate Grammar Assessment](../../../APPLICATIONS/orientation_translation/studies/editorial_grammar_of_orientation_01/CANDIDATE_GRAMMAR_ASSESSMENT.md#L5-L26).
- **Support / limits:** corpus records and operation study; shared authorship,
  variable order, inconsistent visual semantics, and absent reader tests limit
  independence ([limits](../../../APPLICATIONS/orientation_translation/studies/editorial_grammar_of_orientation_01/CANDIDATE_GRAMMAR_ASSESSMENT.md#L28-L36)).
- **Reproducibility / dependencies:** inspectable corpus, not independently
  reproduced; Orientation Translation materials.
- **Open question / public:** independent editors and readers; yes with limits.

### E-006 — No cross-domain formal grammar established

- **Claim:** The reviewed editorial corpus does not establish a provisional
  cross-domain grammar or candidate formal system.
- **Status / scope / kind:** `NOT_SUPPORTED`; independent editorial review;
  negative result.
- **Evidence / authority:** [Candidate Grammar Assessment](../../../APPLICATIONS/orientation_translation/studies/editorial_grammar_of_orientation_01/CANDIDATE_GRAMMAR_ASSESSMENT.md#L5-L11).
- **Support / limits:** absence of mandatory syntax, stable relation semantics,
  parser, conformance target, independent reproduction, and measured reader
  behavior; this does not prove that no future grammar can exist.
- **Reproducibility / dependencies:** review replayable by source inspection;
  reviewed corpus.
- **Open question / public:** whether a new independent corpus changes the
  result; yes.

### E-007 — Orientation Translation has stable inspectability practices

- **Claim:** Across the reviewed program, source records, evidence boundaries,
  traceability, and bounded publication form a recurring source-bounded
  inspectability practice.
- **Status / scope / kind:** `PARTIALLY_SUPPORTED`; application research
  program; finding.
- **Evidence / authority:** [Program Reflection disposition](../../../APPLICATIONS/orientation_translation/reviews/program_reflection_01/FINAL_DISPOSITION.md#L3-L10).
- **Support / limits:** evidence register and reviewed cases; comparison method,
  cartography, analyst independence, domain generality, and scalability remain
  unestablished.
- **Reproducibility / dependencies:** inspectable, not independently reproduced;
  Orientation Translation corpus.
- **Open question / public:** independent reproduction; yes.

### E-008 — Reader effect remains inconclusive

- **Claim:** Current Orientation Translation material does not establish that
  its practices improve reader orientation, navigation, or learning.
- **Status / scope / kind:** `INCONCLUSIVE`; application research program;
  limitation.
- **Evidence / authority:** [Program Reflection disposition](../../../APPLICATIONS/orientation_translation/reviews/program_reflection_01/FINAL_DISPOSITION.md#L11-L18).
- **Support / limits:** internal artifacts demonstrate production and
  inspectability, not causal reader effect.
- **Reproducibility / dependencies:** no reader experiment available; future
  human study.
- **Open question / public:** measured reader outcomes; yes.

## Prime and wheel research

### E-009 — Bounded prime-residue sequential structure

- **Claim:** Under the frozen prime comparison protocol, tested modular residue
  sequences contain held-out predictive transition information beyond their
  training-only baselines.
- **Status / scope / kind:** `EXPERIMENTALLY_SUPPORTED`; specific sequence,
  folds, and metrics; finding.
- **Evidence / authority:** frozen [SPEC](../../../RESEARCH/VALIDATION/prime_modular_residue_comparison_01/SPEC.md)
  and [RESULTS](../../../RESEARCH/VALIDATION/prime_modular_residue_comparison_01/RESULTS.md#L13-L24).
- **Support / limits:** deterministic code, tests, CSV, JSON, checksums; this is
  sequence description, not continuous dynamics or physical law.
- **Reproducibility / dependencies:** fully replayable offline with repository
  Python dependencies.
- **Open question / public:** robustness to other sequence definitions and
  metrics; yes.

### E-010 — Mod 23 led the declared comparison

- **Claim:** Mod 23, not Mod 17, had the highest held-out gain among the declared
  tested moduli under both prime policies.
- **Status / scope / kind:** `EXPERIMENTALLY_SUPPORTED`; one frozen experiment;
  finding.
- **Evidence / authority:** [RESULTS](../../../RESEARCH/VALIDATION/prime_modular_residue_comparison_01/RESULTS.md#L13-L18).
- **Support / limits:** paired folds and machine summary; does not mean “optimal”
  outside the tested set, data, metric, or policy.
- **Reproducibility / dependencies:** fully replayable offline; bundle inputs
  and Python.
- **Open question / public:** out-of-range moduli and alternative metrics; yes.

### E-011 — Special Mod-17 predictive status rejected

- **Claim:** The frozen specificity rule did not support a uniquely privileged
  predictive status for Mod 17.
- **Status / scope / kind:** `NOT_SUPPORTED`; one frozen experiment; negative
  result.
- **Evidence / authority:** [decision and interpretation](../../../RESEARCH/VALIDATION/prime_modular_residue_comparison_01/RESULTS.md#L7-L11).
- **Support / limits:** Mod 17 did exceed Mod 7, but Mod 23 was higher; this does
  not show Mod 17 is uninteresting under every question.
- **Reproducibility / dependencies:** fully replayable offline; bundle.
- **Open question / public:** other predeclared Mod-17 properties; yes.

### E-012 — Fixed affine 7-to-17 bridge rejected

- **Claim:** The predefined mapping `(7*r7+8) mod 17` did not outperform the
  training-only majority baseline on held-out residues.
- **Status / scope / kind:** `NOT_SUPPORTED`; fixed mapping and dataset;
  negative result.
- **Evidence / authority:** [bridge result](../../../RESEARCH/VALIDATION/prime_modular_residue_comparison_01/RESULTS.md#L26-L37).
- **Support / limits:** CI spans zero under both policies; this rejects this
  mapping and test, not every possible relation between the spaces.
- **Reproducibility / dependencies:** fully replayable offline; bundle.
- **Open question / public:** none for this frozen claim; yes.

### E-013 — Mod-6 prime residue property

- **Claim:** Every prime greater than 3 lies in residue class 1 or 5 modulo 6.
- **Status / scope / kind:** `MATHEMATICALLY_EXACT`; integer arithmetic;
  construction.
- **Evidence / authority:** arithmetic definition in the wheel bundle
  [SPEC](../../../RESEARCH/VALIDATION/wheel_product_reference_spaces_01/SPEC.md)
  and exhaustive run check in [RESULTS](../../../RESEARCH/VALIDATION/wheel_product_reference_spaces_01/RESULTS.md#L16-L23).
- **Support / limits:** elementary divisibility argument; says nothing by itself
  about transition predictability or stability.
- **Reproducibility / dependencies:** exact and offline; integer arithmetic.
- **Open question / public:** none; yes.

### E-014 — Mod 6 carries held-out transition information

- **Claim:** Mod-6 residue transitions carried positive held-out information
  relative to the frozen null under both declared prime policies.
- **Status / scope / kind:** `EXPERIMENTALLY_SUPPORTED`; specific sequence and
  metric; finding.
- **Evidence / authority:** [RESULTS](../../../RESEARCH/VALIDATION/wheel_product_reference_spaces_01/RESULTS.md#L16-L23).
- **Support / limits:** deterministic folds and null test; distinct from the
  exact residue-class fact and not evidence of stabilization.
- **Reproducibility / dependencies:** fully replayable offline; bundle.
- **Open question / public:** other nulls and sequence regimes; yes.

### E-015 — CRT equivalence for 42, 6, and 7

- **Claim:** The mapping between `Z/42Z` and `Z/6Z × Z/7Z` is exact and
  invertible.
- **Status / scope / kind:** `MATHEMATICALLY_EXACT`; finite coordinate systems;
  construction.
- **Evidence / authority:** CRT construction and exhaustive round-trip in
  [SPEC](../../../RESEARCH/VALIDATION/wheel_product_reference_spaces_01/SPEC.md).
- **Support / limits:** machine-checked arithmetic inventory; coordinate
  equivalence does not establish independence of transition dynamics.
- **Reproducibility / dependencies:** exact, fully replayable offline; integer
  arithmetic.
- **Open question / public:** none; yes.

### E-016 — Independent Mod-6 × Mod-7 transition model failed

- **Claim:** On the frozen dataset, independently factorized Mod-6 and Mod-7
  transition models did not reproduce the joint Mod-42 transition kernel.
- **Status / scope / kind:** `EXPERIMENTALLY_SUPPORTED`; one dataset and model
  comparison; finding.
- **Evidence / authority:** [RESULTS](../../../RESEARCH/VALIDATION/wheel_product_reference_spaces_01/RESULTS.md#L25-L32).
- **Support / limits:** positive held-out joint advantage with paired CI; does
  not prove universal “coupling” or non-factorization under every model.
- **Reproducibility / dependencies:** fully replayable offline; bundle.
- **Open question / public:** alternative factorized models; yes.

### E-017 — Mod 280 and Mod 360 are empirically distinguishable

- **Claim:** Despite equal Euler totients, Mod 280 and Mod 360 differed under
  the frozen normalized-gain metric.
- **Status / scope / kind:** `EXPERIMENTALLY_SUPPORTED`; one metric and prime
  dataset; finding.
- **Evidence / authority:** [RESULTS](../../../RESEARCH/VALIDATION/wheel_product_reference_spaces_01/RESULTS.md#L34-L39).
- **Support / limits:** paired CI excludes zero; does not rank either modulus
  universally or infer geometric stability.
- **Reproducibility / dependencies:** fully replayable offline; bundle.
- **Open question / public:** which arithmetic factors explain the difference;
  yes.

### E-018 — Predefined 31/32/33 anomaly rejected

- **Claim:** The predefined 31/32/33 boundary did not reach the top-5% local
  curvature threshold.
- **Status / scope / kind:** `NOT_SUPPORTED`; one predeclared anomaly test;
  negative result.
- **Evidence / authority:** [RESULTS](../../../RESEARCH/VALIDATION/wheel_product_reference_spaces_01/RESULTS.md#L41-L45).
- **Support / limits:** observed percentile was 83.33%; not proof that the
  numbers have no other relevant relation.
- **Reproducibility / dependencies:** fully replayable offline; bundle.
- **Open question / public:** none for this frozen test; yes.

### E-019 — Mod-17 stabilization remains open

- **Claim:** No current frozen prime bundle establishes dynamical damping,
  recovery, attraction, error correction, or stabilization by Mod 17.
- **Status / scope / kind:** `OPEN_HYPOTHESIS`; prime research; hypothesis.
- **Evidence / authority:** [prime comparison interpretation boundary](../../../RESEARCH/VALIDATION/prime_modular_residue_comparison_01/RESULTS.md#L33-L39).
- **Support / limits:** current experiments test sequence description and
  coordinate reconstruction, not dynamics.
- **Reproducibility / dependencies:** no adequate test exists; requires a
  separately frozen dynamical experiment.
- **Open question / public:** whether any operational definition survives
  preregistration; yes as open.

## Implementation, applications, representation, and blocked chains

### E-020 — Demonstrator gate is not a transition detector

- **Claim:** In the Demonstrator experiments, high gate-field values neither
  guaranteed transitions nor captured many transitions, supporting an
  instability-field rather than event-detector interpretation.
- **Status / scope / kind:** `EXPERIMENTALLY_SUPPORTED`; Demonstrator behavior;
  finding.
- **Evidence / authority:** [Demonstrator README](../../../PROTO_CORE/NEXAH_DEMONSTRATOR/README.md#L150-L164).
- **Support / limits:** implemented deterministic example and ablations; not a
  universal theorem about dynamical systems.
- **Reproducibility / dependencies:** replayable with repository dependencies.
- **Open question / public:** quantitative evaluation across systems; yes.

### E-021 — Demonstrator sheet-label boundary

- **Claim:** Requesting six historical radial sheets currently yields seven
  observed labels because the maximum radius enters an additional digitization
  bin.
- **Status / scope / kind:** `DOCUMENTED_LIMITATION`; implementation-only
  behavior; limitation.
- **Evidence / authority:** [Demonstrator replay notes](../../../PROTO_CORE/NEXAH_DEMONSTRATOR/README.md#L289-L294).
- **Support / limits:** deterministic generator and tests; not an externally
  validated regime model.
- **Reproducibility / dependencies:** replayable with repository dependencies.
- **Open question / public:** whether a future version intentionally changes
  the boundary convention; yes.

### E-022 — Frozen IEEE Geometry V1 protocol passed its bounded gate

- **Claim:** The frozen IEEE-9 development / IEEE-14 evaluation method ran
  without evaluation retuning and preserved its declared provenance,
  insufficiency, and claim boundaries.
- **Status / scope / kind:** `EXPERIMENTALLY_SUPPORTED`; benchmark application;
  application result.
- **Evidence / authority:** [IEEE protocol README](../../../APPLICATIONS/power_systems/ieee_geometry_v1/README.md#L1-L22)
  and [validation test](../../../tests/validation/test_ieee_geometry_v1.py#L17-L76).
- **Support / limits:** manifest, canonical JSON, replay checks, and claim audit;
  solver byte streams may vary by platform, and this is not an operational-grid
  case.
- **Reproducibility / dependencies:** replayable with locked repository
  dependencies.
- **Open question / public:** timestamped independently observed outcome; yes.

### E-023 — IEEE benchmark does not establish a physical boundary

- **Claim:** Pandapower non-convergence and sampled geometric change in the
  frozen IEEE protocol do not establish certified voltage stability, causal
  prediction, operational generalization, or control advice.
- **Status / scope / kind:** `NOT_SUPPORTED`; benchmark application; negative
  result.
- **Evidence / authority:** prohibited claims in the
  [manifest](../../../APPLICATIONS/power_systems/ieee_geometry_v1/case_manifest.json#L109-L134).
- **Support / limits:** IEEE-14 had no sampled solver-boundary record and the
  bridge to observed evidence remains closed
  ([README](../../../APPLICATIONS/power_systems/ieee_geometry_v1/README.md#L165-L184)).
- **Reproducibility / dependencies:** replayable benchmark; real observed input
  absent.
- **Open question / public:** independent observed outcome; yes.

### E-024 — Library catalog and repository authority remain distinct

- **Claim:** The Living Library curates Works and reader journeys while code,
  evidence, and specifications retain authority in their responsible repository
  areas.
- **Status / scope / kind:** `ARCHITECTURALLY_VALIDATED`; repository editorial
  architecture; proof.
- **Evidence / authority:** maintained [Library README](../../../LIBRARY/README.md).
- **Support / limits:** Library status and registry records; this does not
  validate the claims inside a Work.
- **Reproducibility / dependencies:** documentary and inspectable offline.
- **Open question / public:** synchronization of catalog and canonical Works;
  yes.

### E-025 — POA sequence is not repository-addressable

- **Claim:** No POA experiment, freeze report, or synthesis document requested
  by this audit was found in the current checkout or any inspected Git history.
- **Status / scope / kind:** `BLOCKED`; repository evidence chain; limitation.
- **Evidence / authority:** repository-wide filename and content search plus
  `git log --all --name-only`; no primary source.
- **Support / limits:** absence in this repository is not evidence that the work
  never existed elsewhere.
- **Reproducibility / dependencies:** search reproducible locally; missing
  authoritative source.
- **Open question / public:** locate or restore the owning repository/revision;
  no public claim until resolved.

### E-026 — NTO reference-space review is not repository-addressable

- **Claim:** No NTO formal specification, reference-space review, or dependency
  graph was found in the current checkout or inspected Git history.
- **Status / scope / kind:** `BLOCKED`; proposed reference-space review;
  limitation.
- **Evidence / authority:** repository-wide filename and content search; no
  primary source.
- **Support / limits:** conversation or visuals cannot substitute for a
  repository artifact.
- **Reproducibility / dependencies:** search reproducible locally; missing
  source.
- **Open question / public:** identify authoritative source and evidence; no.

### E-027 — DERIS/HYDRA intake is not repository-addressable

- **Claim:** No controlled DERIS/HYDRA evidence bundle matching the requested
  intake was found in the current checkout or inspected Git history.
- **Status / scope / kind:** `BLOCKED`; research intake; limitation.
- **Evidence / authority:** repository-wide search; no primary evidence bundle.
- **Support / limits:** incidental use of “Hydra” or external images is not a
  substitute for specification, inputs, code, and results.
- **Reproducibility / dependencies:** blocked by missing repository materials.
- **Open question / public:** complete controlled intake and provenance; no.

### E-028 — Visuals are representations, not mathematical evidence

- **Claim:** Polar, wheel, architecture, and application figures can represent
  source records but do not independently establish common mathematics,
  capability, or physical truth.
- **Status / scope / kind:** `DOCUMENTED_LIMITATION`; visual representation;
  representation.
- **Evidence / authority:** wheel
  [interpretation boundary](../../../RESEARCH/VALIDATION/wheel_product_reference_spaces_01/RESULTS.md#L47-L56),
  Architecture visual warning ([source](../../README.md#L23-L34)), and IEEE
  authority statement ([source](../../../APPLICATIONS/power_systems/ieee_geometry_v1/README.md#L186-L194)).
- **Support / limits:** multiple responsible source statements; a particular
  visual may still be reproducibly generated and useful.
- **Reproducibility / dependencies:** varies by visual; source record required.
- **Open question / public:** attach source-evidence links consistently; yes.

## Status count

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
