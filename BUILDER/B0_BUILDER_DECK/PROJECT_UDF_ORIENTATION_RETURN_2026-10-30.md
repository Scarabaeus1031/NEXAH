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

## Owner-selected integration review scope — 2 November 2026

State: `REVIEW_SCOPE_BOUND / NOT_AN_ACTIVE_BUILD / EXISTING_PROJECT_REUSED`

The following five questions are retained inside this existing Builder and
Mission Control project. They do not create another project, tool row, format,
operator, Study, Finding or Source Graph identity.

1. **ULLINIRIUM View Anchor extension.** Reuse the existing source-bound
   local coordination view in
   `A0_BOOK/A0_BLUE_PINK_DODECA_CELL_RETURN.html#module-entry`: the `12+1`
   ring, `135° VIEW ANCHOR`, four shadow residuals and Pink/Blue covariant
   body views around the common Return pivot. Freeze only what the additional
   working terms `13 ↔ 3,1 / 1,3` and `AL U Li Ri Um Ti tan` denote.
   ULLINIRIUM is not new and is not promoted from a view into an operator or
   axis; its extension still requires declared carrier, state, transition,
   inverse and Return.
2. **Address arithmetic.** Keep the exact generator
   `L×L+1=50²+1=2501` and its double `5002` separate from the still-open
   `12+12` reading. A visual or verbal correspondence does not establish a
   mathematical map.
3. **Hourglass / X Cube lens.** Test whether `}{` and `X` can be expressed as
   a typed hinge, crossing or antipodal view over the existing Cube/Q4 state.
   Reuse the current Dürer/Khajuraho and Blue/Pink controls; do not infer new
   geometry from the glyph.
4. **LUX → nXeT → XVA route.** Treat `LUX`, the folded `nXeT`/lowered-T
   reading and `XVA` as a candidate user-facing sequence. `LUX` may display
   the bound 2501/5002 address relation, while `nXeT` and `XVA` remain lens
   labels until their state transition and inverse are executable.
5. **Historical visual reading lens.** Reuse the retained eleven-stage gallery
   path, lowered-T routing view, Alpha/Beta/Gamma bridge and GLB/Cube view as a
   provenance-bound reading sequence. The sequence must preserve variant and
   source status; it is not evidence that every visual shares one operator.

Review order:

```text
DEFINE TYPES
  → REPLAY EXISTING EXACT TESTS
  → ADD NEGATIVE CONTROLS
  → TEST RETURN / INVERSE
  → CLASSIFY EXACT / VIEW / HYPOTHESIS
  → BUILDER + SCIENCE RETURN
```

No Human participant work is introduced by this integration review. The
parked Human Test 7 gate and the project's `NOT_ACTIVE` state remain unchanged.

## Historical NXA / SCARAB / XVA binding

The older NXA/SCARAB/UDF/XVA material is bound here as a provenance comparator
for the existing `OP-UDF-01` / `BT-045` project, not as a second project and
not as proof that the current experimental UDF profile implements those
historical roles.

The controlling source audits are:

- `30 SCIENCE LAB/NEXAH-Science-Lab/NUMBER_OPERATOR_ARCHITECTURE_CONCORDANCE_AUDIT/CATHEDRAL_FORMAT_SOURCE_RETURN_2026-10-18.json`;
- `30 SCIENCE LAB/NEXAH-Science-Lab/NUMBER_OPERATOR_ARCHITECTURE_CONCORDANCE_AUDIT/CATHEDRAL_FORMAT_VISUAL_PROVENANCE_2026-10-18.json`.

Their bounded reading is retained:

- `.scarab`: documented core-container role with one inspected JSON sample;
- `.nxa`: documented axes/panels/flows role with one inspected JSON sample;
- `.xva`: documented audiovisual/axis-bridge role, with no standalone
  implementation recovered in the examined sources;
- UDF: inspected historical HTML/JSON prototype, distinct from the current
  `nexah.udf.orientation-return/0.1.0-experimental` profile.

The recurring architecture

```text
content / carrier
  → structured address and relation
  → time-dependent projection
  → explicit trace and Return
```

is a comparison frame only. No common codec, universal grid mechanism,
cross-format equivalence or automatic conversion is established.

NSNavigator disposition: reference-only extension of the existing Builder
brief and Mission Control opportunity. Canonical effect is `0` identities,
`0` relations and `0` aliases. A later semantic binder would require a
separate Science Desk and Navigator-governance return.

## Independent integration review · Pass 1 — 2 November 2026

This review replays existing sources and tests. It does not activate the
project or repair the concurrently edited A0 return.

