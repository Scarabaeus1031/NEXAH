# ENGINE/analysis/field_decomposition/scripts/save_pipeline.py

import json
import os
from datetime import datetime
from typing import Any

import matplotlib.pyplot as plt
import numpy as np


BASE_DIR = "ENGINE/analysis/field_decomposition"
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")


def ensure_dir(path: str) -> str:
    os.makedirs(path, exist_ok=True)
    return path


def script_stem(script_path: str) -> str:
    name = os.path.basename(script_path)
    return os.path.splitext(name)[0]


def get_run_dir(script_path: str) -> str:
    stem = script_stem(script_path)
    return ensure_dir(os.path.join(OUTPUTS_DIR, stem))


def save_figure(script_path: str, filename: str | None = None, dpi: int = 150, close: bool = True) -> str:
    run_dir = get_run_dir(script_path)
    if filename is None:
        filename = f"{script_stem(script_path)}.png"
    out_path = os.path.join(run_dir, filename)
    plt.savefig(out_path, dpi=dpi, bbox_inches="tight")
    if close:
        plt.close()
    return out_path


def save_array(script_path: str, name: str, arr: np.ndarray) -> str:
    run_dir = get_run_dir(script_path)
    out_path = os.path.join(run_dir, f"{name}.npy")
    np.save(out_path, arr)
    return out_path


def save_json(script_path: str, name: str, data: dict[str, Any]) -> str:
    run_dir = get_run_dir(script_path)
    out_path = os.path.join(run_dir, f"{name}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return out_path


def save_run_info(script_path: str, extra: dict[str, Any] | None = None) -> str:
    payload: dict[str, Any] = {
        "script": os.path.basename(script_path),
        "output_dir": get_run_dir(script_path),
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }
    if extra:
        payload.update(extra)
    return save_json(script_path, "run_info", payload)


def save_text(script_path: str, filename: str, text: str) -> str:
    run_dir = get_run_dir(script_path)
    out_path = os.path.join(run_dir, filename)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)
    return out_path
