from FRAMEWORK.explorer.system_explorer import SystemExplorer


def test_explorer():

    explorer = SystemExplorer(
        "APPLICATIONS/examples/energy_grid.json"
    )

    print("\n--- GRAPH ---")
    explorer.show_graph()

    print("\n--- RISK ---")
    explorer.print_risk()

    print("\n--- NAVIGATION ---")
    trajectory = explorer.run_navigation("stable")

    print("Trajectory:", trajectory)


if __name__ == "__main__":
    test_explorer()
