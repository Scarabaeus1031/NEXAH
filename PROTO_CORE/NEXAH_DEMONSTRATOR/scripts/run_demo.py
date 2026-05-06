"""
NEXAH Demonstrator — Quick Entry

Runs a minimal pipeline:
field → transition structure → navigation behavior
"""

import subprocess
import sys
import os


# ============================
# Helper
# ============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def run(script_rel_path):
    script_path = os.path.join(BASE_DIR, script_rel_path)

    print(f"\n▶ Running: {script_rel_path}\n")

    try:
        subprocess.run([sys.executable, script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error while running {script_rel_path}")
        print(e)
        sys.exit(1)


# ============================
# Main
# ============================

if __name__ == "__main__":

    print("⚡ NEXAH Demonstrator — Quick Run")

    # 1. Transition structure (discrete layer)
    run("generate_transition_structure.py")

    # 2. Kernel / gate field (continuous layer)
    run("kernel/nexah_transition_geometry_kernel_mask_v12.py")

    # 3. HERO — transition-aware navigation (v13)
    run("hero/run_transition_navigation_v13.py")

    print("\n✅ All steps completed.")
