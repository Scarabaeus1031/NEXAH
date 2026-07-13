# Phase IV — Network Orientation Application

Status: V2 read-only learning probes and illustrative validation complete

## Objective

Phase IV moves the Orientation Layer from a source-adapter ecosystem into its
first non-temporal graph application. The objective is learning through
structure and comparison, not control:

```text
observe → represent → orient → compare → remember → learn
```

## Implemented path

```text
GraphSourceAdapter
→ GraphRepresentationBackend
→ GraphAnalysis
→ Network Orientation Report
→ structural snapshot comparison
→ Supply Chain development fixture
→ Ecosystem held-out fixture
```

### Work package A — Graph representation backend

Implemented in `nexah/backends/graph.py`.

The backend accepts only entity-indexed square adjacency batches. Declared node
identifiers remain persistent within the graph representation. Non-zero entries
become directed edges, not transition probabilities.

Computed descriptions:

- directed reachability and shortest paths
- strong and weak components
- in-degree and out-degree
- dead ends
- weak articulation points
- focus-relative reachability-critical edges

No regime, risk, stability, or action meaning is inferred.

### Work package B — Structural orientation report

Implemented in `nexah/applications/network_orientation.py`.

The report preserves the generic `OrientationReport` contract and adds a
machine-readable `GraphAnalysis` companion. Reachable options mean only that a
declared directed path exists. Blocked means absent from the supplied map, not
impossible in reality.

### Work package C — Comparison and training context

The application compares baseline and current graph snapshots. It records
added, removed, and reweighted edges; newly reachable or unreachable nodes; and
changed shortest paths.

The CLI can generate one explicit edge-removal training scenario. This is a
counterfactual structural comparison, not causal evidence and not an external
intervention.

### Work package D — Supply-chain application

`nexah orient-network` provides JSON and compact text outputs. The repository
supply-chain graph is the development fixture. Its authored regime, collapse,
risk, action, and shock metadata remain outside the typed source boundary.

### Work package E — Held-out ecosystem transfer

The unchanged source adapter, backend, and application process the ecosystem
food-web graph. The held-out gate demonstrates domain-blind software reuse over
the shared graph schema. Both inputs are illustrative and use the same
bidirectional five-node chain pattern, so the result is neither real-world
cross-domain validation nor evidence of transfer to a new graph family.

## Canonical result

The frozen validation is in
**[validation/network_orientation_v1](../../validation/network_orientation_v1/)**.

- Supply Chain: all four other nodes are reachable from `normal_operation`.
- Training scenario: removing
  `production_slowdown → distribution_backlog` makes two downstream nodes
  unreachable from the focus.
- Ecosystem held-out: the unchanged path finds all four other declared nodes
  and the target path from `balanced_ecosystem` to `ecosystem_collapse`.

## Scientific boundary

Supported:

- deterministic topology analysis of declared directed graphs
- persistent declared node identity within one representation
- evidence-bound reachability and connectivity reports
- structural sensitivity comparison
- domain-blind contract reuse across two illustrative fixtures

Not supported:

- complete or operational models of either domain
- generalization to topologically distinct network families
- empirical stability or resilience estimates
- causal effects of edge removal
- outcome prediction
- control recommendations or autonomous execution

## Next plateau — Multi-perspective learning probes

### Work package F — Probe contract

Implemented in `nexah/orientation/probes.py`. A `ProbeResult` binds one named
perspective to a representation, evidence references, assumptions, missing
information, uncertainty, and provenance. `read_only=False` is rejected at the
contract boundary.

### Work package G — Five network perspectives

Implemented in `nexah/applications/network_probes.py`:

- reachability and paths
- structural bottlenecks
- declared snapshot perturbation
- evidence and provenance
- claim-boundary criticism

These are deterministic analytical perspectives, not autonomous agents or
domain authorities.

### Work package H — Transparent synthesis

All findings remain inspectable. Two probes taking the same stance on the same
narrowly named subject create an agreement record. Support/challenge conflict
creates a contradiction record. The synthesis does not vote, silently resolve
disagreement, or mutate the graph.

`NetworkLearningContext` deliberately records `outcome_recorded=False`.
Episodic memory requires a later observed `Outcome`; a declared training
scenario is not converted into one.

### Work package I — V2 topology validation

The canonical V2 record is in
**[validation/network_orientation_v2](../../validation/network_orientation_v2/)**.
It preserves V1 and adds a synthetic graph with two branches, a merge, a
directed cycle, a target leaf, and an isolated node. Removing the one declared
edge to the target makes only that target newly unreachable. This demonstrates
broader deterministic topology coverage, not real-world generalization.

## Next evidence plateau

Phase IV's software and illustrative gates are complete. The next increase in
claim strength requires independently acquired graph or event data, explicit
source-completeness evidence, and a genuinely observed outcome. The direction
remains learning, training, and improved orientation—not control authority.
