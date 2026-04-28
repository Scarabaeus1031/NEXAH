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

---

# 🔷 Extended Structural Interpretation (NEW)

Validation revealed:

```text
NEXAH is NOT a signal detector.
```

It operates as:

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

Shapes embedded via PCA:

```text
shape → vector → low-dimensional geometry
```

Reveals:

- clusters  
- regime separation  
- transition regions  

---

## Motion Layer (CRITICAL)

Events are not independent:

```text
they move through shape space
```

This enables:

- trajectory reconstruction  
- motion-based detection  
- early instability signals  

---

# 📊 Outputs

## Core (validation_skeleton.py)

- multi-scenario comparison  
- event extraction  
- shape overlay  
- shape space (PCA)  
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
- motion metrics (speed / angle)  
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

- `validation_report_v1.md` → shape & structure  
- `validation_report_v2.md` → motion & dynamics  
- `validated_findings.md` → consolidated results  

---

# ⚖️ Validation Criteria

Validation is successful if NEXAH shows:

- earlier detection  
OR  
- richer structural insight  

AND / OR:

- trajectory-level information  
- transition dynamics  

---

# ⚠️ Constraints

- limited system set (currently IEEE14)  
- curvature sensitive to noise  
- PCA is a reduced representation  

---

# 🧠 Interpretation

Classical:

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
- real-world validation (IEEE): 🟡 ongoing  

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

```text
scripts/validation_skeleton.py
experiments/
experiments_log.md
reports/validated_findings.md
```
