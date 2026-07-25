# Proposed NEXAH Evidence Atlas Structure

Status: design proposal only; no atlas implemented

## Proposed location and name

```text
docs/
└── evidence/
    └── README.md
```

Recommended name: **NEXAH Evidence Atlas**.

The location is cross-system documentation, not Research, Architecture,
Library, or OLS authority. The first implementation should contain one page
only.

## Entry layout

Group entries by evidence role, not repository ownership:

1. Exact constructions
2. Architectural validations
3. Experimental findings
4. Negative and inconclusive results
5. Open hypotheses and blocked chains
6. Application results
7. Representations and historical explorations

Each row should contain:

```text
ID | claim | status | scope | authoritative source | reproducibility | limits
```

The status vocabulary is defined in
[Discovery Taxonomy](DISCOVERY_TAXONOMY.md). Negative results must appear in the
main table and in navigation filters; they must not be moved to an appendix.

## Claim-page template for later use

Do not create claim pages initially. If the single page becomes unmanageable,
use:

```markdown
# E-000 — Conservative title

Claim:
Status:
Kind:
Scope:
Evidence type:
Authoritative source:
Supporting sources:
Limiting or contradicting sources:
Reproducibility:
Dependencies:
Does not imply:
Open questions:
Last source review:
```

No result table, artifact, or source prose should be copied into the page.

## Relationships

- **POA:** entries point to frozen POA specs, runs, and freeze reports when those
  sources become repository-addressable. Missing chains remain `BLOCKED`.
- **OLS:** entries point to releases and reviews; the atlas never defines
  semantics or conformance.
- **Research:** hypotheses and historical work stay in Research; the atlas marks
  their status and links to them.
- **Validation:** frozen bundles remain the primary empirical authority.
- **Findings:** thematic narratives remain useful; atlas entries point to later
  limiting evidence when necessary.
- **Applications:** domain protocols retain domain authority and prohibited
  implications.
- **Library:** Library may link to atlas entries for evidence orientation, but
  the atlas neither catalogs Works nor becomes editorial authority.
- **Visuals:** an entry links the generating record and marks the figure as a
  representation.

## Machine-readable metadata

Do not add JSON in the first iteration. After one maintenance cycle, a
`claims.json` file may mirror the human table if:

1. validation checks every source path;
2. enum values match the controlled taxonomy;
3. Markdown is generated from, or checked against, one record source;
4. metadata never copies result payloads;
5. the source document remains authoritative.

## External reader path

```text
Root README
  → Evidence Atlas
      → bounded claim and status
          → authoritative source
              → specification / evidence / review
```

Suggested links after implementation: root README, Research Index, Validation
portal, Applications index, and `docs/README.md`.

## Proposed sample entries

These are catalog examples, not new evidence.

| ID | Proposed entry | Status | Authority | Boundary |
|---|---|---|---|---|
| E-001 | OLS 1.0.0 is the first complete canonical release | `ARCHITECTURALLY_VALIDATED` | OLS Publication Summary | Not general implementation conformance |
| E-012 | Fixed `(7*r7+8) mod 17` bridge did not beat majority baseline | `NOT_SUPPORTED` | Prime comparison RESULTS | Does not reject every relation between spaces |
| E-015 | `Z/42Z ↔ Z/6Z × Z/7Z` is exact and invertible | `MATHEMATICALLY_EXACT` | Wheel/product SPEC | Does not imply dynamic independence |
| E-018 | 31/32/33 did not meet the predefined top-5% anomaly rule | `NOT_SUPPORTED` | Wheel/product RESULTS | Does not establish irrelevance under other questions |
| E-022 | Frozen IEEE method transferred to IEEE14 without evaluation retuning | `EXPERIMENTALLY_SUPPORTED` | IEEE manifest and validation | Benchmark result, not operational-grid validity |

## Explicit exclusions

The atlas must not contain:

- a runtime, API, registry service, processor abstraction, or graph database;
- new OLS vocabulary, operators, or semantics;
- copied raw data, plots, result tables, or checksum payloads;
- rankings such as “most important discovery”;
- claims derived from visual resemblance;
- conversational materials without repository provenance;
- universal, causal, physical, or operational wording absent from the source;
- automatic promotion from “experiment completed” to “finding supported”.

## Minimal implementation sequence

1. Restore or locate POA, NTO, and DERIS/HYDRA primary sources, or explicitly
   accept that they remain blocked.
2. Create the single `docs/evidence/README.md`.
3. Transfer the 28 reviewed entries without expanding their wording.
4. Add four or five navigation links.
5. Run link, frozen-boundary, and documentation checks.
6. Review maintenance cost before adding files or metadata.
