#!/usr/bin/env python3
"""Independent structural verifier for the Q106 contrast result."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main(path: Path) -> int:
    data = json.loads(path.read_text(encoding="utf-8"))
    result = data["result"]
    homologues = result["homologues"]
    checks = [
        data["contract_id"] == "A0-Q106:46_106_194_CONTRAST_AUDIT:V1",
        data["classification"] == "PASS_Q106_LOCAL_AND_BOUNDED_HOMOLOGUE_SELECTIVITY",
        data["summary"] == {"passed": 16, "total": 16, "failed": 0},
        [item["k"] for item in homologues] == [3, 4, 5],
        [item["carrier"] for item in homologues] == [46, 106, 194],
        [item["square_index_primes"] for item in homologues]
        == [[7, 23, 53], [23, 53, 97], [53, 97, 151]],
        [item["return_residual"] for item in homologues] == [-7, 9, 43],
        [item["target_square"] for item in homologues] == [4, 9, 16],
        result["direct_homologue_hits"] == [4],
        result["finite_scan"] == {"minimum_k": 2, "maximum_k": 1000, "hits": [4]},
        result["root_pythagorean_hits"] == [4],
        result["local_exact_hits"] == [106],
        [item["minus_p25"] for item in result["local_perturbations"]] == [7, 8, 9, 10, 11],
        [item["minus_2p16"] for item in result["local_perturbations"]] == [-2, -1, 0, 1, 2],
        any("no R(Q46) or R(Q194)" in item for item in data["claim_boundary"]),
        any("not uniqueness for all positive integers" in item for item in data["claim_boundary"]),
    ]
    passed = sum(checks)
    print(json.dumps({"status": "PASS" if all(checks) else "FAIL", "passed": passed, "total": len(checks)}, indent=2))
    return 0 if all(checks) else 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: verify_result.py RESULT.json")
    raise SystemExit(main(Path(sys.argv[1])))
