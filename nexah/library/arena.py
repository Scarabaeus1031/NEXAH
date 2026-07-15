from __future__ import annotations

import hashlib
import json
import os
import time
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

from .registry import Registry, RegistryError


class ArenaError(RuntimeError):
    pass


@dataclass(frozen=True)
class ArenaClient:
    token: str | None = None
    base_url: str = "https://api.are.na/v3"
    timeout: float = 30.0

    @classmethod
    def from_environment(cls) -> "ArenaClient":
        return cls(token=os.environ.get("ARENA_TOKEN"))

    def _get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        query = f"?{urlencode(params)}" if params else ""
        url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}{query}"
        headers = {
            "Accept": "application/json",
            "User-Agent": "nexah-library-registry/0.1 (read-only comparison)",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        request = Request(url, headers=headers, method="GET")
        try:
            with urlopen(request, timeout=self.timeout) as response:
                return json.load(response)
        except HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise ArenaError(f"Are.na GET {path} failed with HTTP {exc.code}: {body[:300]}") from exc
        except (URLError, TimeoutError, json.JSONDecodeError) as exc:
            raise ArenaError(f"Are.na GET {path} failed: {exc}") from exc

    def get_channel(self, channel_id_or_slug: str | int) -> dict[str, Any]:
        return self._get(f"channels/{quote(str(channel_id_or_slug), safe='')}")

    def get_user_channels(
        self,
        user_id_or_slug: str | int,
        *,
        per: int = 24,
        max_pages: int = 50,
        delay: float = 0.25,
    ) -> list[dict[str, Any]]:
        """Read the public Channel inventory exposed by a user's contents."""
        channels: list[dict[str, Any]] = []
        page = 1
        while page <= max_pages:
            payload = self._get(
                f"users/{quote(str(user_id_or_slug), safe='')}/contents",
                {
                    "page": page,
                    "per": min(per, 100),
                    "type": "Channel",
                    "sort": "updated_at_desc",
                },
            )
            channels.extend(item for item in payload.get("data", []) if item.get("type") == "Channel")
            meta = payload.get("meta", {})
            if not meta.get("has_more_pages"):
                return channels
            page += 1
            time.sleep(delay)
        raise ArenaError(f"Stopped after {max_pages} pages while reading user {user_id_or_slug}")

    def get_contents(
        self,
        channel_id_or_slug: str | int,
        *,
        per: int = 24,
        max_pages: int = 50,
        delay: float = 0.25,
    ) -> list[dict[str, Any]]:
        contents: list[dict[str, Any]] = []
        page = 1
        while page <= max_pages:
            payload = self._get(
                f"channels/{quote(str(channel_id_or_slug), safe='')}/contents",
                {"page": page, "per": min(per, 100), "sort": "position_desc"},
            )
            contents.extend(payload.get("data", []))
            meta = payload.get("meta", {})
            if not meta.get("has_more_pages"):
                return contents
            page += 1
            time.sleep(delay)
        raise ArenaError(f"Stopped after {max_pages} pages while reading {channel_id_or_slug}")


def _normalized_title(value: str | None) -> str:
    return " ".join((value or "").split()).casefold()


def _sequence_fingerprint(contents: list[dict[str, Any]]) -> str:
    ordered = [
        {
            "id": item.get("id"),
            "position": item.get("connection", {}).get("position"),
            "type": item.get("type"),
        }
        for item in contents
    ]
    encoded = json.dumps(ordered, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def compare_entity(
    registry: Registry,
    entity_id: str,
    client: ArenaClient,
    *,
    include_sequence: bool = False,
) -> dict[str, Any]:
    entity = registry.entity(entity_id)
    external = entity["external_ids"]
    remote_payload = client.get_channel(external["arena_slug"])
    remote = remote_payload.get("data", remote_payload)
    differences: list[dict[str, Any]] = []

    checks = [
        ("arena_channel_id", external["arena_channel_id"], remote.get("id")),
        ("arena_slug", external["arena_slug"], remote.get("slug")),
        ("member_count", entity["edition"]["member_count"], remote.get("counts", {}).get("contents")),
        ("source_updated_at", entity["edition"].get("source_updated_at"), remote.get("updated_at")),
    ]
    for field, canonical, observed in checks:
        if canonical != observed:
            differences.append({"field": field, "registry": canonical, "arena": observed})

    expected_title = entity.get("display_title", entity["canonical_title"])
    if _normalized_title(expected_title) != _normalized_title(remote.get("title")):
        differences.append(
            {"field": "title", "registry": expected_title, "arena": remote.get("title")}
        )

    result: dict[str, Any] = {
        "entity_id": entity_id,
        "arena_slug": external["arena_slug"],
        "state": "current" if not differences else "stale",
        "differences": differences,
    }
    if include_sequence:
        contents = client.get_contents(external["arena_slug"])
        result["sequence"] = {
            "member_count": len(contents),
            "sha256": _sequence_fingerprint(contents),
        }
        if len(contents) != entity["edition"]["member_count"]:
            result["state"] = "stale"
    return result


def compare_all(
    registry: Registry, client: ArenaClient, *, include_sequence: bool = False
) -> list[dict[str, Any]]:
    registry.require_valid()
    return [
        compare_entity(registry, entity_id, client, include_sequence=include_sequence)
        for entity_id in sorted(registry.entities)
    ]
