"""
NEXAH Lorenz Core Pipeline

Full structural pipeline:

Flow → Lyapunov → FTLE → Density → Regimes → Navigation → Visualization

This is the REAL core of the Lorenz module (not just a demo).

Outputs are stored in:
APPLICATIONS/outputs/lorenz_core/
"""

import os

# ---------------------------------------------------
# Setup
# ---------------------------------------------------

OUTPUT_DIR = "APPLICATIONS/outputs/lorenz_core"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("\n🧠 Starting NEXAH Lorenz Core Pipeline...\n")

# ---------------------------------------------------
# Safe import helper (prevents crashes)
# ---------------------------------------------------

def safe_import(module_path, func_name):
    try:
        module = __import__(module_path, fromlist=[func_name])
        return getattr(module, func_name)
    except Exception as e:
        print(f"⚠️ Could not import {func_name} from {module_path}: {e}")
        return None


# ---------------------------------------------------
# Load Core Functions (with fallbacks)
# ---------------------------------------------------

run_flow_field = safe_import(
    "APPLICATIONS.dynamical_systems.lorenz.analysis.lorenz_flow_vector_field",
    "run_flow_field"
)

run_lyapunov = safe_import(
    "APPLICATIONS.dynamical_systems.lorenz.analysis.lorenz_lyapunov_field",
    "run_lyapunov"
)

run_ftle = safe_import(
    "APPLICATIONS.dynamical_systems.lorenz.analysis.lorenz_ftle_filament_graph",
    "run_ftle"
)

run_density = safe_import(
    "APPLICATIONS.dynamical_systems.lorenz.landscapes.lorenz_density_map",
    "run_density"
)

run_regimes = safe_import(
    "APPLICATIONS.dynamical_systems.lorenz.regimes.lorenz_regime_map",
    "run_regime_map"
)

run_navigation = safe_import(
    "APPLICATIONS.dynamical_systems.lorenz.navigation.lorenz_gradient_controller",
    "run_navigation"
)

run_visualization = safe_import(
    "APPLICATIONS.dynamical_systems.lorenz.pipeline.lorenz_visual_pipeline",
    "main"  # fallback: reuse existing visual pipeline
)


# ---------------------------------------------------
# Pipeline Execution
# ---------------------------------------------------

data = {}

# 1. Flow Field
if run_flow_field:
    print("→ Flow Field")
    data["flow"] = run_flow_field()
else:
    print("❌ Skipping Flow Field")

# 2. Lyapunov
if run_lyapunov:
    print("→ Lyapunov Field")
    data["lyap"] = run_lyapunov(data.get("flow"))
else:
    print("❌ Skipping Lyapunov")

# 3. FTLE
if run_ftle:
    print("→ FTLE / Filament Structure")
    data["ftle"] = run_ftle(data.get("lyap"))
else:
    print("❌ Skipping FTLE")

# 4. Density / Topography
if run_density:
    print("→ Density / Topography")
    data["density"] = run_density(data.get("ftle"))
else:
    print("❌ Skipping Density")

# 5. Regimes
if run_regimes:
    print("→ Regime Detection")
    data["regimes"] = run_regimes(data.get("density"))
else:
    print("❌ Skipping Regimes")

# 6. Navigation
if run_navigation:
    print("→ Navigation / Control")
    data["nav"] = run_navigation(data.get("regimes"))
else:
    print("❌ Skipping Navigation")

# 7. Visualization
if run_visualization:
    print("→ Visualization")
    try:
        run_visualization()
    except Exception as e:
        print(f"⚠️ Visualization fallback failed: {e}")
else:
    print("❌ No visualization module found")


# ---------------------------------------------------
# Done
# ---------------------------------------------------

print("\n✅ Pipeline finished.\n")

print("Generated data layers:")
for k in data.keys():
    print(f" - {k}")
