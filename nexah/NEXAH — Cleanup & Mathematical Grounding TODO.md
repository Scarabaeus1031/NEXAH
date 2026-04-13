
# NEXAH — Cleanup & Mathematical Grounding TODO

**Date:** April 2026  
**Focus:** Move from intuitive geometry → formal geometric framework

---

### Main Goal

Transition NEXAH from **visual/intuitive geometry** to a **mathematically explicit geometric state-space framework**.

---

### Priority 1 – Mathematical Grounding (Most Important)

- [ ] Define the reduced state vector formally:  
  `x = (coherence, switch_signal, radius, phase, ...)`

- [ ] Define stability as a **region** in state space:  
  `S = { x | r_min < r < r_max  AND  C(x) > c* }`

- [ ] Define a stability metric:  
  `stability_score = time_inside(S) / total_time`

- [ ] Write the control equation:  
  `dx/dt = f(x) + u(x, C(x), geometry)`

- [ ] Explicitly link geometry to IEEE results:  
  “Trajectory enters unstable region ~43.9 s before voltage collapse”

---

### Priority 2 – Repository Cleanup

- [ ] Create `nexah/core/` folder  
- [ ] Create `nexah/core/geometric_framework.md` with clear definitions (state space, trajectory, stability region, control)
- [ ] Move strongly symbolic files (e.g. Root-432_Cylinder_Codex_Breakthrough.md) to `nexah/symbolic_lexicon/experimental/` and add clear disclaimer
- [ ] Clean main README and engineering docs: replace ambiguous terms ("resonance", "breathes at 7.83 Hz", codex language) with geometric/state-space language where appropriate

---

### Priority 3 – Reframing & Documentation

- [ ] Reinterpret existing visuals and descriptions in geometric terms (trajectory behavior, attractor regions, boundary interaction)
- [ ] Document current control capabilities and clear limitations (orbit shaping, multi-attractor navigation, stable switching still missing)

---

### Next Concrete Milestones (Next 2–4 Weeks)

1. Finish `nexah/core/geometric_framework.md`
2. Make adaptive control run on IEEE118 (even basic version)
3. Create one clean minimal demo script
4. Update main README to reflect the geometric state-space framing

---

**Final Target**

NEXAH should be describable as:

> **A geometric state-space framework for analyzing and influencing the dynamics of complex systems.**

---

**Personal Note**  
You already have the geometry, the visuals and the intuition.  
The current task is to make the core mathematically explicit and cleanly structured.
