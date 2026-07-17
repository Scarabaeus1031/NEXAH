# Identity Tests

Identity is the strongest and most dangerous comparison claim. It must be established through scoped evidence, not resemblance.

## Candidate indicators

| Candidate indicator | Sufficient alone? | What it can support | Failure risk |
|---|---|---|---|
| Same label | No | Candidate review | Homonymy, translation variation, or different scope |
| Same function | No | Functional correspondence | Different entities can perform the same function |
| Same source concept | No, unless source identity and scope are also fixed | Strong identity candidate | Sources can use one term at different granularity |
| Same role | No | Role correspondence | Role is local and editorial |
| Same position | No | Structural analogy | Position depends on local topology |
| Same process | No | Process correspondence | Different representations can participate in one process |
| Same scale | No | Scale compatibility | Many distinct entities share a scale |
| Same canonical external identifier and matching scope | Strong but still reviewed | Referential identity | Version, edition, or context may differ |
| Matching definition, referent, scope, and evidence | Yes for a scoped comparison claim | Reviewed identity correspondence | Later source revisions require versioning |

## Identity procedure

1. Resolve each node to its immutable local record.
2. Compare referent, definition, scope, scale, source, and version.
3. Record label differences without normalizing them away.
4. Test for narrower, broader, overlapping, or disjoint scope.
5. Classify the result:

   - `same_scoped_referent`
   - `partial_overlap`
   - `functional_analogue`
   - `same_label_different_referent`
   - `different`
   - `unresolved`

6. Preserve both local identities regardless of result.

## Identity firewall

Even `same_scoped_referent` creates a comparison correspondence, not one merged node. Local roles, evidence, edges, and histories remain attached to their original neighborhood.

## Insufficient tests

String matching, embeddings, diagram alignment, shared parent terms, and analyst familiarity may nominate candidates. None may decide identity.
