# Supply-Chain Orientation Brief — Illustrative Showcase

This directory shows the same orientation product in two forms:

- `orientation-brief.md` — readable invitation for a researcher or practitioner
- `orientation-brief.json` — equivalent typed contract for software integration

The source is the repository's authored `supply_chain.json` fixture. One edge
is explicitly removed to construct a transparent training scenario. The output
describes changes in the declared graph; it is not operational supply-chain
evidence and records no observed outcome.

## Regenerate

From the repository root:

```bash
nexah orient-network APPLICATIONS/datasets/supply_chain.json \
  --focus normal_operation \
  --target system_disruption \
  --domain supply-chain \
  --recorded-at 2026-07-13T22:45:00+00:00 \
  --remove-edge production_slowdown distribution_backlog \
  --format brief \
  --out APPLICATIONS/network_orientation/showcase/supply_chain_scenario/orientation-brief.md

nexah orient-network APPLICATIONS/datasets/supply_chain.json \
  --focus normal_operation \
  --target system_disruption \
  --domain supply-chain \
  --recorded-at 2026-07-13T22:45:00+00:00 \
  --remove-edge production_slowdown distribution_backlog \
  --format brief-json \
  --out APPLICATIONS/network_orientation/showcase/supply_chain_scenario/orientation-brief.json
```

> **NO OBSERVED OUTCOME → NO EPISODIC MEMORY UPDATE**
