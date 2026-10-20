# Formal contract — Q106 46/106/194 contrast

Date: `2026-10-11`  
Identity: reuse `SCC-003 / A0OE:PASCAL_PENTAGON_D5_TEST`

Let `p_n` denote the `n`th prime with one-based indexing. Define the arithmetic
comparison carrier

```text
C_k = 2*p_(k^2)
```

and its three square-index-prime values

```text
H_k = (p_((k-1)^2), p_(k^2), p_((k+1)^2)).
```

The tested return predicate is

```text
E(k) iff C_k - p_((k+1)^2) = (k-1)^2.
```

The direct contrast set is `k in {3,4,5}`. A declared finite search checks
`2 <= k <= 1000`. The local perturbation set is `N in {104,...,108}` with
the frozen Q106 constants `p16=53`, `p25=97` and `3^2=9`.

The comparison deliberately does **not** define `R(Q46)` or `R(Q194)`.
Only the previously frozen `R(Q106)=(9,16,25,106)` is an admitted readout.

Positive classification requires:

1. the frozen parent result hash matches;
2. `(C_3,C_4,C_5)=(46,106,194)`;
3. the return residuals are `(-7,9,43)` and targets `(4,9,16)`;
4. only `k=4` satisfies `E(k)` among `k=3,4,5`;
5. only `k=4` satisfies `E(k)` in the declared scan through `1000`;
6. only `N=106` in `104..108` satisfies both frozen Q106 closures;
7. type and claim boundaries remain explicit.

The result is a bounded selectivity statement, not an infinite theorem or a
new Pascal construction.
