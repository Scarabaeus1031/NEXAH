# ARCHY Layer – Regime & Dynamics Layer

The ARCHY layer is responsible for **regime theory, regime transitions, and system dynamics**.

It sits between the abstract relational principles (META) and the measurable field construction (MESO).

---

## Purpose

ARCHY defines:
- What a **regime** is and how regimes are formed
- How systems transition between different regimes (using the Δ operator)
- Stability structures and dynamical behavior within and between regimes

ARCHY turns the relational order from META into concrete dynamical concepts.

---

## Current Structure

- `core/` — Core regime logic and operators
  - `regime_mapper.py`
  - `stability_models/` (delta_operator, stability_index, hybrid_coherence, etc.)
- `docs/` — Architecture and principles documentation

---

## Connection to Other Layers

- **META** provides the minimal relational axioms (A0–A4)
- **MESO** translates regimes into continuous fields and coherence metrics
- **NEXAH** uses regime transitions and stability structures for geometric navigation and control
- **MEVA** applies regime dynamics to multi-agent and emergent behavior

ARCHY is the **bridge layer** that makes abstract relational order dynamically usable.

---

## Status

The core regime mapping and transition logic is in place.  
Large application models (planet/, urban/, etc.) and experimental tools are still present in this folder but will be moved to BUILDER_LAB or APPLICATIONS in a later phase.

**Goal:** Keep ARCHY focused as the clean "Regime & Dynamics Layer".

---

**Last updated:** April 2026
