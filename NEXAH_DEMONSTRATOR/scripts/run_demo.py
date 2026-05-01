"""
NEXAH Demonstrator — Quick Entry

Runs a minimal pipeline:
field → transition structure → navigation behavior
"""

import subprocess
import sys

def run(script):
    print(f"\n▶ Running: {script}\n")
    subprocess.run([sys.executable, script])


if __name__ == "__main__":

    print("⚡ NEXAH Demonstrator — Quick Run")

    # 1. Transition structure
    run("NEXAH_DEMONSTRATOR/scripts/generate_transition_structure.py")

    # 2. Kernel navigation
    run("NEXAH_DEMONSTRATOR/scripts/kernel/nexah_transition_geometry_kernel_mask_v12.py")

    # 3. Optional: Kuramoto or others
    # run("NEXAH_DEMONSTRATOR/scripts/kuramoto/...")

    print("\n✅ Done.")
