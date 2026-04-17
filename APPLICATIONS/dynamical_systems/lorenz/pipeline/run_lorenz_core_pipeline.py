"""
NEXAH Lorenz Core Pipeline - Fixed Version
Flow → Lyapunov → FTLE → Density → Regimes → Navigation → Visualization
"""

import sys
import os

# === WICHTIG: Repo-Root zum Python-Path hinzufügen ===
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
sys.path.insert(0, repo_root)

# ---------------------------------------------------
# Setup
# ---------------------------------------------------
OUTPUT_DIR = "APPLICATIONS/outputs/lorenz_core"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("\n🧠 Starting NEXAH Lorenz Core Pipeline...\n")

# ---------------------------------------------------
# Safe import helper
# ---------------------------------------------------
def safe_import(module_path, func_name):
    try:
        module = __import__(module_path, fromlist=[func_name])
        func = getattr(module, func_name)
        print(f"✓ Imported {func_name} from {module_path}")
        return func
    except Exception as e:
        print(f"⚠️ Could not import {func_name} from {module_path}: {e}")
        return None


# ---------------------------------------------------
# Load Core Functions
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
    "main"   # oder den tatsächlichen Funktionsnamen, falls anders
)

# ---------------------------------------------------
# Pipeline Execution
# ---------------------------------------------------
data = {}

if run_flow_field:
    print("→ Flow Field")
    data["flow"] = run_flow_field()
else:
    print("❌ Skipping Flow Field")

if run_lyapunov and "flow" in data:
    print("→ Lyapunov Field")
    data["lyap"] = run_lyapunov(data["flow"])
else:
    print("❌ Skipping Lyapunov")

if run_ftle and "lyap" in data:
    print("→ FTLE / Filament Structure")
    data["ftle"] = run_ftle(data["lyap"])
else:
    print("❌ Skipping FTLE")

if run_density and "ftle" in data:
    print("→ Density / Topography")
    data["density"] = run_density(data["ftle"])
else:
    print("❌ Skipping Density")

if run_regimes and "density" in data:
    print("→ Regime Detection")
    data["regimes"] = run_regimes(data["density"])
else:
    print("❌ Skipping Regimes")

if run_navigation and "regimes" in data:
    print("→ Navigation / Control")
    data["nav"] = run_navigation(data["regimes"])
else:
    print("❌ Skipping Navigation")

if run_visualization:
    print("→ Visualization")
    try:
        run_visualization()
    except Exception as e:
        print(f"⚠️ Visualization failed: {e}")
else:
    print("❌ No visualization module found")

print("\n✅ Pipeline finished.\n")
print("Generated data layers:")
for k in data.keys():
    print(f"   • {k}")
