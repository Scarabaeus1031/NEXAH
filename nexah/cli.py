"""
NEXAH CLI (v0.8 – Navigation + Plotting)

Adds:

- target-based navigation
- regime visualization
- automatic plot saving

---

Examples:

Analyze:
    nexah analyze data.csv

With target:
    nexah analyze data.csv --target 0

With plot:
    nexah analyze data.csv --plot

Full:
    nexah analyze data.csv --target 0 --plot --out result.json

---

Output:

- JSON (stdout or file)
- optional plot → outputs/plots/



import argparse
import numpy as np
import json
import os
import matplotlib.pyplot as plt
from nexah.core import NEXAH


# =========================
# IO
# =========================

def load_csv(path):
    try:
        data = np.loadtxt(path, delimiter=",")
        return data
    except Exception as e:
        print(f"[ERROR] Could not load file: {e}")
        return None


def save_output(result, path):
    try:
        with open(path, "w") as f:
            json.dump(result, f, indent=2, default=str)
        print(f"[INFO] Saved output to {path}")
    except Exception as e:
        print(f"[ERROR] Could not save file: {e}")


# =========================
# PLOTTING
# =========================

def plot_regimes(data, result, filename="plot.png"):
    os.makedirs("outputs/plots", exist_ok=True)

    plt.figure()
    plt.plot(data, label="data")

    # regime zones (if available)
    zones = result.get("regime_zones", [])
    for (start, end) in zones:
        plt.axvspan(start, end, alpha=0.3)

    plt.title("NEXAH Regime Detection")
    plt.legend()

    path = f"outputs/plots/{filename}"
    plt.savefig(path)
    plt.close()

    print(f"[INFO] Plot saved to {path}")


# =========================
# COMMANDS
# =========================

def analyze_command(args):
    data = load_csv(args.file)
    if data is None:
        return

    nx = NEXAH(
        n_clusters=args.clusters,
        window=args.window,
        random_state=args.seed,
        normalize=not args.no_normalize
    )

    result = nx.analyze(
        data,
        target_state=args.target
    )

    # ---- OUTPUT ----
    if args.out:
        save_output(result, args.out)
    else:
        print(json.dumps(result, indent=2, default=str))

    # ---- PLOT ----
    if args.plot:
        fname = os.path.basename(args.file).replace(".csv", "_plot.png")
        plot_regimes(data, result, fname)


def compare_command(args):
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
# CLI
# =========================

def main():
    parser = argparse.ArgumentParser(description="NEXAH CLI")

    subparsers = parser.add_subparsers(dest="command")

    # ---- ANALYZE ----
    analyze_parser = subparsers.add_parser("analyze")
    analyze_parser.add_argument("file")

    analyze_parser.add_argument("--clusters", type=int, default=4)
    analyze_parser.add_argument("--window", type=int, default=5)
    analyze_parser.add_argument("--seed", type=int, default=42)
    analyze_parser.add_argument("--no-normalize", action="store_true")

    analyze_parser.add_argument("--target", type=int, help="Target state")
    analyze_parser.add_argument("--plot", action="store_true", help="Create plot")

    analyze_parser.add_argument("--out", help="Save JSON output")

    # ---- COMPARE ----
    compare_parser = subparsers.add_parser("compare")
    compare_parser.add_argument("file_a")
    compare_parser.add_argument("file_b")

    compare_parser.add_argument("--clusters", type=int, default=4)
    compare_parser.add_argument("--window", type=int, default=5)
    compare_parser.add_argument("--seed", type=int, default=42)
    compare_parser.add_argument("--no-normalize", action="store_true")

    compare_parser.add_argument("--out", help="Save JSON output")

    args = parser.parse_args()

    if args.command == "analyze":
        analyze_command(args)

    elif args.command == "compare":
        compare_command(args)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()---


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
