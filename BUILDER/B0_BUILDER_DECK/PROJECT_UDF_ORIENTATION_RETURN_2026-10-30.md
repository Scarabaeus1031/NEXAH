# UDF Orientation Return — bounded Builder project candidate

**State:** `BACKLOG_CANDIDATE / NOT_ACTIVE / OWNER_ACCEPTED_CLASSIFICATION`

**Date:** `2026-10-30`

## Goal

Prove one useful UDF profile by transporting a complete, source-bound
orientation Return through the existing Bench path:

```text
Breathing Crystal Orientation Ledger
  → experimental .udf.json profile
  → V12 / X–Y Translator
  → exact Return to the Crystal Ledger
```

This is a project candidate, not a frozen universal format, product
capability, active workstream or public release.

## Owning sources

- Science implementation and evidence:
  `A0_BOOK/a0-udf-orientation-return-profile.cjs`
- Five-proof harness:
  `A0_BOOK/a0-udf-orientation-return-proof-tests.cjs`
- Machine receipt:
  `A0_BOOK/results/a0-udf-orientation-return-proof-2026-10-30.json`
- Existing Builder tool reused: `BT-045`

## Proven cut

Profile: `nexah.udf.orientation-return/0.1.0-experimental`

The profile carries source identity and hash, source and target contracts,
pair, PIN, H/X and V/Y nodes, angle, radius, quadrant, crossings, direction,
winding, the two distinct V12 comparator roles and an explicit Return target.
It permits no new canonical ID or Source Graph relation.

## Evidence gate

`5/5 PASS`:

1. deterministic serialization and digest;
2. lossless Crystal → UDF → V12 → Ledger replay within `1e-12` numeric tolerance;
3. one profile for `AB`, `BC` and `CA`;
4. rejection of malformed hash, pair, node, winding, comparator and JSON input;
5. semantic separation of Crystal vector, `RE · EXIT` and `DO′ · RETURN`.

Existing regressions also remain green: `166` Breathing Crystal checks and
`306` Spin-to-Bloom checks.

## Strong-baseline preflight

The equal-information PROV / RO-Crate comparator returns `TIE 6/6`. Both the
UDF candidate and the baseline preserve deterministic source provenance,
AB/BC/CA orientation roles, numeric frame values, distinct comparator roles,
explicit Return and the matched missing-axis loss point. The UDF record is
more compact and domain-direct; no incremental information or reconstruction
advantage is established for this single profile.

This retained null result prevents a novelty claim based only on serialization,
provenance or typed Return. The next meaningful evidence gate is a second
genuinely different source instrument or an independent reconstruction test.
Neither is activated by this project brief.

- Science preflight:
  `A0_UDF_ORIENTATION_RETURN_PROV_ROCRATE_BASELINE_BENCHMARK_2026-10-30.md`
- Machine receipt:
  `A0_BOOK/results/a0-udf-orientation-return-baseline-benchmark-2026-10-30.json`

## Seven-part lens campaign

The follow-up campaign produces a mixed result rather than a promotion:

- raw UDF size is `45.26%` of the matched baseline; gzip/Brotli size is about
  `69–71%` of baseline;
- seven implemented lenses pass isolated ablation and cross-lens consistency;
- matched corruption rejection remains `22/22 TIE`;
- Panel V is correctly rejected because the current profile is
  Crystal-specific and not cross-instrument portable;
- incomplete values fail closed, but explicit
  `UNKNOWN / UNOBSERVED / UNRESOLVED / NOT_APPLICABLE` semantics are absent;
- the Human reconstruction protocol is ready but has no participant result.

Human Test 7 is returned as
`PARKED_AWAITING_SEPARATE_HUMAN_PARTICIPANT_GATE`. Builder may retain the
fixtures, protocol and a future local runner specification, but may not recruit
participants, expose fixtures or collect responses without a separate Owner
authorization and Science participant-governance return.

The smallest responsible design continuation is therefore not a universal UDF
freeze. It is an unfrozen profile-family sketch with a minimal common
Source/Return/Claim core and separate instrument-specific profiles. This
continuation remains unactivated.

The later scientific order is fixed as a proposal, not a build activation:
Human reconstruction first; explicit incomplete-state semantics second; one
preregistered Crystal/Panel-V profile-family comparison third.

- Science return:
  `A0_UDF_ORIENTATION_RETURN_LENS_CAMPAIGN_2026-10-30.md`
- Campaign receipt:
  `A0_BOOK/results/a0-udf-orientation-return-lens-campaign-2026-10-30.json`
- Human protocol:
  `A0_BOOK/results/a0-udf-orientation-return-human-reconstruction-protocol-2026-10-30.json`

## Backlog cut

If Mission Control later activates this project, the smallest next build is a
Bench load/save/validate panel for this one profile plus a replay receipt. The
profile must remain versioned and experimental until a second genuinely
different instrument proves what is reusable.

## STOP

- do not call the profile universal;
- do not freeze `.udf.json` from one use case;
- do not embed arbitrary executable code;
- do not mutate GLB nodes or source assets;
- do not assign product capability, Study, Finding or publication state;
- do not activate while `M-PUB01` remains the one active Mission Control cut
  without a separate Human Owner reprioritization.

## Return

Builder classification returns to Mission Control
`CURRENT/STRATEGIC_OPPORTUNITY_REGISTER.md#op-udf-01` and to the A0 Science
Findings Workspace. Activation remains a separate Owner decision.
