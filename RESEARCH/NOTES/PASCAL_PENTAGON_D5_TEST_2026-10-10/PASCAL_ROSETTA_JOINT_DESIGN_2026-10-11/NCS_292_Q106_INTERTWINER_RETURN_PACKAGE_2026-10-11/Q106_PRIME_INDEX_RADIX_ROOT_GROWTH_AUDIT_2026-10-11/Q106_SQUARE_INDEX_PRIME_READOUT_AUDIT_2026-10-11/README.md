# Q106 Square-Index Prime Readout Audit

Date: `2026-10-11`  
Status: `PASS / 17_OF_17 / R2_LOCAL_REPLAY / AWAITING_OWNER_DISPOSITION`  
Identity: reuses `SCC-003 / A0OE:PASCAL_PENTAGON_D5_TEST`

This bounded audit tests whether the frozen Q106 readout
`(F,O,L)=(9,16,25)` is exactly the `3-4-5` square triple and whether the
standard one-based lift `P_square(n)=p_(n^2)` supplies a typed prime readout
and scalar closure without creating a 53-node geometric half.

## Result

Primary and Replay are byte-identical with SHA-256
`31e4315f9e1a3de86fdb0212d135b71d269de8ef3f3c18a6c859ca5724e02492`.
The independent verifier passes `13/13` structural checks.

```text
R(Q106) = (F,O,L,N) = (9,16,25,106)
         = (3^2,4^2,5^2,106)

P_square(3,4,5) = (p9,p16,p25) = (23,53,97)
```

The exact closure is

```text
97-53 = 44 = 4*p5
106-97 = 9 = 3^2
44+9 = 53 = p16
106 = 2*p16
```

The value layer remains typed: `p_(n^2)` is not `(p_n)^2`, and
`23^2+53^2 != 97^2`. The exhaustive orbit-union control finds no D5-invariant
53-node subcarrier. Therefore the result is an exact readout composition, not
a prime-to-node embedding.

Classification:

```text
PASS_EXACT_SQUARE_INDEX_PRIME_READOUT_WITH_NO_D5_INVARIANT_53_SUBCARRIER
```

## 46/106/194 contrast

The Owner-authorized
[`Q106_46_106_194_CONTRAST_AUDIT_2026-10-11`](Q106_46_106_194_CONTRAST_AUDIT_2026-10-11/README.md)
passes `16/16`, with byte-identical replay and an independent `16/16`
verifier. For `C_k=2*p_(k^2)`, the three direct carriers are
`(C3,C4,C5)=(46,106,194)`. Only `k=4` satisfies
`C_k-p_((k+1)^2)=(k-1)^2`, both among `k={3,4,5}` and in the declared finite
scan `2<=k<=1000`.

This is bounded selectivity. It does not define `R(Q46)` or `R(Q194)` and
does not establish global uniqueness or a new Pascal identity.

## Files

- `CONTRACT.json` — frozen sources, outcomes and STOP boundary
- `FORMAL_CONTRACT.md` — typed maps and exact relations
- `RUN_CONTRACT.md` — reproducibility and failure semantics
- `verify_square_index_prime_readout.py` — deterministic primary runner
- `PRIMARY_RESULT.json` / `REPLAY_RESULT.json` — byte-identical runs
- `RESULT.json` — canonical result snapshot
- `verify_result.py` — independent result verifier
- `Q106_46_106_194_CONTRAST_AUDIT_2026-10-11/` — bounded homologue and
  perturbation controls

No new Study, PENT layer, Family or Navigator identity is created. Owner
acceptance or revision remains a separate disposition.
