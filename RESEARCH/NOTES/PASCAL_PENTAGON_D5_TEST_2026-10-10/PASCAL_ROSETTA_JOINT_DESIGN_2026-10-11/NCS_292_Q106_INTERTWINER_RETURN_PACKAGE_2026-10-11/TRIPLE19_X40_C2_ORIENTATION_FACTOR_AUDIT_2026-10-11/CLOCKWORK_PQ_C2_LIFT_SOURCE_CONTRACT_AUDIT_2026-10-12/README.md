# Clockwork P/Q · NCS C2 Lift Audit

Status: `FORMAL_DESIGN_VALIDATION_NOT_ADMITTED_NOT_PENT_08`

This bounded audit connects the already registered Clockwork v7 source to the
existing NCS/Triple-19 C2 factor without creating a new identity.

It asks whether the `p/q` conjugate paths give a faithful two-sheet display of
the orientation coordinate erased by `X40 -> X20`. It separately asks whether
the source selects which sheet is bit `0` and which is bit `1`.

Run:

```bash
python3 verify_clockwork_pq_c2_lift.py
```

Expected bounded result:

```text
X40 ≅ X20 x C2
          |
          | two admissible global labelings
          v
L_PQ = X20 x {p,q}

quotient / display projection forgets the same two-valued coordinate
```

The output does not supply X20 edges, a Triple-19-to-X20 map, a Q106
intertwiner, a canonical Janus law, or A0 evidence authority.
