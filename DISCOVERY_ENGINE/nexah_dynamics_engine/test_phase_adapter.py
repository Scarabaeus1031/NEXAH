import sys
import os

# 🔥 ROOT FIX (damit APPLICATIONS gefunden wird)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

# 🔥 WICHTIG: run_phase_map importieren!
from pipelines.phase_map import run_phase_map, get_results
from APPLICATIONS.adapters.phase_space_adapter import PhaseSpaceAdapter


def main():

    print("\n=== TEST: PHASE → ADAPTER ===\n")

    try:
        # --------------------------------------------------
        # 🔥 STEP 1: PHASE MAP AUSFÜHREN (DATEN GENERIEREN)
        # --------------------------------------------------
        print("\n--- RUNNING PHASE MAP ---\n")
        run_phase_map()

        # --------------------------------------------------
        # 🔥 STEP 2: RESULTS HOLEN
        # --------------------------------------------------
        results = get_results()

        print(f"\nLoaded {len(results)} states\n")

        # --------------------------------------------------
        # 🔥 STEP 3: ADAPTER
        # --------------------------------------------------
        adapter = PhaseSpaceAdapter(results)
        graph = adapter.to_state_graph()

        # --------------------------------------------------
        # OUTPUT
        # --------------------------------------------------
        print("\n--- STATES ---")
        print(graph["states"])

        print("\n--- TRANSITIONS ---")
        for k, v in graph["transitions"].items():
            print(k, "→", v)

        print("\n--- METADATA ---")
        print(graph["metadata"])

    except Exception as e:
        print("\n❌ ERROR:", e)


if __name__ == "__main__":
    main()
