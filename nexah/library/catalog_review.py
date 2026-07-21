from __future__ import annotations

import hashlib
import json
import re
from typing import Any, Iterable


SCHEMA_VERSION = "0.1"

CATALOG_DOMAINS = {
    "publication",
    "concept",
    "operator",
    "laboratory",
    "atlas",
    "navigation",
}

VISUAL_ROLES = {
    "cover",
    "title_page",
    "foreword",
    "index",
    "part_opener",
    "chapter_opener",
    "body_text",
    "definition",
    "research_question",
    "method",
    "model",
    "diagram",
    "map",
    "table",
    "evidence",
    "observation",
    "hypothesis",
    "case_study",
    "implementation",
    "conclusion",
    "open_question",
    "appendix",
    "reference",
    "transition",
    "reflection",
    "promotional",
    "closing",
    "decorative",
    "duplicate",
    "unreadable",
    "uncertain",
}

REVIEW_STATES = {"extracted", "queued", "reviewed", "accepted", "revised", "rejected"}
EXTRACTION_STATUSES = {
    "not_reviewed",
    "machine_observed",
    "visually_reviewed",
    "human_confirmed",
    "accepted",
    "rejected",
}

RESEARCH_ELEMENT_FIELDS = (
    "definitions",
    "questions",
    "observations",
    "hypotheses",
    "methods",
    "models",
    "evidence_statements",
    "limitations",
    "open_questions",
    "concepts",
    "operator_candidates",
    "atlas_objects",
)


class CatalogReviewError(ValueError):
    """Raised when a non-canonical review record violates its evidence contract."""


def source_fingerprint(publication_key: str, block: dict[str, Any]) -> str:
    """Return a deterministic fingerprint of source metadata, never image meaning."""

    image = block.get("image") if isinstance(block.get("image"), dict) else {}
    payload = {
        "publication_key": publication_key,
        "arena_block_id": block.get("arena_block_id"),
        "sequence_index": block.get("sequence_index"),
        "title": block.get("title"),
        "updated_at": block.get("updated_at"),
        "image_url": image.get("original_url"),
    }
    encoded = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def source_block_url(block_id: int) -> str:
    return f"https://www.are.na/block/{block_id}"


def infer_visual_role(block: dict[str, Any]) -> str:
    """Conservative role suggestion used after a human contact-sheet pass."""

    title = " ".join(str(block.get("title") or "").upper().split())
    page_role = block.get("page_role")
    if page_role == "cover":
        return "cover"
    if page_role == "foreword":
        return "foreword"
    if page_role == "index":
        return "index"
    if page_role == "part":
        return "part_opener"
    if page_role == "appendix":
        return "appendix"
    if page_role == "closing":
        return "closing"
    if "GLOSSARY" in title or "REFERENCE" in title:
        return "reference"
    if "QUESTION" in title or "DON'T KNOW" in title or "REMAINS OPEN" in title:
        return "open_question"
    if "METHOD" in title or "BENCHMARK" in title:
        return "method"
    if "EVIDENCE" in title or "WHAT WE KNOW" in title:
        return "evidence"
    if "DEFINITION" in title or title.startswith("05 WHAT IS ORIENTATION"):
        return "definition"
    if "MODEL" in title or "FRAMEWORK" in title or "ARCHITECTURE" in title:
        return "model"
    if "MAP" in title or "ATLAS" in title or "LANDSCAPE" in title:
        return "map"
    if "HYPOTH" in title:
        return "hypothesis"
    if "APPLICATION" in title or "IMPLEMENT" in title or "INFRASTRUCTURE" in title:
        return "implementation"
    if "ROADMAP" in title or "FUTURE" in title or "COLLABORATION" in title:
        return "conclusion"
    if "TRANSITION" in title or "BRIDGE" in title:
        return "transition"
    if page_role == "numbered_section":
        return "body_text"
    return "body_text"


