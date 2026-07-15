# NEXAH Library — Phase IX Editorial Writer

## Purpose

The Editorial Writer executes previously approved human editorial decisions on
Are.na. It is not a synchronizer, importer, recommendation engine, or source of
editorial decisions.

Architecture v1.0 remains frozen. `nexah/library/arena.py` remains GET-only.
All write capability is isolated in `nexah/library/editorial_writer.py`.

## Control flow

```text
Accepted Queue Action
        ↓
Verified Source Snapshot
        ↓
Dry Run + stable Plan ID
        ↓
Human approval of that Plan ID
        ↓
--apply + ARENA_WRITE_TOKEN
        ↓
Fingerprint guard before every mutation
        ↓
Live verification after every mutation
        ↓
Immutable Source Snapshot
        ↓
Traversability · Editorial Diff · Health · Release Check
```

## Production operation allowlist

- Create Text Block
- Create Channel Connection
- Move Connection
- Update Description

The production client exposes no Delete, Rename, Visibility, Ownership,
Registry, ID, Operator, Proposal, Canonical, or Queue operations.

The private Batch 0 harness has two additional cleanup calls: delete its test
block and remove its test connection. They are isolated in `ArenaSandboxClient`
and are never used by the production apply path.

## Preconditions

An apply aborts when any of the following is true:

- `ARENA_WRITE_TOKEN` is missing;
- `--apply` is absent;
- the approved Plan ID is absent or no longer matches;
- an Action ID is unknown;
- an Action is not `accepted`;
- a Channel is missing from the latest verified Source Snapshot;
- a Channel is unavailable;
- its live `sequence_fingerprint` differs from the Snapshot;
- its fingerprint changes between two Writer mutations;
- a description differs from the exact reviewed source text;
- final live verification does not reproduce the planned top sequence.

The Action Queue is never updated by a command. Review state changes remain
explicit repository edits.

## Secret handling

The Writer reads the token only from `ARENA_WRITE_TOKEN`. It does not search the
Desktop, read text files, accept a token argument, serialize a token, or log a
token.

```bash
export ARENA_WRITE_TOKEN="..."
```

## Batch 0

Preview:

```bash
python -m nexah.library editorial-sandbox
```

Execute only after the token is present:

```bash
python -m nexah.library editorial-sandbox --apply
```

The command creates or reuses the private `NEXAH API SANDBOX`, then tests:

1. create text block;
2. verify;
3. delete test block;
4. create Channel connection;
5. move connection to the visual top;
6. verify;
7. remove test connection.

The sandbox must be empty of test material when the test completes. The command
then captures a public Source Snapshot and runs Editorial Diff, Health, and
Release Check.

## Batch 1

The only Batch 1 Action IDs are:

- `ACQ-001`
- `ACQ-002`
- `ACQ-006`
- `ACQ-013`

First generate a Dry Run:

```bash
python -m nexah.library editorial-write --batch BATCH-01 --format yaml
```

At the time of implementation all four Actions remain `pending`; therefore the
Writer correctly reports them as ignored and performs no live reads or writes.
A human editor must change the intended records to `accepted`, commit that
decision separately, rerun the Dry Run, and review its exact Plan ID.

Only that reviewed plan can be applied:

```bash
python -m nexah.library editorial-write --batch BATCH-01 \
  --apply --plan-id <approved-plan-id>
```

After a successful apply the command automatically captures a new immutable
Snapshot and runs live Traversability, Editorial Diff against the pre-write
baseline, Health, and Release Check. It writes
`LIBRARY/review/BATCH_01_VERIFICATION.md` with actions, fingerprints,
Traversability before/after, warnings, errors, and deviations.

Successful execution does not mark Queue Actions `completed`. That remains a
separate human review decision.
