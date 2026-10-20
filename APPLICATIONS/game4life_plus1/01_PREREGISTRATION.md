# LIFE08 — Frozen Boundary Cylinder Protocol

Status: `FROZEN_BEFORE_EXECUTION`

The exact machine-readable protocol is `PREREGISTRATION.json`. The primary
comparison holds the rule, schedule, grid sizes and initial states fixed while
changing only the declared boundary operator.

The Study separates:

1. **view wrap** — a planar state is drawn on a cylinder without changing its
   neighbours;
2. **dynamics wrap** — the neighbour operator identifies one axis;
3. **Return comparison** — state, event counts, event sets, connectivity and
   seam activity are compared without forcing identity.

The quaternion-valued event register is a reversible representation only:

```text
Phi(B,S,D) = (B+S+D)1 + B i + S j + D k.
```

It does not make event-channel permutation a Life symmetry and does not import
the Pascal carrier into Life.

