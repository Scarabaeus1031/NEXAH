import os

ROOT = "FRAMEWORK/ARCHY"
OUTPUT = "FRAMEWORK/ARCHY_MODULE_INDEX.md"

sections = {
    "planet": "Planetary System Models",
    "urban": "Urban System Models",
    "infrastructure": "Infrastructure Networks",
    "stability_models": "Stability Models",
    "experiments": "Exploration & Optimization",
    "explorer": "Design Exploration Tools",
    "environments": "Simulation Environments",
    "visualization": "Visualization Tools"
}

modules = {k: [] for k in sections}

for root, dirs, files in os.walk(ROOT):
    for f in files:
        if f.endswith(".py") and "__pycache__" not in root:
            rel = os.path.join(root, f).replace("FRAMEWORK/ARCHY/", "")
            parts = rel.split(os.sep)

            if len(parts) > 1:
                section = parts[0]
                if section in modules:
                    modules[section].append(rel)

lines = []

lines.append("# ARCHY Module Index\n")
lines.append("This document provides an overview of the simulation modules implemented in the **ARCHY layer** of the NEXAH framework.\n")
lines.append("ARCHY currently contains a large collection of experimental models exploring planetary-scale system dynamics, including climate stress, infrastructure networks, economic cascades, migration flows, and collapse scenarios.\n")

lines.append("---\n")

lines.append("## Module Overview\n")
lines.append("ARCHY modules are grouped into functional domains corresponding to different simulation responsibilities.\n")

for key, title in sections.items():

    lines.append(f"\n## {title}\n")

    if modules[key]:
        for m in sorted(modules[key]):
            lines.append(f"- `{m}`")
    else:
        lines.append("_No modules detected._")

lines.append("\n---\n")
lines.append("## Notes\n")
lines.append("This index is automatically generated from the ARCHY directory structure. It reflects the current implementation state of the planetary simulation layer.\n")

lines.append("ARCHY is an experimental modeling environment designed to explore systemic interactions between environmental, economic, and geopolitical subsystems.\n")

with open(OUTPUT, "w") as f:
    f.write("\n".join(lines))

print("ARCHY module index generated.")
