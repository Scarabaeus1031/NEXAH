# NEXAH v0.7 Validation Strategy

## Purpose

Validation is claim-specific. A successful execution is evidence that software
runs on an input; it is not by itself evidence that inferred regimes are true,
that a mechanism is causal, or that an intervention will work in a real system.

## Validation levels

### 1. Software characterization

Questions:

- Does the implementation produce stable, documented outputs?
- Are transition rows normalized?
- Are indices, seeds, and failure modes understood?
- Can a clean environment reproduce the run?

Evidence:

- automated characterization tests
- pinned package and environment versions
- deterministic fixtures where the algorithm is deterministic
- recorded stochastic seeds and call conditions where it is not

Current status: covered for the bounded behaviors listed in
**[BASELINE_STATUS.md](BASELINE_STATUS.md)**. Coverage is not yet comprehensive
for invalid inputs, numerical edge cases, or all stochastic branches.

### 2. Representation validation

Questions:

- Does the window embedding preserve the information relevant to the task?
- Are clusters stable under seeds, parameters, noise, and resampling?
- Does overlapping-window dependence distort persistence estimates?

Evidence required:

- sensitivity analysis
- alternative embeddings and clustering baselines
- stability metrics with uncertainty
- explicit raw-to-embedded index alignment

Current status: raw-to-embedded alignment is characterized; bounded proxy,
memory, IEEE attribution, continuation, and resolution-sensitivity experiments
exist. General representation stability across domains remains open.

### 3. Task validation

Questions:

- Do reported regimes or transitions match declared ground truth?
- Does navigation outperform simple baselines under a defined objective?
- Are warnings earlier and more accurate than comparison methods?

Evidence required:

- labeled synthetic benchmarks and/or defensible domain labels
- predefined metrics
- baseline comparisons and ablations
- held-out evaluation and failure cases

Current status: bounded canonical validations now cover the Lorenz Demonstrator,
Memory V1/V2, IEEE Orientation V1, and IEEE Scaling Pattern V1/V2. These remain
claim-specific; no package-wide general validation claim is made.

### 4. Mechanism and intervention validation

Questions:

- Is a proposed mechanism causally identified?
- Does an intervention change the physical or simulated system as predicted?
- Does the result generalize across conditions and systems?

Evidence required:

- controlled interventions
- causal alternatives and confound analysis
- repeated and cross-system experiments
- domain-appropriate safety and uncertainty treatment

Current status: research hypothesis, not established by v0.7.

## Release gate for the frozen baseline

v0.7 is considered characterized when:

- package, module, and CLI version labels agree
- the characterization suite passes in the declared environment
- known legacy semantics are documented
- documentation distinguishes execution, task validation, and causal evidence
- no production, universal, or causal capability is implied

## Next validation step

The original Orientation Layer Demonstrator gate and the Phase III power-system
gate are complete. The next validation should combine the V3 directed-graph
source with a graph-native representation backend, first on explicit fixtures
and then on independently sourced topology or event data. Authored supply-chain
regimes and actions must not be used as ground truth without separate evidence.
