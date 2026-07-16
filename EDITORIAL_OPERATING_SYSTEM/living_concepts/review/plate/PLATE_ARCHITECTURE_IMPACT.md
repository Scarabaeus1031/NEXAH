# Plate — Architecture Impact Review

**Phase:** X3 · bounded editorial research  
**Decision scope:** impact assessment only  
**Architecture v1.0:** unchanged

## Executive assessment

Plate clarifies NEXAH if it names an existing **human-facing editorial
pattern**: a bounded presentation of a larger field from a situated view. It
creates confusion if promoted into a universal primitive or used to rename
existing technical structures.

No architecture change is warranted by the present review.

## Classification assessment

| Candidate classification | Evidence | Assessment |
|---|---|---|
| Concept | recurring meaning exists, but no reviewed definition, evolution timeline, or stable occurrence set | not ready |
| Explanatory metaphor | clearly helps explain representation limits and perspective | supported |
| Visual grammar | direct use across Atlases, Maps, Whiteboards, and historical visual manifests | strongly supported |
| Editorial pattern | Library Architecture names Plate; Works use it for compression, sequence, projection, and perspective | strongest classification |
| Orientation primitive | existing primitives already cover Observer, Reference Frame, Context, Representation, Map, and Transition | reject for current architecture |
| Operator | Plate does not act; it is better understood as a produced or curated view | reject |

Several classifications may coexist, but only the metaphor, visual grammar,
and editorial-pattern roles are supported now.

## Potential contribution by layer

### Library

Plate already appears beside Part, Chapter, and Page. A later editorial guide
could distinguish pagination from explanatory function, but the frozen object
model requires no change.

### Geometry

Plate can help people understand why a projection, cross-section, declared
view, or map is not the represented field itself. It must not replace those
technical terms or weaken their evidence requirements.

### Living Concepts

A Plate could present one bounded occurrence, comparison, or development step
of a Concept. It must not become the Concept, its identity, or its provenance.

### Editorial Explanation Layer

Plate may eventually be a useful name for a human-facing rendition assembled
under an Answer Contract. The contract would continue to govern the question,
answer, evidence, boundaries, and explanation. The Plate would be one possible
presentation of that governed content.

### Orientation Kernel

No Kernel type, inference rule, relation, ranking signal, or response format is
needed. The current review yields no executable semantics.

## Vocabulary conflicts

The working hypothesis overlaps five controlled Operators:

- **Aperture** selects an opening or frame through which part of a field
  becomes perceivable;
- **Observer** establishes a situated act of selection and representation;
- **Boundary** distinguishes regions, states, or domains;
- **Projection** maps structure between frames or representations with
  preservation and loss;
- **Scale** establishes the level at which relations are represented.

Promoting Plate as an Operator would duplicate their combined work while
removing their distinctions. The safer interpretation is compositional:

```text
existing operations and context
        ↓
bounded editorial presentation
```

That composition is explanatory only. It creates no new Registry relation.

## Clarification test

Plate clarifies the architecture when all of the following are true:

1. a larger field, landscape, Work, or evidence body remains outside the view;
2. selection, perspective, scale, or projection is declared or inspectable;
3. the boundary of the presentation is meaningful;
4. the presentation supports comparison, reflection, explanation, or a next
   step;
5. the reader is not encouraged to mistake the representation for reality.

Plate merely renames existing material when it means only:

- page;
- image;
- panel;
- map;
- projection;
- cross-section;
- state representation;
- Answer Contract.

## Architectural risks

| Risk | Consequence | Guardrail |
|---|---|---|
| universalizing the metaphor | every artifact becomes a Plate and the term loses meaning | require boundedness, situatedness, and editorial function |
| duplicating Operators | Aperture, Observer, Projection, Boundary, and Scale become ambiguous | do not add Plate to the Operator Registry |
| reifying the representation | Plate is mistaken for an object or the field itself | preserve map/territory and evidence boundaries |
| collapsing technical models | graphs, cross-sections, frames, and reports are treated as one type | retain exact domain terms |
| premature canonicalization | a fresh phrase gains authority from attractive visuals | keep all findings in review status |
| visual-only evidence inflation | recurring layout is mistaken for conceptual recurrence | require text, metadata, or human-reviewed context |

## Impact decision

```yaml
architecture_change: none
registry_change: none
operator_change: none
concept_overlay_change: none
kernel_change: none
recommended_status: bounded_editorial_pattern_under_review
```

The present evidence warrants further research into Plate as a visual and
editorial grammar. It does not warrant a new architectural layer, identity, or
primitive.
