# 03 — Totient Gap Report

## Realized side: 6/7

```text
2401=7⁴
φ(2401)=7³(7−1)=2058
φ(2401)/2401=6/7
1−φ(2401)/2401=1/7
```

Because `7⁴=49²` and every odd square is centered octagonal, 2401 simultaneously has prime-power, square and centered-octagonal representations. This conjunction is correct but follows immediately from standard formulas.

## Empty-preimage side: 7/8

Assume an integer `n>1` satisfies `φ(n)/n=7/8`.

- If `n` is even, 2 divides `n`; the Euler product contains `(1−1/2)=1/2`. Every other factor is below 1, so `φ(n)/n≤1/2`, contradiction.
- If `n` is odd, every prime divisor of `n` is odd. Before reduction, the Euler product has an odd denominator; after reduction its denominator still divides an odd number and is therefore odd. The reduced denominator 8 is even, contradiction.

Therefore:

```text
No integer n>1 satisfies φ(n)/n=7/8.
```

Classification:

```text
FORMALLY EXPECTED CONTINUATION WITH EMPTY INTEGER PREIMAGE
STANDARD COROLLARY · NOT A NEW THEOREM
```

This is the strongest NEXAH teaching case in the package: a visually natural continuation fails the return map into integer totient ratios.

## 4⁷

```text
4⁷=2¹⁴=16384
φ(4⁷)=8192
φ(4⁷)/4⁷=1/2
```

It does not operationally connect to `7/8`; it is excluded from the mathematical core and retained only as an annotation candidate.

