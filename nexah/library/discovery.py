from __future__ import annotations

import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from .registry import Registry


SERIES_SIGNALS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("The Language Series", re.compile(r"^THE LANGUAGE BOOK(?:\s+[IVX]+)?$", re.I)),
    ("Field Atlas Series", re.compile(r"FIELD ATLAS", re.I)),
    ("Whiteboard Series", re.compile(r"WHITEBOARD SERIES", re.I)),
    ("NEXAH Mathematica", re.compile(r"NEXAH MATHEMATICA", re.I)),
    ("Orientation Atlas", re.compile(r"ORIENTATION ATLAS", re.I)),
    ("NEXAH Field Guides", re.compile(r"NEXAH FIELD GUIDES", re.I)),
)


def _description_plain(channel: dict[str, Any]) -> str:
    description = channel.get("description")
    if not isinstance(description, dict):
        return ""
    value = description.get("plain") or description.get("markdown") or ""
    return str(value).strip()


def _normalized_title(value: str) -> str:
    return " ".join(value.split()).casefold()


def _title_signals(title: str) -> list[str]:
    signals: list[str] = []
    if title != title.strip():
        signals.append("surrounding_whitespace")
    if re.search(r"\s{2,}", title.strip()):
        signals.append("repeated_spacing")
    if re.search(r"\bnew\s+release\b", title, re.I):
        signals.append("temporary_release_phrase")
    if "_" in title:
        signals.append("underscore_title")
    return signals


def build_discovery(
    registry: Registry,
    channels: list[dict[str, Any]],
    *,
    user_slug: str,
) -> dict[str, Any]:
    registered_by_arena_id = {
        entity["external_ids"]["arena_channel_id"]: entity_id
        for entity_id, entity in registry.entities.items()
    }
    records: list[dict[str, Any]] = []
    titles: dict[str, list[dict[str, Any]]] = defaultdict(list)
    series: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for channel in channels:
        channel_id = channel.get("id")
        title = str(channel.get("title") or "").strip("\n")
        description = _description_plain(channel)
        member_count = int(channel.get("counts", {}).get("contents") or 0)
        registered_id = registered_by_arena_id.get(channel_id)
        signals = _title_signals(title)
        if not description:
            signals.append("missing_description")
        if member_count == 0:
            signals.append("empty_channel")
        elif member_count <= 3:
            signals.append("small_channel")

        if registered_id:
            discovery_state = "registered"
        elif not description or member_count <= 3:
            discovery_state = "needs_review"
        else:
            discovery_state = "candidate_entity"

        owner_slug = channel.get("owner", {}).get("slug") or user_slug
        record = {
            "arena_channel_id": channel_id,
            "arena_slug": channel.get("slug"),
            "current_title": title,
            "current_description": description,
            "member_count": member_count,
            "created_at": channel.get("created_at"),
            "updated_at": channel.get("updated_at"),
            "visibility": channel.get("visibility"),
            "public_url": f"https://www.are.na/{owner_slug}/{channel.get('slug')}",
            "registered_entity_id": registered_id,
            "discovery_state": discovery_state,
            "signals": signals,
        }
        records.append(record)
        titles[_normalized_title(title)].append(record)
        for series_name, pattern in SERIES_SIGNALS:
            if pattern.search(title.strip()):
                series[series_name].append(record)

    records.sort(key=lambda item: (item["current_title"].casefold(), item["arena_channel_id"]))
    duplicates = [
        {
            "normalized_title": normalized,
            "channels": [item["arena_channel_id"] for item in group],
            "titles": [item["current_title"] for item in group],
        }
        for normalized, group in sorted(titles.items())
        if len(group) > 1
    ]
    possible_series = [
        {
            "title": series_name,
            "evidence": "title_pattern_only",
            "confidence": "low_until_structure_review",
            "members": [
                {"arena_channel_id": item["arena_channel_id"], "title": item["current_title"]}
                for item in sorted(group, key=lambda value: value["created_at"] or "")
            ],
        }
        for series_name, group in sorted(series.items())
        if len(group) > 1
    ]
    summary = {
        "total_public_channels": len(records),
        "already_registered": sum(item["discovery_state"] == "registered" for item in records),
        "probable_new_entities": sum(item["discovery_state"] == "candidate_entity" for item in records),
        "needs_review": sum(item["discovery_state"] == "needs_review" for item in records),
        "exact_title_duplicate_groups": len(duplicates),
        "title_cleanup_candidates": sum(bool(item["signals"]) for item in records),
        "possible_series_groups": len(possible_series),
    }
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "user_slug": user_slug,
        "scope": "public_channels_visible_to_the_read_only_client",
        "summary": summary,
        "channels": records,
        "exact_title_duplicates": duplicates,
        "possible_series": possible_series,
        "limitations": [
            "Private or otherwise unavailable Channels cannot be enumerated without authorized access.",
            "Discovery states are inventory hypotheses, not canonical classifications.",
            "Series signals are based on titles only and require structural review.",
            "No Are.na content or metadata was changed.",
        ],
    }


