# NEXAH Stability Engine — Visual Gallery

This gallery presents the visual outputs produced by the **NEXAH Stability Engine**.

All images are generated automatically by:

ENGINE/run_stability_engine.py

Location of images:

ENGINE/visuals/

The visual pipeline reveals the **geometric, dynamical, and topological structure of stability landscapes**.

---

# Stability Landscape

![Landscape](ENGINE/visuals/01_landscape.png)

The base stability landscape Z = f(x,y).

This surface defines the global stability structure of the system.  
All subsequent analyses operate on this field.

Module  
stability_landscape_generator.py

---

# Gradient Field

![Gradient Field](ENGINE/visuals/02_gradient_field.png)

The gradient field ∇f(x,y) describes the direction of steepest ascent or descent.

It determines how trajectories evolve across the stability landscape.

Module  
stability_gradient_field.py

---

# Hessian Field

![Hessian Field](ENGINE/visuals/03_hessian_field.png)

Second-order curvature information derived from the Hessian matrix.

The Hessian reveals whether regions of the landscape are locally convex or concave.

Module  
stability_hessian_field.py

---

# Critical Points

![Critical Points](ENGINE/visuals/04_critical_points.png)

Locations where the gradient vanishes.

Three types appear:

Red — maxima  
Blue — minima  
White — saddle points

These points form the **structural anchors of the stability landscape**.

Module  
stability_critical_points.py

---

# Basin Segmentation

![Basin Segmentation](ENGINE/visuals/05_basin_segmentation.png)

Partition of the landscape into attraction basins.

Every point inside a basin converges toward the same attractor.

Module  
stability_basin_segmentation.py

---

# Basin Transition Graph

![Basin Graph](ENGINE/visuals/06_basin_transition_graph.png)

Graph representation of attractor connectivity.

Nodes represent attractors.  
Edges represent possible transitions between basins.

Module  
basin_transition_graph.py

---

# Metastability Map

![Metastability](ENGINE/visuals/07_metastability_map.png)

Regions where trajectories may temporarily reside before escaping.

These areas indicate **metastable structures** and possible tipping points.

Module  
metastability_map.py

---

# Global Stability Structure

![Global Structure](ENGINE/visuals/08_global_structure.png)

Combined representation of:

- basins
- critical points
- transition structure

This visualization summarizes the global topology of the system.

Module  
global_stability_structure.py

---

# Phase Portrait

![Phase Portrait](ENGINE/visuals/09_phase_portrait.png)

Vector field representation of dynamic flow behavior.

Shows how trajectories move across the stability field.

Module  
stability_phase_portrait.py

---

# Information Geometry

![Information Geometry](ENGINE/visuals/10_information_geometry.png)

Geometric representation derived from information-theoretic structure.

Highlights curvature and complexity in the stability landscape.

Module  
stability_information_geometry.py

---

# Morse Complex

![Morse Complex](ENGINE/visuals/11_morse_complex.png)

Topological decomposition of the landscape based on Morse theory.

Critical points and gradient flows form cells of the Morse complex.

Module  
stability_morse_complex.py

---

# Persistence Diagram

![Persistence Diagram](ENGINE/visuals/12_persistence_diagram.png)

Persistent homology diagram.

Each point represents a topological feature appearing and disappearing
across filtration levels.

Module  
stability_persistence_homology.py

---

# Persistence Barcodes

![Persistence Barcodes](ENGINE/visuals/13_persistence_barcodes.png)

Barcode representation of persistent homology.

Each bar corresponds to a topological feature across scales.

Module  
stability_persistence_homology.py

---

# Persistent Features

![Persistent Features](ENGINE/visuals/14_persistent_features.png)

Visualization of the most stable topological structures detected in the landscape.

These features represent dominant structural patterns.

Module  
stability_persistence_homology.py

---

# Eigenmodes

![Eigenmodes](ENGINE/visuals/15_eigenmodes.png)

Eigenmode decomposition of the stability operator.

Reveals dominant spatial patterns in the system.

Module  
stability_eigenmodes.py

---

# Koopman Spectrum

![Koopman Spectrum](ENGINE/visuals/16_koopman_spectrum.png)

Approximation of the Koopman operator spectrum.

Provides a linear representation of nonlinear dynamics.

Module  
stability_koopman_operator.py

---

# Lyapunov Spectrum

![Lyapunov Spectrum](ENGINE/visuals/17_lyapunov_spectrum.png)

Estimated Lyapunov exponents describing trajectory divergence.

Positive exponents indicate chaotic tendencies.

Module  
stability_lyapunov_spectrum.py

---

# Diffusion Map

![Diffusion Map](ENGINE/visuals/18_diffusion_map.png)

Low-dimensional embedding derived from diffusion geometry.

Reveals intrinsic manifold structure within the landscape.

Module  
stability_diffusion_map.py

---

# Wasserstein Geometry

![Wasserstein Geometry](ENGINE/visuals/19_wasserstein_geometry.png)

Comparison between two landscapes using optimal transport distance.

Quantifies structural difference between stability fields.

Module  
stability_wasserstein_geometry.py

---

# Topological Skeleton

![Topological Skeleton](ENGINE/visuals/20_topological_skeleton.png)

Graph connecting critical points via gradient flow trajectories.

This structure represents the **global wiring diagram of the stability landscape**.

Module  
stability_topological_skeleton.py

---

# Summary

The NEXAH Stability Engine extracts the structural layers of a stability system:

• geometric landscape structure  
• gradient dynamics  
• basin topology  
• spectral decomposition  
• topological invariants  
• optimal transport geometry  

Together these analyses reveal the **hidden architecture of complex stability landscapes**.

---

# NEXAH Stability Engine

Structural computation for stability, dynamics, and complex systems.
