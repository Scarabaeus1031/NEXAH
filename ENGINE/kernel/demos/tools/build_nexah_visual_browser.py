"""
NEXAH Visual Browser Builder
============================

Creates a static HTML gallery for all generated visual patterns.

Reads:

demos/database/visual_catalog.csv
demos/database/atlas_index.json

Outputs:

demos/database/browser/index.html
"""

from pathlib import Path
import pandas as pd
import json

# --------------------------------------------------
# paths
# --------------------------------------------------

base_dir = Path(__file__).resolve().parent

database_dir = base_dir / "database"
visual_root = base_dir / "visuals"

browser_dir = database_dir / "browser"
browser_dir.mkdir(parents=True, exist_ok=True)

catalog_file = database_dir / "visual_catalog.csv"
index_file = database_dir / "atlas_index.json"

print("Loading catalog:", catalog_file)

df = pd.read_csv(catalog_file)

with open(index_file) as f:
    atlas_index = json.load(f)

# --------------------------------------------------
# HTML builder
# --------------------------------------------------

html = []

html.append("""
<html>
<head>
<title>NEXAH Visual Atlas</title>

<style>

body{
font-family: Arial;
background:#111;
color:#eee;
}

h1{
text-align:center;
}

.grid{
display:grid;
grid-template-columns:repeat(auto-fill,220px);
gap:14px;
padding:20px;
}

.card{
background:#222;
padding:10px;
border-radius:8px;
}

.card img{
width:200px;
height:200px;
object-fit:contain;
background:black;
}

.meta{
font-size:12px;
margin-top:5px;
color:#aaa;
}

</style>
</head>
<body>

<h1>NEXAH Visual Pattern Atlas</h1>

<div class="grid">
""")

# --------------------------------------------------
# build cards
# --------------------------------------------------

for _, row in df.iterrows():

    rel_path = Path(row["path"]).relative_to(base_dir)

    img_path = f"../../{rel_path}"

    n = row["symmetry_n"]
    drift = row["drift_deg"]
    atlas = row["atlas"]

    html.append(f"""
<div class="card">
<img src="{img_path}">
<div class="meta">
atlas: {atlas}<br>
n = {n}<br>
drift = {drift}
</div>
</div>
""")

# --------------------------------------------------
# finish html
# --------------------------------------------------

html.append("""
</div>
</body>
</html>
""")

html = "\n".join(html)

# --------------------------------------------------
# save html
# --------------------------------------------------

output_file = browser_dir / "index.html"

with open(output_file,"w") as f:
    f.write(html)

print("Browser created:", output_file)
