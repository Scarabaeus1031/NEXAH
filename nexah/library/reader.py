from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

from .registry import Registry, project_root


QUESTION_IDS = {f"UQ-{value:02d}" for value in range(1, 7)}
MODES = {"reader", "explain"}


class ReaderOverlayError(RuntimeError):
    pass


def _yaml(path: Path) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ReaderOverlayError(f"Cannot read Reader Overlay source {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ReaderOverlayError(f"Expected a mapping in Reader Overlay source {path}")
    return value


class ReaderOverlay:
    """Explicit, non-canonical reader layer for the six Phase VI questions."""

    def __init__(
        self,
        registry: Registry,
        classification: dict[str, Any],
        editorial: dict[str, Any],
        journeys: dict[str, Any],
        discovery: dict[str, Any],
    ):
        registry.require_valid()
        self.registry = registry
        self.classification = classification
        self.editorial = editorial
        self.journeys = journeys
        self.discovery = discovery
        self.records = {
            record["arena_channel_id"]: record for record in classification["records"]
        }
        self.questions = {
            question["id"]: question for question in journeys["reader_questions"]
        }
        self.discovery_records = {
            record["arena_channel_id"]: record for record in discovery["channels"]
        }
        self._validate_overlay()

    @classmethod
    def load(
        cls, registry: Registry, review_root: Path | str | None = None
    ) -> "ReaderOverlay":
        root = Path(review_root) if review_root else project_root() / "LIBRARY" / "review"
        return cls(
            registry,
            _yaml(root / "full_library_classification.yaml"),
            _yaml(root / "editorial_sequence_review.yaml"),
            _yaml(root / "reader_journey_review.yaml"),
            _yaml(root / "full_library_discovery.yaml"),
        )

    def _validate_overlay(self) -> None:
        proposal_policy = self.classification.get("proposal_policy", {})
        if proposal_policy.get("allocates_ids") is not False:
            raise ReaderOverlayError("Reader Overlay must not allocate IDs")
        if proposal_policy.get("loads_as_canonical") is not False:
            raise ReaderOverlayError("Proposal classification must never load as canonical")
        if self.editorial.get("policy", {}).get("allocates_ids") is not False:
            raise ReaderOverlayError("Editorial review must not allocate IDs")
        if self.journeys.get("policy", {}).get("allocates_ids") is not False:
            raise ReaderOverlayError("Reader journeys must not allocate IDs")
        if set(self.questions) != QUESTION_IDS:
            raise ReaderOverlayError(
                "Reader Overlay is intentionally limited to UQ-01 through UQ-06"
            )
        if len(self.records) != len(self.classification.get("records", [])):
            raise ReaderOverlayError("Duplicate Arena IDs in Proposal classification")
        for record in self.records.values():
            if record["classification_state"] == "proposed" and record.get("registered_entity_id"):
                raise ReaderOverlayError("Proposal record may not resolve to a canonical NEXAH ID")

    def answer(self, question_id: str, *, mode: str = "reader") -> dict[str, Any]:
        if question_id not in QUESTION_IDS:
            raise ReaderOverlayError(f"Unsupported Reader question {question_id}")
        if mode not in MODES:
            raise ReaderOverlayError(f"Unsupported Reader mode {mode}")
        question = self.questions[question_id]
        if question_id == "UQ-04":
            items = self._transition_items(mode)
        elif question_id == "UQ-05":
            items = self._navigation_items(question, mode)
        else:
            items = self._configured_items(question, mode)
        if question_id == "UQ-01":
            if len(items) != 5 or any(item.get("object_family") == "navigation" for item in items):
                raise ReaderOverlayError("UQ-01 must return exactly five Works")
        return {
            "question_id": question_id,
            "prompt": question["prompt"],
            "mode": mode,
            "items": [{"position": index, **item} for index, item in enumerate(items, 1)],
            "notice": self._notice(items),
        }

    def _configured_items(self, question: dict[str, Any], mode: str) -> list[dict[str, Any]]:
        slots = {
            "UQ-01": ["entry", "learning", "foundation", "navigation", "practice"],
            "UQ-02": ["field", "field", "field"],
            "UQ-03": ["learn", "practice", "navigate", "document", "synthesize"],
            "UQ-06": ["visual", "field_atlas", "handbook", "unexpected"],
        }.get(question["id"], [])
        return [
            self._entity_item(
                self.records[result["arena_channel_id"]],
                mode=mode,
                note=self._note(
                    question["id"], index, slots[index] if index < len(slots) else None
                ),
                evidence=self._configured_evidence(question, result),
                curatorial_slot=slots[index] if index < len(slots) else None,
            )
            for index, result in enumerate(question.get("expected_results", []))
        ]

    def _transition_items(self, mode: str) -> list[dict[str, Any]]:
        operator_id = "NX-OP-0005"
        canonical = [
            self._canonical_item(
                entity,
                mode=mode,
                note="Transition is explicitly curated for this Work.",
                evidence=[
                    {
                        "class": "canonical_operator_reference",
                        "source": f"LIBRARY/registry/entities/{entity['id']}.yaml",
                        "operator_id": operator_id,
                    }
                ],
            )
            for entity in sorted(self.registry.entities.values(), key=lambda value: value["id"])
            if operator_id in entity.get("core_operator_refs", [])
        ]
        inferred: list[dict[str, Any]] = []
        for channel_id, record in sorted(self.records.items()):
            if record["classification_state"] != "proposed" or record["object_family"] != "work":
                continue
            description = self.discovery_records.get(channel_id, {}).get("current_description", "")
            if not re.search(r"\btransition(?:s|al)?\b", description, re.I):
                continue
            inferred.append(
                self._entity_item(
                    record,
                    mode=mode,
                    note=(
                        "Its public description mentions Transition; Operator use is not "
                        "yet confirmed."
                    ),
                    evidence=[
                        {
                            "class": "inferred_description_match",
                            "source": "LIBRARY/review/full_library_discovery.yaml",
                            "term": "Transition",
                        }
                    ],
                    state="inferred",
                )
            )
        return canonical + inferred

    def _navigation_items(self, question: dict[str, Any], mode: str) -> list[dict[str, Any]]:
        series_name = question["expected_series"][0]
        series = next(
            value for value in self.editorial["series"] if value["series"] == series_name
        )
        if series["review_state"] != "confirmed":
            raise ReaderOverlayError(f"Series {series_name} is not human-confirmed")
        series_item: dict[str, Any] = {
            "title": series_name,
            "state": "proposal",
            "object_family": "navigation",
            "note": "Begin with its confirmed four-volume sequence.",
        }
        if mode == "explain":
            series_item.update(
                {
                    "reference": f"series:{series_name}",
                    "evidence": [
                        {
                            "class": "confirmed_series",
                            "source": "LIBRARY/review/editorial_sequence_review.yaml",
                            "review_state": series["review_state"],
                        }
                    ],
                    "sequence": [member["title"] for member in series["ordered_members"]],
                }
            )
        companions = [
            self._entity_item(
                self.records[result["arena_channel_id"]],
                mode=mode,
                note="Use this as a complementary navigation map.",
                evidence=[
                    {
                        "class": "curated_reader_companion",
                        "source": "LIBRARY/review/reader_journey_review.yaml",
                    }
                ],
            )
            for result in question.get("expected_companions", [])
        ]
        return [series_item, *companions]

    def _canonical_item(
        self,
        entity: dict[str, Any],
        *,
        mode: str,
        note: str,
        evidence: list[dict[str, Any]],
    ) -> dict[str, Any]:
        item = {
            "title": entity["canonical_title"],
            "state": "canonical",
            "object_family": entity["object_family"],
            "note": note,
        }
        if mode == "explain":
            item.update(
                {
                    "reference": entity["id"],
                    "type": entity["type"],
                    "form": entity["form"],
                    "library_function": entity["library_function"],
                    "publication_status": entity["publication_status"],
                    "evidence": evidence,
                }
            )
        return item

    def _entity_item(
        self,
        record: dict[str, Any],
        *,
        mode: str,
        note: str,
        evidence: list[dict[str, Any]],
        state: str | None = None,
        curatorial_slot: str | None = None,
    ) -> dict[str, Any]:
        if record["classification_state"] == "canonical":
            entity = self.registry.entity(record["registered_entity_id"])
            item = self._canonical_item(entity, mode=mode, note=note, evidence=evidence)
        else:
            item = {
                "title": record["proposed_canonical_title"],
                "state": state or "proposal",
                "object_family": record["object_family"],
                "note": note,
            }
            if mode == "explain":
                item.update(
                    {
                        "reference": f"arena:{record['arena_channel_id']}",
                        "type": record["type"],
                        "form": record["form"],
                        "library_function": record["library_function"],
                        "publication_status": record["publication_status"],
                        "evidence": evidence,
                    }
                )
        if curatorial_slot:
            item["curatorial_slot"] = curatorial_slot
        return item

    def _configured_evidence(
        self,
        question: dict[str, Any], result: dict[str, Any]
    ) -> list[dict[str, Any]]:
        evidence = [
            {
                "class": "curated_reader_journey",
                "source": "LIBRARY/review/reader_journey_review.yaml",
                "question_id": question["id"],
                "record_state": result["classification_state"],
            }
        ]
        if question["id"] == "UQ-02":
            series = next(
                value
                for value in self.editorial["series"]
                if value["series"] == "Field Atlas Series"
            )
            evidence.append(
                {
                    "class": "confirmed_series",
                    "source": "LIBRARY/review/editorial_sequence_review.yaml",
                    "series": series["series"],
                    "review_state": series["review_state"],
                }
            )
        if question["id"] == "UQ-06":
            evidence.append(
                {
                    "class": "curated_diversity_slot",
                    "source": "LIBRARY/review/reader_journey_review.yaml",
                }
            )
        return evidence

    @staticmethod
    def _note(question_id: str, index: int, slot: str | None) -> str:
        notes = {
            "UQ-01": [
                "Begin with how the Library can be navigated.",
                "Learn the vocabulary before entering the complete model.",
                "See how the vocabulary becomes a foundation model.",
                "Move from concepts into a visual map.",
                "Turn the language into observable practice.",
            ],
            "UQ-02": [
                "Begin with water as a landscape of transition.",
                "Continue from material transition into agency.",
                "Compare recurring morphology across systems.",
            ],
            "UQ-03": [
                "Learn the language used by the model.",
                "Practice the recurring operations.",
                "Navigate the model as a visual map.",
                "See how the research environment is documented.",
                "Enter the large working synthesis only after the earlier branches.",
            ],
            "UQ-06": [
                "A visual synthesis of orientation.",
                "A grounded Field Atlas beginning with water.",
                "A practical companion for recurring operations.",
                "An unexpected turn toward the observer’s inner landscape.",
            ],
        }
        values = notes.get(question_id, [])
        return values[index] if index < len(values) else (slot or "Curated result.")

    @staticmethod
    def _notice(items: list[dict[str, Any]]) -> str | None:
        states = {item["state"] for item in items}
        if "inferred" in states:
            return "Inferred results are description matches, not confirmed Operator references."
        if "proposal" in states:
            return "Proposal results have no canonical NEXAH identity."
        return None
