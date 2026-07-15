from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .registry import project_root


class OperationError(RuntimeError):
    pass


def default_review_root() -> Path:
    return project_root() / "LIBRARY" / "review"


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise OperationError(f"Cannot read operational source {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise OperationError(f"Expected a mapping in operational source {path}")
    return value


def dump_yaml(value: dict[str, Any]) -> str:
    return yaml.safe_dump(value, allow_unicode=True, sort_keys=False, width=100)


def latest_snapshot(review_root: Path) -> Path | None:
    snapshots = sorted((review_root / "source_snapshots").glob("arena-*.yaml"))
    return snapshots[-1] if snapshots else None
