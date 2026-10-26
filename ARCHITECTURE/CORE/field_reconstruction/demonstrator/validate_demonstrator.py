#!/usr/bin/env python3
"""Dependency-free integrity checks for the field reconstruction demonstrator."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
HTML = ROOT / "NEXAH_FIELD_RECONSTRUCTION_DEMONSTRATOR.html"


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


text = HTML.read_text(encoding="utf-8")
match = re.search(r'<script id="stage-data" type="application/json">\s*(.*?)\s*</script>', text, re.S)
if not match:
    fail("stage-data JSON block missing")

stages = json.loads(match.group(1))
expected_ids = [
    "delay", "sheet", "mesh", "boundary", "gradient", "stability", "smooth", "channels",
    "trajectory", "target", "v68", "v68-clean", "v69-clean", "resolution", "stable-mask", "transition",
]
actual_ids = [stage["id"] for stage in stages]
if actual_ids != expected_ids:
    fail(f"stage order mismatch: {actual_ids}")

required = {"id", "group", "title", "operation", "carrier", "image", "compare", "producer", "boundary"}
for stage in stages:
    missing = required - stage.keys()
    if missing:
        fail(f"{stage.get('id', '?')} missing fields: {sorted(missing)}")
    for key in ("image", "compare", "producer"):
        if key != "producer" and ".." in Path(stage[key]).parts:
            fail(f"{stage['id']} {key} escapes the browser package root: {stage[key]}")
        path = (ROOT / stage[key]).resolve()
        if not path.is_file():
            fail(f"{stage['id']} {key} missing: {path}")
    if len(stage["boundary"]) < 35:
        fail(f"{stage['id']} claim boundary is too weak")

for asset in (
    HERE / "field-reconstruction-demonstrator.css",
    HERE / "field-reconstruction-demonstrator.js",
):
    if not asset.is_file():
        fail(f"asset missing: {asset}")

for token in ("U / I WINDOW", "C | RIS | T", "ORANGE SPARK", "ANNOTATION LAYER · NOT A MEASUREMENT"):
    if token not in text:
        fail(f"annotation boundary token missing: {token}")

print(f"PASS: {len(stages)} stages, all assets/producers present, annotation boundary explicit")
