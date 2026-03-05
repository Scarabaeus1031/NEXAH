# ==========================================================
# NEXAH SYSTEM GENERATOR
# Create a new NEXAH system JSON template
# ==========================================================

import os
import json
import argparse


BASE_DIR = os.path.dirname(os.path.abspath(file))
SYSTEMS_DIR = os.path.join(BASE_DIR, "systems")

os.makedirs(SYSTEMS_DIR, exist_ok=True)


# ----------------------------------------------------------
# TEMPLATE
# ----------------------------------------------------------

def system_template(name):

    return {
        "name": name,
        "states": [
            "S0_start",
            "S1_growth",
            "S2_stress",
            "S3_failure"
        ],

        "regimes": {
            "S0_start": "STABLE",
            "S1_growth": "STABLE",
            "S2_stress": "STRESS",
            "S3_failure": "FAILURE"
        },

        "transitions": {
            "S0_start": "S1_growth",
            "S1_growth": "S2_stress",
            "S2_stress": "S3_failure",
            "S3_failure": "S3_failure"
        }
    }


# ----------------------------------------------------------
# CREATE SYSTEM
# ----------------------------------------------------------

def create_system(name):

    path = os.path.join(SYSTEMS_DIR, f"{name}.json")

    if os.path.exists(path):
        print("System already exists:", name)
        return

    data = system_template(name)

    with open(path, "w") as f:
        json.dump(data, f, indent=2)

    print("\nSystem created:")
    print(path)


# ----------------------------------------------------------
# LIST SYSTEMS
# ----------------------------------------------------------

def list_systems():

    print("\nAvailable systems:\n")

    for f in os.listdir(SYSTEMS_DIR):
        if f.endswith(".json"):
            print(" •", f.replace(".json",""))

    print()


# ----------------------------------------------------------
# MAIN
# ----------------------------------------------------------

if name == "main":

    parser = argparse.ArgumentParser(
        description="NEXAH System Generator"
    )

    parser.add_argument(
        "name",
        nargs="?",
        help="Name of new system"
    )

    parser.add_argument(
        "--list",
        action="store_true",
        help="List existing systems"
    )

    args = parser.parse_args()


    if args.list:
        list_systems()

    elif args.name:
        create_system(args.name)

    else:
        print("\nUsage:")
        print("  python nexah_system_generator.py <system_name>")
        print("  python nexah_system_generator.py --list")
