# NEXAH Safety and Misuse Boundaries

Status: normative safety boundary for the current public kernel

NEXAH can reveal paths, dependencies, bottlenecks, sampled boundaries, and
structural sensitivities. Those capabilities can support protection and
learning, but they can also be used to identify targets, optimize disruption,
launder simulation into authority, or automate action without adequate
evidence.

This document defines the boundary between orientation and operational power.
It applies to the `nexah` package, maintained applications, future adapters,
reports, memory, and any external execution layer built around them.

## Core safety principle

> NEXAH may reveal structural sensitivity to support protection and learning.
> It must not silently convert that knowledge into targeting, authority, or
> action.

Orientation, recommendation, authorization, execution, observation, and
learning are separate stages. A result from one stage does not inherit the
authority of the next.

## Primary misuse risks

| Risk | Unsafe conversion |
|---|---|
| Vulnerability targeting | bottleneck or critical-edge analysis → target list |
| Disruption optimization | training perturbation → damage-maximizing plan |
| Autonomous execution | Orientation Report → unreviewed actuator command |
| Evidence laundering | simulation or correlation → operational or causal claim |
| Memory poisoning | fabricated outcome → trusted episodic experience |
| Surveillance or manipulation | human/social map → coercive profiling or influence |
| Sensitive topology exposure | protected infrastructure map → public actionable detail |

These risks are properties of how a capability is connected and used, not only
of an individual algorithm.

## Current enforced boundaries

The maintained kernel is designed so that:

- the Orientation Core has no direct actuator or execution authority
- probes are read-only and cannot mutate a backend
- multiple perspectives preserve disagreement rather than vote a truth
- structural results do not automatically become risk, stability, or causal
  claims
- scenarios and simulations remain distinct from observations and outcomes
- unknown uncertainty is reported as unknown rather than fabricated
- episodic memory requires a separately admitted observed outcome
- source identity, context, provenance, and evidence roles remain inspectable
- decision support and execution remain outside the Core

The outcome firewall enforces the governing learning rule:

> **NO OBSERVED OUTCOME → NO EPISODIC MEMORY UPDATE**

## Uses that require control or are outside the public kernel

The following capabilities must not be enabled merely by attaching an adapter:

- direct control of physical, biological, financial, social, or critical
  infrastructure systems
- automated ranking of real-world targets by disruption potential
- autonomous intervention selection or execution
- covert monitoring, behavioral manipulation, or coercive profiling of people
- publication of actionable sensitive topology or vulnerability details
- causal or safety guarantees derived only from structural analysis
- automatic learning from simulations, declared scenarios, or unverified
  external claims

Legitimate research into these areas requires a separately governed project,
domain review, controlled data handling, and explicit authorization. The open
orientation contracts alone are not approval.

## Data and publication boundary

Public artifacts may contain illustrative fixtures, synthetic data, standard
benchmarks, redacted summaries, and methods whose limitations are explicit.

Operationally sensitive material requires at least:

- documented ownership, license, and purpose
- data minimization and entity redaction where appropriate
- access control and least-privilege roles
- separation of public summaries from actionable topology
- audit logs for access, transformation, and export
- review of whether outputs reveal exploitable paths or dependencies
- retention and deletion rules
- an incident and disclosure process

The repository must not become an accidental catalog of real-world attack
surfaces.

## Release ladder

Capabilities advance independently; production readiness is not inherited from
research validity.

| Level | Permitted role | Required gate |
|---|---|---|
| 1. Orientation | describe and compare supplied representations | current typed contracts and validation |
| 2. Decision support | present bounded options to a human | domain evidence, calibrated limitations, auditability |
| 3. Recommendation | rank options without executing | explicit objectives, constraints, causal basis, human review |
| 4. Authorized action | execute a human-approved bounded action | separate executor, identity, authorization, rollback |
| 5. Limited automation | repeat reversible actions inside a safety envelope | monitoring, abstention, fail-safe behavior, independent assurance |
| 6. Domain autonomy | select and execute consequential actions | domain-specific safety case and external governance |

The current public kernel is at Level 1. Components must not describe
themselves as a higher level without satisfying and documenting that level's
gate.

## Requirements before a real-world source enters

Before operational or public measurements are admitted:

1. Complete the
   [Observed-Evidence Admission Checklist](../testkit/observed_evidence/ADMISSION_CHECKLIST.md).
2. Define the legitimate purpose, affected people or systems, and prohibited
   uses.
3. Classify sensitivity of inputs, derived maps, and reports.
4. Specify who may view vulnerability-level findings.
5. Freeze development/evaluation separation and outcome definitions.
6. Test abstention, missing data, adversarial inputs, and evidence leakage.
7. Keep execution disconnected unless it has its own authorization and safety
   review.
8. Record how incidents, errors, and harmful outputs can be reported and
   contained.

If these conditions are absent, the source remains unadmitted and cannot
authorize operational claims or episodic learning.

## Requirements for any future executor

An executor, if ever built, must be a separate component with:

- explicit user and system identity
- least-privilege action permissions
- allowlisted, bounded, and preferably reversible actions
- human confirmation for consequential actions
- constraint and conflict checks independent of the Orientation Core
- abstention on unknown, incomplete, or out-of-distribution context
- dry-run and simulation modes that remain labeled as such
- rollback, fail-safe state, rate limits, and emergency stop
- immutable audit records connecting evidence, proposal, authorization, action,
  and observed outcome
- no automatic memory update from the act of execution itself

The interface must preserve this separation:

```text
OrientationReport
→ ActionProposal
→ independent safety and policy checks
→ explicit authorization
→ separate Executor
→ independently observed outcome
→ outcome firewall
→ eligible learning record
```

## Review questions

Before releasing a new capability, ask:

1. Does it reveal a sensitive dependency or target?
2. Could a scenario output be mistaken for observed evidence?
3. Does it increase authority, automation, or irreversibility?
4. Can the system abstain when evidence is missing or unfamiliar?
5. Who is affected, and who can contest the result?
6. Are access, authorization, and accountability explicit?
7. Can a harmful output be contained and traced?

An unclear answer is a reason to stop at orientation, not permission to
continue toward action.

