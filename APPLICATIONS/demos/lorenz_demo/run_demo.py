import os
import subprocess
from datetime import datetime

# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

BASE_DIR = os.path.dirname(__file__)
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------------------------------------------------
# Scripts to run
# ---------------------------------------------------------

scripts = [
    "lorenz_filament_3d.py",
    "lorenz_lyapunov_map.py",
    "lorenz_ftle_lcs_map.py",
    "lorenz_separatrix_map.py",
    "lorenz_chaos_navigation_map.py",
    # optional:
    # "lorenz_5d_polar_projection.py",
]

# ---------------------------------------------------------
# Run Demo
# ---------------------------------------------------------

print("\n🚀 Running NEXAH Lorenz Demo\n")

run_log = []
start_time = datetime.now()

for script in scripts:
    path = os.path.join(SCRIPTS_DIR, script)

    if not os.path.exists(path):
        print(f"⚠️  Skipping missing script: {script}")
        continue

    print(f"→ Running {script}")

    result = subprocess.run(
        ["python", path, "--output_dir", OUTPUT_DIR],
        capture_output=True,
        text=True
    )

    run_log.append({
        "script": script,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    })

    if result.returncode != 0:
        print(f"❌ Error in {script}")
        print(result.stderr)
    else:
        print(f"✅ Finished {script}")

# ---------------------------------------------------------
# Summary Report
# ---------------------------------------------------------

end_time = datetime.now()
duration = end_time - start_time

summary_path = os.path.join(OUTPUT_DIR, "run_summary.txt")

with open(summary_path, "w") as f:
    f.write("NEXAH Lorenz Demo — Run Summary\n")
    f.write("=" * 40 + "\n\n")

    f.write(f"Start Time: {start_time}\n")
    f.write(f"End Time:   {end_time}\n")
    f.write(f"Duration:   {duration}\n\n")

    f.write("Executed Scripts:\n")
    f.write("-" * 20 + "\n")

    for entry in run_log:
        status = "OK" if entry["returncode"] == 0 else "FAIL"
        f.write(f"{entry['script']} → {status}\n")

    f.write("\nGenerated Files:\n")
    f.write("-" * 20 + "\n")

    for root, _, files in os.walk(OUTPUT_DIR):
        for file in files:
            if file != "run_summary.txt":
                f.write(os.path.join(root, file) + "\n")

print("\n📄 Summary written to:", summary_path)
print("\n✅ Demo complete.\n")
