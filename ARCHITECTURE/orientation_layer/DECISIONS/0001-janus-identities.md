# ADR 0001 — Separate the JANUS identities

Status: accepted for the Orientation Layer plan

## Context

Repository language has used “Janus” both for a broad complementary-perspective
principle and for a mathematical forward/backward operator. This makes symbolic
architecture appear to be implemented by a particular scientific algorithm.

## Decision

Use three explicit identities:

1. **JANUS** — conceptual principle; no implementation class is required.
2. **Janus Bridge** — architectural translation between representations.
3. **Janus Directional Coherence Operator** — scientific forward/backward
   coherence analysis.

The Bridge and scientific Operator are sibling realizations of JANUS. The
Operator may support a Bridge, but neither component depends on the other by
definition.

Generic implementation classes named only `Janus` are avoided. If an existing
public `JanusFieldOperator` is renamed, it remains temporarily available as a
documented deprecated compatibility alias.

## Consequences

- theory and visual language retain the JANUS identity
- architecture gains a separate bridge contract
- scientific code receives method-specific names and tests
- repository occurrences require classification as Concept, Architecture, or
  Scientific Operator
- ambiguous occurrences are recorded for manual review rather than renamed
  mechanically

