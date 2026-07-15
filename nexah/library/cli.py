from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .arena import ArenaClient, ArenaError, compare_all, compare_entity
from .discovery import build_discovery, write_discovery_files
from .health import build_health, render_health_text
from .kernel import OrientationQueries, graph_to_mermaid
from .operations import OperationError, default_review_root, dump_yaml
from .reader import ReaderOverlay, ReaderOverlayError
from .regression import run_reader_regression, render_reader_regression_text
from .registry import Registry, RegistryError
from .snapshot import build_source_snapshot, write_source_snapshot


def _json(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="nexah-library")
    parser.add_argument("--registry", type=Path, help="Path to the registry directory")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("validate", help="Validate Registry YAML and references")

    compare = sub.add_parser("compare", help="Read and compare Registry records with Are.na")
    target = compare.add_mutually_exclusive_group(required=True)
    target.add_argument("--all", action="store_true")
    target.add_argument("--entity")
    compare.add_argument("--include-sequence", action="store_true")

    discover = sub.add_parser("discover", help="Build a read-only public Channel inventory")
    discover.add_argument("--user", default="nexah-scarabaeus1031")
    discover.add_argument("--report", type=Path)
    discover.add_argument("--inventory", type=Path)

    path = sub.add_parser("reading-path", help="Build a conservative registry-backed reading path")
    path.add_argument("--audience")

    operators = sub.add_parser("operators", help="Find works using a controlled Operator")
    operators.add_argument("--operator", required=True)

    graph = sub.add_parser("graph", help="Render the curated relationship graph")
    graph.add_argument("--format", choices=["json", "mermaid"], default="json")
    graph.add_argument("--without-operators", action="store_true")

    recommend = sub.add_parser("recommend", help="Recommend related registered works")
    recommend.add_argument("entity")
    recommend.add_argument("--limit", type=int, default=5)

    reader = sub.add_parser(
        "reader-question", help="Answer one of the six reviewed Reader questions"
    )
    reader.add_argument("question", choices=[f"UQ-{value:02d}" for value in range(1, 7)])
    reader.add_argument("--mode", choices=["reader", "explain"], default="reader")
    reader.add_argument("--review-root", type=Path)

    health = sub.add_parser("health", help="Report local Living Library health")
    health.add_argument("--format", choices=["text", "yaml"], default="text")
    health.add_argument("--strict", action="store_true")
    health.add_argument("--review-root", type=Path)

    snapshot = sub.add_parser(
        "source-snapshot", help="Capture a read-only public Are.na source snapshot"
    )
    snapshot.add_argument("--user", default="nexah-scarabaeus1031")
    snapshot.add_argument("--output", type=Path)

    regression = sub.add_parser(
        "reader-regression", help="Verify the six accepted Reader Policies"
    )
    regression.add_argument(
        "--question", choices=[f"UQ-{value:02d}" for value in range(1, 7)]
    )
    regression.add_argument("--format", choices=["text", "yaml"], default="text")
    regression.add_argument("--review-root", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        registry = Registry.load(args.registry)
        if args.command == "validate":
            errors = registry.validate()
            if errors:
                _json({"valid": False, "errors": errors})
                return 1
            _json(
                {
                    "valid": True,
                    "entities": len(registry.entities),
                    "concepts": len(registry.concepts),
                    "arena_write_policy": registry.manifest["write_policy"]["arena"],
                }
            )
            return 0

        if args.command == "compare":
            client = ArenaClient.from_environment()
            result = (
                compare_all(registry, client, include_sequence=args.include_sequence)
                if args.all
                else compare_entity(
                    registry, args.entity, client, include_sequence=args.include_sequence
                )
            )
            _json(result)
            return 0

        if args.command == "discover":
            if bool(args.report) != bool(args.inventory):
                raise RegistryError("discover requires both --report and --inventory, or neither")
            client = ArenaClient.from_environment()
            discovery = build_discovery(
                registry,
                client.get_user_channels(args.user),
                user_slug=args.user,
            )
            if args.report and args.inventory:
                write_discovery_files(
                    discovery,
                    report_path=args.report,
                    inventory_path=args.inventory,
                )
                _json(
                    {
                        "summary": discovery["summary"],
                        "report": str(args.report),
                        "inventory": str(args.inventory),
                    }
                )
            else:
                _json({"summary": discovery["summary"], "channels": discovery["channels"]})
            return 0

        if args.command == "reader-question":
            overlay = ReaderOverlay.load(registry, args.review_root)
            _json(overlay.answer(args.question, mode=args.mode))
            return 0

        if args.command == "health":
            report = build_health(registry, review_root=args.review_root)
            print(dump_yaml(report) if args.format == "yaml" else render_health_text(report))
            return 1 if args.strict and report["failures"] else 0

        if args.command == "source-snapshot":
            checked = datetime.now(timezone.utc).isoformat(timespec="seconds")
            snapshot = build_source_snapshot(
                registry,
                ArenaClient.from_environment(),
                user_slug=args.user,
                observed_at=checked,
            )
            output = args.output or (
                default_review_root() / "source_snapshots" / f"arena-{checked[:10]}.yaml"
            )
            write_source_snapshot(snapshot, output)
            _json({"snapshot": str(output), "summary": snapshot["summary"]})
            return 0

        if args.command == "reader-regression":
            report = run_reader_regression(
                registry,
                review_root=args.review_root,
                question_id=args.question,
            )
            print(
                dump_yaml(report)
                if args.format == "yaml"
                else render_reader_regression_text(report)
            )
            return 0 if report["status"] == "pass" else 1

        queries = OrientationQueries(registry)
        if args.command == "reading-path":
            _json(queries.reading_path(args.audience))
        elif args.command == "operators":
            _json(queries.operator_usage(args.operator))
        elif args.command == "graph":
            value = queries.graph(include_operators=not args.without_operators)
            print(graph_to_mermaid(value) if args.format == "mermaid" else json.dumps(value, ensure_ascii=False, indent=2))
        elif args.command == "recommend":
            _json(
                [
                    {
                        "id": item.entity_id,
                        "title": item.title,
                        "score": item.score,
                        "reasons": list(item.reasons),
                    }
                    for item in queries.recommendations(args.entity, args.limit)
                ]
            )
        return 0
    except (RegistryError, ArenaError, ReaderOverlayError, OperationError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
