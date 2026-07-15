from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

from .registry import Registry, project_root


QUESTION_IDS = {f"UQ-{value:02d}" for value in range(1, 7)}
MODES = {"reader", "explain"}

ORIENTATIONS = {
    "UQ-01": "A good place to begin:",
    "UQ-02": "Follow water from a concrete field study into wider patterns:",
    "UQ-03": "There is no single required sequel; choose the branch that helps you next:",
    "UQ-04": "Transition appears in two different evidence groups:",
    "UQ-05": "Begin with one thematic Series, then use two companion maps:",
    "UQ-06": "A small, deliberate cross-section of the Library:",
}

ROLES = {
    "UQ-01": ["Starting point", "Vocabulary", "Foundation", "Visual map", "Practice"],
    "UQ-02": ["Water", "Agency", "Morphology"],
    "UQ-03": [
        "Learn the language",
        "Practice the operators",
        "Navigate the map",
        "See the laboratory",
        "Enter the synthesis",
    ],
    "UQ-06": ["Visual Work", "Field Atlas", "Handbook", "Unexpected connection"],
}

ADDITIONS = {
    "entry": "A human-scale entrance to the Library and its way of reading.",
    "learning": "The vocabulary and visual grammar used by later Works.",
    "foundation": "A foundation model that connects the Library’s recurring concepts.",
    "navigation": "A visual map for moving between concepts and scales.",
    "practice": "A practical way to recognize and apply recurring operations.",
    "research": "A research perspective grounded in a specific field or transition.",
    "reference": "A stable reference map that can be revisited while building.",
    "documentation": "A view into the Library’s documented research environment.",
    "synthesis": "A wider synthesis that connects several Library branches.",
    "meta_navigation": "A map of how different atlases and navigation layers relate.",
}

