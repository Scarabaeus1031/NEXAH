# Repository Direction

## Decision

Do not add an “Orientation Methodology” subsystem, layer, OLS profile, operator,
runtime, or authority.

Current evidence justifies making the methodological interpretation more
explicit in future synthesis and navigation. It does not justify redesign.

## Minimal practical consequences

### Repository structure

Keep the six established responsibility areas and existing program placement.
A methodology label should be a cross-reference describing shared practice,
not a seventh owner and not a directory into which programs are moved.

### Architecture

Architecture should continue to own responsibility boundaries. At most, a
future informative paragraph may state that the recurring boundaries support
an emerging evidence-bound orientation methodology. It should link to evidence
and preserve the statement that repository-level movement is not a mandatory
workflow.

No architecture change is required by this review.

### Evidence Atlas

The proposed Evidence Atlas remains non-authoritative navigation. It can make
method evidence discoverable by linking:

- claims to original sources;
- procedures to results and limitations;
- positive, negative, incomplete, and blocked evidence;
- exact, empirical, architectural, application, and editorial statuses.

It must not assign methodological validity merely because an artifact is
registered.

### OLS

No OLS change follows.

OLS already defines canonical semantics, preservation obligations,
non-implications, and conformance boundaries. “Orientation Methodology” should
use those meanings where applicable, but must not be presented as an OLS
extension or as automatically conformant. OLS conformance also must not be
treated as scientific validation of the methodology.

### Research

Research programs should continue to state their own:

- object and question;
- representation and applicable reference conditions;
- method, baselines, and tests;
- evidence and provenance;
- uncertainty and limitations;
- supported and prohibited conclusions.

Cross-program comparison should test whether the shared practice is useful. It
should not presume that the scientific mechanisms are shared.

### Applications

Applications remain the strongest place to test transfer. A method claim should
be widened only when an unchanged, declared practice transfers to a genuinely
different bounded case and preserves the same epistemic boundaries.

Application success remains local to the application evidence.

### Library and public explanation

Library and Editorial OS should explain the distinctions among representation,
evidence, validation, publication, interpretation, and authority. They should
not convert the emerging methodology into a project worldview or claim
scientific priority.

### Implementation

No framework refactor is justified. Existing typed records, immutable evidence,
failure-aware operators, and outcome firewalls are useful realizations, but no
one implementation should become the definition of the methodology.

## What should become more explicit

1. The phrase **emerging evidence-bound orientation methodology** is
   informative and provisional.
2. Its smallest scope is epistemic and procedural discipline, not a universal
   sequence or scientific mechanism.
3. OLS semantics, scientific methods, implementation behavior, evidence
   assessment, publication, and human authority remain distinct.
4. Domain results remain owned by their programs.
5. The method's novelty and effectiveness are open research questions.
6. Historical artifacts may illustrate the development but cannot override
   maintained limitations.

## Research needed before stronger adoption

A stronger methodology claim would require evidence not currently present:

- an explicit, source-derived method statement reviewed against maintained
  practice;
- independent application by researchers who did not create the source
  corpus;
- comparison with credible alternative research and reporting practices;
- defined measures of traceability, error prevention, understanding, or
  decision support;
- documented failures and costs of applying the practice;
- cross-domain transfer without changing the claimed core;
- evidence that the methodology adds value beyond ordinary good scientific and
  software-engineering practice.

These are research questions, not a roadmap mandated by this review.

## What should not change

- the six responsibility boundaries;
- OLS semantic ownership and release governance;
- frozen validation artifacts and POAs;
- original scientific evidence and limitations;
- the separation of orientation from recommendation, authority, execution, and
  outcome;
- human responsibility for interpretation and consequential decisions;
- the ability of exploratory work to remain explicitly exploratory.

## Recommendation

Use “Orientation Methodology” cautiously in informative review and onboarding
material, always with the qualifiers **emerging**, **evidence-bound**, and
**not a common mechanism**. Do not freeze, standardize, or architect it until
independent and comparative evidence exists.
