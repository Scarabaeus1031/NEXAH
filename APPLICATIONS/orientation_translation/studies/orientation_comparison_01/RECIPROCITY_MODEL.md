# Reciprocity Model

Reciprocity is a reviewed relationship between two independently supported directional edges. It is not the automatic inverse of one edge.

## Directional test

Given A and B, create two separate questions:

1. What supports A → B, within which scope, and with which exclusions?
2. What supports B → A, within which scope, and with which exclusions?

Then classify:

| Result | Condition |
|---|---|
| `reciprocal_supported` | Both directions are independently supported with compatible relation semantics and scope. |
| `bidirectional_different` | Both directions are supported but express different relations, roles, or scopes. |
| `one_way_supported` | Only one direction is supported. |
| `editorial_reverse_only` | Reverse direction is useful for navigation but not source-supported. |
| `apparent_reciprocity` | Diagram or language suggests two-way relation without two evidence records. |
| `incomparable` | Scale, scope, or identity prevents directional comparison. |
| `unresolved` | Evidence is insufficient. |

## When reciprocal appearance misleads

- one edge is causal and the other is contextual;
- one direction is source-supported and the reverse is editorial;
- endpoints overlap only partially;
- scale changes between directions;
- relation wording is symmetric but the process is not;
- a graph renderer draws one line for two different claims;
- shared labels conceal different scoped identities.

## Reciprocity record

```yaml
edge_forward:
edge_reverse:
forward_support:
reverse_support:
scope_alignment:
semantic_alignment:
classification:
asymmetry_preserved:
unsupported_implications:
```

## Boundary

Reciprocity can be established only after identity, direction, evidence, semantics, and scope are reviewed. It never follows from co-occurrence or shared diagrams.
