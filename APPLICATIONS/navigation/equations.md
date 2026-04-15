# NEXAH Navigation – Mathematical Formulation

**Version:** April 2026  
**Status:** Empirical prototype implementation

## 1. Mod-77 Hierarchical State Space

The discrete state space is constructed as the direct product of two cyclic groups:

\[
\mathbb{Z}/7\mathbb{Z} \times \mathbb{Z}/11\mathbb{Z}
\]

- Number of base states: \(7 \times 11 = 77\)
- Each base state is locally refined by four points using offset \(\delta = 0.17\), resulting in \(77 \times 4 = 308\) fine states.

**Voltage-to-state mapping**

A continuous bus voltage \(V\) (in per-unit, typically in \([0.65, 1.05]\)) is first normalized:

\[
v_{\text{norm}} = \frac{V - 0.65}{0.40}
\]

Then quantized to grid coordinates:

\[
r_7 = \round(v_{\text{norm}} \cdot 6) \mod 7
\]
\[
r_{11} = \round(v_{\text{norm}} \cdot 10) \mod 11
\]

The integer index of a base state is:

\[
\text{index} = r_7 \cdot 11 + r_{11}
\]

**Drift between consecutive states**

\[
\Delta r_7 = (r_7^{(t+1)} - r_7^{(t)}) \mod 7
\]
\[
\Delta r_{11} = (r_{11}^{(t+1)} - r_{11}^{(t)}) \mod 11
\]

Normalized drift magnitude:

\[
\text{drift\_magnitude} = \max\left( \left| \frac{\Delta r_7}{7} \right|, \left| \frac{\Delta r_{11}}{11} \right| \right)
\]

## 2. Event Detection Rules (heuristic thresholds)

- **Phi-Split**: triggered when \(\text{drift\_magnitude} > 0.25\)
- **Transfer Event**: triggered when \(\text{drift\_magnitude} > 0.7\)

These thresholds were chosen empirically based on visual inspection of a synthetic voltage collapse trajectory (0.98 p.u. → 0.65 p.u.).

## 3. Observed Scaling Behavior

On the tested voltage trajectories, the following empirical relation was observed:

\[
d^2 c \approx a \cdot c^p \cdot (dc)^q \quad \text{with} \quad p \approx 0.308
\]

where \(c\) represents a state variable and \(dc\) its change. The value \(p \approx 0.308\) indicates sub-linear dependence on the state magnitude and increasing dominance of flow (drift) terms for the tested cases.

Multiplication chain (observed):

- \(0.308 \times 1 = 0.308\)
- \(0.308 \times 2 = 0.616\)
- \(0.308 \times 3 = 0.924\)
- \(0.308 \times 4 = 1.232\)

No theoretical derivation from power system equations (e.g. differential-algebraic equations of the swing or power flow model) is currently available.

## 4. Connection to IEEE Test Systems

The grid has been applied to a synthetic trajectory resembling IEEE 9-bus voltage collapse behavior. In this specific run (13 time steps from 0.98 p.u. to 0.65 p.u.) the method detected:

- 9 Phi-Split events
- 9 Transfer events

The implementation is modular and can in principle be applied to larger IEEE benchmark systems (IEEE 118, IEEE 300, etc.). Systematic validation across multiple realistic contingencies and dynamic simulations has not yet been performed.

## 5. Limitations and Current Status

- The choice of moduli 7 and 11, refinement factor 4, and offset \(\delta = 0.17\) are design decisions without direct derivation from the underlying physics of power grids.
- The exponent \(p \approx 0.308\) and associated geometric interpretations (e.g. relation to 28°) are empirical observations on limited test data.
- The detected events (Phi-Split, Transfer) are heuristic indicators of significant drift changes, not yet proven predictors of voltage instability with quantified false-positive/false-negative rates.
- No rigorous comparison against established methods (e.g. continuation power flow, eigenvalue analysis, or energy function methods) has been conducted so far.

All equations above are directly implemented and numerically executable in the current codebase (`APPLICATIONS/navigation/core/`).

**Next required steps for scientific credibility:**
- Systematic testing on multiple IEEE benchmark cases with realistic dynamic models
- Statistical evaluation of detection performance (ROC curves, lead time, etc.)
- Sensitivity analysis with respect to grid parameters (7/11, δ, thresholds)
- Comparison with classical stability indicators

