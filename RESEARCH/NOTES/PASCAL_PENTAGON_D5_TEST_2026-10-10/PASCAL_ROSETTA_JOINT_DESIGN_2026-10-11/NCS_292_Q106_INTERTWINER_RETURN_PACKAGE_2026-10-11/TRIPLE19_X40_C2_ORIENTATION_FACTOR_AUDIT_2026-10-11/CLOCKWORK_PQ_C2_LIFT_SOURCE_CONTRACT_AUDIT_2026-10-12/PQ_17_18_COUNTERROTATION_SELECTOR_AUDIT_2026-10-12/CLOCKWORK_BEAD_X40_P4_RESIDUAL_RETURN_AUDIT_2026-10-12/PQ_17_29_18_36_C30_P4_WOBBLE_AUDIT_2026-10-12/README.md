# P/Q 17→29 and 18→36 · C30 counter-step / P4 wobble audit

This bounded audit tests the Human Owner's candidate extension of the existing
Clockwork bead/X40 Return contract:

```text
P: 17 → 29 = prime P10
Q: 18 → 36 = 3×6 → 6×6 = 2²×3²
wobble: one extra tag every four positions
```

The two increments are complementary in `C30`:

```text
29 − 17 = 12 = 6×2
36 − 18 = 18 = 6×3 ≡ −12 (mod 30)
```

On the embedded `C5` address set `6·C5⊂C30`, these are the opposite generator
steps `+2` and `−2`. The two observed pairs are also mirror addresses:

```text
17 ≡ +2, 18 ≡ −2 (mod 5)
29 ≡ −1, 36 ≡ +1 (mod 5)
```

Therefore the new numbers are compatible with the already bound P/Q
counter-rotation and same-index mirror contract. They select phase chart `k=0`
only if the additional numeric-address convention is declared:
`P(n)=n mod 5`, `Q(n)=−n mod 5`. Without that convention the five global
phase charts remain equivalent.

## Wobble distinction

- A full tag `p=t mod 4` is exactly a `P4` coordinate and closes the four-state
  fibre left by the ten-bead display.
- A pulse `w=1[t mod 4=0]` is only binary. Its fibres have sizes `1` and `3`, so
  it cannot reconstruct `P4` by itself.

The audit records both readings instead of silently strengthening “every
fourth” into a four-valued state.

## Boundary

This is an Owner-declared finite arithmetic/address contract. It does not
recover a historical Clockwork encoding, prove that a GLB wobble stores `P4`,
define X20 adjacency, create a Q106 intertwiner, identify a physical mechanism,
admit a Study, modify A0 evidence or authorize publication.

Run:

```bash
python3 verify_pq_17_29_18_36_c30_p4_wobble.py
```

The source-binding follow-up in
[`ROOT40_FIBONACCI_C30_P4_SOURCE_BINDING_AUDIT_2026-10-12`](ROOT40_FIBONACCI_C30_P4_SOURCE_BINDING_AUDIT_2026-10-12/README.md)
binds the existing 15/15 Root-40/Fibonacci result, recovers a compatible
`C5×C6≅C30` schedule and leaves the four-slot-to-four-role P4 map null.
