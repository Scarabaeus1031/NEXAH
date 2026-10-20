# TripleSix S3 / cube-grid fold contract

## Question

Do the six depicted permutations form an exact three-axis plus two-orientation
address, and how far does that address resolve the information lost when a
`64` coordinate is folded to `63`?

## TripleSix carrier

The six glyphs are treated literally as the permutations of `(1,2,3)`, hence
as the state set of `S3`. Right composition with the reversal
`tau=(13)` gives the three displayed antipodal pairs:

```text
A: 123 <-> 321
B: 132 <-> 231
C: 213 <-> 312
```

Permutation parity changes across every pair. Therefore each state has the
exact address `(axis, parity)` in `{A,B,C} x C2`. This is a bijection of state
sets, not a direct-product group claim: `S3` is non-abelian.

Every glyph has digit sum `6`. The center label `6` is therefore an exact
readout invariant of these six states, but it is not a proof of resonance.

## Operator-convention boundary

With the displayed reversal acting on the right and the three-axis cycle
acting on the left, the two operators commute. This is compatible with the
commuting X40 convention `J_c`.

If rotation and reflection are instead both right actions, the dihedral law
`J r J = r^-1` holds, but that rotation does not descend to the displayed
three-pair axis quotient. It is compatible with `J_d` only under a different
action convention.

The visuals do not freeze left/right action semantics. The audit therefore
retains both comparisons and makes no historical Janus selection.

## Declared 64-to-63 fold

For `i in {0,...,63}`, define

```text
q(i) = i      for i <= 31
q(i) = i - 1  for i >= 32.
```

This surjection collapses `{31,32}` to the single pivot address `31`. Its
coordinatewise products `Q_2` and `Q_3` connect `64x64` to `63x63` and
`64^3` to `63^3`.

TripleSix supplies one selected axis and one binary side. That is exactly
enough to type one oriented fold crossing. It does not supply the two or three
independent side bits required where two or three fold coordinates meet. At
the 3D pivot the quotient fibre has eight states, while the TripleSix carrier
has six.

## Decision boundary

Passing establishes a formal address-and-fold bridge only. The map `q` is an
explicit construction introduced by this audit. The owner-supplied visuals
motivate the question and are hash-bound documentary sources; they do not
prove that this is their historical generator or a physical cube mechanism.
