# 🧭 NEXAH — Field Decomposition Layer

![Lyapunov Map](outputs/v8_0_lyapunov_map/v8_0_lyapunov_map.png)

---

## Overview

This module explores a continuous 2D dynamical field and extracts:

- structure (basins, boundaries, channels)
- dynamics (trajectories, orbits)
- transitions (sensitivity, separatrix-like regions)
- navigation (cost, reachability, optimal flow)
- stability (Lyapunov structure)

It is built through iterative simulation, visualization, and structural analysis.

It is:

→ not a physical theory  
→ not a new mathematical framework  

It is:

→ a **computational system for extracting geometry from dynamics**

---

## Core Idea

> Structure shapes motion.

The system is defined by:

$begin:math:display$
\\dot\{x\} \= \-\\nabla V\(x\) \+ R\(x\)
$end:math:display$

Where:

- gradient → attraction  
- rotation → curvature and persistence  

Result:

→ motion is not imposed  
→ it **emerges from field geometry**

---

## Pipeline

The module transforms:

```text
field
→ trajectories
→ structure detection
→ boundary extraction
→ cost field
→ navigation
→ stability analysis
```

---

## Key Capabilities

- basin detection  
- orbit classification  
- separatrix-like boundary detection  
- sensitivity mapping  
- cost-based navigation  
- energy landscape estimation  
- Lyapunov stability mapping  
- gate detection (weak stability regions)  

---

## Visual System

The system is explored through layered visualizations:

| Layer | Meaning |
|------|--------|
| Q1 | trajectory class map |
| Q2 | field + trajectories |
| Q3 | sensitivity |
| Q4 | geometric projection |
| Q5 | orbit bands |
| Q6 | representative trajectories |

Extended layers:

- V7 → cost, navigation, reachability  
- V8 → stability (Lyapunov), gates, injection behavior  

---

## Key Observations

Across all phases, the system consistently shows:

- multiple attractor basins  
- orbit-like trajectories  
- structured transition regions ("Riss")  
- narrow transition corridors ("splinter")  
- asymmetric flow behavior  
- layered orbit families  

Important:

→ these structures **emerge from the field**  
→ they are not manually imposed  

---

## Navigation Layer (V7)

The system can be interpreted as a navigation problem:

- cost field → effort to reach a target  
- navigation field → optimal direction  
- reachability → where motion is possible  

Key result:

→ motion is **not globally free**  
→ it is **geometrically constrained**

---

## Stability Layer (V8)

A Lyapunov-like analysis reveals:

- global stability structure of the field  
- weak regions along boundaries ("gates")  
- strong stability inside basins  

### Critical Result

```text
The system contains gates, but no decisions.
```

Meaning:

- transition regions exist  
- entry points exist  
- but no branching outcomes occur  

→ all tested perturbations converge to the same attractor  

---

## System Interpretation

The system is best described as:

→ a **directed dynamical system**

Properties:

- structured flow  
- constrained transitions  
- dominant attractor behavior  
- no multi-branch decision topology  

---

## Example Visuals

### Navigation Field

![Navigation](outputs/v7_3/v7_3_navigation.png)

---

### Energy Landscape

![Energy](outputs/v7_7/v7_7_energy_map.png)

---

### Injection Behavior

![Injection](outputs/v8_5_injection_tests/v8_5_injection_tests.png)

---

## Project Structure

```text
ENGINE/analysis/field_decomposition/

scripts/
├── v2_* → field separation
├── v3_* → structure detection
├── v4_* → unified field views
├── v5_* → gradient vs rotation
├── v6_* → classification + boundaries
├── v7_* → cost + navigation
├── v8_* → stability + gates

outputs/
├── v6_*/
├── v7_*/
├── v8_*/
```

---

## How to Run

Example:

```bash
python scripts/v6_6_core.py
python scripts/v7_2_transition_cost_map.py
python scripts/v8_0_lyapunov_map.py
```

Outputs are saved to:

```text
ENGINE/analysis/field_decomposition/outputs/<version>/
```

---

## Status

Current phase:

→ exploratory but structurally consistent  

Evolution:

```text
visual exploration
→ structure detection
→ navigation
→ stability geometry
```

---

## Interpretation Scope

This work:

✔ explores structure in dynamical systems  
✔ provides reproducible simulations  
✔ identifies consistent geometric patterns  

This work does NOT:

✖ claim new physical laws  
✖ provide analytical proofs  
✖ map directly to real-world systems  

---

## Final Insight

```text
The system does not offer choices.

It defines paths.
```

---

## Next Steps

- stochastic perturbation (noise)
- multi-target navigation
- higher-dimensional extension
- analytical approximation
- integration into NEXAH Navigator

---

## Final Note

This module is best understood by:

- running the scripts  
- inspecting the visuals  
- comparing layers  

Understanding emerges from:

> reading the field — not just observing trajectories
