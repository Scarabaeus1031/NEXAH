"""
NEXAH CLI (Command Line Interface)

This module provides a simple command-line interface for the NEXAH kernel.

It allows users to:

- analyze a single time series (CSV)
- compare two time series
- optionally save results as JSON

---

Usage examples:

Analyze a file:
    nexah analyze data.csv

Analyze with parameters:
    nexah analyze data.csv --clusters 5 --window 20

Save output:
    nexah analyze data.csv --out result.json

Compare two systems:
    nexah compare a.csv b.csv

---

Input format:

- CSV file
- 1D or multi-dimensional numeric data
- no headers required

---

Output:

- JSON printed to terminal OR saved to file
- includes:
    - system states
    - transitions
    - stability metrics
    - regime shifts
    - system signature

---

Design principles:

- minimal dependencies
- simple interface
- transparent output
- no hidden behavior

This CLI is a thin wrapper around:

    nexah.core.NEXAH

All core logic lives in the kernel.

---
"""

import argparse
import numpy as np
import json
from nexah.core import NEXAH


# =========================
# IO HELPERS
# =========================

def load_csv(path):
    """
    Load CSV file into numpy array.

    Returns:
        np.ndarray or None if error
    """
    try:
        data = np.loadtxt(path, delimiter=",")
        return data
    except Exception as e:
        print(f"[ERROR] Could not load file: {e}")
        return None


def save_output(result, path):
    """
    Save result dictionary to JSON file.
    """
    try:
        with open(path, "w") as f:
            json.dump(result, f, indent=2, default=str)
        print(f"[INFO] Saved output to {path}")
    except Exception as e:
        print(f"[ERROR] Could not save file: {e}")


# =========================
# COMMANDS
# =========================

def analyze_command(args):
    """
    Run NEXAH analysis on a single CSV file.
    """
    data = load_csv(args.file)
    if data is None:
        return

    nx = NEXAH(
        n_clusters=args.clusters,
        window=args.window,
        random_state=args.seed,
        normalize=not args.no_normalize
    )

    result = nx.analyze(data)

    if args.out:
        save_output(result, args.out)
    else:
        print(json.dumps(result, indent=2, default=str))


def compare_command(args):
    """
    Compare two time series using NEXAH.
    """
    data_a = load_csv(args.file_a)
    data_b = load_csv(args.file_b)

    if data_a is None or data_b is None:
        return

    nx = NEXAH(
        n_clusters=args.clusters,
        window=args.window,
        random_state=args.seed,
        normalize=not args.no_normalize
    )

    result = nx.compare(data_a, data_b)

    if args.out:
        save_output(result, args.out)
    else:
        print(json.dumps(result, indent=2, default=str))


# =========================
# CLI ENTRY POINT
# =========================

def main():
    """
    Main CLI entry point.
    Defines commands and arguments.
    """

    parser = argparse.ArgumentParser(
        description="NEXAH CLI – Dynamical System Analysis Tool"
    )

    subparsers = parser.add_subparsers(dest="command")

    # ---------------------
    # ANALYZE COMMAND
    # ---------------------
    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze a time series (CSV)"
    )

    analyze_parser.add_argument(
        "file",
        help="Path to CSV file"
    )

    analyze_parser.add_argument(
        "--clusters",
        type=int,
        default=4,
        help="Number of states (default: 4)"
    )

    analyze_parser.add_argument(
        "--window",
        type=int,
        default=5,
        help="Embedding window size (default: 5)"
    )

    analyze_parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed (default: 42)"
    )

    analyze_parser.add_argument(
        "--no-normalize",
        action="store_true",
        help="Disable normalization"
    )

    analyze_parser.add_argument(
        "--out",
        help="Save output JSON to file"
    )

    # ---------------------
    # COMPARE COMMAND
    # ---------------------
    compare_parser = subparsers.add_parser(
        "compare",
        help="Compare two time series"
    )

    compare_parser.add_argument("file_a", help="First CSV file")
    compare_parser.add_argument("file_b", help="Second CSV file")

    compare_parser.add_argument("--clusters", type=int, default=4)
    compare_parser.add_argument("--window", type=int, default=5)
    compare_parser.add_argument("--seed", type=int, default=42)
    compare_parser.add_argument("--no-normalize", action="store_true")

    compare_parser.add_argument(
        "--out",
        help="Save output JSON to file"
    )

    args = parser.parse_args()

    # ---------------------
    # COMMAND ROUTING
    # ---------------------
    if args.command == "analyze":
        analyze_command(args)

    elif args.command == "compare":
        compare_command(args)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
