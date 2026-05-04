# NEXAH – System Status Report (v0.7 Freeze)

## Overview

NEXAH is a minimal, interpretable framework for analyzing and navigating dynamical systems.

It transforms time series into discrete state systems and enables:

- structure extraction  
- transition modeling  
- regime detection  
- probabilistic navigation  
- intervention estimation  

The system is fully functional and validated on real-world data.

---

## Quick Start

### 1. Installation (once)

```bash
pip install -e .
```

---

### 2. Example Data

Create test data:

```bash
python - <<EOF
import numpy as np
np.savetxt("data.csv", np.sin(np.linspace(0,20,500)), delimiter=",")
EOF
```

---

### 3. Run Analysis

```bash
nexah analyze data.csv
```

Optional:

```bash
nexah analyze data.csv --clusters 5 --window 20
nexah analyze data.csv --out result.json
```

---

### 4. Compare Systems

```bash
nexah compare a.csv b.csv
```

---

### 5. Visualize Regimes

```bash
python plot_regimes.py
```

---

## Output Includes

- current_state  
- best_state  
- transitions  
- regime_zones  
- signature  

---

## Interpretation

- regime_zones → structural instability (important transitions)  
- stable_states → persistent regimes  
- transitions → system dynamics  

---

## Core API

```python
nexah.analyze(trajectory, target_state=None)
nexah.compare(trajectory_a, trajectory_b)
nexah.analyze_many(list_of_trajectories)
```

---

## Repository Structure

### Core Files

- `core.py` → main kernel (ALL core logic)  
- `cli.py` → command-line interface  
- `plot_regimes.py` → visualization tool  

---

## Core Functional Blocks

### 1. Preprocessing

- normalization (optional)  
- multi-dimensional support  

Functions:
- `_preprocess()`

---

### 2. Representation

- sliding window embedding  

Functions:
- `_embed()`

---

### 3. Structure Extraction

- clustering (KMeans)  
- transition matrix (Markov-like)  

Functions:
- `_compute_transitions()`

---

### 4. Stability Analysis

- stable states detection  
- escape difficulty  

Functions:
- `_detect_stable_states()`  
- `_escape_difficulty()`

---

### 5. Regime Detection

- regime shifts (label changes)  
- local instability score  
- regime aggregation (zones)  

Functions:
- `_detect_regime_shifts()`  
- `_instability_score()`  
- `_aggregate_regimes()`

---

### 6. Navigation

- shortest path (BFS)  
- probabilistic path (Monte Carlo)  

Functions:
- `_find_path_bfs()`  
- `_navigate_probabilistic()`

---

### 7. Intervention Layer

- path-based intervention cost  

Functions:
- `_minimal_intervention()`

---

### 8. Dynamics Estimation

Monte Carlo simulation:

- hit probability  
- expected steps  

Functions:
- `_estimate_transition_dynamics()`

---

### 9. Control Layer

- transition optimization (local perturbation)  

Functions:
- `_optimize_transition()`

---

### 10. State Scoring

- stability vs mobility heuristic  

Functions:
- `_score_states()`  
- `_best_state()`

---

### 11. System Signature (Fingerprint)

Each system produces:

- number of states  
- dominant state  
- occupancy distribution  
- escape difficulty  
- transition entropy  

Functions:
- `_state_signature()`  
- `_transition_entropy()`

---

### 12. System Comparison

- similarity metric  
- based on stability + entropy  

Function:
- `compare()`

---

### 13. Batch Processing

Function:
- `analyze_many()`

---

## CLI (v0.8 Ready)

Commands:

```bash
nexah analyze data.csv
nexah analyze data.csv --clusters 5 --window 20
nexah analyze data.csv --out result.json

nexah compare a.csv b.csv
```

---

## Visualization

### Regime Plot

File:
`plot_regimes.py`

Features:

- time series plotting  
- regime zone overlay  
- visual validation of system behavior  

---

## Validated Behavior (Empirical)

Tested on:

- synthetic signals (sin, cos)  
- noisy signals  
- structural shifts  
- BTC-USD real market data  

### Observed Results

- high state stability (~0.98 self-transition)  
- low transition entropy (structured dynamics)  
- regime zones align with:
  - trend changes  
  - volatility spikes  
  - structural transitions  

---

## System Capabilities

NEXAH enables:

### 1. Structure Extraction
Time series → discrete state system  

### 2. Dynamic Modeling
Transition probabilities between states  

### 3. Regime Detection
Identification of instability and transitions  

### 4. Navigation
Simulation of possible system paths  

### 5. Intervention Estimation
What needs to change to reach a target  

### 6. System Comparison
Compare different dynamical systems  

---

## Core Insight

NEXAH does NOT predict values.

It detects:

- stability  
- transitions  
- structural uncertainty  

This makes it robust across domains.

---

## Design Principles

- minimal complexity  
- interpretable outputs  
- simulation over assumption  
- no black-box models  
- modular extension  

---

## Known Limitations

- discrete approximation of continuous systems  
- clustering sensitivity  
- no real-time processing yet  
- no global optimal control  
- no semantic interpretation of states  

---

## Core Freeze (v0.7)

The kernel is now frozen.

No further changes to:

- embedding  
- clustering  
- transitions  
- navigation  
- control logic  

Reason:

- preserve reproducibility  
- ensure comparability  
- maintain stability  

---

## Current System Level

NEXAH is now:

→ a State-Space Extraction Engine  
→ a Dynamical System Interpreter  
→ a Navigation & Intervention Framework  

---

## Next Phase

Focus shifts from:

→ building the core  

to:

→ using the core  

### Planned Directions

- CLI refinement (v0.8)  
- real-world datasets  
- visualization layer  
- application development  

---

## Summary

NEXAH v0.7 provides:

- structure extraction  
- dynamic modeling  
- regime detection  
- navigation  
- intervention estimation  
- system comparison  

It is a minimal but powerful foundation for analyzing complex dynamical systems.

---

## Status

Core complete  
Validated on real data  
CLI operational  
Visualization working  

→ System ready for application phase
