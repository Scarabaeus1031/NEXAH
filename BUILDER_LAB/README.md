# Builder Lab Demos

Ready-to-run examples that show what NEXAH can do in practice.

This folder contains interactive demos — from simple regime exploration to complex multi-agent stabilization and cascade visualization.

### Quick Start

```bash
cd BUILDER_LAB/demos
python nexah_demo.py              # Basic demo
python nexah_explorer.py          # Interactive explorer
python nexah_graph_simulation.py  # Graph + multi-agent navigation
```
### Available Demos

| Demo                        | Description                                              | File |
|-----------------------------|----------------------------------------------------------|------|
| **Basic Demo**              | Simple regime landscape navigation                       | `nexah_demo.py` |
| **Explorer**                | Interactive regime landscape explorer                    | `nexah_explorer.py` |
| **Graph Simulation**        | Dynamic state graph + multi-agent navigation             | `nexah_graph_simulation.py` |
| **Control Room**            | Dashboard-style overview of system stability             | `nexah_control_room.py` |
| **Cascade Visualizer**      | Real-time cascade failure simulation                     | `nexah_cascade_visualizer.py` |
| **Global System Map**       | Planetary-scale system visualization                     | `nexah_global_system_map.py` |

### Visual Gallery

Here are some highlights from the demos — see NEXAH in action:

| Preview | Description |
|---------|-------------|
| ![Cascade](visuals/nexah_cascade.gif) | **Cascade Simulation** – Real-time cascading failures |
| ![Explorer](visuals/nexah_explorer_walk.gif) | **Explorer** – Interactive regime landscape navigation |
| ![System Walk](visuals/nexah_system_walk.gif) | **System Navigation** – Agent moving through state space |
| ![Energy Grid](visuals/energy_grid_walk.gif) | **Energy Grid** – Stabilizing a power grid under stress |
| ![Simulation](visuals/nexah_simulation.gif) | **General Simulation** – Overview of NEXAH dynamics |

### Want to create your own demo?

Just add a new Python file in this folder. The adapter layer makes it easy to connect any system.

### Want to go deeper?

→ **[Extended Documentation](../README_extended.md)**  
(full architecture, system models, folder structure and future plans)

---

**License**  
Apache 2.0