WHY_THIS = {
    "Starting point": "It explains how to enter and explore the Library.",
    "Vocabulary": "It introduces the vocabulary used by later Works.",
    "Foundation": "It gathers that vocabulary into a larger foundation model.",
    "Visual map": "It turns the language into a navigable visual structure.",
    "Practice": "It helps the reader apply the recurring operations.",
    "Water": "It is the Library’s direct field study of water.",
    "Agency": "It continues the confirmed Field Atlas sequence beyond water.",
    "Morphology": "It follows the Field Atlas sequence into recurring forms across systems.",
    "Learn the language": "It provides a learning branch after the dense foundation model.",
    "Practice the operators": "It provides a practical branch after the foundation model.",
    "Navigate the map": "It provides a visual navigation branch after the foundation model.",
    "See the laboratory": "It shows the documented environment in which the system is developed.",
    "Enter the synthesis": "It offers the large synthesis without making it the first sequel.",
    "Confirmed Operator reference": "Transition is explicitly assigned to this Work in the Registry.",
    "Description match": "The public description contains the word Transition.",
    "Primary thematic Series": "It is the confirmed editorial sequence centered on orientation.",
    "Companion Work": "It offers a complementary map for the navigation theme.",
    "Visual Work": "It opens discovery through a visual synthesis.",
    "Field Atlas": "It grounds discovery in a specific field study.",
    "Handbook": "It adds a practical Work to the selection.",
    "Unexpected connection": "It changes scale from external maps to the inner observer.",
}


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
            if record["classification_state"] == "proposed" and record.get(
                "registered_entity_id"
            ):
                raise ReaderOverlayError(
                    "Proposal record may not resolve to a canonical NEXAH ID"
                )

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
        if question_id == "UQ-01" and len(items) != 5:
            raise ReaderOverlayError("UQ-01 must return exactly five Works")
        positioned = [{"position": index, **item} for index, item in enumerate(items, 1)]
        return {
            "question_id": question_id,
            "prompt": question["prompt"],
            "mode": mode,
            "orientation": ORIENTATIONS[question_id],
            "items": positioned,
            "groups": self._groups(question_id, positioned),
            "notice": self._notice(positioned),
        }

    def _configured_items(
        self, question: dict[str, Any], mode: str
    ) -> list[dict[str, Any]]:
        roles = ROLES.get(question["id"], [])
        return [
            self._entity_item(
                self.records[result["arena_channel_id"]],
                mode=mode,
                guidance=self._guidance(question["id"], index),
                role=roles[index] if index < len(roles) else "Recommendation",
                evidence=self._configured_evidence(question, result),
            )
            for index, result in enumerate(question.get("expected_results", []))
        ]

    def _transition_items(self, mode: str) -> list[dict[str, Any]]:
        operator_id = "NX-OP-0005"
        canonical = [
            self._canonical_item(
                entity,
                mode=mode,
                role="Confirmed Operator reference",
                guidance="Transition is explicitly curated for this Work.",
                evidence=[
                    {
                        "class": "canonical_operator_reference",
                        "source": f"LIBRARY/registry/entities/{entity['id']}.yaml",
                        "operator_id": operator_id,
                    }
                ],
                group="Canonical Operator references",
            )
            for entity in sorted(
                self.registry.entities.values(), key=lambda value: value["id"]
            )
            if operator_id in entity.get("core_operator_refs", [])
        ]
        inferred: list[dict[str, Any]] = []
        for channel_id, record in sorted(self.records.items()):
            if (
                record["classification_state"] != "proposed"
                or record["object_family"] != "work"
            ):
                continue
            description = self.discovery_records.get(channel_id, {}).get(
                "current_description", ""
            )
            if not re.search(r"\btransition(?:s|al)?\b", description, re.I):
                continue
            inferred.append(
                self._entity_item(
                    record,
                    mode=mode,
                    role="Description match",
                    guidance=(
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
                    group="Inferred description matches",
                )
            )
        return canonical + inferred

    def _navigation_items(
        self, question: dict[str, Any], mode: str
    ) -> list[dict[str, Any]]:
        series_name = question["expected_series"][0]
        series = next(
            value for value in self.editorial["series"] if value["series"] == series_name
        )
        if series["review_state"] != "confirmed":
            raise ReaderOverlayError(f"Series {series_name} is not human-confirmed")
        evidence = [
            {
                "class": "confirmed_series",
                "source": "LIBRARY/review/editorial_sequence_review.yaml",
                "review_state": series["review_state"],
            }
        ]
        series_item = self._format_item(
            title=series_name,
            state="proposal",
            role="Primary thematic Series",
            guidance="Begin with its confirmed four-volume orientation sequence.",
            mode=mode,
            function="navigation",
            evidence=evidence,
            reference=f"series:{series_name}",
            technical={
                "type": "series",
                "form": "editorial_sequence",
                "function": "navigation",
                "publication_status": "proposed",
            },
            sequence=[member["title"] for member in series["ordered_members"]],
            group="Primary thematic Series",
        )
        companions = [
            self._entity_item(
                self.records[result["arena_channel_id"]],
                mode=mode,
                role="Companion Work",
                guidance="Use this as a complementary navigation map.",
                evidence=[
                    {
                        "class": "curated_reader_companion",
                        "source": "LIBRARY/review/reader_journey_review.yaml",
                    }
                ],
                group="Companion Works",
            )
            for result in question.get("expected_companions", [])
        ]
        return [series_item, *companions]

    def _canonical_item(
        self,
        entity: dict[str, Any],
        *,
        mode: str,
        role: str,
        guidance: str,
        evidence: list[dict[str, Any]],
        group: str | None = None,
    ) -> dict[str, Any]:
        return self._format_item(
            title=entity["canonical_title"],
            state="canonical",
            role=role,
            guidance=guidance,
            mode=mode,
            function=entity["library_function"],
            evidence=evidence,
            reference=entity["id"],
            technical={
                "type": entity["type"],
                "form": entity["form"],
                "function": entity["library_function"],
                "publication_status": entity["publication_status"],
            },
            group=group,
        )

    def _entity_item(
        self,
        record: dict[str, Any],
        *,
        mode: str,
        role: str,
        guidance: str,
        evidence: list[dict[str, Any]],
        state: str | None = None,
        group: str | None = None,
    ) -> dict[str, Any]:
        if record["classification_state"] == "canonical":
            entity = self.registry.entity(record["registered_entity_id"])
            return self._canonical_item(
                entity,
                mode=mode,
                role=role,
                guidance=guidance,
                evidence=evidence,
                group=group,
            )
        return self._format_item(
            title=record["proposed_canonical_title"],
            state=state or "proposal",
            role=role,
            guidance=guidance,
            mode=mode,
            function=record["library_function"],
            evidence=evidence,
            reference=f"arena:{record['arena_channel_id']}",
            technical={
                "type": record["type"],
                "form": record["form"],
                "function": record["library_function"],
                "publication_status": record["publication_status"],
            },
            group=group,
        )

    @staticmethod
    def _format_item(
        *,
        title: str,
        state: str,
        role: str,
        guidance: str,
        mode: str,
        function: str,
        evidence: list[dict[str, Any]],
        reference: str,
        technical: dict[str, Any],
        group: str | None = None,
        sequence: list[str] | None = None,
    ) -> dict[str, Any]:
        item: dict[str, Any] = {
            "title": title,
            "state": state,
            "role": role,
            "guidance": guidance,
        }
        if group:
            item["section"] = group
        if mode == "explain":
            source_labels = {
                "curated_reader_journey": "human-confirmed Reader Journey",
                "canonical_operator_reference": "Canonical Operator Registry",
                "inferred_description_match": "public description match",
                "confirmed_series": "human-confirmed editorial sequence",
                "curated_reader_companion": "human-curated thematic companion",
            }
            primary_class = evidence[0]["class"]
            item.update(
                {
                    "explanation": {
                        "why_this_work": WHY_THIS.get(
                            role, "It has a distinct editorial purpose in this answer."
                        ),
                        "what_it_adds": ADDITIONS.get(
                            function, "A distinct perspective within the curated path."
                        ),
                        "why_here": guidance,
                        "state_note": ReaderOverlay._state_note(state),
                        "recommendation_source": source_labels.get(
                            primary_class, primary_class.replace("_", " ")
                        ),
                    },
                    "technical": {"reference": reference, **technical},
                    "evidence": evidence,
                }
            )
            if sequence is not None:
                item["editorial_sequence"] = sequence
        return item

    def _configured_evidence(
        self, question: dict[str, Any], result: dict[str, Any]
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
    def _guidance(question_id: str, index: int) -> str:
        guidance = {
            "UQ-01": [
                "Learn how the Library is meant to be explored.",
                "Acquire the basic vocabulary before entering the larger model.",
                "See how that vocabulary becomes a foundation model.",
                "Move from concepts into a visual map.",
                "Turn the language into observable practice.",
            ],
            "UQ-02": [
                "Begin with water as a landscape of transition.",
                "Continue from material transition into agency.",
                "Compare recurring morphology across systems.",
            ],
            "UQ-03": [
                "Return to the language if the foundation model feels dense.",
                "Practice the recurring operations.",
                "Navigate the model as a visual map.",
                "See how the research environment is documented.",
                "Enter the large working synthesis after the earlier branches.",
            ],
            "UQ-06": [
                "Begin with a visual synthesis of orientation.",
                "Ground the selection in a Field Atlas about water.",
                "Keep a practical companion for recurring operations.",
                "Turn unexpectedly toward the observer’s inner landscape.",
            ],
        }
        values = guidance.get(question_id, [])
        return values[index] if index < len(values) else "Follow this curated result."

    @staticmethod
    def _state_note(state: str) -> str:
        return {
            "canonical": "This Work has a stable identity in the Canonical Registry.",
            "proposal": "This is a reviewed Proposal and has no canonical NEXAH identity.",
            "inferred": (
                "This is a description match, not a confirmed Operator annotation."
            ),
        }[state]

    @staticmethod
    def _groups(question_id: str, items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        if question_id == "UQ-04":
            definitions = [
                "Canonical Operator references",
                "Inferred description matches",
            ]
        elif question_id == "UQ-05":
            definitions = [
                "Primary thematic Series",
                "Companion Works",
            ]
        else:
            return []
        return [
            {
                "label": label,
                "positions": [
                    item["position"] for item in items if item.get("section") == label
                ],
            }
            for label in definitions
        ]

    @staticmethod
    def _notice(items: list[dict[str, Any]]) -> str | None:
        states = {item["state"] for item in items}
        if "inferred" in states:
            return "Inferred results are description matches, not confirmed Operator references."
        if "proposal" in states:
            return "Proposal results have no canonical NEXAH identity."
        return None
