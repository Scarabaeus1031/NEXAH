"""
NEXAH Demo Entry Point

This script demonstrates the core idea of NEXAH:

dynamics → structure → field → navigation

Includes:
- Lorenz Core Pipeline (full system)
- Lorenz Visual Demo (quick understanding)

Run:
python run_nexah_demo.py
"""

import subprocess
import os

print("\n🧠 NEXAH — Demo Starting\n")

# ---------------------------------------------------
# Helper
# ---------------------------------------------------

def run_step(name, command):
    print(f"\n{'='*50}")
    print(f"→ {name}")
    print(f"{'='*50}\n")

    try:
        subprocess.run(command, shell=True, check=True)
    except Exception as e:
        print(f"⚠️ Step failed: {e}")


# ---------------------------------------------------
# STEP 1 — Lorenz Core (REAL SYSTEM)
# ---------------------------------------------------

run_step(
    "Lorenz Core Pipeline (structure → field → regimes → navigation)",
    "python -m APPLICATIONS.dynamical_systems.lorenz.pipeline.run_lorenz_core_pipeline"
)

# ---------------------------------------------------
# STEP 2 — Lorenz Quick Visual (INTUITION)
# ---------------------------------------------------

run_step(
    "Lorenz Visual Demo (quick intuition)",
    "python -m APPLICATIONS.dynamical_systems.lorenz.pipeline.lorenz_visual_pipeline"
)

# ---------------------------------------------------
# OPTIONAL — IEEE (later)
# ---------------------------------------------------

# run_step(
#     "IEEE Power Grid Demo",
#     "python APPLICATIONS/power_systems/nexah_ieee9/nexah_closed_loop_ieee9_v6.py"
# )

# ---------------------------------------------------
# DONE
# ---------------------------------------------------

print("\n✅ NEXAH Demo Completed\n")

print("""
🧭 What you just saw:

1. Lorenz Core Pipeline
   → Chaos becomes structure
   → Structure becomes geometry
   → Geometry becomes navigable

2. Lorenz Visual Demo
   → Trajectories
   → Regimes
   → Field-aware interpretation

----------------------------------------

🧠 Core Idea:

You are not controlling the system.

You are navigating the geometry
that the system unfolds.

----------------------------------------

🚀 Next:
- Explore APPLICATIONS/
- Try IEEE demo
- Dive into nexah/ core modules
""")
