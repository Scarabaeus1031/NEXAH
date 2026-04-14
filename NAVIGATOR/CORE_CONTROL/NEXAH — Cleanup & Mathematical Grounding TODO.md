# NEXAH — Cleanup & Mathematical Grounding TODO (Release Edition)

**Date:** April 2026  
**Goal:** Prepare the project for release and first collaborators — exit solo mode

---

## 🧠 Main Goal

Transition NEXAH from visual/intuitive geometry toward a  
**mathematically explicit geometric state-space framework** — while keeping it readable, reproducible, and attractive for new contributors.

---

## 🔴 Priority 1 – Mathematical Core (2–3 weeks focus)

- [ ] Define unified state representations and the mapping between them  
  (engineering features ↔ geometric coordinates: C, switch, r, θ)

- [ ] Write precise, reproducible definitions for all core features  
  (coherence, derivatives, residual, distance, risk, etc.)

- [ ] Formalize stability as a region in state space and define the Risk Field

- [ ] Write the control equation:  
  `dx/dt = f(x) + u(x, risk, geometry)`

- [ ] Create a clean, self-contained document:  
  `nexah/core/geometric_framework.md` (1–2 pages max)

→ Explicitly link everything to the 43.9 s result.

---

## 🟠 Priority 2 – Repository Cleanup (parallel, 1 week)

- [ ] Create `nexah/core/` as the clean engineering core
- [ ] Move strongly symbolic/experimental files to `nexah/symbolic_lexicon/experimental/` with clear disclaimer
- [ ] Remove or rephrase symbolic language in main README and engineering documentation

---

## 🔵 Priority 3 – Release & Collaboration Preparation

- [ ] Get adaptive control running on IEEE118 (basic version)
- [ ] Create one clean minimal demo script (`run_nexah_demo.py`)
- [ ] Update main README + APPLICATIONS README to reflect the geometric state-space framing

---

## 🚀 Next Milestones (Next 3–4 Weeks)

1. Finish `nexah/core/geometric_framework.md`
2. Adaptive control working on IEEE118
3. Minimal demo script ready
4. Main README updated

---

## 🧭 Final Target

> **NEXAH** is a geometric state-space framework that extracts emergent structure from dynamical systems and enables navigation and adaptive control — without rewards or neural networks.

---

## 🧠 Reality Check

You already have the geometry, the visuals, the IEEE pipeline and a working prototype.  
What you need now is **clarity and a clean core** — not perfection.

**Last Updated:** April 14, 2026  
© Thomas K. R. Hofmann
