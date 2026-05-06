from FRAMEWORK.core.system_loader import load_system


def test_loader():

    system = load_system("APPLICATIONS/examples/energy_grid.json")

    print(system.nodes)
    print(system.regimes)
    print(system.risk_target)


if __name__ == "__main__":
    test_loader()
