# Frozen Experimental Specification

## Question

For one deterministic prime sequence, do modulo-17 residue transitions show
stronger out-of-sample predictive structure than modulo 7 and control moduli?
Separately, does the already proposed affine rule from modulo 7 to modulo 17
reconstruct held-out modulo-17 coordinates above a trivial baseline?

## Input

The canonical input is the first 20,000 prime numbers in ascending order,
including 2 and 3. The sequence is generated locally by a deterministic sieve.

Two predeclared policies are evaluated:

- `all_primes`: includes every generated prime;
- `without_2_3`: removes 2 and 3 from the training prefix only.

Both policies use identical held-out index ranges from the canonical sequence.
Because 2 and 3 occur before every test range, this isolates their effect on
the learned training distributions.

## Prediction task

For each modulus in `{5, 7, 11, 13, 17, 19, 23}`, map primes to residues and
fit a first-order Markov model to the chronological training prefix. Additive
smoothing is fixed at `alpha = 0.5`.

The baseline is the training-only marginal distribution of the next residue.
The primary metric is held-out information gain:

```text
(marginal log loss - Markov log loss) / log(2)
```

in bits per event. Positive values mean that the preceding residue provides
held-out information beyond the training marginal.

Five expanding chronological folds are fixed:

| Fold | Training indices | Test indices |
|---|---:|---:|
| 1 | 0–50% | 50–60% |
| 2 | 0–60% | 60–70% |
| 3 | 0–70% | 70–80% |
| 4 | 0–80% | 80–90% |
| 5 | 0–90% | 90–100% |

No test observation is used for fitting.

For each fold, 100 deterministic training-sequence shuffles form a null
distribution. Shuffling preserves the training marginal while breaking
sequential order. The shuffled models are evaluated against the unchanged
held-out sequence.

## Prediction decision rules

The evidence supports “modulo 17 exceeds modulo 7 in this experiment” only if:

1. the paired bootstrap 95% interval for mean fold-wise information-gain
   difference `mod17 - mod7` is strictly above zero under both prime policies;
   and
2. modulo 17 has the highest mean information gain among all declared moduli
   under both policies.

Ten thousand deterministic paired bootstrap resamples are used.

The 2/3 sensitivity result is flagged if the sign of `mod17 - mod7` changes or
if the absolute difference between the two policy estimates exceeds
0.001 bits/event.

## Proposed 7-to-17 bridge

The fixed candidate is:

```text
r7  = prime mod 7
r17 = (7 * r7 + 8) mod 17
```

It is evaluated on the same held-out folds. Its exact-match accuracy is
compared with:

- a training-only majority residue baseline; and
- a training-only lookup that maps each observed modulo-7 residue to its most
  frequent modulo-17 residue.

The fixed bridge receives support only if the paired bootstrap 95% interval
for `fixed bridge accuracy - majority accuracy` is strictly above zero under
both prime policies.

This formula is treated as a proposed representative recoding, not as a
canonical group embedding from `Z/7Z` into `Z/17Z`.

## Comparison limitation

Different moduli produce different residue-alphabet sizes. Information gain in
bits per event is directly measurable across them, but a larger alphabet also
permits more possible sequential structure. The control-modulus ranking is
therefore a specificity screen: it can reject a unique Mod-17 interpretation,
but it cannot by itself identify an optimal modulus or a causal mechanism.

## Explicitly untested claim

This experiment contains no dynamical system, intervention, perturbation or
stability endpoint. It therefore cannot establish that modulo 17 is a clamp,
reset, attractor, error corrector or stabilizer. Such a claim requires a
separate controlled dynamical experiment with a predeclared stability metric.

## Determinism

- Python standard library only.
- No network, database, API or external data.
- Fixed seeds.
- No timestamps or absolute paths in generated artifacts.
- Generated candidates are written to temporary paths during verification.
