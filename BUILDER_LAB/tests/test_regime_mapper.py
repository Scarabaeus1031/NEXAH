from FRAMEWORK.core.system_loader import load_system
from FRAMEWORK.ARCHY.regime_mapper import map_regimes
from FRAMEWORK.ARCHY.visualize_regimes import visualize_regime_map
from FRAMEWORK.MESO.risk_geometry import compute_risk_geometry


def test_regime_mapper():

    system = load_system("APPLICATIONS/examples/energy_grid.json")

    regime_map = map_regimes(system)

    visualize_regime_map(regime_map)

    risk = compute_risk_geometry(regime_map)

    print("Risk distance:", risk["risk_distance"])
    print("Risk gradient:", risk["risk_gradient"])


if __name__ == "__main__":
    test_regime_mapper()
