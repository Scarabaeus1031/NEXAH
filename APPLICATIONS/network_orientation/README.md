# NEXAH Network Orientation V1

Status: implemented and canonically tested with illustrative graph fixtures

Network Orientation V1 is the first graph-native application of the typed
Orientation Layer. It describes a declared directed network from an explicit
focus without passing entity rows into the temporal v0.7 backend.

## What it does

```text
declared nodes and edges
→ GraphSourceAdapter
→ GraphRepresentationBackend
→ structural topology and paths
→ evidence-bound Network Orientation Report
→ optional snapshot or training-scenario comparison
```

The application reports:

- directed reachability and blocked nodes
- shortest declared paths
- in-degree and out-degree
- dead ends
- strong and weak components
- weak articulation points
- edges whose removal reduces reachability from the chosen focus
- structural differences between a baseline and another graph
- provenance, assumptions, missing information, and qualitative uncertainty

These are topology statements. They do not establish stability, risk, desired
outcomes, causal effects, or a control policy.

## Run the supply-chain fixture

From the repository root:

```bash
nexah orient-network APPLICATIONS/datasets/supply_chain.json \
  --focus normal_operation \
  --target system_disruption \
  --domain supply-chain \
  --recorded-at 2026-07-13T22:45:00+00:00
```

The default output is the complete JSON contract. Add `--format text` for a
compact human-readable report or `--out report.json` to write the JSON result.

## Run a declared training scenario

```bash
nexah orient-network APPLICATIONS/datasets/supply_chain.json \
  --focus normal_operation \
  --target system_disruption \
  --domain supply-chain \
  --recorded-at 2026-07-13T22:45:00+00:00 \
  --remove-edge production_slowdown distribution_backlog \
  --format text
```

This does not issue a command to a system. It constructs a transparent second
graph and learns how the declared map changes: which nodes become unreachable
and which shortest paths change. An independent current graph can instead be
compared with `--baseline baseline.json`.

## Held-out fixture

The same application processes
`APPLICATIONS/datasets/ecosystem_food_web.json` without ecosystem-specific
logic. This verifies contract portability across two illustrative graph
fixtures. Both fixtures share the same bidirectional five-node chain pattern;
the gate therefore does not establish transfer to a new topology, ecological
validity, or supply-chain validity.

Canonical evidence and reproduction instructions live in
**[validation/network_orientation_v1](../../validation/network_orientation_v1/)**.

## V2 — Multi-perspective learning

Add `--probes` to wrap the V1 orientation in five read-only perspectives:

```bash
nexah orient-network APPLICATIONS/datasets/supply_chain.json \
  --focus normal_operation \
  --target system_disruption \
  --recorded-at 2026-07-13T22:45:00+00:00 \
  --probes
```

The probes examine reachability, bottlenecks, declared perturbations, evidence,
and claim boundaries. They preserve agreement and contradiction without voting
and have no execution authority. See the additive
**[V2 validation](../../validation/network_orientation_v2/)** for the distinct
branched/cyclic fixture.

## Learning direction

The Phase IV objective is orientation through experience:

```text
observe → map → compare → remember → refine orientation
```

Multi-perspective probes now contribute reachability, bottleneck, perturbation,
evidence, and critique views to the same result. Episodic storage still waits
for a genuinely observed outcome. Autonomous execution is not the objective of
this application.
