# NN / ILAU crosswalk — 432 record/play and gap-to-return

Date: `2026-10-11`  
Status: **read-only Navigator audit; no new identity or relation admitted**

## Recovered Navigator route

The supplied white-background HTML series is already preserved in the NEXAH
Navigator as:

```text
route:     #ilau-orientation
binder:    NEXAH:NAVIGATOR:ILAU_ORIENTATION_INSTRUMENTS:V1:2026-10-09
status:    INTERNAL_READ_ONLY_SOURCE_BOUND_LENS
scope:     19 curated HTML instruments from one 28-HTML source family
```

The relevant existing identities are:

| Instrument | Existing ID | Family |
|---|---|---|
| The Record / Play Operator | `ILAU:RECORD_PLAY_432` | `RECORD_PLAY_FAMILY` |
| Intertwined Clefs / B–8–ß Loop | `ILAU:INTERTWINED_CLEFS` | `RECORD_PLAY_FAMILY` |
| BPS–MS · Cover, Cut, Kernel & Gap | `ILAU:BPS_MS_COVER_CUT_KERNEL_GAP` | `NEON_CARTOGRAPHY_FAMILY` |
| From Gap to Return | `ILAU:FROM_GAP_TO_RETURN` | `RETURN_RESIDUAL_FAMILY` |

The exact caption

```text
FRAME = 4 Quadranten · COVER = 5 Zustände · S = 1 Fixpunkt · LINSEN = Übergänge
```

is already present in the bound BPS–MS HTML. Its typed reading is:

- `4` counts frame quadrants;
- `5` counts cover states;
- `1` is the displayed common fixed point;
- lenses encode overlaps/transitions, not additional states.

## Existing checks versus open tests

Executed Navigator check:

```text
validate_ilau_orientation_binder.mjs
PASS · 63 checks · 0 failures
```

Those checks establish route status, publication and registry boundaries,
the nineteen-file count, ILAU order, file presence, byte counts and SHA-256
identity. They are custody/integrity checks, not a numerical BPS–MS experiment.

The controlling intake remains:

```text
B — COHERENT_OPERATIONAL_EXTENSION_TEST_REQUIRED
```

It explicitly records:

- `RC-01`, the minimum seam test: proposed, not executed in that intake;
- `NBV-01`, the n-band visibility and false-gate audit: proposed, not executed;
- BPS–MS: coherent method sketch, but without a complete typed band registry,
  calibration, weights, fusion rule, metric, cross-band invariant and artifact
  tolerance.

## Relation to the present 432 audit

The present `39/39` audit adds an exact finite arithmetic result to the
existing `ILAU:RECORD_PLAY_432` display:

```text
d = 180 * (3,4,6,8) = (540,720,1080,1440)
10 * 432/d          = (8,6,4,3)
return map          = k -> 24/k
return pairs        = 3 <-> 8, 4 <-> 6
```

This is a bounded arithmetic replay and a candidate source note for the
existing instrument. It does **not** operationalize BPS–MS, execute `RC-01` or
`NBV-01`, validate a physical frequency mechanism, or authorize a new
Navigator relation.

## New loose visual finds

The newly supplied MIAU dial is not source-less. The Navigator HTML registry
contains the frozen provisional test surface:

```text
ART:HTML:0A614C567C41
SCIENCE_LAB/CASE_STUDIES/
  NEXAH_DESKTOP_GOLD_CUSTODY_AND_NAVIGATOR_INTAKE_2026-10-07/
  sources/acr/NEXAH_MIAU_VOWEL_SOURCE_FILTER_TEST.html
```

Its current registry assessment is `provenance_or_unresolved`, historical,
provisional, low-confidence and `UNASSESSED`; it has no assigned module,
representation group or connection family. The HTML contains the exact
`i`-vowel formant tuple `(270,2290,3010)`. Consequently the dial's readouts

```text
2290+3010 = 5300
5300/270  = 19.629629... ~= 19.63
```

are reproducible as a source/filter summary, but they are not yet an admitted
Navigator mechanism.

No governed source match was recovered for the supplied WUFF
`attack -> /u/ core -> /f/ release` emblem or for the rendered Q432 coordinate
poster. They remain loose visual leads. The Q432 arithmetic itself is replayed
in M8 of this audit; source custody remains open.

## Governance return

Reuse the existing `#ilau-orientation` route and instrument identities. Do not
create a second HTML-series identity. A future binding of this audit into NN
requires an admitted source update or typed evidence relation under Navigator
governance.
