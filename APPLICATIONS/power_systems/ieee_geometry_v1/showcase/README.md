# NEXAH IEEE Geometry V1 — Public Showcase

This showcase provides three entry depths into one canonical Phase V result.
All numbers and figures derive from the committed IEEE-9 development and
IEEE-14 evaluation artifacts. Choose the depth that matches your available
time:

1. **[90-second map](90_SECOND_MAP.md)** — purpose, pipeline, result, boundary.
2. **[10-minute runnable case](QUICKSTART_10_MINUTES.md)** — reproduce the full
   frozen gate with one command.
3. **[Research path](RESEARCH_PATH.md)** — inspect contracts, methods, evidence,
   failures, claims, and open questions.

## Canonical figures

| View | What it shows |
|---|---|
| [Physical campaign](figures/01-physical-campaign.png) | voltage and line-loading summaries over the declared parameter |
| [Path geometry](figures/02-path-geometry.png) | local drift and accumulated path in the frozen standardized representation |
| [Turning geometry](figures/03-turning-geometry.png) | direction change and local discrete curvature |
| [Evidence boundary](figures/04-evidence-boundary.png) | available and failed frames, plus the boundary of interpretation |

Regenerate all four from the repository root:

```bash
python APPLICATIONS/power_systems/ieee_geometry_v1/showcase/generate_figures.py
```

These are scientific communication figures, not additional evidence. The
canonical JSON records govern every value and interpretation.
