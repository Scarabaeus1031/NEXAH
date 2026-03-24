# NEXAH

**From simulation → structure → navigation.**

*A framework for discovering, mapping and navigating stability in complex dynamical systems.*

---

### What if we didn’t just simulate systems —  
### but extracted their structure and learned how to move through it?

![NEXAH Multi-Agent Navigation](BUILDER_LAB/visuals/nexah_multi_agent.gif)

*No reward. No predefined goal.  
Systems organize. Structure emerges.  
Navigation becomes possible.*

---

## 🧠 What NEXAH actually is

NEXAH is **not just a navigation engine**.

It is a **multi-layer framework** that:

1. **simulates systems**  
2. **extracts structural dynamics**  
3. **builds state graphs**  
4. **enables navigation across stability regimes**

---

## 🧱 The NEXAH Stack

```
Real Systems / Simulations (ARCHY)
        ↓
Discovery Engine (structure extraction)
        ↓
State Graph (Adapter Layer)
        ↓
NEXAH Kernel (navigation)
        ↓
Agents / Policy
```

---

## 🔬 Core Capabilities

### 1. Discovery Engine (Structural Extraction)

NEXAH can extract structure directly from dynamic systems:

- phase maps & parameter scans  
- flow fields & directional dynamics  
- basin detection (stability regions)  
- transition overlays (regime boundaries)  
- meta-fields (combined structural signals)  
- topology extraction:
  - loops (attractors)
  - channels (transitions)
  - nodes (instabilities)
  - networks (global structure)

👉 This turns:

```
simulation → structure → topology
```

---

### 2. Dynamic System Simulation (ARCHY Layer)

Real-world style simulations:

- earth system stress models  
- migration dynamics  
- food production landscapes  
- Monte Carlo risk scenarios  
- collapse trajectories  

Example outputs include:

- global stress maps  
- instability curves  
- conflict dynamics  
- system-wide risk projections  

---

### 3. Adapter Layer (System-Agnostic Integration)

Connect any system:

- power grids (MATPOWER, pandapower, PyPSA)  
- dynamical systems (Lorenz, Kuramoto)  
- supply chains  
- traffic systems  
- biological networks  

Adapters convert:

```
simulator → finite state graph
```

---

### 4. Navigation Engine (NEXAH Kernel)

Agents operate on extracted structure:

- no reward function  
- no predefined objective  
- navigation based on **structural stability**

Core idea:

> Agents do not optimize —  
> they **discover and move within stable regimes**

---

## ⚠️ Important Note (Current Status)

The framework is **fully functional for structure discovery and mapping**.

The **navigation layer is operational**, but:

- strong regime transitions are still emerging  
- navigation becomes more powerful as structure becomes richer  

👉 NEXAH is currently strongest as a:

> **structure discovery + analysis system with emerging navigation capabilities**

---

## 🚀 Use Cases

- stabilizing power grids  
- analyzing cascading failures  
- mapping climate / ecosystem risk  
- understanding chaotic systems  
- discovering hidden structure in simulations  
- autonomous scientific exploration  

---

## ⚡ Quick Start

```bash
git clone https://github.com/Scarabaeus1033/NEXAH.git
cd NEXAH
pip install -e .
```

Run demo:

```bash
python -m nexah demo kuramoto
```

---

## 🧪 What makes this different?

Most systems:

→ simulate behavior  

NEXAH:

→ **extracts structure from behavior**  
→ **maps stability landscapes**  
→ **enables navigation through them**

---

---

## 🔬 Experimental Validation — Prime Modular Resonance

As a minimal test case, NEXAH was applied to a purely discrete system:

→ prime number sequences projected into modular spaces (mod 7)

The system:

- has no geometry  
- no physical dynamics  
- no continuous structure  

---

### 🖼 Discrete → Structure

![Title Visual I](ENGINE/research/experiments/prime_modular_resonance/analysis/output/plots/title_visual_mod7.png)

- nodes → modular states  
- edges → transition probabilities  

---

### 🖼 Structure → Flow

![Title Visual II](ENGINE/research/experiments/prime_modular_resonance/analysis/output/plots/title_visual_ii_mod7.png)

- discrete transitions produce continuous trajectories  
- rotational structure emerges  

---

### 🖼 Flow → Topology

![Title Visual III](ENGINE/research/experiments/prime_modular_resonance/analysis/output/plots/title_visual_iii_mod7.png)

- basin formation  
- dominant cycles  
- loop dynamics  

---

### Result

Even in a fully discrete number system:

→ non-random transition structure  
→ geometric patterns  
→ flow-like behavior  
→ stable cycles  

emerge purely from structure.

---

### Interpretation

> Structure is not imposed —  
> it is **extracted from dynamics**.

---

📄 Full experiment:  
[Prime Modular Resonance](ENGINE/research/experiments/prime_modular_resonance/)

---

## 📂 Key Entry Points

- **[Discovery Engine](./DISCOVERY_ENGINE/)**  
  → structural extraction, topology, phase maps  

- **[Applications](./APPLICATIONS/)**  
  → real system models & simulations  

- **[Adapters](./APPLICATIONS/adapters/README.md)**  
  → connect external systems  

- **[Builder Lab](./BUILDER_LAB/demos/)**  
  → runnable demos  

---

## 🧭 Conceptual Pipeline

```
Simulation
    ↓
Dynamics
    ↓
Flow
    ↓
Topology
    ↓
State Graph
    ↓
Navigation
```

---

## 📊 Core Features

| Feature | Description |
|--------|------------|
| Discovery Engine | Extracts structure from dynamic systems |
| Phase Mapping | Reveals hidden system regimes |
| Flow & Topology | Identifies loops, channels, networks |
| Adapter Layer | Connects any simulator |
| Multi-Agent System | Explores stability landscapes |
| Navigation Kernel | Enables structural system navigation |

---

## 🧠 Key Insight

> Systems do not just evolve —  
> they **organize into structures**  
> that can be **mapped and navigated**

---

## 📈 Implementation Status

Current release: **v1.0**

- discovery engine: ✅ strong  
- simulation layer (ARCHY): ✅ active  
- adapter system: ✅ working  
- navigation engine: ⚠️ emerging  

---

## 📚 Documentation

→ [Extended Framework Documentation](./README_nexah_framework_extended.md)

---

## 📜 Citation

Hofmann, T.K.R. (2026)  
**NEXAH: Structural Discovery and Navigation in Complex Systems**  
https://github.com/Scarabaeus1033/NEXAH  

---

## License

Code: **Apache 2.0**  
Docs: **CC BY 4.0**

© 2026 Thomas K. R. Hofmann
