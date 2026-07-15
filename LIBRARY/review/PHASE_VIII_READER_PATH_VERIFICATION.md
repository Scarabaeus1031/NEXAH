# Phase VIII — Reader Path Verification

**Live check:** `2026-07-15T21:28:52+00:00`  
**Rule:** only a direct public Channel connection counts as walkable.

## Beginner

| Transition | Current | Manual action |
|---|---|---|
| START → Visitor’s Guide | present | retain; keep visible at entrance |
| Visitor’s Guide → Language Book | missing | ACQ-002 · `Beginner →` |
| Language Book → Geometria Nova | missing | ACQ-003 · `Continue →` |
| Geometria Nova → Language Atlas | missing | ACQ-004 · `Continue →` |
| Language Atlas → Operator’s Handbook | missing | ACQ-005 · `Practice →` or `Continue →` |

Reader intent: orientation → vocabulary → foundation → visual map → practice.
START does not consume a Work slot.

## Builder

| Transition | Current | Manual action |
|---|---|---|
| START → Operator | missing | ACQ-006 · `Builder Path →` |
| Operator → Operator Map | missing | ACQ-007 · `Continue →` |
| Operator Map → Operator’s Handbook | missing | ACQ-008 · `Continue →` |
| Operator’s Handbook → Cartography Laboratory | missing | ACQ-009 · `Continue →` |
| Cartography Laboratory → Librarybook | missing | ACQ-010 · `Continue →` |

Reader intent: foundation → visual bridge → practice → research environment →
working synthesis. Operator Library remains an optional `Reference →` branch
from the Handbook and must not interrupt the main route.

## Research

| Transition | Current | Manual action |
|---|---|---|
| Field Atlas I → Field Atlas II | missing | ACQ-011 · `Next Volume →` |
| Field Atlas II → Field Atlas III | missing | ACQ-012 · `Next Volume →` |
| Field Atlas III → Operational Geometry | missing | ACQ-014 · `Bridge →` |
| Operational Geometry → Mathematica I | missing | ACQ-015 · `Continue →` |
| Mathematica I → Living Equation | missing | ACQ-016 · `Continue →` |

Reader intent: field observation → agency → morphology → geometric bridge →
formal research → synthesis. Do not remove Operational Geometry or recommend a
direct Morphology → Mathematica jump without explaining the domain change.

## Verification after each manual batch

1. Run live Traversability for the affected journey.
2. Confirm the new item is a Channel connection, not only title text.
3. Confirm the label is visible beside or directly before the connection.
4. Confirm no unrelated block was deleted or reordered accidentally.
5. Update the corresponding ACQ item to `completed` only through a reviewed repo
   edit after the public connection is observed.
