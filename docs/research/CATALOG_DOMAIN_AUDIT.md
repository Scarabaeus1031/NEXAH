# Catalog Domain Audit

## Result

The repository already contains stable authorities for several proposed
catalog domains. The sprint therefore defines coordination and boundaries, not
six replacement databases.

## Existing object inventory

| Existing area | Objects found | Catalog overlap | Decision |
|---|---|---|---|
| `LIBRARY/catalog/` | 61 source-keyed Works, descriptions, covers, 1,647 ordered Blocks, structural roles | Publication | Treat as first Publication Catalog implementation; retain path and Website Catalog label for compatibility. |
| `LIBRARY/registry/entities/` | Ten human-approved `NX-*` entities | Publication / identity | Remains canonical identity authority. Catalog references it; never allocates into it. |
| `LIBRARY/registry/concepts/` | Seventeen controlled `NX-OP-*` Operators | Operator | Remains canonical Operator authority. Do not duplicate in catalog records. |
| Proposal classification and overlays | 61 visible Work proposals and editorial classifications | Publication / review | Remains isolated; catalog inclusion does not promote a Proposal. |
| `EDITORIAL_OPERATING_SYSTEM/living_concepts/` | Concept reviews, accepted overlay v0.1, answer contracts | Concept / explanation | Reuse as reviewed Concept and contract evidence. Do not create a parallel accepted-concept registry. |
| Editorial Explanation Layer | reviewed question-answer-evidence-boundary contracts | Concept / Navigation | Accepted contracts can be evidence; audience rendition does not change meaning or boundaries. |
| Reader policies and journeys | UQ-01–UQ-06, sequences, paths, recommendations | Navigation | Existing implementation of curated audience-dependent navigation. |
| Series review | exact editorial series names, accepted/deferred/pending sequences | Publication / Navigation | Series navigation is editorial; series identity still requires separate approval. |
| `RESEARCH/` and validation artifacts | methods, experiments, claims, limitations, replay and evidence records | Laboratory | Distributed but authoritative within their owning research process. |
| `APPLICATIONS/orientation_translation/studies/` | bounded reviews, comparison protocols, neighborhoods, maps, dispositions | Laboratory / Atlas | Research artifacts and representational outputs; current directory ownership does not make them canonical architecture. |
| Kernel models | structured representations, Operators, reports, paths, provenance | Consumer layer | Kernel consumes reviewed records; it is not a Catalog authority. |
| Atlas publications and visual Works | atlases, maps, plates, diagrams | Publication / Atlas | Publication identity exists; object-level Atlas descriptions are not yet unified. |
| Are.na Connector and Editorial Writer | read-only source client; separately governed approved writer | Source / execution | Catalog review is read-only and must not import writer capability. |

## Gaps

1. No shared evidence contract previously covered all six catalog domains.
2. No unified page-level visual review schema preserved exact Block provenance,
   claim boundaries, and review state.
3. Atlas objects inside publications were not distinguished consistently from
   Atlas publications.
4. Laboratory activities and their published reports were sometimes adjacent
   in prose but lacked an explicit object boundary.
5. Existing Navigation is mature but distributed across Reader, sequence,
   shelf, and cleanup artifacts.

## Naming decision

**Publication Catalog** is the durable architectural name. **Website Catalog**
remains the name of the current implementation because it is already generated,
tested, and used for the public website. “Editorial Catalog” is too broad: it
would blur Publications with Navigation and human review decisions.

## Prototype location decision

Batch A belongs in `LIBRARY/catalog/review/orientation_foundations/` because it
reviews pages belonging to Publication Catalog records. It does not belong in
the Registry, Living Concepts, an ongoing Laboratory environment, or an
Orientation Translation study. Any later accepted Concept, Operator,
Laboratory, or Atlas object must be promoted through its own authority.

## Audit boundary

This audit describes repository objects and conventions. It does not validate
the scientific claims printed in the Works and does not change Architecture,
Registry, Proposals, Operators, Kernel behavior, or Are.na.

