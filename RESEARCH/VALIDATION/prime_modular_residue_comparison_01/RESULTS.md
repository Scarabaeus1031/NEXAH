# Results

Status: deterministic evidence generated from the frozen specification.

## Decision summary

| Claim | Result |
|---|---|
| Modulo 17 has a held-out predictive advantage over modulo 7 and controls | NOT SUPPORTED |
| Fixed `(7*r7+8) mod 17` bridge exceeds the majority baseline | NOT SUPPORTED |
| Modulo 17 stabilizes dynamics | NOT TESTED / NOT SUPPORTED |

## Modulo 17 versus modulo 7

| Prime policy | Mean difference (bits/event) | 95% paired bootstrap CI | Highest-gain modulus |
|---|---:|---:|---:|
| `all_primes` | 0.379748 | [0.365569, 0.393276] | 23 |
| `without_2_3` | 0.379760 | [0.365573, 0.393302] | 23 |

## Primes 2 and 3

The canonical run includes 2 and 3. The sensitivity policy removes them only from the training prefix while keeping every test range unchanged.

Observed change in the modulo-17 minus modulo-7 estimate: 0.000012 bits/event. Predeclared sensitivity flag: NO.

## Proposed 7-to-17 bridge

| Prime policy | Fixed accuracy | Majority accuracy | Learned lookup | Fixed-minus-majority 95% CI |
|---|---:|---:|---:|---:|
| `all_primes` | 0.060900 | 0.061100 | 0.059200 | [-0.004100, 0.003600] |
| `without_2_3` | 0.060900 | 0.061100 | 0.059200 | [-0.004400, 0.003600] |

## Interpretation boundary

Modulo 17 exceeds modulo 7 in the held-out comparison, but modulo 23 has the highest gain under both policies. The predeclared specificity rule therefore rejects a special Mod-17 predictive status. This is evidence for modular transition structure in the tested prime sequence, not evidence that 17 is uniquely privileged.

The fixed 7-to-17 rule does not exceed its training-only majority baseline. The observed interval spans zero, so the proposed affine bridge is not supported as a reconstructive mapping by this test.

A predictive result concerns residue-sequence description. A bridge result concerns coordinate reconstruction. Neither is evidence of dynamical damping, recovery, attraction, error correction or stability. The repository's proposed Mod-17 stabilizer remains an unvalidated hypothesis after this experiment.
