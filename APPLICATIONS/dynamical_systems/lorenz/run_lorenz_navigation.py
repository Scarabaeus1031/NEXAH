"""
NEXAH Chaos Navigator
Lorenz Reference System
"""

import argparse
from pathlib import Path

# real analysis modules
from analysis.lorenz_ftle_map import main as run_ftle
from regimes.lorenz_regime_map import main as run_regime


OUTPUT_DIR = Path("../../outputs/lorenz_navigation")


def run_all():

    print("Running full Lorenz navigation pipeline...")
    print("Outputs:", OUTPUT_DIR)
    print()

    print("[1/2] FTLE chaos structure")
    run_ftle()

    print()
    print("[2/2] Regime structure map")
    run_regime()


def run_ftle_only():

    print("Running FTLE chaos structure analysis")
    run_ftle()


def run_regime_only():

    print("Running regime structure analysis")
    run_regime()


def main():

    parser = argparse.ArgumentParser(
        description="NEXAH Chaos Navigator (Lorenz)"
    )

    parser.add_argument(
        "--mode",
        choices=["all", "ftle", "regime"],
        default="all"
    )

    args = parser.parse_args()

    print()
    print("=== NEXAH Chaos Navigator ===")
    print("Lorenz Reference System")
    print()

    if args.mode == "all":
        run_all()

    elif args.mode == "ftle":
        run_ftle_only()

    elif args.mode == "regime":
        run_regime_only()

    print()
    print("Done.")


if name == "main":
    main()
