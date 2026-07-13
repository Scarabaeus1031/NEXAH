# Network Orientation V1 Validation

Status: canonical illustrative validation for Phase IV

This validation checks whether one domain-blind graph path can:

1. orient a declared supply-chain transition graph,
2. describe the structural effect of removing one declared edge, and
3. process an ecosystem food-web fixture without domain-specific code.

The two JSON inputs are illustrative repository fixtures. The held-out result
demonstrates software-contract portability, not real-world generalization. Both
fixtures also share the same bidirectional five-node chain pattern, so this gate
does not test transfer to a topologically distinct graph family.

## Reproduce

From the repository root:

```bash
python validation/network_orientation_v1/run_validation.py
```

To compare the canonical artifact:

```bash
python validation/network_orientation_v1/run_validation.py \
  --out /tmp/network-orientation-v1.json
diff validation/network_orientation_v1/canonical_summary.json \
  /tmp/network-orientation-v1.json
```

## Frozen result

- Supply-chain focus reaches all four other declared nodes.
- Removing `production_slowdown → distribution_backlog` makes
  `distribution_backlog` and `system_disruption` unreachable from the focus.
- The unchanged application and backend recover the analogous five-node path
  in the held-out ecosystem fixture.
- No regime, stability, risk, causal, or control semantics are imported from
  either fixture.

The perturbation is a declared training scenario: it teaches the application
how topology changes its map. It is not evidence that a real system would react
in the same way.
