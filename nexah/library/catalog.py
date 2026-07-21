from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from .arena import ArenaClient
from .operations import OperationError, load_yaml


SCHEMA_VERSION = "0.1"


def _plain(value: Any) -> str | None:
    if isinstance(value, str):
        return value.strip() or None
    if isinstance(value, dict):
        plain = value.get("plain")
        if isinstance(plain, str):
            return plain.strip() or None
    return None


def _page_role(title: str | None, sequence_index: int) -> str:
    normalized = " ".join((title or "").upper().split())
    if sequence_index == 1:
        return "cover"
    if "FOREWORD" in normalized or "PREFACE" in normalized:
        return "foreword"
    if normalized == "INDEX" or "TABLE OF CONTENTS" in normalized:
        return "index"
    if re.match(r"^(PART|BOOK)\s+[IVXLC0-9]+\b", normalized):
        return "part"
    if re.match(r"^(CHAPTER|CH\.)\s*[0-9IVXLC]+\b", normalized):
        return "chapter"
    if re.match(r"^[0-9]{1,3}[\s._|)-]+\S", normalized):
        return "numbered_section"
    if re.match(r"^APPENDIX\b", normalized):
        return "appendix"
    if normalized in {"END", "THE END", "EPILOGUE", "AFTERWORD", "COLOPHON"}:
        return "closing"
    return "page"


def _editorial_roles(title: str | None) -> list[str]:
    normalized = " ".join((title or "").upper().replace("_", " ").split())
    patterns = {
        "opening": r"\b(OPENING|PROLOGUE)\b",
        "story": r"\bSTORY\b",
        "plate": r"\bPLATE\b",
        "reflection": r"\bREFLECT(?:ION|IOTION)?\b",
        "transition": r"\bTRANSIT(?:ION|ON)?\b",
        "recap": r"\bRECAP\b",
        "journey": r"\bJOURNEY\b",
        "question": r"\bQUESTION(?:S)?\b",
    }
    return [name for name, pattern in patterns.items() if re.search(pattern, normalized)]


def _image_record(item: dict[str, Any]) -> dict[str, Any] | None:
    image = item.get("image")
    if not isinstance(image, dict):
        return None
    variants = {}
    for name in ("small", "medium", "large", "square"):
        value = image.get(name)
        if isinstance(value, dict) and value.get("src"):
            variants[name] = value.get("src")
    return {
        "original_url": image.get("src"),
        "variants": variants,
        "width": image.get("width"),
        "height": image.get("height"),
        "aspect_ratio": image.get("aspect_ratio"),
        "content_type": image.get("content_type"),
        "filename": image.get("filename"),
        "file_size": image.get("file_size"),
        "alt_text": image.get("alt_text"),
    }


def _block_record(item: dict[str, Any], sequence_index: int) -> dict[str, Any]:
    connection = item.get("connection") if isinstance(item.get("connection"), dict) else {}
    record = {
        "sequence_index": sequence_index,
        "arena_block_id": item.get("id"),
        "block_type": item.get("type"),
        "title": item.get("title"),
        "description": _plain(item.get("description")),
        "page_role": _page_role(item.get("title"), sequence_index),
        "editorial_roles": _editorial_roles(item.get("title")),
        "connection_position": connection.get("position"),
        "created_at": item.get("created_at"),
        "updated_at": item.get("updated_at"),
    }
    image = _image_record(item)
    if image:
        record["image"] = image
    return record


def _catalog_depth(classification: dict[str, Any], override: dict[str, Any]) -> str:
    if override.get("catalog_depth"):
        return override["catalog_depth"]
    if classification.get("series") == "The Human Journey":
        return "bibliographic_and_dramaturgic"
    if classification.get("type") == "research_report" or classification.get(
        "library_function"
    ) in {"research", "documentation"}:
        return "research_structure"
    if classification.get("type") == "atlas":
        return "atlas_structure"
    if classification.get("library_function") in {"foundation", "reference", "synthesis"}:
        return "knowledge_work_structure"
    if classification.get("library_function") in {"learning", "practice"}:
        return "knowledge_work_structure"
    return "bibliographic"


