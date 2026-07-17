# README Hierarchy

## Repository root README

Purpose: explain NEXAH in one paragraph and present five primary paths.

Required first-level links:

1. Research
2. Orientation Language
3. Library
4. Applications
5. Implementations

The root README should not lead with phase history, corpus size, or internal architecture.

## Domain READMEs

Every top-level domain README contains:

- purpose;
- authority and responsibility;
- what belongs there;
- what does not;
- relationship to the other domains;
- primary audience paths;
- current status;
- next navigation step.

## Orientation Language hierarchy

| README | Audience | Required content |
| --- | --- | --- |
| `ORIENTATION_LANGUAGE/README.md` | Everyone | Purpose, boundaries, five paths, authority, current release |
| `SPECIFICATION/README.md` | Specification readers | Part order, status, manifest, normative/informative distinction |
| `SPECIFICATION/OLS-x/README.md` | Part readers | Part responsibility, dependencies, canonical file, annexes, next part |
| `COMPANION/README.md` | General readers and implementers | Informative status, compatible release, contents |
| `REGISTRIES/README.md` | Maintainers and tools | Registry ownership, generated/source status, update rules |
| `EXAMPLES/README.md` | Users and educators | Informative status, controlling OLS references, validation status |
| `VISUALS/README.md` | General visitors | Three canonical diagram roles and archive boundary |
| `CHANGELOG/README.md` | Maintainers | Releases, migration map, deprecation, correction history |
| `HISTORY/README.md` | Researchers and historians | Phase chronology, status boundary, link to current publication |
| `ARCHITECTURE_DECISIONS/README.md` | Maintainers | ADR scope, status, relation to OLS-6 governance |

## Part README template

```markdown
# OLS-x

Status: [normative/informative and release]
Document ID: OLS-x
Suite version: x.y.z
Canonical file: [link]
Dependencies: [Document IDs]

## Responsibility
## Intended readers
## Contents and annexes
## Authority boundary
## Previous and next reading step
## Release and checksum
```

The template is navigation metadata. It shall not paraphrase normative definitions when a stable link is sufficient.

