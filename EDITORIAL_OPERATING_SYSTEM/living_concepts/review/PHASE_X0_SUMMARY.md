# Phase X0 Summary — Concept Census and Evidence Review

**Status:** completed review pass · non-canonical  
**Scope date:** 2026-07-16

## Inventory

| Measure | Count |
|---|---:|
| Candidate terms discovered | 47 |
| Candidates retained for review | 39 |
| Likely Keywords excluded | 8 |
| Existing Operator matches | 17 |
| Candidates with distinct NEXAH-specific definition evidence | 25 |
| Candidates with Discovery Provenance only | 4 |
| Candidates lacking adequate Definition Provenance | 8 |
| Candidates with unassessed Claim Provenance | 9 |
| Historical/speculative candidates | 6 |
| Ambiguous Work-title/Concept cases | 3 |

The inventory is scoped to approved repository text and stored Are.na Source
Snapshots. Raw term frequency was used only for discovery and contains lexical
false positives. No count establishes meaning or identity.

## Concept families

### Existing Operators with broader Concept questions

The 17 controlled Operators remain unchanged. Strong broader-Concept questions
exist for Aperture, Transition, Memory, Bridge, Field, Orientation, Relation,
Projection, Navigation, and JANUS. Other Operators require narrower or later
review. Existing `NX-OP-...` identity and vocabulary status remain
authoritative.

### Strong Research Concepts

Vessel, Transition Geometry, Phase, Mismatch, Coherence, Multi-Layer
Interaction, Topology, and Directional Coherence have identifiable Research
provenance. Their scientific support varies and remains scoped.

### Library-wide Concepts

Resonance, Meaning, Perspective, Agency, Morphology, Whole, Stack, and Living
Equation recur in Library material. Only some currently show enough distinct
meaning for deeper review. Work-title recurrence is not Concept identity.

### Historical/speculative Concepts

Risk Field, Resilience Architecture, Architecture DNA, Universal Law, Energy
Landscape, and Probability Field preserve Discovery Engine lineage. They do
not become current theory through inclusion in the Census.

### Likely Keywords

Water, nonlinear systems, geometry, visualization, learning, field study,
visual map, and books remain search or documentary terms in X0.

### Unresolved terms

Stack, Whole, Agency, Morphology, and Living Equation lack adequate independent
Concept definitions. Living Equation is retained as an intentional Work-title
identity test. Stack is not promoted to X1 because raw frequency is dominated
by generic and computational uses.

## Model findings

### Is the proposed Concept record sufficient?

Sufficient for X1 dossier review, but not for production. It needs a candidate
key, preferred name, Operator overlap, specificity rationale, scoped summary,
three provenance classes, maturity proposal, relations, open questions, and
warnings.

### Are Occurrence records practical?

Yes. The fixed sample produced 15 verified Occurrences across five structural
cases without modifying canonical data. Source, locator, role, verification,
assertion origin, and claim support are all necessary.

### Are the two relationship vocabularies sufficient?

They are sufficient for X1 testing if kept separate. Concept relations may
later require `part_of`, but X0 does not add it. Source roles such as `defines`
and `tests` must remain Occurrence roles.

### Are separate Definition records needed?

Probably yes. Aperture and JANUS show that a controlled Operator definition,
Research definition, and pedagogical formulation may be related without being
interchangeable. X1 should test versioned Definition candidates rather than a
single canonical string.

### Do Open Questions need first-class identity?

Not yet. Embedded, provenance-bound question records are sufficient for five
dossiers. Identity should be considered only if questions must be referenced,
closed, reopened, or shared across Concepts.

### Required X1/X2 architecture proposals

- decide whether broader Concepts live beside or above Operator records;
- define permanent identity policy only after dossier approval;
- formalize versioned Definitions and their supersession;
- approve a small Concept relation vocabulary;
- define a read-only Concept proposal overlay for Kernel evaluation;
- preserve canonical/proposal/inferred separation in every response.

None of these proposals amends Library Architecture v1.0 in X0.

## Kernel compatibility review

