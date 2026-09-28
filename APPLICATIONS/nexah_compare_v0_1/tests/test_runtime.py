from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from nexah_compare.runtime import (  # noqa: E402
    CompareError,
    canonical_bytes,
    canonical_sha256,
    compare_records,
    evaluate_formula,
    load_json,
    validate_schema,
)


class RuntimeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.case = load_json(ROOT / "fixtures/positive/case.json")
        cls.alpha = load_json(ROOT / "fixtures/positive/analysis-a.json")
        cls.beta = load_json(ROOT / "fixtures/positive/analysis-b.json")
        cls.alignment = load_json(ROOT / "runtime_fixtures/market-entry-alignment.json")

    def compare(self):
        return compare_records(
            copy.deepcopy(self.case),
            [copy.deepcopy(self.alpha), copy.deepcopy(self.beta)],
            alignment_plan=copy.deepcopy(self.alignment),
        )

    def test_declared_alignment_is_deterministic_and_schema_valid(self) -> None:
        first = self.compare()
        second = self.compare()
        self.assertEqual(canonical_bytes(first), canonical_bytes(second))
        self.assertEqual(canonical_sha256(first), canonical_sha256(second))
        validate_schema(first)
        self.assertEqual(
            [item["classification"] for item in first["relation_groups"]],
            ["UNAVAILABLE", "UNAVAILABLE", "ADDED", "UNAVAILABLE"],
        )
        self.assertEqual(
            [item["reason_code"] for item in first["relation_groups"]],
            [
                "EVIDENCE_ASYMMETRY",
                "TIME_BASIS_MISMATCH",
                "PRESENT_ONLY_OUTSIDE_REFERENCE",
                "CRITERION_UNAVAILABLE",
            ],
        )

    def test_formula_evaluation_uses_decimal_and_allowlist(self) -> None:
        calculation = self.alpha["claims"][1]["calculation"]
        self.assertEqual(
            evaluate_formula(calculation["formula"], calculation["operands"]),
            360000,
        )
        with self.assertRaises(CompareError) as caught:
            evaluate_formula("__import__('os').system('echo no')", calculation["operands"])
        self.assertEqual(caught.exception.code, "UNSUPPORTED_FORMULA")

    def test_auto_alignment_is_exact_only_and_order_independent(self) -> None:
        beta = copy.deepcopy(self.beta)
        beta["claims"] = [copy.deepcopy(self.alpha["claims"][0])]
        beta["claims"][0]["claim_id"] = "CLM-BETA-EXACT-0001"
        beta["claims"][0]["evidence_ids"] = self.alpha["claims"][0]["evidence_ids"]
        alpha = copy.deepcopy(self.alpha)
        alpha["claims"] = [alpha["claims"][0]]
        left = compare_records(
            copy.deepcopy(self.case),
            [alpha, beta],
            reference_analysis_id=alpha["record_id"],
        )
        right = compare_records(
            copy.deepcopy(self.case),
            [beta, alpha],
            reference_analysis_id=alpha["record_id"],
        )
        self.assertEqual(canonical_bytes(left), canonical_bytes(right))
        self.assertEqual(left["relation_groups"][0]["classification"], "INVARIANT")

    def test_alignment_must_cover_every_claim_exactly_once(self) -> None:
        broken = copy.deepcopy(self.alignment)
        broken["groups"] = broken["groups"][:-1]
        with self.assertRaises(CompareError) as caught:
            compare_records(self.case, [self.alpha, self.beta], alignment_plan=broken)
        self.assertEqual(caught.exception.code, "UNALIGNED_CLAIMS")

    def test_exact_mode_rejects_nonidentical_payloads(self) -> None:
        broken = copy.deepcopy(self.alignment)
        broken["groups"][0]["mode"] = "EXACT"
        with self.assertRaises(CompareError) as caught:
            compare_records(self.case, [self.alpha, self.beta], alignment_plan=broken)
        self.assertEqual(caught.exception.code, "EXACT_ALIGNMENT_MISMATCH")

    def test_schema_rejects_unconfirmed_analysis(self) -> None:
        broken = copy.deepcopy(self.beta)
        broken["human_confirmation"]["status"] = "PENDING"
        with self.assertRaises(CompareError) as caught:
            compare_records(self.case, [self.alpha, broken], alignment_plan=self.alignment)
        self.assertEqual(caught.exception.code, "SCHEMA_VALIDATION_FAILED")

    def test_cli_writes_canonical_output_and_hash(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "comparison.json"
            command = [
                sys.executable,
                str(ROOT / "scripts/nexah_compare.py"),
                "compare",
                "--case",
                str(ROOT / "fixtures/positive/case.json"),
                "--analysis",
                str(ROOT / "fixtures/positive/analysis-a.json"),
                "--analysis",
                str(ROOT / "fixtures/positive/analysis-b.json"),
                "--alignment",
                str(ROOT / "runtime_fixtures/market-entry-alignment.json"),
                "--output",
                str(output),
            ]
            completed = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            summary = json.loads(completed.stdout)
            record = load_json(output)
            self.assertEqual(summary["comparison_sha256"], canonical_sha256(record))
            self.assertEqual(output.read_bytes(), canonical_bytes(record))


if __name__ == "__main__":
    unittest.main()
