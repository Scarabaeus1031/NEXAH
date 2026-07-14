# Phase V — IEEE Geometry Case and Research Testkit

Status: in progress; Orientation Brief foundation implemented

## Objective

Phase V turns the repository's strongest benchmark line into a concise,
reproducible, and scientifically bounded public case:

```text
IEEE benchmark model
→ ordered load campaign
→ typed physical snapshots
→ declared geometric views
→ orientation probes
→ evidence-bound report
→ reproducible showcase
```

The purpose is to help another person understand, run, inspect, and question
the case. The purpose is not to present a benchmark simulation as operational
grid evidence.

## Foundation — Orientation Brief

The backend-independent
[`OrientationBrief`](ORIENTATION_BRIEF_CONTRACT.md) contract is implemented
before IEEE-specific geometry. It turns an Orientation Report plus read-only
perspectives into a reproducible document containing the question, scope,
position, findings, disagreement, evidence, limits, and next questions.

Network Orientation is the executable reference path. The IEEE case will use
the same contract after work packages A–D produce its manifest, geometry frame,
operators, and probes.

## Phase boundary

Phase V is **IEEE benchmark evidence and repository usability**. It prepares an
observed-evidence bridge but does not require a real utility dataset in order to
close.

IEEE and PEGASE cases are standard benchmark models executed through
Pandapower. Their computed voltages, angles, flows, loading values, and solver
statuses are reproducible computational results. They are not measurements of
a live electrical grid and are not independently observed physical outcomes.

Therefore:

> **NO OBSERVED OUTCOME → NO EPISODIC MEMORY UPDATE**

A declared contingency, load change, removed line, failed solver run, or
training scenario must not be silently converted into real-world experience.

## Geometric working model

For a predeclared ordered load scale \(\lambda_i\), the coupled IEEE adapter
produces a physical snapshot:

```text
X(λᵢ) = [bus voltage, bus angle, active/reactive power,
         line loading, line flow, topology identity, solver status]
```

The campaign is a parameterized state family:

```text
T = { X(λ) | λ in the declared campaign }
```

The historical "tube" is retained as an explanatory metaphor for this state
family. It is not assumed to be a physical tube, a globally smooth manifold, or
a universal stability field.

A cross-section is a declared view or projection:

```text
Cⱼ(λ) = πⱼ(X(λ))
```

Examples include voltage profile, angle structure, line loading, bus/line
attribution, local state displacement, and distance to the last converged
sample. Every projection must declare its variables, units, normalization,
scope, and information loss.

## Work package A — Case protocol and freeze

Create a machine-readable case manifest before implementing new geometry:

- benchmark case and exact source version
- campaign parameter and ordered values
- variables, units, and missing-value policy
- development cases and untouched evaluation case
- predeclared projections and operators
- target claims and explicit non-claims
- environment and deterministic configuration

Previously inspected PEGASE-9241 is not a fresh held-out case for a new Phase V
method. A new evaluation case or a predeclared resampling protocol is required.

## Work package B — Typed geometry frames

Implement a minimal `IEEEGeometryFrame` around existing coupled snapshots. It
must contain:

- campaign position and axis semantics
- immutable topology identity
- physical variables with units
- convergence and failure record
- declared feature vector
- projection definitions
- provenance and uncertainty

The frame wraps existing evidence; it does not replace the coupled source or
reinterpret ordered load scale as time.

## Work package C — Minimal geometry operators

Begin with inspectable measurements:

- adjacent-state displacement
- normalized local drift
- path length along the sampled campaign
- direction change between adjacent displacements
- local discrete curvature where enough samples exist
- distance to the last converged sample
- agreement and disagreement between declared projections

Operators must return explicit insufficiency when sampling, alignment, or scale
does not support a value. No prime-number gates, fixed angular apertures,
universal return law, or control semantics are assumed.

## Work package D — IEEE orientation probes

Use the Phase IV read-only pattern:

1. **Physical-State Probe** — variables, limits, convergence, and missing data.
2. **Geometry Probe** — displacement, drift, curvature, and projection changes.
3. **Boundary Probe** — sampled numerical continuation and resolution limits.
4. **Evidence Probe** — provenance, units, configuration, and leakage checks.
5. **Claim Critic** — separates numerical, geometric, physical, and causal
   interpretations.

The probes share a representation identity and preserve disagreement. They do
not vote, execute, or mutate a simulation.

## Work package E — Outcome firewall

The testkit must distinguish three record types:

| Record | Example | May create an episode? |
|---|---|---:|
| `ScenarioRecord` | declared load increase or line removal | No |
| `ComputationResult` | Pandapower convergence, voltage, or flow | No |
| `ObservedOutcome` | independently sourced event after orientation | Yes |

Only an `ObservedOutcome` with valid temporal order, provenance, and scope may
enter the episodic-memory path. Benchmark computations remain canonical
validation records.

## Work package F — Validation ladder

1. deterministic unit fixtures for every geometry operator
2. one small IEEE development case with manually checkable values
3. multi-case campaign comparison without case-specific branches
4. failure and insufficient-resolution cases
5. frozen evaluation case with no parameter retuning
6. byte-reproducible machine-readable summary
7. claim audit against the case manifest

Negative and indeterminate results remain first-class outputs.

## Work package G — Public showcase set

Produce three entry depths from the same canonical artifacts:

- **90-second map** — what goes in, what is computed, and where evidence stops
- **10-minute runnable case** — one command, compact report, and four figures
- **research path** — methods, manifests, failures, evaluation, and open work

All showcase figures must be generated from versioned outputs. Promotional
visuals may explain the hypothesis, but they do not override the canonical
record.

## Work package H — Observed-evidence bridge

Document how a later operational or public measurement source would enter the
same contracts:

- acquisition and license
- timestamped topology and measurements
- entity alignment
- event definition
- independently recorded outcome
- privacy and redaction
- train/evaluation separation

This bridge is a Phase V deliverable. A real observed dataset is a later
evidence milestone and must not be fabricated to complete the benchmark case.

## Definition of done

Phase V closes when:

- the case manifest and outcome firewall are executable and tested
- one canonical IEEE geometry case runs from source to report
- geometry operators are minimal, typed, and failure-aware
- a new frozen evaluation gate is reproduced without retuning
- JSON, text, and figure artifacts derive from the same run
- a newcomer can reproduce the case from one documented command
- the 90-second, 10-minute, and research entry paths are published
- benchmark, simulation, observation, and outcome language remain distinct
- no scenario enters episodic memory as observed experience

## Beyond Phase V

The next evidence plateau applies the testkit to timestamped external
measurements and independently recorded outcomes. Only then can NEXAH test
outcome-linked learning or make claims about observed operational behavior.
