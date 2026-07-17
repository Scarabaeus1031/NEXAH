# Comparison Dimensions

Each dimension asks a bounded question. No dimension may stand in for another.

| Dimension | What is compared | What is not inferred | Minimum record |
|---|---|---|---|
| Identity | Whether two references denote the same scoped representation | Same label, role, or location is not identity | Two immutable references, identity test, result, confidence, reviewer |
| Direction | A → B independently from B → A | Reciprocity or undirected relation | Directional statement and evidence per direction |
| Evidence | Source type, location, entailment, support class, uncertainty | Equal support labels do not imply equal evidence quality | Source citation, support rationale, unsupported implication |
| Role | Function within each local neighborhood | Role does not define the entity | Local role, reason, scope, alternatives |
| Scale | Representational or domain scale and transitions between scales | Proximity across scales does not imply causal continuity | Declared scale and explicit scale change |
| Function | What the object or relation does for orientation | Function is not identity or scientific mechanism | Function statement and reader question |
| Neighborhood depth | Distance under each neighborhood's own construction rules | Equal depth does not imply equal importance | Local depth definition and path |
| Stopping behavior | Stop reason, unresolved branches, and reopen rule | Larger size is not greater completeness | Stopping record and boundary |
| Rejections | What was considered but not admitted and why | Absence is not rejection without a record | Candidate, decision, reason, evidence gap |
| Bridge structure | Explicit editorial or evidential connectors | A bridge is not automatically an edge | Bridge status, endpoints, purpose, limits |
| Hidden questions | Questions exposed but unanswered | Shared questions do not prove shared answers | Question, originating artifact, status |
| Growth events | Admissions, rejections, revisions, and closure events | Identical sequence is not required | Event identity, trigger, decision, effect |

## Dimension independence

A positive result in one dimension cannot settle another. Examples:

- identity does not establish identical role;
- identical role does not establish identity;
- shared evidence class does not establish the same relation;
- matching direction does not establish reciprocity;
- matching topology does not establish matching meaning;
- shared scale does not establish comparable function.

## Comparison output

Every comparison statement should contain:

```yaml
object_a:
object_b:
dimension:
result: equivalent | compatible | different | incomparable | unresolved
rationale:
evidence:
uncertainty:
preserved_difference:
reviewer:
```

`Equivalent` is dimension-specific. It never authorizes merging the underlying records.
