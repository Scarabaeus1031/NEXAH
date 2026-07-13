# IEEE Geometry Showcase Plan

Status: Phase V public-use plan; implementation pending

## Invitation

The IEEE line is the strongest place to show what NEXAH currently means in
practice: one familiar engineering benchmark, viewed as an ordered family of
physical states, with its evidence and limits visible.

The showcase should spark three reactions:

1. **I understand the question.**
2. **I can run and inspect the case.**
3. **I can see where my expertise or data could improve it.**

It should not require readers to accept the broader NEXAH vocabulary before
they can evaluate the result.

## The central question

> As an IEEE benchmark is continued across a declared load campaign, do its
> physical state snapshots form reproducible geometric changes that help us
> orient around numerical boundaries without overstating stability or control?

## One case, three entry depths

### 1. Ninety-second overview

For visitors and collaborators:

- one system diagram
- one ordered campaign ribbon
- one geometry-change plot
- one boundary result
- one evidence card
- one sentence each for supported and unsupported claims

No installation is required to understand this page.

### 2. Ten-minute runnable case

For researchers, engineers, and developers:

```text
install
→ run one frozen command
→ inspect JSON and Markdown report
→ inspect four generated figures
→ compare output checksums
```

Target artifacts:

1. network and campaign definition
2. parameterized state-family view
3. drift and projection comparison
4. numerical-boundary view
5. evidence and claim-boundary report

### 3. Research path

For domain specialists:

- exact variables and units
- adapter and solver configuration
- geometry definitions
- development/evaluation protocol
- negative and indeterminate cases
- comparisons with established power-system measures
- open hypotheses and contribution points

## Scientific visual translation

The historical Tube Cross-Section visual is retained as a concept source, with
these Phase V translations:

| Historical visual language | Phase V technical language |
|---|---|
| Field | sampled physical state family |
| Tube | load-parameterized campaign |
| Cross-section | declared projection of one snapshot |
| Movement through field | ordered load continuation |
| Languages | alternative physical or geometric views |
| Atlas | collection of versioned campaign maps |
| Gate | sampled numerical or structural boundary |
| Control layer | future work outside the Phase V showcase |

Prime lines, fixed angular apertures, universal return, and direct control stay
experimental unless separately formalized and tested.

## Showcase outputs

The canonical run should generate:

```text
outputs/phase_v_ieee_geometry/
├── case_manifest.json
├── orientation_report.json
├── orientation_report.md
├── geometry_summary.json
├── figures/
│   ├── 01-network-and-campaign.png
│   ├── 02-parameterized-state-family.png
│   ├── 03-local-drift-and-projections.png
│   └── 04-boundary-and-evidence.png
└── checksums.sha256
```

Every figure must be derivable from the same canonical result. Hand-authored
concept art may accompany it, but must be labeled conceptual.

## User paths

| User | Start here | Invitation |
|---|---|---|
| Curious visitor | 90-second overview | Understand the question and boundary |
| Power engineer | physical variables and comparison | Challenge the interpretation |
| Complex-systems researcher | state family and geometry | Compare methods and hypotheses |
| Developer | ten-minute case | Reproduce, test, and extend |
| Data holder | observed-evidence bridge | Contribute a properly scoped case |
| Designer or educator | generated figures and case card | Improve communication without changing claims |

## Interest without overclaiming

The most compelling message is not that NEXAH has solved grid stability. It is:

> We have a reproducible way to inspect how a benchmark system's representation
> changes across an ordered campaign, to compare perspectives, and to show
> exactly where the evidence ends.

That leaves meaningful work for others: alternative projections, established
baselines, new benchmark cases, observed measurements, uncertainty models, and
better explanations.

## Release gate

The showcase is public-ready when:

- a fresh clone reproduces it through one documented command
- the manifest and outputs pass the observed-evidence testkit
- all charts derive from canonical machine-readable data
- failure and indeterminate states render clearly
- a domain specialist can locate variables, units, and assumptions
- the README distinguishes benchmark computation from observation
- no scenario or solver result updates episodic memory
- the contribution path names concrete open questions
