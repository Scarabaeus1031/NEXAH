from FRAMEWORK.core.system_loader import load_system
from FRAMEWORK.ARCHY.regime_mapper import map_regimes
from FRAMEWORK.ARCHY.visualize_regimes import visualize_regime_map


def test_regime_mapper():

    system = load_system("APPLICATIONS/examples/energy_grid.json")

    regime_map = map_regimes(system)

    print("Collapse states:", regime_map["collapse_states"])
    print("Basins:", regime_map["basins"])
    print("Graph nodes:", regime_map["graph"].nodes())

    visualize_regime_map(regime_map)


if __name__ == "__main__":
    test_regime_mapper()