| Question | Current state | Available now | Smallest required addition | Human review and overclaim risk |
|---|---|---|---|---|
| What is JANUS? | partly answerable | NX-OP-0016 plus JANUS Research and Foundation records | Reviewed Concept Profile with scoped Definitions and Occurrences | Decide broader Concept boundary; avoid merging principle, Bridge, and scientific operator |
| Where does Stack first appear? | unsupported | Lexical search and Git history only | Retained Concept decision plus verified chronological Occurrences | First repository occurrence is not absolute origin; Stack may not be a Concept |
| How does Aperture develop across the Library? | partly answerable | Operator definition, Research framework, Library descriptions | Ordered, reviewed Occurrences and versioned Definitions | Avoid turning metaphorical Library language into scientific support |
| Which Concepts connect Agency and Orientation? | unsupported | Orientation Operator and an Agency Work title | Reviewed Agency Concept plus provenance-bearing relation proposals | Do not infer a relation from co-occurrence or title similarity |
| Show unresolved questions around Resonance. | partly answerable | Dispersed Library descriptions and Research caveats | Reviewed Resonance Profile with explicit Open Questions | Separate mathematical, physical, structural, and editorial uses |

The current Kernel remains unchanged. It can query Work–Operator usage, but not
non-Operator Concepts, Occurrences, Definitions, timelines, or Open Questions.

## Discovery Engine decision

The historical Discovery Engine contributes research lineage, reproducible
questions, selected observations, and corrected claim boundaries. Autonomous
theory canonicalization, universal-law generation, random equation candidates
as theory, and statistical association as explanation are rejected as
production principles.

## Risks

1. **Concept inflation** — recurring vocabulary can be mistaken for stable
   intellectual identity.
2. **Circular definitions** — Concepts may define one another without an
   external source or operational scope.
3. **Terminology drift** — the same term changes between Research, Library,
   Kernel, and historical experiments.
4. **Alias collapse** — related scopes may be merged because their words look
   similar.
5. **Scientific overclaim** — publication or textual occurrence may be treated
   as validation.
6. **Occurrence/evidence confusion** — a verified passage may be mislabeled as
   an observed outcome.
7. **Work-title/Concept confusion** — a title may acquire an unsupported second
   identity.
8. **Historical resurfacing** — deprecated claims can lose their corrective
   context.
9. **Excessive annotation** — completeness pressure can overwhelm editorial
   value.
10. **Unreviewed inferred relations** — co-occurrence and frequency can appear
    authoritative when rendered as a graph.

## Exactly five recommended X1 dossiers

1. **JANUS** — tests an existing Operator whose Foundation and Research history
   explicitly distinguishes principle, Bridge, and Directional Coherence
   analysis.
2. **Aperture** — tests an existing Operator with strong Research
   formalization and a separate pedagogical Library usage.
3. **Vessel** — replaces Stack as the non-Operator case because it has a clear
   Working Definition, explicit limitations, and multiple Research
   occurrences.
4. **Resonance** — tests a widely distributed term whose mathematical,
   structural, and editorial meanings must not be collapsed.
5. **Living Equation** — tests the negative boundary between a verified Work
   title and an as-yet unsupported independent Concept identity.

These recommendations do not allocate IDs or approve Concepts.

## Validation

- X0 proposal YAML parsed successfully.
- 39 retained candidates all contain Discovery Provenance.
- 17 existing Operator matches resolve to the unchanged Operator Registry.
- five sample candidates contain exactly 15 verified Occurrences.
- every sampled source path resolves in the repository.
- alias review declares `automatic_merge: false`.
- no `NX-C-...` identity was created.
- protected Registry, Operator, Kernel, Writer, and Architecture-v1.0 files
  retain the pre-X0 aggregate SHA-256 baseline
  `6fe9caea35e2a7b3ae1782696b06f42ed8a90e94c4bf66254f0da309d00194f7`.
- the complete repository suite passes: **262 tests passed**.

The test run reported dependency deprecation warnings and a sandbox warning
that Pytest could not update its local cache. No test failed.

## Governance conclusion

The Concept Census can locate terms, compare definitions, document appearances,
and expose uncertainty. It cannot determine canonical meaning. X0 demonstrates
that a provenance-bound dossier process is possible without Registry, Operator,
Kernel, Writer, Architecture, or Are.na mutation.

READY FOR FIVE CONCEPT DOSSIERS
