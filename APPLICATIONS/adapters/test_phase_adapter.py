# test_phase_adapter.py

from pipelines.phase_map import get_results
from APPLICATIONS.adapters.phase_space_adapter import PhaseSpaceAdapter


def main():

    print("\n=== TEST: PHASE → ADAPTER ===\n")

    try:
        # 🔥 Ergebnisse aus Phase Map holen
        results = get_results()

        # 🔥 Adapter bauen
        adapter = PhaseSpaceAdapter(results)

        # 🔥 State Graph erzeugen
        graph = adapter.to_state_graph()

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
