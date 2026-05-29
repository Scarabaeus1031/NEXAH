# 🧭 NEXAH Field Navigation Findings

# EXP_01 — Stability Seeking

## Result

A field-guided trajectory was compared to an uncontrolled trajectory.

Observed:

- mean distance uncontrolled: **2.997**
- mean distance guided: **0.705**
- distance reduction: **76.46 %**

---

# 📊 Visual Evidence

## Figure 1 — Navigation Trajectory

![EXP01 Trajectory](./outputs/EXP_01_STABILITY_SEEKING/exp01_navigation_trajectory.png)

The field-guided trajectory remains close to the reconstructed rift structure,
while the uncontrolled trajectory drifts away.

---

## Figure 2 — Distance Evolution

![EXP01 Distance](./outputs/EXP_01_STABILITY_SEEKING/exp01_distance_comparison.png)

Distance to the stability corridor over time.

The guided trajectory maintains a significantly lower distance.

---

## Figure 3 — Summary Dashboard

![EXP01 Summary](./outputs/EXP_01_STABILITY_SEEKING/exp01_navigation_summary.png)

Combined overview of:

- trajectory navigation
- distance evolution
- quantitative comparison

---

## Interpretation

The controller successfully used the reconstructed field as a navigational object.

This demonstrates the feasibility of stability-seeking navigation within a reconstructed field structure.

---

## Status

✅ Passed

---

## Core Insight

```text
Instability is not merely detectable.

It is navigable.
```
# EXP_02 — Corridor Acquisition

![EXP02 Summary](outputs/EXP_02_CORRIDOR_ACQUISITION/exp02_summary_dashboard.png)

## Result

A field-guided controller successfully acquired a stability corridor from a distant initial condition.

Observed:

- Mean distance (uncontrolled): 7.798
- Mean distance (guided): 0.336
- Distance reduction: 95.70 %
- Acquisition step: 27

---

## Corridor Acquisition

![Corridor Acquisition](outputs/EXP_02_CORRIDOR_ACQUISITION/exp02_corridor_acquisition.png)

The guided trajectory starts far from the corridor,
approaches the structure, acquires it, and subsequently
follows the corridor.

---

## Distance Evolution

![Distance Evolution](outputs/EXP_02_CORRIDOR_ACQUISITION/exp02_distance_evolution.png)

The acquisition process becomes visible as a rapid
reduction in distance to the corridor, followed by
stable tracking.

---

## Distance Field Navigation

![Distance Field](outputs/EXP_02_CORRIDOR_ACQUISITION/exp02_distance_field.png)

The reconstructed corridor acts as a navigational
structure embedded within a stability-distance field.

The guided trajectory converges toward the minimum-distance
region and remains attached to the corridor.

---

## Interpretation

The controller successfully:

1. detected the corridor
2. approached the corridor
3. acquired the corridor
4. remained attached to the corridor

This demonstrates that reconstructed field structures can
function as navigational objects rather than passive observations.

---

## Status

✅ Passed


# EXP_03 — Corridor Retention

## Corridor Retention

![Retention Trajectory](outputs/EXP_03_CORRIDOR_RETENTION/exp03_corridor_retention.png)

---

## Distance Recovery After Disturbances

![Distance Recovery](outputs/EXP_03_CORRIDOR_RETENTION/exp03_distance_recovery.png)

---

## Recovery Statistics

![Recovery Statistics](outputs/EXP_03_CORRIDOR_RETENTION/exp03_recovery_statistics.png)

---

## Summary Dashboard

![Summary Dashboard](outputs/EXP_03_CORRIDOR_RETENTION/exp03_summary_dashboard.png)

---

## Results

Mean distance:

**0.353**

Maximum distance:

**4.173**

Corridor occupancy:

**86.29 %**

Mean recovery time:

**10.67 steps**

---

## Interpretation

Three external disturbances were injected into the trajectory.

After each disturbance:

- the trajectory left the corridor
- the controller detected the deviation
- the trajectory re-entered the corridor
- stable navigation resumed

The system maintained corridor occupancy of more than 86%.

---

## Key Finding

The reconstructed field can be used not only for corridor acquisition but also for corridor retention and recovery.

This demonstrates that field-guided navigation remains functional under repeated disturbances.

---

## Status

✅ Passed


# EXP_04 — Collapse Avoidance

## Navigation

![Navigation](./outputs/EXP_04_COLLAPSE_AVOIDANCE/exp04_collapse_navigation.png)

---

## Collapse Distance

