# G4 Entry and Clean-Replay Contract

Status: **fixed before G4 execution**  
Date: 2026-07-26

## Authorised purpose

G4 asks only whether a clean, documented environment can execute the frozen
IEEE Geometry V1 replay and the current SR-1 sidecar checks through one command
and produce a complete disposable result bundle.

It is an internal clean-environment replay. It is not external replication,
external or scientific validation, Comparator evaluation, performance
comparison, prediction, early warning, decision support, control, or
operational readiness.

## Entry criteria

All must pass before replay:

1. approved protocol ID `sr1-ieee-geometry-comparator-analysis-v1`, version
   `1.0.0`, exact approved SHA-256
   `bd9d0fa2094b17333b18ec7621f33fd32271c2e759f2b01c9b27f76702ffe5ba`;
2. G3 classification `G3_equivalence_passed`, zero IEEE-9 and IEEE-14
   discrepancies;
3. all 15 frozen V1 hashes match `fixtures/expected_hashes.json`;
4. source revision is exactly
   `d3a19138b96aa07dfd623bdebb1003cb02cc60e8`;
5. clean environment matches Python `3.12.7`, NumPy `1.26.4`, pandas `2.3.3`,
   Pandapower `3.4.0`, SciPy `1.13.1`, pytest `7.4.4`, and NEXAH `0.7.0`.

Failure of any entry criterion classifies G4 as `G4_blocked` or
`G4_clean_replay_failed`; no scientific source is repaired.

## Commands

The documented one-command route is:

```bash
python validation/ieee_geometry_external_replay_v1/run_external_replay.py \
  --source-root /absolute/path/to/clean/NEXAH \
  --source-revision d3a19138b96aa07dfd623bdebb1003cb02cc60e8 \
  --out /absolute/disposable/output
```

The orchestrator invokes three explicit commands in order:

1. IEEE-9 development replay through `replay_development.py`;
2. IEEE-14 evaluation replay through `replay_evaluation.py`, only after the
   development command passes and only after the approved protocol hash is
   verified;
3. the unchanged frozen V1 pytest gate:
   `python -m pytest tests/validation/test_ieee_geometry_v1.py -q`.

The evaluation command also invokes the unchanged canonical runner:

```bash
python validation/ieee_geometry_v1/run_validation.py \
  --out <disposable-output>/canonical_replay.json
```

## Expected artifacts

- `environment.json`
- `package-lock.txt`
- `commands.json`
- `logs/development.stdout.txt`
- `logs/development.stderr.txt`
- `logs/evaluation.stdout.txt`
- `logs/evaluation.stderr.txt`
- `logs/pytest.stdout.txt`
- `logs/pytest.stderr.txt`
- `development/development_replay.json`
- `evaluation/evaluation_replay.json`
- `evaluation/canonical_replay.json`
- `artifact_hashes.json`
- `g4_result.json`

All paths must be below the caller-selected disposable output directory and
outside both clean source and canonical repository paths.

## Acceptance

- no manual source/data editing;
- every command, exit code, runtime, warning, and failure recorded;
- development passes before evaluation is loaded;
- evaluation refuses before source loading when the approved protocol digest is
  absent or wrong;
- canonical required checks pass;
- the two frozen V1 tests pass;
- IEEE-9 failures at 2.3 and 2.4 remain explicit, null, and unbridged;
- all 19 IEEE-14 frames, 18 adjacent steps, and 17 centred turns remain
  represented;
- all frozen hashes match before and after;
- clean source worktree remains clean;
- output can be deleted without changing source;
- no Comparator output, G5, G6, canonical edit, or commit.

## Stop conditions

Stop and preserve evidence if:

- protocol/G3/hash/source/environment entry verification fails;
- development replay fails;
- evaluation can run with a mismatched protocol;
- any command returns non-zero;
- canonical checks, tests, or frozen hashes fail;
- a repair would require changing frozen V1;
- output isolation fails;
- the task expands into Comparator analysis, G5/G6, external contact, paper,
  grant, new theory, case, outcome, or metric.

