# G4 clean-environment replay protocol

Status: review candidate, not yet committed  
Gate: G4 only  
Baseline revision: `d3a19138b96aa07dfd623bdebb1003cb02cc60e8`

This protocol implements the fixed G4 contract in
`G4_ENTRY_AND_REPLAY_CONTRACT.md`. It does not authorise comparator analysis,
G5, G6, canonical edits, or claim changes.

## Clean setup

1. Create a fresh checkout at the baseline revision.
2. Create a copied Python 3.12.7 virtual environment.
3. Install `environment/requirements-direct.txt`.
4. Install the checkout package as NEXAH 0.7.0 without changing the checkout.
5. Confirm `pip check` and record `pip freeze --all`.
6. Disable package-index access for the replay.

The executed clean environment also reconstructed the G1 runtime dependencies
that were present but not listed in the six-package G1 identity:

- matplotlib 3.9.2
- scikit-learn 1.5.1
- PyYAML 6.0.1
- setuptools 82.0.0

Their complete dependency closure is recorded in
`reports/g4_clean_replay/raw/environment_identity.json`.

## One-command replay

```bash
PIP_NO_INDEX=1 /path/to/venv/bin/python \
  validation/ieee_geometry_external_replay_v1/run_external_replay.py \
  --source-root /path/to/clean/checkout \
  --source-revision d3a19138b96aa07dfd623bdebb1003cb02cc60e8 \
  --out /disposable/path/g4-review
```

The runner performs these separately recorded commands:

1. IEEE-9 development replay only.
2. A negative protocol-hash control that must refuse before IEEE-14 is loaded.
3. Explicit IEEE-14 evaluation replay only after the preceding controls pass.
4. Frozen V1 tests.
5. Frozen-hash and checkout-cleanliness verification.

The development program does not invoke or display the evaluation case.
The evaluation program refuses unless the approved G2 protocol bytes hash to
`bd9d0fa2094b17333b18ec7621f33fd32271c2e759f2b01c9b27f76702ffe5ba`.

## Stop conditions

Stop and classify G4 as blocked or failed if any entry check, hash binding,
case-separation control, command, canonical replay check, frozen hash, or
checkout-cleanliness check fails. Do not repair the scientific protocol during
G4. Do not proceed to G5 or G6.

