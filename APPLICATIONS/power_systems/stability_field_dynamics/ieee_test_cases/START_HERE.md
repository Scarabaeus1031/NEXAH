## 🚀 Quick Start — Reproduce Results

This module is fully executable and reproducible.

### 1. Run core experiments

From the project root:

`python -m APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.experiments.run_ieee_unified_dataset_v43`

→ builds unified dataset for all IEEE systems  

---

### 2. Fit collapse manifold

`python -m APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.experiments.run_ieee_manifold_fit_v43`

→ derives empirical manifold equation  

---

### 3. Extract collapse boundary (rift)

`python -m APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.experiments.run_ieee_rift_extraction_v51`

→ identifies residual ≈ 0 boundary  

---

### 4. Compute stability distance + collapse geometry

`python -m APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.experiments.run_ieee_stability_distance_v52`

→ generates distance maps and collapse topology  

---

### 5. Optional — flow + residual analysis

`python -m APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.experiments.run_ieee_vector_field_v47`

`python -m APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.experiments.run_ieee_residual_flow_v49`

---

## Output

All results are written to:

`APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/`

Includes:

- CSV datasets  
- manifold fits  
- rift boundaries  
- stability maps  
- visualizations (PNG)

---

## Minimal Workflow

`Dataset → Manifold → Rift → Distance → Topology`

This sequence reproduces the full collapse analysis pipeline.
