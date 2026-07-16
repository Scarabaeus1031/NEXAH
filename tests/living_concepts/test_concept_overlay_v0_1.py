from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
OVERLAY_PATH = (
    ROOT
    / "EDITORIAL_OPERATING_SYSTEM"
    / "living_concepts"
    / "overlay"
    / "concept_overlay_v0_1.yaml"
)
BASELINE_PATH = (
    ROOT
    / "EDITORIAL_OPERATING_SYSTEM"
    / "living_concepts"
    / "review"
    / "transition_geometry"
    / "transition_geometry_concept_family_test.yaml"
)


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_overlay_is_explicitly_noncanonical_and_nonmutating():
    overlay = load_yaml(OVERLAY_PATH)

    assert overlay["canonical"] is False
    assert overlay["load_policy"] == "manual_evaluation_only"
    assert overlay["authority"] == {
        "modifies_registry": False,
        "allocates_identities": False,
        "modifies_operators": False,
        "creates_canonical_graph_edges": False,
        "modifies_kernel": False,
        "writes_to_arena": False,
        "inference_from_cooccurrence": "prohibited",
    }


def test_overlay_contains_exactly_seven_unique_pilot_handles():
    overlay = load_yaml(OVERLAY_PATH)
    handles = [concept["handle"] for concept in overlay["concepts"]]

    assert len(handles) == len(set(handles)) == 7
    assert set(handles) == {
        "concept:transition-geometry",
        "concept:janus",
        "concept:aperture",
        "concept:inbetween",
        "concept:boundary",
        "concept:transition",
        "concept:balance",
    }
    assert not any(handle.startswith("NX-C-") for handle in handles)


def test_existing_operator_profiles_bind_without_allocating_new_identities():
    overlay = load_yaml(OVERLAY_PATH)
    concepts = {concept["handle"]: concept for concept in overlay["concepts"]}
    expected = {
        "concept:aperture": "NX-OP-0002",
        "concept:boundary": "NX-OP-0006",
        "concept:transition": "NX-OP-0005",
    }

    for handle, operator_ref in expected.items():
        concept = concepts[handle]
        assert concept["identity_state"] == "bound_to_existing_operator"
        assert concept["existing_operator_ref"] == operator_ref
        operator_path = ROOT / "LIBRARY" / "registry" / "concepts" / f"{operator_ref}.yaml"
        assert operator_path.exists()
        assert load_yaml(operator_path)["id"] == operator_ref

    assert concepts["concept:janus"]["existing_operator_ref"] == "NX-OP-0016"
    assert concepts["concept:balance"]["maturity"] == "multiple_related_models"


def test_occurrences_relations_and_paths_resolve_inside_overlay():
    overlay = load_yaml(OVERLAY_PATH)
    handles = {concept["handle"] for concept in overlay["concepts"]}
    occurrences = {
        occurrence["occurrence_id"]: occurrence for occurrence in overlay["occurrences"]
    }
    relations = {
        relation["relation_id"]: relation for relation in overlay["relations"]
    }
    paths = {path["path_id"]: path for path in overlay["paths"]}

    assert len(occurrences) == 13
    assert len(relations) == 2
    assert len(paths) == 3

    for occurrence in occurrences.values():
        assert occurrence["concept"] in handles
        assert occurrence["verification"] == "verified"
        assert occurrence["assertion_origin"]
        assert occurrence["claim_support"]

    for relation in relations.values():
        assert relation["subject"] in handles
        assert relation["object"] in handles
        assert relation["status"] == "review_only"
        assert relation["qualification"]
        assert all(ref in occurrences for ref in relation["evidence_refs"])

    for path in paths.values():
        assert path["status"] == "curated"
        assert path["canonical_relation"] is False
        assert path["focus"] in handles
        assert all(ref in occurrences for ref in path["evidence_refs"])


def test_question_bindings_reproduce_six_human_baseline_results():
    overlay = load_yaml(OVERLAY_PATH)
    baseline = load_yaml(BASELINE_PATH)
    concepts = {concept["handle"] for concept in overlay["concepts"]}
    occurrences = {item["occurrence_id"] for item in overlay["occurrences"]}
    relations = {item["relation_id"] for item in overlay["relations"]}
    paths = {item["path_id"] for item in overlay["paths"]}
    questions = {item["question_id"]: item for item in overlay["question_bindings"]}
    expected_results = {item["id"]: item["result"] for item in baseline["tests"]}

    assert set(questions) == set(expected_results) == {
        "CFQ-01",
        "CFQ-02",
        "CFQ-03",
        "CFQ-04",
        "CFQ-05",
        "CFQ-06",
    }

    for question_id, question in questions.items():
        assert question["expected_result"] == expected_results[question_id]
        assert question["reader_answer"].strip()
        assert question["explain_disclosures"]
        assert question["focus"] in concepts
        assert set(question["basis"]["concept_refs"]) <= concepts
        assert set(question["basis"]["occurrence_refs"]) <= occurrences
        assert set(question["basis"]["relation_refs"]) <= relations
        assert set(question["basis"]["path_refs"]) <= paths


def test_registry_counts_remain_frozen():
    entity_files = list((ROOT / "LIBRARY" / "registry" / "entities").glob("NX-*.yaml"))
    operator_files = list((ROOT / "LIBRARY" / "registry" / "concepts").glob("NX-OP-*.yaml"))

    assert len(entity_files) == 10
    assert len(operator_files) == 17

