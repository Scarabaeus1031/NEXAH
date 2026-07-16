from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import yaml


SCHEMA_VERSION = "0.1-proposal"
OVERLAY_ID = "living-concepts-transition-geometry-pilot-v0.1"
ACCEPTED_STATUS = "editorial_baseline_accepted"
PILOT_QUESTION_KEYS = {f"CFQ-{value:02d}" for value in range(1, 7)}
REQUIRED_ACCEPTED_SCOPE = {
    "overlay_schema",
    "reviewed_concept_handles",
    "documentary_occurrences",
    "review_only_relations",
    "curated_paths",
    "reader_answer_contracts",
    "explain_answer_contracts",
    "six_question_baseline_evaluation",
}
REQUIRED_EXCLUSIONS = {
    "canonical_concept_identity",
    "registry_integration",
    "operator_mutation",
    "graph_truth",
    "automatic_inference",
    "general_kernel_runtime_integration",
    "arena_mutation",
}
PROHIBITED_MUTATION_FLAGS = {
    "modifies_registry": False,
    "allocates_identities": False,
    "modifies_operators": False,
    "creates_canonical_graph_edges": False,
    "modifies_kernel": False,
    "writes_to_arena": False,
}
ALLOWED_CLAIM_SUPPORT = {
    "authored_conceptual_synthesis",
    "supported_architectural_boundary",
    "reviewed_conceptual_synthesis",
    "supported_within_declared_research_scope",
    "authored_visual_explanation",
    "authored_whiteboard_statement",
    "authored_process_taxonomy",
    "authored_whiteboard_sequence",
    "relational_balance_work_model",
    "directional_balance_work_model",
    "multiple_related_models",
}
REQUIRED_DISCLOSURES = {
    "CFQ-01": {
        "declared_representation_not_reality",
        "representation_independent_transition_space_not_supported",
    },
    "CFQ-02": {
        "relation_is_review_only",
        "janus_identity_layers_remain_distinct",
    },
    "CFQ-03": {
        "route_is_human_curated",
        "no_canonical_inbetween_identity",
    },
    "CFQ-04": {
        "path_is_human_curated_not_a_graph_edge",
        "path_is_not_a_deterministic_state_machine",
        "core_recurrence_remains_a_hypothesis",
    },
    "CFQ-05": {
        "operator_record_remains_authoritative",
        "work_explanation_is_distinct_from_research_support",
    },
    "CFQ-06": {
        "outcome_is_multiple_related_models",
        "no_balance_concept_identity_or_graph_edge",
        "balance_remains_distinct_from_adjacent_terms",
    },
}


class ConceptOverlayError(RuntimeError):
    """Raised when an Overlay violates the accepted editorial contract."""


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def accepted_overlay_path() -> Path:
    return (
        project_root()
        / "EDITORIAL_OPERATING_SYSTEM"
        / "living_concepts"
        / "overlay"
        / "concept_overlay_v0_1.yaml"
    )


def _mapping_by_unique_key(
    records: Any, key: str, label: str
) -> dict[str, dict[str, Any]]:
    if not isinstance(records, list) or not records:
        raise ConceptOverlayError(f"Overlay requires a non-empty {label} list")
    result: dict[str, dict[str, Any]] = {}
    for record in records:
        if not isinstance(record, dict) or not isinstance(record.get(key), str):
            raise ConceptOverlayError(f"Every {label} record requires {key}")
        value = record[key]
        if value in result:
            raise ConceptOverlayError(f"Duplicate {label} key {value}")
        result[value] = record
    return result


def _contains_permanent_concept_id(value: Any) -> bool:
    if isinstance(value, str):
        return value.startswith("NX-C-")
    if isinstance(value, list):
        return any(_contains_permanent_concept_id(item) for item in value)
    if isinstance(value, dict):
        return any(
            _contains_permanent_concept_id(key)
            or _contains_permanent_concept_id(item)
            for key, item in value.items()
        )
    return False


