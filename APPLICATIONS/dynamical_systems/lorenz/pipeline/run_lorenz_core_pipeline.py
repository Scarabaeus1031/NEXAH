"""
NEXAH Demo — CLEAN VERSION

Shows:
- Lorenz trajectory
- Regime detection
- Density structure (attractor geometry)

This is the CURRENT working demo of NEXAH.
"""

import subprocess

print("\n🧠 NEXAH Demo Starting\n")


def run(title, cmd):
    print(f"\n{'='*50}")
    print(f"→ {title}")
    print(f"{'='*50}\n")

    subprocess.run(cmd, shell=True)


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
- Attractor geometry via density mapping

----------------------------------------

🧠 Core Idea:

NEXAH does not control systems via targets.

It observes structure,
detects regimes,
and reconstructs geometry —
preparing navigation within the system.

----------------------------------------

🚀 Next Steps:

- Add IEEE demo (real system)
- Introduce field layer (from density)
- Enable navigation within the field
""")
