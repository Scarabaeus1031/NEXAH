# ⚡ NEXAH — A Geometric Framework for Dynamical Systems

> NEXAH is a computational framework that reveals structure, transitions, and stability directly from system dynamics.

> Complex systems are not random.  
> They evolve within **structured fields that constrain motion, transitions, and outcomes**.

---

![Off-Manifold Flow](APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/ieee118_v69_off_manifold_flow.png)

This visualization shows a trajectory from a real IEEE power grid model.

NEXAH reconstructs the local **flow field** around the system state.

What becomes visible:

- directional structure  
- transition channels  
- stability constraints  

→ the system does not move freely  
→ it is **guided by an underlying field geometry**

---

🧪 Reproduce this visualization:

    python APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/analysis/run_ieee_off_manifold_flow_v69.py

---

# 🧠 What NEXAH does

NEXAH transforms time-series system data into a **geometric representation**:

- states → field  
- time evolution → trajectories  
- events → regime transitions  

Instead of detecting isolated failures, NEXAH identifies:

> how systems **move within structured dynamical landscapes**  
> and how **stability constrains possible transitions**

---

# 🔥 Core Principle

```text
dynamics → structure → field → regimes → stability → navigation
```

---

# ⚡ Key Result — Power Systems (IEEE)

NEXAH has been tested on real IEEE grid models (118 → 9241 buses).

Result:

> Voltage collapse can be detected **~43.9 seconds earlier**  
> than classical methods — consistently across system sizes.

---

![NEXAH Mic Drop](APPLICATIONS/power_systems/stability_field_dynamics/iee_core_geometry/ieee_scaling/NEXAH_MicDrop_IEEE300_Final.png)
*Note: The “Mic Drop” label reflects an early internal milestone.  
It is not a scientific claim, but marks a transition from intuition to measurable structure.*

Interpretation:

- classical methods detect **state failure**  
- NEXAH detects **structural transition**

---

# 🧪 Minimal Demo — Structure inside Chaos

Run:

    python -m nexah.run_nexah_demo

---

![NEXAH Demo](outputs/demo/nexah_lorenz_transitions.png)

---

### Interpretation

The highlighted points mark **structural transitions** in the system.

They are not random.

They emerge from the **geometry of the dynamical field**:

- trajectories follow structure  
- transitions occur at specific regions  
- the system reveals where change happens  

---

> NEXAH does not detect events.  
>  
> It reveals the structure that produces them.  
>  
> It does not detect collapse.  
> It detects the structure that leads to it.

---

### 📊 Results (Lorenz Demo)

Across repeated runs:

- peak count remains stable (~45–55 per run)  
- peaks cluster in specific regions  
- transition patterns are reproducible  

Example:

- Max risk: 1.000  
- Mean risk: 0.025  
- Peak count: 50  

---

> The signal is not noise.  
> It is a stable structural feature of the system dynamics.

---

### 🔬 Stability Insight

- stability forms a continuous gradient  
- boundaries are **weakly stable regions**  
- no branching decisions occur  

> The system contains gates, but no decisions.

→ motion is constrained  
→ transitions are structured  
→ outcomes are determined by geometry  

---

## ⚡ IEEE Demo — Early Collapse Detection

Run:

    python run_ieee_demo.py

---

![IEEE Demo](outputs/demo/nexah_ieee_collapse.png)

---

Result:

- detection: t ≈ 248  
- collapse: t ≈ 700  
- lead time: **~450 steps**

→ transition visible in structure long before failure

---

# 🧪 Validation — Structure Under Noise & Across Systems

A central question:

> Is the detected structure real — or a noise artifact?

---

## 1. Synthetic Noise Robustness

    python run_noise_robustness_demo.py

- structural peaks remain aligned  
- match ratio ≈ **1.00**

---

## 2. Multi-Run Stability

    python run_noise_robustness_multirun.py

- 50 runs → identical results  
- mean match ratio: **1.000 ± 0.000**

---

## 3. Noise Stress Test

    python run_noise_robustness_stress_test.py

- structure persists under increasing noise  
- defines operational limits  

---

## 4. Real System Robustness (IEEE)

    python run_ieee_noise_robustness.py

- gradient correlation ≈ **0.69**  
- curvature correlation ≈ **0.61**

→ global structure remains stable  
→ local transitions partially degrade  

---

## 5. Cross-System Validation

    python run_lorenz_vs_ieee_noise_robustness.py

Results:

- Lorenz (oscillatory):
  - raw: low correlation  
  - smoothed: **0.895 → structure recovered**

- IEEE (drift system):
  - raw: **0.55 → stable trend**
  - smoothed: **0.78 → improved clarity**

---

## 🧠 Key Insight

Structure exists at multiple scales:

- high-frequency → noise-sensitive  
- low-frequency → robust  
- smoothing reveals latent structure  

---

## 🔥 Conclusion

Across all experiments:

- structure persists under noise  
- structure is reproducible  
- structure generalizes across systems  

> NEXAH does not depend on clean data.  
> It reveals the **underlying structure of the system itself**.

---

# 🧭 System Architecture

```text
Dynamics  
→ Discovery Engine  
→ Field Layer (geometry + stability)  
→ Navigator  
```

---

## 🔬 Discovery Engine
Extracts structure from raw dynamics.

## 🌊 Field Layer
Builds continuous representations of:

- flow  
- geometry  
- stability  

## 🧭 Navigator
Operates on structure:

- transition detection  
- regime tracking  
- trajectory control  

---

# 🌀 From Chaos to Structure

![Lorenz Chaos](DISCOVERY_ENGINE/outputs/lorenz_core_v4.png)

![Manifold](DISCOVERY_ENGINE/outputs/lorenz_v8_manifold.png)

![State Graph](DISCOVERY_ENGINE/outputs/v15_state_machine.png)

---

# ⚡ What NEXAH enables

- transition detection  
- geometric interpretation  
- early-warning signals  
- system navigation  

---

# 🧠 Current State

### ✔ Working

- structure extraction  
- regime detection  
- early transition signals  

---

### ⚠️ Limitations

- no formal proof yet  
- system-dependent performance  
- ongoing validation  

---

# 💡 Core Insight

> Stability is not a value.  
> It is a **region in a structured field**

---

# 🌀 NEXAH

From dynamics → structure  
From structure → geometry  
From geometry → regimes  
From regimes → navigation  

---

**Thomas K. R. Hofmann · 2026**
