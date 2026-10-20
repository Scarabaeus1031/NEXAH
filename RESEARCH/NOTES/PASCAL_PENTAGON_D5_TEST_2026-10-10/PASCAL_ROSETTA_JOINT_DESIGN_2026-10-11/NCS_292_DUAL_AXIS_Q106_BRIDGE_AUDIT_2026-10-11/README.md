# NCS-292 dual-axis / Q106 bridge audit

Date: `2026-10-11`  
Status: `PASS_WITH_VALIDATED_OPEN_BRIDGES`  
Classification: `COMPILED_40_TO_20_CANDIDATE_OPEN_INTERTWINERS`

Reused identity: `SCC-003 / A0OE:PASCAL_PENTAGON_D5_TEST`

## Result

The bounded candidate compiles, but the proposed mechanism identity does not.

Exact controls confirm:

- `292` is a palindrome with `2+9=9+2=11`;
- `29=P10`;
- `P23..P27 = 83,89,97,101,103`;
- the `97<->101` and `97<->103` cuts have adjacent midpoints `99` and `100`;
- the right endpoint moves by `2`, while the midpoint moves by `1`;
- `97+4=101`, `97+3=100`, `103+3=106`, and `106=2*53`;
- `53^2=2809`, so it is not another spelling of `106`;
- the historical NCS source contains four pink points and moves all four in
  its display animation;
- the declared `C5 x P4 x C2_J` carrier has forty states, and free horizontal
  layer gluing gives twenty quotient classes with two states per fibre;
- the independent SCC-003 reference remains the verified `106`-node,
  `180`-directed-edge graph.

## Validated open bridges

Three maps are still absent:

1. no typed permutation identifies the historical four NCS points with
   `carrier`, `frame/cut`, `transform/view`, and `return/record`;
2. no node/edge map sends the twenty quotient classes to Q106;
3. the Root Cube v15 count of fifteen primary nodes has no declared map to
   Q106.

Therefore `103+3=106` is retained as a numeric P-exit candidate, not as a
derivation of Q106. The Root Cube count `15` is a source-local visual
comparator and is not multiplied into the candidate carrier.

## Interpretation

The test sharpens the working architecture:

```text
ABC / 123 x orientation     -> six local path states
292 NCS                     -> historical four-point display mover
97-101 / 97-103             -> adjacent cut pair, midpoints 99 / 100
C5 x P4 x C2_J              -> declared 40-state unfolded carrier
horizontal Janus gluing     -> declared 20-class quotient
103 + 3                     -> numeric arrival at 106
Q106                        -> separate verified Pascal quotient
```

The gap between the 20-class quotient and Q106 is now explicit rather than
hidden by the shared number `106`.

## Replay

```bash
python3 verify_ncs_292_dual_axis_q106.py
python3 verify_ncs_292_dual_axis_q106.py --write
```

This is deterministic formal-design validation, not an admitted Science Lab
run and not `PENT-08`.
