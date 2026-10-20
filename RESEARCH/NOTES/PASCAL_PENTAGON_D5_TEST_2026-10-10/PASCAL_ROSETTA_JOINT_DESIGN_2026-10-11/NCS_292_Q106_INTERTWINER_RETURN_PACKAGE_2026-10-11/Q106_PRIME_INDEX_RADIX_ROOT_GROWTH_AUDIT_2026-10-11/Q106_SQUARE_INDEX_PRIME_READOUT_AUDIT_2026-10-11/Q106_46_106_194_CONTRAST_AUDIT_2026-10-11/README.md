# Q106 46/106/194 Contrast Audit

Date: `2026-10-11`  
Status: `PASS / 16_OF_16 / R2_LOCAL_REPLAY / AWAITING_OWNER_DISPOSITION`  
Identity: extends the existing `SCC-003 / A0OE:PASCAL_PENTAGON_D5_TEST` lens

This audit asks whether the Q106 return survives in its immediate arithmetic
homologues. It defines only the comparison carriers

```text
C_k = 2*p_(k^2)
```

and does not invent `R(Q46)` or `R(Q194)`.

## Result

Primary and Replay are byte-identical with SHA-256
`016758c50f249742ea06101979474c6c68af893af92051a343abdb9f0ea1918f`.
The independent result verifier passes `16/16` checks.

```text
k=3: (p4,p9,p16)   = (7,23,53)   C3=46   C3-p16=-7  != 2^2
k=4: (p9,p16,p25)  = (23,53,97)  C4=106  C4-p25=9   = 3^2
k=5: (p16,p25,p36) = (53,97,151) C5=194  C5-p36=43  != 4^2
```

Thus only `k=4` satisfies

```text
2*p_(k^2) - p_((k+1)^2) = (k-1)^2
```

in both the direct `k={3,4,5}` contrast and the declared finite scan
`2<=k<=1000`. Independently, the consecutive-root square equation factors as

```text
(k-1)^2+k^2-(k+1)^2 = k(k-4),
```

so the positive consecutive-root Pythagorean window also selects `k=4`.

The local perturbation test `104..108` selects only `106`: its residuals from
`p25=97` are `7,8,9,10,11`, while its residuals from `2*p16=106` are
`-2,-1,0,1,2`.

Classification:

```text
PASS_Q106_LOCAL_AND_BOUNDED_HOMOLOGUE_SELECTIVITY
```

This strengthens Q106 as a bounded typed readout lens. It does not prove
global uniqueness, define an `R` operator on 46 or 194, add a Pascal
coefficient transform, or create a Prime Pascal Pyramid identity.

## Files

- `CONTRACT.json` — definitions, declared windows and STOP boundary
- `FORMAL_CONTRACT.md` — finite mathematical statement
- `RUN_CONTRACT.md` — local replay contract
- `verify_q106_contrast.py` — deterministic primary runner
- `PRIMARY_RESULT.json` / `REPLAY_RESULT.json` — byte-identical results
- `RESULT.json` — canonical result snapshot
- `verify_result.py` — independent structural verifier
