# 🧪 NEXAH — Fractal Transition Validation (Building Log)

Path:
RESEARCH/VALIDATION/fractal_tests/

---

## 🎯 Goal

Investigate whether structural transitions in Julia dynamics:

- are detectable via frame-to-frame change (Δ)
- correlate with parameter-space position
- form a structured transition field

---

## 🧩 Phase 1 — Δ Detection

Script:
scripts/fractal_delta_test.py

Outputs:
- delta_circle_plot.png
- delta_peaks.png

---

### Observation

- Δ shows sharp peaks along parameter paths
- Peaks cluster near Mandelbrot boundary structures

---

## 🔁 Phase 2 — Random Path Sampling

Script:
scripts/fractal_delta_random_paths.py

Outputs:
- delta_random_paths.png

---

### Observation

- Δ peaks occur across random paths
- Not restricted to circular sampling
- Heavy-tailed distribution

---

## 🧠 Phase 3 — Topology Check

Script:
scripts/fractal_topology_metrics.py

Outputs:
- topology_check_peak_*.png
- topology_metrics.csv

---

### Method

Compare:
- binary structure before peak
- at peak
- after peak

Metric:
- structural_change(before, after)

---

### Observation

- Most Δ peaks do NOT produce persistent topology change
- Structural differences often revert

→ Δ peak ≠ guaranteed transition

---

## 🔺 Phase 4 — Transition Classification

Types introduced:

- Type I — noise
- Type II — local deformation
- Type III — reversible variation
- Type IV — structural transition

---

### Result

- Type IV extremely rare
- Majority = Type III

---

## 🧭 Phase 5 — Transition Path

Script:
scripts/fractal_transition_path.py

Outputs:
- transition_path_delta.png
- transition_path_area.png
- forced_transition_sequence.png

---

### Observation

- Transition can be forced via path
- Occurs near Δ spike + structural instability
- Transition is localized in parameter space

---

## 📊 Phase 6 — Transition Probability

Script:
scripts/fractal_transition_probability.py

Outputs:
- transition_probability_vs_delta.png
- raw_transition_data.png

---

### Result

- Total peaks: ~100
- Transitions: ~2–5
- Rate: ~2–3%

---

### Observation

- Δ alone insufficient predictor
- High Δ does not always → transition

---

## 🌐 Phase 7 — Continuous Distance Integration

Script:
scripts/fractal_transition_probability_continuous.py

Outputs:
- transition_map_continuous.png
- transition_heatmap_continuous.png
- transition_probability_data.csv

---

### Method

Introduce:
continuous Mandelbrot distance:

distance(c)

---

### Observation

- Data forms structured scatter in (Δ, distance)
- Transitions cluster in specific regions

---

## 🔬 Phase 8 — Clean Transition Field

Script:
scripts/fractal_transition_field_clean.py

Outputs:
- transition_field_clean.png
- transition_field_overlay.png

---

### Method

- Kernel smoothing (Gaussian)
- Avoid histogram artifacts
- Normalize by local density

---

### Result

Stable transition field emerges

---

## 📐 Phase 9 — Field Fit

Script:
scripts/fractal_transition_field_fit.py

Outputs:
- transition_field_fit.png

---

### Observation

- Transition boundary approximates linear separation
- but requires 2D model (Δ + distance)

---

## 📦 Outputs

All visuals stored in:

scripts/outputs/

Key files:

- transition_field_clean.png
- transition_field_overlay.png
- transition_field_fit.png
- transition_map_continuous.png
- transition_probability_data.csv

---

## 🧠 Summary (Process)

```text
Δ → peak detection
→ topology comparison
→ transition classification
→ probability estimation
→ 2D field reconstruction
