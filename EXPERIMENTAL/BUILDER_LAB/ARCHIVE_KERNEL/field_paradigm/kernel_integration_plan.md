# 🧭 NEXAH — Kernel Integration Plan (v1)

**Date:** April 2026  
**Purpose:** Stabilize, unify, and operationalize the NEXAH system  

---

# 🧠 1. CURRENT REALITY (GROUND TRUTH)

NEXAH is no longer a prototype.

It already implements a full structural pipeline:

```text
dynamics
→ field reconstruction
→ geometry (basins, channels, separatrix)
→ stability (Lyapunov, gradients)
→ transition geometry (gates, corridors)
→ control (flow-aligned, structure-aware)
→ navigation (trajectory steering)
```

---

## 🔥 Key Observation

The system is **functionally complete**, but:

```text
❌ not unified
❌ not cleanly structured
❌ not exposed as a single execution system
```

---

## ⚠️ Core Problem

```text
Multiple parallel representations of NEXAH exist:

- old (signal-based)
- mid (transition-based)
- current (field + control + navigation)
```

👉 This causes confusion and loss of overview.

---

# 🧭 2. GOAL (NEXT PHASE)

Transition from:

```text
experimental modules
→ integrated system
```

---

## 🎯 Target State

```text
NEXAH = executable kernel
```

That performs:

```text
state → field → geometry → transitions → control → next_state
```

---

# 🧱 3. TARGET STRUCTURE (nexah/)

---

## 🔴 Core Principle

```text
SYSTEM ≠ DEMOS
```

---

## 📁 Proposed Structure

```text
nexah/
│
├── core/                    # 🔥 SYSTEM (NEW CENTER)
│   ├── kernel.py            # ⭐ main execution loop
│   ├── field.py             # field computation
│   ├── geometry.py          # basins, channels, separatrix
│   ├── transition.py        # transition + gate logic
│   ├── control.py           # control logic
│
├── modules/                 # existing logic (reused)
│   ├── field_layer/
│   ├── navigation/
│   ├── transitions/
│
├── demos/                   # visual + pipeline demos
│   ├── pipeline_demo.py
│   ├── pipeline_control_demo.py
│
├── outputs/
├── README.md
```

---

# 🧠 4. THE MISSING PIECE

## 🔥 Nexah Kernel

This does NOT exist yet as a unified component.

---

## 🎯 Required Component

```python
class NexahKernel:
    def step(self, x):
        field = ...
        geometry = ...
        transitions = ...
        control = ...

        x_next = x + field + control

        return x_next
```

---

## 🧠 Interpretation

This is the moment where NEXAH becomes:

```text
a system (not a collection of modules)
```

---

# 🧪 5. CURRENT MODULE STATUS

---

## ✔ Already Exists (Reusable)

- field computation → `field_layer`
- transition graph → `transition_graph.py`
- navigation → `navigator.py`
- control → `field_control.py`

---

## ❗ Problem

These are:

```text
spread across files
not unified
partially mixed with demos
```

---

# 🔧 6. REFACTORING PLAN

---

## STEP 1 — Create Kernel

- create:
  ```text
  nexah/core/kernel.py
  ```
- implement minimal `step(x)`

---

## STEP 2 — Connect Pipeline

Use:

- `field_layer` → field
- `transition_graph` → transitions
- `field_control` → control

---

## STEP 3 — Separate Demos

Move:

```text
app/
navigation/*.py (visuals)
```

→ into:

```text
nexah/demos/
```

---

## STEP 4 — Define Clean Interfaces

Each layer must expose:

```text
input → output
```

Example:

```text
field(x) → F(x)
transition(x, F) → gates
control(x, F, gates) → u(x)
```

---

# 🔬 7. WHAT NOT TO DO

---

❌ Do NOT rebuild system  
❌ Do NOT introduce new theory  
❌ Do NOT add new experimental modules  
❌ Do NOT refactor everything at once  

---

# 🧠 8. WHAT TO DO

---

✔ Extract kernel  
✔ Stabilize interfaces  
✔ Separate demos from system  
✔ Align all modules to one pipeline  

---

# 🧭 9. CURRENT DEVELOPMENT PHASE

```text
Builder Phase → System Integration Phase
```

---

# 🚀 10. NEXT WORK SESSION (START HERE)

---

## Minimal plan for tomorrow:

1. create:
   ```text
   nexah/core/kernel.py
   ```

2. implement:

```python
def step(x):
    return x
```

3. plug into:

```text
pipeline_demo.py
```

4. run system through kernel

---

## Goal:

```text
everything flows through ONE entry point
```

---

# 🧠 FINAL INSIGHT

```text
You already built NEXAH.

Now you are turning it into a system.
```

---

**Status:** Integration Phase  
**Focus:** Kernel + Structure  
**Mode:** Reduce complexity, increase clarity  

---

Thomas K. R. Hofmann · NEXAH · 2026
