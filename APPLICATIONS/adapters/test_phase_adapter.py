# test_phase_adapter.py

from pipelines.phase_map import results  # ⚠️ nur wenn du results exportierst!

from APPLICATIONS.adapters.phase_space_adapter import PhaseSpaceAdapter


def main():

    print("\n=== TEST: PHASE → ADAPTER ===\n")

    try:
        adapter = PhaseSpaceAdapter(results)

        graph = adapter.to_state_graph()

        print("\n--- STATES ---")
        print(graph["states"])

        print("\n--- TRANSITIONS ---")
        for k, v in graph["transitions"].items():
            print(k, "→", v)

        print("\n--- METADATA ---")
        print(graph["metadata"])

    except Exception as e:
        print("ERROR:", e)


if __name__ == "__main__":
    main()
