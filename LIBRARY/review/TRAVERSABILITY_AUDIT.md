# NEXAH Library — Traversability Audit

**Public Are.na · read-only observation · 2026-07-15**

This audit asks two separate questions: does a transition make editorial sense,
and can a reader follow it through a direct public Channel connection? A Work
being searchable on Are.na does not count as a clickable transition.

No Are.na content was changed. The audit combines the earlier public-interface
walkthrough with read-only `GET /channels/{id}/contents` observations.

## Result

| Journey | Curated transitions | Direct links present | Direct links missing |
|---|---:|---:|---:|
| Beginner | 5 | 1 | 4 |
| Builder | 5 | 0 | 5 |
| Research | 5 | 0 | 5 |
| **Total** | **15** | **1** | **14** |

The Library has coherent conceptual paths, but those paths are not yet public
walking routes. Only `START → THE VISITOR’S GUIDE` is currently represented by
a direct Channel connection.

## Beginner Journey

| From → To | Conceptual | Clickable | Reader friction | Manual action |
|---|---|---|---|---|
| START → Visitor’s Guide | confirmed | present | none at transition | retain and label as primary entry |
| Visitor’s Guide → Language Book | confirmed | missing | reader must return to search | add Continue connection |
| Language Book → Geometria Nova | confirmed | missing | learning order is not walkable | add Continue connection |
| Geometria Nova → Language Atlas | confirmed | missing | model does not route to visual map | add Continue connection |
| Language Atlas → Operator’s Handbook | confirmed | missing | map does not route to practice | add Continue connection |

## Builder Journey

| From → To | Conceptual | Clickable | Reader friction | Manual action |
|---|---|---|---|---|
| START → Operator | confirmed | missing | builder entrance is invisible | add Builder Path connection |
| Operator → Operator Map | confirmed | missing | bridge map is not reachable | add Continue connection |
| Operator Map → Operator’s Handbook | confirmed | missing | map does not route to practice | add Continue connection |
| Operator’s Handbook → Cartography Laboratory | confirmed | missing | practice does not route to research environment | add Continue connection |
| Cartography Laboratory → Librarybook | confirmed | missing | laboratory does not route to synthesis | add Continue connection |

The Operator Library remains a reference branch and is intentionally not placed
inside this main sequence.

## Research Journey

| From → To | Conceptual | Clickable | Reader friction | Manual action |
|---|---|---|---|---|
| Field Atlas I → Field Atlas II | confirmed | missing | Series order is not walkable | add Next Volume connection |
| Field Atlas II → Field Atlas III | confirmed | missing | Series order is not walkable | add Next Volume connection |
| Field Atlas III → Operational Geometry | confirmed bridge hypothesis | missing | domain bridge is invisible | add Bridge connection |
| Operational Geometry → Mathematica I | confirmed | missing | bridge does not route into formal research | add Continue connection |
| Mathematica I → Living Equation | confirmed | missing | formal research does not route to synthesis | add Continue connection |

## Interpretation

`conceptual_status` records editorial judgment. `clickable_status` records only
what the public Channel contents expose. Neither one implies the other. The
missing links are manual editorial tasks, not Registry defects and not grounds
for automatic Are.na writes.
