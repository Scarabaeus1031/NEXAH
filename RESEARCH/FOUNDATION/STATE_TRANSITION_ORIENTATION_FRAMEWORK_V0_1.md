# Evidence-Bound Orientation over Heterogeneous State–Transition Systems

## Mathematical Framework Note v0.1

Status: non-normative research note  
Date: 2026-07-14  
Maturity: candidate vocabulary and formalization; no novelty, theorem, or
universality claim

## Purpose

Existing mathematics already provides state spaces, transition systems,
directed graphs, Markov processes, path spaces, bifurcations, uncertainty
models, projections, and representation theory.

The open NEXAH question is not whether another mathematical “space” can be
named. It is whether heterogeneous representations can be connected while
preserving order, boundaries, evidence, uncertainty, and the limits of each
claim.

A candidate description is:

> An evidence-bound framework for contextual orientation over heterogeneous
> state-transition systems with explicit boundaries.

The candidate central statement is:

> **Orientation is a context-dependent evaluation of which statements about
> position, change, paths, and boundaries are supported by a declared
> representation, its evidence, assumptions, and uncertainty—and which
> statements remain unsupported.**

This note defines a minimal object language for investigating that possibility.
It does not make the language part of the public kernel API.

## Non-assumptions

The framework does not initially assume:

- one universal state space;
- physical time as the ordering parameter;
- a metric, topology, manifold, bundle, or smooth flow;
- reversible dynamics;
- a probabilistic or Markov process;
- causal interpretation of observed succession;
- a universal geometry across representations;
- complete observations;
- solver failure as a physical system boundary;
- automatic semantic equivalence between representations;
- autonomous decision or control authority.

## 1. Representation-indexed state systems

Let \(R\) be a set of declared representations. For each \(r\in R\), let

\[
X_r
\]

be the set of states expressible in representation \(r\).

Examples may include a physical IEEE frame, a feature vector, a graph node, a
locally fitted cluster state, or a report-level reference. These are not assumed
to share coordinates, metrics, or persistent identity.

Using a family \(\{X_r\}_{r\in R}\) avoids prematurely treating heterogeneous
representations as one universal state space. If a combined carrier is needed,
it may be represented as a tagged disjoint union while retaining the
representation identity:

\[
X = \bigsqcup_{r\in R}\{r\}\times X_r.
\]

## 2. Typed transitions

For each representation \(r\), a transition relation may be written as

\[
T_r \subseteq X_r\times X_r.
\]

A transition record should preserve more than its endpoints. A candidate typed
record is

\[
\tau=(id,s,t,a,k,e,u,r),
\]

where:

- \(s\) and \(t\) are source and target states;
- \(a\) declares ordering or parameter semantics and, where available, its
  interval;
- \(k\) classifies the transition as observed, computed, declared,
  interpolated, or hypothetical;
- \(e\) references evidence and provenance;
- \(u\) records uncertainty or explicit unknown uncertainty;
- \(r\) records the representation scope.

This is a candidate common denominator. It does not imply that a graph edge, a
continuation step, and an empirical cluster transition have identical domain
meaning.

An optional probability does not by itself define a Markov kernel. Probability
normalization, conditioning, parameter semantics, and the relevant assumptions
would have to be declared separately.

## 3. Paths as primary relational objects

A finite path is a composable sequence

\[
\gamma=(\tau_1,\tau_2,\ldots,\tau_n)
\]

such that

\[
t(\tau_i)=s(\tau_{i+1})
\]

whenever both endpoints are defined in the same representation and identity
scope.

Path identity must preserve:

- ordering;
- parameter semantics;
- representation scope;
- evidence lineage;
- uncertainty;
- interruptions, censoring, and failed positions;
- any declared alignment to source observations.

Two paths containing the same set of states may remain different because their
order, evidence, parameterization, boundary encounters, or representation
differ.

Let \(\Pi_r\) denote a declared family of allowed or observed paths in
representation \(r\). This is a path or trajectory family, not automatically a
smooth path space.

## 4. Explicit boundary records

Boundaries should not initially be identified with one mathematical boundary
operator. A candidate `BoundaryRecord` attaches a scoped limit to a state,
transition, path segment, parameter interval, representation, or query.

Useful facets include:

- solver or computational failure;
- sampling or resolution limit;
- structural cut or reachability boundary;
- censoring or incomplete continuation;
- epistemic unknown;
- representation boundary;
- domain-of-validity boundary.

These facets need not be disjoint. One record may represent a solver failure
that also terminates sampling while leaving the physical interpretation
unknown.

For example, an IEEE boundary record may preserve

\[
b=(\lambda_{last\;converged},\lambda_{first\;failed},
type,evidence,resolution,uncertainty).
\]

This does not identify the interval with a certified physical bifurcation.

## 5. Evidence and uncertainty

Let \(\mathcal E\) denote the evidence and provenance structure, and let \(U\)
denote uncertainty records or attachment rules.

Evidence and uncertainty should be attachable to states, transitions, paths,
boundaries, representation maps, and orientation statements. They need not use
one numerical confidence scale.

An explicit unknown is a valid result. Lack of calibrated uncertainty must not
be replaced by an invented probability.

## 6. Representation maps

For selected pairs \(r,s\in R\), a partial representation map may be declared:

\[
F_{r\rightarrow s}:D_{rs}\subseteq X_r\longrightarrow X_s.
\]

Such maps may be non-injective, non-surjective, partial, or information-losing.
They therefore require:

- source and target representation identities;
- a declared domain;
- transformation method and parameters;
- provenance;
- information-loss statement;
- uncertainty and failure behavior.

No inverse is implied by the existence of a reverse map.

## 7. JANUS and round-trip consistency

The accepted repository separation remains in force:

