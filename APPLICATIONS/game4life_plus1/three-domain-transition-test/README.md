# WINDOW 03 — Three-Domain Transition Test

Status: `UNADMITTED_EXPLORATORY_MODEL_BENCHMARK`

This isolated demonstrator tests whether the same declared 4+1 observation
grammar can inspect three different finite model operators without treating
their objects, semantics or mechanisms as identical.

- chemical model: Gray–Scott reaction–diffusion;
- artificial-life model: Conway B3/S23;
- physical model: deterministic-seed Glauber-like spin updates.

The common observation alphabet is `1 = all active transitions`, `i = positive
transition`, `j = retained positive state`, `k = negative transition`, with
`Q°` carrying model, boundary and time. The comparison measures cubical-complex
`beta0`, `beta1`, transition counts and a cell-address boundary residual.

The chemistry lane is thresholded and therefore explicitly lossy. The page is
a model/instrument benchmark, not empirical chemistry, biology or physics. It
does not modify the frozen LIFE08 result, create a shared mechanism or carry
publication status.

## Euler View

The fourth card is a shared mathematical view, not a fourth domain. Each exact
transition ledger is mapped to a complex phasor

`z = (C11-C00)/N + i(C01-C10)/N`,

so the three models can be compared in one Euler plane while their operators,
objects and semantics remain distinct. The displayed mean `Z-bar` is only the
mean of those three normalized readouts.

The lower Euler motor reuses the GAME 4 LIFE +1 arithmetic/geometric gearbox.
The shared Three-Domain generation drives `n=g mod 8`, the exact zero-insertion
sequence `a_n=10^(n+1)+1`, and the even/odd XI-Hinge versus Janus-axis view.
Manual phase inspection detaches the motor until **Follow Three-Domain clock**
is enabled again. None of these projections alters Gray-Scott, Conway B3/S23,
the Glauber-like spin update, their seeds, or boundary operators.

## Verify

```bash
node tests.cjs
```
