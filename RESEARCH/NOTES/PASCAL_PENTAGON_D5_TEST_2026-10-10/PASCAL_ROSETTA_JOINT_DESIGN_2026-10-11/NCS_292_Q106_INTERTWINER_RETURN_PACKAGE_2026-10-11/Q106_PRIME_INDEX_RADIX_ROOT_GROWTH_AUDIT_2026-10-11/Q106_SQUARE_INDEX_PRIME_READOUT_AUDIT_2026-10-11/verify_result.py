#!/usr/bin/env python3
"""Independent structural verifier for the frozen Q106 square-index result."""

from __future__ import annotations

import json
import sys
from pathlib import Path


EXPECTED = "PASS_EXACT_SQUARE_INDEX_PRIME_READOUT_WITH_NO_D5_INVARIANT_53_SUBCARRIER"


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: verify_result.py RESULT.json")
        return 2
    payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    readout = payload["readout"]
    q106 = readout["Q106"]
    checks = payload["checks"]
    conditions = [
        payload["classification"] == EXPECTED,
        payload["summary"] == {"passed": len(checks), "total": len(checks), "failed": 0},
        all(item["status"] == "PASS" for item in checks),
        [q106["F"], q106["O"], q106["L"], q106["N"]] == [9, 16, 25, 106],
        readout["square_roots"] == [3, 4, 5],
        readout["square_indices"] == [9, 16, 25],
        readout["square_index_primes"] == [23, 53, 97],
        readout["five_root_ladder"]["adjacent_sums"] == [9, 30, 76, 150],
        readout["closure"]["p25_minus_p16"] == 44,
        readout["closure"]["four_p5_plus_3_squared"] == 53,
        readout["closure"]["two_p16"] == 106,
        readout["D5_invariant_53_witnesses"] == [],
        readout["consecutive_root_hits_1_to_10000"] == [3],
    ]
    if all(conditions):
        print(f"PASS independent verifier: {len(conditions)}/{len(conditions)}")
        return 0
    print(f"FAIL independent verifier: {sum(conditions)}/{len(conditions)}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
