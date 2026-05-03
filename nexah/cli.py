import argparse
import numpy as np
import json
from nexah.core import NEXAH


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

    result = nx.analyze(data)

    if args.out:
        save_output(result, args.out)
    else:
        print(json.dumps(result, indent=2, default=str))


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


def main():
    parser = argparse.ArgumentParser(description="NEXAH CLI")

    subparsers = parser.add_subparsers(dest="command")

    # --- ANALYZE ---
    analyze_parser = subparsers.add_parser("analyze")
    analyze_parser.add_argument("file", help="Path to CSV file")

    analyze_parser.add_argument("--clusters", type=int, default=4)
    analyze_parser.add_argument("--window", type=int, default=5)
    analyze_parser.add_argument("--seed", type=int, default=42)
    analyze_parser.add_argument("--no-normalize", action="store_true")

    analyze_parser.add_argument("--out", help="Save output JSON to file")

    # --- COMPARE ---
    compare_parser = subparsers.add_parser("compare")
    compare_parser.add_argument("file_a")
    compare_parser.add_argument("file_b")

    compare_parser.add_argument("--clusters", type=int, default=4)
    compare_parser.add_argument("--window", type=int, default=5)
    compare_parser.add_argument("--seed", type=int, default=42)
    compare_parser.add_argument("--no-normalize", action="store_true")

    compare_parser.add_argument("--out", help="Save output JSON to file")

    args = parser.parse_args()

    if args.command == "analyze":
        analyze_command(args)

    elif args.command == "compare":
        compare_command(args)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
