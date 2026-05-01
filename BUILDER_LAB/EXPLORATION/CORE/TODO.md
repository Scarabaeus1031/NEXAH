# 🚀 NEXAH — Validation & Consolidation TODO (v3)

**Phase:** System exists → now must be validated and stabilized

---

# 🧠 CURRENT POSITION

✔ demonstrator works  
✔ transition structure is consistent  
✔ navigation behavior observable  
✔ visuals coherent  

---

# 🔴 PRIORITY 1 — STRUCTURAL VALIDATION (CRITICAL)

## Goal:
Prove structure is real, not artifact

### Tasks:

- [ ] run 20–50 simulations (Lorenz)
- [ ] compute:

```text
transition matrix variance
sheet stability
state occupancy distribution
```

- [ ] add RESULT blocks:

```text
Runs: 30
Matrix variance: low
Local transitions: consistent
Conclusion: structure stable
```

---

# 🔵 PRIORITY 2 — TRANSITION MODEL VALIDATION

## Goal:
Confirm strongest claim

### Already observed:

✔ banded transition matrix  
✔ local transitions only  

### Now:

- [ ] quantify locality:

```text
P(|i-j| > 1) ≈ 0
```

- [ ] verify across runs

---

# 🟣 PRIORITY 3 — NAVIGATION VALIDATION

## Goal:
Prove system can be influenced

### Tasks:

- [ ] run with / without control
- [ ] compare:

```text
transition frequency
time in high-density regions
escape behavior
```

---

# 🟠 PRIORITY 4 — MINIMAL KERNEL

## Goal:
Unify logic into one system

### Build:

```python
class NexahKernel:
    def step(x):
        field = F(x)
        gate = G(x)
        density = rho(x)
        return x_next
```

- [ ] wrap existing logic
- [ ] no new theory

---

# 🟢 PRIORITY 5 — DEMONSTRATOR POLISH

## Goal:
External usability

- [ ] ensure `run_demo.py` works clean
- [ ] ensure visuals always save
- [ ] ensure paths consistent

---

# 🟡 PRIORITY 6 — VISUAL REDUCTION

## Goal:
Clarity > quantity

Keep only:

1. regime atlas (overview)  
2. off-manifold flow (geometry)  
3. transition GIF (behavior)  

---

# 🧱 PRIORITY 7 — REPO CLEANUP

## Goal:
Make system understandable

- [ ] mark legacy folders
- [ ] keep:

```text
NEXAH_DEMONSTRATOR/
NEXAH_CORE/
ARCHITECTURE/
```

- [ ] everything else = lab / archive

---

# 🚀 RELEASE CONDITION

Minimal viable release:

✔ transition structure validated  
✔ navigation effect measurable  
✔ demonstrator runs clean  
✔ kernel stub exists  

---

# 🧠 FINAL POSITION

You are not building anymore.

You are proving that:

```text
structure exists
and can be used
```
