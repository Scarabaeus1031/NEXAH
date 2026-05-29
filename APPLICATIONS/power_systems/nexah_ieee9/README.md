# ⚡ NEXAH — IEEE9 Stability Field Navigation

![Status](https://img.shields.io/badge/status-active-success)
![Field Model](https://img.shields.io/badge/field-model-blue)
![Control](https://img.shields.io/badge/control-prototype-orange)

---

## 🧭 Abstract

NEXAH introduces a new paradigm for power system stability:

> **Stability is not a binary condition — it is a navigable field.**

Instead of detecting collapse after it occurs, NEXAH:

- reconstructs the **underlying stability geometry**
- defines a **continuous risk field**
- enables **closed-loop control along safe trajectories**

👉 Control becomes **trajectory-aware and geometry-informed**

---

## 🔁 System Pipeline

```text
Simulation → Features → Manifold → Field → Risk → Policy → Control → Navigation
```

---

## 📂 Repository Structure

```text
nexah_ieee9/
├── analysis/          # prediction and risk estimation
├── context/           # channel and field detection
├── control/           # intervention mechanisms
├── controller/        # controller evolution (v6–v11)
├── data/              # IEEE9 test system definitions
├── decision/          # policies and state decisions
├── features/          # coherence and structural metrics
├── overlay/           # manifold and residual analysis
├── simulation/        # power-flow solvers
├── visualization/     # plotting and animations
├── results/           # experimental outputs

├── main.py            # main NEXAH pipeline entry point
├── nexah_solver_v2.py # closed-loop physics coupling layer

├── architecture.md
├── architecture_v12.md
├── nexah_controller_evolution.md
├── results_summary.md
└── run_log.md
```

---

## 📚 Core Components
```
| Component | Purpose |
|------------|----------|
| main.py | end-to-end NEXAH pipeline execution |
| nexah_solver_v2.py | closed-loop physics-aware solver |
| architecture.md | NEXAH IEEE9 field-navigation architecture |
| architecture_v12.md | multi-agent navigation architecture |
| nexah_controller_evolution.md | controller evolution history |
| results_summary.md | experimental findings |
| run_log.md | development history |
```

---

## 🔬 Research Progression

The IEEE9 system represents the first complete NEXAH development chain:

```text
Detection
    ↓
Prediction
    ↓
Adaptive Control
    ↓
Field Extraction
    ↓
Geometry Analysis
    ↓
Navigation
```

The repository therefore contains both:

- reproducible controller implementations
- experimental navigation research
- architecture evolution documents
- complete development history

```
The IEEE9 system serves as the conceptual precursor to the larger IEEE57 X-Ray Pipeline.
```
---

## 🧭 Version Map (Controller Evolution)

| Version | Status | Description |
|--------|--------|------------|
| v6 | ✅ public | stable closed-loop control (reproducible) |
| v7–v9 | 🧪 experimental | dynamical system behavior |
| v10–v11 | 🧪 internal | field geometry & early navigation |

👉 **v6 is the current reproducible reference**  
👉 later versions represent ongoing development toward full navigation

---

# 📊 Field Reconstruction

## 🔹 Voltage Collapse

![Voltage Collapse](results/run_20260412_223816/plot.png)

Collapse is not abrupt — it follows a **continuous trajectory in state space**.

---

## 🔹 Risk Field

![Risk](results/run_20260412_223816/risk.png)

- low values → stable region  
- sharp increase → collapse boundary  

👉 Instability appears as a **structured region**, not a threshold.

---

## 🔹 Flow Field (Core Object)

![Flow Field](results/controller_runs/controller_replay_20260413_214411/field_overlay.png)

System trajectories follow structured flow paths:

- motion is directional  
- instability follows field geometry  
- stable regions form naturally  

👉 This field is the **central object of NEXAH**

---

# 🔁 Closed-Loop Control

## 🔹 Controller Response

![Control](results/run_20260412_223816/intervention.png)

Control reshapes trajectories instead of reacting to states:

- early intervention  
- smooth response  
- geometry-aware behavior  

---

## 🔹 Time Evolution

![Timeseries](results/controller_runs/controller_replay_20260413_214411/timeseries.png)

👉 The controller becomes part of the **system dynamics**

---

# 🌀 Dynamical System Behavior (v7 → v9)

NEXAH evolves from static control to a **coupled dynamical system**.

### Phase System (v9)

![λ vs ψ](results/controller_v9/output_v9_phase_lambda_psi.png)

![Risk vs Distance](results/controller_v9/output_v9_phase_risk_distance.png)

👉 System + controller form a **joint phase-space process**

---

# 🔥 Field Geometry (Experimental)

## 🔹 Stability Surface

![Surface](results/controller_v10/output_v10_plot.png)

## 🔹 Field Structure

![Field Structure](results/controller_v10_3/output_v10_3_phase_risk_distance.png)

---

## 🧠 Emergent Structure

Two regimes appear:

- 🟡 Transition region (~λ ≈ 0.8) → deformation  
- 🔴 Instability region (~λ ≈ 1.25+) → nonlinear amplification  

---

## ⚠️ Critical Insight

> Instability is NOT triggered by first curvature  
> but by **nonlinear amplification of the field**

---

# 🎬 Field Navigation (Prototype)

![Navigation GIF](results/visuals/nexah_navigation_v11.gif)

Controller behavior:

- approaches critical boundary  
- stabilizes before collapse  
- operates near optimal utilization  

⚠️ Based on internal experimental versions (v7–v11)

---

# 🧭 Navigation Result

λ = 0.600 → 0.7717  

→ operation close to critical boundary **without collapse**

---

# 🧠 System Interpretation

The system operates as:

> a trajectory evolving within a structured stability field

where:

- field = extracted from system physics  
- geometry = defines stability structure  
- control = trajectory shaping within the field  

---

# 🚀 Run (Public Version)

```bash
PYTHONPATH=. python APPLICATIONS/power_systems/nexah_ieee9/controller/nexah_closed_loop_ieee9_v6.py
```

---

# 🔥 Key Results

The IEEE9 project demonstrated that a power system can be:

- mapped into a stability field
- analyzed geometrically
- controlled through trajectory shaping
- navigated relative to structural boundaries

---

# 🧭 Development Status

| Layer | Status |
|---------|---------|
| Detection | ✅ |
| Prediction | ✅ |
| Adaptive Control | ✅ |
| Closed Loop Control | ✅ |
| Field Extraction | ✅ |
| Geometry Analysis | ✅ |
| Navigation Prototype | ✅ |
| Multi-Agent Architecture | 🧪 |
| Real Grid Deployment | ⚙️ |

---

# 🚀 Position within NEXAH

IEEE9 represents the foundational NEXAH research platform.

Key concepts first developed here:

- stability fields
- risk geometry
- field navigation
- trajectory-aware control
- multi-agent navigation concepts

Many of these ideas were later extended and tested at larger scale in the IEEE57 X-Ray Pipeline.
```
