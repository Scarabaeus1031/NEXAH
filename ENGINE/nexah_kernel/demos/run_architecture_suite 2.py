"""
NEXAH Architecture Demo Suite

Runs all architecture-related demos sequentially.

Usage:

python -m ENGINE.nexah_kernel.demos.run_architecture_suite
"""

import subprocess
import sys


DEMOS = [

    "demo_architecture_landscape_3D",
    "demo_architecture_flow_density",
    "demo_architecture_flow_field",
    "demo_architecture_flow_rivers_3D",

    "demo_architecture_morse_complex",
    "demo_architecture_morse_smale_map",

    "demo_architecture_stability_landscape",
    "demo_architecture_phase_diagram",
    "demo_architecture_transition_map",

    "demo_architecture_navigation_graph",
    "demo_architecture_attractor_map",
    "demo_architecture_regime_detection",

    "demo_architecture_ridge_detector",
    "demo_architecture_search",
    "demo_architecture_optimizer",

]


def run():

    print("\n==============================")
    print("NEXAH Architecture Demo Suite")
    print("==============================\n")

    for demo in DEMOS:

        module = f"ENGINE.nexah_kernel.demos.architecture.{demo}"

        print(f"\nRunning {demo}\n")

        subprocess.run(
            [sys.executable, "-m", module],
            check=False
        )

    print("\nAll architecture demos finished.\n")


if __name__ == "__main__":
    run()
