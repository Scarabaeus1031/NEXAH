# Planetary Orientation Whiteboard Proposal

This is an editorial architecture for a future visual. It is not artwork and
does not authorize a canonical map.

## Layout

Use five vertically stacked, independently labelled bands rather than one
left-to-right causal pipeline.

```text
A  Comparison context and reference planes
B  World cards: measured atmospheric state
C  Species occurrence matrix
D  Observed process matrix
E  Comparative paths, contrasts and open questions
```

The viewer should be able to enter from a world, a molecule, or a process
without implying that one layer causes the next.

## Sections

### A — Comparison contract

Always show:

- mixing-ratio basis;
- altitude or pressure level;
- time/variability qualifier;
- surface versus atmosphere versus bulk interior;
- evidence status.

### B — World cards

Group by atmospheric state, not by a single planet sequence:

1. surface-bound exospheres — Mercury, Moon;
2. rocky worlds with collisional atmospheres — Venus, Earth, Mars;
3. dense moon atmosphere — Titan;
4. gas giants — Jupiter, Saturn;
5. ice giants — Uranus, Neptune.

Every card contains only title, major mixture, declared pressure/reference,
temperature reference, major clouds, variability and one evidence link.

### C — Species occurrence matrix

Rows are species; columns are worlds. Cell symbols distinguish:

- dominant;
- major;
- minor;
- trace;
- cloud/condensate only;
- detected but abundance uncertain;
- not established.

Do not use arrows from elements to worlds. Elements may appear in a separate
legend explaining molecular composition.

### D — Process matrix

Rows: greenhouse behavior, condensation/weather, photochemistry, atmospheric
escape, surface exchange, volcanism/cryovolcanism, magnetosphere interaction,
and internally driven circulation.

Each cell receives one status:

- observed;
- mechanism-supported;
- unresolved;
- not applicable;
- insufficient evidence.

### E — Orientation paths

Offer five curated paths:

- **Same molecule, different world:** CO₂ → Venus ↔ Mars;
- **Same background gas, different chemistry:** N₂ → Earth ↔ Titan;
- **Giant envelopes:** Jupiter ↔ Saturn ↔ Uranus ↔ Neptune;
- **Sparse atmospheres:** Mercury ↔ Moon;
- **Condensable landscapes:** H₂O/Earth ↔ CH₄/Titan, explicitly marked as a
  process analogy rather than chemical identity.

## Relationship grammar

| Line | Meaning |
|---|---|
| Solid blue | Direct observation / measured occurrence |
| Solid green | Well-established physical relation |
| Dashed amber | Model-supported interpretation |
| Dotted violet | Editorial comparison path |
| Gray break | Comparison prohibited or reference mismatch |
| Open circle | Unknown / unresolved |

No line may exist without a legend class and a source anchor.

## Colour logic

Colour should encode evidence class, not planet identity or habitability.
Planet images may retain natural colour, while data cells use a colour-blind
safe status palette plus shape or line style.

## Required corrections to the supplied sketch

1. Remove the cosmic-abundance donut from the atmospheric data plane or place
   it in a clearly detached context panel.
2. Replace “Molecules” with “Atmospheric atoms and molecules” so He is valid.
3. Remove unexplained numerals beside species.
4. Replace element-to-atmosphere causal wires with an occurrence matrix.
5. Correct Titan to a sourced profile and display vertical variability.
6. Give Ar a visible role for Earth and Mars.
7. Replace Moon “No Atmosphere” with “Variable surface-bound exosphere.”
8. Remove “surface pressure” from giant-planet cards; declare a pressure level.
9. Separate observed properties from habitability interpretation.
10. Replace the bottom causal slogan with:

> Composition, pressure, energy, gravity, history and exchange interact.
> Compare before interpreting.

## Reader test for a future visual

A future whiteboard should be rejected if a reader cannot answer:

- Which values are measured at compatible reference levels?
- Which connection is observed and which is editorial?
- Why do Venus and Mars remain different despite similar CO₂ fractions?
- Why is the Moon not simply “airless”?
- Which comparison is blocked because the objects are not commensurate?