- **JANUS** is a complementary-perspective principle;
- **Janus Bridge** is an architectural translation between representations;
- **Janus Directional Coherence Operator** is a scientific local-flow analysis.

A future Janus Bridge may permit investigation of a round trip

\[
x\xmapsto{F_{r\rightarrow s}}y
 \xmapsto{F_{s\rightarrow r}}\hat{x}.
\]

If representation \(r\) supplies an appropriate comparison rule, the difference
between \(x\) and \(\hat{x}\) could characterize round-trip inconsistency or
representation loss.

This is a research candidate, not the definition of JANUS, not an assumed
inverse, and not the current Directional Coherence Operator.

## 8. Optional representation-dependent geometry

Geometry enters only after appropriate structure is declared. A representation
may define one or more scoped comparison rules:

\[
d_X^{(r)}(x_i,x_j),\qquad
d_T^{(r)}(\tau_i,\tau_j),\qquad
d_\Pi^{(r)}(\gamma_i,\gamma_j).
\]

These may be metrics, pseudometrics, divergences, edit distances, or other
domain-appropriate comparisons. They are not assumed interchangeable.

Examples might include physically normalized feature distance for an IEEE
campaign or combinatorial distance for a directed graph. Every choice must state
its variables, units, normalization, invariances, information loss, provenance,
and validity scope.

The family

\[
\mathcal G=\{G_r\}_{r\in R}
\]

is therefore a collection of declared representation geometries, not one true
universal geometry.

## 9. Contextual orientation

Let \(C\) contain context and let \(q\) be an explicit orientation query. The
query may include a focus state, reference frame, target, goals, constraints,
and the question being asked.

A candidate evidence-bound system description is

\[
\mathcal N=
(R,\{X_r\},\{T_r\},\{\Pi_r\},B,\mathcal E,U,C,\{F_{r\rightarrow s}\}).
\]

Orientation is then not assumed to be a point in another space. It is initially
an evaluation:

\[
\mathcal O(\mathcal N,q)\longrightarrow Report.
\]

The report may contain:

- the scoped current position;
- represented change;
- reachable and blocked paths;
- relevant boundaries;
- representation and context;
- supporting and conflicting evidence;
- uncertainty and missing information;
- prior outcome-linked episodes;
- statements that are not justified by the available structure.

The evaluation may be partial or return insufficiency. It does not guarantee an
answer, prescribe an action, or convert a scenario into an observed outcome.

Equivalently, the report can be viewed schematically as preserving three
classes of result:

\[
\mathcal O(\mathcal N,q)
\longrightarrow
\bigl(\text{supported statements},\text{unsupported statements},
\text{boundaries}\bigr).
\]

Support remains relative to the declared representation, context, query,
evidence, assumptions, uncertainty, and validity scope. Structural reachability
must not be silently promoted to physical feasibility, causal influence,
recommended action, or an observed outcome.

## 10. Candidate contribution

No individual component is proposed as new. The candidate contribution is their
strict integration:

- heterogeneous, explicitly scoped representations;
- transitions as first-class typed records;
- evidence-preserving paths;
- explicit and differentiated boundaries;
- evidence and uncertainty attached to claims;
- multiple read-only perspectives;
- contextual orientation rather than context-free prediction;
- no automatic equivalence of order, time, probability, or causality.

Whether this combination is novel requires a dedicated literature review. In
particular, it should be compared with labelled and partial transition systems,
hybrid systems, coalgebraic models, attributed and provenance graphs,
belief-state approaches, categorical system representations, and related
multi-representation formalisms.

## 11. Connection to the current repository

The current kernel already provides bounded realizations of parts of this
candidate model:

| Candidate object | Current repository realization |
|---|---|
| representation identity | `RepresentationRef`, `MapRef`, backend scope |
| represented state | `StateRef`, `OrientationState`, IEEE geometry frame |
| directed relation | `Transition`, `GraphEdge`, empirical transition map |
| ordered family | `SourceBatch`, IEEE campaign, geometry campaign, continuation branch |
| boundary record | failed frame, `RefinedBoundary`, blocked option, uncertainty |
| evidence structure | `Evidence`, `Provenance`, evidence references |
| contextual evaluation | report generators and `OrientationReport` |
| history | immutable State–Report–Outcome `Episode` and append-only store |
| representation bridge | planned; not yet a common kernel contract |

The architecture review governing this mapping is
[`../../ARCHITECTURE/orientation_layer/STATE_TRANSITION_ORIENTATION_REVIEW.md`](../../ARCHITECTURE/orientation_layer/STATE_TRANSITION_ORIENTATION_REVIEW.md).

## 12. Open research questions

1. What is the minimal common transition record that remains useful across
   temporal, parameterized, and graph-native systems?
2. When are transitions composable across representation boundaries?
3. How should identity survive a lossy representation change?
4. Which boundary facets are exclusive, overlapping, or hierarchical?
5. How should interrupted and right-censored paths be represented?
6. What comparison structures are justified for states, transitions, and paths
   in each domain?
7. Can orientation statements be checked for monotonicity under loss or gain of
   evidence?
8. How should contradictory read-only perspectives be represented without
   voting them into truth?
9. Which properties belong to an orientation query, and which belong to the
   underlying represented system?
10. Which parts of this model duplicate established frameworks and should be
    adopted rather than renamed?

## 13. Possible later kernel contracts — not decisions

The following are candidates for later architectural evaluation only:

- `TypedTransition`;
- `OrderedPath` or `TrajectoryRecord`;
- `BoundaryRecord`;
- `RepresentationMap`;
- `OrientationQuery`;
- explicit path-family and alignment identity.

No candidate in this list is approved by this note. Adoption requires review of
usefulness, compatibility, invariants, migration cost, and existing mathematical
terminology. A binding decision, if justified, belongs in a later ADR.
