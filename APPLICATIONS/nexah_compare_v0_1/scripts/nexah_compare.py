#!/usr/bin/env python3
"""Repository-local entry point without requiring package installation."""

from __future__ import annotations

import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from nexah_compare.cli import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main())
