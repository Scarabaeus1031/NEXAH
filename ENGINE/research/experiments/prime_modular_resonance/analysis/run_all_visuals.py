import subprocess
from pathlib import Path
from datetime import datetime
import os

# ============================================================
# CONFIG
# ============================================================

SCRIPTS = [
    "mod7_transition_matrix.py",
    "mod7_transition_matrix_ii.py",
    "mod7_top_transitions.py",
    "stationary_distribution_mod7.py",
    "mod_sweep_entropy.py",
    "mod17_transition_entropy.py",
    "spectral_modes_mod7.py",
    "spectral_flow_projection.py",
    "spectral_flow_complex_plane.py",
    "clockwise_vs_counterclockwise_mod7.py",
    "circulation_measure_mod7.py",
    "streamline_field_mod7.py",
    "energy_flux_field_mod7.py",
    "energy_density_map_mod7.py",
    "resonance_node_tracker_mod7.py",
    "basin_map_mod7.py",
    "basin_transition_dynamics_mod7.py",
    "basin_flow_field_visualizer.py",
    "loop_detection_mod7.py",
    "loop_stability_mod7.py",
    "circulation_loops_mod7.py",
    "cycle_detector_mod7.py",
    "cycle_flow_field_overlay.py",
    "vortex_field_detector_mod7.py",
    "diagonal_vortex_zoom_mod7.py",
    "threshold_pairs_2n_3n_analysis.py",
    "threshold_impact_on_mod7_flow.py",
    "edge_flow_circulation_mod7_mod11.py",
    "symmetry_break_circulation_mod7_mod11.py",
    "torus_projection_mod7.py",
    "triangle_flow_animation.py",
    "unified_flow_torus_map.py",
]

# ============================================================
# RUNNER
# ============================================================

def main():
    base = Path(__file__).parent

    output_dir = base / "output"
    plots_dir = output_dir / "plots"
    gifs_dir = output_dir / "gifs"
    log_dir = output_dir / "logs"

    plots_dir.mkdir(parents=True, exist_ok=True)
    gifs_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"pipeline_run_{timestamp}.log"

    print("\n🚀 RUNNING FULL VISUAL PIPELINE\n")

    with log_file.open("w", encoding="utf-8") as f:
        for script in SCRIPTS:
            script_path = base / script

            if not script_path.exists():
                msg = f"[SKIP] {script} (not found)\n"
                print(msg.strip())
                f.write(msg)
                continue

            print(f"▶ RUN: {script}")

            try:
                env = os.environ.copy()

                # 🔥 KEY TRICK
                env["MPLBACKEND"] = "Agg"  # no GUI
                env["AUTO_SAVE"] = "1"     # signal to scripts

                result = subprocess.run(
                    ["python", script],
                    cwd=base,
                    capture_output=True,
                    text=True,
                    timeout=120,
                    env=env
                )

                f.write(f"\n=== {script} ===\n")
                f.write(result.stdout)

                if result.stderr:
                    f.write("\n[stderr]\n")
                    f.write(result.stderr)

                if result.returncode != 0:
                    print(f"❌ ERROR in {script}")
                else:
                    print(f"✅ DONE: {script}")

            except subprocess.TimeoutExpired:
                msg = f"⏱ TIMEOUT: {script}\n"
                print(msg.strip())
                f.write(msg)

    print(f"\n📄 Log saved to: {log_file}")
    print("✅ PIPELINE COMPLETE\n")


if __name__ == "__main__":
    main()
