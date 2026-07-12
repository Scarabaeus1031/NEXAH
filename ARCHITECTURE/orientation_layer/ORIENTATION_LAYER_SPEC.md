# Orientation Layer Specification

Status: normative planning baseline; WP1 contracts implemented
Scope: contracts and component boundaries, not a claim of implementation

## Purpose

The Orientation Layer converts observations and backend representations into a
traceable account of a system's present position, relevant change, available
options, missing information, evidence, and uncertainty. Its default output is
decision support, not autonomous execution.

## System boundary

```text
observations + context + goals + constraints
                    ↓
         representation backend
                    ↓
             orientation core
                    ↓
            orientation report
                    ↓
       human or external decision layer
```

Backends may include the frozen v0.7 package, the verified Demonstrator, or a
domain adapter. Backend-specific state identifiers and confidence measures must
retain their scope and provenance.

## Normative responsibilities

### Input and context

Carries observations, timestamps, provenance, reference frame, domain context,
goals, and constraints. It must not invent missing domain meaning.

### Representation backend

Produces a documented representation such as an embedding, state graph, field,
or transition model. Every backend declares whether its map is local or
persistent and what its identifiers mean.

### Q° Orientation Core

Q° is the architectural name for the component that combines context, maps,
memory, options, evidence, and uncertainty. In the MVP it is a typed software
contract and orchestration boundary, not a universal equation or intelligence
claim.

### Orientation Report

Reports:

- where the system appears to be
- what changed and under which representation
- observed regimes or transition indicators
- reachable and blocked options
- related prior episodes, if available
- missing information and assumptions
- evidence references and uncertainty

### Decision support and execution

Decision support compares options and explains trade-offs. Execution is opt-in,
external to the core, and must receive explicit authorization and safeguards.

### Outcome and learning

Observed outcomes may become provenance-preserving episodes. Learning must be
auditable and reversible; the MVP does not silently mutate backend models.

## Core contracts

The field names below define the intended information boundary. Their initial
Python contracts are implemented in `nexah/orientation/`; backend population of
those contracts begins in WP2.

```text
OrientationState
  observations
  representation
  location
  reference_frame
  context
  goals
  constraints
  map
  episodes
  options
  evidence
  uncertainty
  timestamp
  provenance

OrientationReport
  position
  change
  regimes
  reachable_options
  blocked_options
  similar_episodes
  missing_information
  assumptions
  evidence_references
  uncertainty
  explanation
  timestamp
```

## Primitive language

The initial vocabulary is: Observer, ReferenceFrame, Context, State,
Transition, Regime, Map, Time, Operator, Similarity, Goal, Constraint, Option,
Evidence, Uncertainty, Episode, and Outcome.

Each primitive requires an operational definition before it becomes part of the
public API. Symbolic or book-level uses do not automatically define software
semantics.

## JANUS separation

- **JANUS** is the principle that one reality may require complementary
  perspectives. It is not an algorithm.
- **Janus Bridge** is an architectural translation interface between
  representations.
- **Janus Directional Coherence Operator** is a scientific forward/backward
  trajectory analysis.

The Bridge and Operator are sibling realizations of the principle. Neither is
the automatic implementation of the other. See ADR 0001.

## Evidence requirements

Every orientation claim must link to observations, assumptions, method,
representation scope, provenance, and uncertainty. Evaluation spans
characterization tests, baselines, reproducibility, domain validation, and
recorded failure cases.

## Explicit non-goals for the MVP

- a universal orientation equation
- all-domain intelligence
- autonomous action by default
- a simulation of biological brain structures
- a general meaning engine
- production control guarantees
