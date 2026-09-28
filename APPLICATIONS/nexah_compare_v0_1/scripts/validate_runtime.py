#!/usr/bin/env python3
"""Run the WP3 deterministic core test suite."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    command = [
        sys.executable,
        "-m",
        "unittest",
        "discover",
        "-s",
        str(ROOT / "tests"),
        "-p",
        "test_*.py",
        "-v",
    ]
    completed = subprocess.run(command, cwd=ROOT, check=False)
    if completed.returncode:
        return completed.returncode
    print(
        json.dumps(
            {
                "status": "VALID",
                "profile": "NC01-ADVISORY-0.1",
                "schema_engine": "jsonschema Draft202012Validator",
                "runtime_tests": 14,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
