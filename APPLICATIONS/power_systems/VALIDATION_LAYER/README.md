# ⚡ NEXAH — Validation Layer (Golden Line)

---

# 🧭 Objective

Establish a **minimal, clear, and reproducible validation** of the NEXAH framework  
against classical power system stability analysis.

The goal is not to prove the full system, but to demonstrate:

> **NEXAH provides earlier or structurally richer insight than classical methods**

---

# 🎯 Core Question

Can NEXAH detect or represent instability **earlier or more structurally** than:

- voltage threshold methods  
- derivative-based indicators (dv/dt)  

---

# 🧪 Validation Strategy

We construct a **controlled comparison** between:

## Classical View

- voltage magnitude `V(t)`  
- threshold crossing (collapse definition)  
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
- synthetic baseline scenarios (smooth, nonlinear, noisy)  

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
Detection Comparison
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

| Method      | Lead Time |
|------------|----------|
| Classical   | Δt_classical |
| NEXAH       | Δt_nexah |

---

# 🔷 Extended Structural Interpretation (NEW)

Validation revealed that NEXAH does not operate as a simple signal detector.

Instead:

```text
signal → event → shape → geometry → motion
```

---

## Event Layer

- curvature peaks form **events**  
- events are not scalar → they have **shape**  

---

## Shape Layer

Each event becomes:

```text
normalized curvature profile
```

---

## Shape Space

Shapes can be embedded into a geometric space:

```text
shape → vector → PCA projection
```

This reveals:

- clusters (noise / structure)  
- separation of regimes  
- transition regions  

---

## Motion Layer (Experiments)

Events are not independent:

```text
they move through shape space
```

This enables:

- trajectory reconstruction  
- motion analysis  
- instability detection via geometry  

---

# 📊 Outputs

## Core (Skeleton)

- multi-scenario comparison table  
- event extraction  
- shape overlay  
- shape space (PCA)  
- clustering  

---

## Experiments

Located in:

```text
experiments/
```

Includes:

- shape geometry analysis  
- motion metrics (speed / angle)  
- statistical validation  
- IEEE system validation  
- collapse sweep  

---

## Reports

Located in:

```text
reports/
```

- `validation_report_v1.md` → shape & structure  
- `validation_report_v2.md` → dynamics & motion  
- `validated_findings.md` → final condensed insights  

---

# ⚖️ Validation Criteria

A successful validation shows:

- earlier detection OR  
- richer structural insight  

AND / OR:

- detection of trajectory-level behavior  
- identification of transition dynamics  

---

# ⚠️ Constraints

- limited number of systems (currently IEEE14)  
- curvature sensitive to noise  
- PCA is a reduced representation  

---

# 🧠 Interpretation

Classical methods:

```text
Instability = threshold crossing in V(t)
```

NEXAH:

```text
Instability = geometric deviation in trajectory space
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
- real-world validation (IEEE): 🟡 (in progress)  

---

# 🧭 Philosophy

This is not about proving a full theory.

It is about establishing:

> a **small, clear, and reproducible structural advantage**

---

# ⚡ NEXAH

```text
signal → structure → geometry → motion
```

---

# 🔗 See Also

- `scripts/validation_skeleton.py`  
- `experiments/`  
- `reports/validated_findings.md`  V(t)
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
Distance Signal
    ↓
Detection Comparison
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

## NEXAH Detection

State:

```text
x(t) = (V, dV/dt, d²V/dt²)
```

Stable reference:

```text
μ_stable = mean(x(t)) over early stable window
```

Distance:

```text
d(t) = || x(t) - μ_stable ||
```

Detection:

```text
t_nexah = first t where d(t) > mean(d) + 2·std(d)
```

---

# 📈 Golden Metric

```text
Lead Time = t_collapse - t_detection
```

| Method      | Lead Time |
|------------|----------|
| Classical   | Δt_classical |
| NEXAH       | Δt_nexah |

---

# 📊 Outputs

The validation produces:

## 1. Time Series Plot

- Voltage `V(t)`
- Collapse point
- Classical detection
- NEXAH detection  

---

## 2. NEXAH Signal Plot

- Distance `d(t)`
- Threshold + detection  

---

## 3. State Space Plot

- Projection: `V vs dV/dt`
- Trajectory evolution  

---

## 4. Golden Line (optional)

```text
time →
|---- classical ----|
|-------- NEXAH --------|
|------------- collapse -------------|
```

---

# ⚖️ Validation Criteria

A successful validation shows:

- NEXAH detects instability:
  - earlier OR  
  - more consistently  

AND / OR:

- NEXAH reveals:
  - structure not visible in scalar signals  

---

# ⚠️ Constraints

- single system  
- single scenario  
- fixed thresholds (no tuning)  
- fully reproducible  

---

# 🧠 Interpretation

Classical methods:

```text
Instability = threshold crossing in V(t)
```

NEXAH:

```text
Instability = trajectory deviation in reconstructed state space
```

---

# 🌀 Golden Line

> If trajectory-based signals derived from V(t)  
> detect instability earlier or reveal structural precursors,  
> then the geometric interpretation is justified.

---

# 🚀 Usage

```bash
python validation_skeleton.py
```

---

# 🧭 Philosophy

This is not about proving a full theory.

It is about establishing:

> a **small, clear, and reproducible advantage**

---

# 📌 Status

- minimal validation: ✅  
- scalable validation: ⏳  
- real-world validation: ⏳  

---

# ⚡ NEXAH

> From signal → to structure  
> From structure → to trajectory  
> From trajectory → to stability insight  
