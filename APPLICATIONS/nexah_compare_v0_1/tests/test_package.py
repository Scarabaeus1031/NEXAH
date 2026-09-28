from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from nexah_compare.package import (  # noqa: E402
    create_return,
    render_markdown,
    run_package,
    verify_package,
)
from nexah_compare.runtime import CompareError, canonical_bytes, load_json  # noqa: E402


class PackageTests(unittest.TestCase):
    def assemble(self, parent: Path) -> Path:
        package = parent / "case-package"
        (package / "inputs/analyses").mkdir(parents=True)
        (package / "evidence").mkdir()
        market = b"year,growth_percent\n2026,5.0\n"
        cost = b'{"annual_cost":"360000","currency":"EUR"}\n'
        (package / "evidence/market.csv").write_bytes(market)
        (package / "evidence/cost-model.json").write_bytes(cost)
        case = copy.deepcopy(load_json(ROOT / "fixtures/positive/case.json"))
        case["evidence"][0]["sha256"] = hashlib.sha256(market).hexdigest()
        case["evidence"][1]["sha256"] = hashlib.sha256(cost).hexdigest()
        (package / "inputs/case.json").write_bytes(canonical_bytes(case))
        (package / "inputs/analyses/alpha.json").write_bytes(
            canonical_bytes(load_json(ROOT / "fixtures/positive/analysis-a.json"))
        )
        (package / "inputs/analyses/beta.json").write_bytes(
            canonical_bytes(load_json(ROOT / "fixtures/positive/analysis-b.json"))
        )
        (package / "inputs/alignment.json").write_bytes(
            canonical_bytes(load_json(ROOT / "runtime_fixtures/market-entry-alignment.json"))
        )
        descriptor = {
            "schema_id": "nexah.compare.case-package",
            "schema_version": "0.1.0",
            "package_id": "PKG-MARKET-ENTRY-0001",
            "profile_id": "NC01-ADVISORY-0.1",
            "privacy_class": "SYNTHETIC",
            "case_path": "inputs/case.json",
            "analysis_paths": [
                "inputs/analyses/alpha.json",
                "inputs/analyses/beta.json",
            ],
            "alignment_path": "inputs/alignment.json",
            "reference_analysis_id": "AN-MARKET-ENTRY-ALPHA",
            "comparison_path": "outputs/comparison.json",
            "report_path": "outputs/report.md",
            "manifest_path": "manifest.json",
            "receipt_path": "receipts/run-receipt.json",
            "return_path": "returns/return.json",
        }
        (package / "package.json").write_bytes(canonical_bytes(descriptor))
        return package

    def test_run_seal_verify_and_replay_are_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            package = self.assemble(Path(directory))
            first = run_package(package)
            receipt = (package / "receipts/run-receipt.json").read_bytes()
            report = (package / "outputs/report.md").read_bytes()
            second = run_package(package)
            self.assertEqual(first, second)
            self.assertEqual(receipt, (package / "receipts/run-receipt.json").read_bytes())
            self.assertEqual(report, (package / "outputs/report.md").read_bytes())
            self.assertEqual(verify_package(package), first)

    def test_markdown_is_exact_projection_of_comparison(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            package = self.assemble(Path(directory))
            run_package(package)
            comparison = load_json(package / "outputs/comparison.json")
            self.assertEqual(
                (package / "outputs/report.md").read_bytes(), render_markdown(comparison)
            )
            for relation in comparison["relation_groups"]:
                self.assertIn(relation["relation_id"], (package / "outputs/report.md").read_text())

    def test_evidence_tamper_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            package = self.assemble(Path(directory))
            run_package(package)
            (package / "evidence/market.csv").write_bytes(b"tampered\n")
            with self.assertRaises(CompareError) as caught:
                verify_package(package)
            self.assertEqual(caught.exception.code, "EVIDENCE_HASH_MISMATCH")

    def test_undeclared_file_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            package = self.assemble(Path(directory))
            (package / "private-notes.txt").write_text("must not leak", encoding="utf-8")
            with self.assertRaises(CompareError) as caught:
                run_package(package)
            self.assertEqual(caught.exception.code, "UNDECLARED_PACKAGE_FILE")

    def test_symlinked_evidence_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            package = self.assemble(Path(directory))
            evidence = package / "evidence/market.csv"
            target = package / "evidence/market-real.csv"
            evidence.rename(target)
            evidence.symlink_to(target.name)
            with self.assertRaises(CompareError) as caught:
                run_package(package)
            self.assertEqual(caught.exception.code, "PACKAGE_SYMLINK_REJECTED")

    def test_human_return_is_separate_hash_bound_and_verified(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            package = self.assemble(Path(directory))
            run_package(package)
            returned = create_return(
                package,
                action="ABSTAIN",
                actor_id="ACTOR-OWNER-01",
                statement="Resolve the time-basis mismatch before deciding.",
                returned_at="2026-09-28T10:00:00Z",
                selected_residual_ids=["RES-MARKET-ENTRY-0002"],
            )
            self.assertEqual(returned["human_action"], "ABSTAIN")
            self.assertEqual(verify_package(package)["human_return"], "ABSTAIN")
            with self.assertRaises(CompareError) as caught:
                run_package(package)
            self.assertEqual(caught.exception.code, "EXISTING_RETURN_BLOCKS_RERUN")

    def test_cli_runs_and_verifies_package(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            package = self.assemble(Path(directory))
            base = [sys.executable, str(ROOT / "scripts/nexah_compare.py")]
            run = subprocess.run(
                [*base, "run-package", "--package", str(package)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertEqual(json.loads(run.stdout)["status"], "VALID")
            verify = subprocess.run(
                [*base, "verify-package", "--package", str(package)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(verify.returncode, 0, verify.stderr)
            self.assertEqual(json.loads(verify.stdout)["status"], "VALID")


if __name__ == "__main__":
    unittest.main()
