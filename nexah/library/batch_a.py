from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .catalog_review import (
    RESEARCH_ELEMENT_FIELDS,
    source_block_url,
    source_fingerprint,
    triage_publication,
    validate_visual_research_record,
)


REVIEWED_AT = "2026-07-20T00:00:00Z"
SOURCE_IDS = (5416617, 5415690, 5309625, 5250350)
SELECTED_BLOCKS = {
    47707647: {
        "role": "definition",
        "transcription": "Orientation is the structured understanding of position, context, possibilities and direction within a complex system.",
        "definitions": ["Orientation is the structured understanding of position, context, possibilities and direction within a complex system."],
        "concepts": ["position", "context", "possibilities", "direction", "orientation"],
        "boundary": "Records an explicit definition printed by the publication; it does not establish a canonical Concept definition or domain-neutral scientific validity.",
    },
    47707644: {
        "role": "model",
        "transcription": "Transition geometry describes the shape of change between states in a complex system. Transitions are not points. They are regions with structure.",
        "definitions": ["Transition geometry describes the shape of change between states in a complex system."],
        "models": ["The page depicts Basin A → corridor → gate → bottleneck → corridor → Basin B."],
        "concepts": ["corridor", "gate", "bottleneck", "basin", "ridge", "transition geometry"],
        "atlas_objects": ["Visual anatomy of a transition"],
        "boundary": "The diagram is a publication model. It does not demonstrate that all transitions share this geometry or that the labels are canonical Operators.",
    },
    47707628: {
        "role": "evidence",
        "transcription": "What We Know — Validated Findings and Key Insights.",
        "evidence_statements": ["The page presents patterns, structure, transition rules, multi-scale connection, and navigation as validated findings."],
        "limitations": ["The visible page supplies summary claims but no independently inspected protocol, dataset, or validation record within this catalog review."],
        "boundary": "All findings remain publication assertions. The catalog does not mark them as validated repository evidence.",
    },
    47699758: {
        "role": "definition",
        "transcription": "Orientation Design is the study and intentional design of how humans and intelligent systems can understand, navigate and act in complex, dynamic worlds.",
        "definitions": ["Orientation Design is the study and intentional design of how humans and intelligent systems can understand, navigate and act in complex, dynamic worlds."],
        "questions": ["How can orientation be intentionally designed?"],
        "concepts": ["orientation design", "complex dynamic worlds"],
        "boundary": "This is the Work's field definition and central question, not a canonical discipline definition or validated claim of generality.",
    },
    47699746: {
        "role": "method",
        "transcription": "Observe → Structure → Represent → Analyze → Validate → Apply.",
        "methods": ["Method stack: Observe, Structure, Represent, Analyze, Validate, Apply."],
        "models": ["The page groups knowledge cartography, structural analysis, transition mapping, visual modeling, computational models, experimental validation, and atlas construction as method families."],
        "boundary": "The page documents a proposed method stack. It does not show that each family has been implemented or validated in every named domain.",
    },
    47699736: {
        "role": "research_question",
        "transcription": "We do not start with answers. We start with questions worth asking.",
        "questions": ["How do complex systems generate themselves?", "How can orientation be measured, not as output, but as state?", "How do transitions emerge?", "How can orientation be evaluated?", "How can we transfer orientation across domains?"],
        "boundary": "Questions are recorded as an authored research agenda. They are not answered, prioritized, or accepted by this catalog review.",
    },
    47026858: {
        "role": "model",
        "transcription": "Navigation follows instructions. Orientation chooses the right instructions.",
        "models": ["Captain Principle: many maps inform local orientation, decision, and action."],
        "limitations": ["The map is presented as a model and reality as final authority."],
        "concepts": ["navigation", "orientation", "decision", "action", "context"],
        "boundary": "The captain example is an editorial model. Its transfer to other systems is not independently demonstrated here.",
    },
    47026853: {
        "role": "model",
        "transcription": "Reality → Models → Map Ecosystem → Map Selection → Chrono-Compass → Orientation → Decision → Action.",
        "models": ["The NEXAH Map Orientation Framework organizes a stack from reality and models through map selection to action."],
        "open_questions": ["How should maps be ranked?", "How should maps be selected?", "Which clock matters most?", "Can map selection improve decisions?"],
        "boundary": "The framework is a publication proposal. No claim is made here that it is a canonical Kernel architecture or empirically confirmed pipeline.",
    },
    47026851: {
        "role": "research_question",
        "transcription": "How can an observer orient within an ecosystem of incomplete maps?",
        "questions": ["How can an observer orient within an ecosystem of incomplete maps?"],
        "hypotheses": ["The publication proposes that orientation, rather than prediction, is the most important capability for complex systems."],
        "models": ["Eight research pillars cover map discovery, relevance, regimes, scales, map ecosystems, dynamics, human and AI orientation, and navigation."],
        "boundary": "The hypothesis and pillars are the Work's stated research program, not supported findings or canonical system commitments.",
    },
    46658894: {
        "role": "map",
        "transcription": "NEXAH explores whether their structures can be mapped, translated and navigated.",
        "models": ["The page positions NEXAH between physics, cybernetics, control theory, complexity science, topology, cognitive science, power systems, AI, network science, and systems theory."],
        "atlas_objects": ["Scientific landscape", "Cartography stack", "Translation layer"],
        "boundary": "Spatial adjacency in the map expresses editorial positioning, not equivalence, shared mechanism, or disciplinary authority.",
    },
    46658897: {
        "role": "method",
        "transcription": "Observe → Recognize → Translate → Map → Navigate.",
        "definitions": ["The cartographer is presented as a perspective, not a person."],
        "methods": ["The cartographer's work is depicted as Observe, Recognize, Translate, Map, Navigate."],
        "concepts": ["cartographer", "observer", "translator", "navigator"],
        "boundary": "This is an editorial role model. It does not create a canonical actor class or Operator sequence.",
    },
    46658901: {
        "role": "transition",
        "transcription": "The Bridge — Between Vision and Validation.",
        "models": ["Vision → structural language → scientific language → actionable language is presented as a translation bridge."],
        "methods": ["The page connects vision, structure, validation, understanding, and impact as a bidirectional living process."],
        "boundary": "The bridge is an editorial architecture. It does not show that validation has occurred or that translated ideas are true.",
    },
}


