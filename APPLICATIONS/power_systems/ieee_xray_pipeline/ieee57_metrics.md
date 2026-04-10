# IEEE57 Metrics — NEXAH Controllers

## Metrics Used

### Core Stability Metrics
- Mean coherence
- Max radius
- Mean radius

### Dynamic Behavior
- Escape count
- Collapse timing
- Time in band
- Reentry count

### Control Metrics
- Control signal magnitude
- Control saturation (|u| ≈ U_MAX)
- Activation counts:
  - lift
  - pulse
  - snap

### Phase / Gate Metrics
- Gate score
- Time near gate (score threshold)
- Snap activation count

---

## v14.5 Key Results

- Mean coherence ↑
- Max excursion ↓
- Escape count: **30 → 0**
- Control saturation near **U_MAX**

### Interpretation

- strong stabilization effect
- insufficient orbital energy
- gate activation negligible

---

## v14.6 Key Results (Orbit Capture)

- Escape reduction maintained
- Time in band ↑
- First successful **core → capture → band transitions**

### Observations

- trajectory lifted out of core
- partial band occupation achieved

### Limitations

- no sustained orbit
- gate_lock not triggered
- inward collapse persists

---

## v14.7–v14.7c (Orbital Flow Injection)

- Angular forcing applied
- Increased phase alignment pressure

### Observations

- slight drift appears
- trajectory becomes more rigid

### Limitation

- no full rotation
- phase clustering remains

---

## v14.8 (Two-Axis Control)

- radial control (P) effective
- tangential control (Q) introduced

### Observations

- coherence ↑
- stability maintained

### Critical Result

- tangential control ineffective
- no rotation emerges

---

## v14.9 (State-Space Orbit Injection)

- artificial tangential dynamics introduced
- rotation applied directly in NEXAH space

### Observations

- first controlled angular motion (prototype)
- decoupling of:
  - grid dynamics
  - NEXAH field dynamics

---

## Cross-Version Insight

### What Works

- stability improvement ✔
- escape suppression ✔
- structural state space ✔

### What Fails

- orbit formation ❌
- gate locking ❌
- sustained angular motion ❌

---

## Fundamental Finding

> The IEEE57 system supports **radial control (stability)**  
> but does NOT support **tangential control (rotation)**.

---

## Interpretation

### Current Capability

- strong stabilizer
- reliable anomaly suppression
- measurable control impact

### Missing Capability

- expansion to target orbit band
- sustained rotation
- phase-gate engagement

---

## Structural Limitation

- system is strongly **dissipative**
- trajectories collapse toward equilibrium
- control inputs are effectively **non-orthogonal**

---

## Open Questions

- how to inject **energy / expansion** into the system?
- how to construct a **true tangential control axis**?
- how to generate **stable limit cycles (orbits)**?
- how to map NEXAH control to **physical actuators**?
- is orbit behavior:
  - extractable from system?
  - or must it be **constructed as a field layer**?

---

## Next Direction

- explicit field construction (NEXAH layer)
- orbit generation independent of system dissipation
- hybrid control:
  - physical stabilization (grid)
  - synthetic navigation (field)
