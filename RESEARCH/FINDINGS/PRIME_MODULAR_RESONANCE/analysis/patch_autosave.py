from pathlib import Path

BASE = Path(__file__).parent

HOOK = """

# ================= AUTO SAVE HOOK =================
import os
import matplotlib.pyplot as plt

if os.environ.get("AUTO_SAVE") == "1":

    figs = list(map(plt.figure, plt.get_fignums()))

    if not figs:
        print("[WARN] No figures to save.")

    for i, fig in enumerate(figs):
        filename = __file__.split("/")[-1].replace(".py", f"_{i}.png")
        fig.savefig(f"output/plots/{filename}", dpi=150, bbox_inches="tight")

    plt.close("all")

else:
    plt.show()

# =================================================
"""

for file in BASE.glob("*.py"):

    # wichtige Dateien NICHT anfassen
    if file.name in ["run_all_visuals.py", "patch_autosave.py"]:
        continue

    content = file.read_text()

    # schon gepatcht → skip
    if "AUTO_SAVE" in content:
        print(f"SKIP (already patched): {file.name}")
        continue

    print(f"PATCHING: {file.name}")

    file.write_text(content.rstrip() + "\n" + HOOK)

print("\nDONE: All scripts patched.")
