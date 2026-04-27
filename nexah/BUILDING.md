# 🧱 NEXAH — Building Plan

This document defines the current state and development path of the  
**NEXAH Core System**.

It answers:

- what currently exists  
- what has been observed  
- what is still unclear  
- what the next steps are  

---

## 1. Current Position

NEXAH currently provides a **prototype pipeline** demonstrated in the Lorenz system.

This pipeline connects:

```text
dynamics → field → metrics → signal → behavior
```

Observed:

* local structure can be extracted from chaotic dynamics
* simple field-based metrics produce interpretable signals
* signals correlate with trajectory transitions
* basic trajectory shaping (control) is possible

👉 Important:

This is experimental validation, not a generalized solution.

---

### Phase 1.5 — Structure Extraction (NEW)

Goal:

extract a minimal, reusable core system from experimental scripts  

Steps:

* identify stable components across experiments  
* isolate field, signal, and transition logic  
* refactor into modular components inside `nexah/`  
* remove duplication and script-specific artifacts  

Outcome:

a minimal NEXAH engine with reusable building blocks  

---

## 2. What Actually Exists (Implemented)

### Field Layer

* time series → vector field (dx/dt)
* local flow representation

### Metrics

* flow strength (‖dx/dt‖)
* acceleration (second derivative proxy)
* simple structural indicators

### Signal (Prototype)

* combined signal:

```text
risk ≈ curvature × flow_strength
```

### Behavior (Lorenz Demo)

* local predictability (short horizon)
* regime-like transitions
* observable response to control input

---

## 3. Observed Behavior

Across experiments (Lorenz):

* signals produce sparse high-intensity peaks  
* peaks align with:
  * rapid trajectory changes  
  * transitions between regions  
  * deformation of local flow  

👉 Interpretation:

local flow changes contain information about structural transitions  

---

## 4. What is NOT yet proven

* robustness across systems  
* stability under noise  
* general validity of the risk signal  
* consistency across parameter changes  
* transfer to real-world systems  

👉 Therefore:

NEXAH is currently a validated prototype in a controlled system  

---

## 5. Guiding Idea

NEXAH explores:

**whether system dynamics can be interpreted as a navigable field**

Core hypothesis:

* systems evolve as trajectories in structured spaces  
* local dynamics encode transition information  
* movement can be guided using structural signals  

---

## 6. Minimal System View (IMPORTANT)

At its core, NEXAH is:

```text
state → field → signal → (optional) action
```

Not:

* a full controller  
* not a complete framework  
* not a general solution  

👉 Just a minimal working loop  

---

## 7. Development Strategy

### Phase 1 — Signal Validation (CURRENT FOCUS)

Goal:

determine whether the observed signal is real and robust  

Steps:

* vary Lorenz parameters  
* introduce noise  
* repeat runs  
* compare signal behavior  

---

### Phase 2 — Cross-System Testing

Goal:

test if behavior generalizes  

Systems:

* Lorenz (baseline)  
* second dynamical system (e.g. Van der Pol / Rössler)  

---

### Phase 3 — Minimal Control

Goal:

test whether the signal enables intervention  

Example:

```python
if risk > threshold:
    adjust trajectory slightly
```

Observation:

* does stability improve?  
* does behavior change meaningfully?  

---

### Phase 4 — Integration (LATER)

Only after validation:

* connect field → signal → navigation  
* define reusable interfaces  
* extract core modules  

---

## 8. What is NOT the focus (yet)

* full architecture  
* API design  
* packaging  
* large abstractions  
* production readiness  

👉 These come after validation  

---

## 9. Role of `nexah/`

The `nexah/` package is evolving into:

the minimal executable core of the NEXAH system  

It will contain:

* field construction  
* signal computation  
* transition modeling  
* navigation logic  

It replaces script-based experimentation with reusable structure  

`NEXAH_CORE/` remains the experimental source space
---

## 10. Immediate Next Step

Focus exclusively on:

```text
FIELD → SIGNAL → TRANSITIONS → EXTRACTION → VALIDATION
```

Concrete:

* test robustness of the risk signal  
* document behavior  
* compare across runs  

---

## 🧠 Final Insight

The key question is not:

“Does NEXAH work?”

but:

“Is the observed signal a real structural property of dynamics?”

---

## 🌀 Working Principle

You are not building a framework.

You are testing whether:

dynamics can be navigated through their own structure
