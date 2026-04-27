# NEXAH — Halvorsen Build Log
============================================================

Status: ACTIVE
System: Halvorsen Attractor (Coarse → Control Pipeline)

------------------------------------------------------------
0. RAW SYSTEM
------------------------------------------------------------

Simulation + Attractor

![Halvorssen Attractor](outputs/halvorsen_attractor_20260427_014720.png)

→ Continuous chaotic system
→ No discrete structure yet


------------------------------------------------------------
1. TRANSITION EXTRACTION
------------------------------------------------------------

![Transition Matrix](outputs/transition_matrix_20260427_015925.png)

→ Discretization of flow
→ Probabilistic transition graph


------------------------------------------------------------
2. MASS CONSERVATION CHECK
------------------------------------------------------------

![Mass Conservation](outputs/mass_conservation_20260427_015614.png)

→ Row normalization valid
→ Markov structure confirmed


------------------------------------------------------------
3. COARSE GRAINING
------------------------------------------------------------

![Coarse Matrix](outputs/coarse_matrix_20260427_022349.png)

→ Collapse into basins
→ Emergent diagonal structure

Key observation:
- quasi-chain + weak off-diagonal jumps


------------------------------------------------------------
4. GATE DETECTION
------------------------------------------------------------

![Gates](outputs/gates_20260427_022645.png)

→ rare transitions identified
→ “escape channels”

Example:
- 10 → 9 (rel = 1.0)
- multiple ~0.33 structures


------------------------------------------------------------
5. GATE GRAPH
------------------------------------------------------------

![Gate Graph](outputs/gate_graph_20260427_023206.png)

→ sparse control skeleton
→ directional switching structure

Interpretation:
- local cycles
- partial reversibility


------------------------------------------------------------
6. PATH PLANNING (FAILED)
------------------------------------------------------------

→ No global path found
→ system fragmented


------------------------------------------------------------
7. REACHABILITY ANALYSIS
------------------------------------------------------------

![Reachability](outputs/reachability_20260427_024039.png)

→ multiple disconnected regions

Detected components:
- upper basin
- middle cyclic region
- lower terminal region


------------------------------------------------------------
8. COMPONENT CONNECTION (MANUAL CONTROL)
------------------------------------------------------------

![Connected Matrix](outputs/connected_matrix_20260427_024610.png)

Bridges added:
- 5 → 3
- 14 → 9
- 11 → 15

→ minimal intervention strategy


------------------------------------------------------------
9. GLOBAL POLICY (TARGET = 15)
------------------------------------------------------------

![Global Policy](outputs/global_policy_20260427_024840.png)

→ only partial reachability

Key region:
- 9 → 17 → 15 funnel


------------------------------------------------------------
10. ADAPTIVE BRIDGING
------------------------------------------------------------

![Adaptive Matrix](outputs/adaptive_matrix_20260427_025214.png)

→ data-driven bridge suggestion
→ smoother connectivity

Key edges:
- 2 → 3
- 6 → 7
- 12 → 10


------------------------------------------------------------
11. POLICY GRADIENT (LEARNING)
------------------------------------------------------------

![Policy Gradient](outputs/policy_gradient_success_20260427_025829.png)

→ learning improves success slightly (~0.11 → ~0.23)

![Learned Policy](outputs/policy_gradient_matrix_20260427_025829.png)

→ distributed policy (not deterministic chain)


------------------------------------------------------------
12. GATE-AWARE POLICY
------------------------------------------------------------

![Gate Policy Matrix](outputs/gate_aware_policy_matrix_20260427_025844.png)

![Policy Delta](outputs/gate_aware_policy_delta_20260427_025844.png)

→ emphasizes critical transitions
→ suppresses noise transitions

Effect:
- sharper control directions
- stronger structure along gates


------------------------------------------------------------
13. FLOW DECOMPOSITION (DUAL VIEW)
------------------------------------------------------------

![Dual System](outputs/dual_system_overlay_20260427_030748.png)

Comparison:

Lorenz-like:
- discrete switching
- few strong edges

Halvorsen:
- distributed cyclic flow
- many medium edges

Metrics:

Halvorsen:
- diag ≈ 0.635
- offdiag ≈ 0.365
- gates = 21

Lorenz:
- diag ≈ 0.6
- gates = 4


------------------------------------------------------------
GLOBAL INTERPRETATION
------------------------------------------------------------

Halvorsen is NOT:
→ a regime-switch system

Halvorsen IS:
→ a distributed cyclic transport system
→ with embedded local gate structures
→ requiring active intervention for global navigation

Key insight:
- control ≠ path finding
- control = restructuring flow topology


------------------------------------------------------------
NEXT STEPS
------------------------------------------------------------

[ ] Full pipeline runner
[ ] Cross-system embedding (Lorenz ↔ Halvorsen)
[ ] Continuous-space control injection
[ ] Real system application (grid / ecosystem)


============================================================
END OF LOG
============================================================
