# NEXAH Experimental Results

This document summarizes key dynamical structures observed in the NEXAH regime landscape experiments.

The goal is not to claim formal results, but to document **empirical observations emerging from parameter scans and simulations**.

These results are generated using the analysis tools in:

```
ENGINE/nexah_kernel/tools
```

and visualized in:

```
ENGINE/nexah_kernel/demos/visuals/resonance_landscape
```

---

# 1 Resonance Landscapes

Large parameter scans over structural symmetry and drift parameters produce structured resonance landscapes.

Typical parameter space:

(n, drift)

where

n = symmetry order  
drift = dynamic drift parameter  

These scans produce maps revealing:

- resonance zones
- attractor regions
- chaotic bands
- quasiperiodic islands

Example visual output:

```
resonance_landscape.png
```

---

# 2 Attractor Structures

Analysis of resonance fields reveals discrete attractor structures.

Example experiment:

```
nexah_resonance_attractor_finder.py
```

Typical result:

- dozens of localized attractors
- stable resonance centers
- basin structures surrounding attractors

Example output:

```
resonance_attractors_map.png
```

Observed example:

```
Attractors found: 64
```

The repeated appearance of structured attractor counts suggests hidden resonance symmetries in the parameter space.

---

# 3 Arnold Tongue Structures

Frequency locking regions appear in resonance parameter scans.

These structures resemble classical **Arnold tongues** known from forced oscillator systems.

Characteristics observed:

- wedge-shaped locking regions
- rational rotation plateaus
- symmetry-dependent locking patterns

Generated using:

```
nexah_arnold_tongue_map.py
```

Output example:

```
arnold_tongues.png
```

---

# 4 Devil's Staircase Behavior

Rotation number analysis reveals step-like structures characteristic of the **Devil’s staircase**.

These plateaus correspond to frequency locking zones.

Tool:

```
nexah_devils_staircase.py
```

Example output:

```
devils_staircase.png
```

---

# 5 KAM-like Stability Regions

Some regions of parameter space display smooth quasiperiodic structures surrounded by chaotic areas.

These resemble **KAM tori** predicted by Kolmogorov–Arnold–Moser theory.

Tool:

```
nexah_kam_torus_detector.py
```

Example output:

```
kam_torus_map.png
kam_surface_plot.png
```

Observed behavior:

- smooth stability islands
- chaotic boundaries
- mixed phase space

---

# 6 Chaotic Regions

Lyapunov maps reveal chaotic bands separating stable regions.

Tool:

```
nexah_lyapunov_map.py
```

Example output:

```
lyapunov_map.png
```

Observed pattern:

- stable islands embedded in chaotic fields
- resonance-driven transitions
- chaotic corridors between attractor zones

---

# 7 Fractal Parameter Structure

Parameter scans reveal fractal boundaries between dynamical regimes.

Example:

```
nexah_parameter_fractal_map.py
```

Output:

```
parameter_fractal_map.png
fractal_dimension.png
```

Observed structures:

- fine-scale resonance filaments
- fractal regime boundaries
- nested resonance clusters

---

# 8 Universality Search

Experiments attempted to detect period-doubling cascades and Feigenbaum-like scaling.

Tools:

```
nexah_feigenbaum_analysis.py
nexah_universality_detector.py
```

Example output:

```
feigenbaum_plot.png
```

Preliminary observations:

- no clear period-doubling cascade detected
- possible transition portals between regime families
- universality behavior remains an open question

---

# 9 Resonance Ridge Structures

Resonance ridge detection reveals coherent high-energy structures in parameter space.

Tool:

```
resonance_ridge_detector.py
```

Output:

```
resonance_ridges.png
```

Observed patterns:

- ridge networks across symmetry orders
- ridge intersections acting as attractor hubs
- harmonic clustering of resonance zones

---

# 10 Visual Atlas

The NEXAH experiments produce a growing atlas of dynamical structures.

Example visual datasets:

- resonance landscapes
- Arnold tongue diagrams
- Lyapunov maps
- KAM surfaces
- fractal parameter maps
- attractor maps
- symmetry resonance atlases

These datasets collectively reveal the **geometry of dynamical regimes** in NEXAH systems.

---

# Interpretation

The repeated appearance of classical nonlinear structures suggests that NEXAH landscapes behave similarly to well-known dynamical systems such as:

- circle maps
- forced oscillators
- coupled phase systems
- nonlinear lattice models

However, in NEXAH these structures emerge from **structural graph dynamics rather than explicit oscillator equations**.

This suggests that graph topology may act as a generator of dynamical resonance landscapes.

---

# Open Questions

Key questions for further research include:

- Why do Arnold tongue structures appear in symmetry-drift parameter space?
- What determines the attractor counts in resonance scans?
- Can graph topology predict resonance ridge structures?
- Are there universality classes for structural regime landscapes?

Answering these questions is the central motivation of the NEXAH research program.

---

# NEXAH

Part of the **SCARABÆUS1033 research framework**, exploring structural navigation and resonance dynamics in complex systems.
