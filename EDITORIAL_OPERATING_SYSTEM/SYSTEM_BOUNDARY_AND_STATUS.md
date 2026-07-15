# NEXAH Editorial Operating System — System Boundary and Status

**Status date:** 2026-07-16  
**Visual snapshot:** pre-Batch 1  
**Authority:** repository state and explicit human editorial decisions

This document separates the reusable Editorial Operating System concept from
capabilities that are actually implemented and verified in the repository.
It is intentionally factual and may be updated more frequently than the main
[README](README.md).

## Two development tracks

NEXAH currently uses two phase histories for different scopes:

| Track | Current marker | Meaning |
|---|---|---|
| Orientation Kernel and technical architecture | Kernel v0.7; technical Phase V complete | Typed orientation, network orientation, evidence-bound reporting, validation paths, and related kernel work |
| NEXAH Library editorial track | Phase IX | Governed editorial execution for the Living Library |

The numbering is not interchangeable. “Phase IX” does not mean that every
technical or domain application is implemented.

## Implemented and evidenced

| Capability | Status | Primary repository location |
|---|---|---|
| Orientation Kernel v0.7 | Implemented | [`nexah/`](../nexah/) |
| Canonical Library Registry | Implemented as a 10-Work pilot | [`LIBRARY/registry/`](../LIBRARY/registry/) |
| Proposal Overlay | Implemented and explicitly non-canonical | [`LIBRARY/review/`](../LIBRARY/review/) |
| Controlled Core Operators | 17 implemented in the pilot Registry | [`LIBRARY/registry/`](../LIBRARY/registry/) |
| Reader Policies UQ-01–UQ-06 | Human-approved | [`LIBRARY/review/reader_journey_review.yaml`](../LIBRARY/review/reader_journey_review.yaml) |
| Reader Journeys | Six canonical journeys represented in the editorial review | [`LIBRARY/review/reader_journey_review.yaml`](../LIBRARY/review/reader_journey_review.yaml) |
| Explain Mode | Implemented for Library orientation queries | [`nexah/library/`](../nexah/library/) |
| Health, Series, Traversability, Snapshot, Diff, and Release reporting | Implemented | [`nexah/library/`](../nexah/library/) |
| Read-only Are.na connector | Implemented; GET-only | [`nexah/library/arena.py`](../nexah/library/arena.py) |
| Editorial Writer | Implemented as a separate guarded module | [`nexah/library/editorial_writer.py`](../nexah/library/editorial_writer.py) |
| Batch 0 sandbox | Verified | [`LIBRARY/review/BATCH_00_SANDBOX_VERIFICATION.md`](../LIBRARY/review/BATCH_00_SANDBOX_VERIFICATION.md) |
| Batch 1 action selection | Four actions explicitly accepted | [`LIBRARY/review/arena_manual_cleanup_queue.yaml`](../LIBRARY/review/arena_manual_cleanup_queue.yaml) |
| Batch 1 public application | Not yet evidenced in the repository at this snapshot | Verification report absent |

## Current Library figures

The dated architecture visual records the following pre-Batch 1 editorial
state:

- 10 Canonical Registry entities;
- 61 visible Proposal candidates;
- 17 controlled Core Operators;
- Reader Policies UQ-01 through UQ-06;
- six canonical Reader Journeys;
- 16 Manual Cleanup Queue actions;
- Traversability baseline of 1/15 directly walkable connections;
- Batch 0 verified;
- Batch 1 accepted but not yet publicly applied.

These figures describe a dated source and review state. They are not permanent
architectural constants. Source snapshots and generated review artifacts remain
the operational evidence for later comparisons.

## Editorial Writer boundary

The Writer is not a synchronizer and does not decide what should change. Its
production allowlist is limited to:

- create a text block;
- create a Channel connection;
- move a connection;
- update a description.

Before applying an accepted action, the Writer requires:

- an available `ARENA_WRITE_TOKEN` environment variable;
- an explicit `--apply` invocation;
- the reviewed plan ID;
- a verified Source Snapshot;
- matching live Channel identity and sequence fingerprint;
- successful verification after every mutation.

It does not allocate Registry IDs, promote Proposals, change Operators, rename
or delete production Channels, change visibility or ownership, or modify the
cleanup queue.

See the full
[Phase IX Editorial Writer contract](../LIBRARY/review/PHASE_IX_EDITORIAL_WRITER.md).

## Human authority boundary

The following remain human decisions:

- canonical identity;
- Proposal promotion;
- Reader Policy approval;
- editorial sequence and Series membership;
- Operator assignment;
- public editorial changes;
- acceptance and completion state of cleanup actions;
- interpretation of observed reader behavior.

The Kernel may derive paths and explanations from approved structures. It may
not silently turn an inference into canonical knowledge.

## Not implemented or not claimed

The current system does not claim:

- individual learner profiles;
- automatic path optimization from reader behavior;
- autonomous editorial decisions;
- automatic Registry growth or Proposal promotion;
- a general-purpose synchronization layer;
- completed Wikipedia, museum, education, research, enterprise, or personal-AI
  integrations;
- scientific or operational validity merely because a structural contract or
  software test passes;
- replacement of human editors, librarians, teachers, researchers, or readers.

The application patterns shown in the visuals remain a design horizon until an
adapter, dataset, working demonstration, and domain-appropriate validation
exist.

## Updating this status

When a public editorial batch is applied:

1. preserve the prior visual and Source Snapshot;
2. add the new verification report;
3. capture a new immutable Source Snapshot;
4. rerun Traversability, Editorial Diff, Health, and Release Check;
5. update this document from those artifacts;
6. create a newly dated visual snapshot rather than overwriting the old one.

Architecture images may explain stable relationships. Any image containing
counts, phase states, test results, queue states, or traversability values must
be treated as a dated snapshot.
