# Audience Entry Points

## Researchers

Start with the ecosystem overview, then use traceability to move between research evidence and the owning OLS clause.

Recommended path:

```text
OVERVIEW → Research index → Trace ID → owning OLS part → OLS-I rationale
```

Researchers should not cite an experiment as though it were a published language rule, or cite an OLS rule as empirical proof.

## Specification readers

Start with OLS-0 and the [Specification Reader Guide](SPECIFICATION_GUIDE.md).

Recommended path:

```text
OLS-0 → OLS-1 → owning part → normative annex or registry → OLS-5 if claiming conformance
```

## Developers

Developers creating tools, schemas, or adapters begin with the universal semantics and then read the contracts and profiles they implement.

Recommended path:

```text
OLS-0 → OLS-1 → OLS-2 → applicable OLS-3 profiles → OLS-4 transitions → OLS-5 tests → OLS-I guidance
```

The implementation mapping lists supported OLS IDs and does not turn code types into language definitions.

## Implementers

Implementers include software teams and authors of repeatable human procedures.

Recommended path:

```text
Claimed capability
→ applicable base requirements
→ declarations and operator contracts
→ active profiles and dependencies
→ derivations/transitions
→ OLS-5 conformance class and tests
→ evidence-backed report
```

## General visitors

Start with [OVERVIEW.md](OVERVIEW.md) and the simple public diagram. Continue to OLS-I for explanation. Use the normative suite only when precise definitions or conformance claims are needed.

## Maintainers

Maintainers follow:

```text
ARCHITECTURE → OLS-6 → release manifest → migration/change record → conformance verification
```

No maintenance operation may silently change specification semantics.

