# Pascal-quaternion → NCS P4 adapter gate

Date: `2026-10-12`  
Class: source-bound formal adapter audit; not an admitted Study

## Typed objects

The closed Pascal connector supplies the four labelled slots

```text
S = {scalar, i, j, k}
Phi(a,b,c) = (a+b+c)1 + ai + bj + ck
gamma = (scalar)(i j k).
```

The declared NCS package coordinate is

```text
R = {carrier, frame_cut, transform_view, return_record}.
```

Both NCS rotation and both candidate Janus laws preserve the package coordinate
`p`. Their declared action on `R` is therefore the identity `id_R`.

## Tests

For every bijection `f:S→R`, test two different claims:

1. **Address Return:** `f^-1(f(s))=s`. This asks only whether the four labels can
   encode one another.
2. **Operator intertwining:** `f∘gamma=id_R∘f`. This asks whether the proved
   Pascal `C3` action is the same typed action as the declared NCS role action.

The first claim may hold without the second. A vocabulary-motivated assignment
such as `scalar→carrier`, `i→frame_cut`, `j→transform_view`,
`k→return_record` receives no special status unless it passes the same operator
test and is independently source-declared.

## Induced-action control

Every chosen bijection can transport `gamma` to a new permutation
`f gamma f^-1` on the NCS role labels. This construction is exact, but it does
not recover an NCS operator. The audit records how many distinct transported
actions occur and what extra source input would be required to select a map.

## Stop boundary

No target fit, visual order, semantic resemblance, Root-40 coefficient, wobble
phase or Q106 structure may be used to manufacture the missing source law.
Failure of operator equivariance leaves the canonical adapter null.
