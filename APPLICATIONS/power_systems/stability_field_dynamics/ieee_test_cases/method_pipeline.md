# Method Pipeline — Stability Field Dynamics

## Overview

This pipeline describes how raw power system simulations  
are transformed into a geometric + dynamical + topological representation  
of stability and collapse.

Process:

Simulation → Feature Extraction → Field Construction → Structure Detection → Analysis

---

## 1. System Simulation

Input:
- IEEE test systems (9, 14, 30, 57, 118)
- Load variation (parameter sweep)

Output:
- Time series of system states under increasing load stress

---

## 2. Feature Extraction

Compute:

- c   = normalized system state
- dc  = first derivative (drift)
- d²c = second derivative (acceleration)

Phase representation:
(c, dc, d²c)

---

## 3. Phase Space Construction

Embed trajectory in:

(c, dc)

Use d²c for curvature and dynamics.

---

## 4. Manifold Extraction

Fit empirical relation:

d²c ≈ a · c^p · (dc)^q

Procedure:
- log-transform variables
- linear regression in log-space
- estimate (a, p, q)

Result:
→ collapse manifold

---

## 5. Residual Computation

residual = d²c − a · c^p · (dc)^q

Interpretation:
- residual ≈ 0 → aligned with manifold
- residual ≠ 0 → deviation from structure

---

## 6. Rift Extraction (Collapse Boundary)

rift = { (c, dc) | residual ≈ 0 }

Method:
- threshold filtering
- smoothing / interpolation

Result:
→ continuous collapse boundary

---

## 7. Stability Distance

distance = min || (c, dc) − rift ||

Meaning:
- small → stable
- large → unstable

---

## 8. Vector Field Construction

F(c, dc) = (Δc, Δdc)

Method:
- finite differences
- optional smoothing

Result:
→ phase-space flow field

---

## 9. Flow Analysis

Extract:
- direction consistency
- divergence / convergence
- curvature

Identify:
- coherent flow regions (GH corridor)
- unstable regions

---

## 10. Projection Analysis

Project into:

(distance, residual)

Reveals:
- clusters
- deformation regions
- collapse topology

---

## 11. Clustering

Apply clustering on (distance, residual)

Detect:
- core cluster (stable)
- secondary cluster (pre-collapse)
- noise (transition / collapse)

---

## 12. Collapse Metrics

collapse_strength ≈ |residual| × τ

Additional:
- curvature (from derivatives)
- divergence (local expansion rate)

---

## 13. Temporal Analysis

Track over time:
- distance(t)
- residual(t)
- curvature(t)
- divergence(t)

Detect:
→ early warning signals

---

## 14. Universality Validation

Compare across systems:
- manifold parameters (p, q)
- geometry (distance, residual)
- cluster structure

Result:
→ scale-invariant behavior

---

## 15. Output Artifacts

Generated outputs:
- phase plots
- manifold fits
- vector fields
- rift boundary
- stability maps
- clustering results

Stored in:
outputs/

---

## Core Principle

Raw dynamics → structure → field → topology → prediction

---

## Final Insight

The pipeline does not detect collapse as an event.

It reconstructs the structure that makes collapse inevitable.
