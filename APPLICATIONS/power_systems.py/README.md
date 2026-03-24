# IEEE Test Systems in NEXAH

Application: Stability Analysis of Real Power Grid Benchmarks

This module introduces IEEE test systems as a first real-world application of the NEXAH framework.

---

## What this module does

We use standard IEEE power grid models (starting with the 14-bus system) and perform a simple experiment:

Gradually increase system load and observe when the grid becomes unstable.

At each step:
- power flow is computed
- system stability is evaluated (convergence vs collapse)

---

## Why IEEE test systems?

IEEE test systems (14, 30, 57, 118 bus) are widely used benchmarks in power systems research.

They provide:
- realistic network topology
- well-defined load and generation profiles
- a standard reference for stability analysis

---

## First goal (Phase 1)

Detect the stability boundary of the IEEE 14-bus system.

Result:
- below threshold → system stable
- above threshold → collapse (no convergence)

---

## Run the demo

```bash
cd APPLICATIONS/p
