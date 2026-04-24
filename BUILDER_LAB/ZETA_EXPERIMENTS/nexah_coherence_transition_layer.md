# NEXAH — Coherence Transition Layer (Build Plan)

## 🎯 Goal

Develop a reproducible, structure-based transition detection mechanism:

> Transitions occur at coherence collapse induced by field structure

---

# 🧪 PHASE 1 — SIGNAL VALIDITY

- [ ] signal shows clear regime separation
- [ ] includes at least one true structural break
- [ ] not just amplitude increase
- [ ] stable → oscillatory → decoherent → new regime

---

# 📊 PHASE 2 — COHERENCE MODEL

- [ ] replace lag-1 correlation
- [ ] implement multi-lag coherence
- [ ] test spectral coherence (FFT)
- [ ] optional: entropy / phase variance

Validation:

- [ ] coherence drops significantly at transition
- [ ] coherence stable within regimes

---

# 🚪 PHASE 3 — GATE DETECTION

- [ ] remove simple threshold logic
- [ ] detect sustained collapse regions
- [ ] implement minimum duration filter
- [ ] avoid initialization artifacts

---

# 📈 PHASE 4 — VISUAL VALIDATION

- [ ] signal plot
- [ ] coherence plot
- [ ] gate overlay
- [ ] transitions align with coherence collapse

---

# 🔁 PHASE 5 — MULTI-RUN VALIDATION

- [ ] run ≥ 30 simulations
- [ ] measure gate consistency
- [ ] compute mean + variance
- [ ] check robustness to noise

---

# 🧠 PHASE 6 — STRUCTURAL VALIDATION

- [ ] gates align with field geometry
- [ ] not random in time
- [ ] reproducible across seeds
- [ ] linked to interference structure

---

# 📦 PHASE 7 — MODULE READINESS

To move into core system:

## FIELD_LAYER candidate if:
- [ ] coherence is field-derived
- [ ] transitions emerge from geometry
- [ ] no hard thresholds needed

## ARCHITECTURE candidate if:
- [ ] usable for navigation
- [ ] enables decision-making
- [ ] supports control / intervention

## APPLICATION candidate if:
- [ ] validated on IEEE test case
- [ ] real data compatibility
- [ ] measurable improvement

---

# 🚫 NOT ALLOWED

- [ ] no symbolic explanations
- [ ] no metaphors (tunnel, snake, etc.)
- [ ] no unverifiable claims
- [ ] no complexity without validation

---

# 🔥 SUCCESS CONDITION

We can state:

> Regime transitions correspond to measurable coherence collapse  
> induced by underlying field structure

---

# STATUS

⚠️ Currently in experimental stage (Builder Lab)

Next step:
→ implement v2 and validate collapse

# NEXAH — IEEE Gate Detection (v2 PLAN)

## Status
⚠️ Prototype exists (v1)  
⚠️ Not yet scientifically valid  
✅ Concept promising  

---

## 🧠 Core Idea

Regime transitions occur at:

> **loss of coherence**, not arbitrary thresholds

Pipeline:

Field → Signal → Coherence → Gate → Transition

---

## 🔴 CURRENT PROBLEM (v1)

Observed:

- coherence C(t) stays ~0.9
- no real collapse
- gates detected only at initialization

Conclusion:

> ❌ No real regime transition detected  
> ❌ Current coherence metric too weak  

---

## 🧪 REQUIRED FIXES (v2)

### 1. SIGNAL DESIGN (CRITICAL)

We need:

- clear regime separation
- actual structural break

Target signal:

```text
stable → oscillatory → decoherence → new regime
```

NOT just:
```text
stable → stronger oscillation
```

---

### 2. COHERENCE METRIC (CORE UPGRADE)

Replace simple lag-1 correlation with a more expressive measure.

Options:

- [ ] multi-lag autocorrelation
- [ ] spectral coherence (FFT-based)
- [ ] phase variance
- [ ] entropy-based measure

Minimal v2 approach:

```python
# multi-lag coherence proxy
def compute_coherence(segment):
    lags = [1, 2, 3, 5]
    vals = []
    for lag in lags:
        if len(segment) > lag:
            c = np.corrcoef(segment[:-lag], segment[lag:])[0, 1]
            if not np.isnan(c):
                vals.append(c)
    return np.mean(vals) if vals else 0.0
```

---

### 3. WINDOW STABILITY

Fix initialization artifacts:

- [ ] ignore first N timesteps (warmup)
- [ ] require minimum window fill
- [ ] avoid division-by-zero / flat signals

Example:

```python
warmup = 50

for i in range(window, len(x)):
    if i < warmup:
        C[i] = np.nan
        continue
```

---

### 4. GATE DEFINITION (REFINED)

Replace simple thresholding:

Current:
```
|C| < epsilon
```

Upgrade:
```
Gate = sustained coherence collapse
```

Implementation idea:

```python
epsilon = 0.2
min_duration = 10

gate_mask = np.abs(C) < epsilon

gates = []
start = None

for i, val in enumerate(gate_mask):
    if val and start is None:
        start = i
    elif not val and start is not None:
        if i - start >= min_duration:
            gates.append((start, i))
        start = None
```

---

### 5. VISUAL VALIDATION

Required output:

- [ ] 3-panel plot
- [ ] visible coherence collapse
- [ ] gate aligned with collapse

Enhancement:

```python
for (s, e) in gates:
    ax2.axvspan(t[s], t[e], alpha=0.2)
```

---

### 6. MULTI-RUN VALIDATION (PRIORITY 1)

Run multiple simulations:

```python
runs = 30
results = []

for r in range(runs):
    np.random.seed(r)
    x = generate_signal()
    C = compute_C(x)
    gates = detect_gates(C)
    results.append(len(gates))
```

Metrics:

- [ ] mean gate count
- [ ] variance
- [ ] timing consistency

---

## 📊 TARGET RESULT FORMAT

```
Runs: 30
Mean gates: 2.1 ± 0.3
Mean coherence drop: 0.92 → 0.08
Timing variance: low
```

---

## 🧭 SCIENTIFIC CLAIM (TO VALIDATE)

If validated:

> Regime transitions correspond to structural coherence loss

NOT:

> threshold crossing

---

## ⚠️ DO NOT DO

- ❌ no new theory
- ❌ no symbolic extensions
- ❌ no complexity explosion

---

## ✅ NEXT EXECUTION STEP

When resuming:

1. redesign signal (true collapse)
2. upgrade coherence metric
3. rerun detection
4. validate visually
5. run multi-test

---

## 📂 FILE PLAN

```
demos/
├── ieee_gate_detection_v1.py
├── ieee_gate_detection_v2.py
└── outputs/
    ├── v1.png
    └── v2.png
```

---

## 🔥 FINAL GOAL

Turn:

```
nice idea
```

into:

```
reproducible structural signal
```

---

Last updated: April 2026
© Thomas K. R. Hofmann




