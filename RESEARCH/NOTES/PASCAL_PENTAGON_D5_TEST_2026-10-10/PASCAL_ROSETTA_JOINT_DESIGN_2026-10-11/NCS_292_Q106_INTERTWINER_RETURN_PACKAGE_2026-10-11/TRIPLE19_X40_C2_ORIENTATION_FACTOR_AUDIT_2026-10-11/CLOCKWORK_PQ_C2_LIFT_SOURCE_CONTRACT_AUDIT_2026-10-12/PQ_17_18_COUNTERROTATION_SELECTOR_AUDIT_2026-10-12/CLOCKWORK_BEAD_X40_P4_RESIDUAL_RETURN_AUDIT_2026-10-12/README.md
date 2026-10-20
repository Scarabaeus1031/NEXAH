# Clockwork bead → X40/P4 residual Return audit

This bounded formal audit attaches the ten source-bound Clockwork transfer
beads to the declared NCS carrier

```text
X40 = C5 × P4 × C2
```

without pretending that ten GLB nodes are forty carrier states.

The preceding Owner-declared selector fixes `P↔e=1` and `Q↔e=0`. The GLB
supplies five indexed P beads, five indexed Q beads, opposite turns and the
same-index mirror relation. The audit tests all five possible global C5 phase
offsets rather than silently selecting one.

For chart offset `k∈C5` the display map is

```text
d_k(s,p,1) = P bead (s+k)
d_k(s,p,0) = Q bead (-s+k)
```

The sign reversal on the Q sheet is required by counter-rotation. Every bead
has a four-state P4 fibre. Exact Return therefore requires the two-bit package
residual `p∈P4` after a global phase chart has been declared.

## Boundary

The same-index P/Q mirror flip realizes the dihedral candidate `Jd` on the
displayed `C5×C2` quotient and rejects `Jc` there. This is a conditional
selection inside the declared bead-index/action contract. The five global
phase charts remain equivalent, no historical phase origin is recovered, and
no X20 adjacency, Q106 intertwiner, GLB-to-Q106 node map, physical orbit,
admitted Study or publication authority follows.

Run:

```bash
python3 verify_clockwork_bead_x40_return.py
```

