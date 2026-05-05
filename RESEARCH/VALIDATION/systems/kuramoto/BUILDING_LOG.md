# NEXAH FIELD_LAYER — Building Log  
## Field Projection Experiments: Lorenz → Rössler → Halvorsen → Kuramoto

Status: **Experimental phase completed / core finding stabilized**

---

## 1. Goal

This experiment series tests whether a common FIELD_LAYER representation can extract comparable transition structure from different dynamical systems.

Systems explored:

- Lorenz
- Rössler
- Halvorsen
- Kuramoto oscillator network

Core pipeline:

```text
dynamics
→ PCA field projection
→ phase coordinate θ
→ phase drift Δθ
→ regime classification
→ Iota event detection
→ sweep / boundary extraction
```

No symbolic interpretation was used in the final analysis.  
Focus: **data, structure, measurability**.

---

## 2. Core Method

For each system, state trajectories are projected into a PCA-aligned field coordinate system:

```text
x → (alpha, beta, gamma)
```

Phase is defined in the transverse plane:

```text
θ = arctan2(gamma, beta)
```

The main observable is:

```text
Δθ = phase drift
```

Regimes:

```text
Theta : low drift / baseline
Tao   : positive organized drift
Dao   : negative organized drift
Iota  : high drift event
```

---

## 3. Early V3 Results

### Rössler V3

Key result:

```text
Iota ≈ 8.00 %
transition_rate ≈ 0.00309
iota_event_count = 139
```

![Rössler PCA Projection](runs/outputs/roessler_v3/roessler_v3_pca_projection.png)

![Rössler Phase Drift + Iota](runs/outputs/roessler_v3/roessler_v3_phase_drift_iota.png)

---

### Halvorsen V3

Key result:

```text
Iota ≈ 8.00 %
transition_rate ≈ 0.01056
iota_event_count = 475
```

![Halvorsen PCA Projection](runs/outputs/halvorsen_v3/halvorsen_v3_pca_projection.png)

![Halvorsen Phase Drift + Iota](runs/outputs/halvorsen_v3/halvorsen_v3_phase_drift_iota.png)

---

## 4. Kuramoto V3

Initial V3 result at K = 1.8:

```text
r_mean ≈ 0.8115
Iota ≈ 8.00 %
transition_rate ≈ 0.00456
```

![Kuramoto r(t)](runs/outputs/kuramoto_v3/K_1_800/kuramoto_v3_order_parameter.png)

![Kuramoto Slice Projection](runs/outputs/kuramoto_v3/K_1_800/kuramoto_v3_slice_r_dr_dt.png)

---

## 5. V3 Limitation

```text
iota_quantile = 0.92 → forced ~8%
```

Conclusion:

```text
V3 Iota was NOT a true physical measure.
```

---

## 6. V4 / V5 Correction

```text
Iota = mean(|Δθ|) + k * std(|Δθ|)
```

→ dynamic, data-driven threshold

![Kuramoto Phase Cloud](runs/outputs/kuramoto_v5/runs/K_1_800_1777941892/phase_cloud.png)

![Kuramoto Lyapunov](runs/outputs/kuramoto_v5/runs/K_1_800_1777941892/lyapunov.png)

---

## 7. V6 Master Sweep

Sweep:

```text
K ∈ [0.5, 3.0]
```

Key outputs:

- r_mean vs K  
- drift_std vs K  
- transition_rate vs K  
- Lyapunov vs K  

![Mean Synchronization vs K](runs/outputs/kuramoto_v6/master_runs/run_1777943097/sweep/r_mean_vs_K.png)

![Drift STD vs K](runs/outputs/kuramoto_v6/master_runs/run_1777943097/sweep/drift_std_vs_K.png)

![Transition Rate vs K](runs/outputs/kuramoto_v6/master_runs/run_1777943097/sweep/transition_rate_vs_K.png)

![Lyapunov vs K](runs/outputs/kuramoto_v6/master_runs/run_1777943097/sweep/lyapunov_vs_K.png)

---

## 8. Core Finding

```text
Synchronization and internal stability separate.
```

---

## 9. Phase Boundary (V7 / V8)

![Kuramoto Phase Diagram Final](runs/outputs/kuramoto_v8/final_1777944907/phase_diagram_final.png)

![Kuramoto System Overview](runs/outputs/kuramoto_v8/final_1777944907/system_overview.png)

---

## 10. Critical Points

```json
{
  "onset": 2.32,
  "max_drift": 2.55,
  "max_events": 2.77
}
```

---

## 11. Final Interpretation

```text
incoherent
→ synchronized
→ synchronized + drift-active
→ high-transition regime
```

---

## 12. Final Statement

```text
FIELD_LAYER reveals internal structure inside synchronization.
```

---

## 13. Scripts

```text
scripts/kuramoto_master_v6.py
scripts/kuramoto_phase_boundary_v8.py
```

---

## 14. Status

```text
Experimental phase completed
Core finding stabilized
```