def _structure(blocks: list[dict[str, Any]]) -> dict[str, Any]:
    roles = {
        role: []
        for role in (
            "foreword",
            "index",
            "part",
            "chapter",
            "numbered_section",
            "appendix",
            "closing",
        )
    }
    editorial_roles: dict[str, list[dict[str, Any]]] = {}
    titled = 0
    for block in blocks:
        if block.get("title"):
            titled += 1
        role = block["page_role"]
        if role in roles:
            roles[role].append(
                {
                    "sequence_index": block["sequence_index"],
                    "arena_block_id": block["arena_block_id"],
                    "title": block.get("title"),
                }
            )
        for editorial_role in block["editorial_roles"]:
            editorial_roles.setdefault(editorial_role, []).append(
                {
                    "sequence_index": block["sequence_index"],
                    "arena_block_id": block["arena_block_id"],
                    "title": block.get("title"),
                }
            )
    return {
        "block_count": len(blocks),
        "titled_block_count": titled,
        "title_coverage": round(titled / len(blocks), 3) if blocks else 0.0,
        **roles,
        "editorial_roles": editorial_roles,
        "visual_text_status": "not_extracted",
        "note": (
            "Roles are inferred only from public block titles. Text rendered inside image pages "
            "requires a separate visual review."
        ),
    }


def build_work_catalog_record(
    client: ArenaClient,
    classification: dict[str, Any],
    *,
    override: dict[str, Any] | None = None,
) -> dict[str, Any]:
    override = override or {}
    arena_id = classification["arena_channel_id"]
    channel = client.get_channel(arena_id)
    contents = client.get_contents(arena_id, per=100)
    blocks = [_block_record(item, index) for index, item in enumerate(contents, start=1)]
    cover = next((block for block in blocks if block.get("image")), None)
    live_title = channel.get("title") or classification.get("current_title")
    display_title = override.get("display_title") or classification.get(
        "proposed_canonical_title"
    ) or live_title

    editorial = {
        key: classification.get(key)
        for key in (
            "classification_state",
            "object_family",
            "type",
            "form",
            "library_function",
            "publication_status",
            "revision_state",
            "content_maturity",
            "series",
            "confidence",
            "human_decision",
        )
    }
    for key in ("series", "shelves", "catalog_note"):
        if key in override:
            editorial[key] = override[key]

    return {
        "schema_version": SCHEMA_VERSION,
        "catalog_key": f"arena:{arena_id}",
        "authority": "noncanonical_website_catalog",
        "registered_entity_id": classification.get("registered_entity_id"),
        "display_title": display_title,
        "source": {
            "arena_channel_id": arena_id,
            "arena_slug": channel.get("slug"),
            "canonical_url": f"https://www.are.na/nexah-scarabaeus1031/{channel.get('slug')}",
            "live_title": live_title,
            "description": _plain(channel.get("description")),
            "visibility": channel.get("visibility"),
            "state": channel.get("state"),
            "member_count": channel.get("counts", {}).get("contents"),
            "created_at": channel.get("created_at"),
            "updated_at": channel.get("updated_at"),
        },
        "editorial": editorial,
        "catalog_depth": _catalog_depth(classification, override),
        "cover": (
            {
                "arena_block_id": cover["arena_block_id"],
                "title": cover.get("title"),
                **cover["image"],
            }
            if cover
            else None
        ),
        "structure": _structure(blocks),
        "blocks": blocks,
        "evidence_policy": {
            "api_description": "source_evidence",
            "block_titles": "source_evidence",
            "page_roles": "machine_assisted_structural_inference",
            "image_text": "not_reviewed",
            "semantic_summary": "not_generated",
        },
    }


def build_website_catalog(
    client: ArenaClient,
    classification: dict[str, Any],
    *,
    overrides: dict[str, Any] | None = None,
) -> dict[str, Any]:
    overrides_by_id = {
        int(item["arena_channel_id"]): item
        for item in (overrides or {}).get("records", [])
    }
    works = [
        item for item in classification.get("records", []) if item.get("object_family") == "work"
    ]
    records = [
        build_work_catalog_record(
            client,
            item,
            override=overrides_by_id.get(int(item["arena_channel_id"])),
        )
        for item in works
    ]
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "status": "noncanonical_read_only_overlay",
        "purpose": "Website catalog and future human editorial review",
        "source_classification": "LIBRARY/review/full_library_classification.yaml",
        "summary": {
            "works": len(records),
            "canonical_records": sum(bool(item["registered_entity_id"]) for item in records),
            "proposal_records": sum(not item["registered_entity_id"] for item in records),
            "with_description": sum(bool(item["source"]["description"]) for item in records),
            "with_cover": sum(bool(item["cover"]) for item in records),
            "with_foreword": sum(bool(item["structure"]["foreword"]) for item in records),
            "with_index": sum(bool(item["structure"]["index"]) for item in records),
        },
        "records": records,
    }


