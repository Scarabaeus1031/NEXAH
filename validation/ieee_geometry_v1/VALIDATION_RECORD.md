# Validation Record — Phase V IEEE Geometry V1

## Question

Can the geometry method frozen on IEEE-9 be applied unchanged to the locked
IEEE-14 benchmark campaign while preserving failures, provenance, uncertainty,
claim limits, and reproducibility?

## Method

The runner reconstructs IEEE-14 directly from the manifest-declared Pandapower
source and fixed 19-point load-scale campaign. It applies the standardization
stored by the IEEE-9 development result and the same six operator
implementations. It then rebuilds the five-probe synthesis and Orientation
Brief and compares every product with the committed canonical artifacts.

## Result

The gate passes. IEEE-14 produces 19 converged frames, 18 available adjacent
steps, and 17 available centered turns. No solver failure appears on the frozen
grid, so no solver-boundary record is available. The IEEE-9 development case
continues to preserve its two explicit failed frames at load scales 2.3 and 2.4.

## Evidence status

This is deterministic benchmark-model and computation evidence. Uncertainty is
not calibrated. No operational observation or independent outcome is present.
The result therefore cannot update episodic memory.

## Reproduction

```bash
python validation/ieee_geometry_v1/run_validation.py \
  --out validation/ieee_geometry_v1/canonical_summary.json
```
