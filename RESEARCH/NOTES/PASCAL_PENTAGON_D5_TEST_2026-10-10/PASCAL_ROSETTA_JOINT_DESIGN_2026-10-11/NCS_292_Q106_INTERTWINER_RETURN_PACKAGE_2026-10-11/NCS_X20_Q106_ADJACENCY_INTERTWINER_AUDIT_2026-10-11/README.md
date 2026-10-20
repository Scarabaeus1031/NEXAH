# NCS X20 → Q106 adjacency intertwiner audit

Status: `PASS_UNDEFINED_CONTRACT_ADJACENCY_MISSING`  
Identity: extension of `A0-BL-023:NCS_292_Q106_INTERTWINER_RETURN_PACKAGE:V1`

## Result

The frozen Q106 carrier again yields one unique connected interface made from
four five-node D5 orbits. The interface has 20 undirected internal edges and
degree profile

```text
degree 1: 5 nodes
degree 2: 10 nodes
degree 3: 5 nodes.
```

The parent X20 record supplies 20 states and the C5 rotation, but no adjacency
or edge types. Consequently the graph-intertwiner question is not false; it is
not yet defined.

The audit narrows the remaining freedom:

- `15000` rotation-equivariant bijections exist;
- after declaring the candidate source reflection and frozen target
  reflection, `24` D5-equivariant bijections remain;
- no one of those 24 charts is canonical from the frozen sources;
- adjacency preservation cannot be evaluated until an independent `E_X` is
  supplied.

The generated `Q106_INTERFACE_COORDINATES.csv` is a target-side coordinate
chart only. It is not an asserted X20 mapping.

## Downstream effect

- `typed_intertwiner_to_q106` remains `null`;
- β remains open over 720 assignments;
- the historical Janus selection remains open;
- Triple-19 Pc/Pd compatibility remains open and explicitly related rather
  than identified;
- the arithmetic, prime-index, Lissajous, return and OIL/RIS source relations
  remain available to the Navigator crosswalk without promoting this result.

## Replay

From this directory:

```bash
python3 verify_x20_q106_intertwiner.py
```

The command rewrites `RESULT.json` and `Q106_INTERFACE_COORDINATES.csv`
deterministically.