| Scope | Review state | Verified now | Still missing |
|---|---|---|---|
| 1 · ULLINIRIUM View Anchor | `EXISTING VIEW / EXTENSION CONTRACT OPEN` | the A0 Blue/Pink module already binds the `12+1` local coordination view, `135°` rotatable View Anchor, four shadow residuals and Pink/Blue covariant views around a common Return pivot | meaning of `13 ↔ 3,1 / 1,3` and `AL U Li Ri Um Ti tan`; a typed transition, inverse and Return connecting the existing view to Cube/Q4 and `LUX → nXeT → XVA` |
| 2 · address arithmetic | `EXACT CORE / OPEN READING` | `L=50`, `L×L+1=2501=41×61`, `2×2501=5002`, `5002−2501=2501`; LUX/PINK/BLUE independently reproduce A1Z26 `57/50/40` and German Scrabble without bonuses `11/10/7` | a declared map from `12+12` to the address arithmetic |
| 3 · hourglass / X Cube | `PARTIAL VIEW` | A0 already contains the rotated static Hourglass bench; Leaf Fold now exposes the Q4 antipode/window ledger and Blue/Pink view control | one typed state shared by hourglass, Cube/Q4 crossing, transition and exact inverse; the glyph alone is not the contract |
| 4 · LUX → nXeT → XVA | `PARTIAL ROUTE` | LUX is an executable word fixture and can display the separate 2501/5002 address relation | `nXeT` exists only as a working label; XVA remains historical provenance; no executable end-to-end transition or Return exists |
| 5 · historical visual lens | `PROVENANCE-BOUND / NOT BUILT` | the eleven-stage gallery path and Alpha/Beta/Gamma variants are retained in the Cathedral visual provenance audit | an interactive sequence `11-stage → lowered T → α/β/γ → GLB/Cube`, with variant identity and source status preserved |

### Regression replay at review time

- `a0-ioi-leaf-fold-tour-tests.cjs`: `PASS`, `81` checks;
- `a0-root7-q4-coupling-tests.cjs`: `PASS`, `354` checks;
- `a0-coupled-window-tests.cjs`: `FAIL` because the test still expects
  `56` tour stations while the current Bench displays `62`;
- `a0-ninefold-three-window-integration-tests.cjs`: `FAIL` because the bound
  Leaf Fold hash still records
  `0b66c856135e00b0f68bffc4ca8df678e7792395e14a3eeed457909f33aba2f9`,
  while the concurrently edited source currently hashes to
  `b995efc2113f4391cd3dd11fcc2436c8b369a8504293f9194f10ab520adb8141`.

The two failures are return/currentness gaps, not evidence against the exact
arithmetic or Q4 controls. They must be closed by the active A0 writer before
this review may call the integrated cut green.

### Review verdict

The exact numerical findings are small but solid. The larger value is the
typed integration opportunity: one interface could let a reader move from
address arithmetic through a hinge/antipode view into a historical
axis/bridge projection while preserving source, view and Return separately.
At review time that integration was not yet implemented; the subsequent
bounded cut below does not turn it into scientific novelty.

## Owner-authorized bounded connector cut — 3 November 2026

State: `LOCAL_BUILD_COMPLETE / OWNER_AUTHORIZED_BOUNDED_EXTENSION / NOT_PUBLISHED`

The previously open typed integration opportunity is now implemented inside
the existing Blue/Pink source instrument. It reuses `OP-UDF-01`, `BT-045`,
the existing ULLINIRIUM local coordination view and `MOD:TESSAREC`; it does
not activate the wider UDF backlog or the parked Human participant gate.

Implemented route:

```text
ULLINIRIUM outer view slot 1…12
  → declared ordinal binding
  → one of 12 unordered Q4 antipodal face pairs
  → YELLOW or PINK split-route view (`nXeT` working label)
  → XVA provenance receipt view
  → exact source slot Return (`A²=id`)
```

The common ULLINIRIUM pivot remains a Return witness and is not mapped to a
thirteenth Q4 object. The bridge is an exact `12↔12` index bijection, not a
geometric identity. The LUX lens displays the independent exact arithmetic
`L×L+1=50²+1=2501` and `2×2501=5002`; neither address is derived from the
selected ULLINIRIUM slot. `nXeT` remains a lowered-T route label rather than
an operator, and XVA remains historical Axis/Bridge provenance rather than a
recovered format implementation.

Owning implementation:

