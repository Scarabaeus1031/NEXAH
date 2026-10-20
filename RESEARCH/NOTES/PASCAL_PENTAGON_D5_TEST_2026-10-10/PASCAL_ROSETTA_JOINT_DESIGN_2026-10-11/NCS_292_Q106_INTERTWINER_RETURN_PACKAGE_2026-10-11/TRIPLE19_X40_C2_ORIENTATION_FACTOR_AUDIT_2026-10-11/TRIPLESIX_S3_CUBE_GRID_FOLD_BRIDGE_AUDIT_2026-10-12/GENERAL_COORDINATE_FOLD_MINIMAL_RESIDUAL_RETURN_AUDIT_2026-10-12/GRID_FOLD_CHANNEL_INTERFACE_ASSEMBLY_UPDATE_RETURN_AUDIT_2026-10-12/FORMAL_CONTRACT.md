# Grid–Fold–Channel interface contract

## Typed objects

For `m,d >= 1`, the source carrier is `X_m^d` and the folded carrier is
`Y_m^d`, using the already validated coordinate fold `Q_{m,d}`.

1. **Embedding** `e:Y_m^d -> Z^d` is injective.
2. **Envelope** `B` is the graph boundary of the embedded finite grid.
3. **Interface** `I` is an explicitly selected subset of `B` with injective
   left and right anchor maps.
4. **Assembly** is the quotient of two labelled folded carriers `L` and `R`
   obtained by identifying corresponding interface anchors only.
5. **Coupling** is the common quotient class of each declared anchor pair.
6. **Update** is admissible only when its branch maps preserve the interface
   and agree there through one interface permutation.
7. **Return** reconstructs branch and pre-fold source coordinates from the
   assembled observation plus a minimal residual address.

## Residual theorem for the declared two-branch assembly

Let `k(y)` count central folded coordinates and let `g(y)=1` when `y` is on
the glued interface, otherwise `0`. Then the assembled observation fibre has

```text
2^(k(y)+g(y)) source states.
```

Consequently exact Return needs and suffices with:

```text
k(y) fold bits + g(y) branch bit.
```

Outside the interface the assembly key retains the branch. At the interface
the branch is erased by gluing and must be supplied as residual information.

## Controls

### Path seam

- `m=2`, `d=1`, embedded target path `{0,1,2}`;
- envelope/interface `{0,2}`;
- two path copies glued at both endpoints;
- reflection update `y -> 2-y` and source lift `x -> 3-x`.

All four assembled observations have two source states. The endpoint fibres
lose branch, while the two centre observations lose the fold-side bit.

### Square boundary channel

- `m=2`, `d=2`, embedded target grid `{0,1,2}^2`;
- envelope/interface is its eight-point boundary;
- two grids glued along that boundary;
- quarter-turn update `(x,y)->(y,2-x)` and source lift
  `(x,y)->(y,3-x)`.

The four corners have fibre size `2`; four edge midpoints plus the two
branch-distinct centre observations have fibre size `4`. Thus the assembled
profile is `4` fibres of size `2` and `6` fibres of size `4`, reconstructing
all `32` labelled source states.

## Decision boundary

This is a finite interface and information-accounting theorem. “Channel” means
the declared anchor quotient plus an admissible update. It does not mean a
physical conduit, dynamical stability, energy transport or historical visual
generator. Formal-design completion is not Study admission.
