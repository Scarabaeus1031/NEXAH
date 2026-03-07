from FRAMEWORK.core.system_loader import load_system
from FRAMEWORK.ARCHY.regime_mapper import map_regimes
from FRAMEWORK.ARCHY.visualize_regimes import visualize_regime_map
from FRAMEWORK.MESO.risk_geometry import compute_risk_geometry
from FRAMEWORK.NEXAH.navigation_policy import compute_safe_path
from FRAMEWORK.MEVA.execution_engine import ExecutionEngine


class SystemExplorer:

    def __init__(self, system_file):

        self.system = load_system(system_file)

        self.regime_map = map_regimes(self.system)

        self.risk = compute_risk_geometry(self.regime_map)

        self.engine = ExecutionEngine(self.regime_map, self.risk)


    def show_graph(self):

        visualize_regime_map(self.regime_map)


    def run_navigation(self, start_state):

        self.engine.set_initial_state(start_state)

        def policy(state):

            path = compute_safe_path(state, self.regime_map, self.risk)

            if len(path) > 1:
                return path[1]

            return None

        trajectory = self.engine.run(policy)

        return trajectory


    def print_risk(self):

        print("Risk distance:", self.risk["risk_distance"])
        print("Risk gradient:", self.risk["risk_gradient"])
