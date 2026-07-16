# Cross-Repository Provenance Review

**Phase:** X0.5

**Status:** completed review pass · non-canonical

**Scope date:** 2026-07-16

## Decision

The two adjacent repositories are useful evidence sources, but they do not
enter the completed X0 Census as additional authority. X0.5 adds a historical
provenance overlay before the five X1 dossiers.

> Historical sources can show where a formulation appeared and how it changed.
> They cannot make that formulation canonical or scientifically supported.

No Concept identity, Registry record, Operator assignment, relationship, or
Kernel behavior is created by this review.

## Frozen source boundary

| Source | Pinned state | Editorial role | Authority |
|---|---|---|---|
| `NEXAH-CODEX` | `cc1962237940867becb7beb7d4d9fb9f6b613253` | frozen historical archive; terminology and definition lineage | no present scientific or canonical authority |
| `Scarabaeus1033-System-v1.0` | `c5d030482a13082fededc42a60e04de2c503a111` · tag `v1.0` | early experimental motivation and project lineage | no present scientific or canonical authority |

`NEXAH-CODEX` was already dirty and strongly divergent when reviewed. It was
not cleaned, pulled, checked out, or modified. `Scarabaeus1033-System-v1.0`
contained only an untracked `.DS_Store`. All cited passages refer to tracked
content at the pinned commits.

## How evidence was handled

Twelve X0 terms were searched case-insensitively in tracked Markdown, YAML, and
text. Raw results were used only to locate candidate passages. The search found
very broad vocabularies in `NEXAH-CODEX`—for example 5,826 matched lines for
Resonance, 5,769 for Field, 1,361 for Fold, and 529 for Observer. These counts
show lexical saturation, not Concept stability.

The accompanying YAML retains a smaller curated set of passages. Each passage
separates:

- repository and pinned commit;
- source and locator;
- occurrence role;
- assertion origin;
- support available in the reviewed source;
- independence from other formulations;
- effect on the future dossier.

No duplicated or derivative wording was counted as independent confirmation.

## Source assessment

### NEXAH-CODEX

The root README explicitly freezes the repository as an exploratory structural
archive. That status is the controlling interpretation for X0.5.

The archive is highly valuable for intellectual genealogy. It contains early
JANUS visual and gatekeeper formulations, Aperture as lunar valve language,
several Observer systems, a large transition vocabulary, and many Field,
Bridge, Fold, Scale, Stack, and Resonance constructions.

It also contains incompatible levels of assertion. The glossary offers useful
historical definitions, while other documents state broad cross-domain or
physical claims without support in the reviewed passage. X0.5 preserves both:
the first as definition history and the second as claim-boundary evidence.
Neither becomes current theory.

### Scarabaeus1033-System-v1.0

This repository is narrower. Its manifest establishes Resonance as an early
organizing theme spanning geometry, temperature, materials, time, and symbolic
logic. The Lunar-Kern module describes possible analog investigations using
pendulums, water vapor, aluminum, and temperature.

The reviewed files do not contain measurements, a protocol sufficient for
reproduction, or validation results. The repository therefore contributes
experimental motivation and lineage, not empirical confirmation.

## Principal findings

1. **JANUS has genuine prehistory.** The archive contains a mythic gatekeeper,
   polarity-transfer usage, and a quaternionic visual series. These are related
   but not interchangeable with the current controlled JANUS Operator.
2. **Aperture has an older speculative physical usage.** This strengthens the
   need for versioned, scoped definitions; it does not support lunar-neutrino
   claims.
3. **Vessel does not gain an independent historical definition.** Older uses
   are metaphorical or ordinary container language. The X1 dossier must remain
   anchored in current Research.
4. **Resonance is the clearest semantic-overload case.** Historical glossary,
   symbolic, mathematical, physical, pedagogical, and editorial meanings must
   be separated rather than collapsed.
5. **Living Equation remains a boundary test.** Neither external repository
   contains the exact phrase in tracked text at the pinned commits. This is
   useful negative evidence, not proof of absolute origin.
6. **Stack remains excluded from X1.** Historical matches are mostly compounds,
   layout descriptions, or technical uses and do not supply the missing
   independent definition.
7. **Observer, Transition, Field, Bridge, Fold, and Scale have deep lineage but
   excessive breadth.** They require scoped future reviews rather than immediate
   Concept identities.

## Governance outcome

X0.5 changes the evidence available to X1, not the five-dossier decision:

1. JANUS
2. Aperture
3. Vessel
4. Resonance
5. Living Equation

The order remains useful because it tests five different boundaries: Operator
overlap, definition drift, non-Operator Research identity, semantic overload,
and Work-title/Concept separation.

The X1 dossiers must cite historical material as `historical` and must show
current and historical definitions separately. No dossier may inherit a claim
merely because it occurred earlier or often.

## Deliverables

- [Machine-readable provenance review](cross_repository_occurrences.yaml)
- [Concept lineage deltas](CONCEPT_LINEAGE_DELTAS.md)

## Readiness

The cross-repository evidence boundary is explicit, reproducible at pinned
commits, and compatible with the X0 Outcome Firewall.

**READY FOR FIVE X1 CONCEPT DOSSIERS**
