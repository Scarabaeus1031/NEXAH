from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Any

from .registry import Registry


FUNCTION_ORDER = {
    "entry": 0,
    "foundation": 1,
    "learning": 2,
    "navigation": 3,
    "practice": 4,
    "research": 5,
    "documentation": 6,
    "reference": 7,
    "synthesis": 8,
    "meta_navigation": 9,
    "archive": 10,
}


@dataclass(frozen=True)
class Recommendation:
    entity_id: str
    title: str
    score: int
    reasons: tuple[str, ...]


class OrientationQueries:
    def __init__(self, registry: Registry):
        registry.require_valid()
        self.registry = registry

    def reading_path(self, audience: str | None = None) -> list[dict[str, Any]]:
        published = {
            entity_id: entity
            for entity_id, entity in self.registry.entities.items()
            if entity.get("publication_status") == "published"
            and entity.get("edition", {}).get("revision_state") == "approved"
        }
        if audience:
            selected = {
                entity_id
                for entity_id, entity in published.items()
                if audience in entity.get("audience", []) or "general" in entity.get("audience", [])
            }
            changed = True
            while changed:
                changed = False
                for entity_id in list(selected):
                    for relation in published[entity_id].get("relations", []):
                        if relation["type"] in {"requires", "recommended_next", "derives_from"}:
                            target = relation["target"]
                            if target in published and target not in selected:
                                selected.add(target)
                                changed = True
            published = {entity_id: published[entity_id] for entity_id in selected}

        before: dict[str, set[str]] = defaultdict(set)
        for entity_id, entity in published.items():
            for relation in entity.get("relations", []):
                target = relation["target"]
                if target not in published:
                    continue
                if relation["type"] == "recommended_next":
                    before[target].add(entity_id)
                elif relation["type"] in {"requires", "derives_from"}:
                    before[entity_id].add(target)

        result: list[str] = []
        remaining = set(published)
        while remaining:
            ready = [entity_id for entity_id in remaining if not (before[entity_id] & remaining)]
            if not ready:
                ready = list(remaining)
            ready.sort(
                key=lambda entity_id: (
                    FUNCTION_ORDER.get(published[entity_id].get("library_function"), 99),
                    entity_id,
                )
            )
            chosen = ready[0]
            result.append(chosen)
            remaining.remove(chosen)
        return [self._summary(self.registry.entities[entity_id]) for entity_id in result]

    def operator_usage(self, operator_id: str) -> dict[str, Any]:
        concept = self.registry.concept(operator_id)
        works = [
            self._summary(entity)
            for entity in self.registry.entities.values()
            if operator_id in entity.get("core_operator_refs", [])
        ]
        works.sort(key=lambda item: item["id"])
        return {
            "operator": {
                "id": operator_id,
                "name": concept["preferred_name"],
                "definition": concept["definition"],
            },
            "works": works,
        }

    def graph(self, *, include_operators: bool = True) -> dict[str, Any]:
        nodes: list[dict[str, Any]] = []
        edges: list[dict[str, str]] = []
        for entity_id, entity in sorted(self.registry.entities.items()):
            nodes.append(
                {
                    "id": entity_id,
                    "kind": entity["object_family"],
                    "label": entity["canonical_title"],
                }
            )
            for relation in entity.get("relations", []):
                edges.append(
                    {"source": entity_id, "type": relation["type"], "target": relation["target"]}
                )
            if include_operators:
                for operator_id in entity.get("core_operator_refs", []):
                    edges.append({"source": entity_id, "type": "uses_operator", "target": operator_id})
        if include_operators:
            for operator_id, concept in sorted(self.registry.concepts.items()):
                nodes.append({"id": operator_id, "kind": "concept", "label": concept["preferred_name"]})
        return {"nodes": nodes, "edges": edges}

    def recommendations(self, entity_id: str, limit: int = 5) -> list[Recommendation]:
        source = self.registry.entity(entity_id)
        source_ops = set(source.get("core_operator_refs", []))
        outgoing = {(r["target"], r["type"]) for r in source.get("relations", [])}
        candidates: list[Recommendation] = []
        for candidate_id, candidate in self.registry.entities.items():
            if candidate_id == entity_id or candidate.get("publication_status") == "archived":
                continue
            score = 0
            reasons: list[str] = []
            shared_ops = sorted(source_ops & set(candidate.get("core_operator_refs", [])))
            if shared_ops:
                score += 2 * len(shared_ops)
                names = [self.registry.concepts[op]["preferred_name"] for op in shared_ops]
                reasons.append("shared operators: " + ", ".join(names))
            direct = [relation_type for target, relation_type in outgoing if target == candidate_id]
            incoming = [
                r["type"]
                for r in candidate.get("relations", [])
                if r.get("target") == entity_id
            ]
            if direct or incoming:
                score += 5
                reasons.append("curated relation: " + ", ".join(sorted(set(direct + incoming))))
            shared_audience = sorted(set(source.get("audience", [])) & set(candidate.get("audience", [])))
            if shared_audience:
                score += len(shared_audience)
                reasons.append("shared audience: " + ", ".join(shared_audience))
            if source.get("series") and source.get("series") == candidate.get("series"):
                score += 3
                reasons.append(f"same series: {source['series']}")
            if score:
                candidates.append(
                    Recommendation(candidate_id, candidate["canonical_title"], score, tuple(reasons))
                )
        candidates.sort(key=lambda item: (-item.score, item.entity_id))
        return candidates[:limit]

    @staticmethod
    def _summary(entity: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": entity["id"],
            "title": entity["canonical_title"],
            "type": entity["type"],
            "form": entity["form"],
            "library_function": entity["library_function"],
            "version": entity["edition"]["version"],
        }


def graph_to_mermaid(graph: dict[str, Any]) -> str:
    lines = ["graph TD"]
    for node in graph["nodes"]:
        node_key = node["id"].replace("-", "_")
        label = str(node["label"]).replace('"', "'")
        lines.append(f'  {node_key}["{label}"]')
    for edge in graph["edges"]:
        source = edge["source"].replace("-", "_")
        target = edge["target"].replace("-", "_")
        lines.append(f"  {source} -->|{edge['type']}| {target}")
    return "\n".join(lines)
