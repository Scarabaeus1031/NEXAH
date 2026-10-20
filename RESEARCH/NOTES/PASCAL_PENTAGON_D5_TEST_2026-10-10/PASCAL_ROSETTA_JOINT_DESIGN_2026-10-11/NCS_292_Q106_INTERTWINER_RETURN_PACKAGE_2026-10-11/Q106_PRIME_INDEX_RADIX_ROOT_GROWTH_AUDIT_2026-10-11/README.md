# Q106 Prime-Index · Radix Mirror · Root-Growth Audit

This bounded subtest reuses `A0OE:PASCAL_PENTAGON_D5_TEST` and the frozen
SCC-003/Q106 carrier. It creates no new Navigator identity and makes no
physical or publication claim.

## What is tested

1. The seven cumulative Q-level counts follow `Q_m=1+5T_m` and end at 106.
2. The `2–3–5` seed has three exact contacts: `2+3=5`, `2·3=6=Q_1`, and
   the fivefold coefficient of the growth law. `2/3=0.666…` is kept as a
   rational identity; it is not the integer 6. `2^3=8` is not found in the
   Q-sequence, while `Q_2=16=2^4`.
3. The frozen D5 orbit profile supplies `O=16` orbits and `F=9` five-orbits.
   The final level contains `L=25=O+F` interior nodes. Therefore the exact
   prime-index joint is `p_16=53`, `p_25=97`, `106=2·53`, `106-9=97`, and
   `53+97=150`.
4. No D5-invariant 53-node half exists.
5. Euclidean radix coordinates expose a real but coordinate-dependent
   20→40 column preservation for 53 and 97, plus the declared base-50
   involution `J_50(x)=150-x` exchanging them.
6. The layer sequence is quadratic and discretely convex; its residual is
   discretely concave. A fractal is **not established** because no recursive
   substitution or scale law is present.

## Replay

```bash
python3 RESEARCH/NOTES/PASCAL_PENTAGON_D5_TEST_2026-10-10/PASCAL_ROSETTA_JOINT_DESIGN_2026-10-11/NCS_292_Q106_INTERTWINER_RETURN_PACKAGE_2026-10-11/Q106_PRIME_INDEX_RADIX_ROOT_GROWTH_AUDIT_2026-10-11/verify_prime_radix_root_growth.py
```

The verifier emits the full JSON replay record to standard output. The
checked-in `RESULT.json` is the corresponding audit snapshot.

## Leo/Lilith 3:2 follow-up

The nested
`LEO_LILITH_3_2_ROOT_PAIR_CONNECTOR_AUDIT_2026-10-11` package recovers a
historical Lilith-labelled `3/2` frequency marker and verifies the exact
square-index prime ladder
`2,7,23,53,97 -> 9,30,76,150`. It classifies the proposed Leo/Lilith bridge
as an arithmetic observer-joint candidate, not a recovered operator.

## Owner-authorized Q106 square-index readout

The bounded
[`Q106_SQUARE_INDEX_PRIME_READOUT_AUDIT_2026-10-11`](Q106_SQUARE_INDEX_PRIME_READOUT_AUDIT_2026-10-11/README.md)
passes `17/17` checks, a byte-identical Primary/Replay and an independent
`13/13` verifier. It makes explicit that

```text
(F,O,L) = (9,16,25) = (3^2,4^2,5^2),
P_square(3,4,5) = (p9,p16,p25) = (23,53,97).
```

The index layer satisfies `9+16=25`. The prime-value layer does not satisfy a
Pythagorean identity. The Q106 C-closure remains exact, while the exhaustive
D5 orbit-union control confirms that no invariant 53-node subcarrier exists.
This is a typed prime-index readout over the existing Q106 carrier, not a new
Prime Pascal Pyramid identity or a node embedding.

The nested
[`Q106_46_106_194_CONTRAST_AUDIT_2026-10-11`](Q106_SQUARE_INDEX_PRIME_READOUT_AUDIT_2026-10-11/Q106_46_106_194_CONTRAST_AUDIT_2026-10-11/README.md)
then tests the same arithmetic grammar against `C_k=2*p_(k^2)` for
`k=3,4,5`. The carriers are `46,106,194`, but only `106` satisfies the exact
return equation `C_k-p_((k+1)^2)=(k-1)^2`. The classification is
`PASS_Q106_LOCAL_AND_BOUNDED_HOMOLOGUE_SELECTIVITY`; no `R(Q46)` or `R(Q194)`
is introduced.

## Files

- `CONTRACT.json` — machine-readable scope and claim boundary
- `FORMAL_CONTRACT.md` — equations, modules, and stop rules
- `verify_prime_radix_root_growth.py` — deterministic replay
- `RESULT.json` — verified result snapshot
- `LEO_LILITH_3_2_ROOT_PAIR_CONNECTOR_AUDIT_2026-10-11/` — archaeological
  and square-index-prime follow-up
- `Q106_SQUARE_INDEX_PRIME_READOUT_AUDIT_2026-10-11/` — Owner-authorized
  square-readout, prime-lift, negative-subcarrier and bounded homologue audits

