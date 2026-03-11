"""
Discover Resonance Zones
========================

Scans symmetry/drift parameter space and finds high resonance regions.

Run:
    python -m ENGINE.nexah_kernel.tools.discover_resonance_zones
"""

import numpy as np
import json
from pathlib import Path

from ENGINE.nexah_kernel.pattern_engine import generate_pattern
from ENGINE.nexah_kernel.resonance_metrics import compute_metrics
from ENGINE.nexah_kernel.pattern_classifier import classify_pattern


OUTPUT_DIR = Path("ENGINE/nexah_kernel/demos/data/resonance_discovery")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def scan_parameter_space():

    results = []

    symmetry_range = range(3, 21)

    drift_range = np.linspace(0, 6, 40)

    for n in symmetry_range:

        for drift in drift_range:

            x, y = generate_pattern(
                n=n,
                drift_deg=drift,
                iterations=1500
            )

            metrics = compute_metrics(x, y)

            classification = classify_pattern(x, y)

            result = {

                "n": int(n),
                "drift": float(drift),

                "pattern_type": classification["type"],

                "resonance_score": metrics["resonance_score"],
                "closure_error": metrics["closure_error"],
                "radial_variance": metrics["radial_variance"],
                "angular_irregularity": metrics["angular_irregularity"]

            }

            results.append(result)

    return results


def find_top_resonances(results, top_n=20):

    sorted_results = sorted(
        results,
        key=lambda r: r["resonance_score"],
        reverse=True
    )

    return sorted_results[:top_n]


def save_results(results, top):

    all_file = OUTPUT_DIR / "resonance_scan_full.json"

    with open(all_file, "w") as f:
        json.dump(results, f, indent=2)

    top_file = OUTPUT_DIR / "top_resonance_zones.json"

    with open(top_file, "w") as f:
        json.dump(top, f, indent=2)

    print("\nSaved full scan:", all_file)
    print("Saved top zones:", top_file)


def print_top(top):

    print("\nTop Resonance Zones\n")

    for r in top:

        print(
            f"n={r['n']:2d}   "
            f"drift={r['drift']:.2f}°   "
            f"type={r['pattern_type']}   "
            f"score={r['resonance_score']:.4f}"
        )


def main():

    print("\nScanning symmetry / drift parameter space...\n")

    results = scan_parameter_space()

    top = find_top_resonances(results)

    print_top(top)

    save_results(results, top)


if __name__ == "__main__":

    main()
