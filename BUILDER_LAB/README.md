# ⚡ NEXAH Builder Lab — Demos

Ready-to-run examples that show what NEXAH can do in practice.

This folder contains **interactive demos and simulations** — from simple regime exploration to multi-agent navigation and cascade dynamics.

---

## 🚀 Quick Start

```bash
cd BUILDER_LAB/demos

python nexah_demo.py              # Basic demo
python nexah_explorer.py          # Interactive explorer
python nexah_graph_simulation.py  # Graph + multi-agent navigation
```

Or run the full demo suite:

```bash
python BUILDER_LAB/run_builder_lab.py
```

---

## 🧪 Available Demos

| Demo | Description | File |
|------|------------|------|
| **Basic Demo** | Simple regime landscape navigation | `demos/nexah_demo.py` |
| **Explorer** | Interactive regime landscape explorer | `demos/nexah_explorer.py` |
| **Graph Simulation** | Dynamic state graph + multi-agent navigation | `demos/nexah_graph_simulation.py` |

---

## 🖥️ Additional Tools

| Tool | Description | Location |
|------|------------|----------|
| **Control Room** | Dashboard-style system overview | `dashboards/` |
| **Cascade Visualizer** | Real-time cascade simulation | `visualizers/` |
| **Global System Map** | Planetary-scale visualization | `visualizers/` |

---

## 🎨 Visual Gallery

| Preview | Description |
|---------|-------------|
| ![Cascade](visuals/nexah_cascade.gif) | **Cascade Simulation** – cascading failures |
| ![Explorer](visuals/nexah_explorer_walk.gif) | **Explorer** – regime navigation |
| ![System Walk](visuals/nexah_system_walk.gif) | **System Navigation** – agent movement |
| ![Energy Grid](visuals/energy_grid_walk.gif) | **Energy Grid** – stabilization |
| ![Simulation](visuals/nexah_simulation.gif) | **General Simulation** |

---

## 🧠 What this shows

The demos illustrate:

- systems as **state graphs**
- regime-based system behavior (stable → collapse)
- transitions between system states
- navigation through dynamic structures
- cascade behavior in interconnected systems

---

## 🧩 Create your own demo

Add a new Python file to:

```
BUILDER_LAB/demos/
```

You can connect your own system using the existing structure.

---

## 🧭 CLI Usage

```bash
python BUILDER_LAB/nexah_cli.py demo
python BUILDER_LAB/nexah_cli.py explorer
python BUILDER_LAB/nexah_cli.py systems-list
python BUILDER_LAB/nexah_cli.py create-system my_system
python BUILDER_LAB/nexah_cli.py simulate my_system
```

---

## 🔗 Go deeper

→ **[Extended Documentation](README_extended.md)**  
(architecture, system models, folder structure, future plans)

---

## 🧪 Status

- prototype-level
- exploratory
- focused on system understanding (not production use)

---

## 🧠 Core Idea

NEXAH treats systems as:

> **navigable structures instead of static states**

---

**License**  
Apache 2.0
