# 🚀 START HERE — Reproduce Stability Field Results

This module is fully executable and reproduces all results shown in the README.

It implements a complete pipeline for:

→ collapse prediction  
→ manifold extraction  
→ rift detection  
→ stability geometry  

---

## 🧭 Minimal Workflow

`Dataset → Manifold → Rift → Distance → Topology`

---

## ⚙️ 1. Build dataset (all IEEE systems)

Run from project root:

`python -m APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.experiments.run_ieee_unified_dataset_v43`

→ generates normalized dataset for IEEE 9 / 14 / 30  

---

## 📈 2. Fit collapse manifold

`python -m APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.experiments.run_ieee_manifold_fit_v43`

→ derives empirical law:

d²c ≈ a · c^p · (dc)^q  

---

## 🧩 3. Extract collapse boundary (rift)

`python -m APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.experiments.run_ieee_rift_extraction_v51`

→ identifies residual ≈ 0 region  
→ defines collapse boundary  

---

## 📏 4. Compute stability distance + collapse geometry

`python -m APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.experiments.run_ieee_stability_distance_v52`

→ computes:

- distance to rift  
- collapse strength  
- residual–distance structure  

---

## 🌊 5. (Optional) Flow + residual dynamics

`python -m APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.experiments.run_ieee_vector_field_v47`

`python -m APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.experiments.run_ieee_residual_flow_v49`

→ reveals:

- flow structure  
- instability propagation  

---

## 📦 Output

All results are written to:

`APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/`

Includes:

- CSV datasets  
- manifold fits  
- rift boundaries  
- stability maps  
- collapse geometry  
- visualizations (PNG)

---

## 🧠 What You Should See

After running:

- systems converge to a **collapse manifold**
- collapse occurs along a **rift (boundary)**
- stability is measurable as **distance to structure**
- collapse forms **topological regions (triangle / polygon / extremes)**

---

## 🔬 Next Step

👉 For theory, interpretation, and full visual analysis:

→ see [README.md](README.md)

---

## Core Idea

> Stability is not a condition.  
>  
> It is alignment with structure.  
>  
> Collapse begins when that alignment is lost.