![Distance](./outputs/EXP_04_COLLAPSE_AVOIDANCE/exp04_collapse_distance.png)

---

## Collapse Risk

![Risk](./outputs/EXP_04_COLLAPSE_AVOIDANCE/exp04_collapse_risk.png)

---

## Summary Dashboard

![Summary](./outputs/EXP_04_COLLAPSE_AVOIDANCE/exp04_summary_dashboard.png)

## Result

Observed:

- Collapse entries (uncontrolled): 0
- Collapse entries (guided): 0
- Minimum collapse distance (uncontrolled): 1.844
- Minimum collapse distance (guided): 2.775

Risk reduction:

**50.50 %**

## Interpretation

The field-guided controller maintained a significantly larger
distance from the collapse basin than the uncontrolled
trajectory.

While neither trajectory entered the collapse region,
the guided controller increased safety margins by
approximately 50%.

## Status

✅ Passed


# EXP_04B — Collapse Avoidance Stress Test

## Result

A stress-test scenario was created where the collapse basin intersects the natural navigation corridor.

Observed:

- Collapse entries (uncontrolled): 1
- Collapse entries (guided): 1

Minimum collapse distance:

- uncontrolled: 0.362
- guided: 0.480

Risk reduction:

**24.56 %**

Avoidance success:

❌ NO

---

## Navigation

![Navigation](./outputs/EXP_04B_COLLAPSE_AVOIDANCE_STRESS_TEST/exp04b_navigation.png)

The collapse basin was intentionally positioned directly on the natural corridor.

The guided controller follows the corridor successfully but is ultimately forced through the hazardous region.

---

## Collapse Distance

![Collapse Distance](./outputs/EXP_04B_COLLAPSE_AVOIDANCE_STRESS_TEST/exp04b_collapse_distance.png)

The guided controller consistently maintains a larger distance from the collapse basin than the uncontrolled trajectory.

However, the safety margin eventually becomes insufficient due to corridor-basin overlap.

---

## Collapse Entries

![Collapse Entries](./outputs/EXP_04B_COLLAPSE_AVOIDANCE_STRESS_TEST/exp04b_basin_entries.png)

Both trajectories eventually enter the collapse basin.

```text
Uncontrolled: 1 entry
Guided:       1 entry
```

---

## Summary Dashboard

![Summary](./outputs/EXP_04B_COLLAPSE_AVOIDANCE_STRESS_TEST/exp04b_summary_dashboard.png)

---

## Interpretation

This experiment reveals an important limitation of pure corridor-following navigation.

The controller successfully follows the reconstructed field structure.

However:

```text
Corridor Following
≠
Guaranteed Collapse Avoidance
```

when

```text
Corridor ∩ Collapse Basin ≠ ∅
```

In this configuration the safest path is no longer identical to the natural corridor.

---

## Scientific Finding

EXP_04B provides the first indication that field navigation requires a second decision layer:

```text
Corridor Attraction
+
Hazard Repulsion
```

or more generally:

```text
Field Navigation
+
Risk-Aware Navigation
```

---

## Implication for Next Phase

EXP_04B directly motivates:

```text
EXP_05 — Risk-Aware Navigation
```

where navigation is no longer based solely on corridor attraction but also incorporates collapse-risk information.

---

# EXP_05 — Risk-Aware Navigation

## Objective

Evaluate whether a risk-aware NEXAH controller can actively avoid collapse regions by modifying its trajectory before entering a critical basin.

This experiment extends EXP_04B by introducing a dynamic repulsion mechanism that reacts to increasing collapse risk.

---

## Hypothesis

If collapse basins can be detected as geometric risk regions, then a risk-aware controller should:

1. detect proximity to collapse,
2. activate avoidance forces,
3. redirect trajectory,
4. maintain a larger safety distance,
5. avoid basin entry.

---

## Results

| Metric | Uncontrolled | Risk-Aware Guided |
|----------|----------|----------|
| Collapse Entries | 1 | 0 |
| Minimum Collapse Distance | 0.188310 | 2.970839 |
| Avoidance Success | NO | YES |

---

## Key Observation

The uncontrolled trajectory crossed the collapse boundary and entered the collapse basin.

The risk-aware controller detected the approaching basin and activated a repulsion force that redirected the trajectory away from the collapse region.

No collapse basin entry occurred during guided navigation.

---

## Interpretation

This experiment demonstrates active geometric navigation rather than passive corridor following.

The controller does not simply remain on the nominal path.

Instead it:

