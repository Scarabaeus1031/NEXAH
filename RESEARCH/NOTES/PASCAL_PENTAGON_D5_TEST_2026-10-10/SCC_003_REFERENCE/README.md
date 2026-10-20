# SCC-003 canonical reference package

Status: `REFERENCE_OBJECT / REPRODUCIBILITY_INFRASTRUCTURE / NOT_ADMITTED / NOT_ACTIVE`

This package completes the first two preparation priorities for the existing
`SCC-003 / A0OE:PASCAL_PENTAGON_D5_TEST` identity:

1. an implementation-independent formal specification and compact proof
   package; and
2. a deterministic 106-node reference export with a separate verifier.

It creates no `PENT-08`, no new Study, no generalized family run and no claim
promotion.

Priority 3 is now documented as a separate bounded literature audit. It
located close baselines but no exact or controlling predecessor in the
declared accessible search. The result retains an explicit database-coverage
limit and does not establish worldwide novelty.

## Formal package

- [FORMAL_SPECIFICATION.md](FORMAL_SPECIFICATION.md)
- [PROPOSITIONS_AND_PROOFS.md](PROPOSITIONS_AND_PROOFS.md)

## Prior-art package

- [PRIOR_ART_PROTOCOL_2026-10-10.md](PRIOR_ART_PROTOCOL_2026-10-10.md)
- [PRIOR_ART_AUDIT_2026-10-10.md](PRIOR_ART_AUDIT_2026-10-10.md)
- [PRIOR_ART_COMPARISON.csv](PRIOR_ART_COMPARISON.csv)

Audit outcome:

```text
CLOSE_BASELINE_FOUND_NO_EQUIVALENCE_ESTABLISHED
SEARCH_INCOMPLETE_ACCESS_OR_COVERAGE_LIMIT
```

## Reference artifacts

The generated [artifacts](artifacts/) contain:

- `nodes.csv` — canonical 106-node list;
- `edges.csv` — 180 directed quotient edges;
- `weights.csv` — binomial quotient weights;
- `face_incidence.csv` — all 140 raw Pascal positions and their quotient IDs;
- `face_edges.csv` — all 210 facewise recurrence-edge incidences;
- `seam_classes.csv` — the apex and thirty nontrivial seam classes;
- `adjacency_matrix.csv` — directed `106 x 106` adjacency matrix;
- `underlying_graph.g6` — graph6 serialization of the underlying simple graph
  in the declared node order;
- `automorphisms.json` — the ten typed `D_5` permutations;
- `expected_metrics.json` — expected counts and fingerprints;
- `manifest.json` and `SHA256SUMS` — artifact byte counts and SHA-256 hashes;
- `VERIFICATION.json` — result of the separate verifier.

The graph6 value is a deterministic reference serialization, not by itself a
canonical-label certificate for arbitrary relabelings. Reconstruction checks
use the full typed package plus hashes.

## Rebuild and verify

From this directory:

```sh
python3 generate_reference.py
python3 verify_reference.py
```

The generator uses direct canonical formulas. The verifier does not import
the generator: it independently reconstructs the equivalence relation with
union-find, then checks all exported tables, hashes and propositions.

Expected terminal summaries:

```text
{"artifacts": 11, "edges": 180, "nodes": 106, "status": "PASS"}
{"checks": 177, "failures": [], "status": "PASS"}
```

## Completion test

A third party needs only Python 3 and this directory to reconstruct the
106-node carrier, verify `28,49,70,91,112 -> 106`, check the typed `D_5`
action, and compare the resulting serialization and SHA-256 manifest. No HTML
Explorer is required.