ROLE_OVERRIDES = {
    5416617: {47707704: "foreword", 47707701: "index", 47707630: "part_opener", 47707527: "closing"},
    5415690: {47699761: "foreword", 47699760: "index", 47699719: "closing"},
    5309625: {47026852: "title_page", 47026825: "foreword", 47026826: "body_text", 47026829: "model", 47026824: "evidence"},
    5250350: {46658878: "title_page", 46997013: "model", 46658968: "map", 46658902: "map"},
}


def _load(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _dump(path: Path, data: dict[str, Any]) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")


def _evidence(block_id: int, level: str = "visible_page_text") -> list[dict[str, Any]]:
    return [{"evidence_level": level, "arena_block_id": block_id, "source_url": source_block_url(block_id), "note": None}]


def _assertions(block_id: int, statements: list[str], status: str = "publication_assertion") -> list[dict[str, Any]]:
    return [{"statement": statement, "evidence": _evidence(block_id), "status": status} for statement in statements]


def _research_record(publication: dict[str, Any], block_id: int, spec: dict[str, Any]) -> dict[str, Any]:
    block = next(item for item in publication["blocks"] if item["arena_block_id"] == block_id)
    elements = {field: [] for field in RESEARCH_ELEMENT_FIELDS}
    for field in RESEARCH_ELEMENT_FIELDS:
        if field in spec:
            elements[field] = _assertions(block_id, spec[field], "observed_label" if field in {"concepts", "atlas_objects"} else "publication_assertion")
    record = {
        "schema_version": "0.1",
        "authority": "noncanonical_catalog_review",
        "page_key": f"arena-block:{block_id}",
        "publication": {
            "catalog_key": publication["catalog_key"],
            "arena_channel_id": publication["source"]["arena_channel_id"],
            "title": publication["display_title"],
        },
        "source_block": {
            "arena_block_id": block_id,
            "sequence_index": block["sequence_index"],
            "title": block.get("title"),
            "url": source_block_url(block_id),
            "image_url": block["image"]["original_url"],
            "source_fingerprint": source_fingerprint(publication["catalog_key"], block),
        },
        "visual_role": spec["role"],
        "visible_text": {"transcription_status": "partial", "transcription": spec["transcription"]},
        "research_elements": elements,
        "claim_boundary": spec["boundary"],
        "review": {
            "method": "machine_assisted_visual_review",
            "extraction_status": "visually_reviewed",
            "review_state": "queued",
            "reviewed_at": REVIEWED_AT,
            "reviewed_by": "Codex visual review",
            "confidence": "high",
            "requires_human_review": True,
            "notes": "Partial transcription and bounded extraction; human acceptance pending.",
        },
    }
    validate_visual_research_record(record)
    return record


def generate_batch_a(root: Path) -> dict[str, Any]:
    output = root / "LIBRARY/catalog/review/orientation_foundations"
    publications = {
        source_id: _load(root / f"LIBRARY/catalog/works/arena-{source_id}.yaml")
        for source_id in SOURCE_IDS
    }
    triages = []
    for source_id, publication in publications.items():
        triage = triage_publication(publication, role_overrides=ROLE_OVERRIDES.get(source_id))
        triages.append(triage)
        _dump(output / "triage" / f"arena-{source_id}.yaml", triage)

    records = []
    for block_id, spec in SELECTED_BLOCKS.items():
        publication = next(
            publication for publication in publications.values()
            if any(block["arena_block_id"] == block_id for block in publication["blocks"])
        )
        record = _research_record(publication, block_id, spec)
        records.append(record)
        _dump(output / "records" / f"arena-block-{block_id}.yaml", record)

    summary = {
        "schema_version": "0.1",
        "batch_id": "catalog-review-orientation-foundations-a",
        "authority": "noncanonical_catalog_review",
        "review_state": "queued",
        "source_publications": [triage["publication"] for triage in triages],
        "page_count": sum(triage["page_count"] for triage in triages),
        "triaged_page_count": sum(len(triage["pages"]) for triage in triages),
        "eligible_page_count": sum(
            page["visual_review_result"] == "eligible_for_deeper_extraction"
            for triage in triages
            for page in triage["pages"]
        ),
        "deep_extraction_count": len(records),
        "series_assessment": {
            "relationship_status": "strongly_implied",
            "canonical_series": False,
            "evidence": "Shared Orientation framing plus explicit Volume II, Volume III, and Volume IV titles; ORIENTATION SCIENCE is a prospectus without a volume number.",
            "requires_human_review": True,
        },
        "mutations": {"arena": False, "registry": False, "proposal": False, "operator": False, "kernel": False},
    }
    _dump(output / "batch.yaml", summary)
    return summary
