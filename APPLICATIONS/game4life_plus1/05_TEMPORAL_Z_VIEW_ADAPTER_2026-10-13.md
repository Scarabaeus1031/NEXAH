# Temporal Z Cylinder — Post-Close View Adapter

Date: `2026-10-13`  
Status: `IMPLEMENTED_INTERNAL_VIEW_ADAPTER / NON-EVIDENTIARY`  
Reused Study identity: `NEXAH_LIFE_BOUNDARY_CYLINDER_LIFE08_2026_10_11`

## Coordinate contract

For an addressed event `(x,y,g)` on a declared `cylinder-x` or `cylinder-y`
carrier, the adapter renders

```text
theta = 2*pi*wrapped_address/N
radius = R + lane_depth*other_address/(N-1)
z = scaled(g-first_generation)
```

Thus no source coordinate is discarded: the wrapped coordinate becomes angle,
the other spatial coordinate becomes a radial lane, and discrete generation
becomes world Z. Birth, survival and death retain the existing event alphabet
and persistent event IDs. Green segments join the same native address only
across adjacent discrete generations.

## Animation and export boundary

The moving Z sweep is visual interpolation. It is not a Life state, does not
alter B3/S23 and is excluded from scientific interpretation. The GLB export
stores axis semantics, address sources, generation interval, boundary,
`projection_only=true` and `rule_unchanged=true` as extras.

## Authority effect

- new Life rule: `NO`
- Study reopen: `NO`
- new Navigator node or relation: `NO`
- canonical count effect: `NONE`
- source authority: unchanged closed LIFE08 run and result

This record extends the application view surface only. It does not modify the
2026-10-12 frozen snapshot or its receipts.
