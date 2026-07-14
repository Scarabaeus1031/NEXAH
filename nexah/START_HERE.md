# Start with the NEXAH Kernel

The NEXAH Kernel is an evidence-bound orientation layer for complex systems.
It turns declared observations into inspectable maps, comparisons, reports,
and learning context while keeping evidence, uncertainty, and authority
explicit.

```text
observations
→ typed representation
→ structure and relationships
→ orientation from a declared position
→ evidence-bound explanation
→ human review
```

NEXAH helps a user ask where a system is, how its observed structure changed,
what is reachable in the supplied representation, what information is missing,
and which conclusions the evidence does not support. It is not an oracle,
causal authority, or autonomous controller.

## Choose your entry

| You want to… | Start here |
|---|---|
| Orient and compare a declared network | [Network Orientation](../APPLICATIONS/network_orientation/README.md) |
| Inspect an ordered IEEE benchmark campaign | [IEEE Geometry V1 Showcase](../APPLICATIONS/power_systems/ieee_geometry_v1/showcase/README.md) |
| Analyze a numerical trajectory | `nexah analyze data.csv` |
| Compare two numerical datasets | `nexah compare before.csv after.csv` |
| Produce a typed Orientation Report | `nexah orient data.csv --recorded-at <ISO-8601> --domain <name>` |
| Inspect validated capabilities and limits | [Orientation Layer](../ARCHITECTURE/orientation_layer/README.md) |
| Connect a future observed data source | [Observed-Evidence Bridge](../testkit/observed_evidence/OBSERVED_EVIDENCE_BRIDGE.md) |
| Understand safe-use boundaries | [Safety and Misuse Boundaries](SAFETY_AND_MISUSE.md) |

## What works today

The current package can:

- embed and cluster ordered numerical trajectories locally
- construct empirical state-transition maps
- orient from a declared position in a directed graph
- report reachability, shortest paths, components, dead ends, and structural
  bottlenecks
- compare a baseline graph with another observed or explicitly declared graph
- represent ordered IEEE/Pandapower campaigns as typed physical frames
- measure sampled path displacement, drift, direction change, curvature, and
  solver-visible boundaries
- combine five read-only perspectives without voting them into truth
- produce JSON and human-readable Orientation Reports and Briefs
- store and retrieve explicitly admitted episodic context
- preserve provenance, assumptions, missing information, and qualitative
  uncertainty
- replay frozen validation workflows deterministically

Every result is scoped to its input representation and declared context.
Persistent real-world identity, causal effects, calibrated uncertainty,
operational validity, and autonomous action are not inferred automatically.

## Quick start: orient a network

Install the package from the repository root:

```bash
python -m pip install -e .
```

Run the illustrative supply-chain case:

```bash
nexah orient-network APPLICATIONS/datasets/supply_chain.json \
  --focus normal_operation \
  --target system_disruption \
  --domain supply-chain \
  --recorded-at 2026-07-13T22:45:00+00:00 \
  --format brief
```

The result explains the supplied graph's reachable and blocked nodes, declared
paths, structural sensitivities, evidence, limitations, and next questions.
It does not establish a real supply-chain risk or issue an intervention.

## Quick start: replay the IEEE Geometry case

```bash
python validation/ieee_geometry_v1/run_validation.py
```

This rebuilds the frozen IEEE-14 benchmark evaluation, applies the unchanged
IEEE-9 development method, reproduces the canonical geometry and Orientation
Brief, and audits the declared claim boundary. Follow the
[10-minute guide](../APPLICATIONS/power_systems/ieee_geometry_v1/showcase/QUICKSTART_10_MINUTES.md)
for the complete walkthrough.

## Bring your own system

A useful NEXAH application begins with a question, not an adapter:

1. State the orientation question and the position from which it is asked.
2. Declare entities, observations, ordering, units, timestamps, and provenance.
3. Choose an existing representation backend or write a narrow typed adapter.
4. Preserve unknown, missing, failed, and out-of-scope information.
5. Generate an Orientation Report before proposing any action.
6. Validate the method on frozen development and evaluation cases.
7. Admit an episodic-memory update only when an independent observed outcome
   passes the outcome firewall.

```text
source data
→ source adapter
→ representation backend
→ OrientationState
→ read-only probes
→ OrientationReport / OrientationBrief
→ human or separately authorized decision process
```

New domains require their own adapter, semantics, and validation. Passing a
generic software contract demonstrates technical compatibility; it does not
establish scientific or operational validity in that domain.

## Suitable uses

Current and near-term uses include:

- research and reproducible experiment comparison
- network and dependency mapping
- supply-chain and infrastructure training scenarios
- power-system benchmark exploration
- scientific parameter campaigns and simulation studies
- process, service, and knowledge-graph orientation
- education about models, evidence, uncertainty, and boundaries
- human orientation and review before decisions

Use with real infrastructure, people, health, finance, security, or autonomous
systems requires additional domain evidence, governance, access control, and
authorization. Structural sensitivity must not be silently converted into a
target list or action command.

## Authority boundary

The package currently stops at orientation:

```text
observe → represent → compare → orient → explain → review
```

It does not authorize:

- causal claims from structural association alone
- autonomous selection or execution of interventions
- operational control of physical or social systems
- treating simulations or scenarios as observed experience
- exposing sensitive real-world vulnerabilities without access controls

The governing rule for learning is:

> **NO OBSERVED OUTCOME → NO EPISODIC MEMORY UPDATE**

For misuse risks, controlled capabilities, and future release gates, read
**[Safety and Misuse Boundaries](SAFETY_AND_MISUSE.md)** before connecting a
real-world source.

## Go deeper

- [Package reference](README.md)
- [Orientation Layer specification](../ARCHITECTURE/orientation_layer/ORIENTATION_LAYER_SPEC.md)
- [Building plan and accepted plateaus](../ARCHITECTURE/orientation_layer/BUILDING_PLAN.md)
- [Phase V closure](../ARCHITECTURE/orientation_layer/PHASE_V_IEEE_GEOMETRY_TESTKIT.md)
- [Repository map](../REPOSITORY_MAP.md)
