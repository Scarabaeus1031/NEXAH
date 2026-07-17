# Checksum Report

## Method

SHA-256 was calculated over the exact bytes of every locally available release candidate. Checksums were compared with the Phase 4A preservation baseline and the byte-identical delivery copies under `outputs/`.

## Available specification candidates

| Document | SHA-256 | Phase 4A match | Output-copy match |
| --- | --- | --- | --- |
| OLS-0 | `4be9c059362e10cb7b8d29f75225bc05c9458af1b453ed0d5a64c30b4d30f157` | Yes | Yes |
| OLS-1 | `fe1e71aed19be46fe62c99219c599ec470c1becebce1e3b6ab0fcc5230a2c7dc` | Yes | Yes |
| OLS-2 | `77358857c7eaea1db36e501d2a53bfa194a5f264b6608fb88d38ca000028ede7` | Yes | Yes |
| OLS-3 | `a06a15a291c3cbdb2206ec658442ec4c02ed0ee76a796896a7de1a3e94cb836d` | Yes | Yes |
| OLS-4 | `c1ed8f5b224829b03d19d1326fbfb6fc6f0f8d66a627ef741e7df0a32f6bfba4` | Yes | Yes |
| OLS-5 | `726136a423d0e3f2ad21b5d775c3132303d9b1733cee34058f90b7e223440aed` | Yes | Yes |
| OLS-6 | Not available | Not testable | Not available |
| OLS-I | Not available | Not testable | Not available |

## Result

Content preservation passes for OLS-0 through OLS-5. Complete-suite checksum verification is INCOMPLETE because OLS-6 and OLS-I are absent. No post-move checksum exists because Stage 3 and Stage 4 were not executed.

