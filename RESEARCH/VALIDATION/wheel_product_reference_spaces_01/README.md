# Wheel and Product Reference Spaces 01

Status: bounded research validation; not an OLS release and not evidence of
dynamical stabilization.

This bundle follows the completed prime-modular residue comparison without
changing it. It tests five related but independent questions:

1. whether modulo 6 provides the minimal dual prime-residue structure;
2. whether modulo 42 is exactly equivalent to the product coordinates
   modulo 6 and modulo 7, and whether their transition dynamics factorize;
3. how the wheel/lift family `30 → 120 → 360` behaves;
4. whether modulo 280 and modulo 360 differ despite both having 96 unit
   residues; and
5. whether the local neighborhood `31, 32, 33` is exceptional in a
   predeclared modulus scan.

The first 20,000 primes, including 2 and 3, are generated offline. As in the
previous experiment, a sensitivity policy removes 2 and 3 only from training
prefixes while retaining identical chronological test ranges.

## Offline replay

From this directory:

```sh
python3 run_experiment.py
python3 -m unittest -v test_experiment.py
python3 run_experiment.py --check
```

`--check` writes candidates to a temporary directory, byte-compares them with
the committed evidence and verifies `SHA256SUMS`. It never overwrites committed
evidence.

## Artifacts

- `SPEC.md`: frozen questions, metrics and decision rules.
- `run_experiment.py`: deterministic Python-standard-library implementation.
- `test_experiment.py`: arithmetic, coordinate and model invariants.
- `results/prediction_folds.csv`: chronological held-out measurements.
- `results/modulus_summary.csv`: aggregate scan across moduli.
- `results/product_folds.csv`: Mod-42 joint versus Mod-6×Mod-7 factorization.
- `results/complement_folds.csv`: reflection-symmetry measurements.
- `results/arithmetic_invariants.json`: exact wheel, CRT and grid facts.
- `results/summary.json`: machine-readable decisions.
- `RESULTS.md`: human-readable report.
- `SHA256SUMS`: evidence manifest.

No OLS primitive, operator, architecture boundary or Processor contract is
introduced or modified.