def write_website_catalog(catalog: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    works_dir = output_dir / "works"
    works_dir.mkdir(parents=True, exist_ok=True)
    index = {key: value for key, value in catalog.items() if key != "records"}
    index["records"] = []
    for record in catalog["records"]:
        filename = f"arena-{record['source']['arena_channel_id']}.yaml"
        index["records"].append(
            {
                "catalog_key": record["catalog_key"],
                "display_title": record["display_title"],
                "registered_entity_id": record["registered_entity_id"],
                "type": record["editorial"]["type"],
                "form": record["editorial"]["form"],
                "series": record["editorial"].get("series"),
                "catalog_depth": record["catalog_depth"],
                "record": f"works/{filename}",
            }
        )
        (works_dir / filename).write_text(
            yaml.safe_dump(record, allow_unicode=True, sort_keys=False, width=120),
            encoding="utf-8",
        )
    (output_dir / "website_catalog.yaml").write_text(
        yaml.safe_dump(index, allow_unicode=True, sort_keys=False, width=120),
        encoding="utf-8",
    )
    (output_dir / "CATALOG_STATUS.md").write_text(
        render_catalog_status(catalog), encoding="utf-8"
    )


def render_catalog_status(catalog: dict[str, Any]) -> str:
    records = catalog["records"]
    total_blocks = sum(item["structure"]["block_count"] for item in records)
    lines = [
        "# NEXAH Website Catalog — Current Status",
        "",
        f"Generated: `{catalog['generated_at']}`",
        "",
        "This is a read-only, non-canonical website catalog. It records public source evidence",
        "and conservative structural observations; it does not change Registry or Proposal state.",
        "",
        "## Coverage",
        "",
        f"- Works: **{catalog['summary']['works']}**",
        f"- Ordered public Blocks: **{total_blocks}**",
        f"- Channel descriptions: **{catalog['summary']['with_description']}**",
        f"- Cover references: **{catalog['summary']['with_cover']}**",
        f"- Works with a detected Foreword: **{catalog['summary']['with_foreword']}**",
        f"- Works with a detected Index: **{catalog['summary']['with_index']}**",
        "",
        "## Review depth",
        "",
        "Research books, reports, atlases, and whiteboards receive structural catalog records.",
        "Journey Works remain bibliographic and dramaturgic until separately reviewed.",
        "",
    ]
    labels = {
        "research_structure": "Research structures",
        "atlas_structure": "Atlas structures",
        "knowledge_work_structure": "Knowledge works",
        "bibliographic_and_dramaturgic": "Journey / dramaturgic records",
        "bibliographic": "Bibliographic records",
    }
    for depth in labels:
        selected = [item for item in records if item["catalog_depth"] == depth]
        lines.extend([f"### {labels[depth]} ({len(selected)})", ""])
        for item in sorted(selected, key=lambda value: value["display_title"].casefold()):
            source = item["source"]
            lines.append(
                f"- [{item['display_title']}]({source['canonical_url']}) — "
                f"{item['editorial']['type']}; {item['structure']['block_count']} Blocks"
            )
        lines.append("")
    lines.extend(
        [
            "## What remains",
            "",
            "The API does not expose text rendered inside image pages. A later bounded visual review",
            "can therefore add evidence-backed summaries, subjects, and page-level knowledge only for",
            "selected Works. Those additions must cite their source Blocks and remain separate from",
            "Registry identity and canonical Operator semantics.",
            "",
        ]
    )
    return "\n".join(lines)


def load_catalog_sources(
    classification_path: Path, overrides_path: Path | None
) -> tuple[dict[str, Any], dict[str, Any]]:
    classification = load_yaml(classification_path)
    overrides: dict[str, Any] = {}
    if overrides_path and overrides_path.exists():
        overrides = load_yaml(overrides_path)
    elif overrides_path:
        raise OperationError(f"Cannot read catalog overrides {overrides_path}")
    return classification, overrides
