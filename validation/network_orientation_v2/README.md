# Network Orientation V2 Validation

Status: canonical illustrative validation for Phase IV read-only probes

V2 extends the frozen V1 record without rewriting it. It validates five typed
perspectives over the same `NetworkOrientationResult`:

- reachability
- structural bottlenecks
- declared perturbation comparison
- evidence and provenance
- claim-boundary criticism

The synthesis preserves every finding. Agreement is recorded when two probes
take the same stance on the same narrowly named subject. Support/challenge
disagreement is exposed as a contradiction; it is never resolved by voting.

## Distinct topology fixture

`branched_cycle_graph.json` contains two branches, a merge, one directed cycle,
a target leaf, and an isolated node. It is deliberately different from the
five-node chain topology used by the V1 Supply Chain and Ecosystem fixtures.
This broadens synthetic structural coverage. It still does not establish
real-world generalization.

The declared scenario removes `loop_2 → target`. The application must report
the target as newly unreachable while the remaining cycle stays represented.

## Reproduce

```bash
python validation/network_orientation_v2/run_validation.py
python validation/network_orientation_v2/run_validation.py --out /tmp/network-v2.json
diff validation/network_orientation_v2/canonical_summary.json /tmp/network-v2.json
```

## Boundary

No observed outcome is created, so the append-only episodic store is not
updated. These probes support learning by comparison and criticism. They are
not agents, controllers, domain experts, or execution authorities.
