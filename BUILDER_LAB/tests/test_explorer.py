from FRAMEWORK.explorer.system_explorer import SystemExplorer


def test_explorer():
    """
    Runs the full NEXAH exploration pipeline.

    META   → system_loader
    ARCHY  → regime_mapper
    MESO   → risk_geometry
    NEXAH  → navigation policy
    MEVA   → execution trajectory
    """

    print("\n--- NEXAH System Explorer ---\n")

    explorer = SystemExplorer(
        "APPLICATIONS/examples/energy_grid.json"
    )

    # visualize regime graph
    explorer.show_graph()

    # print MESO risk geometry
    explorer.print_risk()

    # run navigation from initial state
    trajectory = explorer.run_navigation("stable")

    print("\nNavigation Trajectory:")
    print(trajectory)

    print("\n--- End of Explorer Run ---\n")


if __name__ == "__main__":
    test_explorer()
