# System Models

Status: neutral research navigation; no active model authority

This directory is reserved for concise reference records about established or
externally defined systems used in NEXAH research. It is not a new theory
layer, executable toolbox, validation store, or application owner.

A system record may state:

- the standard mathematical definition;
- the parameters and conventions actually used;
- the representations produced in NEXAH;
- pointers to owning code, experiments, outputs, and reports;
- known transformation, projection, and artifact risks;
- the current claim and evidence status.

It must not duplicate scripts, GIFs, datasets, or full experimental reports.
Those remain with their existing owners in `APPLICATIONS/`, `VALIDATION/`,
`APPLIED_CASES/`, or another declared package.

## Initial system families

The current cross-system work includes:

- Lorenz
- Roessler
- Halvorsen
- Kuramoto
- Mandelbrot and Julia iteration
- prime modular residue systems
- IEEE state-space and continuation representations

Until individual records are needed, use the central
[NEXAH Mathematics Map](../MATHEMATICS_MAP.md). Create a system record only when
it resolves a concrete ambiguity of definition, parameterization, provenance,
or representation.

## Separation of responsibilities

```text
SYSTEM_MODELS   -> neutral definition and pointers
APPLIED_CASES   -> worked research interpretations
VALIDATION      -> bounded tests and evidence
APPLICATIONS    -> domain implementations and programs
ORION           -> certified deterministic execution only
```
