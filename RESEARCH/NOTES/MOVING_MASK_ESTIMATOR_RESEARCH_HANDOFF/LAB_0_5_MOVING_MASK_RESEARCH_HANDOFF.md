# NEXAH Lab 0.5 — The Moving Mask

## Mathematical research handoff

### Status

**Proposed bounded experiment — not yet implemented**

This document preserves the first directly formalizable research question that emerged from:

**NEXAH — The Pattern of Orientation: From Maps to Whip**

The purpose is not to prove the complete NEXAH architecture. It is to select one stone, define it precisely, and make it available for mathematical and computational examination.

---

## 1. Central research question

> **How does a moving observation mask affect the stability of a weighted relational state estimator?**

The question separates:

- the underlying state;
- the observation process;
- the moving mask;
- the local estimates;
- their weighting and binding;
- the resulting relational estimate;
- the information that cannot be recovered.

This is the smallest useful bridge from the symbolic Q° architecture to a concrete mathematical experiment.

---

## 2. Scientific boundary

Lab 0.5 does **not** test whether Q° is:

- a universal mathematical operator;
- a new physical object;
- a fifth quaternion component;
- a single mechanism shared by unrelated physical domains;
- proof that every observer-relative structure follows the same law.

It tests one declared estimator under one declared class of masks.

\[
\boxed{
\text{one model}
+\text{one mask family}
+\text{one estimator}
+\text{explicit metrics}
}
\]

---

## 3. Minimal formal setting

Begin in a finite-dimensional real vector space:

\[
x_t\in\mathbb R^d.
\]

This restriction is deliberate. It allows the first experiment to use ordinary linear algebra before considering rotations, manifolds, graphs, probability measures, or other non-Euclidean objects.

### 3.1 Underlying state

Let:

\[
x_{t+1}=A_tx_t+\eta_t,
\]

where:

- \(x_t\) is the latent state;
- \(A_t\) is the declared state-transition operator;
- \(\eta_t\) is process disturbance or model error.

The first implementation may use a known synthetic trajectory, so the true \(x_t\) is available for evaluation.

### 3.2 Observation operator

For observer or channel \(i\):

\[
y_{i,t}
=
W_{i,t}H_i x_t+\varepsilon_{i,t}.
\]

Here:

- \(H_i\) is the projection or measurement operator;
- \(W_{i,t}\) is a time-dependent mask;
- \(\varepsilon_{i,t}\) is observation noise;
- \(y_{i,t}\) is the visible record.

The mask may be represented initially by a diagonal matrix:

\[
W_{i,t}
=
\operatorname{diag}
\left(
\omega_{i,t}^{(1)},\ldots,\omega_{i,t}^{(m_i)}
\right),
\]

with:

\[
\omega_{i,t}^{(k)}\in\{0,1\}.
\]

Later experiments may allow:

\[
\omega_{i,t}^{(k)}\in[0,1],
\]

to represent attenuation rather than complete occlusion.

### 3.3 Local estimates

Each channel produces a local estimate:

\[
\hat x_{i,t}
=
\mathcal E_i
\left(
y_{i,0:t},
W_{i,0:t},
H_i
\right).
\]

The estimator \(\mathcal E_i\) must be declared. The first experiment should use a simple reproducible estimator before introducing more elaborate filters.

Possible later variants include:

- least-squares reconstruction;
- recursive least squares;
- Kalman filtering;
- Bayesian estimation;
- regularized inverse reconstruction.

### 3.4 Translation into a shared comparison space

If local estimates use different coordinates, define:

\[
z_{i,t}
=
\mathcal T_i[\hat x_{i,t}]
\in\mathbb R^d.
\]

Every \(\mathcal T_i\) must be explicit.

No binding is performed until all \(z_{i,t}\) occupy the same declared comparison space.

### 3.5 Weights

Let:

\[
w_{i,t}\geq0,
\qquad
\sum_iw_{i,t}>0.
\]

Normalized weights are:

\[
\lambda_{i,t}
=
\frac{w_{i,t}}
{\sum_jw_{j,t}},
\qquad
\sum_i\lambda_{i,t}=1.
\]

Possible weighting rules include:

- fixed equal weights;
- inverse estimated variance;
- visible fraction of the record;
- recent reconstruction error;
- declared confidence;
- another measured and documented reliability criterion.

The experiment must never switch between weighting interpretations without recording the change.

### 3.6 Relational estimator

The first Euclidean Q° estimator is:

\[
\boxed{
Q_t^\circ
=
\sum_{i=1}^{n}
\lambda_{i,t}z_{i,t}
}
\]

or equivalently:

\[
\boxed{
Q_t^\circ
=
\frac{
\sum_iw_{i,t}\mathcal T_i[\hat x_{i,t}]
}{
\sum_iw_{i,t}
}
}
\]

In Lab 0.5:

\[
Q_t^\circ
\in\mathbb R^d
\]

is a weighted relational state estimate.

It is not the underlying state itself:

\[
\boxed{
Q_t^\circ\neq x_t
}
\]

The difference can be measured because the experiment uses a known synthetic \(x_t\).