- monitors collapse proximity,
- estimates risk,
- temporarily leaves the corridor,
- avoids the hazardous region,
- returns to a safe navigation regime.

This behaviour is consistent with the NEXAH concept of field-aware navigation.

---

## Conclusion

EXP_05 provides the first successful demonstration of:

- collapse-aware trajectory modification,
- dynamic risk avoidance,
- active navigation within a stability landscape.

The experiment supports the hypothesis that geometric risk information can be used to improve navigation through complex dynamical environments.

## Status

⚠️ Partial Success

The controller reduces collapse proximity and lowers risk by:

**24.56 %**

but cannot fully avoid collapse when the corridor itself intersects the hazardous region.


## Visual Evidence

### Navigation Behaviour

![Risk Navigation](./outputs/EXP_05_RISK_AWARE_NAVIGATION/exp05_navigation.png)

The guided trajectory actively avoids the collapse basin while the uncontrolled trajectory enters the hazardous region.

---

### Collapse Distance

![Collapse Distance](./outputs/EXP_05_RISK_AWARE_NAVIGATION/exp05_collapse_distance.png)

The guided trajectory maintains a significantly larger distance from the collapse basin throughout the experiment.

---

### Repulsion Force Activation

![Repulsion Force](./outputs/EXP_05_RISK_AWARE_NAVIGATION/exp05_repulsion_force.png)

Repulsion forces activate automatically when collapse risk exceeds the safety threshold.

---

### Summary Dashboard

![Dashboard](./outputs/EXP_05_RISK_AWARE_NAVIGATION/exp05_summary_dashboard.png)

Combined overview of navigation behaviour, collapse distance evolution and avoidance performance.


# EXP_06 + EXP_07 FINDINGS
# IEEE39 TOPOLOGY ↔ DYNAMICS VALIDATION
# NEXAH FIELD NAVIGATION PROGRAM

---
### EXP_06 — IEEE39 COMMUNITY DETECTION
---

Objective
--------------------------------------------------------

Identify natural topological communities
within the IEEE39 network.

Methods

• Louvain Community Detection
• Spectral Clustering
• Modularity Analysis

Results
--------------------------------------------------------

Louvain Communities:

4

Community Sizes:

Community 0 : 15 nodes
Community 1 : 16 nodes
Community 2 : 4 nodes
Community 3 : 4 nodes

Louvain Modularity:

Q = 0.463277

Best Spectral k:

k = 4

Spectral Modularity:

Q = 0.463277

Findings
--------------------------------------------------------

The IEEE39 network exhibits a clear
non-random modular structure.

Both Louvain and Spectral clustering
converge to the same solution:

    4 communities

The agreement between independent
methods suggests a robust partition.

Interpretation
--------------------------------------------------------

The network naturally decomposes into
four topological regions.

No assumptions regarding:

    3
    7
    13

were imposed.

The structure emerged directly
from the graph itself.

Scientific Assessment
--------------------------------------------------------

Community structure is present.

The modularity value:

    Q = 0.463

is sufficiently high to indicate
meaningful clustering.

Status
--------------------------------------------------------

COMMUNITY STRUCTURE DETECTED

Validation: PASSED

Visuals
--------------------------------------------------------

### Visual 1 — IEEE39 Network Structure

![IEEE39 Network Structure](./outputs/EXP_06_IEEE39_COMMUNITY_DETECTION/exp06_network_structure.png)

Raw IEEE39 topology.

---

### Visual 2 — Louvain Communities

![Louvain Communities](./outputs/EXP_06_IEEE39_COMMUNITY_DETECTION/exp06_louvain_communities.png)

Four natural communities detected.

---

### Visual 3 — Spectral Modularity Sweep

![Spectral Modularity Sweep](./outputs/EXP_06_IEEE39_COMMUNITY_DETECTION/exp06_spectral_modularity_sweep.png)

Peak modularity occurs at k = 4.

---

### Visual 4 — Spectral Communities

![Spectral Communities](./outputs/EXP_06_IEEE39_COMMUNITY_DETECTION/exp06_spectral_communities.png)

Independent confirmation of the four-community decomposition.
---

========================================================
EXP_07 — COMMUNITY TO BASIN MAPPING
========================================================

Objective
--------------------------------------------------------

Investigate whether graph communities
correspond to dynamical stability basins.

Question:

    Communities ≟ Basins ?

Results
--------------------------------------------------------

Louvain Communities:

4

Modularity:

Q = 0.463277

Mean Basin Purity:

0.809375

Normalized Mutual Information:

0.412767

