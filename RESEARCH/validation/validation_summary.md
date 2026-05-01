# 🔬 NEXAH — Validation Summary (Lorenz System)

**System:** Lorenz  
**Phase:** Initial Validation Series  
**Status:** Active (multi-run + noise + transition validation)

---

# 🧪 1. Multi-Run Validation

**Script:** `run_lorenz_multirun_validation.py`  
**Runs:** 10  

## Results

- Mean endpoint distance: **9.7892**  
- Std deviation: **5.9301**  
- Attractor stability: **MEDIUM**

## Visual Evidence

![Trajectory Overlay](./validation/lorenz/results/trajectory_overlay.png)  
![Endpoint Distribution](validation/lorenz/results/endpoint_distribution.png)

## Interpretation

- Trajectories diverge (expected for chaotic systems)  
- Endpoints remain bounded within attractor region  
- Global structure is preserved across runs  

---

# 🌫️ 2. Noise Robustness (Trajectory Level)

**Script:** `run_lorenz_noise_validation.py`  
**Runs:** 10  
**Noise level:** 1.0  

## Results

**Clean:**
- Mean distance: **9.7892**
- Std: **5.9301**

**Noisy:**
- Mean distance: **10.4864**
- Std: **4.9895**

## Visual Evidence

![Endpoint Comparison](validation/lorenz/results/noise_endpoint_comparison.png)  
![Clean vs Noisy Trajectories](validation/lorenz/results/noise_trajectory_comparison.png)

## Interpretation

- Noise shifts endpoints slightly  
- No structural collapse observed  
- Attractor geometry remains stable  

---

# 🔁 3. Transition Stability under Noise

**Script:** `run_transition_noise_validation.py`  
**Runs:** 10  
**Noise level:** 1.0  

## Results

- Mean transition difference: **0.0008**

## Visual Evidence

![Transition Matrices](validation/lorenz/results/transition_noise_comparison.png)

## Interpretation

- Clean vs noisy matrices visually similar  
- Differences are small and localized  
- Transition structure remains intact  

---

# 🧭 4. Transition Sensitivity (Grid Partition)

**Script:** `run_transition_sensitivity_map.py`  
**Runs:** 20  
**Noise level:** 1.0  

## Results

- Mean difference: **0.001060**  
- Mean noisy variance: **0.000022**

## Visual Evidence

![Sensitivity Map (Grid)](validation/lorenz/results/transition_sensitivity_map.png)

## Interpretation

- Transition probabilities are highly stable  
- Low global sensitivity  
- Local amplification in specific regions  

---

# 🧩 5. Transition Sensitivity (Real Partition)

**Script:** `run_transition_sensitivity_real_partition.py`  
**Runs:** 20  
**Noise level:** 1.0  
**Clusters:** 6  

## Results

- Mean difference: **0.004940**  
- Mean noisy variance: **0.000223**

## Visual Evidence

![Sensitivity Map (Real Partition)](validation/lorenz/results/transition_sensitivity_real_partition.png)

## Interpretation

- Higher sensitivity than grid partition  
- Real partitions introduce irregular boundaries  
- Increased local variance  

BUT:

structure remains stable across runs  

---

# 🧠 GLOBAL OBSERVATIONS

Across all tests:

- High variation at trajectory level (chaotic behavior)  
- Stable structure at geometric level  
- Transition dynamics are:
  - reproducible  
  - noise-robust  
  - structurally constrained  

---

# 🔑 CORE INSIGHT

Dynamics are unstable at the trajectory level  

BUT  

stable at the structural level  

---

# ✅ CONCLUSION

- Structure is **reproducible across runs**  
- Structure is **robust under noise**  
- Stability is **geometric, not point-based**  
- Transitions behave as **structured processes**, not random events  

---

# ⚠️ VALIDATION STATUS

Level: PRELIMINARY  
Confidence: MEDIUM (increasing)  

---

# 🔜 NEXT STEPS

- increase runs (30–50)  
- validate on additional systems  
- test control layer reproducibility  
- extend to IEEE system  

---

**NEXAH Validation Layer**  
Initial Lorenz Validation Series  
© Thomas K. R. Hofmann · 2026
