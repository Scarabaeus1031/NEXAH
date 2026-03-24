from pathlib import Path

BASE = Path(__file__).parent

HOOK = """

# ================= AUTO SAVE HOOK =================
import os
import matplotlib.pyplot as plt

if os.environ.get("AUTO_SAVE") == "1":
    filename = __file__.split("/")[-1].replace(".py", ".png")
    plt.savefig(f"output/plots/{filename}", dpi=150, bbox_inches="tight")
    plt.close()
else:
    plt.show()
# =================================================
"""

for file in BASE.glob("*.py"):
    if file.name in ["run_all_visuals.py", "patch_autosave.py"]:
        continue

    content = file.read_text()

    if "AUTO_SAVE" in content:
        print(f"⏭ SKIP (already patched): {file.name}")
        continue

    print(f"🔧 PATCHING: {file.name}")
    file.write_text(content.strip() + "\n" + HOOK)

print("\n✅ DONE: All scripts patched.")und