def triage_publication(
    publication: dict[str, Any],
    *,
    role_overrides: dict[int, str] | None = None,
) -> dict[str, Any]:
    """Build a deterministic, source-keyed visual triage record.

    The caller is responsible for actually reviewing the images. This function only
    records the resulting role choices and source evidence.
    """

    role_overrides = role_overrides or {}
    key = publication["catalog_key"]
    pages = []
    for block in publication.get("blocks", []):
        block_id = int(block["arena_block_id"])
        role = role_overrides.get(block_id, infer_visual_role(block))
        if role not in VISUAL_ROLES:
            raise CatalogReviewError(f"Unknown visual role: {role}")
        eligible = role in {
            "body_text",
            "definition",
            "research_question",
            "method",
            "model",
            "diagram",
            "map",
            "table",
            "evidence",
            "observation",
            "hypothesis",
            "case_study",
            "implementation",
            "conclusion",
            "open_question",
        }
        pages.append(
            {
                "page_key": f"arena-block:{block_id}",
                "arena_block_id": block_id,
                "sequence_index": block["sequence_index"],
                "title": block.get("title"),
                "visual_role": role,
                "visual_review_result": "eligible_for_deeper_extraction" if eligible else "no_research_content",
                "source_url": source_block_url(block_id),
                "image_url": (block.get("image") or {}).get("original_url"),
                "source_fingerprint": source_fingerprint(key, block),
                "review_method": "human_visual_contact_sheet_review",
                "extraction_status": "visually_reviewed",
                "requires_human_review": eligible,
            }
        )
    return {
        "schema_version": SCHEMA_VERSION,
        "authority": "noncanonical_catalog_review",
        "publication": {
            "catalog_key": key,
            "arena_channel_id": publication["source"]["arena_channel_id"],
            "title": publication["display_title"],
            "source_url": publication["source"]["canonical_url"],
        },
        "page_count": len(pages),
        "pages": pages,
    }


def duplicate_block_ids(records: Iterable[dict[str, Any]]) -> list[int]:
    seen: set[int] = set()
    duplicates: set[int] = set()
    for record in records:
        block_id = int(record["source_block"]["arena_block_id"])
        if block_id in seen:
            duplicates.add(block_id)
        seen.add(block_id)
    return sorted(duplicates)


def record_is_stale(record: dict[str, Any], publication: dict[str, Any]) -> bool:
    block_id = record["source_block"]["arena_block_id"]
    block = next(
        (item for item in publication.get("blocks", []) if item.get("arena_block_id") == block_id),
        None,
    )
    if block is None:
        return True
    return record["source_block"].get("source_fingerprint") != source_fingerprint(
        publication["catalog_key"], block
    )


def validate_visual_research_record(record: dict[str, Any]) -> None:
    """Validate the evidence and review boundaries of a page-level record."""

    if record.get("authority") != "noncanonical_catalog_review":
        raise CatalogReviewError("Visual research records must remain non-canonical")
    source = record.get("source_block") or {}
    block_id = source.get("arena_block_id")
    if not isinstance(block_id, int) or record.get("page_key") != f"arena-block:{block_id}":
        raise CatalogReviewError("page_key must be the stable Are.na Block identity")
    if not source.get("source_fingerprint") or not source.get("url") or not source.get("image_url"):
        raise CatalogReviewError("Exact source provenance and fingerprint are required")
    if record.get("visual_role") not in VISUAL_ROLES:
        raise CatalogReviewError("Invalid visual_role")
    review = record.get("review") or {}
    if review.get("extraction_status") not in EXTRACTION_STATUSES:
        raise CatalogReviewError("Invalid extraction_status")
    if review.get("review_state") not in REVIEW_STATES:
        raise CatalogReviewError("Invalid review_state")
    if review.get("confidence") not in {"low", "medium", "high"}:
        raise CatalogReviewError("Invalid confidence")
    if "claim_boundary" not in record or not record.get("claim_boundary"):
        raise CatalogReviewError("Every extracted page requires an explicit claim boundary")
    if any(key in record for key in ("registered_entity_id", "canonical_operator_id", "registry_mutation")):
        raise CatalogReviewError("Catalog review must not allocate or mutate canonical identities")

    elements = record.get("research_elements") or {}
    unknown_fields = set(elements) - set(RESEARCH_ELEMENT_FIELDS)
    if unknown_fields:
        raise CatalogReviewError(f"Unknown research element fields: {sorted(unknown_fields)}")
    for field in RESEARCH_ELEMENT_FIELDS:
        values = elements.get(field, [])
        if not isinstance(values, list):
            raise CatalogReviewError(f"{field} must be a list")
        for value in values:
            if not isinstance(value, dict) or not value.get("statement"):
                raise CatalogReviewError(f"{field} entries require a statement")
            evidence = value.get("evidence")
            if not isinstance(evidence, list) or not evidence:
                raise CatalogReviewError(f"Unsupported semantic claim in {field}")
            if any(item.get("arena_block_id") != block_id for item in evidence):
                raise CatalogReviewError("Evidence must resolve to the reviewed source Block")
            if field == "operator_candidates" and value.get("canonical") is not False:
                raise CatalogReviewError("Operator candidates must be explicitly non-canonical")
