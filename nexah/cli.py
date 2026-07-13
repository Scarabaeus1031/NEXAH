"""
NEXAH CLI (v0.7 – Navigation + Plotting)

Features:
- analyze time series
- compare systems
- generate evidence-bound Orientation Reports
- orient declared directed networks
- target-based navigation
- regime plotting

Example:
    nexah analyze data.csv --plot
    nexah analyze data.csv --target 0 --plot
    nexah orient data.csv --recorded-at 2026-07-13T08:00:00+00:00
    nexah orient-network graph.json --focus a --target b \
        --recorded-at 2026-07-13T08:00:00+00:00
"""

import argparse
import numpy as np
import json
import os
from datetime import datetime
from nexah.backends import V07BackendAdapter
from nexah.applications import (
    NetworkOrientationApplication,
    remove_declared_edge,
    render_network_orientation_text,
)
from nexah.core import NEXAH
from nexah.orientation import (
    Context,
    Provenance,
    generate_orientation_report,
)


# =========================
# IO
# =========================

def load_csv(path):
    try:
        return np.loadtxt(path, delimiter=",")
    except Exception as e:
        print(f"[ERROR] Could not load file: {e}")
        return None


def load_json_object(path):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            value = json.load(handle)
    except Exception as e:
        print(f"[ERROR] Could not load JSON file: {e}")
        return None
    if not isinstance(value, dict):
        print("[ERROR] Network source must be a JSON object")
        return None
    return value


def save_output(result, path):
    try:
        with open(path, "w") as f:
            json.dump(result, f, indent=2, default=str)
        print(f"[INFO] Saved output to {path}")
    except Exception as e:
        print(f"[ERROR] Could not save file: {e}")


def parse_timestamp(value):
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise argparse.ArgumentTypeError("timestamp must be ISO 8601") from error
    if parsed.tzinfo is None:
        raise argparse.ArgumentTypeError("timestamp must include a timezone")
    return parsed


# =========================
# PLOTTING
# =========================

def plot_regimes(data, result, filename):
    import matplotlib.pyplot as plt

    os.makedirs("outputs/plots", exist_ok=True)

    plt.figure()
    plt.plot(data, label="data")

    for (start, end) in result.get("regime_zones", []):
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

    result = nx.analyze(data, target_state=args.target)

    if args.out:
        save_output(result, args.out)
    else:
        print(json.dumps(result, indent=2, default=str))

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


def orient_command(args):
    data = load_csv(args.file)
    if data is None:
        return

    adapter = V07BackendAdapter(
        n_clusters=args.clusters,
        window=args.window,
        random_state=args.seed,
        normalize=not args.no_normalize,
    )
    adapted = adapter.adapt(
        data,
        analysis_id=args.analysis_id or os.path.splitext(os.path.basename(args.file))[0],
        provenance=Provenance(
            source=args.file,
            method="CSV loaded by NEXAH CLI",
            recorded_at=args.recorded_at,
            record_id=args.analysis_id,
        ),
        context=Context(domain=args.domain),
    )
    report = generate_orientation_report(adapted).to_dict()

    if args.out:
        save_output(report, args.out)
    else:
        print(json.dumps(report, indent=2))