---

## 4. The moving-mask family

The mask should vary independently along controlled dimensions.

### Mask position

\[
p_t\in[0,1]
\]

describes the normalized position of the masked interval or region.

### Mask width

\[
b_t\in[0,1]
\]

describes the obscured fraction of the observation domain.

### Mask velocity

\[
v_t=\frac{dp_t}{dt}.
\]

### Mask acceleration

\[
a_t=\frac{d^2p_t}{dt^2}.
\]

### Mask schedule

Candidate schedules:

1. static mask;
2. constant-velocity sweep;
3. sinusoidal movement;
4. abrupt jumps;
5. stochastic movement;
6. adversarial movement targeting high-information regions.

The first version needs only:

- no mask;
- static mask;
- one constant-velocity sweep.

---

## 5. Primary hypotheses

### H0 — Mask invariance

The movement of the mask has no systematic effect on relational-estimator error beyond the amount of information removed.

This is the null hypothesis.

### H1 — Width effect

Increasing mask width increases the estimation error:

\[
b_t\uparrow
\quad\Rightarrow\quad
\|Q_t^\circ-x_t\|\uparrow
\]

under otherwise fixed conditions.

This relation need not be strictly monotonic for every trajectory, but the aggregate tendency can be tested.

### H2 — Velocity effect

For estimators using retained history, equal mask width with different mask velocity produces different stability and reconstruction error.

The mask geometry alone is therefore insufficient; its temporal behaviour matters.

### H3 — Weighting effect

Reliability-aware weights reduce error relative to equal weights when channels have unequal mask exposure or noise.

### H4 — False-confidence boundary

An estimator may remain numerically smooth while becoming informationally unsupported.

Therefore low short-term variation:

\[
\|Q_t^\circ-Q_{t-1}^\circ\|
\]

does not by itself imply accuracy:

\[
\|Q_t^\circ-x_t\|.
\]

This tests a central NEXAH distinction:

> Apparent stability is not necessarily justified orientation.

### H5 — Reacquisition

After the mask leaves an informative region, the estimator requires a measurable recovery interval before returning within a declared error tolerance.

---

## 6. Existence, uniqueness, and stability questions

### Existence

Under what conditions is \(Q_t^\circ\) defined?

For the weighted Euclidean estimator:

\[
\sum_iw_{i,t}>0
\]

is required.

If every channel receives zero weight, Q° is undefined rather than silently set to zero.

### Uniqueness

The Euclidean weighted mean is unique for a declared set of translated estimates and weights.

But the full process may still be non-unique because:

- local inverse problems may admit multiple solutions;
- translation maps may be ambiguous;
- different legitimate weighting rules may produce different results;
- hidden regions may be underdetermined.

### Stability

Investigate whether small changes in:

\[
y_{i,t},\quad
W_{i,t},\quad
w_{i,t},\quad
\mathcal T_i
\]

produce bounded changes in:

\[
Q_t^\circ.
\]

A local sensitivity measure is:

\[
\frac{
\|Q_t^\circ(\theta+\delta\theta)
-Q_t^\circ(\theta)\|
}{
\|\delta\theta\|
},
\]

where \(\theta\) collects the experimental parameters.

### Information loss

Which components of \(x_t\) become unobservable under \(W_{i,t}H_i\)?

The rank:

\[
\operatorname{rank}(W_{i,t}H_i)
\]

provides a first linear diagnostic.

Across a time window, the experiment should examine whether movement of the mask restores aggregate observability or repeatedly hides the same state directions.

### Reconstruction boundary

The experiment must distinguish:

- directly observed;
- masked but reconstructable under declared assumptions;
- underdetermined;
- unknown.

Unknown regions must not be filled merely to maintain visual continuity.

---

## 7. Experimental conditions

Use a synthetic ground-truth trajectory and vary one factor at a time.

### Minimum condition matrix

| Condition | Mask | Weights | History | Purpose |
|---|---|---|---|---|
| C0 | none | equal | available | unmasked reference |
| C1 | static | equal | available | spatial-loss baseline |
| C2 | moving | equal | available | temporal mask effect |
| C3 | moving | reliability-aware | available | weighting comparison |
| C4 | moving | equal | unavailable | reconstruction boundary |
| C5 | moving | reliability-aware | unavailable | confidence without history |

### Controlled variables

- latent trajectory;
- noise seed;
- observation operators;
- sampling frequency;
- estimator family;
- initial conditions;
- mask width when testing velocity;
- mask velocity when testing width.

---

## 8. Measurements

### State-estimation error

\[
e_t
=
\|Q_t^\circ-x_t\|.
\]

Report:

- mean error;
- median error;
- maximum error;
- error distribution;
- error during masked and unmasked intervals.

### Stability

\[
s_t
=
\|Q_t^\circ-Q_{t-1}^\circ\|.
\]

This measures estimator movement, not correctness.

### Reacquisition time

Time required after mask release until:

\[
\|Q_t^\circ-x_t\|\leq\tau
\]

for a declared tolerance \(\tau\).

### Information availability

Track:

- visible fraction;
- rank of the masked observation operator;
- estimated uncertainty;
- number of contributing channels;
- effective weight concentration.

### False confidence

Compare smoothness and uncertainty against actual error.

A false-confidence event occurs when the estimator reports or visually suggests high certainty while:

\[
e_t>\tau.
\]

The uncertainty rule and threshold must be declared in advance.

---

## 9. Baselines

The Q° estimator should be compared with simple alternatives:

1. unmasked ground-truth reference;
2. equal-weight mean;
3. last-observation-carried-forward;
4. single best channel;
5. reliability-weighted mean;
6. a standard estimator such as a Kalman filter, if the model assumptions permit it.

Without baselines, visual smoothness is not evidence of improved orientation.

---

## 10. Falsification and failure criteria

The experiment should count against the proposed relational architecture if:

- Q° performs no better than simple baselines under the conditions for which weighting is claimed to help;
- reliability-aware weighting consistently increases error;
- the proposed stability measure does not distinguish supported orientation from smooth but inaccurate output;
- results depend mainly on undocumented parameter tuning;
- conclusions disappear under new random seeds or trajectories;
- the operator is undefined for common conditions that the architecture claims to handle;
- reconstruction labels fail to distinguish measured, inferred, and unknown values;
- moving-mask effects can be completely explained by removed sample count, contrary to a claimed temporal effect.

Negative results remain useful. They identify where the symbolic architecture does not justify a new formal mechanism.

---

## 11. Expected outputs

A completed Lab 0.5 should produce:

1. a short protocol;
2. a deterministic synthetic model;
3. explicit parameter definitions;
4. automated tests;
5. baseline comparisons;
6. plots of truth, observations, masks, estimates, and uncertainty;
7. a result record;
8. a limitations statement;
9. a clear distinction between observation, reconstruction, and unknown;
10. a decision on whether a successor experiment is justified.

The interactive visual is secondary. The mathematical definitions and recorded outputs are authoritative.

---

## 12. Implementation order

### Phase A — Definition

- select \(d\);
- define \(A_t\);
- define \(H_i\);
- define the first mask family;
- define the local estimator;
- define the weighting rules;
- declare the metrics and thresholds.

### Phase B — Deterministic benchmark

- generate one fixed trajectory;
- run C0–C5 with fixed seeds;
- save all parameters and outputs;
- verify automated invariants.

### Phase C — Sensitivity

- vary mask width;
- vary mask velocity;
- vary noise;
- vary weight concentration;
- repeat across seeds.

### Phase D — Result

- compare baselines;
- assess the hypotheses;
- document failure cases;
- decide whether the model warrants extension.

No public claim should precede Phase D.

---

## 13. Further connections — preserved, not combined

The following questions emerged from the wider orientation series. They should not be folded into Lab 0.5 until the moving-mask experiment is understood.

### A. Transition consistency

> When do different routes between local maps produce the same translated state?

\[
\mathcal T_{ik}
\stackrel{?}{=}
\mathcal T_{ij}\circ\mathcal T_{jk}.
\]

Possible successor:

**Lab 0.6 — The Joints**

### B. Observer dependence

> Which properties of Q° remain invariant when the observer frame changes?

Possible successor:

**Lab 0.7 — The Observer Change**

### C. Five-reference geometry

> What changes when five weighted reference points form a simplex, graph, or constrained reference structure rather than an unconstrained Euclidean mean?

Possible successor:

**Lab 0.8 — The Five References**

### D. Q° as estimator versus controller

> When should Q° describe a state estimate, and when should it generate a control action?

Keep separate:

\[
Q_t^\circ=\text{estimate}
\]

and:

\[
u_t=\pi(Q_t^\circ,r_t,C_t).
\]

Possible successor:

**Lab 0.9 — Estimate to Action**

### E. Dynamic alignment

> Under what conditions does relational estimation improve or destabilize phase alignment between coupled moving components?

Possible successor:

**Lab 1.0 — The Whip**

### F. Biomechanical application

> Can measured grip pressure, joint angles, shaft orientation, and impact timing support the proposed golf mappings?

This requires domain expertise and measurement data. It should remain an application study, not a premise of the mathematical model.

---

## 14. The research ladder

\[
\boxed{
\text{MASK}
\rightarrow
\text{ESTIMATE}
\rightarrow
\text{WEIGHT}
\rightarrow
Q^\circ
\rightarrow
\text{TEST}
\rightarrow
\text{BOUNDARY}
}
\]

Lab 0.5 begins with the mask because it creates a clean distinction between:

- what exists in the synthetic source;
- what is projected;
- what is visible;
- what is reconstructable;
- what remains unknown;
- what the relational estimator reports.

That distinction is the scientific bridge between the symbolic NEXAH architecture and a falsifiable model.

---

## 15. Freeze statement

The research direction is preserved.

No complete theory is claimed. No implementation is required tonight.

The next valid step is:

> **Define and benchmark one moving-mask estimator before extending Q° into additional domains.**

The wider connections remain visible as separate successor questions. They are not lost, and they are not prematurely combined.

