"""
NEXAH Demo — CLEAN VERSION

Shows:
- Lorenz trajectory
- Regime detection
- Density structure (attractor geometry)

This is the CURRENT working demo of NEXAH.
"""

import subprocess
import sys


print("\n🧠 NEXAH Demo Starting\n")


def run(title, cmd):
    print(f"\n{'='*50}")
    print(f"→ {title}")
    print(f"{'='*50}\n")

    try:
        result = subprocess.run(cmd, shell=True)
        if result.returncode != 0:
            print(f"\n⚠️ Step failed: {title}\n")
    except Exception as e:
        print(f"\n❌ Error running step: {title}")
        print(e)


# -----------------------------------
# STEP 1 — Lorenz Visual Pipeline
# -----------------------------------

run(
    "Lorenz System (Trajectory + Regimes)",
    "python -m APPLICATIONS.dynamical_systems.lorenz.pipeline.lorenz_visual_pipeline"
)

# -----------------------------------
# STEP 2 — Attractor Structure (Density)
# -----------------------------------

run(
    "Attractor Structure (Density Map)",
    "python APPLICATIONS/dynamical_systems/lorenz/attractor/lorenz_density_map.py"
)

# -----------------------------------
# STEP 3 — Field (Gradient from Density)
# -----------------------------------

run(
    "Field Approximation (Density Gradient)",
    "python APPLICATIONS/dynamical_systems/lorenz/attractor/lorenz_field_gradient.py"
)

# -----------------------------------
# OPTIONAL — IEEE (later)
# -----------------------------------

# run(
#     "IEEE Power Grid Control",
#     "python APPLICATIONS/power_systems/nexah_ieee9/nexah_closed_loop_ieee9_v6.py"
# )


# -----------------------------------
# DONE
# -----------------------------------

print("\n✅ Demo Complete\n")

print("""
🧭 What you saw:

- A chaotic system (Lorenz)
- Its trajectory structure
- Regime transitions
- Attractor geometry (density)
- A first field approximation (gradient)

----------------------------------------

🧠 Core Idea:

NEXAH does not control systems via targets.

It observes structure,
detects regimes,
reconstructs geometry,
and derives fields from data.

----------------------------------------

🚀 Next Steps:

- Add IEEE demo (real system)
- Connect field layer to nexah/
- Enable true navigation on the field
""")
