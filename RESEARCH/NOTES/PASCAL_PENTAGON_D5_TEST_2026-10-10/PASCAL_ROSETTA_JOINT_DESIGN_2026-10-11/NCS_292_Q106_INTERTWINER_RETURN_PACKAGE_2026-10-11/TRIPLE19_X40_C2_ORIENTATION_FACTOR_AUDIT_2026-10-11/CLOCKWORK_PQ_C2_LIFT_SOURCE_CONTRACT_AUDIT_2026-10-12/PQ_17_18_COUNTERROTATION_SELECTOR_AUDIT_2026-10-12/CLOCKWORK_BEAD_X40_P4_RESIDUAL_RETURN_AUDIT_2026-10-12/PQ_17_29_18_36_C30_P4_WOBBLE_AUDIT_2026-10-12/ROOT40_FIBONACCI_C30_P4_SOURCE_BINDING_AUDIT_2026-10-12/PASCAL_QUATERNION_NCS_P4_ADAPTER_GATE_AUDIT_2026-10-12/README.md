# Pascal-quaternion → NCS P4 adapter gate audit

This bounded audit performs the adapter test left open by the Root-40 /
Fibonacci correction. It reuses the existing A0 Pascal-quaternion evidence and
the declared NCS carrier; it creates no new scientific or Navigator identity.

## Result

The four Pascal slots and four NCS roles admit `4!=24` static bijections. Every
one has an exact set-theoretic inverse, so all 24 can serve as a declared
address encoding.

None is an operator intertwiner under the currently declared actions:

```text
Pascal: gamma = (scalar)(i j k)
NCS P4: id = (carrier)(frame_cut)(transform_view)(return_record)
```

Cycle type is invariant under relabelling. A permutation of type `(1)(3)`
cannot be conjugate to the identity `(1)(1)(1)(1)`. Exhaustive enumeration
therefore returns zero operator-equivariant adapters.

Transporting the Pascal action through a chosen bijection produces eight
possible target `C3` actions: one for each choice of fixed NCS role and each
orientation of the remaining three-role cycle. Each such action admits three
equivariant bijections. But none of those eight actions is currently an NCS
source law.

## Decision

```text
STATIC ADDRESS ADAPTERS                     24
EXACT ADDRESS RETURN                        24
PASCAL-C3 → DECLARED-NCS-IDENTITY ADAPTERS   0
CANONICAL NCS P4 ADAPTER                  null
```

The intuitive assignment
`scalar→carrier, i→frame_cut, j→transform_view, k→return_record` is retained as
an unprivileged lexical candidate. It also fails the operator-intertwiner gate.

The minimal new source input is either:

- a complete declared four-slot-to-role map; or
- an NCS role action of cycle type `(1)(3)` plus one typed slot-to-role anchor.

Root-40 remains outside the Pascal `Phi` image. The full wobble tag remains a
four-address carrier without role semantics. No X20 adjacency, Q106
intertwiner, historical NCS mechanism or physical claim follows.

Run:

```bash
python3 verify_pascal_quaternion_ncs_p4_adapter.py
```
