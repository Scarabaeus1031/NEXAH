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
import shlex
from datetime import datetime
from nexah.backends import V07BackendAdapter
from nexah.applications import (
    NetworkOrientationApplication,
    build_network_orientation_brief,
    remove_declared_edge,
    render_network_learning_text,
    render_network_orientation_text,
    run_network_probe_suite,
)
from nexah.core import NEXAH
from nexah.power_systems import (
    IEEEGeometryCaseManifest,
    build_ieee_geometry_campaign,
    check_manifest_adapter_protocol,
    check_manifest_environment,
)
from nexah.sources import IEEEPandapowerAdapter
from nexah.orientation import (
    Context,
    Provenance,
    generate_orientation_report,
    render_orientation_brief_markdown,
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


def save_text_output(text, path):
    try:
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text)
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
    learning = (
        run_network_probe_suite(result)
        if args.probes or args.format in ("brief", "brief-json")
        else None
    )
    if args.format in ("brief", "brief-json"):
        assert learning is not None
        command_parts = [
            "nexah",
            "orient-network",
            args.file,
            "--focus",
            args.focus,
            "--recorded-at",
            args.recorded_at.isoformat(),
            "--domain",
            args.domain,
        ]
        if args.target:
            command_parts.extend(("--target", args.target))
        if args.analysis_id:
            command_parts.extend(("--analysis-id", args.analysis_id))
        if args.baseline:
            command_parts.extend(("--baseline", args.baseline))
        elif args.remove_edge:
            command_parts.extend(("--remove-edge", *args.remove_edge))
        command_parts.extend(
            ("--format", "brief", "--out", "orientation-brief.md")
        )
        command = shlex.join(command_parts)
        brief = build_network_orientation_brief(
            learning,
            question=args.question,
            reproduction_command=command,
        )
        if args.format == "brief-json":
            payload = brief.to_dict()
            if args.out:
                save_output(payload, args.out)
            else:
                print(json.dumps(payload, indent=2))
        else:
            rendered = render_orientation_brief_markdown(brief)
            if args.out:
                save_text_output(rendered, args.out)
            else:
                print(rendered)
        return
    payload = learning.to_dict() if learning is not None else result.to_dict()
    if args.out:
        save_output(payload, args.out)
    elif args.format == "text":
        print(
            render_network_learning_text(learning)
            if learning is not None
            else render_network_orientation_text(result)
        )
    else:
        print(json.dumps(payload, indent=2))


def validate_ieee_manifest_command(args):
    source = load_json_object(args.file)
    if source is None:
        return
    manifest = IEEEGeometryCaseManifest.from_dict(source)
    environment = check_manifest_environment(manifest)
    protocol_mismatches = check_manifest_adapter_protocol(manifest)
    payload = {
        "manifest_id": manifest.manifest_id,
        "schema_valid": True,
        "environment": environment.to_dict(),
        "adapter_protocol_compatible": not protocol_mismatches,
        "adapter_protocol_mismatches": protocol_mismatches,
        "case_roles": {case.case_id: case.role for case in manifest.cases},
        "outcome_status": manifest.outcome_status,
        "episode_update_allowed": manifest.episode_update_allowed,
    }
    print(json.dumps(payload, indent=2))


def build_ieee_frames_command(args):
    source = load_json_object(args.manifest)
    if source is None:
        return
    manifest = IEEEGeometryCaseManifest.from_dict(source)
    try:
        case = next(item for item in manifest.cases if item.case_id == args.case)
    except StopIteration as error:
        raise ValueError(f"case {args.case!r} is not declared by the manifest") from error
    campaign_id = args.campaign_id or f"{manifest.manifest_id}-{case.case_id}"
    campaign = IEEEPandapowerAdapter(case_id=case.case_id).run_campaign(
        case.load_scales,
        campaign_id=campaign_id,
        provenance=Provenance(
            source=case.source_loader,
            method="frozen independent Newton-Raphson load-scale campaign",
            recorded_at=args.recorded_at,
            record_id=campaign_id,
            metadata={"manifest_id": manifest.manifest_id},
        ),
        context=Context(
            domain="power-system",
            values={
                "evidence_class": manifest.evidence_class,
                "case_role": case.role,
                "campaign_axis": manifest.campaign_axis,
            },
        ),
    )
    geometry = build_ieee_geometry_campaign(campaign, manifest)
    payload = geometry.to_dict()
    if args.out:
        save_output(payload, args.out)
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
    network_parser.add_argument(
        "--format",
        choices=("json", "text", "brief", "brief-json"),
        default="json",
    )
    network_parser.add_argument(
        "--question",
        help="human question shown in an Orientation Brief",
    )
    network_parser.add_argument(
        "--probes",
        action="store_true",
        help="add five read-only learning perspectives (V2 wrapper)",
    )
    network_parser.add_argument("--out")

    # VALIDATE IEEE MANIFEST
    manifest_parser = subparsers.add_parser(
        "validate-ieee-manifest",
        description="Validate a frozen Phase V IEEE geometry case protocol",
    )
    manifest_parser.add_argument("file")

    # BUILD IEEE GEOMETRY FRAMES
    frames_parser = subparsers.add_parser(
        "build-ieee-frames",
        description="Build manifest-bound physical frames without geometry claims",
    )
    frames_parser.add_argument("manifest")
    frames_parser.add_argument("--case", required=True)
    frames_parser.add_argument("--recorded-at", type=parse_timestamp, required=True)
    frames_parser.add_argument("--campaign-id")
    frames_parser.add_argument("--out")

    args = parser.parse_args()

    if args.command == "analyze":
        analyze_command(args)
    elif args.command == "compare":
        compare_command(args)
    elif args.command == "orient":
        orient_command(args)
    elif args.command == "orient-network":
        orient_network_command(args)
    elif args.command == "validate-ieee-manifest":
        validate_ieee_manifest_command(args)
    elif args.command == "build-ieee-frames":
        build_ieee_frames_command(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
