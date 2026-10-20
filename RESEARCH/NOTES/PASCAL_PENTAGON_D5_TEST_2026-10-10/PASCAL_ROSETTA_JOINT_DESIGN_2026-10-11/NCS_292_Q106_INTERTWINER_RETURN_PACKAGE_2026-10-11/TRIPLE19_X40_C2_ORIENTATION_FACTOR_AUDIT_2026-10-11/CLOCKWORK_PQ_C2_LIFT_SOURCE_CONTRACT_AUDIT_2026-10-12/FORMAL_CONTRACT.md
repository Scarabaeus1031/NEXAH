# Clockwork P/Q · NCS C2 lift source contract

## Question

Can the source-bound Clockwork v7 `p/q` conjugate pair represent the two
orientation sheets of the exact NCS quotient

`q : X40 = X20 x C2 -> X20`,

without claiming that the GLB supplies the missing X20 graph or a full carrier
map?

## Candidate lift

Define the display carrier

`L_PQ = X20 x {p,q}`

with projection `lambda(x,ell)=x` and deck flip
`tau(x,p)=(x,q)`, `tau(x,q)=(x,p)`.

Each of the two global labelings

- `e=0 -> p`, `e=1 -> q`;
- `e=0 -> q`, `e=1 -> p`

is a bijection `X40 -> L_PQ`, commutes with projection to X20 and sends the
C2 flip induced by either NCS Janus candidate to the `p/q` sheet swap.

## Source question

The finite construction alone cannot choose between those two labelings. The
audit therefore inspects the retained v7 GLB metadata and builder for an
explicit orientation-bit assignment. Mirror angles, opposite tilts, opposite
turns, colors or the words `p` and `q` do not select `e=0` versus `e=1` unless
the source declares that map.

## Gamma boundary

Under the sheet swap, `(p+q)/2` is symmetric and `(p-q)/2` changes sign. This
is a useful display-basis decomposition. In v7 it remains
`VISUAL_COUPLING_GRAMMAR_ONLY`; it is not a numerically evaluated NCS
operator.

## Decision boundary

A pass establishes only an **unlabeled two-sheet display lift** of the already
proved C2 factor. It does not recover X20 adjacency, choose `J_c` or `J_d`,
construct `Triple19 -> X20`, or create a Q106 intertwiner. The center remains
outside this lift and is not promoted to a state or switch.
