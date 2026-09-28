"""Command-line interface for the deterministic WP3 core."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .package import create_return, run_package, verify_package
from .runtime import CompareError, canonical_bytes, canonical_sha256, compare_records, load_json


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(prog="nexah-compare")
    sub = result.add_subparsers(dest="command", required=True)
    compare = sub.add_parser("compare", help="create one canonical ComparisonRecord")
    compare.add_argument("--case", required=True, type=Path)
    compare.add_argument("--analysis", required=True, type=Path, action="append")
    compare.add_argument("--reference", help="reference AnalysisRecord ID")
    compare.add_argument("--alignment", type=Path, help="explicit declared-key alignment JSON")
    compare.add_argument("--output", type=Path, help="canonical output file; stdout when omitted")
    run = sub.add_parser("run-package", help="run, seal and verify one local Case package")
    run.add_argument("--package", required=True, type=Path)
    verify = sub.add_parser("verify-package", help="replay and verify a sealed Case package")
    verify.add_argument("--package", required=True, type=Path)
    returned = sub.add_parser("create-return", help="write one Human ReturnRecord")
    returned.add_argument("--package", required=True, type=Path)
    returned.add_argument("--action", required=True, choices=["CONFIRM", "AMEND", "ABSTAIN", "STOP"])
    returned.add_argument("--actor", required=True)
    returned.add_argument("--statement", required=True)
    returned.add_argument("--returned-at", required=True, help="explicit RFC 3339 timestamp")
    returned.add_argument("--residual", action="append", default=[])
    returned.add_argument("--amendments", type=Path, help="JSON array of amendments")
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "compare":
            case = load_json(args.case)
            analyses = [load_json(path) for path in args.analysis]
            alignment = load_json(args.alignment) if args.alignment else None
            comparison = compare_records(
                case,
                analyses,
                reference_analysis_id=args.reference,
                alignment_plan=alignment,
            )
            payload = canonical_bytes(comparison)
            digest = canonical_sha256(comparison)
            if args.output:
                args.output.write_bytes(payload)
                result = {
                    "comparison_id": comparison["record_id"],
                    "comparison_sha256": digest,
                    "output": str(args.output),
                    "status": "VALID",
                }
                print(json.dumps(result, sort_keys=True))
            else:
                sys.stdout.buffer.write(payload)
                print(f"comparison_sha256={digest}", file=sys.stderr)
        elif args.command == "run-package":
            print(json.dumps(run_package(args.package), sort_keys=True))
        elif args.command == "verify-package":
            print(json.dumps(verify_package(args.package), sort_keys=True))
        else:
            amendments = load_json(args.amendments) if args.amendments else []
            if not isinstance(amendments, list):
                raise CompareError("INVALID_AMENDMENTS", "expected JSON array")
            returned = create_return(
                args.package,
                action=args.action,
                actor_id=args.actor,
                statement=args.statement,
                returned_at=args.returned_at,
                selected_residual_ids=args.residual,
                amendments=amendments,
            )
            print(
                json.dumps(
                    {
                        "status": "VALID",
                        "return_id": returned["record_id"],
                        "human_action": returned["human_action"],
                        "return_sha256": canonical_sha256(returned),
                    },
                    sort_keys=True,
                )
            )
        return 0
    except CompareError as error:
        print(
            json.dumps(
                {"status": "REJECTED", "reason_code": error.code, "detail": error.detail},
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        return error.exit_code
    except OSError as error:
        print(
            json.dumps(
                {"status": "REJECTED", "reason_code": "IO_ERROR", "detail": str(error)},
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
