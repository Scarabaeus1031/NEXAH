# General coordinate-fold and minimal residual Return contract

## Declared fold

Let `m,d >= 1`, `X_m={0,...,2m-1}` and `Y_m={0,...,2m-2}`. Define

```text
q_m(i) = i      when i <= m-1
q_m(i) = i - 1  when i >= m
```

and let `Q_{m,d}` apply `q_m` coordinatewise. The only non-singleton
one-dimensional fibre is `q_m^-1(m-1)={m-1,m}`.

## Fibre theorem

For `y in Y_m^d`, let `k(y)` be the number of coordinates equal to `m-1`.
Independent coordinate choices give

```text
|Q_{m,d}^-1(y)| = 2^k(y).
```

Choose the `k` central coordinates in `C(d,k)` ways. Every remaining
coordinate has `2m-2` non-central values. Therefore

```text
number of targets with fibre size 2^k = C(d,k)(2m-2)^(d-k).
```

The two conservation identities are

```text
sum_k C(d,k)(2m-2)^(d-k)       = (2m-1)^d
sum_k 2^k C(d,k)(2m-2)^(d-k)   = (2m)^d.
```

## Minimal residual and exact Return

At a target with `k` central coordinates, exact Return requires at least `k`
binary decisions because its fibre has `2^k` elements. This lower bound is
attained: record one bit only at each central target coordinate.

Coordinatewise reconstruction is

```text
y_j < m-1  -> x_j = y_j
y_j > m-1  -> x_j = y_j + 1
y_j = m-1  -> x_j = m-1 + residual_bit_j.
```

Thus the pointwise minimal residual length is `k(y)`. A fixed-length residual
that must work for every target requires `d` bits, because the all-central
target has a `2^d`-element fibre.

## TripleSix boundary

The six TripleSix states are a state-set address `{A,B,C} x C2`. They can
label the disjoint union of three selected one-axis double fibres (`3x2=6`).
They cannot label all source states above one simultaneous three-axis central
target (`2^3=8`). This is a capacity statement, not a cube identity.

## A0-BL-025 boundary

This package closes the coordinate-fold fibre and minimal-Return subproblem
with two non-identical controls. The wider Grid–Fold–Channel backlog item
remains open because embedding, envelope, channel/interface, assembly and
update rules are not specified here.
