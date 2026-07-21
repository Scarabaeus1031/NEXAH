# NEXAH Governance Index

This index separates constitutional purpose from governance, architecture,
repository documentation, implementation and generated artifacts.

## Start here

1. **[Ecosystem Constitution v1.0](ECOSYSTEM_CONSTITUTION.md)** — highest
   governance document; defines the constitutional Houses, their authority,
   boundaries and enduring principles.
2. **Governance** — assigns canonical responsibility and defines change,
   review, compatibility and publication procedures. Ecosystem governance
   begins in this directory; each House may maintain narrower governance
   documents within its own responsibility.
3. **[Architecture](../ARCHITECTURE/README.md)** — describes structures,
   contracts and dependencies that conform to the Constitution and Governance.
4. **Repository documentation** — explains the current contents, status,
   contribution paths and local operation of a particular maintained body of
   work.
5. **Implementation** — realizes approved architecture within the boundaries of
   its constitutional House.
6. **Generated artifacts** — render, project, export or snapshot canonical
   sources and remain derived from them.

```text
Constitution
    ↓
Governance
    ↓
Architecture
    ↓
Repository Documentation
    ↓
Implementation
    ↓
Generated Artifacts
```

An artifact lower in this hierarchy cannot redefine one above it.

## Constitutional status

The German Ecosystem Constitution v1.0 is adopted and canonical. Approved
translations must identify themselves as translations of the same version and
cannot establish independent constitutional authority.

The material in [`constitution_review_01/`](constitution_review_01/README.md)
records an earlier, non-canonical constitutional investigation. It remains
historical governance evidence and does not compete with the adopted Ecosystem
Constitution.

## House-local governance

The Constitution defines purpose. House-local documents define how that purpose
is maintained in a concrete body of work:

- the NEXAH Framework governs framework semantics, Research, OLS, Kernel and the
  current canonical Library Registry within their documented boundaries;
- ORION governs deterministic navigation, reports, validation and LYRA;
- Experience governs presentation, navigation and temporary interaction state;
- Living Atlas governs explicit editorial Relations;
- Operations governs continuity without acquiring content authority.

House-local documentation should reference the Constitution rather than repeat
its articles.

## Adoption record

The documentation-only alignment review is recorded in
[`ECOSYSTEM_CONSTITUTION_ADOPTION.md`](ECOSYSTEM_CONSTITUTION_ADOPTION.md).

## Operations reviews

Publication readiness is assessed in
[`OPERATIONS_01_PUBLIC_LAUNCH_PREPARATION.md`](OPERATIONS_01_PUBLIC_LAUNCH_PREPARATION.md).
Operations reviews apply the Constitution and Governance to continuity and
publication without acquiring authority over their subjects.