def _escape_table(value: Any) -> str:
    return str(value if value is not None else "").replace("|", "\\|").replace("\n", " ")


def render_discovery_markdown(discovery: dict[str, Any]) -> str:
    summary = discovery["summary"]
    lines = [
        "# NEXAH Library — Full Library Discovery",
        "",
        "**Phase VI · Pass A · Read-only inventory**",
        "",
        f"Generated: `{discovery['generated_at']}`",
        "",
        f"Are.na user: `{discovery['user_slug']}`",
        "",
        "This report is a discovery artifact, not a canonical classification. No new",
        "Registry identities are allocated here and no Are.na data was changed.",
        "",
        "## Summary",
        "",
        f"- Public Channels visible to the client: **{summary['total_public_channels']}**",
        f"- Already registered Pilot Works: **{summary['already_registered']}**",
        f"- Probable new Entity candidates: **{summary['probable_new_entities']}**",
        f"- Channels requiring early manual review: **{summary['needs_review']}**",
        f"- Exact normalized-title duplicate groups: **{summary['exact_title_duplicate_groups']}**",
        f"- Title or metadata cleanup candidates: **{summary['title_cleanup_candidates']}**",
        f"- Possible Series groups from title signals: **{summary['possible_series_groups']}**",
        "",
        "`candidate_entity` means only that the Channel has a description and more than",
        "three members. Family, Type, Form, status, and stable identity remain undecided",
        "until Pass B.",
        "",
        "## Exact normalized-title duplicates",
        "",
    ]
    if discovery["exact_title_duplicates"]:
        for duplicate in discovery["exact_title_duplicates"]:
            lines.append(
                f"- `{duplicate['normalized_title']}` — Channels "
                + ", ".join(str(value) for value in duplicate["channels"])
            )
    else:
        lines.append("No exact normalized-title duplicate groups were detected.")

    lines.extend(["", "## Possible Series signals", ""])
    if discovery["possible_series"]:
        for series in discovery["possible_series"]:
            lines.append(f"### {series['title']}")
            lines.append("")
            lines.append(
                f"Evidence: `{series['evidence']}` · Confidence: `{series['confidence']}`"
            )
            lines.append("")
            for member in series["members"]:
                lines.append(f"- {member['title']} (`{member['arena_channel_id']}`)")
            lines.append("")
    else:
        lines.append("No repeated title-pattern groups were detected.")

    cleanup = [item for item in discovery["channels"] if item["signals"]]
    lines.extend(
        [
            "## Cleanup and uncertainty signals",
            "",
            "These are review signals only. No title or description change is proposed or",
            "performed during Discovery.",
            "",
            "| Channel | Title | Signals |",
            "|---:|---|---|",
        ]
    )
    for item in cleanup:
        lines.append(
            f"| {item['arena_channel_id']} | {_escape_table(item['current_title'])} | "
            f"{', '.join(item['signals'])} |"
        )

    lines.extend(
        [
            "",
            "## Full public inventory",
            "",
            "| Arena ID | Current title | Members | Visibility | Registry | Discovery state | Updated |",
            "|---:|---|---:|---|---|---|---|",
        ]
    )
    for item in discovery["channels"]:
        lines.append(
            f"| {item['arena_channel_id']} | [{_escape_table(item['current_title'])}]"
            f"({item['public_url']}) | {item['member_count']} | {item['visibility']} | "
            f"{item['registered_entity_id'] or '—'} | {item['discovery_state']} | "
            f"{item['updated_at'] or '—'} |"
        )

    lines.extend(
        [
            "",
            "## Unavailable and private scope",
            "",
            "The report can only enumerate Channels visible to the read-only client. Private",
            "or missing references cannot be counted as discovered Channels unless authorized",
            "access later exposes them. They must be recorded separately when encountered in",
            "descriptions or human review.",
            "",
            "## Pass B boundary",
            "",
            "The next pass may inspect candidate structure and propose Family, Type, Form,",
            "Library Function, status, Series, Operators, and relationships. Proposed records",
            "must remain in the proposal overlay until human confirmation.",
            "",
        ]
    )
    return "\n".join(lines)


def write_discovery_files(
    discovery: dict[str, Any], *, report_path: Path, inventory_path: Path
) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    inventory_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(render_discovery_markdown(discovery), encoding="utf-8")
    inventory_path.write_text(
        yaml.safe_dump(discovery, allow_unicode=True, sort_keys=False, width=100),
        encoding="utf-8",
    )
