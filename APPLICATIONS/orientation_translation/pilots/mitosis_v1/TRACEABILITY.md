# Traceability

## Source codes

| Code | Fixed source region |
|---|---|
| M-S-LEAD | lead definition, stages, results, errors, organismal variation |
| M-S-OV | Phases / Overview |
| M-S-INT | Interphase |
| M-S-PRE | Preprophase |
| M-S-PRO | Prophase |
| M-S-PROM | Prometaphase |
| M-S-META | Metaphase |
| M-S-ANA | Anaphase |
| M-S-TELO | Telophase |
| M-S-CYTO | Cytokinesis |
| M-S-FUNC | Function |
| M-S-VAR | Variations / Forms of mitosis |
| M-S-ERR | Errors and other variations |
| M-S-DIAG | Diagnostic marker |

Every code resolves only to Wikipedia revision `1359310650`.

## Observation → representation mapping

| Representation | Observations | Principal source codes |
|---|---|---|
| M-REP-01 Phase landmarks | 03, 04, 06, 08–12 | PRO, PROM, META, ANA, TELO |
| M-REP-02 Chromosome continuity/state | 02–04, 07–12, 17, 20 | OV, PRO–TELO, ERR |
| M-REP-03 Spatial reorganization | 04–08, 10–14 | PRE, PRO–CYTO |
| M-REP-04 Attachment/conditions | 07–09, 17 | PROM, META, ERR |
| M-REP-05 Process boundary | 01–02, 12–14, 20 | LEAD, OV, INT, TELO, CYTO |
| M-REP-06 Variation/outcome | 05–06, 11, 14, 16–19 | PRO, PROM, ANA, CYTO, VAR, ERR, DIAG |
| M-REP-07 Result/function | 01, 12–15, 17–18 | LEAD, OV, TELO, CYTO, FUNC, ERR |

## Representation → path → neighborhood candidates

| Path | Representations | Candidate node families | Admission authority |
|---|---|---|---|
| A Named landmarks | REP-01, 05, 07 | focal process, phases, nuclei, Cytokinesis | Neighborhood edge audit |
| B Chromosome continuity | REP-02, 01 | replicated chromosomes, sister chromatids, condensation, daughter chromosomes | Neighborhood edge audit |
| C Spatial reorganization | REP-03, 01 | spindle, kinetochores, metaphase plate, poles, nuclear envelope | Neighborhood edge audit |
| D Continuation/deviation | REP-04, 06 | attachment, checkpoint, nondisjunction, multipolarity | Neighborhood edge/rejection audit |
| E Process boundary | REP-05, 07 | Interphase prerequisite, Mitosis, Cytokinesis, daughter nuclei/cells | Neighborhood edge audit |

## Status firewall

- Source codes import tertiary-source evidence.
- M-OBS records are source-grounded observations.
- M-REP and paths are editorial orientation operations.
- M-N/M-E records are later neighborhood decisions.
- Unresolved questions, candidate bridges, and rejected interpretations cannot be promoted without a new source or governed stage.

No trace path authorizes comparison, hypothesis, Atlas membership, graph merge, or canonical vocabulary.
