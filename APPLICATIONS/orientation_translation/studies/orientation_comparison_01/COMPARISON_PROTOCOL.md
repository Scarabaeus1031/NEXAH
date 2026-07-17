# Comparison Protocol

This protocol is designed for future use after two independently frozen Orientation Neighborhoods exist.

## Required inputs

- immutable neighborhood A and B identifiers and versions;
- their source and provenance records;
- node, edge, role, support, rejection, bridge, growth, and stopping records where available;
- an explicit comparison question;
- named reviewers and review date;
- declared tool assistance, if any.

## Procedure

| Step | Operation | Required output | Preserved property | Stop condition |
|---|---|---|---|---|
| 0. Verify independence | Confirm distinct source boundaries, construction histories, and no inherited results. | Independence record | Independence | Stop if one input copied or mutated the other. |
| 1. Freeze inputs | Hash or otherwise fix both packages and versions. | Input manifest | Traceability | Stop if either input is unstable. |
| 2. Declare question | State why comparison is being attempted and what it excludes. | Comparison scope record | Uncertainty and purpose | Stop if no bounded orientation question exists. |
| 3. Inventory objects | Identify eligible objects without matching them. | Two local inventories | Local identity | Stop if required records are missing. |
| 4. Nominate candidates | Generate possible correspondences from evidence, not appearance alone. | Candidate list with nomination reason | Independence | Appearance-only candidates remain unadmitted. |
| 5. Test identity | Apply referent, definition, scope, scale, source, and version tests. | Dimension-specific identity results | Identity and difference | Unresolved identity blocks edge equivalence. |
| 6. Compare roles | Compare local functions separately from identity. | Role correspondence and divergence records | Context | No role normalization. |
| 7. Compare edges | Test endpoints, direction, semantics, support, scope, and exclusions. | Edge correspondence records | Direction and support | Stop each edge if evidence is insufficient. |
| 8. Test reciprocity | Evaluate both directions independently. | Reciprocity classifications | Direction | No reverse edge by implication. |
| 9. Record asymmetry | Document structural, evidential, role, scale, rejection, and stopping differences. | Asymmetry register | Difference and uncertainty | None; difference is a valid result. |
| 10. Compare boundaries | Review stopping, rejection, unresolved questions, and reopen rules. | Boundary comparison | Stopping and rejection | No inference from size alone. |
| 11. Audit failures | Run all comparison failure-mode checks. | Failure audit | Integrity | Any destructive merge or support transfer invalidates the comparison. |
| 12. Evaluate Atlas eligibility | Apply minimum criteria without constructing an Atlas. | Eligibility recommendation | Governance | Human approval required; no automatic admission. |
| 13. Freeze comparison | Preserve inputs, outputs, uncertainties, reviewer decisions, and hashes. | Versioned comparison package | Reproducibility | Later changes require a new version. |

## Mandatory output fields

Every correspondence or difference must include:

```yaml
comparison_id:
question:
object_a:
object_b:
dimension:
result:
evidence_a:
evidence_b:
rationale:
direction:
support_difference:
uncertainty:
preserved_asymmetry:
rejected_implications:
reviewer:
input_versions:
```

## Prohibitions

The protocol must not:

- mutate either neighborhood;
- merge nodes or edges;
- transfer evidence or support;
- assume reciprocity or transitivity;
- normalize roles before comparison;
- infer correspondence from layout;
- treat absence as rejection;
- convert a recommendation into Atlas membership;
- create canonical identities, ontology, or OH-001.

## Valid final results

A comparison may conclude equivalence in one dimension, compatibility, material difference, incomparability, unresolved status, or no meaningful comparison. Failure to find symmetry is not protocol failure.
