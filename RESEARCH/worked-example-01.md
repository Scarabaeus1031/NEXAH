# Worked Example 01  
## Minimal Structural Stabilization on a Finite Poset

This example demonstrates how the NEXAH operator chain operates on a small finite partially ordered set.

The goal is to illustrate:

- Closure (Γ)
- Regime transition (Δ)
- Stabilization (Ω)
- Basin structure
- Frame-dependent interpretation

---

## 1. Base Structure

Let Q = {a, b, c, d, e, f}

Define the partial order ⪯ as:

- a ⪯ c  
- b ⪯ c  
- c ⪯ d  
- c ⪯ e  
- d ⪯ f  
- e ⪯ f  

This defines a finite poset with one maximal element f.

---

## 2. Closure Operator Γ

Define Γ as upward closure toward c:

Γ(x) = least element ≥ x that lies in {c, d, e, f}

Thus:

- Γ(a) = c  
- Γ(b) = c  
- Γ(c) = c  
- Γ(d) = d  
- Γ(e) = e  
- Γ(f) = f  

Γ is:

- Monotone  
- Extensive  
- Idempotent  

---

## 3. Regime Operator Δ

Define Δ as monotone upward propagation toward f:

- Δ(a) = c  
- Δ(b) = c  
- Δ(c) = d  
- Δ(d) = f  
- Δ(e) = f  
- Δ(f) = f  

Δ is:

- Monotone  
- Extensive  

---

## 4. Stabilization via Iteration

Compute iterations:

a → c → d → f  
b → c → d → f  
c → d → f  
d → f  
e → f  
f → f  

All chains stabilize at f.

Define:

Ω(x) = stabilized value of Δ-iteration

Thus:

Ω(x) = f for all x ∈ Q

---

## 5. Fixpoint Structure

Fix(Δ) = {f}

Ω is the projection:

Ω : Q → {f}

There is a single basin:

B(f) = Q

---

## 6. Alternative Regime Definition

If instead Δ' is defined as:

- Δ'(a) = c  
- Δ'(b) = c  
- Δ'(c) = d  
- Δ'(d) = d  
- Δ'(e) = e  
- Δ'(f) = f  

Then:

- d stabilizes at d  
- e stabilizes at e  
- f stabilizes at f  

Now:

Fix(Δ') = {d, e, f}

Basins become non-trivial.

---

## 7. Frame Interpretation

Under a global frame:

- System converges to f (total dominance regime)

Under a regional frame:

- Multiple stabilization regions exist

This demonstrates:

Structure is primary.  
Regime restricts.  
Frame projects.

---

## 8. Structural Insight

This example illustrates:

- Extensivity + finiteness ⇒ stabilization
- Fixpoints emerge from operator definition
- Basin partition depends on regime definition
- Interpretation depends on frame selection

Application meaning emerges only after structural instantiation.
