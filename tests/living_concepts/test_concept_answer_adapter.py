from pathlib import Path

import yaml

from nexah.living_concepts import ConceptAnswerAdapter, ConceptOverlay
from nexah.living_concepts.cli import main


ROOT = Path(__file__).resolve().parents[2]
EXPECTED_PATH = (
    ROOT
    / "EDITORIAL_OPERATING_SYSTEM"
    / "living_concepts"
    / "overlay"
    / "concept_overlay_v0_1_expected_answers.yaml"
)


def load_expected() -> dict:
    return yaml.safe_load(EXPECTED_PATH.read_text(encoding="utf-8"))


def reader_meaning_fields(response: dict) -> dict:
    return {
        "state": response["state"],
        "answer": response["answer"],
        "status_note": response["status_note"],
        "paths": [
            {
                "name": path["name"],
                "status": path["status"],
                "labels": [step["label"] for step in path["steps"]],
            }
            for path in response.get("paths", [])
        ],
    }


def explain_meaning_fields(response: dict) -> dict:
    return {
        "concept_handles": response["concept_handles"],
        "operator_bindings": response["operator_bindings"],
        "occurrence_ids": [item["occurrence_id"] for item in response["occurrences"]],
        "claim_support": [item["claim_support"] for item in response["occurrences"]],
        "relations": [
            {"relation_id": item["relation_id"], "status": item["status"]}
            for item in response["relations"]
        ],
        "paths": [
            {
                "path_id": item["path_id"],
                "status": item["status"],
                "canonical_relation": item["canonical_relation"],
            }
            for item in response["paths"]
        ],
        "disclosures": response["disclosures"],
    }


def test_all_six_reader_and_explain_contracts_match_accepted_baseline():
    adapter = ConceptAnswerAdapter(ConceptOverlay.load())
    expected = load_expected()

    assert expected["canonical"] is False
    assert expected["overlay_id"] == adapter.overlay.overlay_id
    assert [item["question_key"] for item in expected["questions"]] == [
        f"CFQ-{value:02d}" for value in range(1, 7)
    ]

    for contract in expected["questions"]:
        key = contract["question_key"]
        reader = adapter.answer(key, mode="reader")
        explain = adapter.answer(key, mode="explain")
        assert reader["authority_class"] == contract["authority_class"]
        assert explain["authority_class"] == contract["authority_class"]
        assert reader["non_canonical"] is True
        assert explain["non_canonical"] is True
        assert reader_meaning_fields(reader) == contract["reader"]
        assert explain_meaning_fields(explain) == contract["explain"]


def test_reader_mode_hides_internal_provenance_and_operator_ids():
    adapter = ConceptAnswerAdapter.load()
    forbidden = {
        "overlay_id",
        "concept_handles",
        "operator_bindings",
        "occurrences",
        "relations",
        "disclosures",
        "confidence",
        "claim_support",
    }

    for value in range(1, 7):
        response = adapter.answer(f"CFQ-{value:02d}", mode="reader")
        assert forbidden.isdisjoint(response)
        assert "NX-OP-" not in repr(response)
        assert "/" not in response["answer"]


def test_explain_mode_preserves_provenance_and_noncanonical_status():
    adapter = ConceptAnswerAdapter.load()
    for value in range(1, 7):
        response = adapter.answer(f"CFQ-{value:02d}", mode="explain")
        assert response["answer_source_type"] == "accepted_overlay_question_contract"
        assert response["non_canonical"] is True
        assert response["occurrences"]
        assert response["disclosures"]
        for occurrence in response["occurrences"]:
            assert occurrence["source"]
            assert occurrence["assertion_origin"]
            assert occurrence["claim_support"]
        assert all(item["status"] == "review_only" for item in response["relations"])
        assert all(item["status"] == "curated" for item in response["paths"])
        assert all(item["canonical_relation"] is False for item in response["paths"])


def test_balance_remains_multiple_related_models():
    adapter = ConceptAnswerAdapter.load()
    reader = adapter.answer("CFQ-06", mode="reader")
    explain = adapter.answer("CFQ-06", mode="explain")

    assert reader["authority_class"] == "multiple_related_models"
    assert "not one fixed" in reader["answer"]
    assert "intentionally uncollapsed" in reader["status_note"]
    assert "outcome_is_multiple_related_models" in explain["disclosures"]
    assert "multiple_related_models" in {
        item["claim_support"] for item in explain["occurrences"]
    }


def test_unknown_question_and_mode_return_structured_unsupported_result():
    adapter = ConceptAnswerAdapter.load()

    question = adapter.answer("CFQ-07")
    mode = adapter.answer("CFQ-01", mode="semantic")
    assert question == {
        "mode": "unsupported",
        "question_key": "CFQ-07",
        "state": "unsupported",
        "authority_class": "unsupported",
        "reason": (
            "The read-only Concept Answer Adapter supports only the six "
            "accepted pilot contracts in version 0.1."
        ),
    }
    assert mode["state"] == "unsupported"
    assert mode["authority_class"] == "unsupported"


def test_cli_requires_explicit_module_and_returns_structured_json(capsys):
    assert main(["answer", "CFQ-01", "--mode", "reader"]) == 0
    output = yaml.safe_load(capsys.readouterr().out)
    assert output["question_key"] == "CFQ-01"
    assert output["state"] == "answered"

    assert main(["answer", "CFQ-99", "--mode", "reader"]) == 2
    output = yaml.safe_load(capsys.readouterr().out)
    assert output["state"] == "unsupported"

