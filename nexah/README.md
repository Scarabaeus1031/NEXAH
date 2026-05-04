# ARCHIVE_KERNEL

## Purpose

This directory contains historical and experimental versions of NEXAH.

These are NOT part of the active kernel.

---

## Paradigms

### 1. Field Paradigm

- continuous dynamics
- vector fields
- geometry (basins, separatrix)
- flow-based control

Status:
experimental, not stabilized

---

### 2. Transition Paradigm

- discrete states
- transition probabilities
- navigation via graph
- intervention via transition shaping

Status:
→ ACTIVE (see nexah/core.py)

---

## Important

Do not mix paradigms.

The active system is:

→ transition-based kernel (v0.7)
