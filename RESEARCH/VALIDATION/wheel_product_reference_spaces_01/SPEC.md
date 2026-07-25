# Frozen Experimental Specification

## Scope

This experiment distinguishes three kinds of claims:

- **arithmetic identities**, which can be checked exhaustively;
- **descriptive transition structure**, which requires held-out evidence; and
- **stability claims**, which are not tested here.

The experiment does not infer dynamics from a circular drawing.

## Input and folds

The canonical sequence is the first 20,000 primes in ascending order,
including 2 and 3.

Policies:

- `all_primes`;
- `without_2_3`, removing only 2 and 3 from each training prefix.

Both policies share identical test ranges. Five expanding chronological folds
are fixed: train 0–50/60/70/80/90 percent and test the immediately following
10 percent.

## A. Mod-6 dual prime structure

The exact claim is:

```text
Every prime p > 3 satisfies p mod 6 ∈ {1, 5}.
```

The empirical claim is that the preceding Mod-6 residue provides held-out
information about the next residue beyond the training marginal.

A first-order Markov model with additive smoothing `alpha = 0.5` is compared
with a training-only marginal model. The primary metric is information gain in
bits per event. One hundred deterministic training-sequence shuffles preserve
the marginal and destroy order.

Support requires positive mean information gain and maximum fold-wise
one-sided empirical null probability at most 0.05 under both policies.

Gap classes are reported exactly:

- `5 → 1`: gap congruent to 2 modulo 6;
- `1 → 5`: gap congruent to 4 modulo 6;
- equal classes: gap congruent to 0 modulo 6.

Exact gaps 2 and 4 are reported separately.

## B. Mod-42 product coordinates

Because `gcd(6, 7) = 1`, the Chinese remainder theorem gives:

```text
Z/42Z ≅ Z/6Z × Z/7Z
```

The fixed coordinate maps are:

```text
decode(x) = (x mod 6, x mod 7)
encode(a, b) = (7a + 36b) mod 42
```

All 42 states must round-trip exactly.

Arithmetic equivalence does not imply transition independence. The empirical
test compares:

- a joint Mod-42 transition model; and
- the product of independently learned Mod-6 and Mod-7 transition models.

Joint interaction is supported only if the paired bootstrap 95% interval for
`product log loss - joint log loss`, in bits per event, is strictly above zero
under both policies.

## C. Wheel and lift family

The modulus scan contains every modulus 5 through 60 plus 120, 210, 280 and
360. For each modulus, held-out information gain is also divided by
`log2(phi(m))` to reduce the direct influence of accessible alphabet size.

Exact checks:

- `rad(360) = 30`;
- `phi(280) = phi(360) = 96`;
- every unit class modulo 30 has exactly 12 unit lifts modulo 360;
- `lcm(20, 24, 30) = 120`;
- the 24-node and 60-tick angular grids meet at 12 positions, every 30 degrees;
- 360 refines the 20-, 24-, 30-, 60- and 120-grids.

## D. Matched Mod-280 versus Mod-360 comparison

The paired fold-wise difference is:

```text
normalized information gain (360) - normalized information gain (280)
```

The spaces are considered distinguishable under this metric only if the paired
bootstrap 95% interval excludes zero under both policies. No direction is
predeclared.

## E. Local 31/32/33 boundary test

For each center `m = 6..59`, define normalized-gain curvature:

```text
C(m) = G(m-1) - 2G(m) + G(m+1)
```

where `G` is mean normalized held-out information gain under `all_primes`.

The `31/32/33` neighborhood is flagged only if `abs(C(32))` lies at or above
the 95th percentile of all predeclared centers. This is a local anomaly screen,
not evidence of a phase transition.

## F. Complement symmetry

For selected spaces `{6, 30, 40, 42, 120, 280, 360}`, compare the held-out
edge-frequency distribution `q(i,j)` with its reflected distribution
`q(-i,-j)`. Total-variation distance zero means exact reflection symmetry.
This measurement is descriptive; no universal threshold is imposed.

## Explicit non-claims

This experiment does not establish:

- that any modulus stabilizes a dynamical system;
- that recurrence is attraction;
- that a polar axis is emergent merely because coordinates use angles;
- that Mod 360 is universal;
- that 31–33 is a transition without the predeclared anomaly result;
- or that arithmetic coordinate equivalence implies independent dynamics.
