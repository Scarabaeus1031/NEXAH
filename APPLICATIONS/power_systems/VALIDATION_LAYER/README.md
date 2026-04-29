# ⚡ NEXAH — Validation Layer (Golden Line)

---

# 🧭 Objective

Establish a **minimal, clear, and fully reproducible validation** of the NEXAH framework  
against classical power system stability analysis.

The goal is not to validate the full system, but to demonstrate:

> **NEXAH provides earlier or structurally richer insight than classical methods**

---

# 🎯 Core Question

Can NEXAH detect or represent instability **earlier or more structurally** than:

- voltage threshold methods  
- derivative-based indicators (`dV/dt`)  

---

# 🧪 Validation Strategy

We construct a **controlled comparison** between:

## Classical View

- voltage magnitude `V(t)`  
- threshold-based collapse definition  
- derivative signal `dV/dt`  

## NEXAH View

- reconstructed state:

```text
x(t) = (V(t), dV/dt, d²V/dt²)
```

- trajectory geometry  
- structural deviation  
- curvature-based dynamics  

---

# 🧱 Minimal Setup

## System

- IEEE test case (recommended: IEEE14)  
- synthetic baseline scenarios:
  - smooth  
  - nonlinear  
  - noisy  

## Data

Input:

```text
V(t)
```

Derived:

```text
dV/dt, d²V/dt²
```

---

# 🔁 Pipeline

```text
Simulation
    ↓
Time Series (V(t))
    ↓
Feature Extraction
    ↓
State Reconstruction
    ↓
Curvature Signal
    ↓
Event Extraction
    ↓
Shape Representation
    ↓
Geometry & Motion Analysis
```

---

# 📊 Detection Definitions

## Collapse (Reference)

```text
t_collapse = first t where V(t) < threshold
```

---

## Classical Detection

```text
t_classical = first t where dV/dt < dv_threshold
```

---

## NEXAH Detection (Core Layer)

State:

```text
x(t) = (V, dV/dt, d²V/dt²)
```

Curvature:

```text
κ(t) = || d²x/dt² ||
```

Detection:

```text
t_nexah = first sustained increase in curvature
```

---

# 📈 Golden Metric

```text
Lead Time = t_collapse - t_detection
```

All time values are measured in **simulation steps**.

---

# 🔷 Extended Structural Interpretation

Validation reveals that:

```text
NEXAH is not a signal detector.
```

Instead, it operates as:

```text
signal → event → shape → geometry → motion
```

---

## Event Layer

- curvature peaks define **events**  
- events are structured objects, not scalar values  

---

## Shape Layer

Each event is represented as:

```text
normalized curvature profile
```

---

## Shape Space

Shapes are embedded via PCA:

```text
shape → vector → low-dimensional geometry
```

This reveals:

- clusters (regimes)  
- separations  
- transition regions  

---

## Motion Layer (Critical)

Events evolve over time:

```text
they move through shape space
```

This enables:

- trajectory reconstruction  
- motion-based detection  
- early instability signals  

---

# 🔬 Experimental Evaluation

---

## 3.1 Experimental Setup

We evaluate NEXAH on both synthetic and real-world scenarios.

### Synthetic Scenarios

We construct three controlled time-series regimes:

- **smooth** → gradual decay  
- **nonlinear** → accelerated transition  
- **noisy** → stochastic perturbations  

These scenarios test robustness under increasing complexity.

---

### Real System

- IEEE14 test case  
- load increase (collapse sweep)  

This provides a physically grounded validation environment.

---

## 3.2 Evaluation Protocol

For each scenario, we compute:

- classical detection time:
```text
t_classical
```

- NEXAH detection time:
```text
t_nexah
```

- collapse time:
```text
t_collapse
```

We evaluate:

```text
Lead Time = t_collapse - t_detection
```

All results are measured in **simulation steps**.

---

## 3.3 Synthetic Results

### Observation

- smooth systems → strong early warning  
- nonlinear systems → clear structural signal  
- noisy systems → degraded but detectable signal  

---

### Interpretation

