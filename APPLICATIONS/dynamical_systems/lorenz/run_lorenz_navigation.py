"""
NEXAH Chaos Navigator
Lorenz Reference System
"""

import argparse
from pathlib import Path


OUTPUT_DIR = Path("../../outputs/lorenz_navigation")


def run_all():

    print("Running full Lorenz navigation pipeline...")
    print("Outputs:", OUTPUT_DIR)

    # später werden hier echte Analysen aufgerufen
    print("FTLE analysis")
    print("Switch corridor detection")
    print("Return map reconstruction")
    print("Symbolic dynamics")
    print("Parameter atlas")


def run_ftle():

    print("Running FTLE map generation")


def run_switch():

    print("Running switch corridor detection")


def main():

    parser = argparse.ArgumentParser(
        description="NEXAH Chaos Navigator (Lorenz)"
    )

    parser.add_argument(
        "--mode",
        choices=["all", "ftle", "switch"],
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
        run_ftle()

    elif args.mode == "switch":
        run_switch()

    print()
    print("Done.")


if __name__ == "__main__":
    main()
