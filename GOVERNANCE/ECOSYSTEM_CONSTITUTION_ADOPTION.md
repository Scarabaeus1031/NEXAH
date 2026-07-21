# Constitution Adoption Report

- Review: Governance 03 — Constitution Adoption
- Constitutional baseline: NEXAH Ecosystem Constitution v1.0
- Canonical language: German
- Scope: documentation, terminology and governance references only
- Architecture changes: none
- Implementation changes: none

## Adoption decision

The NEXAH Ecosystem Constitution v1.0 is ready as the official constitutional
baseline. It is not a release candidate: its Houses, authority model, ownership
rules, boundaries, evolution rules and governance hierarchy have already been
reviewed and adopted. Remaining visual-production and repository-publication
work is derived presentation and does not block constitutional validity.

## Repository consistency review

| Responsibility area | Constitutional reading | Review result | Documentation alignment |
|---|---|---|---|
| NEXAH | The NEXAH Framework defines; OLS specifies; the Kernel executes; Research explores; Library remembers. | Subsystem architecture remains compatible. The root README still named the earlier Constitution Candidate as the primary constitutional entry. | Point the front door and Architecture index to Constitution v1.0 and identify the earlier candidate as historical review evidence. |
| ORION | ORION navigates; LYRA translates at the ORION boundary. | Runtime and architecture boundaries remain compatible. The README mixed ORION repository status with Experience and LUCY project phases and assumed Library was necessarily a separate repository. | Reference the Constitution, describe Library as a House currently canonical in `NEXAH/LIBRARY`, and keep Experience status outside the ORION status summary. |
| Experience | Experience presents; Library remembers; Living Atlas relates; Human interprets and decides. | Implementation boundaries remain compatible. Some wording used “Library” both for canonical publication authority and for the Experience presentation room. | Name the Experience Library room as a presentation and retain publication identity with the NEXAH Library Registry. |

No reviewed repository claims authority that requires an architectural change.
The deviations are terminology and reference-placement issues.

## Terminology review

The following constitutional terms are adopted where they clarify authority:

- **House** for a durable responsibility, independent of repository or
  technology;
- **authority** for the right and duty to define canonical artifacts;
- **canonical** for the controlled source;
- **boundary** for the end of one authority and beginning of another;
- **reference** for a non-authoritative link to a canonical source;
- **derived** for generated reports, projections, renderings and snapshots;
- **presentation** for Experience-owned form without semantic ownership;
- **interpretation, Reflection and decision** for Human authority.

Terminology is not forced into implementation descriptions when established
technical terms are more precise. Repository, component, package, contract and
runtime remain valid implementation vocabulary; they are not constitutional
Houses by implication.

## Documentation hierarchy review

The adopted hierarchy is:

```text
Constitution
    ↓
Governance
    ↓
Architecture
    ↓
Repository Documentation
    ↓
Implementation
    ↓
Generated Artifacts
```

Observed deviations:

1. The earlier non-canonical candidate was presented from the NEXAH front door
   as the only constitutional entry.
2. ORION's README included Experience-phase narrative in its repository-status
   section.
3. Experience documentation retained a historical statement that the ORION
   workshop was the canonical Experience source after Experience had acquired
   its own maintained documentation.
4. The distinction between canonical Library records and their Experience
   presentation was not always explicit.

The adoption changes only references and descriptions. Historical evidence,
architecture records and implementation remain unchanged.

## Governance index

The canonical entry is [`README.md`](README.md). It records where the
Constitution lives, where Governance operates, where Architecture begins, where
repository documentation describes current state, and where Implementation and
derived artifacts begin.

## Diagram strategy

Three diagrams in the Constitution form the canonical semantic set:

1. **Canonical Constitutional Diagram** — institutional blueprint of all
   Houses and their relationships.
2. **Simplified Ecosystem Diagram** — one-minute introduction containing only
   the Houses.
3. **Governance Hierarchy Diagram** — authority order from Constitution to
   generated artifacts.

The Mermaid definitions remain canonical diagram sources for Constitution v1.0.
Permanent NEXAH Plates may later be created as derived visual companions if
they preserve the same Houses, verbs, edges and hierarchy exactly. Such Plates
must have editable vector sources, generated documentation images and an
explicit reference to the governing diagram. They may not add concepts or
change authority.

## Baseline recommendation

**Adopt: Constitution v1.0.**

`v1.0-RC1` would imply that constitutional content or adoption authority
remains unresolved. That is no longer the case. Outstanding work concerns
publication, cross-references and future derived Plates, not the Constitution's
substance.

Any later change to its Axiom, Houses, authority, principles, ownership rules,
boundaries, evolution rules or governance hierarchy requires an explicit
constitutional amendment and a new version.

## Verification scope

This adoption review changes documentation and governance references only. It
does not change code, architecture, runtime behavior, repository structure,
deployment, remotes, releases or ownership settings.
