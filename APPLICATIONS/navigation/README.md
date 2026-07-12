# NEXAH Navigation

> **Status: Legacy / experimental navigation prototype.** This area preserves
> an earlier Mod-77 and IEEE9-oriented navigation line. It is executable
> research material, not the canonical or fully integrated NEXAH navigator.

This directory contains the **navigation layer** of the NEXAH framework.  
It translates structural insights (field geometry, resonance grids, emergent exponents) into practical, executable navigation for complex dynamic systems — with a strong focus on power system stability.

## Directory Structure

```bash
APPLICATIONS/navigation/
├── core/                    # Core mathematical and resonance components
│   ├── mod77_state_space.py          # Hierarchical Mod-77 grid (77 + 308 states)
│   ├── scaling_exponent.py           # Emergent p ≈ 0.308 and multiplication chain
│   ├── drift_quantization.py         # Drift analysis, Phi-Split & Transfer detection
│   └── visualization.py              # Trajectory and event plotting
├── integration/             # Prototypes and integration scripts
│   ├── ieee9_navigation.py           # IEEE9 voltage collapse navigation example
│   └── run_navigation_demo.py        # Abstract risk-aware navigation demo
├── results/                 # Generated outputs and plots
│   └── plots/
└── README.md
```
---

## Key Concepts Implemented

- **Mod-77 Hierarchical Resonance Grid**: Discrete state space based on Mod-7 × Mod-11 (77 base states, extended to 308 fine states with δ = 0.17)
- **Emergent Scaling Exponent**: `p ≈ 0.308` — describes transition from state-dominated to flow-dominated behavior in large systems
- **Phi-Split & Transfer Events**: Early detection of significant drift changes for proactive navigation
- **Geometry-informed Navigation**: Instead of reactive control, the system uses structured stability landscape and resonance patterns

## Quick Start

From the repository root, run the IEEE9-style prototype:

```bash
python APPLICATIONS/navigation/integration/ieee9_navigation.py
```

**Expected output includes:**
- Voltage trajectory mapped to Mod-77 states
- Detected Phi-Split and Transfer Events
- Scaling exponent p ≈ 0.308
- Prime Leap observation (13 + 16 = 29)

---

## Current Status (April 2026)

- Mod-77 state-space prototype implemented
- Drift quantization and Phi-Split detection implemented
- Basic IEEE9-like trajectory example available
- Integration with the older `run_navigation_demo.py` remains incomplete
- Comparison with current power-system pipelines remains open

## Next Steps

1. Clean up remaining internal imports in core files (`scaling_exponent.py`, `visualization.py`)
2. Connect `run_navigation_demo.py` (risk-aware policy) with the new Mod-77 grid
3. Compare against maintained IEEE benchmark pipelines (IEEE9 → IEEE118 → IEEE300)
4. Implement Meta-Layer scaling and Fibonacci Root Shrinking
5. Create comprehensive visualization of trajectories in the resonance grid

---

**NEXAH · Thomas K. R. Hofmann · 2026**  
From dynamics → structure → geometry → navigable stability landscape
