# NEXAH IEEE X-Ray Pipeline

Structural projection of power system dynamics into a geometric state space.

## Overview

The IEEE X-Ray Pipeline is the experimental development environment for the NEXAH power-system framework.

Its purpose is to transform classical power-system simulations into a low-dimensional structural representation that can be analyzed geometrically.

Core transformation:

    simulation
        ↓
    feature extraction
        ↓
    state-space reconstruction
        ↓
    geometric analysis
        ↓
    experimental control

---

## Main Goals

- identify structural precursors of instability
- reconstruct system trajectories in state space
- analyze stability as geometry rather than thresholds
- explore trajectory-based control concepts

---

## Repository Structure

    README.md
    visual-gallery.md

    pipeline_versions/
        Historical pipeline and controller versions

    results/
        Generated figures, reports, and experiment outputs

    archive/
        Experimental history and supporting concepts

---

## Development History

The pipeline evolved through several stages:

### Structure Discovery
- v1–v13
- state-space extraction
- geometric interpretation of dynamics

### Experimental Controllers
- v14 series
- stabilization and orbit-control experiments

### Root Cube Navigation
- v15–v39
- 3D geometric representations
- navigation and field concepts

### Attractor & Aperture Dynamics
- v40–v56
- attractor regions
- sector transitions
- event-driven navigation

---

## Current Status

### Structural Analysis

Functional.

The pipeline consistently produces low-dimensional state-space representations and identifies structural patterns associated with instability.

### Control & Navigation

Experimental.

Trajectory shaping, attractor dynamics, and transition control have been explored, but robust navigation and stable multi-regime control remain open research topics.

---

## Related Documents

- visual-gallery.md
- archive/experimental_history/
- archive/symbolic_concepts/

---

## NEXAH Principle

    simulation
        ↓
    structure
        ↓
    geometry
        ↓
    dynamics
        ↓
    navigation
