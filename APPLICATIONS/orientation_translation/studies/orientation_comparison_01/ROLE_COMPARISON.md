# Role Comparison

Role describes what a representation does inside a particular Orientation Neighborhood. It does not define what the representation is.

## Core findings

- Identical nodes may legitimately receive different roles.
- Different nodes may legitimately receive identical roles.
- A role change does not invalidate comparison when it is explicit and locally justified.
- Role equivalence never establishes node identity.

## Comparison cases

| Case | Interpretation | Valid comparison? | Required preservation |
|---|---|---|---|
| Same identity, same role | Local functions align | Yes | Different evidence and paths may remain |
| Same identity, different role | The same scoped referent serves different orientation purposes | Yes; often highly informative | Both role rationales and contexts |
| Different identity, same role | Functional analogy | Yes, as role correspondence only | Explicit non-identity |
| Different identity, different role | No role match | Yes, as a recorded difference | Do not force a common category |
| Unresolved identity, same role | Candidate functional correspondence | Conditional | Identity remains unresolved |
| Role absent in one neighborhood | Asymmetry or recording difference | Yes | Absence versus unrecorded must be distinguished |

## Role record

```yaml
local_object:
neighborhood:
role:
role_definition:
reader_question:
rationale:
source_supported: true | false | mixed
alternatives:
```

## Role-change rule

A role may change across neighborhood versions only through a versioned editorial decision. Cross-neighborhood comparison merely observes different roles; it does not rewrite either role.

## Failure boundary

If roles are normalized into one universal taxonomy before local meanings are inspected, comparison becomes role collapse. A shared vocabulary may be useful later, but it cannot replace local role evidence.