class ConceptOverlay:
    """Validated, read-only view of the accepted Concept Overlay pilot."""

    def __init__(self, source_path: Path, data: dict[str, Any]):
        self.source_path = source_path
        self._data = deepcopy(data)
        self.concepts = _mapping_by_unique_key(data.get("concepts"), "handle", "concept")
        self.occurrences = _mapping_by_unique_key(
            data.get("occurrences"), "occurrence_id", "occurrence"
        )
        self.relations = _mapping_by_unique_key(
            data.get("relations"), "relation_id", "relation"
        )
        self.paths = _mapping_by_unique_key(data.get("paths"), "path_id", "path")
        self.question_bindings = _mapping_by_unique_key(
            data.get("question_bindings"), "question_id", "question binding"
        )
        self._validate()

    @classmethod
    def load(cls, path: Path | str | None = None) -> "ConceptOverlay":
        source_path = Path(path) if path is not None else accepted_overlay_path()
        try:
            value = yaml.safe_load(source_path.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError) as exc:
            raise ConceptOverlayError(f"Cannot read Concept Overlay {source_path}: {exc}") from exc
        if not isinstance(value, dict):
            raise ConceptOverlayError("Concept Overlay root must be a mapping")
        return cls(source_path, value)

    @property
    def overlay_id(self) -> str:
        return self._data["overlay_id"]

    @property
    def canonical(self) -> bool:
        return self._data["canonical"]

    def binding(self, question_key: str) -> dict[str, Any] | None:
        binding = self.question_bindings.get(question_key)
        return deepcopy(binding) if binding is not None else None

    def concept(self, handle: str) -> dict[str, Any]:
        return deepcopy(self.concepts[handle])

    def occurrence(self, occurrence_id: str) -> dict[str, Any]:
        return deepcopy(self.occurrences[occurrence_id])

    def relation(self, relation_id: str) -> dict[str, Any]:
        return deepcopy(self.relations[relation_id])

    def path(self, path_id: str) -> dict[str, Any]:
        return deepcopy(self.paths[path_id])

    def _validate(self) -> None:
        data = self._data
        if data.get("schema_version") != SCHEMA_VERSION:
            raise ConceptOverlayError(f"Unsupported schema_version {data.get('schema_version')}")
        if data.get("overlay_id") != OVERLAY_ID:
            raise ConceptOverlayError(f"Unsupported overlay_id {data.get('overlay_id')}")
        if data.get("status") != ACCEPTED_STATUS:
            raise ConceptOverlayError("Concept Overlay is not an accepted editorial baseline")
        if data.get("canonical") is not False:
            raise ConceptOverlayError("Concept Overlay must remain non-canonical")
        if data.get("load_policy") != "manual_evaluation_only":
            raise ConceptOverlayError("Concept Overlay load policy must remain manual_evaluation_only")
        if _contains_permanent_concept_id(data):
            raise ConceptOverlayError("Permanent NX-C identities are prohibited in the pilot Overlay")
        self._validate_acceptance()
        self._validate_authority()
        self._validate_concepts()
        self._validate_occurrences()
        self._validate_relations()
        self._validate_paths()
        self._validate_question_bindings()
        self._validate_balance_boundary()

    def _validate_acceptance(self) -> None:
        acceptance = self._data.get("editorial_acceptance")
        if not isinstance(acceptance, dict) or acceptance.get("state") != "accepted_baseline":
            raise ConceptOverlayError("Accepted editorial state is required")
        if not acceptance.get("accepted_at"):
            raise ConceptOverlayError("Editorial acceptance date is required")
        if set(acceptance.get("accepted_scope", [])) != REQUIRED_ACCEPTED_SCOPE:
            raise ConceptOverlayError("Editorial accepted_scope does not match the pilot contract")
        if set(acceptance.get("explicitly_excluded", [])) != REQUIRED_EXCLUSIONS:
            raise ConceptOverlayError("Editorial exclusions do not match the pilot contract")

    def _validate_authority(self) -> None:
        authority = self._data.get("authority")
        if not isinstance(authority, dict):
            raise ConceptOverlayError("Overlay authority block is required")
        for flag, required in PROHIBITED_MUTATION_FLAGS.items():
            if authority.get(flag) is not required:
                raise ConceptOverlayError(f"Overlay authority must keep {flag}: false")
        if authority.get("inference_from_cooccurrence") != "prohibited":
            raise ConceptOverlayError("Inference from co-occurrence must remain prohibited")

    def _validate_concepts(self) -> None:
        if len(self.concepts) != 7:
            raise ConceptOverlayError("Accepted pilot requires exactly seven Concept handles")
        operator_root = project_root() / "LIBRARY" / "registry" / "concepts"
        for handle, concept in self.concepts.items():
            if not handle.startswith("concept:"):
                raise ConceptOverlayError(f"Invalid local Concept handle {handle}")
            operator_ref = concept.get("existing_operator_ref")
            if operator_ref is None:
                continue
            operator_path = operator_root / f"{operator_ref}.yaml"
            try:
                operator = yaml.safe_load(operator_path.read_text(encoding="utf-8"))
            except (OSError, yaml.YAMLError) as exc:
                raise ConceptOverlayError(f"Unknown Operator reference {operator_ref}") from exc
            if not isinstance(operator, dict) or operator.get("id") != operator_ref:
                raise ConceptOverlayError(f"Unknown Operator reference {operator_ref}")

    def _validate_occurrences(self) -> None:
        required = {
            "concept",
            "source",
            "locator",
            "role",
            "verification",
            "assertion_origin",
            "claim_support",
        }
        for occurrence_id, occurrence in self.occurrences.items():
            if not required <= occurrence.keys():
                missing = sorted(required - occurrence.keys())
                raise ConceptOverlayError(
                    f"Occurrence {occurrence_id} lacks provenance fields: {', '.join(missing)}"
                )
            if occurrence["concept"] not in self.concepts:
                raise ConceptOverlayError(
                    f"Occurrence {occurrence_id} references unknown Concept handle"
                )
            if occurrence["verification"] != "verified":
                raise ConceptOverlayError(
                    f"Occurrence {occurrence_id} is not verified for accepted pilot use"
                )
            if occurrence["claim_support"] not in ALLOWED_CLAIM_SUPPORT:
                raise ConceptOverlayError(
                    f"Occurrence {occurrence_id} escalates or invents claim support"
                )

    def _validate_relations(self) -> None:
        for relation_id, relation in self.relations.items():
            if relation.get("status") != "review_only":
                raise ConceptOverlayError(f"Relation {relation_id} must remain review_only")
            if relation.get("subject") not in self.concepts or relation.get("object") not in self.concepts:
                raise ConceptOverlayError(f"Relation {relation_id} has an unknown endpoint")
            if not relation.get("qualification"):
                raise ConceptOverlayError(f"Relation {relation_id} requires a qualification")
            evidence_refs = relation.get("evidence_refs")
            if not isinstance(evidence_refs, list) or not evidence_refs:
                raise ConceptOverlayError(f"Relation {relation_id} requires provenance")
            if any(ref not in self.occurrences for ref in evidence_refs):
                raise ConceptOverlayError(f"Relation {relation_id} has unknown evidence")

    def _validate_paths(self) -> None:
        for path_id, path in self.paths.items():
            if path.get("status") != "curated":
                raise ConceptOverlayError(f"Path {path_id} must remain curated")
            if path.get("canonical_relation") is not False:
                raise ConceptOverlayError(f"Path {path_id} must not claim a canonical relation")
            if path.get("focus") not in self.concepts:
                raise ConceptOverlayError(f"Path {path_id} has an unknown focus")
            if not path.get("steps") and not path.get("semantic_steps"):
                raise ConceptOverlayError(f"Path {path_id} requires ordered steps")
            evidence_refs = path.get("evidence_refs")
            if not isinstance(evidence_refs, list) or not evidence_refs:
                raise ConceptOverlayError(f"Path {path_id} requires provenance")
            if any(ref not in self.occurrences for ref in evidence_refs):
                raise ConceptOverlayError(f"Path {path_id} has unknown evidence")

    def _validate_question_bindings(self) -> None:
        if set(self.question_bindings) != PILOT_QUESTION_KEYS:
            raise ConceptOverlayError("Adapter accepts exactly CFQ-01 through CFQ-06")
        for question_key, binding in self.question_bindings.items():
            if not binding.get("question") or not binding.get("reader_answer"):
                raise ConceptOverlayError(f"Question contract {question_key} is incomplete")
            disclosures = binding.get("explain_disclosures")
            if not isinstance(disclosures, list) or not disclosures:
                raise ConceptOverlayError(f"Question contract {question_key} lacks Explain disclosures")
            if not REQUIRED_DISCLOSURES[question_key] <= set(disclosures):
                raise ConceptOverlayError(
                    f"Question contract {question_key} lacks required uncertainty disclosures"
                )
            if binding.get("focus") not in self.concepts:
                raise ConceptOverlayError(f"Question contract {question_key} has an unknown focus")
            basis = binding.get("basis")
            if not isinstance(basis, dict):
                raise ConceptOverlayError(f"Question contract {question_key} lacks evidence basis")
            reference_sets = {
                "concept_refs": self.concepts,
                "occurrence_refs": self.occurrences,
                "relation_refs": self.relations,
                "path_refs": self.paths,
            }
            for field, available in reference_sets.items():
                refs = basis.get(field)
                if not isinstance(refs, list):
                    raise ConceptOverlayError(
                        f"Question contract {question_key} lacks {field} provenance"
                    )
                if any(ref not in available for ref in refs):
                    raise ConceptOverlayError(
                        f"Question contract {question_key} has unresolved {field}"
                    )
            if not basis["concept_refs"] or not basis["occurrence_refs"]:
                raise ConceptOverlayError(
                    f"Question contract {question_key} requires Concept and Occurrence provenance"
                )

    def _validate_balance_boundary(self) -> None:
        balance = self.concepts.get("concept:balance", {})
        if balance.get("maturity") != "multiple_related_models":
            raise ConceptOverlayError("Balance must remain multiple_related_models")
        if balance.get("definition_status") != "comparison_summary_not_canonical_definition":
            raise ConceptOverlayError("Balance must not be collapsed into a canonical definition")
        if "no_single_balance_concept" not in balance.get("boundaries", []):
            raise ConceptOverlayError("Balance must preserve its non-unification boundary")
        binding = self.question_bindings.get("CFQ-06", {})
        if binding.get("expected_result") != "pass_with_concept_boundary":
            raise ConceptOverlayError("CFQ-06 must preserve the Balance Concept boundary")