- `A0_BOOK/A0_BLUE_PINK_DODECA_CELL_RETURN.html#ulliniriumQ4ViewAnchor`;
- `A0_BOOK/a0-ullinirium-q4-view-anchor.js`;
- `A0_BOOK/a0-ullinirium-q4-view-anchor-tests.cjs`.

Verification:

- ULLINIRIUM/Q4 connector: `PASS`, `25` checks;
- existing Q4 face coupler: `PASS`, `54` checks;
- existing UDF orientation Return: `PASS`, `5/5` proofs;
- existing Root7/Q4 coupling: `PASS`, `354` checks;
- local browser interaction: Pink and Yellow routes preserve their endpoints,
  use distinct hinge views and Return to the selected source slot.

NSNavigator disposition: source-bound implementation extension only. Reused
identities are `MOD:TESSAREC`, `BT-045` and `OP-UDF-01`; canonical effect is
`0` identities, `0` relations and `0` aliases. The implementation creates no
Study, Finding, capability, publication or public admission.

## Owner-authorized THE MACHINA consumer cut — 3 November 2026

State: `LOCAL_BUILD_COMPLETE / EXISTING_MACHINA_ASSEMBLY_PORT / NOT_PUBLISHED`

The typed fixture is now implemented as `ULLINIRIUM / SCARAB VIEW PORT`
inside the existing THE MACHINA Assembly. It consumes the connector receipt;
it is not a seventh Assembly station, ninth body, new machine or `.scarab`
carrier implementation.

```text
INSIDE  · ULLINIRIUM source slot
  → OUTSIDE · Q4 antipodal pair / SCARAB view
  → INSIDE  · exact source-slot Return
```

The Owner shorthand `IOI (j)` is recorded as a working display mark only;
`j` is not promoted to an operator. Yellow and Pink preserve distinct split
paths with the same endpoints. LUX `2501/5002` remains a separate address
lens. The port mutates neither source nor GLB and creates no carrier identity,
Navigator relation, Study, Finding, capability or publication effect.

Owning implementation:

- `A0_BOOK/A0_MACHINA_COCKPIT.html#ulliniriumScarabPort`;
- `A0_BOOK/a0-machina-ullinirium-scarab-port.js`;
- `A0_BOOK/a0-machina-ullinirium-scarab-port.css`;
- `A0_BOOK/a0-machina-ullinirium-scarab-port-tests.cjs`.

Verification: `PASS`, `35` port checks; existing connector `25`, Q4 coupler
`54` and Machina Assembly `32/32` remain green. Browser interaction verified
Pink route plus `IN → OUT → IN` exact Return to the selected slot.

## Owner-authorized Three‑Vortex sorting view — 3 November 2026

State: `LOCAL_BUILD_COMPLETE / EXISTING_RELATION_CHAMBER_VIEW / NOT_PUBLISHED`

The historical visual set is now sorted inside the existing THE MACHINA
Relation Chamber as a `Three‑Vortex Switchyard`. This is a consumer view of
the existing ULLINIRIUM/Q4 port and evidence line. It is not a new project,
machine, operator, carrier, capability or Source Graph identity.

```text
NT · NUMBER / TOPOLOGY VIEW
  → SG · SCARAB / GEOMETRY VIEW
  → ER · EXIT / RETURN VIEW
  → NT · EXACT VIEW RETURN
```

The common `}{` sandglass is an internal handoff pivot. The three number
registers remain explicitly separate:

- `12×12 = 144`: even finite view register; four cells meet around the
  geometric centre;
- `11×11 = 121`: odd observer grid; one centre cell;
- `23³ = 12167₁₀ = 2F87₁₆`: address / base-translation view, not a grid-centre
  claim.

The exact marker `17399 = 127×137` is displayed separately. Historical
`α/NXA`, `β/SCARAB` and `γ/XVA` are view labels only. `SG` in this control is
`Scarab / Geometry`, not the Source Graph prefix, and the three visual
vortices assert no physical vortex mechanism.

Owning implementation:

- `A0_BOOK/A0_MACHINA_COCKPIT.html#threeVortexSwitchyard`;
- `A0_BOOK/a0-machina-three-vortex-switchyard.js`;
- `A0_BOOK/a0-machina-three-vortex-switchyard.css`;
- `A0_BOOK/a0-machina-three-vortex-switchyard-tests.cjs`.

Verification: `PASS`, `32` switchyard checks. The visible six-step automatic
demo and manual tour now stage source reading, SG geometry, the `11×11`
centre-type change, ER / `23³`, the `}{` receipt handoff and exact NT / `12×12`
Return. Browser interaction verified the intermediate state and final Return.
Canonical effect is `0` identities, `0` relations and `0` aliases.

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
