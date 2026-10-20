# PENT-06 — Pascal edge growth / dynamic boundary test

Date: `2026-10-10`

Status: `PASS_WITH_BOUNDARY / BOUNDED_CANDIDATE_EVIDENCE / NOT_ADMITTED`

## Question

Can the verified depth-six Pascal faces be grown one compatible open edge at a
time, with the boundary treated as state, and can the existing NEXAH
`C5 + C6 + C6` material be retained as a typed comparator without identifying
it with the Pascal carrier?

## Contract A — face growth and closure

Start with one depth-six Pascal triangle. Attach each new triangle along the
current right radial seam, reversing the seam orientation. Both seam chains
carry weight `1`, so the quotient is weight-compatible.

For `f = 1..5` before cyclic closure:

```text
N_open(f) = 28 + 21(f-1) = 21f + 7
B_open(f) = f + 2
chi = V - E + F = 1
```

Each attachment consumes one open carrier edge and exposes two: the new outer
base edge and the next radial edge. Thus the boundary is part of the current
state, not a permanent frame.

The five-face preclosure state has `112` Pascal nodes and `7` carrier boundary
edges. Closing the last radial seam identifies its six non-apex lattice nodes,
recovering the already verified `106`-node carrier and its five-edge outer
pentagonal boundary.

## Contract B — 5/6 clock control

The regular pentagon and regular hexagon share a minimal `30`-step angular
raster:

```text
pentagon anchors: 0, 6, 12, 18, 24
hexagon anchors:  0, 5, 10, 15, 20, 25
step angle:       12 degrees
shared anchor:    0 mod 30
```

This verifies the familiar `72° - 60° = 12°` phase walk and exact realignment
after `360°`. Adding a second hexagon does not change the least common period
unless a separate phase map is declared.

## Existing Core comparator — one pentagon, two hexagons

The archived Symmetry Graph material already declares:

```text
C5 + C6 + C6 = 17 shell nodes
```

Its source implementation has three disjoint cycles without the hub
(`17` nodes, `17` edges, `3` components). With the declared center connected
to every shell node it has `18` nodes, `34` edges and one component. Therefore
the exact structural statement presently available is:

> the archived pentagon and two hexagons are coupled by a common hub.

That is not the same operation as gluing Pascal faces along a full seven-node
edge. The archived result summary also reports that rapid synchronization was
not specific to the `5+6+6` partition; the dominant tested factor was the
hub-cycle topology.

Source fixtures:

- `EXPERIMENTAL/BUILDER_LAB/ARCHIVE_ENGINE/archived/research/experiments/symmetry_graph_experiment/symmetry_graph_3cycle.py`
- `EXPERIMENTAL/BUILDER_LAB/ARCHIVE_ENGINE/archived/research/experiments/symmetry_graph_experiment/symmetry_graph_no_hub_experiment.py`
- `EXPERIMENTAL/BUILDER_LAB/ARCHIVE_ENGINE/archived/research/experiments/RESULT_SUMMARY_Symmetry_Graph_Experiment.md`

## Result

- face-by-face Pascal growth: `PASS`;
- dynamic carrier-boundary accounting: `PASS`;
- five-face closure back to `106` nodes: `PASS`;
- `C5/C6` 30-step clock control: `PASS`;
- historical `C5 + C6 + C6` topology reconstruction: `PASS`;
- map from that historical topology to the Pascal carrier:
  `UNDEFINED_NO_INTERTWINER`.

Also, `106 != 13 * 8`; exactly `13 * 8 = 104`, so the observed arithmetic is
`106 = 13 * 8 + 2`. No structural role for that remainder is introduced here.

Replay:

```sh
python3 run_test.py
```

## Boundary

This test establishes a finite combinatorial growth grammar and two explicit
controls. It does not establish resonance, a physical mechanism, a universal
dynamic-boundary law, a canonical Family, or an identification of the archived
`C5 + C6 + C6` oscillator fixture with the `106`-node Pascal quotient. Such an
identification requires a separately declared map that preserves specified
nodes, edges, weights and operators.
