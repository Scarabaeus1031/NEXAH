from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


ENTITY_ID = re.compile(r"^NX-\d{6}$")
OPERATOR_ID = re.compile(r"^NX-OP-\d{4}$")

OBJECT_FAMILIES = {"work", "environment", "navigation", "asset", "concept"}
WORK_TYPES = {"book", "atlas", "guide", "research_report", "visual_essay", "notebook"}
PUBLICATION_STATUSES = {"working", "published", "archived"}
REVISION_STATES = {"draft", "review", "approved", "superseded"}
MATURITY_STATES = {"exploratory", "developing", "stable"}
STRUCTURE_MODES = {"linear", "guided_non_linear", "unordered"}
RELATION_TYPES = {
    "contains",
    "member_of_series",
    "continues",
    "derives_from",
    "applies",
    "maps",
    "documents",
    "implements",
    "references",
    "synthesizes",
    "has_asset",
    "requires",
    "recommended_next",
    "supersedes",
    "related_to",
}


class RegistryError(RuntimeError):
    pass


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _load_yaml(path: Path) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise RegistryError(f"Cannot read {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise RegistryError(f"Expected a mapping in {path}")
    return value


@dataclass(frozen=True)
class Registry:
    root: Path
    manifest: dict[str, Any]
    entities: dict[str, dict[str, Any]]
    concepts: dict[str, dict[str, Any]]

    @classmethod
    def load(cls, root: Path | str | None = None) -> "Registry":
        if root:
            registry_root = Path(root)
        else:
            library_registry = project_root() / "LIBRARY" / "registry"
            registry_root = library_registry if library_registry.exists() else project_root() / "registry"
        manifest = _load_yaml(registry_root / "registry.yaml")
        entities = cls._load_records(registry_root / "entities", ENTITY_ID)
        concepts = cls._load_records(registry_root / "concepts", OPERATOR_ID)
        return cls(registry_root, manifest, entities, concepts)

    @staticmethod
    def _load_records(directory: Path, pattern: re.Pattern[str]) -> dict[str, dict[str, Any]]:
        records: dict[str, dict[str, Any]] = {}
        for path in sorted(directory.glob("*.yaml")):
            record = _load_yaml(path)
            record_id = record.get("id")
            if not isinstance(record_id, str) or not pattern.fullmatch(record_id):
                raise RegistryError(f"Invalid or missing id in {path}")
            if path.stem != record_id:
                raise RegistryError(f"Filename {path.name} does not match id {record_id}")
            if record_id in records:
                raise RegistryError(f"Duplicate id {record_id}")
            records[record_id] = record
        return records

    def validate(self) -> list[str]:
        errors: list[str] = []
        if self.manifest.get("entity_count") != len(self.entities):
            errors.append("manifest entity_count does not match entity files")
        if self.manifest.get("concept_count") != len(self.concepts):
            errors.append("manifest concept_count does not match concept files")
        if self.manifest.get("write_policy", {}).get("arena") != "read_only":
            errors.append("registry must declare Are.na as read_only")

        for entity_id, entity in self.entities.items():
            prefix = entity_id
            required = {
                "canonical_title",
                "object_family",
                "type",
                "form",
                "library_function",
                "publication_status",
                "current_edition",
                "summary",
                "audience",
                "language",
                "canonical_url",
                "external_ids",
                "edition",
                "last_verified",
            }
            missing = sorted(required - entity.keys())
            if missing:
                errors.append(f"{prefix}: missing {', '.join(missing)}")
            if entity.get("object_family") not in OBJECT_FAMILIES:
                errors.append(f"{prefix}: invalid object_family")
            if entity.get("object_family") == "work" and entity.get("type") not in WORK_TYPES:
                errors.append(f"{prefix}: invalid work type {entity.get('type')}")
            if entity.get("publication_status") not in PUBLICATION_STATUSES:
                errors.append(f"{prefix}: invalid publication_status")
            edition = entity.get("edition", {})
            expected_edition = f"{entity_id}-E01"
            if entity.get("current_edition") != edition.get("edition_id"):
                errors.append(f"{prefix}: current_edition does not resolve to embedded edition")
            if edition.get("edition_id") != expected_edition:
                errors.append(f"{prefix}: pilot edition must be {expected_edition}")
            if edition.get("revision_state") not in REVISION_STATES:
                errors.append(f"{prefix}: invalid revision_state")
            if edition.get("content_maturity") not in MATURITY_STATES:
                errors.append(f"{prefix}: invalid content_maturity")
            if edition.get("structure_mode") not in STRUCTURE_MODES:
                errors.append(f"{prefix}: invalid structure_mode")
            if not isinstance(edition.get("member_count"), int) or edition.get("member_count", -1) < 0:
                errors.append(f"{prefix}: invalid member_count")
            external = entity.get("external_ids", {})
            if not isinstance(external.get("arena_channel_id"), int) or not external.get("arena_slug"):
                errors.append(f"{prefix}: incomplete Are.na external_ids")
            for operator_id in entity.get("core_operator_refs", []):
                if operator_id not in self.concepts:
                    errors.append(f"{prefix}: unknown operator {operator_id}")
            for relation in entity.get("relations", []):
                if relation.get("type") not in RELATION_TYPES:
                    errors.append(f"{prefix}: invalid relation {relation.get('type')}")
                if relation.get("target") not in self.entities:
                    errors.append(f"{prefix}: unknown relation target {relation.get('target')}")

        for concept_id, concept in self.concepts.items():
            prefix = concept_id
            if concept.get("object_family") != "concept" or concept.get("type") != "operator":
                errors.append(f"{prefix}: initial concept registry only accepts operators")
            if concept.get("vocabulary_status") not in {"candidate", "provisional", "core", "deprecated"}:
                errors.append(f"{prefix}: invalid vocabulary_status")
            if not concept.get("preferred_name") or not concept.get("definition"):
                errors.append(f"{prefix}: preferred_name and definition are required")
            for source_id in concept.get("source_works", []):
                if source_id not in self.entities:
                    errors.append(f"{prefix}: unknown source work {source_id}")
            for related_id in concept.get("related_concepts", []):
                if related_id not in self.concepts:
                    errors.append(f"{prefix}: unknown related concept {related_id}")
        return errors

    def require_valid(self) -> None:
        errors = self.validate()
        if errors:
            raise RegistryError("Registry validation failed:\n- " + "\n- ".join(errors))

    def entity(self, entity_id: str) -> dict[str, Any]:
        try:
            return self.entities[entity_id]
        except KeyError as exc:
            raise RegistryError(f"Unknown entity {entity_id}") from exc

    def concept(self, concept_id: str) -> dict[str, Any]:
        try:
            return self.concepts[concept_id]
        except KeyError as exc:
            raise RegistryError(f"Unknown concept {concept_id}") from exc
