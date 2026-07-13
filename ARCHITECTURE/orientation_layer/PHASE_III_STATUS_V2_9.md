# Phase III Status — v2.9 Working Baseline

Status date: 2026-07-13  
Scope: Adapter ecosystem and IEEE/Pandapower domain validation  
Classification: versioned working baseline, not a software release

## What v2.9 records

Phase III has completed work packages A–G:

- the generic `SourceAdapter` and `SourceBatch` boundary;
- array and schema-driven table reference adapters;
- the coupled IEEE/Pandapower source with separate entity and ordered-campaign
  views;
- scoped translation into the frozen v0.7 representation backend;
- non-causal spatial attribution to buses and lines;
- frozen IEEE-9 / held-out IEEE-14 validation; and
- reconstruction of the historical scaling pattern across eight systems through
  PEGASE-9241.

The current evidence supports a reproducible adapter-to-orientation path and
boundary acceleration in six usable upper-bound scans. It does not establish a
universal, edge-independent precursor. IEEE-300 and PEGASE-9241 encounter the
lower bound of the global scan and therefore require a baseline-anchored
continuation design before they can test that question.

## Frozen evidence at this point

- Memory V1 and V2 remain unchanged.
- IEEE Orientation V1 remains unchanged: threshold alignment 2/3 and entity
  attribution overlap 11/12, including the documented IEEE-14 miss.
- Scaling Pattern V1 remains unchanged: eight systems audited, six usable
  upper-bound scans, and two explicit lower-bound failures.
- Canonical runs remain deterministic; new claims require a new validation
  version rather than retrospective changes to these records.

Exact counts and result values are governed by the canonical files under
`validation/`, not by the explanatory diagrams.

## Remaining Phase III work

### H — Baseline-anchored continuation

Define each system's native operating point as `lambda = 1.0`, scan upward and
downward separately, and preserve solver failure as evidence.

### I — Adaptive boundary refinement

Resolve the interval between the last converged and first failed point instead
of treating a truncated global grid as the physical boundary.

### J — Edge-independent pattern test

Predeclare a local derivative estimator, peak prominence and boundary-distance
criteria, multi-resolution checks, and a monotone null. Distinguish a stable
interior candidate precursor from boundary acceleration.

### K — PEGASE-9241 held-out gate

Apply the frozen H–J method without parameter retuning. The acceptable outcomes
are either cross-scale support or an explicit boundary of validity.

### L — Broader adapter families

Only after the power-system gate, extend the same orientation contract to other
trajectory, event-stream, tabular-sequence, or domain-specific sources.

## Visual record

### Page 3 — Implemented Phase III path and present boundary

![NEXAH Phase III v2.9 status](visuals/phase-iii-v2.9-status-page-3.png)

### Page 4 — Continuation and completion plan

![NEXAH Phase III v2.9 continuation](visuals/phase-iii-v2.9-continuation-page-4.png)

### Page 5 — Plain-language capability state

![NEXAH v2.9 orientation skeleton status](visuals/nexah-v2.9-skeleton-status-page-5.png)

The visuals explain this baseline. Normative specifications, tests, and
canonical validation records remain authoritative.
