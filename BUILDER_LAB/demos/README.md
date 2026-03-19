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

| Demo                        | Description                                      | Command |
|-----------------------------|--------------------------------------------------|---------|
| **Basic Demo**              | Simple regime landscape navigation                | `python nexah_demo.py` |
| **Explorer**                | Interactive regime landscape explorer             | `python nexah_explorer.py` |
| **Graph Simulation**        | Dynamic state graph + multi-agent navigation      | `python nexah_graph_simulation.py` ||

---

## Want to create your own demo?

Just add a new Python file in this folder and register it in the demo runner. The adapter layer makes it easy to connect any system.


