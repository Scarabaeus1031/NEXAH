from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest
import yaml

from nexah.library.batch_a import SOURCE_IDS, generate_batch_a
from nexah.library.catalog_review import (
    CATALOG_DOMAINS,
    CatalogReviewError,
    duplicate_block_ids,
    record_is_stale,
    source_fingerprint,
    triage_publication,
    validate_visual_research_record,
)


ROOT = Path(__file__).resolve().parents[2]
BATCH = ROOT / "LIBRARY/catalog/review/orientation_foundations"


def load(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def records():
    return [load(path) for path in sorted((BATCH / "records").glob("*.yaml"))]


def test_six_domains_are_distinct_and_defined():
    domains = load(ROOT / "data/catalog_domains.yaml")["catalogs"]
    assert set(domains) == CATALOG_DOMAINS
    assert domains["publication"]["canonical_authority"] != domains["operator"]["canonical_authority"]
    assert "reading_path" in domains["publication"]["excluded_object_types"]
    assert "scientific_relation" in domains["navigation"]["excluded_object_types"]


def test_batch_has_exact_scope_and_no_mutations():
    batch = load(BATCH / "batch.yaml")
    assert batch["page_count"] == batch["triaged_page_count"] == 96
    assert batch["eligible_page_count"] == 69
    assert batch["deep_extraction_count"] == 12
    assert len(batch["source_publications"]) == 4
    assert not any(batch["mutations"].values())
    assert batch["series_assessment"]["canonical_series"] is False


def test_every_record_has_stable_source_provenance():
    for record in records():
        validate_visual_research_record(record)
        block = record["source_block"]
        assert record["page_key"] == f"arena-block:{block['arena_block_id']}"
        assert block["url"].endswith(str(block["arena_block_id"]))
        assert len(block["source_fingerprint"]) == 64


def test_review_state_validation_rejects_unknown_state():
    record = deepcopy(records()[0])
    record["review"]["review_state"] = "auto_accepted"
    with pytest.raises(CatalogReviewError, match="review_state"):
        validate_visual_research_record(record)


def test_unsupported_semantic_claim_is_rejected():
    record = deepcopy(next(item for item in records() if item["research_elements"]["definitions"]))
    record["research_elements"]["definitions"][0]["evidence"] = []
    with pytest.raises(CatalogReviewError, match="Unsupported semantic claim"):
        validate_visual_research_record(record)


def test_registry_or_operator_allocation_fields_are_rejected():
    record = deepcopy(records()[0])
    record["registered_entity_id"] = "NX-999999"
    with pytest.raises(CatalogReviewError, match="canonical identities"):
        validate_visual_research_record(record)


def test_review_module_has_no_arena_write_or_registry_capability():
    source = (ROOT / "nexah/library/catalog_review.py").read_text(encoding="utf-8")
    assert "ArenaClient" not in source
    assert "editorial_writer" not in source
    assert "create_block" not in source
    assert "move_connection" not in source
    assert "registry/entities" not in source


def test_triage_is_deterministic():
    publication = load(ROOT / "LIBRARY/catalog/works/arena-5416617.yaml")
    assert triage_publication(publication) == triage_publication(publication)
    first = publication["blocks"][0]
    assert source_fingerprint(publication["catalog_key"], first) == source_fingerprint(publication["catalog_key"], first)


def test_duplicate_source_blocks_are_detected():
    sample = records()[0]
    assert duplicate_block_ids([sample]) == []
    assert duplicate_block_ids([sample, deepcopy(sample)]) == [sample["source_block"]["arena_block_id"]]


def test_stale_source_detection_handles_change_and_missing_block():
    record = records()[0]
    channel_id = record["publication"]["arena_channel_id"]
    publication = load(ROOT / f"LIBRARY/catalog/works/arena-{channel_id}.yaml")
    assert record_is_stale(record, publication) is False
    changed = deepcopy(publication)
    block = next(item for item in changed["blocks"] if item["arena_block_id"] == record["source_block"]["arena_block_id"])
    block["updated_at"] = "2099-01-01T00:00:00Z"
    assert record_is_stale(record, changed) is True
    missing = deepcopy(publication)
    missing["blocks"] = [item for item in missing["blocks"] if item["arena_block_id"] != record["source_block"]["arena_block_id"]]
    assert record_is_stale(record, missing) is True


def test_unknown_content_is_explicit_not_invented():
    for record in records():
        assert record["visible_text"]["transcription_status"] in {"partial", "not_transcribed", "complete", "human_confirmed"}
        for field in record["research_elements"].values():
            assert isinstance(field, list)
        assert record["review"]["requires_human_review"] is True


def test_generated_batch_matches_checked_in_outputs(tmp_path):
    root = tmp_path
    for source_id in SOURCE_IDS:
        target = root / "LIBRARY/catalog/works" / f"arena-{source_id}.yaml"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((ROOT / "LIBRARY/catalog/works" / target.name).read_bytes())
    output = root / "LIBRARY/catalog/review/orientation_foundations"
    (output / "triage").mkdir(parents=True)
    (output / "records").mkdir(parents=True)
    summary = generate_batch_a(root)
    assert summary == load(BATCH / "batch.yaml")
    for generated in sorted(output.rglob("*.yaml")):
        relative = generated.relative_to(output)
        assert generated.read_bytes() == (BATCH / relative).read_bytes()
