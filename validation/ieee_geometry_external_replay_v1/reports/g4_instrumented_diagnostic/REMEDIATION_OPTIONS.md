# Remediation options

These options are separated from the diagnostic evidence. None is authorised by
the instrumented replay.

| Option | Implementation | Environment contract | Serialization contract | Gate semantics | Scientific claims |
|---|---|---|---|---|---|
| Preserve the failed G4 result and diagnostic package without further work | no | no | no | no | no |
| Extend the environment identity to binary wheel/conda hashes, BLAS/LAPACK, numba state, thread settings and transitive lock | tooling only | **yes** | no | no | no |
| Reconstruct the original canonical binary environment and run a separately authorised replay | tooling/setup | **yes** | no | no | no |
| Make pandapower execution-path selection explicit, including numba state and thread controls | possibly | **yes** | no | no | no |
| Retain intermediate payloads and recursive diffs in future replay gates | diagnostic implementation | no | no | no | no |
| Define a canonical float-serialization representation | **yes** | no | **yes** | possibly | no unless retained precision changes |
| Replace exact payload equality with a numerical acceptance rule | gate implementation | possibly | no | **yes** | potentially |
| Regenerate the frozen canonical artifacts in a newly selected environment | **yes** | **yes** | possibly | **yes** | potentially |

No tolerance, rounding, canonical regeneration, gate relaxation or environment
tuning is recommended from this diagnostic alone.

Recommended decision: preserve the present evidence and keep G4 failed. If
portability work is later authorised, first define whether the intended
contract is exact binary-environment replay or scientifically justified
numerical reproducibility. That is a governance decision outside this
diagnostic package.

