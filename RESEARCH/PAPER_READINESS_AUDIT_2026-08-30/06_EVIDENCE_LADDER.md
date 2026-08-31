# Evidence Ladder

Evidence classes used here:

- L0: expression, narrative, or orientation aid.
- L1: conceptual or documentary structure.
- L2: formal artifact, implementation artifact, or reproducible local computation.
- L3: externally validated scientific or operational evidence.

| claim | source | evidence type | reproducible? | independent? | boundary | paper role |
|---|---|---|---|---|---|---|
| The frozen framework has a coherent typed core | Framework freeze; NOS-01 | DOCUMENTARY_SYNTHESIS — L1 | YES, by document inspection | NO | Coherence is not novelty or validity | Central framework definition |
| The core survives metaphor removal | NOS-01 | DOCUMENTARY_SYNTHESIS — L1 destruction control | YES | NO | Shows internal robustness only | Core contribution support |
| A representation-change audit can be expressed formally | `STATE_TRANSITION_ORIENTATION_FRAMEWORK_V0_1.md` | FORMAL_EXAMPLE — L1–L2 proposal | YES | NO | Non-normative; no theorem or novelty claim | Main formal exposition |
| A machine-readable contract exists | RID-01 | IMPLEMENTATION_EVIDENCE — L2 schema plus 20 fixtures | YES, schema level | NO | No validator, serializer, runtime, or integrated prototype | Formal artifact |
| A narrow implementation baseline exists | ORION V1 certified baseline | IMPLEMENTATION_EVIDENCE — L2 software/release artifact | YES within repository | NO | No reasoning, decision making, gateway, application, or full NEXAH machine | Implementation boundary |
| A normative orientation language exists | OLS 1.0 | IMPLEMENTATION_EVIDENCE — L2 specification release | YES | NO | Specification publication is not scientific validation | Vocabulary/contract support |
| Winding preservation is conditional and representation-bound | WNI-01 | FORMAL_EXAMPLE — L2 computational control | YES | NO | Standard winding result; no prime/grid topology novelty | Formal case study |
| External science can be typed without becoming NEXAH evidence | TITAN-01 | EXTERNAL_CASE — L1 documentary control | YES by source mapping | Source science YES; NEXAH mapping NO | No new capability or scientific discovery | External control example |
| The integrated architecture is coherent but incomplete | NOS-01; SWM-01; RID-01 | DOCUMENTARY_SYNTHESIS / IMPLEMENTATION_EVIDENCE — L1–L2 | YES | NO | Interface and executable-machine gaps remain | Limitation and architecture appendix |
| IEEE Geometry operators are reproducible against frozen artifacts | IEEE validation and replay records | SCIENTIFIC_EVIDENCE — L2 bounded deterministic computation | YES | PARTIAL, implementation only | Internal specification equivalence; no independent scientific validation | Secondary applied case |
| IEEE Geometry predicts useful power-system outcomes | None | No adequate evidence | NO | NO | No operational outcome, calibrated uncertainty, external baseline, or field validation | Must not claim |
| EXP-00 contains a bounded positive result | EXP-00 v1/v2 decisions | SCIENTIFIC_EVIDENCE — L2 controlled local computation | YES for retained packages | NO | Passing pairs depend on trajectory; no general fusion advantage | Positive bounded example |
| EXP-00 contains a bounded negative result | EXP-00 v1/v2 decisions | SCIENTIFIC_EVIDENCE — L2 controlled local computation | YES | NO | Continuous quality and some representation pairs failed | Negative/self-correcting example |
| Non-citable evidence can be stopped without deletion | EXP-00 MC002 closure | DOCUMENTARY_SYNTHESIS — L1–L2 custody/reproducibility decision | Partly | NO | Package explicitly closed not citable | Fail-closed example |
| Older transition-geometry experiments establish a universal mechanism | Historical validation/finding summaries | Mixed local computation | PARTIAL | NO | Single-runner, no independent replication, no general statistical or causal basis | Exclude |
| Visual and symbolic recurrences establish scientific structure | Visuals and translations | L0 expression | Display reproducible only | NO | Similar appearance is not mechanism | Exclude |

## Ladder judgment

The central methodological claim reaches L1–L2. The corpus contains meaningful formal, documentary, and computational artifacts, including negative controls. It does not reach L3 for public usefulness, scientific novelty, predictive utility, or cross-domain mechanism.
