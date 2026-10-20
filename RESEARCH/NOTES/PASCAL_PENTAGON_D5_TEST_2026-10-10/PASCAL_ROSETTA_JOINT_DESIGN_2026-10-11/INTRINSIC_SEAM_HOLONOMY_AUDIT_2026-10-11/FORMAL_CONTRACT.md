# Intrinsic seam / Z2 holonomy audit — formal contract

Date: `2026-10-11`  
Status: `FORMAL_AUDIT / NOT_ADMITTED / NOT_PENT_08`

## Bounded question

Does the frozen `SCC-003 / Q106` Pascal carrier determine a nontrivial
intrinsic orientation holonomy, or can Möbius return occur only after a seam
constraint is removed or added externally?

## Declared cellular object

The underlying quotient graph has `V=106` vertices, `E=180` undirected edges
and one connected component. Each raw Pascal commuting square

```text
        (n,k)
       /     \
 (n+1,k)   (n+1,k+1)
       \     /
      (n+2,k+1)
```

is declared as a diamond 2-cell after quotienting. There are

```text
5 faces * (1+2+3+4+5) = 75
```

such cells.

An orientation connection is an edge labeling

```text
omega:E(Q106)->Z2.
```

Local Pascal consistency requires even parity around every diamond boundary.
Gauge-equivalent labelings differ by a vertex sign assignment.

## Exact tests

1. Verify the frozen `106/180` carrier and connectivity.
2. Reconstruct all 75 four-edge diamond boundaries from raw incidences.
3. Compute the graph cycle rank `E-V+1` over `F2`.
4. Compute the rank of the diamond-boundary span.
5. Compute

   ```text
   dim H1 = E - rank(diamond constraints) - rank(vertex coboundaries).
   ```

6. Verify that all ten declared D5 automorphisms preserve the graph and the
   set of diamond cells.
7. Remove each single diamond as a non-symmetric cut control.
8. Partition diamonds into D5 orbits. For each complete orbit removal, solve
   for a D5-invariant edge labeling that is locally closed on all retained
   cells and has odd holonomy on the removed orbit.

## Decision rule

- nonzero `H1` with one D5-selected class: `UNIQUE_INTRINSIC_TWIST`;
- nonzero `H1` with several unselected classes: `MULTIPLE_NONCANONICAL_TWISTS`;
- zero intrinsic `H1`, but a compatible relaxed seam: `ONLY_AFTER_ADDED_SEAM`;
- zero intrinsic `H1` and no compatible relaxed seam: `NO_COMPATIBLE_TWIST`.

The audit stops at classification. It does not name `PENT-08`, select a seam
orbit or change the existing A0/PENT identity.
