# NEXAH — Cleanup & Mathematical Grounding TODO (Release Edition)

**Date:** April 2026  
**Goal:** Prepare the project for release and first collaborators — exit solo mode

---

## 🧠 Main Goal

Transition NEXAH from visual/intuitive geometry toward a  
**mathematically explicit geometric state-space framework** — while keeping it readable, reproducible, and attractive for new contributors.

---

## 🔴 Priority 1 – Mathematical Core (STATUS UPDATE)

- [x] Define unified state representations and the mapping between them  
  (engineering features ↔ geometric coordinates: C, r, θ, s)  
  → DONE in `GEOMETRIC_FRAMEWORK.md`

- [~] Write precise, reproducible definitions for all core features  
  (coherence, derivatives, residual, distance, risk, etc.)  
  → PARTIAL (coherence + risk done, rest still implicit in code)

- [x] Formalize stability as a region in state space and define the Risk Field  
  → DONE (`risk_field.md` + framework integration)

- [x] Write the control equation:  
  `dx/dt = f(x) + u(x, risk, geometry)`  
  → DONE (framework + IEEE implementation)

- [x] Create a clean, self-contained document:  
  `FRAMEWORK/CORE_GEOMETRY/GEOMETRIC_FRAMEWORK.md`  
  → DONE (very strong already)

→ 🔥 Core math layer is now **~80–90% complete**

---

## 🟠 Priority 2 – Repository Cleanup (STATUS UPDATE)

- [ ] Create `nexah/core/` as the clean engineering core  
  → NOT DONE (optional but recommended for collaborators)

- [ ] Move strongly symbolic/experimental files to `nexah/symbolic_lexicon/experimental/`  
  → NOT DONE (low priority unless publishing to academia)

- [~] Remove or rephrase symbolic language in main README  
  → PARTIAL (main README is now clean, rest of repo still mixed)

→ 🧠 Cleanup is **~40% done (good enough for soft release)**

---

## 🔵 Priority 3 – Release & Collaboration Preparation (STATUS UPDATE)

- [ ] Get adaptive control running on IEEE118 (basic version)  
  → PARTIAL (IEEE9 strong, IEEE118 field exists, control not unified)

- [~] Create one clean minimal demo script (`run_nexah_demo.py`)  
  → PARTIAL (START_HERE + Lorenz + IEEE scripts exist, but not unified)

- [x] Update main README + APPLICATIONS README  
  → DONE (Top-level UX now strong)

→ 🚀 Release layer is **~60% ready**

---

## 🚀 Next Milestones (REALISTIC ORDER)

1. Create `run_nexah_demo.py` (SUPER IMPORTANT)
2. Light IEEE118 control integration
3. (Optional) introduce `nexah/core/` structure
4. Polish START_HERE.md

---

## 🧭 Final Target

> **NEXAH** is a geometric state-space framework that extracts emergent structure from dynamical systems and enables navigation and adaptive control — without rewards or neural networks.

---

## 🧠 Reality Check

You already have:

- ✅ geometry  
- ✅ visuals  
- ✅ Lorenz navigation  
- ✅ IEEE results (strong!)  
- ✅ working control prototype  

What you need now is:

> **entry points + clarity + reproducibility**

—not more theory.

---

## 🔥 ACTUAL CURRENT STATE

You are no longer building the core.

You are now:

> **productizing a research system**

---

## 🧭 Immediate Next Step (Most Important)

👉 Build:

```
run_nexah_demo.py
```

One file that does:

```text
Lorenz → visualize navigation
IEEE9 → show control
(optional) multi-agent demo
```

→ This is your **"wow in 30 seconds" file**

---

## 🧠 Final Insight

You don’t need more complexity.

You need:

> **one clean path through what already exists**

---

**Last Updated:** April 14, 2026  
© Thomas K. R. Hofmann
