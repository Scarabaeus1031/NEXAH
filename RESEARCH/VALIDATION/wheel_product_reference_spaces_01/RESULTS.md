# Results

Status: deterministic evidence generated from the frozen specification.

## Decision summary

| Claim | Result |
|---|---|
| Mod 6 carries held-out dual transition information | SUPPORTED |
| `Z/42Z ↔ Z/6Z × Z/7Z` round-trip is exact | SUPPORTED |
| Mod-42 transitions require joint 6×7 interaction | SUPPORTED |
| Mod 280 and 360 differ under matched normalized gain | SUPPORTED |
| The 31/32/33 boundary is a top-5% local anomaly | NOT SUPPORTED |
| Any tested modulus stabilizes dynamics | NOT TESTED / NOT SUPPORTED |

## Mod 6

| Policy | Mean information gain (bits/event) | Maximum null p |
|---|---:|---:|
| `all_primes` | 0.021763 | 0.009901 |
| `without_2_3` | 0.021655 | 0.009901 |

All primes greater than 3 occupied only residues 1 and 5. Exceptions: `[]`. Exact gap-2 pairs: 2370; exact gap-4 pairs: 2354.

## Mod 42 as a product reference space

| Policy | Joint advantage (bits/event) | 95% paired bootstrap CI |
|---|---:|---:|
| `all_primes` | 0.554647 | [0.544395, 0.566214] |
| `without_2_3` | 0.554648 | [0.544404, 0.566200] |

The coordinate equivalence is exhaustive and exact. The interaction result concerns only whether independent Mod-6 and Mod-7 transition models reproduce the joint Mod-42 transition kernel.

## Mod 280 versus Mod 360

| Policy | Normalized-gain difference `360-280` | 95% CI |
|---|---:|---:|
| `all_primes` | 0.020352 | [0.017761, 0.022943] |
| `without_2_3` | 0.020329 | [0.017733, 0.022924] |

## 31/32/33 boundary

Normalized gains: 31 = 0.228244, 32 = 0.098377, 33 = 0.283926.

Local curvature percentile: 83.33%. Predeclared 95% anomaly flag: NO.

## Exact wheel facts

- `rad(360) = 30`.
- `phi(280) = 96` and `phi(360) = 96`.
- `lcm(20,24,30) = 120`.
- The 24-node and 60-tick grids meet at 12 angles.

## Interpretation boundary

Arithmetic round-trips establish coordinate equivalence, not dynamic independence. Held-out predictability establishes descriptive sequence structure, not attraction, recovery or stabilization. Polar and wheel representations remain representations of these records.
