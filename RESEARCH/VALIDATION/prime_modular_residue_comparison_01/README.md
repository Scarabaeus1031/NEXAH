# Prime Modular Residue Comparison 01

Status: bounded research validation; not an OLS release and not a Proof of
Architecture.

This experiment tests two narrow claims already present in the repository's
prime-modular exploration:

1. whether residue transitions modulo 17 carry more held-out predictive
   information than modulo 7 and several control moduli; and
2. whether the proposed coordinate rule
   `r17 = (7 * r7 + 8) mod 17` reconstructs held-out modulo-17 residues better
   than a training-only majority baseline.

It does **not** test or claim that modulo 17 stabilizes a dynamical system.
Prediction, coordinate reconstruction and stabilization are different claims.

The primes 2 and 3 are included in the canonical input. A predeclared
sensitivity run removes only those two finite exceptional terms from the
training prefix while preserving the same held-out test ranges. This prevents
their treatment from becoming post-hoc data cleaning.

## Offline replay

From this directory:

```sh
python3 run_experiment.py
python3 -m unittest -v test_experiment.py
python3 run_experiment.py --check
```

The implementation uses only the Python standard library, performs no network
access and uses deterministic seeds. `--check` generates candidates in a
temporary directory, byte-compares them with the committed evidence and
verifies `SHA256SUMS`; it does not overwrite committed evidence.

## Artifacts

- `SPEC.md` freezes the question, methods and decision rules.
- `run_experiment.py` generates the deterministic evidence.
- `test_experiment.py` checks the mathematical and implementation invariants.
- `results/prediction_folds.csv` records every held-out residue-prediction fold.
- `results/bridge_folds.csv` records every held-out 7-to-17 bridge fold.
- `results/summary.json` records aggregate results and decision outcomes.
- `RESULTS.md` is the human-readable evidence report.
- `SHA256SUMS` binds the experiment and its generated evidence.

No OLS vocabulary, operator, Processor contract or architecture is changed by
this experiment.