```text
NEXAH detects structural deviations before threshold-based methods,
but sensitivity decreases under high noise.
```

---

## 3.4 Shape Space Analysis

Event shapes embedded into PCA space reveal:

- distinct clusters corresponding to regimes  
- overlapping transition regions  
- continuous trajectories between states  

---

### Key Result

```text
events are not independent
they form trajectories in shape space
```

---

## 3.5 Motion-Based Detection

Using motion metrics:

- angle (directional change)  
- speed (displacement)  

we observe:

- angle spikes → early signal  
- speed increase → later confirmation  

---

### Interpretation

```text
instability emerges as directional change in trajectory motion
```

---

## 3.6 Statistical Validation

Across repeated runs:

- detection rate ≈ 86%  
- mean lead time ≈ 11.6 steps  

---

### Interpretation

```text
the method is statistically reliable
but not fully robust under noise
```

---

## 3.7 IEEE14 — Stable Regime

Even without collapse, the system exhibits:

- structured trajectories  
- bounded motion regions  
- persistent geometric patterns  

---

### Insight

```text
stable systems are not static
they exhibit structured motion
```

---

## 3.8 IEEE14 — Collapse Sweep

Under increasing load:

- collapse occurs at ~60–75 steps  
- NEXAH detects deviations at ~20–25 steps  

---

### Key Result

```text
Lead time ≈ 40–50 simulation steps
```

---

## 3.9 Geometric Interpretation

Observed trajectory behavior:

- loop deformation  
- directional drift  
- escape from stable region  

---

### Final Model

```text
stable motion
→ geometric drift
→ directional escape
→ collapse
```

---

## 3.10 Visual Evidence

Key figures (see `figure_map.md`):

- Fig. 3 → trajectory structure  
- Fig. 7 → angle-based early signal  
- Fig. 13 → collapse with early warning  

---

### Interpretation

```text
geometric drift is consistently observable
before collapse becomes visible in V(t)
```

---

# 📊 Outputs

## Core (`validation_skeleton.py`)

- multi-scenario comparison  
- event extraction  
- shape overlay  
- PCA shape space  
- clustering  
- trajectory visualization  

---

## Experiments

Located in:

```text
experiments/
```

Includes:

- shape geometry  
- motion metrics (speed, angle)  
- statistical validation  
- IEEE bridge  
- collapse sweep  

📄 Full log:

```text
experiments_log.md
```

---

## Reports

Located in:

```text
reports/
```

- `validation_report_v1.md` → structure  
- `validation_report_v2.md` → dynamics  
- `validated_findings.md` → consolidated results  
- `nexah_paper_core.md` → formal paper draft  

---

# ⚖️ Validation Criteria

Validation is successful if NEXAH provides:

- earlier detection  
OR  
- richer structural insight  

AND / OR:

- trajectory-level information  
- observable transition dynamics  

---

# ⚠️ Constraints

- limited system set (currently IEEE14)  
- curvature sensitivity to noise  
- PCA as a reduced representation  

---

# 🧠 Interpretation

Classical methods:

```text
Instability = threshold crossing
```

NEXAH:

```text
Instability = geometric drift in trajectory space
```

---

# 🌀 Golden Line

> If trajectory-based signals derived from V(t)  
> detect instability earlier or reveal structural precursors,  
> then the geometric interpretation is justified.

---

# 🚀 Usage

### Core validation

```bash
python scripts/validation_skeleton.py
```

### Experiments

```bash
python experiments/run_XXX_*.py
```

---

# 📌 Status

- minimal validation: ✅  
- structural interpretation: ✅  
- motion-based detection: ✅  
- statistical validation: ✅  
- real-system validation (IEEE): 🟡 ongoing  

---

# 🧭 Philosophy

This is not about proving a complete theory.

It is about establishing:

> a **small, clear, and reproducible structural advantage**

---

# ⚡ NEXAH

```text
signal → structure → geometry → motion
```

---

# 🔗 See Also

```text
scripts/validation_skeleton.py
experiments/
experiments_log.md
reports/validated_findings.md
reports/nexah_paper_core.md
```
