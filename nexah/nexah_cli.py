import argparse
import numpy as np
import json
from nexah import NEXAH


def load_csv(path):
    try:
        data = np.loadtxt(path, delimiter=",")
        return data
    except Exception as e:
        print(f"Error loading file: {e}")
        return None


def analyze_command(args):
    data = load_csv(args.file)
    if data is None:
        return

    nx = NEXAH()

    result = nx.analyze(data)

    print(json.dumps(result, indent=2, default=str))


def compare_command(args):
    data_a = load_csv(args.file_a)
    data_b = load_csv(args.file_b)

    if data_a is None or data_b is None:
        return

    nx = NEXAH()

    result = nx.compare(data_a, data_b)

    print(json.dumps(result, indent=2, default=str))


def main():
    parser = argparse.ArgumentParser(description="NEXAH CLI")

    subparsers = parser.add_subparsers(dest="command")

    # analyze
    analyze_parser = subparsers.add_parser("analyze")
    analyze_parser.add_argument("file", help="Path to CSV file")

    # compare
    compare_parser = subparsers.add_parser("compare")
    compare_parser.add_argument("file_a", help="First CSV file")
    compare_parser.add_argument("file_b", help="Second CSV file")

    args = parser.parse_args()

    if args.command == "analyze":
        analyze_command(args)

    elif args.command == "compare":
        compare_command(args)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
