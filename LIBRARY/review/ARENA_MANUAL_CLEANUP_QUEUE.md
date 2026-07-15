# NEXAH Library — Manual Are.na Cleanup Queue

**Human-executable only · no automatic write authorized**

The YAML queue is authoritative for local review state. IDs are stable and must
never be renumbered. `cleanup-status` reads this queue but cannot modify it.

## P0

| ID | State | Affected Channel | Manual action |
|---|---|---|---|
| ACQ-001 | pending | START | Improve visibility of the designed entrance. |
| ACQ-002 | pending | THE VISITOR’S GUIDE | Add the four orientation links; mark Language Book as beginner continuation. |
| ACQ-013 | pending | FIELD ATLAS III — MORPHOLOGY | Remove only the confirmed editorial residue. |

## P1 — Beginner and Builder links

| ID | State | Affected Channel | Manual action |
|---|---|---|---|
| ACQ-003 | pending | THE LANGUAGE BOOK | Continue → GEOMETRIA NOVA |
| ACQ-004 | pending | GEOMETRIA NOVA | Continue → THE LANGUAGE ATLAS |
| ACQ-005 | pending | THE LANGUAGE ATLAS | Continue → THE OPERATOR’S HANDBOOK |
| ACQ-006 | pending | START | Builder Path → THE OPERATOR |
| ACQ-007 | pending | THE OPERATOR | Continue → THE OPERATOR MAP |
| ACQ-008 | pending | THE OPERATOR MAP | Continue → THE OPERATOR’S HANDBOOK |
| ACQ-009 | pending | THE OPERATOR’S HANDBOOK | Continue → THE CARTOGRAPHY LABORATORY |
| ACQ-010 | pending | THE CARTOGRAPHY LABORATORY | Continue → LIBRARYBOOK |

## P1 — Research links

| ID | State | Affected Channel | Manual action |
|---|---|---|---|
| ACQ-011 | pending | FIELD ATLAS I — WATER | Next Volume → FIELD ATLAS II |
| ACQ-012 | pending | FIELD ATLAS II — THE ARCHITECTURE OF AGENCY | Next Volume → FIELD ATLAS III |
| ACQ-014 | pending | FIELD ATLAS III — MORPHOLOGY | Bridge → Operational Geometry |
| ACQ-015 | pending | Operational Geometry | Continue → NEXAH MATHEMATICA I |
| ACQ-016 | pending | NEXAH MATHEMATICA I | Continue → THE LIVING EQUATION |

## State policy

Allowed states are `pending`, `accepted`, `completed`, `deferred`, and
`rejected`. A human editor changes state only through an explicit repository
edit of `arena_manual_cleanup_queue.yaml`. Completion never triggers an Are.na
action.
