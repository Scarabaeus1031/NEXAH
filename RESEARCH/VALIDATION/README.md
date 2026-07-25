# 🔬 NEXAH — Validation Portal

This directory contains empirical experiments used to test whether structural
patterns observed in NEXAH persist across runs, perturbations,
representations, and dynamical systems.

It is an evidence archive under active development. It is not an independent
verification of a finalized theory.

![NEXAH Validation Summary](./visuals/nexah_validation_summary_visual.png)

---

## 🧭 Start Here

| Goal | Entry point |
|---|---|
| Understand the validation program | Continue with this page |
| Read the complete empirical report | **[VALIDATION_SUMMARY.md](VALIDATION_SUMMARY.md)** |
| Inspect baseline Lorenz experiments | **[lorenz/](lorenz/)** |
| Compare systems | **[cross_validation/](cross_validation/)** |
| Inspect phase, control, and causality experiments | **[causality/](causality/)** |
| Explore Kuramoto field structure | **[systems/kuramoto/README.md](systems/kuramoto/README.md)** |
| Explore the fractal extension | **[fractal_tests/README.md](fractal_tests/README.md)** |
| Inspect JANUS transport geometry | **[JANUS Operator](../CORE_CONCEPTS/JANUS_OPERATOR/)** |

Recommended evidence path:

```text
Lorenz reproducibility
→ noise and partition sensitivity
→ cross-system comparison
→ continuous field reconstruction
→ phase and control experiments
→ experimental extensions
```

---

## 🧠 What Validation Means Here

NEXAH uses three status levels:

| Status | Meaning |
|---|---|
| **Empirical** | Supported by concrete repository experiments and generated results |
| **Experimental** | Reproduced within a limited setup but not sufficiently generalized |
| **Theoretical** | Interpretation or proposed mechanism requiring further evidence |

“Empirical” does not mean independently replicated, universally proven, or
production validated. Results should be evaluated together with their local
method, data, parameters, and limitations.

---

## 🧪 Core Validation Questions

The current experiments investigate:

1. Does reconstructed structure persist across repeated runs?
2. How sensitive is it to noise and perturbation?
3. Does it depend on a particular partition or representation?
4. Which patterns recur across different dynamical systems?
5. Where do transitions concentrate in continuous field geometry?
6. How are phase mismatch and directional control associated with transitions?
7. Which observations remain exploratory extensions rather than core evidence?

---

## 📊 Evidence Matrix

| Research question | Systems | Primary evidence | Current status |
|---|---|---|---|
| Multi-run persistence | Lorenz | [`run_lorenz_multirun_validation.py`](lorenz/run_lorenz_multirun_validation.py) | Empirical |
| Noise robustness | Lorenz | [`run_lorenz_noise_validation.py`](lorenz/run_lorenz_noise_validation.py), [`run_transition_noise_validation.py`](lorenz/run_transition_noise_validation.py) | Empirical |
| Partition sensitivity | Lorenz | [`run_multi_partition_invariance_test.py`](lorenz/run_multi_partition_invariance_test.py), DBSCAN sweeps | Empirical within tested methods |
| Cross-system similarity | Lorenz, Rössler, Duffing | [`cross_validation/`](cross_validation/) | Experimental cross-system evidence |
| Continuous transition fields | Lorenz | [`run_transition_field_estimation.py`](lorenz/run_transition_field_estimation.py), [`run_instability_field_estimation.py`](lorenz/run_instability_field_estimation.py) | Empirical reconstruction |
| Phase mismatch and control response | Primarily Lorenz-derived experiments | [`causality/`](causality/) | Empirical association; causal interpretation remains limited |
| Synchronization-field organization | Kuramoto and comparison systems | [`systems/kuramoto/`](systems/kuramoto/) | Experimental system-level evidence |
| Parameter-driven transition geometry | Mandelbrot / Julia | [`fractal_tests/`](fractal_tests/) | Experimental extension |
| Recursive directional transport | Multiple exploratory systems | [`JANUS_OPERATOR/`](../CORE_CONCEPTS/JANUS_OPERATOR/) | Experimental / semi-formal |
| Prime-residue transition specificity | First 20,000 primes | [`prime_modular_residue_comparison_01/`](prime_modular_residue_comparison_01/) | Bounded held-out validation |
| Wheel and product reference spaces | Prime residues, CRT products, wheel lifts | [`wheel_product_reference_spaces_01/`](wheel_product_reference_spaces_01/) | Bounded held-out and exact-arithmetic validation |

This matrix identifies where evidence lives; it does not assign universal
validity to the associated interpretation.

---

## 🗂️ Directory Structure

