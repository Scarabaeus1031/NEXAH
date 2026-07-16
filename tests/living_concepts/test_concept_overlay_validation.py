from copy import deepcopy
from pathlib import Path

import pytest
import yaml

from nexah.living_concepts import ConceptOverlay, ConceptOverlayError
from nexah.living_concepts.overlay import accepted_overlay_path


def accepted_data() -> dict:
    return yaml.safe_load(accepted_overlay_path().read_text(encoding="utf-8"))


def load_mutation(tmp_path: Path, data: dict) -> None:
    path = tmp_path / "overlay.yaml"
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    ConceptOverlay.load(path)


def test_rejects_canonical_overlay(tmp_path):
    data = accepted_data()
    data["canonical"] = True
    with pytest.raises(ConceptOverlayError, match="non-canonical"):
        load_mutation(tmp_path, data)


def test_rejects_permanent_concept_identity(tmp_path):
    data = accepted_data()
    data["concepts"][0]["handle"] = "NX-C-000001"
    with pytest.raises(ConceptOverlayError, match="Permanent NX-C"):
        load_mutation(tmp_path, data)


def test_rejects_unaccepted_overlay(tmp_path):
    data = accepted_data()
    data["status"] = "human_review_required"
    with pytest.raises(ConceptOverlayError, match="not an accepted editorial baseline"):
        load_mutation(tmp_path, data)


def test_rejects_duplicate_concept_handles(tmp_path):
    data = accepted_data()
    data["concepts"].append(deepcopy(data["concepts"][0]))
    with pytest.raises(ConceptOverlayError, match="Duplicate concept key"):
        load_mutation(tmp_path, data)


def test_rejects_duplicate_question_bindings(tmp_path):
    data = accepted_data()
    data["question_bindings"].append(deepcopy(data["question_bindings"][0]))
    with pytest.raises(ConceptOverlayError, match="Duplicate question binding key"):
        load_mutation(tmp_path, data)


def test_rejects_unknown_operator_reference(tmp_path):
    data = accepted_data()
    data["concepts"][1]["existing_operator_ref"] = "NX-OP-9999"
    with pytest.raises(ConceptOverlayError, match="Unknown Operator reference"):
        load_mutation(tmp_path, data)


def test_rejects_canonical_relation(tmp_path):
    data = accepted_data()
    data["relations"][0]["status"] = "canonical"
    with pytest.raises(ConceptOverlayError, match="must remain review_only"):
        load_mutation(tmp_path, data)


def test_rejects_path_without_curated_status(tmp_path):
    data = accepted_data()
    data["paths"][0].pop("status")
    with pytest.raises(ConceptOverlayError, match="must remain curated"):
        load_mutation(tmp_path, data)


def test_rejects_missing_explain_disclosures(tmp_path):
    data = accepted_data()
    data["question_bindings"][0]["explain_disclosures"] = []
    with pytest.raises(ConceptOverlayError, match="lacks Explain disclosures"):
        load_mutation(tmp_path, data)


def test_rejects_missing_occurrence_provenance(tmp_path):
    data = accepted_data()
    data["occurrences"][0].pop("assertion_origin")
    with pytest.raises(ConceptOverlayError, match="lacks provenance fields"):
        load_mutation(tmp_path, data)


def test_rejects_mutation_permission(tmp_path):
    data = accepted_data()
    data["authority"]["modifies_kernel"] = True
    with pytest.raises(ConceptOverlayError, match="modifies_kernel: false"):
        load_mutation(tmp_path, data)


def test_rejects_claim_support_escalation(tmp_path):
    data = accepted_data()
    data["occurrences"][0]["claim_support"] = "validated_universally"
    with pytest.raises(ConceptOverlayError, match="escalates or invents claim support"):
        load_mutation(tmp_path, data)


def test_rejects_balance_collapsed_into_single_concept(tmp_path):
    data = accepted_data()
    balance = next(item for item in data["concepts"] if item["handle"] == "concept:balance")
    balance["maturity"] = "canonical_unified_concept"
    with pytest.raises(ConceptOverlayError, match="multiple_related_models"):
        load_mutation(tmp_path, data)


def test_adapter_load_does_not_mutate_overlay_file():
    path = accepted_overlay_path()
    before = path.read_bytes()
    ConceptOverlay.load(path)
    after = path.read_bytes()
    assert before == after