Community Purity:

Community 0 : 0.8000
Community 1 : 0.7500
Community 2 : 0.6875
Community 3 : 1.0000

Findings
--------------------------------------------------------

Communities and basins show
non-random alignment.

Community 3 maps completely
to a single basin.

Community 0 and Community 1
show strong basin dominance.

Community 2 displays the
weakest alignment.

Interpretation
--------------------------------------------------------

Community 2 is the most interesting
community in the experiment.

Possible explanations:

1.

Boundary Region

A community positioned
between two basins.


2.

Gate Region

A structural bridge through
which transitions occur.


3.

Transport Corridor

A region that participates
in multiple stability regimes.


The result is consistent with
earlier navigation experiments:

    EXP_05
    EXP_05B

where corridor-based navigation
was observed.

Scientific Assessment
--------------------------------------------------------

Mean Basin Purity:

    0.809

indicates strong correspondence.

NMI:

    0.413

indicates measurable shared
information between topology
and basin assignment.

The result supports the hypothesis:

    Topology
         ↕
    Dynamics

may be coupled.

Important Limitation
--------------------------------------------------------

This experiment uses synthetic basin
assignments for pipeline validation.

Therefore:

    NOT YET

evidence that IEEE39 physical
stability basins correspond to
the detected communities.

Real basin extraction remains
required.

Status
--------------------------------------------------------

PIPELINE VALIDATED

Real IEEE39 Basin Validation Pending

Visuals
--------------------------------------------------------

[### Visual 5 — Community → Basin Overlay

![Community Basin Overlay](exp07_community_basin_overlay.png)

Overlay between community membership and basin assignment.

---

Observation:

Communities show dominant
basin occupancy.

---

### Visual 6 — Dynamical Basin Assignment

![Dynamical Basin Assignment](exp07_basin_map.png)

Stable, transition and collapse regions projected onto the graph.

---

### Visual 7 — Community ↔ Basin Alignment Matrix

![Community Basin Alignment](exp07_alignment_matrix.png)

Alignment between graph communities and basin occupancy.

Community ↔ Basin Alignment Matrix

Strong diagonal structure.

Most communities map predominantly
into a single dynamical basin.

Community 3:

    purity = 1.000

showing a nearly perfect correspondence
between graph topology and dynamical behavior.

Community 2:

    purity = 0.6875

showing the weakest alignment.

This community appears to span
multiple basins and may contain
transition states, corridor nodes,
or gate-like structures linking
different dynamical regimes.

The result suggests that
communities and basins are related,
but not identical.

Graph topology captures part of the
dynamical structure, while basin
membership contains additional
state-space information.

========================================================
COMBINED CONCLUSION
========================================================

EXP_06 established:

    IEEE39 contains
    4 natural communities.

EXP_07 established:

    Communities and basins
    are not randomly related.

Current evidence suggests:

    Communities may contain
    dynamical information.

The strongest candidate for future
investigation is:

    Community 2

which may represent:

    Basin Boundary
    Gate Region
    Transport Corridor

Next Step
--------------------------------------------------------

EXP_07B_REAL_IEEE39_BASIN_MAPPING

Question:

    Are communities actually
    stability basins?

or

    Are communities gates
    between stability basins?

This remains the central open
question following EXP_06
and EXP_07.




## Visuals



### Visual 2 — Louvain Communities

![Louvain Communities](exp06_louvain_communities.png)

Four natural communities detected.

---

### Visual 3 — Spectral Modularity Sweep

![Spectral Modularity Sweep](exp06_spectral_modularity_sweep.png)

Peak modularity occurs at k = 4.

---

### Visual 4 — Spectral Communities

![Spectral Communities](exp06_spectral_communities.png)

Independent confirmation of the four-community decomposition.

---

### Visual 5 — Community → Basin Overlay

![Community Basin Overlay](./outputs/EXP_07_COMMUNITY_TO_BASIN_MAPPING/exp07_community_basin_overlay.png)

Overlay between community membership and basin assignment.

---

### Visual 6 — Dynamical Basin Assignment

![Dynamical Basin Assignment](./outputs/EXP_07_COMMUNITY_TO_BASIN_MAPPING/exp07_basin_map.png)

Stable, transition and collapse regions projected onto the graph.

---

### Visual 7 — Community ↔ Basin Alignment Matrix

![Community Basin Alignment](./outputs/EXP_07_COMMUNITY_TO_BASIN_MAPPING/exp07_alignment_matrix.png)

Alignment between graph communities and basin occupancy.
