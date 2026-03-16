from __future__ import annotations

from pathlib import Path


VISUALS_DIR = Path("visuals")
OUTPUT_FILE = VISUALS_DIR / "index.html"


def find_images():
    """
    Scan visuals directory for PNG images.
    """
    images = []
    for path in VISUALS_DIR.rglob("*.png"):
        rel = path.relative_to(VISUALS_DIR)
        images.append(rel)
    return sorted(images)


def build_html(images):
    """
    Build a simple HTML gallery.
    """

    items = []

    for img in images:
        items.append(
            f"""
<div class="item">
    <h3>{img}</h3>
    <img src="{img}" />
</div>
"""
        )

    html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>NEXAH Visual Navigator</title>

<style>

body {{
    font-family: Arial, sans-serif;
    background: #111;
    color: #eee;
    padding: 40px;
}}

h1 {{
    margin-bottom: 30px;
}}

.gallery {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
    gap: 30px;
}}

.item {{
    background: #1c1c1c;
    padding: 20px;
    border-radius: 10px;
}}

img {{
    max-width: 100%;
}}

</style>
</head>

<body>

<h1>NEXAH Visual Navigator</h1>

<div class="gallery">

{''.join(items)}

</div>

</body>
</html>
"""

    return html


def main():

    VISUALS_DIR.mkdir(exist_ok=True)

    images = find_images()

    html = build_html(images)

    OUTPUT_FILE.write_text(html)

    print("Wrote:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
