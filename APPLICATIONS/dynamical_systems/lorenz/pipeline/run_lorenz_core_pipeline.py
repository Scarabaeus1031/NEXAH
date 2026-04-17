"""
NEXAH Demo — CLEAN VERSION

Shows:
- Lorenz trajectory
- Regime detection
- Visual outputs

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
- A first step toward field-based interpretation

----------------------------------------

🧠 Core Idea:

NEXAH does not control systems via targets.

It observes structure,
detects regimes,
and prepares navigation within the system.

----------------------------------------

🚀 Next Steps:

- Add IEEE demo (real system)
- Connect field layer
- Introduce true navigation
""")
