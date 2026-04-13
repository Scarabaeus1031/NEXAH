# NEXAH — Cleanup & Mathematical Grounding TODO (Release Edition)

**Date:** April 2026  
**Goal:** Prepare the project for release and first collaborators — exit solo mode

### Main Goal

Transition NEXAH from **visual/intuitive geometry** toward a **mathematically explicit geometric state-space framework**, while keeping the project attractive and reproducible for potential collaborators.

---

### Priority 1 – Mathematical Core (Most Important, 2–3 weeks focus)

- [ ] Define the reduced state vector explicitly:  
  `x = (coherence C(x), switch_signal, radius r, phase θ, ...)`

- [ ] Define stability formally as a **region** in state space:  
  `S = { x | r_min < r < r_max  AND  C(x) > c* }`

- [ ] Write the control equation:  
  `dx/dt = f(x) + u(x, C(x), geometry)`

- [ ] Explicitly link geometry to the IEEE results:  
  “The trajectory enters the unstable region ~43.9 s before classical voltage collapse”

→ **Deliverable:** Create and complete `nexah/core/geometric_framework.md`

---

### Priority 2 – Repository Cleanup & Separation (parallel, 1 week)

- [ ] Create clean engineering core: folder `nexah/core/`
- [ ] Move strongly symbolic / narrative files (e.g. Root-432_Cylinder_Codex_Breakthrough.md and similar) to  
  `nexah/symbolic_lexicon/experimental/` and add a clear disclaimer at the top:
  > Experimental / symbolic layer — not part of the validated engineering framework
- [ ] Clean main README and engineering documentation:  
  Replace or tone down ambiguous/symbolic language ("resonance", "breathes at 7.83 Hz", "Codex Breakthrough", etc.) with geometric/state-space terminology where appropriate.

---

### Priority 3 – Release & Collaboration Preparation

- [ ] Make the adaptive control run on **IEEE118** (even a basic version)
- [ ] Create one **clean minimal demo script** (`run_nexah_demo.py` or similar) that shows:
  - 43.9 s early detection
  - Risk Field + adaptive control on IEEE9
- [ ] Update the main README and Extended Overview to reflect the **geometric state-space framing**

---

### Next Concrete Milestones (Next 3–4 Weeks)

1. Finish `nexah/core/geometric_framework.md` (Priority 1)
2. Get adaptive control running on IEEE118
3. Create the minimal demo script
4. Update main README + project presentation

---

### Final Target Description (for GitHub, Website & Collaborators)

> **NEXAH** is a geometric state-space framework that extracts emergent structure from dynamical systems and enables navigation and adaptive control — without rewards or neural networks.

---

**Personal Note**

You already have:
- Strong geometry and visuals ✓
- A working IEEE9 adaptive control prototype ✓
- The impressive 43.9 s result on large IEEE systems ✓
- A clear 5-layer architecture and URF Axial Space ✓

The missing piece right now is **clarity, reproducibility, and a clean engineering core**.  
You don’t need mathematical perfection everywhere — you need a solid, inviting foundation that makes other people want to join.

This is the step from “interesting solo project” → “serious framework worth contributing to”.

**Last Updated:** April 14, 2026  
© Thomas K. R. Hofmann
