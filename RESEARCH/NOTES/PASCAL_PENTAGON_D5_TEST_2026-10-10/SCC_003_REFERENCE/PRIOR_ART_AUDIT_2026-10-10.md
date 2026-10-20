# SCC-003 systematic prior-art audit

Date executed: `2026-10-10`  
Protocol: [`PRIOR_ART_PROTOCOL_2026-10-10.md`](PRIOR_ART_PROTOCOL_2026-10-10.md)  
Identity: `SCC-003 / A0OE:PASCAL_PENTAGON_D5_TEST`  
Status: `BOUNDED_SEARCH_COMPLETE_WITH_COVERAGE_LIMIT / NOT_ACTIVE / NO_NOVELTY_PROMOTION`

## Executive result

Primary outcome:

```text
CLOSE_BASELINE_FOUND_NO_EQUIVALENCE_ESTABLISHED
```

Coverage qualifier:

```text
SEARCH_INCOMPLETE_ACCESS_OR_COVERAGE_LIMIT
```

No inspected source supplied all five controlling features frozen in the
protocol: binomially weighted `(n,k)` positions, complete side-chain gluing,
cyclic five-face closure (or an immediate general `m=5` specialization), the
declared depth-six seam identifications, and the resulting typed quotient.

The strongest located baseline is the Hilton–Pedersen Pascal-Hexagon line of
work. It extends binomial coefficients across six triangular sextants,
preserves a Pascal identity inside the sectors, and explicitly studies
patterns crossing sector boundaries. It is therefore a genuine nearby
multi-sector Pascal construction. It does **not** define five copies of
`P_6`, the SCC-003 side-chain equivalence relation, an open five-face carrier,
or the `112 -> 106` quotient.

This result is not a proof of worldwide novelty or priority. It supports only
the narrower statement that no exact or controlling predecessor was located
within the declared search and accessible source text.

## Search execution

The frozen query families Q1–Q5 were executed with spelling, hyphen and plural
variants across:

- Crossref/DOI and publisher-indexed web results;
- arXiv records and primary preprints;
- zbMATH Open discovery results;
- MathSciNet public discovery surfaces;
- primary publisher, author and institutional full texts;
- backward chaining from the Pascal Hexagon, Pascal graph and binary
  Pascal-symmetry sources.

Representative exact probes included:

```text
"Pascal triangle" graph gluing quotient cyclic
"Pascal graph" amalgamation graph
"Pascal triangle" triangulated surface recurrence
Pascal triangle graph C5 cyclic five triangles gluing
binomial weighted triangular graph dihedral D5
Pascal triangle copies glued along boundary graph
"28, 49, 70, 91, 112" Pascal
"112" "106" Pascal graph
"106 vertices" Pascal graph
"five copies" "Pascal triangle" graph
```

The numeric probes produced only unrelated arithmetic-sequence, file-size or
generic graph-count collisions. They yielded no structurally relevant source.

## Strongest-baseline comparison

The detailed comparison is also exported as
[`PRIOR_ART_COMPARISON.csv`](PRIOR_ART_COMPARISON.csv).

| Rank | Source | Structural overlap | Decisive mismatch | Disposition |
|---|---|---|---|---|
| `B1` | Hilton, Pedersen & Rosenthal, *Pascalian triangles and extensions to hexagons* (1990), together with the accessible Pascal Hexagon construction | ordinary Pascal triangle as one triangular sextant; six triangular sectors; extended integer-index binomial values; Pascal identity; cross-sector patterns | six sextants of one extended array, not five finite copies; no complete side-chain quotient; no depth-six closure; no `C5/D5` typed graph | strongest baseline; no equivalence |
| `B2` | Quint, *Harmonic analysis on the Pascal graph* (2009) | a Pascal-derived graph; two infinite triangular copies are joined at their apex vertices; connected graph and explicit automorphism/spectral structure | erases even coefficients; infinite unweighted 3-regular topology; two copies, not five; only apex join; no SCC-003 seam quotient | close graph-theoretic baseline; no equivalence |
| `B2` | Brunat & Maureso, *Rotational and dihedral symmetries in Steinhaus and Pascal binary triangles* (2011) | Pascal recurrence on triangular positions; explicit rotational and dihedral symmetry | values in `F_2`; symmetry of a single triangle is `120°/240°` plus reflection; no five-copy gluing or quotient | symmetry baseline; no equivalence |
| `B2` | Barbé, *Symmetric patterns in the cellular automaton that generates Pascal's triangle modulo 2* (2000) | triangular grid, Pascal matrix modulo two and classified geometric symmetries | binary cellular-automaton patterns, not a finite binomially weighted seam quotient | contextual symmetry baseline |
| `B2` | Solares-Hernández et al., *Divisibility Patterns within Pascal Divisibility Networks* (2020) | Pascal matrices are used to construct finite networks and study graph metrics | vertices are distinct coefficient values (excluding `1`); edges encode divisibility, not Pascal recurrence or side-chain gluing | network baseline; no equivalence |
| `B4` | Horn, *Pascal Pyramids, Pascal Hyper-Pyramids and a Bilateral Multinomial Theorem* (2003) | higher-dimensional multinomial generalization of the Pascal triangle | simplex/hyper-pyramid extension rather than cyclic boundary quotient | contextual only |
| excluded | Dalfó et al., *Quotient-polynomial graphs* (2017) | general quotient partitions and quotient matrices in algebraic graph theory | no Pascal/binomial carrier; “quotient” has a different typed role | generic method only |

## Control-feature matrix

Legend: `Y` = explicitly present, `P` = partial/analogical overlap, `N` = not
present in the inspected definition.

