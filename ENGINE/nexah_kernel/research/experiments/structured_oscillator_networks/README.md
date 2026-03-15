# Structured Oscillator Networks Experiment

This experiment series investigates **structured network topology** and its effects on synchronization dynamics, vortex formation, and phase transitions in coupled oscillator systems. The experiment utilizes **Kuramoto-type models** on customized graph topologies to explore complex phenomena like **hub-cycle structures**, **ring shells**, and **layered symmetry graphs**.

These networks are designed to test how **topology-driven synchronization regimes and vortex structures** emerge within oscillator networks. The research is focused on navigating **resonance networks, phase transitions**, and **chaotic dynamics**, providing valuable insights into high-dimensional dynamical systems.

## Research Motivation

Coupled oscillator systems, particularly Kuramoto-type models, have widespread applications across various fields, including:

- Power grids
- Neural networks
- Biological rhythms
- Chemical oscillators
- Synchronization in complex networks

While most research deals with **random or regular networks**, this study focuses on **intentional, structured topologies** to understand the effects of network structure on synchronization dynamics.

> **Core Research Question:** How does network topology shape synchronization dynamics and vortex structures in oscillator systems?

---

## Experiment Framework

The **Structured Oscillator Networks** experiments are divided into key research themes:

### 1. **Synchronization Dynamics**
   - **Objective:** Study the synchronization behavior of different network topologies.
   - **Quantities Measured:**
     - Global order parameter \( R \)
     - Synchronization time
     - Cluster persistence
   
### 2. **Vortex Formation in Phase Space**
   - **Objective:** Investigate vortex structures within oscillator phase fields.
   - **Metrics:**
     - Vortex persistence
     - Cycle-phase analysis
     - Topological defects detection

### 3. **Topology-Driven Frustration**
   - **Objective:** Examine network sizes and topologies that create **frustration** leading to delayed synchronization or metastable clusters.
   - **Indicators of Frustration:**
     - Synchronization delay
     - Incomplete phase locking
     - Metastable clusters

### 4. **Resonance Structures**
   - **Objective:** Explore resonance patterns within structured graphs, such as:
     - Phase locking channels
     - Resonance webs
     - Synchronization bands

---

## Key Experiments

### **Experiment 01: Hub-Ring Shell Scan**
- **Objective:** Investigate synchronization time as a function of shell size in hub-ring networks.
- **Results:** Measure synchronization time and observe metastability for certain ring sizes.

### **Experiment 02: Vortex Density Mapping**
- **Objective:** Track the formation of phase vortices across different oscillator topologies.
- **Results:** Identify regions where vortex formation coincides with synchronization transitions.

### **Experiment 03: Frustration Shell Detection**
- **Objective:** Detect frustrated networks that fail to synchronize in a timely manner.
- **Results:** Identify network sizes (e.g., N = 29, 34) where synchronization is delayed due to frustration effects.

### **Experiment 04: Layered Cycle Networks**
- **Objective:** Study synchronization dynamics in layered symmetry graphs like C5 + C6 + C6.
- **Results:** Layered topologies enhance synchronization stability under certain conditions.

### **Experiment 05: Resonance Web Detection**
- **Objective:** Detect resonance channels and phase-locking corridors within oscillator networks.
- **Results:** Visualize resonance structures across phase space and detect hidden synchronization patterns.

---

## Visual Outputs

The experiment generates several types of visual outputs that are essential for understanding the system's dynamics:

- **Synchronization Time vs Shell Size Plots**
- **Vortex Density Maps**
- **Phase Field Visualizations**
- **Network State Diagrams**
- **Resonance Field Maps**

### Example Visuals

- **Chimera State Overlap:**
  ![Chimera State](output/chimera_state_overlap.png)
  *Fraction of coherent vs incoherent states across time.*

- **Resonance Lattice (3D Resonance Grid):**
  ![Resonance Lattice](output/resonance_lattice_3d.png)
  *3D visualization of resonance structures in oscillator networks.*

- **Vortex Field Flow:**
  ![Vortex Flow](output/vortex_field_flow.png)
  *Vortex dynamics in a 3D oscillator field.*

- **4D Phase Shift Projection:**
  ![4D Phase Projection](output/4d_phase_shift_projection.png)
  *4D phase shift projections showing resonance dynamics.*

---

## Research Findings

Early results suggest a strong relationship between network topology and synchronization behavior. Observed phenomena include:

- **Rapid synchronization** in balanced symmetry graphs like C5 + C6 + C6.
- **Vortex formation** along cycle boundaries, visible during intermediate synchronization states.
- **Frustration** observed in networks where shell sizes (e.g., N = 29, 34) produce delayed synchronization.
- **Resonance patterns** identified in phase space, linking certain network topologies to stable synchronization zones.

### Example Result: Chimera State Detection

In several experiments, chimera states were detected using local coherence boundaries, revealing the presence of both coherent and incoherent regions within the same system. This aligns with the experimental goal of exploring how different topologies affect synchronization.

---

## Next Steps

- **Larger Shell-Size Scans:** Continue to explore the effects of larger network sizes on synchronization time and frustration.
- **Vortex Density Mapping:** Further analyze the relationship between vortex density and synchronization transitions.
- **Topology-Synchronization Phase Diagrams:** Develop phase diagrams that connect network topologies to their synchronization behaviors.
- **Multi-Layer Oscillator Networks:** Investigate the effects of multi-layer networks on phase transitions and resonance structures.

---

## Relation to NEXAH Kernel

These experiments are part of the **NEXAH Kernel research framework**, which integrates structured oscillator networks, resonance systems, and nonlinear dynamics within the NEXAH system. The insights gained will inform the **resonance detection**, **phase transition modeling**, and **dynamic navigation** capabilities of the NEXAH Kernel.

---

## Running the Experiments

To run a specific experiment, execute the relevant script:

```bash
python ENGINE/nexah_kernel/research/experiments/structured_oscillator_networks/experiment_01/experiment_01_shell_frustration_scan.py
python ENGINE/nexah_kernel/research/experiments/structured_oscillator_networks/experiment_02/vortex_density_mapping.py
python ENGINE/nexah_kernel/research/experiments/structured_oscillator_networks/experiment_03/frustration_shell_detection.py
```

Status

Active exploratory research. Further results will be integrated into the NEXAH Kernel as new findings emerge.

⸻

Key Takeaways

This experiment series explores complex oscillator network behaviors using topologically structured systems. By integrating these findings into the NEXAH Kernel, we aim to enhance dynamic resonance detection, improve phase transition modeling, and contribute to the understanding of synchronization phenomena in complex systems.