def orient_network_command(args):
    source = load_json_object(args.file)
    if source is None:
        return

    baseline = None
    baseline_provenance = None
    current = source
    method = "declared graph loaded by NEXAH CLI"
    if args.baseline:
        baseline = load_json_object(args.baseline)
        if baseline is None:
            return
        baseline_provenance = Provenance(
            source=args.baseline,
            method="declared baseline graph loaded by NEXAH CLI",
            recorded_at=args.recorded_at,
        )
    elif args.remove_edge:
        baseline = source
        current = remove_declared_edge(source, args.remove_edge[0], args.remove_edge[1])
        method = (
            "declared edge-removal training scenario generated by NEXAH CLI: "
            f"{args.remove_edge[0]} -> {args.remove_edge[1]}"
        )
        baseline_provenance = Provenance(
            source=args.file,
            method="declared baseline graph loaded by NEXAH CLI",
            recorded_at=args.recorded_at,
        )

    analysis_id = args.analysis_id or os.path.splitext(os.path.basename(args.file))[0]
    result = NetworkOrientationApplication().orient(
        current,
        baseline_source=baseline,
        analysis_id=analysis_id,
        provenance=Provenance(
            source=args.file,
            method=method,
            recorded_at=args.recorded_at,
            record_id=args.analysis_id,
        ),
        baseline_provenance=baseline_provenance,
        context=Context(
            domain=args.domain,
            values={"application": "network-orientation-v1"},
        ),
        focus=args.focus,
        target=args.target,
    )
    payload = result.to_dict()
    if args.out:
        save_output(payload, args.out)
    elif args.format == "text":
        print(render_network_orientation_text(result))
    else:
        print(json.dumps(payload, indent=2))


# =========================
# CLI
# =========================

def main():
    parser = argparse.ArgumentParser(description="NEXAH CLI")
    subparsers = parser.add_subparsers(dest="command")

    # ANALYZE
    analyze_parser = subparsers.add_parser("analyze")
    analyze_parser.add_argument("file")
    analyze_parser.add_argument("--clusters", type=int, default=4)
    analyze_parser.add_argument("--window", type=int, default=5)
    analyze_parser.add_argument("--seed", type=int, default=42)
    analyze_parser.add_argument("--no-normalize", action="store_true")
    analyze_parser.add_argument("--target", type=int)
    analyze_parser.add_argument("--plot", action="store_true")
    analyze_parser.add_argument("--out")

    # COMPARE
    compare_parser = subparsers.add_parser("compare")
    compare_parser.add_argument("file_a")
    compare_parser.add_argument("file_b")
    compare_parser.add_argument("--clusters", type=int, default=4)
    compare_parser.add_argument("--window", type=int, default=5)
    compare_parser.add_argument("--seed", type=int, default=42)
    compare_parser.add_argument("--no-normalize", action="store_true")
    compare_parser.add_argument("--out")

    # ORIENT
    orient_parser = subparsers.add_parser(
        "orient", description="Generate an evidence-bound Orientation Report"
    )
    orient_parser.add_argument("file")
    orient_parser.add_argument("--recorded-at", type=parse_timestamp, required=True)
    orient_parser.add_argument("--analysis-id")
    orient_parser.add_argument("--domain", default="unspecified")
    orient_parser.add_argument("--clusters", type=int, default=4)
    orient_parser.add_argument("--window", type=int, default=5)
    orient_parser.add_argument("--seed", type=int, default=42)
    orient_parser.add_argument("--no-normalize", action="store_true")
    orient_parser.add_argument("--out")

    # ORIENT NETWORK
    network_parser = subparsers.add_parser(
        "orient-network",
        description=(
            "Describe reachability and structural sensitivity in a declared "
            "directed graph"
        ),
    )
    network_parser.add_argument("file")
    network_parser.add_argument("--focus", required=True)
    network_parser.add_argument("--target")
    network_parser.add_argument("--recorded-at", type=parse_timestamp, required=True)
    network_parser.add_argument("--analysis-id")
    network_parser.add_argument("--domain", default="unspecified-network")
    comparison = network_parser.add_mutually_exclusive_group()
    comparison.add_argument(
        "--baseline",
        help="independent baseline graph JSON compared with the positional file",
    )
    comparison.add_argument(
        "--remove-edge",
        nargs=2,
        metavar=("SOURCE", "TARGET"),
        help="generate an explicit structural training scenario from the input",
    )
    network_parser.add_argument("--format", choices=("json", "text"), default="json")
    network_parser.add_argument("--out")

    args = parser.parse_args()

    if args.command == "analyze":
        analyze_command(args)
    elif args.command == "compare":
        compare_command(args)
    elif args.command == "orient":
        orient_command(args)
    elif args.command == "orient-network":
        orient_network_command(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
