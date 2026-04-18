"""
NEXAH — ROOT DEMO

Run the full NEXAH demonstration pipeline:

1. Lorenz structure (trajectory + regimes)
2. Attractor density (geometry)
3. Field approximation (gradient)
4. Coherence + risk dynamics (control demo)

This is the official entry point.
"""

import subprocess

print("\n🧠 NEXAH ROOT DEMO\n")


def run(title, cmd):
    print(f"\n{'='*60}")
    print(f"→ {title}")
    print(f"{'='*60}\n")

    subprocess.run(cmd, shell=True)


# --------------------------------------------------
# 1. STRUCTURE
# --------------------------------------------------

run(
    "Lorenz System (Trajectory + Regimes)",
    "python -m APPLICATIONS.dynamical_systems.lorenz.pipeline.lorenz_visual_pipeline"
)

# --------------------------------------------------
# 2. GEOMETRY
# --------------------------------------------------

run(
    "Attractor Geometry (Density)",
    "python APPLICATIONS/dynamical_systems/lorenz/attractor/lorenz_density_map.py"
)

# --------------------------------------------------
# 3. FIELD
# --------------------------------------------------

run(
    "Field Approximation (Gradient)",
    "python APPLICATIONS/dynamical_systems/lorenz/attractor/lorenz_field_gradient.py"
)

# --------------------------------------------------
# 4. DYNAMICS (COHERENCE / RISK)
# --------------------------------------------------

run(
    "Dynamics Layer (Coherence + Risk)",
    "python APPLICATIONS/core_demos/lorenz/scripts/lorenz_nexah_demo_v3_v4.py"
)

# --------------------------------------------------
# DONE
# --------------------------------------------------

print("\n✅ NEXAH DEMO COMPLETE\n")

print("""
🧭 What you saw:

1. STRUCTURE
   → chaotic attractor + regimes

2. GEOMETRY
   → density → shape of the system

3. FIELD
   → gradient → proto-navigation field

4. DYNAMICS
   → coherence + risk
   → control emerges from structure

----------------------------------------

🧠 Core Insight:

NEXAH does not impose control.

It:
- observes structure
- reconstructs geometry
- derives fields
- enables navigation

----------------------------------------

🚀 Next Steps:

- connect field → navigation engine
- introduce instability (phase breaker)
- test on real systems (IEEE)

""")
