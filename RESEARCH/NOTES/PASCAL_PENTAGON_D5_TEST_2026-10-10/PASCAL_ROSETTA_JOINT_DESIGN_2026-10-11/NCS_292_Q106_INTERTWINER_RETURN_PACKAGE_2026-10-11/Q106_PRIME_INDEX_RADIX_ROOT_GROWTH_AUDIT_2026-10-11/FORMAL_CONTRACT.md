# Q106 prime-index · radix mirror · root-growth audit — formal contract

Status: **formal design validation; not an admitted Study**  
Identity: reuses `A0OE:PASCAL_PENTAGON_D5_TEST`; creates none.

## Question

Can the proposed `2–3–5` seed, the numbers `53`, `97`, `106` and `150`,
the frozen `D5` action, and bases `20`, `40`, `50` be joined by exact,
replayable relations? Which relations are coordinate-dependent, and does the
observed root growth establish a fractal?

## M1 — Q106 root growth

Read the node levels from the frozen SCC-003 table. For `m=0,…,6`, test

`Q_m = 1 + 5 T_m`, where `T_m=m(m+1)/2`.

The expected cumulative sequence is

`1, 6, 16, 31, 51, 76, 106`,

with first differences `5,10,15,20,25,30` and constant second difference
`+5`. Thus `Q_m` is discretely convex. The residual room
`R_m=Q_6-Q_m` has second difference `-5` and is discretely concave. These
are operational definitions; they do not import visual curvature.

## M2 — the 2–3–5 seed

Test exactly:

- `2+3=5`, matching the fivefold coefficient in `Q_m`;
- `2·3=6=Q_1`;
- `2/3` is a rational with repeating decimal digit `6`, but is not `6`;
- `2^3=8` is retained as an external comparator, because `8` is absent from
  the cumulative Q-sequence;
- `Q_2=16=2^4`, not `2^3`.

Parity is evaluated directly on the Q-sequence. It is not equated with
convexity: parity and second difference are different typed observables.

## M3 — orbit / prime-index joint

Derive the frozen `D5` orbit profile. Let:

- `O` be the number of orbits;
- `F` be the number of five-node orbits;
- `L` be the number of interior nodes on the final level.

Test `O=16`, `F=9`, `L=25=O+F`, `p_O=53`, `p_L=97`,
`106=2p_O`, `106-F=p_L`, and `p_O+p_L=150`. The index distance from
`p_16` to `p_25` is nine steps; eight primes lie strictly between them.

## M4 — D5 half obstruction

Enumerate all unions of the sixteen `D5` orbits. A 53-node invariant half
would have to be a union of orbit sizes `1`, `5`, and `10`. Such unions have
cardinality congruent to `0` or `1 (mod 5)`, whereas `53 ≡ 3 (mod 5)`.
The exhaustive target count must therefore be zero.

## M5 — radix mirror

For each declared base `b`, use the Euclidean coordinate
`C_b(n)=(floor(n/b), n mod b)`. This makes the test reproducible and avoids
reading geometry into a numeral string.

Test the coordinates of `53`, `97`, `106`, and `150` in bases `20`, `40`,
and `50`. In the 20→40 comparison, `53` and `97` retain columns `13` and
`17` while the row halves. `106` does not: `(5,6)_20 -> (2,26)_40`.

On `[50,100]`, declare `J_50(x)=150-x`. Test that it is an involution,
has fixed point `75`, and swaps `53` with `97`. This is a coordinate
construction, not a Q106 graph automorphism.

## M6 — fractal boundary

Quadratic growth with constant second difference is established. A fractal
requires, at minimum, a recursive substitution or self-similarity rule and a
declared scale relation. Neither is supplied by the frozen node table or D5
action. The audit must therefore return `NOT_ESTABLISHED` for the fractal
claim even when every arithmetic test passes.

## Outcome rule

Return `PASS_EXACT_ORBIT_PRIME_RADIX_ROOT_GROWTH_WITH_FRACTAL_OPEN` only
when all exact checks pass and the fractal claim remains explicitly open.

