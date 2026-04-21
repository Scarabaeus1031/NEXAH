"""
Analyze NEXAH Kernel Structure
==============================

Scans the nexah_kernel folder and prints a structural overview.

Run:
    python analyze_nexah_kernel_structure.py
"""

from pathlib import Path
import json


ROOT = Path("ENGINE/nexah_kernel")


def scan_files():

    stats = {
        "python_files": [],
        "demo_files": [],
        "visual_files": [],
        "data_files": [],
        "other_files": []
    }

    for file in ROOT.rglob("*"):

        if file.is_file():

            if file.suffix == ".py":

                stats["python_files"].append(file)

                if "demo" in str(file):
                    stats["demo_files"].append(file)

            elif file.suffix in [".png", ".jpg", ".svg", ".gif"]:

                stats["visual_files"].append(file)

            elif file.suffix in [".csv", ".json", ".txt"]:

                stats["data_files"].append(file)

            else:

                stats["other_files"].append(file)

    return stats


def print_report(stats):

    print("\nNEXAH Kernel Structure\n")
    print("Root:", ROOT)
    print()

    print("Python modules:", len(stats["python_files"]))
    print("Demo scripts:", len(stats["demo_files"]))
    print("Visual files:", len(stats["visual_files"]))
    print("Data files:", len(stats["data_files"]))
    print()

    print("Key modules:\n")

    for f in stats["python_files"]:

        if "pattern_engine" in f.name \
        or "resonance_metrics" in f.name \
        or "pattern_classifier" in f.name:

            print("  CORE:", f)

    print()

    print("Demo modules:\n")

    for f in stats["demo_files"][:20]:

        print("  ", f)

    if len(stats["demo_files"]) > 20:

        print("  ...", len(stats["demo_files"]) - 20, "more")

    print()

    print("Visual database size:")

    print("  files:", len(stats["visual_files"]))

    print()

    print("Data files:")

    for f in stats["data_files"][:10]:

        print("  ", f)

    if len(stats["data_files"]) > 10:

        print("  ...", len(stats["data_files"]) - 10, "more")


def save_json(stats):

    report = {
        "python_files": len(stats["python_files"]),
        "demo_files": len(stats["demo_files"]),
        "visual_files": len(stats["visual_files"]),
        "data_files": len(stats["data_files"])
    }

    out = Path("nexah_kernel_report.json")

    with open(out, "w") as f:

        json.dump(report, f, indent=4)

    print("\nSaved report:", out)


def main():

    stats = scan_files()

    print_report(stats)

    save_json(stats)


if __name__ == "__main__":

    main()
