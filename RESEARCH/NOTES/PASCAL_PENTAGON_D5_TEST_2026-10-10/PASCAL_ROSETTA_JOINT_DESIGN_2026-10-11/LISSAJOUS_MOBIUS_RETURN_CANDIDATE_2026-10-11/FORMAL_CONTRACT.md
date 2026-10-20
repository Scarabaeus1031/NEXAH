# Lissajous–Möbius return candidate — formal contract

Date: `2026-10-11`  
Status: `FORMAL_DESIGN_VALIDATION / NOT_ADMITTED / NOT_PENT_08`

## Question

Can the already verified Pascal `C30` phase lift be extended by a declared
strip coordinate and an orientation bit so that a Lissajous phase path has
separate cylinder and Möbius return laws?

This is a bounded design question. It does not ask whether the source visual
is itself a Möbius surface or whether a physical mechanism exists.

## State space

The candidate state is

```text
(j,p,e) in C5_D x C30_P x C2_E,
```

where `j` is the existing `D1..D5` register address, `p` is the D30 phase and
`e` is an explicit orientation sign. The state space has `5 x 30 x 2 = 300`
states.

The signed register chart is

```text
D1 ->  0
D2 -> +1
D3 -> +2
D4 -> -2
D5 -> -1.
```

Consequently the existing D5 reflection `j -> -j mod 5` compiles to `v -> -v`
for `v=signed(j)/2`.

## Lissajous phase view

For `theta=2*pi*p/30`, display

```text
x=cos(5 theta),
y=sin(6 theta).
```

The exact phase state is not the floating-point pair `(x,y)`. It is the CRT
signature

```text
(p mod 6, p mod 5),
```

which has period `lcm(6,5)=30` and reconstructs `p` uniquely. The plotted
projection is expected to have collisions and is therefore a view only.

## Seam controls

The same 30-phase carrier receives two alternative seam laws.

Cylinder:

```text
(j,29,e) -> (j,0,e).
```

Möbius:

```text
(j,29,e) -> (-j mod 5,0,-e).
```

The reverse step applies the same reflection and sign flip at `0 -> 29`.
Therefore one forward circuit must reverse register coordinate and
orientation; two circuits must return the complete state.

The boundary graph is checked independently: the cylinder control must have
two boundary components, while the twisted seam must join them into one.

## Pascal word transport

The existing compiler is retained:

```text
L: p -> p-1
R: p -> p+1.
```

All 127 words of length zero through six are transported from every candidate
state. Applying the reversed word with `L/R` exchanged must recover the exact
starting state. The endpoint phase must equal the signed branch sum modulo 30.

## Pass criteria

The candidate passes only if:

1. the exact `(mod 6, mod 5)` signature covers all 30 phases uniquely;
2. the rendered Lissajous projection remains explicitly lossy;
3. cylinder and Möbius seam controls differ;
4. cylinder boundary count is two and Möbius boundary count is one;
5. one Möbius circuit reverses orientation;
6. two Möbius circuits return all 300 states exactly;
7. forward and reverse seam steps are mutual inverses;
8. all bounded Pascal branch words have exact inverse transport;
9. all 140 frozen Pascal incidences receive a defined candidate chart;
10. no new Study, PENT identity, Family or canonical Navigator relation is
    inferred.

## Failure semantics

A failed invariant invalidates this candidate encoding. A pass validates only
the declared finite transport and seam contract; it does not admit PENT-08 or
establish a continuous, physical, astronomical or universal Möbius mechanism.
