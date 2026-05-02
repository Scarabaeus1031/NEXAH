# NEXAH — Core Figures

This section contains the central visual representations of the NEXAH framework.

The figures are organized into:

- **Main Figures** — core conceptual, empirical, and quantitative layers  
- **Extended Figures** — atlas-style and structural expansions  

All figures are derived from trajectory data in reduced slice spaces (v13 / v16).  
Structure is **not assumed** — it is **extracted**.

---

# Main Figures

## Figure 1 — Structural Framework

![Fig1](./main/fig_01_framework.png)

**NEXAH — From Flow to Topology in Dynamical Systems**

This figure presents the core structural pipeline:

**Flow → Sheets → Regimes & Gates → Transitions → Connectivity → Topology**

- Flow generates continuous dynamics in phase space  
- Sheets partition the system into locally coherent motion regions  
- Gates mark regions of structural weakness (low density, coherence, residence)  
- Transitions occur between sheets  
- Connectivity induces global topology  

> Topology is not imposed — it emerges from sheet connectivity.

---

## Figure 2 — Data-Driven Extraction (v13 / v16)

![Fig2](./main/fig_02_extraction.png)

**Empirical Extraction of Sheets, Gates and Transitions**

This figure shows how structural elements are obtained directly from data:

Pipeline:

**Dynamics → Slice → Density → Sheets → Gates → Transitions**

- Slice operator reduces dynamics to structurally relevant coordinates  
- Density and flow fields are estimated from trajectories  
- Sheets are identified as coherent flow layers  
- Gates emerge at low-density, low-coherence intersections  
- Transition statistics are computed from sheet switching  

Right-side panels provide raw evidence:
- Sheet reconstruction (v13)  
- Gate detection (v16)  
- Transition statistics and temporal dynamics  

> All structural elements are empirically extracted from trajectory data.

---

## Figure 3 — Quantitative Characterization

![Fig3](./main/fig_03_quantitative.png)

**Quantitative Structure of Transitions and Connectivity**

This figure provides statistical validation of the framework:

Key observations:

- **Transition probability decreases with proximity to structural cores**
- **Transitions concentrate in intermediate to peripheral regions**
- **Switching is temporally clustered (bursty dynamics)**
- **Residence times follow heavy-tailed distributions**
- **Transitions are local in sheet space**
- **Connectivity structure correlates with emergent topology**

A gate score is defined as:
```text
G(x) ∝ (low density) × (low coherence) × (low residence)
```

Connectivity is quantified via transition matrices and spectral properties.

> Transitions are governed by structural geometry, not random fluctuations.

---

# Extended Figures

These figures expand and generalize the structural framework.

---

## Figure 4 — Extended Structural Pipeline

![Fig4](./extended/fig_04_extended_pipeline.png)

Expanded representation of the full structural pipeline including intermediate layers:
field reconstruction, structure formation, and transition geometry.

---

## Figure 5 — Structural Atlas

![Fig5](./extended/fig_05_structural_atlas.png)

Atlas-style decomposition of dynamical systems into:

- State space  
- Field  
- Sheets  
- Regimes  
- Gates  
- Transitions  
- Temporal dynamics  
- Topology  

Each block is defined both visually and conceptually.

---

## Figure 6 — Topology Emergence Framework

![Fig6](./extended/fig_06_topology_framework.png)

Cross-system comparison showing how different dynamics lead to:

- Twisted (Lorenz-like) topology  
- Spiral (Rössler-like) topology  
- Fragmented (Halvorsen-like) topology  

> Topology emerges from sheet connectivity, not from equations directly.

---

## Figure 7 — Regime Geometry Pipeline

![Fig7](./extended/fig_07_regime_geometry.png)

Detailed view of:

- Sheet aggregation into regimes  
- Basin geometry  
- Gate formation at structural intersections  
- Transition graph construction  

---

## Figure 8 — Full Structural Pipeline with Slice Operator

![Fig8](./extended/fig_08_full_pipeline.png)

Complete pipeline including:

**Dynamics → Slice → Field → Structure → Sheets → Regimes → Gates → Transitions → Time → Navigation**

Includes:

- Temporal switching dynamics  
- Transition intensity  
- Structure-aware navigation  

---

# Core Principle

Across all figures, the same principle holds:

> Flow creates structure.  
> Structure forms sheets.  
> Sheets define transitions.  
> Transitions create connectivity.  
> Connectivity defines topology.

---

# Notes

- All results are computed from trajectory data  
- No topological assumptions are imposed  
- The framework is consistent across multiple dynamical systems  
- Structural elements are robust under system variation  

---

# Integration

These figures connect to:

- `CORE_CONCEPT_MAP.md` — conceptual structure  
- `FINDINGS/` — empirical results  
- `VALIDATION/` — experimental verification  

They form the visual backbone of the NEXAH framework.

