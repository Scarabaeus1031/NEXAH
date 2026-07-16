# Phase X0 — Concept Alias Review

**Status:** proposed · no automatic merges  
**Structured review:** [concept_alias_review.yaml](concept_alias_review.yaml)

## Decision rule

Lexical similarity does not establish shared identity. X0 distinguishes exact
synonyms, likely synonyms, contextual variants, related but distinct terms,
homonyms, and unclear cases.

## Findings

| Group | Important distinction | X0 decision |
|---|---|---|
| Field | Field · Field Model · Field Layer · physical field | Keep scoped; module and scientific homonyms are not aliases. |
| Aperture | Aperture · Aperture Geometry · Transition Aperture · Gate Geometry | Do not collapse Operator and research geometry. |
| JANUS | Janus Operator · Directional Geometry · Directional Coherence Operator · Janus Bridge | Preserve the explicit repository separation. |
| Stack | research stack · concept stack · layer stack · `numpy.stack` | Insufficient definition; raw frequency is misleading. |
| Living Equation | proposed Concept phrase · Work title | Preserve separate possible identities. |
| Orientation | Operator · Orientation Layer · orientation field · reader orientation | Treat as scoped variants pending dossier review. |
| Resonance | broad term · Prime Modular Resonance · resonance locking · coherence | Related uses are not currently synonyms. |
| Transition | operation · event · geometry · corridor · phase transition | Preserve event, operation, and geometry distinctions. |

## Merge warnings

1. `Field Layer` is a repository architecture label, not automatically a
   synonym for the Field Concept.
2. `Coherence` and `Resonance` overlap rhetorically in some Library sources but
   describe different research quantities and must not be merged.
3. `JANUS` has at least three explicitly separated scopes in the Foundation
   record: complementary-perspective principle, representation Bridge, and
   Directional Coherence analysis.
4. `THE LIVING EQUATION` is currently evidenced as a Work. The title does not
   establish a Concept.
5. `Stack` fails the human-meaning test in X0; most reviewed uses are generic or
   computational.

No alias decision in this review changes the Operator Registry.
