from FRAMEWORK.explorer.system_explorer import SystemExplorer


def test_explorer():

    explorer = SystemExplorer(
        "APPLICATIONS/examples/energy_grid.json"
    )

    explorer.show_graph()

    explorer.print_risk()

    trajectory = explorer.run_navigation("stable")

    print("Trajectory:", trajectory)


if __name__ == "__main__":
    test_explorer()
