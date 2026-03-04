from __future__ import annotations

from pathlib import Path
import subprocess


def write_dot(dot: str, path: str | Path) -> Path:
    """
    Write DOT text to file and ensure directory exists.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(dot)

    return path


def render_png(dot_file: str | Path, png_file: str | Path) -> None:
    """
    Call Graphviz to render PNG.
    """
    subprocess.run(
        ["dot", "-Tpng", str(dot_file), "-o", str(png_file)],
        check=True,
    )


def render_graph(
    dot: str,
    name: str,
    *,
    category: str = "graphs",
    base_dir: str = "visuals",
) -> tuple[Path, Path]:
    """
    High-level helper:

    DOT → file → PNG

    Example result:

    visuals/cfg/cfg_demo.dot
    visuals/cfg/cfg_demo.png
    """

    base = Path(base_dir) / category
    base.mkdir(parents=True, exist_ok=True)

    dot_path = base / f"{name}.dot"
    png_path = base / f"{name}.png"

    write_dot(dot, dot_path)
    render_png(dot_path, png_path)

    print("DOT:", dot_path)
    print("PNG:", png_path)

    return dot_path, png_path
