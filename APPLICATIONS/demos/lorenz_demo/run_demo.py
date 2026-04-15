import os
import subprocess
from datetime import datetime

# ---------------------------------------------------------
# Config
# ---------------------------------------------------------

BASE_DIR = os.path.dirname(__file__)
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

os.makedirs(OUTPUT_DIR, exist_ok=True)

scripts = [
    "lorenz_filament_3d.py",
    "lorenz_lyapunov_map.py",
    "lorenz_ftle_lcs_map.py",
    "lorenz_separatrix_map.py",
    "lorenz_chaos_navigation_map.py",
]

# ---------------------------------------------------------
# Run
# ---------------------------------------------------------

print("\n🚀 Running NEXAH Lorenz Demo\n")

start_time = datetime.now()
run_log = []

total = len(scripts)

for i, script in enumerate(scripts, start=1):
    path = os.path.join(SCRIPTS_DIR, script)

    print(f"[{i}/{total}] → Running {script}")

    start_script = datetime.now()

    result = subprocess.run(["python", path])

    end_script = datetime.now()
    duration = end_script - start_script

    run_log.append({
        "script": script,
        "returncode": result.returncode,
        "duration": duration
    })

    if result.returncode != 0:
        print(f"❌ Error in {script}")
    else:
        print(f"✅ Finished {script} ({duration})")

# ---------------------------------------------------------
# Summary
# ---------------------------------------------------------

end_time = datetime.now()
duration_total = end_time - start_time

summary_path = os.path.join(OUTPUT_DIR, "run_summary.txt")

with open(summary_path, "w") as f:
    f.write("NEXAH Lorenz Demo — Run Summary\n")
    f.write("=" * 40 + "\n\n")

    f.write(f"Start Time: {start_time}\n")
    f.write(f"End Time:   {end_time}\n")
    f.write(f"Duration:   {duration_total}\n\n")

    f.write("Executed Scripts:\n")
    f.write("-" * 20 + "\n")

    for entry in run_log:
        status = "OK" if entry["returncode"] == 0 else "FAIL"
        f.write(f"{entry['script']} → {status} ({entry['duration']})\n")

    f.write("\nGenerated Files:\n")
    f.write("-" * 20 + "\n")

    for root, _, files in os.walk(OUTPUT_DIR):
        for file in files:
            if file != "run_summary.txt":
                f.write(os.path.join(root, file) + "\n")

print(f"\n📄 Summary written to: {summary_path}")
print("\n✅ Demo complete.\n")