| Area | Role |
|---|---|
| **[lorenz/](lorenz/)** | Baseline reproducibility, noise, partition, and field experiments |
| **[rossler/](rossler/)** | Rössler and Duffing comparison material |
| **[duffing/](duffing/)** | Generated Duffing validation results |
| **[cross_validation/](cross_validation/)** | Executable cross-system comparisons |
| **[cross_system/](cross_system/)** | Selected cross-system visual results |
| **[causality/](causality/)** | Control, mismatch, intervention, and phase experiments |
| **[systems/](systems/)** | Larger system-specific validation programs |
| **[fractal/](fractal/)** | Conceptual fractal-transition documents |
| **[fractal_tests/](fractal_tests/)** | Executable parameter-driven fractal experiments |
| **[prime_modular_residue_comparison_01/](prime_modular_residue_comparison_01/)** | Held-out Mod-7/Mod-17/control comparison and 7-to-17 bridge test |
| **[wheel_product_reference_spaces_01/](wheel_product_reference_spaces_01/)** | Mod-6 baseline, Mod-42 CRT product, wheel/lift and boundary tests |
| **[visuals/](visuals/)** | Validation overview visuals |

The distinction between `fractal/` and `fractal_tests/` is intentional:
`fractal/` documents the interpretation, while `fractal_tests/` contains the
experiment suite and findings.

---

## 🔥 Current Working Observation

Several investigated systems show an association between transition behavior
and mismatch in local phase or directional organization:

$$M(t)=|\omega(t)-\hat{\omega}(t)|$$

The current working interpretation is:

```text
instability
→ transition potential

phase or directional mismatch
→ possible activation signal
```

The repository contains evidence that mismatch can be more informative than
instability magnitude alone in specific experiments. A general causal law has
not been established.

---

## 🌊 Continuous and System-Level Structure

Field-oriented experiments reconstruct:

- density and instability fields
- transition concentration regions
- directional flow organization
- synchronization and phase structure
- candidate navigation corridors

The Kuramoto program is the largest system-level validation branch in this
directory:

- **[Kuramoto overview](systems/kuramoto/README.md)**
- **[Kuramoto core findings](systems/kuramoto/CORE_FINDINGS.md)**
- **[Field-layer findings](systems/kuramoto/FINDINGS_FIELD_LAYER_KURAMOTO.md)**

These results provide detailed internal evidence, but their broader
generalization remains under investigation.

---

## 🎮 Control and Causality

The **[causality/](causality/)** experiments explore whether localized or
directional interventions alter observed transition behavior.

Representative experiments include:

- [`run_gate_minimal_intervention.py`](causality/run_gate_minimal_intervention.py)
- [`run_gate_resonance_scan_multirun.py`](causality/run_gate_resonance_scan_multirun.py)
- [`run_control_mismatch_analysis.py`](causality/run_control_mismatch_analysis.py)
- [`run_phase_aligned_control.py`](causality/run_phase_aligned_control.py)
- [`run_closed_loop_control_test.py`](causality/run_closed_loop_control_test.py)

Observed response to intervention supports further causal investigation. It
does not yet establish a generalized control law or production-ready control
method.

---

## 🌀 Experimental Extensions

Two major extensions sit beyond the baseline validation stack:

### Fractal transition experiments

The **[fractal test suite](fractal_tests/README.md)** studies parameter-driven
transitions in Mandelbrot and Julia systems. Its own findings explicitly
distinguish empirical transition regions from unresolved interpretation.

### JANUS transport geometry

The **[JANUS Operator](../CORE_CONCEPTS/JANUS_OPERATOR/)** investigates
forward/backward directional coherence, apertures, shell crossings, and
recursive transport organization. This remains experimental and semi-formal.

---

## ♻️ Reproducibility Status

The repository provides many scripts, parameters, generated figures, and saved
arrays. However:

- there is no single runner for the full validation archive
- environments are not yet pinned per historical experiment
- not every script has been re-executed against the current repository state
- generated outputs do not substitute for independent replication
- real-world validation remains limited

Use the individual experiment scripts as evidence trails. The
**[NEXAH Demonstrator](../../PROTO_CORE/NEXAH_DEMONSTRATOR/)** is the preferred
verified entry for a complete runnable pipeline.

---

## ⚠️ Current Limitations

The validation archive does not yet provide:

- independent replication
- a universal transition law
- complete statistical treatment across all claims
- a unified causal model
- comprehensive real-world datasets
- production-grade control guarantees
- a repository-wide reproducibility command

Accordingly, claims should be phrased as observations from investigated
systems, not as universal properties of complex dynamics.

---

## 📄 Detailed Report

The full historical evidence narrative, figures, metrics, and experiment-level
discussion remain available in:

**[VALIDATION_SUMMARY.md](VALIDATION_SUMMARY.md)**

That document is intentionally comprehensive. This README serves only as the
current navigation and status layer.

---

## 🔗 Related Entry Points

- **[Research portal](../README.md)**
- **[Research index](../RESEARCH_INDEX.md)**
- **[Core concept map](../CORE_CONCEPT_MAP.md)**
- **[NEXAH Demonstrator](../../PROTO_CORE/NEXAH_DEMONSTRATOR/)**
- **[Power Systems validation](../../APPLICATIONS/power_systems/)**

---

**NEXAH Validation Portal**

Reproducibility · Robustness · Cross-System Evidence · Experimental Extensions
