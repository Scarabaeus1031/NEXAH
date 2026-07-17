# Registry Inventory and Integrity Report

Release: `OLS-RELEASE-1.0.0`  
Registry set version: `1.0.0`

## Normative registry inventory

| Owner | Annex or clause | Registry content | Version/status |
| --- | --- | --- | --- |
| `OLS-0` | Annex A | Specification document registry | `1.0.0`, Normative |
| `OLS-1` | Annex A | Universal Concept Registry | `1.0.0`, Normative |
| `OLS-1` | Annex B | Universal Boundary Matrix | `1.0.0`, Normative |
| `OLS-2` | Annex A | Declaration Registry | `1.0.0`, Normative |
| `OLS-2` | Annex B | Primitive Operator Ownership Registry | `1.0.0`, Normative |
| `OLS-2` | Annex C | Operator Contract Template | `1.0.0`, Normative |
| `OLS-3` | Annex A | Profile Registry | `1.0.0`, Normative |
| `OLS-3` | Annex B | Dependency and Activation Matrix | `1.0.0`, Normative |
| `OLS-3` | Annex C | Primitive Concept Ownership Registry | `1.0.0`, Normative |
| `OLS-4` | Annex A | Semantic Product Registry | `1.0.0`, Normative |
| `OLS-4` | Annex B | Semantic Transition and Derivation Matrix | `1.0.0`, Normative |
| `OLS-4` | Annex C | Prohibited Derivation Registry | `1.0.0`, Normative |
| `OLS-5` | Annex A | Conformance Class Registry | `1.0.0`, Normative |
| `OLS-5` | Annex B | Requirement-to-Test Matrix | `1.0.0`, Normative |
| `OLS-5` | Annex C | Conformance Status Registry | `1.0.0`, Normative |
| `OLS-6` | Clauses 5–23 | Extension, version, release, change, deprecation, and registry governance | `1.0.0`, Normative |

## Informative indexes

| Owner | Location | Content | Authority boundary |
| --- | --- | --- | --- |
| `OLS-I` | Annex D | Complete bidirectional traceability export | Informative; owning OLS clauses remain authoritative |
| Release package | Publication and digest inventories | Release navigation and byte verification | Release-control metadata only |

## Registry counts

| Registry class | Version 1.0 count |
| --- | ---: |
| Specification documents | 8 |
| Universal concepts | 14 |
| Profile primitive concepts | 4 |
| Declarations | 10 |
| Primitive operators | 10 |
| Semantic profiles | 7 |
| Semantic products | 11 |
| Product transitions | 13 |
| Accepted derivations | 18 |
| Conditional derivations | 18 |
| Conformance classes | 6 |
| Conformance status values | 5 |
| Trace records | 230 |

## Integrity result

Every normative registry remains inside its owning immutable publication. The owning document digest is the registry container digest recorded in the Release Manifest. No detached export claims normative precedence. No registry collision, duplicate primitive owner, orphaned owner, or duplicate Document ID was detected.

