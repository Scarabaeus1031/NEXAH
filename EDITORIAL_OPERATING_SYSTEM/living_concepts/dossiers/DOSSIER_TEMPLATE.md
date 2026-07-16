# Living Concept Dossier Template

**Status:** X1 review instrument · non-canonical

This template is intentionally smaller than a production schema. It supports
human review before identity, Registry, graph, or Kernel decisions.

## Required sections

1. **Identity boundary** — proposal key, preferred name, current status, and
   any existing Operator or Work identity.
2. **Reader definition** — one scoped, understandable proposal sentence.
3. **Definition layers** — current controlled, architectural, research,
   historical, and pedagogical formulations kept separate.
4. **Provenance** — verified source, locator, role, assertion origin, and claim
   support for every selected occurrence.
5. **Relations** — proposal relations with explicit direction and evidence;
   co-occurrence is insufficient.
6. **Exclusions** — meanings, aliases, claims, and identities that must not be
   silently merged.
7. **Open questions** — unresolved conceptual, scientific, and editorial
   questions.
8. **Human decisions** — a small checkpoint that can be accepted, revised, or
   deferred independently.

## Governance rules

- Use a local `concept:...` proposal key; never allocate an `NX-C-...` ID in X1.
- Existing Registry and Operator identities remain authoritative in their own
  scope.
- A historical occurrence establishes lineage, not validity.
- A Work title does not create a Concept.
- A research result does not define the broader Concept automatically.
- Definition variants remain separate until a human editor approves their
  relationship.
- Proposed relations are not graph edges and are not visible to the Kernel.
- Every claim must state its support scope or remain explicitly unassessed.

## Minimal YAML shape

```yaml
candidate_key:
preferred_name:
status: non_canonical_review
identity_boundary:
reader_definition:
definition_layers: []
occurrences: []
proposed_relations: []
exclusions: []
open_questions: []
human_decisions_required: []
recommendation:
```
