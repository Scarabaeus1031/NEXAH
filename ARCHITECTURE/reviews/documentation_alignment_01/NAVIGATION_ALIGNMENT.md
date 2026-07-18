# Navigation Alignment

## Discoverability questions

| Question | Current result | Evidence | Minimal alignment |
|---|---|---|---|
| Can a new visitor discover Orientation Translation? | No, not through canonical front-door links | absent from Root entry table, Repository Map Applications section, and Applications README | add compact links at Root, Repository Map, and Applications |
| Can a researcher discover methodological work? | Only if they already know the path | Research path ends inside `RESEARCH/`; method studies live under Applications | add one cross-boundary related-program pointer |
| Can a developer avoid entering research accidentally? | Yes | Root and Repository Map separate developer, implementation, applications, and research paths | preserve current paths |
| Can readers distinguish Research and Applications? | Generally yes | both READMEs define evidence versus concrete-system work | clarify that Applications may contain applied methodological research |
| Can readers distinguish Architecture and Method? | Mostly, but one sequence risks ambiguity | Architecture presents a shared orientation movement | qualify it as architectural vocabulary, not a canonical method definition |
| Can readers distinguish Orientation Translation and OLS? | Not from navigation because Translation is absent | OLS README boundaries are correct; no visible Translation description exists | program description must state OLS-guided but non-normative and non-conformant unless demonstrated |
| Can readers distinguish Library and Orientation Translation? | Yes by existing content | no cross-link currently implies ownership | preserve separation |
| Can readers distinguish Editorial OS and Orientation Translation? | Conceptually less clear due to shared Reader/Explain language | responsibilities are separately documented | add no link until a formal relation exists |

## Missing paths

### Methodological researcher

Current:

```text
Root → Research → dynamical-system research
```

Missing bounded alternative:

```text
Root → Applications → Orientation Translation
     → Pilots · Studies · Comparisons · Reviews
```

### Application evaluator

Current canonical path privileges Power Systems. It needs a second, clearly different branch:

```text
Applications
├── system/domain application → Network or Power Systems
└── public-knowledge orientation program → Orientation Translation
```

This is not a redesign; both branches already exist physically.

## Broken versus missing navigation

No reviewed link was identified as technically broken. The problem is semantic absence: existing navigation works, but cannot lead to a substantial existing program.

## Backward compatibility

All proposed additions retain current reader paths. No heading, URL, directory, or authority label needs removal or replacement.
