"""
NEXAH Chaos Navigator
Lorenz Reference System
"""

from pathlib import Path

OUTPUT_DIR = Path("../../outputs/lorenz_navigation")


def main():

    print("=== NEXAH Chaos Navigator ===")
    print("Lorenz Reference System")
    print()

    print("Running Lorenz navigation analysis...")
    print("Outputs will be written to:", OUTPUT_DIR)

    # später kommen hier die einzelnen Analysen rein
    # FTLE
    # switch corridor
    # return maps
    # symbolic dynamics
    # parameter atlas

    print()
    print("Navigation run complete.")


if __name__ == "__main__":
    main()
