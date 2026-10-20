#!/usr/bin/env python3
"""PENT-03: arithmetic consistency and 3D-readiness audit."""

from __future__ import annotations

import json
import math


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    return all(value % divisor for divisor in range(2, int(math.sqrt(value)) + 1))


def run() -> dict[str, object]:
    distinct_labels = [43, 97, 83, 137]
    pentagon_positions = [43, 83, 83, 97, 137]
    base_labels = [3, 7, 13, 17]
    quotient = 43 / (97 * 83 * 137)

    checks = {
        "four_printed_labels_are_prime": all(is_prime(value) for value in distinct_labels),
        "four_printed_labels_sum_to_360": sum(distinct_labels) == 360,
        "printed_quotient_rounds_to_0_000039": round(quotient, 6) == 0.000039,
        "drawn_pentagon_has_five_positions_but_only_four_unique_labels": len(pentagon_positions) == 5 and len(set(pentagon_positions)) == 4,
        "drawn_five_position_sum_is_443_not_360": sum(pentagon_positions) == 443 and sum(pentagon_positions) != 360,
        "complementary_pairs_sum_to_20": 17 + 3 == 20 and 13 + 7 == 20,
        "upper_pair_sums_to_30": 17 + 13 == 30,
        "base_label_set_sums_to_40": sum(base_labels) == 40,
        "three_angle_interpretation_51_78_78_fails": 51 + 78 + 78 != 180,
        "three_dimensional_contract_is_incomplete": True,
    }

    return {
        "schema": "nexah.pascal-pentagon-label-audit/1.0.0",
        "status": "PASS_WITH_BOUNDARY" if all(checks.values()) else "FAIL",
        "classification": "BOUNDED_LABEL_AUDIT_NOT_ADMITTED",
        "inputs": {
            "four_label_identity": distinct_labels,
            "five_drawn_positions": pentagon_positions,
            "base_label_set": base_labels,
            "conditional_angle_reading": [51, 78, 78],
        },
        "result": {
            "four_label_sum": sum(distinct_labels),
            "five_position_sum": sum(pentagon_positions),
            "quotient": quotient,
            "unique_pentagon_labels": len(set(pentagon_positions)),
            "label_mapping_between_plates": "UNDEFINED",
            "resonance_measure": "UNDEFINED",
            "three_dimensional_lift": "NOT_READY",
        },
        "checks": checks,
        "claim_ceiling": "Arithmetic identities and contradictions only; no pentagonal invariant, resonance law, historical meaning, physical mechanism or 3D pyramid is established.",
    }


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["status"] == "PASS_WITH_BOUNDARY" else 1)

