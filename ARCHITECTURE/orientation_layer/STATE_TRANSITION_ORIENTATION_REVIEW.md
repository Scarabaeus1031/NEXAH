# Architecture Review — Observed States, Transition Relations, Boundaries, and Orientation

Status: architectural review of the V5 development state  
Date: 2026-07-14  
Scope: static repository assessment; no implementation decision and no
scientific validation

## Review question

Does the current NEXAH architecture naturally support a future mathematical
interpretation based on observed state trajectories and relationships between
successive states?

## Short conclusion

Yes, with an important qualification.

The repository already separates represented states from directed relations,
ordered campaigns, graph paths, continuation branches, boundary records, and
outcome-linked episodes. It is therefore no longer only a collection of
isolated observed states.

It does **not** yet implement one representation-independent mathematical
`TransitionSpace`. The current architecture contains several compatible but
distinct relational structures. The conservative interpretation is:

```text
input records
→ representation-specific state set
→ observed or computed transition relation
→ ordered paths and trajectory families
→ explicit boundary records
→ evidence-bound orientation report
```

Established terms such as *transition relation*, *directed edge set*, *path
space*, *trajectory family*, and *continuation branch* are sufficient at the
current maturity level.

## Existing abstraction layers

### 1. Input domain

`nexah.sources.SourceBatch` preserves ordered numeric observations, declared
features, provenance, quality facts, and the semantic row axis. The axis may be
`ordered_sample`, `time`, `entity`, or `event`; row succession is therefore not
silently equated with physical time.

The coupled IEEE source reinforces this distinction by separating entity-indexed
bus and line snapshots from an ordered load campaign. Its load scale is an
ordering parameter, not a dynamic time coordinate.

This is an explicit architectural input boundary. It is not yet one universal
mathematical input space.

### 2. State representation

`StateRef` identifies a state inside a declared scope. `OrientationState`
contains observations, representation, reference frame, context, map,
uncertainty, provenance, and an optional current location.

State identity is representation-dependent. In particular, v0.7 cluster
identifiers are local to one fit. IEEE geometry frames instead preserve a
campaign position, load scale, physical entity views, feature vector, topology
identity, solver status, provenance, and uncertainty.

The repository therefore contains multiple state representations rather than
one global state space.

### 3. Transition relation

The primitive `Transition` is distinct from `StateRef` and contains source,
target, optional probability, and evidence references. `BackendResult` keeps
the `OrientationState` and its transition collection as separate fields.

The v0.7 adapter creates an empirical directed transition map between local
cluster states. The graph backend represents declared directed edges and
derives paths, reachability, strongly and weakly connected components,
articulation points, and focus-relative critical edges.

These components establish a real relational layer. They do not yet share a
common transition identity, parameter contract, status vocabulary, or
cross-representation persistence rule.

### 4. Ordered paths and trajectory families

The repository preserves order in several forms:

- source trajectories and ordered frames;
- parameter sweeps and IEEE load campaigns;
- v0.7 embedded sequences and empirical transitions;
- baseline-anchored continuation branches;
- graph paths and path changes;
- replayable validation records and append-only episode history.

Order is additional information: the same states in another order constitute a
different path. The natural mathematical objects are currently discrete paths,
directed graph paths, continuation branches, and parameterized state families.

The Phase V IEEE testkit already uses the careful formulation
`X(lambda_i)` and calls the campaign a parameterized state family. It explicitly
does not assume a physical tube, a globally smooth manifold, or a universal
stability field.

### 5. Boundary records

Boundaries are preserved as positive information in several forms:

- a terminal non-converged continuation point;
- the interval between the last converged and first failed point;
- a failed IEEE geometry frame without fabricated physical values;
- an unreachable node or blocked option in a declared directed graph;
- missing information and explicit assumptions in an Orientation Report;
- unknown or interval uncertainty;
- validation boundaries and right-censored branches.

These are currently data, derived structural facts, and metadata. They do not
form one mathematical boundary space or one topology. A solver boundary, graph
cut, sampling limit, and epistemic unknown must not be treated as equivalent.

### 6. Orientation

Orientation is neither only a property of an isolated state nor currently a
coordinate in another mathematical space.

The current report generators begin at a scoped position and evaluate directed
relations relative to that position. They report change, reachable and blocked
options, regimes or structural indicators, similar episodes, missing
information, assumptions, evidence, and uncertainty.

The implemented behavior is therefore best described as a **state-anchored,
contextual, relational evaluation**:

```text
orientation = evaluation(
    position,
    representation,
    relations,
    boundaries,
    evidence,
    uncertainty,
    context,
    query,
)
```

The output is an inspectable `OrientationReport`, not an oracle, controller, or
universal orientation coordinate.

## Does an implicit Transition Space exist?