| Source | `(n,k)` Pascal positions + ordinary weights | complete Pascal side-chain gluing | cyclic five faces / general `m` | apex + six depth-six seam pairs | typed weighted quotient |
|---|---:|---:|---:|---:|---:|
| SCC-003 | `Y` | `Y` | `Y` | `Y` | `Y` |
| Pascal Hexagon | `Y` | `P` | `N` | `N` | `N` |
| Quint Pascal graph | `P` | `N` | `N` | `N` | `N` |
| Brunat–Maureso | `P` | `N` | `N` | `N` | `N` |
| Barbé | `P` | `N` | `N` | `N` | `N` |
| Pascal divisibility networks | `P` | `N` | `N` | `N` | `N` |
| Pascal hyper-pyramids | `P` | `N` | `N` | `N` | `N` |

No row other than SCC-003 passes the controlling-predecessor test.

## Source notes

### B1 — Pascal Hexagon

The accessible primary construction defines ordinary Pascal's triangle as the
positive triangular sextant of a larger integer-index array, extends the
binomial values into six sextants, records a Pascal identity, and explicitly
targets patterns that cross sextant boundaries:

- <https://www.mi.sanu.ac.rs/vismath/hpe/hpe1.htm>
- Peter Hilton, Jean Pedersen and William Rosenthal, *Pascalian triangles and
  extensions to hexagons*, *Quaestiones Mathematicae* 13 (1990), 395–416,
  bibliographic record in the authors' reference list:
  <https://symmetry-us.com/Journals/hpe/ref1.htm>

This is the nearest structural comparison because it combines ordinary
binomial values, multiple triangular regions, symmetry and cross-boundary
continuation. Its six-sector extension is nonetheless a different object from
identifying the complete side chains of five finite Pascal carriers.

### B2 — Quint Pascal graph

Quint constructs an infinite connected planar 3-regular graph by retaining
the odd entries of Pascal's triangle, linking surviving neighbors, taking two
copies, and joining their apex vertices. This is the closest located source
that literally joins Pascal-derived triangular graphs:

- J.-F. Quint, *Harmonic analysis on the Pascal graph*, *Journal of
  Functional Analysis* 256 (2009), 3409–3460,
  <https://doi.org/10.1016/j.jfa.2009.01.011>
- author full text: <https://imag.umontpellier.fr/~quint/Publications/pascale.pdf>

The parity deletion, infinite 3-regular carrier and apex-only two-copy join
prevent specialization to SCC-003.

### B2 — binary rotational/dihedral Pascal triangles

Brunat and Maureso define generalized binary Pascal triangles from boundary
sequences and the usual local recurrence in `F_2`, then characterize
rotational and dihedral symmetry of a single triangular array. Their rotation
is the triangle's `120°/240°` action, not `C5`, and there is no seam quotient:

- <https://upcommons.upc.edu/bitstream/handle/2117/8718/rotationaldihedral.pdf>

Barbé's earlier cellular-automaton analysis likewise treats binary difference
patterns on a triangular grid and symmetries of a Pascal matrix modulo two:

- <https://doi.org/10.1016/S0166-218X(00)00211-0>

### B2 — Pascal divisibility networks

Solares-Hernández et al. build networks from Pascal matrices, but their nodes
are the non-repeated numerical values and an edge means divisibility in either
direction. This differs both from SCC-003's position vertices and its directed
Pascal-recurrence adjacency:

- <https://doi.org/10.3390/math8020254>

### B4 — Pascal pyramids and hyper-pyramids

Horn generalizes the binomial triangle to multinomial pyramids and arbitrary
dimensional hyper-pyramids. It supplies a standard higher-dimensional
neighbor, not a cyclic gluing or quotient baseline:

- <https://arxiv.org/abs/math/0311035>

### Excluded generic quotient terminology

The DOI previously captured during discovery,
`10.1016/j.laa.2015.09.053`, is *Quotient-polynomial graphs*. It studies
regular partitions, quotient matrices and association schemes; it does not
use a Pascal carrier. It is therefore not a prior-art comparator for the
candidate object:

- <https://doi.org/10.1016/j.laa.2015.09.053>

## Coverage limits

1. MathSciNet's public surface did not expose a usable full query result set in
   this environment; it cannot be claimed as exhaustively searched.
2. zbMATH Open discovery was web-index mediated rather than a complete saved
   database export.
3. Forward-citation coverage was not independently exported from Scopus or
   Web of Science.
4. Older non-digitized proceedings, dissertations, non-English sources and
   terminology not represented by the frozen synonyms may remain undiscovered.
5. No independent information scientist or mathematician has repeated the
   search.

For these reasons the result retains the explicit coverage qualifier even
though the accessible primary-source comparison is complete for the frozen
query families.

## Claim boundary after audit

Permitted internal wording:

> Within the frozen 2026-10-10 search, the closest located predecessor is a
> six-sextant Pascal-Hexagon extension; no inspected source defined the same
> five-face depth-six side-chain quotient or the `112 -> 106` closure.

Not permitted:

- “first”, “new”, “unique” or “unprecedented” without independent review;
- worldwide absence-of-prior-art claims;
- inference from the number `106` alone;
- treating the audit as publication authorization.

## Gate disposition

- `A0-BL-013`: `BOUND_WITH_COVERAGE_LIMIT`.
- systematic bounded comparison: complete for the frozen accessible search;
- exact/general predecessor: not located;
- strongest baseline: identified and compared;
- independent mathematical/literature review: still open;
- Human Owner paper/note decision: still open;
- SCC-003 lifecycle status: unchanged (`NOT_ACTIVE`, `NOT_ADMITTED`).

