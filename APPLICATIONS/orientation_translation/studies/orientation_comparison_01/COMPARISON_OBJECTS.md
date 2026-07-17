# Comparison Objects

A comparison object is a frozen, addressable record whose provenance and meaning can be inspected independently in each neighborhood. Not every visible element qualifies.

| Candidate | Eligible? | What may be compared | Required boundary | Why it matters |
|---|---|---|---|---|
| Node | Conditional | Identity claims, label, scope, scale, role, source grounding | Never merge node records; compare referenced identities | A label can conceal different meanings. |
| Edge | Yes | Existence, direction, relation statement, support, scope, exclusions | Each direction and evidence record remains separate | Similar endpoints do not guarantee the same relation. |
| Role | Yes | Editorial or orientational function within each neighborhood | Role is contextual, not identity | Shows how the same representation may function differently. |
| Support class | Yes | Classification and evidence basis | Compare definitions and underlying evidence, not labels alone | Prevents evidence laundering. |
| Neighborhood | Yes | Scope, structure, provenance, admission policy, stopping boundary | Whole inputs remain immutable | Enables comparison without graph merging. |
| Reader path | Conditional | Intended sequence, audience, purpose, and evidence basis | Paths are editorial constructions, not source relations | Useful only if both neighborhoods record them explicitly. |
| Lens | Conditional | Question, viewpoint, output, and limits | Similar lens names do not establish equivalent operations | May reveal different modes of orientation. |
| Stopping boundary | Yes | Stop reason, unresolved branches, reopen conditions | Size is not a proxy for completeness | Exposes how each neighborhood limits growth. |
| Rejection | Yes | Candidate relation, rejection reason, evidence gap, decision status | Rejections remain local and revisable only by version | Negative evidence can distinguish neighborhoods. |
| Bridge | Conditional | Status, endpoints, rationale, and admission state | Editorial bridges cannot become sourced edges by comparison | Reveals possible navigation without promotion. |
| Growth event | Conditional | Event type, input, decision, boundary effect | Requires a compatible event record, not identical chronology | Supports process comparison without forcing structural sameness. |

## Non-objects

The following are not sufficient comparison objects by themselves:

- visual proximity;
- color or icon;
- diagram position;
- raw label occurrence;
- node count;
- edge count;
- topological resemblance;
- an unrecorded intuition that two items are related.

## Preferred comparison hierarchy

1. Compare immutable neighborhood packages and their authority boundaries.
2. Compare their decision records and support systems.
3. Compare addressable nodes, edges, roles, rejections, and stops.
4. Only then record reviewed cross-neighborhood correspondences.

The hierarchy prevents component-level resemblance from silently collapsing the two wholes.
