# Discovery Taxonomy

## Purpose

This taxonomy is for navigation. It does not add an epistemology to OLS or alter
the status of source material.

## Entry kinds

| Kind | Meaning | Why needed |
|---|---|---|
| Proof | A bounded claim established by a formal proof or frozen architectural experiment | Separates proof obligations from ordinary empirical support |
| Construction | An exact, reproducible mathematical or semantic object | Exactness is different from observed performance |
| Finding | A bounded conclusion supported by declared evidence | Main unit for empirical navigation |
| Negative result | A predeclared claim that failed its support rule | Prevents a success-only archive |
| Limitation | A known boundary, insufficiency, or non-claim | Makes responsible reuse possible |
| Hypothesis | A testable claim without sufficient current support | Preserves research without promotion |
| Representation | A view derived from evidence that is not itself the authority | Prevents visual similarity from becoming proof |
| Application result | A bounded result inside a declared domain protocol | Keeps domain scope visible |
| Historical exploration | A preserved earlier interpretation or experiment | Retains provenance without implying current support |

## Controlled epistemic statuses

| Status | Definition |
|---|---|
| `MATHEMATICALLY_EXACT` | Follows exactly from the declared mathematical construction; empirical behavior is not implied |
| `ARCHITECTURALLY_VALIDATED` | A frozen specification, release, or bounded architectural check satisfies its declared criteria |
| `EXPERIMENTALLY_SUPPORTED` | A declared empirical test met its support rule within its stated data and metric |
| `PARTIALLY_SUPPORTED` | Some declared evidence supports the claim, but important scope or independence requirements remain |
| `NOT_SUPPORTED` | A declared test did not meet its support rule; this is not proof of impossibility |
| `INCONCLUSIVE` | Available evidence cannot distinguish the relevant alternatives |
| `OPEN_HYPOTHESIS` | Testable wording exists, but adequate evidence does not |
| `DOCUMENTED_LIMITATION` | A verified boundary, absence, insufficiency, or prohibited implication |
| `HISTORICAL_ONLY` | Preserved for lineage but not a statement of current support |
| `SUPERSEDED` | Replaced by a named later source while retained for history |
| `BLOCKED` | A required source, input, permission, or evidence-chain link is unavailable |
| `UNKNOWN` | Status cannot yet be assigned responsibly |

Status and kind are independent: a negative result normally has
`NOT_SUPPORTED`; a construction may be `MATHEMATICALLY_EXACT`; a representation
may have only a documented limitation.

## Scope vocabulary

- universal formal result;
- repository architecture;
- OLS semantic release;
- specific experiment;
- specific dataset;
- specific application domain;
- implementation-only behavior;
- visual representation;
- independent editorial review;
- historical exploration.

Free text may narrow these terms but must not broaden them.

## Evidence vocabulary

- formal derivation;
- release specification and integrity manifest;
- frozen experiment specification;
- deterministic replay;
- held-out experiment;
- null-model comparison;
- unit-tested implementation;
- independent review;
- generated artifact;
- visual analysis;
- manual observation;
- historical narrative;
- missing primary evidence.

## Terms that must remain distinct

**Proof** means that a declared proof obligation was discharged. It must say
whether the proof is mathematical or architectural.

**Result** is the direct output of an exact construction, computation, or
declared evaluation. A result is not automatically a finding.

**Finding** is a bounded interpretation supported by results and their declared
decision rule.

**Discovery** is useful only as an informal umbrella term. It should not be a
status because it suggests novelty and importance without specifying evidence.

**Evidence** is a source artifact or observation that supports, limits, or
contradicts a claim. It is not the claim itself.

**Experiment** is the full declared procedure, inputs, implementation, and
outputs. It may yield positive, negative, inconclusive, or no stable findings.

**Review** evaluates evidence, wording, placement, or status. It is not proof
unless the review itself executes a declared proof protocol.

## Admission rule

An atlas entry is admissible only when it has:

1. a smallest meaningful claim;
2. declared scope;
3. one controlled status;
4. one authoritative repository source or an explicit `BLOCKED` source gap;
5. supporting and limiting references;
6. reproducibility status;
7. a statement of what the claim does not imply.

Visuals alone cannot satisfy items 3–6. Repeated language alone cannot satisfy
item 1. Historical importance alone does not establish current support.
