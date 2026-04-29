# ⚡ NEXAH — Experiments Log

---

# 🧭 Purpose

Track all validation experiments in a reproducible and structured way.

Each experiment documents:

- goal  
- script  
- key results  
- interpretation  

---

# 🧪 Experiment 001 — Shape Validation

**Script:**  
`run_001_shape_validation.py`

**Goal:**  
Validate event extraction and establish the shape representation concept.

**Key Results:**
- curvature events successfully extracted  
- normalized event shapes constructed  
- initial clustering visible  

**Insight:**
```text
Event shape encodes system dynamics.
```

---

# 🧪 Experiment 002 — Shape Geometry

**Script:**  
`run_002_shape_geometry.py`

**Goal:**  
Analyze geometric relationships between shape clusters.

**Key Results:**
- crossings between shape curves detected  
- area differences between clusters measured  
- end-state divergence identified  

**Insight:**
```text
Shape space is structured, not random.
```

---

# 🧪 Experiment 003 — Shape Dynamics

**Script:**  
`run_003_shape_dynamics.py`

**Goal:**  
Track how events evolve through shape space.

**Key Results:**
- trajectories between shapes identified  
- ordered vs chaotic motion patterns observed  

**Insight:**
```text
Instability is movement through shape space, not a single event.
```

---

# 🧪 Experiment 004 — Pre-Collapse Dynamics

**Script:**  
`run_004_pre_collapse_dynamics.py`

**Goal:**  
Compare system behavior before and after collapse.

**Key Results:**
- separation of regimes in shape space  
- structural shift occurs before collapse  

**Insight:**
```text
The system transitions structurally before observable collapse.
```

---

# 🧪 Experiment 005 — Motion Instability Metric

**Script:**  
`run_005_motion_instability_metric.py`

**Goal:**  
Define a motion-based instability indicator.

**Key Results:**
- angle spikes detected  
- instability quantified as directional change  

**Insight:**
```text
Directional change encodes instability.
```

---

# 🧪 Experiment 006 — Continuous Shape Flow

**Script:**  
`run_006_continuous_shape_flow.py`

**Goal:**  
Track continuous motion through shape space.

**Key Results:**
- speed and angle signals extracted  
- early warning occurs before collapse  
- angle reacts earlier than speed  

**Insight:**
```text
Instability manifests as deviation in motion dynamics.
```

---

# 🧪 Experiment 007 — Statistical Validation

**Script:**  
`run_007_statistical_validation.py`

**Goal:**  
Evaluate robustness across multiple runs.

**Key Results:**
- detection rate: 43 / 50 (~86%)  
- mean lead time: ~11.6 (synthetic baseline)  
- consistent detection behavior  

**Insight:**
```text
The method is statistically stable and reproducible.
```

---

# 🧪 Experiment 008 — IEEE Bridge

**Script:**  
`run_008_ieee_bridge.py`

**Goal:**  
Apply NEXAH to a real power system model (IEEE14).

**Key Results:**
- structured motion visible even in stable regime  
- speed and angle signals active without collapse  
- latent instability patterns present  

**Insight:**
```text
Power systems exhibit structured motion even before instability.
```

---

# 🧪 Experiment 009 — IEEE Collapse Sweep

**Script:**  
`run_009_ieee_collapse_sweep.py`

**Goal:**  
Evaluate early warning across varying load conditions.

**Key Results:**
- collapse occurs at high load rates  
- NEXAH warning appears significantly earlier  
- lead time: ~40–50 time units  

**Insight:**
```text
Geometric drift precedes voltage collapse.
```

---

# 🧠 Unified Insight

```text
signal → event → shape → geometry → motion → instability
```

---

# 📦 Outputs

Each experiment stores results in:

```text
outputs/run_YYYYMMDD_HHMMSS/
```

Typical contents:

- `results.json` → structured results  
- `results.csv` → tabular data  
- `overlay.png` → shape overlay  
- `shape_space.png` → PCA projection  
- `clusters.png` → clustering  

These outputs ensure:

```text
reproducibility
traceability
visual validation
```

---

# 🧭 Interpretation

Across all experiments, a consistent pattern emerges:

```text
Instability is not detected.

It is reconstructed as motion
through a structured geometric space.
```

---

# ⚡ NEXAH

```text
signal → structure → geometry → motion
```

---

# 🧪 PART C — Signal-Level Validation (Critical Layer)

These experiments test whether NEXAH provides **true early warning signals**,  
not just structural interpretation.

Focus:

```text
compare curvature (event), drift (motion), angle (direction), and shape-based signals
```

---

## 🧪 Experiment 010 — Detection Alignment

**Script:**  
`run_010_detection_analysis.py`

**Goal:**  
Compare NEXAH curvature detection vs classical dv/dt detection.

**Key Results:**
- NEXAH and classical detection occur nearly simultaneously  
- both detect **local instability events**  
- no significant lead advantage  

**Insight:**
```text
Curvature is a local event detector, not a global early warning signal.
```

---

## 🧪 Experiment 011 — Drift Signal

**Script:**  
`run_011_drift_signal.py`

**Goal:**  
Test drift (dv/dt) as a continuous early warning signal.

**Key Results:**
- drift detection occurs before collapse  
- lead time: ~2.2 simulation steps  

**Insight:**
```text
Drift captures global system motion and provides weak early warning.
```

---

## 🧪 Experiment 012 — Angle Signal

**Script:**  
`run_012_angle_signal.py`

**Goal:**  
Test directional change (angle) as early instability indicator.

**Key Results:**
- angle signal reacts very early  
- lead time: ~24 simulation steps  
- strong sensitivity to local fluctuations  

**Insight:**
```text
Angle is highly sensitive and can produce very early signals,
but may reflect local geometric fluctuations rather than global instability.
```

---

## 🧪 Experiment 013 — Combined Signal Analysis

**Script:**  
`run_013_combined_signal.py`

**Goal:**  
Compare all signals in a unified timeline.

**Key Results:**
- curvature (κ) detects earliest local event (~t ≈ 1)  
- drift and angle detect near pre-collapse (~t ≈ 22–23)  
- collapse occurs at ~t ≈ 25  

**Insight:**
```text
Different signals capture different aspects of instability:

- κ → local event onset
- drift → global motion
- angle → directional change
```

---

## 🧪 Experiment 014 — Shape Drift Signal (NEW)

**Script:**  
`run_014_shape_drift_signal.py`

**Goal:**  
Test whether **shape-space motion** provides a true global early warning signal.

**Method:**
- sliding window over curvature  
- convert windows → shapes  
- project into shape space (PCA)  
- compute distance to stable region  

**Key Result (to be evaluated):**
- distance(t) forms a continuous signal  
- potential early drift before collapse  

**Insight (hypothesis):**
```text
Global instability may appear as a continuous drift in shape space,
not as discrete events.
```

---

# 🧠 Critical Interpretation

These experiments reveal a hierarchy:

```text
κ(t)       → detects local events
angle(t)   → detects directional instability
drift(t)   → detects global motion
shape drift→ potential global structural signal
```

---

# ⚠️ Important Result

```text
No single signal fully captures instability.
```

Instead:

```text
Instability emerges across multiple geometric layers.
```

---

# 🧭 Updated Understanding

Before:

```text
instability = detected by one signal
```

Now:

```text
instability = multi-scale geometric process
```

---

# ⚡ NEXAH (Refined)

```text
signal → event → shape → geometry → motion → drift → instability
```



