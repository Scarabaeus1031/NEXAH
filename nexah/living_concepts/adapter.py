from __future__ import annotations

from typing import Any

from .overlay import ConceptOverlay


MODES = {"reader", "explain"}
AUTHORITY_CLASS_BY_QUESTION = {
    "CFQ-01": "reviewed_editorial_synthesis",
    "CFQ-02": "reviewed_editorial_synthesis",
    "CFQ-03": "curated_path",
    "CFQ-04": "curated_path",
    "CFQ-05": "operator_authority",
    "CFQ-06": "multiple_related_models",
}
STATUS_NOTE_BY_RESULT = {
    "pass": "Editorially reviewed in the accepted non-canonical Overlay baseline.",
    "pass_with_editorial_synthesis": (
        "This route is human-curated editorial guidance, not a canonical graph relation."
    ),
    "pass_with_concept_boundary": (
        "The related Balance models remain intentionally uncollapsed."
    ),
}


class ConceptAnswerAdapter:
    """Resolve accepted pilot contracts without inference or mutation."""

    def __init__(self, overlay: ConceptOverlay):
        self.overlay = overlay

    @classmethod
    def load(cls, path: str | None = None) -> "ConceptAnswerAdapter":
        return cls(ConceptOverlay.load(path))

    def answer(self, question_key: str, *, mode: str = "reader") -> dict[str, Any]:
        if mode not in MODES:
            return self._unsupported(question_key, f"Unsupported answer mode {mode}.")
        binding = self.overlay.binding(question_key)
        if binding is None:
            return self._unsupported(
                question_key,
                "The read-only Concept Answer Adapter supports only the six "
                "accepted pilot contracts in version 0.1.",
            )
        if mode == "reader":
            return self.render_reader_answer(binding)
        return self.render_explain_answer(binding)

    def render_reader_answer(self, binding: dict[str, Any]) -> dict[str, Any]:
        question_key = binding["question_id"]
        result = {
            "mode": "reader",
            "question_key": question_key,
            "state": "answered",
            "authority_class": AUTHORITY_CLASS_BY_QUESTION[question_key],
            "answer": binding["reader_answer"],
            "status_note": STATUS_NOTE_BY_RESULT[binding["expected_result"]],
            "non_canonical": True,
        }
        public_paths = [
            self._public_path(self.overlay.path(path_id))
            for path_id in binding["basis"]["path_refs"]
        ]
        if public_paths:
            result["paths"] = public_paths
        return result

    def render_explain_answer(self, binding: dict[str, Any]) -> dict[str, Any]:
        question_key = binding["question_id"]
        basis = binding["basis"]
        concepts = [self.overlay.concept(ref) for ref in basis["concept_refs"]]
        occurrences = [
            self.overlay.occurrence(ref) for ref in basis["occurrence_refs"]
        ]
        relations = [self.overlay.relation(ref) for ref in basis["relation_refs"]]
        paths = [self.overlay.path(ref) for ref in basis["path_refs"]]
        return {
            "mode": "explain",
            "question_key": question_key,
            "state": "answered",
            "authority_class": AUTHORITY_CLASS_BY_QUESTION[question_key],
            "reader_answer": binding["reader_answer"],
            "answer_source_type": "accepted_overlay_question_contract",
            "overlay_id": self.overlay.overlay_id,
            "non_canonical": True,
            "concept_handles": [concept["handle"] for concept in concepts],
            "identity_states": [
                {"handle": concept["handle"], "state": concept["identity_state"]}
                for concept in concepts
            ],
            "operator_bindings": [
                {
                    "handle": concept["handle"],
                    "operator_ref": concept["existing_operator_ref"],
                }
                for concept in concepts
                if concept.get("existing_operator_ref")
            ],
            "occurrences": [self._explain_occurrence(value) for value in occurrences],
            "relations": [self._explain_relation(value) for value in relations],
            "paths": [self._explain_path(value) for value in paths],
            "disclosures": list(binding["explain_disclosures"]),
        }

    @staticmethod
    def _public_path(path: dict[str, Any]) -> dict[str, Any]:
        if path.get("steps"):
            steps = [
                {"position": index, "label": step["label"], "purpose": step["purpose"]}
                for index, step in enumerate(path["steps"], 1)
            ]
        else:
            steps = [
                {
                    "position": index,
                    "label": value.split(":", 1)[-1].replace("_", " ").title(),
                }
                for index, value in enumerate(path["semantic_steps"], 1)
            ]
        return {
            "name": path["preferred_name"],
            "status": "curated",
            "steps": steps,
        }

    @staticmethod
    def _explain_occurrence(occurrence: dict[str, Any]) -> dict[str, Any]:
        return {
            "occurrence_id": occurrence["occurrence_id"],
            "concept": occurrence["concept"],
            "source": occurrence["source"],
            "locator": occurrence["locator"],
            "role": occurrence["role"],
            "assertion_origin": occurrence["assertion_origin"],
            "claim_support": occurrence["claim_support"],
        }

    @staticmethod
    def _explain_relation(relation: dict[str, Any]) -> dict[str, Any]:
        return {
            "relation_id": relation["relation_id"],
            "subject": relation["subject"],
            "predicate": relation["predicate"],
            "object": relation["object"],
            "status": relation["status"],
            "qualification": relation["qualification"],
            "evidence_refs": list(relation["evidence_refs"]),
        }

    @staticmethod
    def _explain_path(path: dict[str, Any]) -> dict[str, Any]:
        result = {
            "path_id": path["path_id"],
            "name": path["preferred_name"],
            "status": path["status"],
            "canonical_relation": path["canonical_relation"],
            "evidence_refs": list(path["evidence_refs"]),
        }
        if path.get("steps"):
            result["steps"] = list(path["steps"])
        else:
            result["semantic_steps"] = list(path["semantic_steps"])
            result["source_route"] = list(path["source_route"])
        if path.get("boundaries"):
            result["boundaries"] = list(path["boundaries"])
        return result

    @staticmethod
    def _unsupported(question_key: str, reason: str) -> dict[str, Any]:
        return {
            "mode": "unsupported",
            "question_key": question_key,
            "state": "unsupported",
            "authority_class": "unsupported",
            "reason": reason,
        }

