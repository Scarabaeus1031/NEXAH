from FRAMEWORK.MESO.stability_landscape import compute_stability_landscape
from FRAMEWORK.MESO.visualize_stability_landscape import visualize_stability_landscape
from FRAMEWORK.MESO.collapse_basin import compute_collapse_basin
from FRAMEWORK.MESO.visualize_collapse_basin import visualize_collapse_basin
from FRAMEWORK.MESO.stability_atlas import compute_stability_atlas
from FRAMEWORK.MESO.visualize_stability_atlas import visualize_stability_atlas
from FRAMEWORK.MESO.attractor_detection import detect_attractors
from FRAMEWORK.MESO.visualize_attractors import visualize_attractors

from FRAMEWORK.core.system_loader import load_system
from FRAMEWORK.ARCHY.regime_mapper import map_regimes
from FRAMEWORK.ARCHY.visualize_regimes import visualize_regime_map

from FRAMEWORK.MESO.risk_geometry import compute_risk_geometry
from FRAMEWORK.MESO.visualize_risk_landscape import visualize_risk_landscape
from FRAMEWORK.MESO.visualize_risk_labels import visualize_risk_labels

from FRAMEWORK.NEXAH.navigation_policy import compute_safe_path
from FRAMEWORK.NEXAH.visualize_navigation_path import visualize_navigation_path

from FRAMEWORK.MEVA.execution_engine import ExecutionEngine


class SystemExplorer:
    def __init__(self, system_file):

        self.system = load_system(system_file)
        self.regime_map = map_regimes(self.system)
        self.risk = compute_risk_geometry(self.regime_map)
        self.engine = ExecutionEngine(self.regime_map, self.risk)

    def show_graph(self):
        visualize_regime_map(self.regime_map)

    def show_risk_landscape(self):
        visualize_risk_landscape(self.regime_map, self.risk)

    def show_risk_labels(self):
        visualize_risk_labels(self.regime_map, self.risk)

    def show_navigation(self, start_state):
        path = compute_safe_path(start_state, self.regime_map, self.risk)
        visualize_navigation_path(self.regime_map, path)
        return path

    def show_collapse_basin(self):
        basin = compute_collapse_basin(self.regime_map)
        visualize_collapse_basin(self.regime_map, basin)
        return basin

    def show_stability_atlas(self):
        atlas = compute_stability_atlas(self.regime_map, self.risk)
        visualize_stability_atlas(self.regime_map, atlas)
        return atlas

    def show_attractors(self):
        attractors = detect_attractors(self.regime_map)
        visualize_attractors(self.regime_map)
        return attractors

    def run_navigation(self, start_state):

        self.engine.set_initial_state(start_state)

        def policy(state):
            path = compute_safe_path(state, self.regime_map, self.risk)
            if len(path) > 1:
                return path[1]
            return None

        return self.engine.run(policy)

    def print_risk(self):
        print("\nRisk distance:")
        print(self.risk["risk_distance"])

        print("\nRisk gradient:")
        print(self.risk["risk_gradient"])
        
    def show_stability_landscape(self):

    landscape = compute_stability_landscape(
        self.regime_map,
        self.risk
    )

    visualize_stability_landscape(
        self.regime_map,
        landscape
    )

    return landscape
