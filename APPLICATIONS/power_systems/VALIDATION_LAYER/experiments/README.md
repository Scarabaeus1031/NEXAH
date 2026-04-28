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
