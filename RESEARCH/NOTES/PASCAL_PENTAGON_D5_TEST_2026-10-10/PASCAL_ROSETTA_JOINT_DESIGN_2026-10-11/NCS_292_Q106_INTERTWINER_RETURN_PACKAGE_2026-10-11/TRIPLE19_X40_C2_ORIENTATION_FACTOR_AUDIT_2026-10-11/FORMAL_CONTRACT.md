# Triple-19 / X40 C2 orientation-factor contract

## Question

Does the oriented Triple-19 carrier share an exact, typed factor with the NCS X40 carrier, and does that factor descend through the declared quotient to X20?

## Carriers and operators

Write the Triple-19 row as `u=r-3` in `C7` and its constructor sign as `sigma in C2`. Then

`T14 = C7 x C2`, with `A(u,sigma)=(-u,-sigma)`.

The NCS carrier is

`X40 = C5 x P4 x C2_J`,

with rotation `r_X(s,p,e)=(s+1,p,e)`, commuting Janus `J_c(s,p,e)=(s,p,1-e)`, dihedral Janus `J_d(s,p,e)=(-s,p,1-e)`, and quotient `q(s,p,e)=(s,p)` in `X20=C5 x P4`.

## Exact shared factor

Define `pi_T(u,sigma)=sigma` and `pi_X(s,p,e)=e`. Both Triple-19 antipody and either X40 Janus law induce the nontrivial flip on `C2`:

`pi_T A = flip pi_T`, and `pi_X J_c = pi_X J_d = flip pi_X`.

This is an exact common factor. It is weaker than a carrier map.

## Quotient obstruction

Every X20 state `(s,p)` is the image of the two X40 states `(s,p,0)` and `(s,p,1)`. Their `pi_X` values differ. Therefore no function `rho:X20->C2` can satisfy `rho q = pi_X`: the quotient erases precisely the shared orientation coordinate.

The base cycles do not repair this loss. Any group homomorphism `C7->C5` is trivial because `gcd(7,5)=1`. Thus the full Triple-19 reflection grammar cannot be transported to the X40 five-cycle by a nontrivial cyclic group map.

## Decision boundary

Passing this audit establishes only the shared `C2` factor and the orientation loss in the canonical X40-to-X20 quotient. It leaves `Triple19->X20`, `Triple19->Q106`, the full-carrier intertwiner, X20 adjacency and the historical choice between `J_c` and `J_d` null.

