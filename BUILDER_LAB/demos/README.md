# Builder Lab Demos

Ready-to-run examples that show what NEXAH can do.

This folder contains practical demos that let you instantly see NEXAH in action — from simple oscillator synchronization to complex system stabilization.

### Quick Start

Make sure NEXAH is installed:

```bash
pip install -e .
```

Then run any demo with:
```bash
python -m nexah demo <name>
```
### Available Demos

| Demo                          | Description                                              | File |
|-------------------------------|----------------------------------------------------------|------|
| **Basic Demo**                | Simple regime landscape navigation                       | `nexah_demo.py` |
| **Explorer**                  | Interactive regime landscape explorer                    | `nexah_explorer.py` |
| **Graph Simulation**          | Dynamic state graph + multi-agent navigation             | `nexah_graph_simulation.py` |
| **Control Room**              | Dashboard-style overview of system stability             | `nexah_control_room.py` |
| **Cascade Visualizer**        | Real-time cascade failure simulation                     | `nexah_cascade_visualizer.py` |
| **Global System Map**         | Planetary-scale system visualization                     | `nexah_global_system_map.py` |

**Tipp:** Alle Demos können direkt aus dem BUILDER_LAB-Ordner gestartet werden.

---

## Want to create your own demo?

Just add a new Python file in this folder and register it in the demo runner. The adapter layer makes it easy to connect any system.


