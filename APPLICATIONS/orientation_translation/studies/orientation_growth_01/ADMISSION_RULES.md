# Admission Rules

This document reconstructs the controls that admitted or rejected growth in the completed Photosynthesis sequence. It does not establish general rules for NEXAH.

## Status vocabulary

- **Explicitly used** — visible in the frozen artifacts.
- **Implicitly used** — necessary to explain the recorded procedure, but not stated as a rule.
- **Proposed generalization** — a candidate for an independent replication.
- **Unsupported** — not justified by the present evidence.

## Reconstructed rules

| ID | Rule | Status | Evidence | Role in bounded growth | Limitation |
|---|---|---|---|---|---|
| AR-01 | Do not admit a node merely because it is mentioned or linked. | Explicitly used | N, admission and exclusion logic | Prevents link accumulation from becoming orientation structure. | Relevance judgment remains editorial. |
| AR-02 | Do not admit an edge from shared vocabulary alone. | Explicitly used | N, transition audit | Protects against semantic collapse. | Vocabulary overlap can still prompt a question. |
| AR-03 | Direct source support permits review, not automatic admission. | Explicitly used | N, edge records | Keeps source support necessary while preserving a relevance decision. | The relevance threshold is not quantified. |
| AR-04 | Every admitted edge states why the transition exists, its support, and what it does not support. | Explicitly used | N, transition audit | Makes every transition inspectable. | Quality depends on the analyst's reading. |
| AR-05 | Indirect support requires an explicit missing-representation statement. | Explicitly used | N, indirect edge E25 | Keeps one inferential step visible instead of laundering it as direct evidence. | Only one indirect edge was tested. |
| AR-06 | Editorial bridges remain labeled and are not silently admitted as source-supported edges. | Explicitly used | R candidate bridges; N exclusions | Separates useful navigation from evidence claims. | Does not determine when a bridge should later be reviewed. |
| AR-07 | Unsupported expansions are excluded and recorded. | Explicitly used | R hidden questions and bridge classes; N exclusions | Makes rejection part of the record. | Rejection is local, not permanent. |
| AR-08 | A second-ring representation needs its own support audit. | Explicitly used | N, first and second rings | Prevents support from being inherited transitively. | The two-ring shape is pilot-specific. |
| AR-09 | A–B and B–C do not establish A–C. | Explicitly used | N, no-transitivity boundary | Blocks transitive overreach. | No adversarial transitivity test was run. |
| AR-10 | Visual proximity, symmetry, or diagram placement has no evidential authority. | Explicitly used | N, construction boundaries | Prevents aesthetic authority. | Reader perception was not tested. |
| AR-11 | A reverse edge requires independent support. | Implicitly used | N, directional transition records | Prevents reciprocity from being assumed. | The pilot did not perform a dedicated reciprocity test. |
| AR-12 | Source identity and evidence location remain attached to each transition. | Implicitly used | P traceability; N transition audit | Allows later reinspection and source-drift checks. | Granularity is document-level in places. |
| AR-13 | Freeze the evidence body before each expansion pass. | Proposed generalization | Reconstructed from the frozen P → R → N sequence | Would make additions comparable and protect earlier evidence. | Not independently reproduced. |
| AR-14 | Run reflection before neighborhood expansion. | Proposed generalization | R produced questions and bridge candidates later bounded in N | Could separate question formation from node admission. | A different workflow might combine these steps successfully. |
| AR-15 | Record each admission, rejection, and stop as a growth event. | Proposed generalization | Growth Event Register | Would preserve negative as well as positive change. | Adds editorial workload. |
| AR-16 | Every neighborhood must contain exactly two rings. | Unsupported | No general evidence beyond N | None. | Confuses this pilot's shape with a universal rule. |
| AR-17 | Every first-ring node must receive exactly one secondary neighbor. | Unsupported | N used this editorial limit once | None. | Symmetry may distort other subjects. |
| AR-18 | Direct support alone is always sufficient for admission. | Unsupported | Contradicted by N's relevance and boundary review | None. | Would produce graph expansion rather than orientation. |

## Essential controls in this case

The strongest local safeguards were AR-04, AR-05, AR-06, AR-07, AR-08, and AR-09. Together they preserved direction, support class, explicit uncertainty, rejection, and non-transitivity. AR-13–AR-15 remain candidate procedures only; they require an independent second pilot.

## Boundary

These are reconstructed editorial controls. They are not OLS requirements, Kernel behavior, Registry policy, or canonical architecture.
