# Comparison Failure Modes

| Failure mode | Trigger | Symptom | Damage | Required safeguard | Detection test |
|---|---|---|---|---|---|
| Forced symmetry | Comparison expects matching counts, rings, roles, or paths. | Differences are normalized or marked incomplete. | Independent structure is erased. | Permit asymmetric outputs and `incomparable`. | Remove the template and check whether the result changes. |
| False reciprocity | A → B is treated as evidence for B → A. | One line represents two unreviewed directions. | Direction and support are laundered. | Separate directional records and evidence. | Audit every reciprocal claim for two source records. |
| Identity collapse | Same label, role, or position is treated as same entity. | Local nodes are merged prematurely. | Scope, version, and provenance disappear. | Apply scoped identity tests and preserve both records. | Test homonyms, broader/narrower terms, and version differences. |
| Graph merging | Comparison rewrites inputs into a combined graph. | Original edge and rejection histories become inaccessible. | Evidence boundaries are destroyed. | Produce an external correspondence layer only. | Verify byte-identical inputs before and after comparison. |
| Role collapse | Local roles are forced into one universal category. | Same identity cannot retain different functions. | Editorial context is lost. | Compare roles independently from identity. | Include same-node/different-role cases. |
| Support laundering | Strong evidence in one neighborhood upgrades a weaker correspondence. | Support classifications converge after comparison. | Unequal evidence appears equal. | Preserve source-specific support and prohibit transfer. | Compare pre/post support records for mutation. |
| Cross-scale confusion | Similar labels or relations span different scales without declaration. | A transition appears continuous across incompatible levels. | Meaning and possible causality are distorted. | Record scale on objects and edges; permit incomparability. | Require explicit scale alignment for every match. |
| Atlas inflation | Any shared term or edge is treated as sufficient for an Atlas. | Two neighborhoods are branded an Atlas without comparison governance. | Atlas becomes a decorative aggregate. | Apply minimum Atlas criteria and human approval. | Attempt admission using only shared vocabulary; it must fail. |
| Comparison by appearance | Layout, color, icon, topology, or node count drives correspondence. | Visually similar diagrams receive high confidence. | Aesthetic form becomes epistemic authority. | Compare semantic and evidence records before visuals. | Randomize layout while holding records fixed. |
| Template copying | A second neighborhood copies the first one's lenses, rings, or stops. | Artificial similarity appears as reproducibility. | Independence is invalidated. | Record construction provenance and allow structural difference. | Compare creation histories and preregistered constraints. |

## Additional risks

- **Absence confusion:** unrecorded, rejected, and genuinely absent are treated alike.
- **Version confusion:** correspondences span different source or neighborhood versions silently.
- **Resolution mismatch:** fine-grained nodes are compared with broad composites.
- **Comparator authority:** one reviewer silently resolves uncertainty for both neighborhoods.
- **Comparison accumulation:** provisional correspondences become de facto canonical through repetition.

The protocol must fail closed: an unresolved or incomparable result is preferable to a forced match.
