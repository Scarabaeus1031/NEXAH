# Reviewer Attack

| # | likely reviewer question | strongest current answer | evidence available | severity | blocks paper? |
|---:|---|---|---|---|---|
| 1 | Is this not simply good scientific practice? | Much of it is established good practice; the candidate contribution is a stricter integrated record and non-collapse discipline. | Frozen core, formal proposal | CRITICAL | YES unless prior-art comparison identifies a real contribution |
| 2 | What is technically novel? | No technical novelty is established locally. A combined method may be distinctive, but that is untested. | Novelty boundary; Foundation V0.1 | CRITICAL | YES for novelty claims |
| 3 | Where is the comparative baseline? | There is no comparison against provenance/workflow/type-system methods; case baselines address local computations only. | IEEE and EXP-00 records | CRITICAL | YES |
| 4 | Why is a new vocabulary needed? | Only the neutral typed distinctions are defensible; NEXAH-specific names are unnecessary to the paper. | NOS-01 metaphor-removal control | HIGH | NO if vocabulary is minimized |
| 5 | What is machine-enforced and what is documentary? | RID provides schema-level fixtures and ORION provides a narrow implementation; most framework and authority boundaries remain documentary. | RID-01, SWM-01, ORION baseline | HIGH | Blocks executable-system claims |
| 6 | What is independently reproduced? | No scientific result. IEEE replay independently reimplemented operators but establishes internal specification equivalence only. | IEEE replay and validation records | HIGH | NO if bounded explicitly |
| 7 | What generalizes beyond selected examples? | Only the proposed audit vocabulary and procedure are intended to generalize; empirical or physical mechanisms do not. | WNI, TITAN, NOS, EXP-00 | HIGH | Blocks empirical generalization |
| 8 | What does NEXAH do that provenance systems, workflow systems, or type systems do not? | The record proposes one joined treatment of representation change, loss, trace, interpretation, and authority; superiority or uniqueness is unestablished. | Frozen core and schema | CRITICAL | YES, until literature review |
| 9 | Where is usefulness to external users demonstrated? | It is not demonstrated. Internal cases show inspectability, not user benefit or adoption. | Current evidence ladder | HIGH | Blocks usefulness claims; not a bounded methods description |
| 10 | Is Human Authority formalized or merely asserted? | It is a declared separate role and decision boundary, but no formal behavioral model or user evaluation exists. | Freeze, NEXUS-01, RID-01 | HIGH | Blocks formal governance and HCI claims |

## Reviewer-risk summary

The fatal risk is overclaiming novelty, validation, or system capability. The strongest defensible response is a narrow methods paper that openly states the lack of external validation and treats bounded cases as demonstrations of audit discipline. A literature review and skeptical external technical review are required before submission.

