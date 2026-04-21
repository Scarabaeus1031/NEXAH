# NEXAH Toolbox Reference

This document provides a reference for the analysis tools located in:

```
ENGINE/nexah_kernel/tools
```

The toolbox contains experimental modules for exploring dynamical structures within NEXAH regime landscapes.

Most tools operate on parameter scans stored in:

```
ENGINE/nexah_kernel/demos/data
```

and generate visual outputs in:

```
ENGINE/nexah_kernel/demos/visuals
```

---

# Resonance Analysis

## discover_resonance_zones.py

Identifies high-scoring resonance regions in parameter space.

Output:

- top_resonance_zones.json

---

## resonance_ridge_detector.py

Detects ridge structures within resonance landscapes.

Output:

- resonance_ridges.png
- resonance_ridges.json

---

## resonance_harmonic_analyzer.py

Analyzes harmonic patterns within resonance zones.

Output:

- resonance_harmonics.json
- harmonic spectrum plots

---

# Attractor Analysis

## nexah_resonance_attractor_finder.py

Detects attractor regions in resonance landscapes.

Output:

- resonance_attractors.json
- resonance_attractors_map.png

---

# Rotation & Frequency Analysis

## nexah_rotation_number_analysis.py

Computes rotation numbers across parameter space.

Output:

- rotation_number_map.png
- rotation_numbers.json

---

## nexah_devils_staircase.py

Generates Devil’s Staircase plots from rotation number analysis.

Output:

- devils_staircase.png

---

# Frequency Locking Analysis

## nexah_arnold_tongue_map.py

Detects Arnold tongue structures representing frequency locking.

Output:

- arnold_tongues.png

---

# Stability Analysis

## nexah_lyapunov_map.py

Computes Lyapunov stability across parameter space.

Output:

- lyapunov_map.png

---

## nexah_kam_torus_detector.py

Identifies quasi-periodic regions resembling KAM tori.

Output:

- kam_torus_map.png
- kam_torus_candidates.json

---

## nexah_kam_surface_plot.py

Generates surface visualizations of KAM stability regions.

Output:

- kam_surface_plot.png

---

# Fractal Structure Analysis

## nexah_parameter_fractal_map.py

Visualizes fractal structures in parameter space.

Output:

- parameter_fractal_map.png

---

## nexah_fractal_dimension.py

Estimates fractal dimension of parameter space structures.

Output:

- fractal_dimension.png

---

# Universality Analysis

## nexah_feigenbaum_analysis.py

Searches for period-doubling cascades.

Output:

- feigenbaum_plot.png
- feigenbaum_estimate.json

---

## nexah_universality_detector.py

Attempts to detect universal scaling behavior in regime transitions.

Output:

- universality detection reports

---

# Summary

The NEXAH toolbox provides experimental analysis tools for exploring:

- resonance structures
- attractor landscapes
- frequency locking
- chaotic regions
- fractal parameter boundaries
- universality phenomena

These tools extend the kernel from a structural navigation engine into a **dynamical systems exploration environment**.
