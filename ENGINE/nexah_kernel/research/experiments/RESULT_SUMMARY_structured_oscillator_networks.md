# Results of Structured Oscillator Networks Experiment

This gallery provides a comprehensive view of the **Structured Oscillator Networks** experiment results. The visuals are organized based on key experiment themes such as synchronization dynamics, vortex formation, resonance structures, and the influence of prime number grids on oscillator network behavior. Each section below represents findings from a specific experiment, with corresponding Python scripts and the visuals they generated.

⸻

## 1. Synchronization Dynamics

This section explores the synchronization behavior of oscillator networks across various shell sizes and topologies.

### Synchronization Time vs Shell Size (Version 1)  
![Synchronization Time vs Shell Size](output/sync_time_vs_shell.png)  
*This visualization shows the synchronization time as a function of shell size, exploring the impact of network shell sizes on synchronization time.*

### Synchronization Time vs Shell Size (Version 2)  
![Synchronization Time vs Shell Size (Version 2)](output/sync_time_vs_shell_v2.png)  
*An extended version of this visualization, offering additional data on synchronization dynamics across more complex shell structures.*

> **Explanation:** These visuals help us understand how shell size and the number of nodes in a ring network influence the time it takes for oscillators to synchronize. They also investigate the impact of different shell sizes (N) on synchronization delays caused by frustration effects.

**Python Script Used:**  
[`experiment_01_shell_frustration_scan.py`](ENGINE/nexah_kernel/research/experiments/structured_oscillator_networks/experiment_01/experiment_01_shell_frustration_scan.py)

---

## 2. Vortex Formation in Phase Space

This section focuses on vortex formation in phase space within oscillator networks. The following visuals track the development of these vortex structures, offering insights into synchronization transitions and chaotic behavior.

### Vortex Density Mapping (Version 1)  
![Vortex Density Mapping](output/vortex_density_vs_shell.png)  
*This mapping visualizes the vortex density in phase space across different shell sizes, highlighting the regions where vortex formation and synchronization transitions coincide.*

### Vortex Density Mapping (Version 2)  
![Vortex Density Mapping (Version 2)](output/vortex_density_vs_shell_v2.png)  
*The second version of this visualization extends the analysis to additional shell sizes, providing further insight into vortex distribution and its correlation with synchronization states.*

> **Explanation:** These mappings show how vortex structures emerge in various oscillator network topologies. By visualizing the density and distribution of these vortices, we can analyze how they are related to synchronization transitions, particularly at certain network shell sizes.

**Python Script Used:**  
[`phase_vortex_detector.py`](ENGINE/nexah_kernel/research/experiments/structured_oscillator_networks/phase_vortex_detector.py)

---

## 3. Resonance Structures

This section delves into resonance patterns within the structured oscillator networks. It focuses on how phase-locking channels, resonance webs, and synchronization bands emerge within these complex networks.

### Resonance Field Map  
![Resonance Field Map](output/resonance_field_map.png)  
*This visualization displays the resonance fields within the network, showing regions where oscillators exhibit synchronized behavior in phase space.*

### Resonance Field Strength  
![Resonance Field Strength](output/resonance_field_strength.png)  
*Shows the strength of the resonance fields, giving insights into how the resonance structures evolve across different network configurations.*

> **Explanation:** Resonance structures are crucial for understanding synchronization in complex networks. These visuals reveal how and where resonance channels and synchronization bands form, demonstrating their role in the overall network synchronization.

**Python Script Used:**  
[`resonance_band_tracker.py`](ENGINE/nexah_kernel/research/experiments/structured_oscillator_networks/resonance_band_tracker.py)

---

## 4. Prime Number Grids Experiments

In addition to the above experiments, the **Prime Number Grid** experiments investigate how **Prime Number Lattices** impact the dynamics of oscillator networks. These experiments focus on resonance patterns within **prime-based grids**, and their potential to influence synchronization and chaotic transitions.

### Prime Number Lattice with Symmetry  
![Prime Lattice Symmetry](output/Prime_Number_Lattice_with_Symmetry.png)  
*This visual shows a 3D resonance lattice based on prime number structures.*

### Resonance Lattice 3D  
![Resonance Lattice 3D](output/Resonance_Lattice_3D.png)  
*Visual representation of resonance structures within the prime number grid.*

### Prime Number Grid Visualization (fixed Y-axis)  
![Prime Number Grid](output/grid_prime_visualization_1000.png)  
*Prime-based grid with a fixed Y-axis – illustrating symmetry and phase distribution.*

**Python Script Used:**  
[`Prime_Number_Grid_with_RGB.py`](ENGINE/nexah_kernel/research/experiments/structured_oscillator_networks/Prime_Number_Grid_with_RGB.py)

---

## Additional Visualizations

These visuals provide further insights into the phase structures and defect statistics in oscillator networks.

### Chimera State Overlap  
![Chimera State Overlap](output/chimera_state_overlap.png)  
*This image illustrates the fraction of coherent versus incoherent states in a network over time, revealing the chimera state phenomenon.*

### Phase Surface 3D  
![Phase Surface 3D](output/phase_surface_3d.png)  
*3D-phase surface derived from oscillator dynamics.*

### Triad Defect Distance Histogram  
![Triad Defect Distance](output/triad_defect_distance_hist.png)  
*Histogram showing the distances between triadic defects.*

### Vortex Count vs Time  
![Vortex Count](output/vortex_count_vs_time.png)  
*Graph showing the number of active vortex structures over time.*

### Wave Coherence  
![Wave Coherence](output/wave_coherence.png)  
*Shows the coherence of wave propagation across the network.*

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

## Relation to NEXAH Kernel

These experiments serve as a **core testbed** for the NEXAH Kernel (ENGINE/nexah_kernel). They validate and extend key concepts:

- **Resonance Detection & Operators** (Ω-Projektion): Prime-Grids & Resonance-Webs liefern Metriken für Resonanzkanäle & Locking-Bänder
- **Regime Partitioning & Tipping Points**: Vortex- & Chimera-Detektion (core/) als Basis für Basin-Boundaries & Instabilitäts-Indikatoren
- **Frustration & Risk Geometry**: Shell-Frustration-Scans (topology/) als Proxy für Cascade-Risiken & Delayed Transitions
- **Topology as Relational Order** (META → ARCHY): Strukturierte Topologien testen, wie relationale Ordnung Regime-Landschaften formt
- **Export & Integration**: Alle relevanten Metriken (Vortex-Dichte, Sync-Time, Resonance-Score, Frustration-Level) werden über `kernel_bridge.py` exportiert und in Navigation-Layer (NEXAH) integriert

→ Die Experimente sind **kein isoliertes Toy-Modell**, sondern direkte Vorarbeit für finite, navigierbare Regime-Analyse in komplexen Systemen.

---

## Running the Experiments

The experiments are modularized in Python scripts. Here are a few examples:

```bash
# Shell-Frustration-Scan starten
python -m topology.shell_frustration_scan

# Vortex-Dichte visualisieren
python -m visualization.vortex_topology_map

# Resonance-Lattice berechnen & plotten
python -m resonance.resonance_lattice_3D

# Via Kernel-Bridge (zukünftig)
from .kernel_bridge import extract_regime_metrics
```

## Status

Active exploratory research. Further results will be integrated into the NEXAH Kernel as new findings emerge.
