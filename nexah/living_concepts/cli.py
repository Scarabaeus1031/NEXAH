from __future__ import annotations

import argparse
import json
from collections.abc import Sequence

from .adapter import ConceptAnswerAdapter
from .overlay import ConceptOverlayError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m nexah.living_concepts",
        description="Resolve accepted Living Concepts pilot answer contracts.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    answer = subparsers.add_parser("answer", help="Resolve one accepted pilot contract")
    answer.add_argument("question_key", help="Exact key CFQ-01 through CFQ-06")
    answer.add_argument("--mode", choices=("reader", "explain"), default="reader")
    answer.add_argument(
        "--overlay",
        help="Explicit path to an accepted Living Concepts v0.1 Overlay",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        adapter = ConceptAnswerAdapter.load(args.overlay)
        result = adapter.answer(args.question_key, mode=args.mode)
    except ConceptOverlayError as exc:
        print(json.dumps({"state": "invalid_overlay", "reason": str(exc)}, indent=2))
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["state"] == "answered" else 2

