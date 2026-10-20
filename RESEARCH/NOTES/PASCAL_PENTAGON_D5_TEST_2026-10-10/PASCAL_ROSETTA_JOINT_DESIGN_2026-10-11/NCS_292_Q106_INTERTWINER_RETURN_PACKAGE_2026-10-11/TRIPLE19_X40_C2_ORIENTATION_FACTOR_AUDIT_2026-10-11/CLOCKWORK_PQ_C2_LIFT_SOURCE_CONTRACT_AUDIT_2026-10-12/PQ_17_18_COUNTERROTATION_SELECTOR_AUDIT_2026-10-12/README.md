# P/Q–17/18 counter-rotation selector audit

This bounded formal audit tests whether the Owner-declared ordered bridge
`P -> 17`, `Q -> 18` can label the otherwise unlabeled Clockwork/NCS `C2`
display lift.

The test combines only three declared operations:

1. the source-bound Clockwork turns `P:+1`, `Q:-1`;
2. integer parity `e(n)=n mod 2` on the candidate registers 17 and 18; and
3. the sign encoding `turn=2e-1`.

If all three agree, the ordered candidate selects
`e=1 <-> P <-> 17 <-> +1` and
`e=0 <-> Q <-> 18 <-> -1`.

The reverse assignment is retained as a control. It is equally compatible
with counter-rotation after reversing the sign convention, so the unordered
set `{17,18}` alone cannot select P/Q. PENT-07 and A0-BL-035 remain negative
controls: neither supplies this selector.

## Boundary

Passing this audit establishes a **conditional, Owner-declared labeling
contract**. It does not recover the ordered assignment from historical source
material, choose `J_c` versus `J_d`, create X20 adjacency, map GLB nodes to
X20, produce a Q106 intertwiner, admit a new Study, modify A0 evidence or
authorize publication.

Run:

```bash
python3 verify_pq_17_18_selector.py
```

