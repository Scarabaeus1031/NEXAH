# MESO Layer – Field Construction Layer

MESO is the layer that transforms discrete regimes (from ARCHY) into a **continuous structured stability field**.

It is the bridge between abstract regime theory and geometric navigation (NEXAH).

---

## Purpose

MESO is responsible for:
- Constructing the continuous stability field from system dynamics
- Defining and computing the Coherence metric
- Building the Risk Field and stability landscape
- Providing the geometric foundation for trajectory-aware control and navigation

---

## Core Concepts

- **Coherence**: Measures alignment between system velocity and the underlying field
- **Risk Field**: Continuous scalar representation of instability risk
- **Stability Landscape**: Geometric structure of safe and unsafe regions in state space
- **Field Structure**: Attractors, basins, phase space, tipping points, and collapse boundaries

---

## Current Structure

- `core/` — Fundamental field construction (risk_geometry, stability_landscape)
- `structure/` — Field structures (attractors, basins, phase space)
- `transitional/` — Early warning and tipping point logic
- `visuals/` — Visualization scripts (temporary)
- `docs/` — Documentation

---

## Connection to Other Layers

- **ARCHY** provides discrete regimes and transitions
- **MESO** converts them into continuous, measurable fields
- **NEXAH** uses the resulting field geometry for navigation and control
- **MEVA** applies field dynamics to multi-agent behavior

MESO is the **critical translation layer** from discrete structure to continuous geometry.

---

## Current Status

MESO is still heavily overloaded with experimental scripts, visualizations, and application-specific code.  
The true field construction core is being isolated.  
Many files will be moved to BUILDER_LAB or APPLICATIONS in a later phase.

**Goal:** Make MESO a clean and focused "Field Construction Layer".

---

**Last updated:** April 2026