An implicit transition **layer** exists. A single mathematical transition
**space** does not yet exist.

The existing instances match several established structures:

| Repository structure | Conservative mathematical match |
|---|---|
| v0.7 local states and weighted transitions | finite directed weighted graph / empirical transition relation |
| declared network nodes and edges | directed graph and combinatorial path space |
| ordered IEEE frames | discrete parameterized state family |
| continuation branch | ordered continuation sequence with censoring or a bracketed boundary |
| graph snapshot comparison | structural delta between two directed graphs |
| append-only episodes | ordered, outcome-linked records; not model dynamics |

A Markov process would require a justified probabilistic transition kernel and
additional assumptions. An optional transition probability alone does not
establish that structure.

## Geometry of observed trajectories

One ordered campaign can become a discrete curve or polygonal path after a
representation and distance rule are declared. Multiple campaigns can be
treated as a trajectory family or an ensemble, and graph paths form a
combinatorial path space.

The repository does not currently justify calling such collections a manifold,
fiber bundle, tube, smooth flow, or vector field. Those terms would require
additional structure such as topology, charts, smoothness, compatible
parameterization, base/fiber maps, or a declared local dynamics.

Geometry can be added representation by representation. It must not be inferred
merely from the existence of ordered observations.

## JANUS interpretation

Every directed transition has a source and target. This gives it two endpoint
roles, but not an automatic inverse:

```text
A → B does not imply B → A
```

The architecture already separates:

1. **JANUS** — the complementary-perspective principle;
2. **Janus Bridge** — a planned translation between representations;
3. **Janus Directional Coherence Operator** — experimental forward/backward
   local-flow analysis.

The scientific operator compares a forward and backward local difference around
a centered trajectory position. That generally requires three ordered samples;
it is not the inverse of one graph edge. The Janus Bridge remains a planned
architecture concept and must not be presented as implemented by that operator.

## Compatibility of the proposed hierarchy

| Proposed name | Current correspondence | Assessment |
|---|---|---|
| Input Space | adapters, batches, axes, source context | compatible as an architectural domain; not one mathematical space |
| State Space | scoped backend states and geometry frames | present, but representation-specific |
| Transition Space | transitions, edges, branches, adjacent frames | implicit relational layer; no unified space |
| Boundary Space | failure frames, refined intervals, blocked paths, uncertainty | first-class records; no common topology |
| Orientation Space | state, relations, context, evidence, report | implemented as evaluation and report, not as a space |

The hierarchy is useful as an architectural map if the word *space* is not
mistaken for an already defined topological, metric, or smooth space.

## Missing abstractions

Before the relational interpretation can become a binding mathematical or
kernel contract, the following are missing:

1. a common typed transition identity with source, target, parameter semantics,
   status, evidence, uncertainty, and representation scope;
2. an explicit path contract containing a composable ordered sequence rather
   than only a list of frames;
3. a distinction between observed, computed, interpolated, declared, and
   hypothetical transitions;
4. explicit reversal semantics separating reverse observation, reversed view,
   and mathematical inverse;
5. a boundary taxonomy that does not conflate solver, sampling, structural,
   epistemic, and domain limits;
6. path-family identity and alignment across campaigns;
7. declared representation maps and recorded information loss;
8. scoped metrics or topology where a geometric interpretation is needed;
9. persistent identity rules across local fits and representations;
10. explicit query/focus semantics for orientation.

## Critical assessment

The architecture naturally supports continued work on observed state
relationships. It does not require new universal terminology, and it does not
currently support claims of a universal transition geometry.

The strongest defensible direction is an evidence-bound, representation-aware
formalism for heterogeneous state-transition systems with explicit boundaries.
That direction is compatible with the existing kernel, but it remains research
until its objects, invariants, and relation to established frameworks are made
precise.

## Repository evidence reviewed

- [`ORIENTATION_LAYER_SPEC.md`](ORIENTATION_LAYER_SPEC.md)
- [`CONCEPT_TRACEABILITY.md`](CONCEPT_TRACEABILITY.md)
- [`DECISIONS/0001-janus-identities.md`](DECISIONS/0001-janus-identities.md)
- [`SOURCE_ADAPTER_CONTRACT.md`](SOURCE_ADAPTER_CONTRACT.md)
- [`PHASE_IV_NETWORK_ORIENTATION.md`](PHASE_IV_NETWORK_ORIENTATION.md)
- [`PHASE_V_IEEE_GEOMETRY_TESTKIT.md`](PHASE_V_IEEE_GEOMETRY_TESTKIT.md)
- [`../../nexah/orientation/`](../../nexah/orientation/)
- [`../../nexah/backends/`](../../nexah/backends/)
- [`../../nexah/power_systems/`](../../nexah/power_systems/)
- [`../../validation/`](../../validation/)

