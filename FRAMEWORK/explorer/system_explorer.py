from FRAMEWORK.core.system_loader import load_system
from FRAMEWORK.ARCHY.regime_mapper import map_regimes
from FRAMEWORK.ARCHY.visualize_regimes import visualize_regime_map
from FRAMEWORK.MESO.risk_geometry import compute_risk_geometry
from FRAMEWORK.NEXAH.navigation_policy import compute_safe_path
from FRAMEWORK.MEVA.execution_engine import ExecutionEngine


class SystemExplorer:

    def __init__(self, system_file):
        """
        Initialize the full NEXAH pipeline.

        META   → system_loader
        ARCHY  → regime_mapper
        MESO   → risk_geometry
        NEXAH  → navigation_policy
        MEVA   → execution_engine
        """

        # META
        self.system = load_system(system_file)

        # ARCHY
        self.regime_map = map_regimes(self.system)

        # MESO
        self.risk = compute_risk_geometry(self.regime_map)

        # MEVA
        self.engine = ExecutionEngine(self.regime_map, self.risk)

    def show_graph(self):
        """
        Visualize the regime graph.
        """

        visualize_regime_map(self.regime_map)

    def run_navigation(self, start_state):
        """
        Run the NEXAH navigation policy starting from a given state.
        """

        self.engine.set_initial_state(start_state)

        def policy(state):

            path = compute_safe_path(state, self.regime_map, self.risk)

            if len(path) > 1:
                return path[1]

            return None

        trajectory = self.engine.run(policy)

        return trajectory

    def print_risk(self):
        """
        Print MESO risk geometry.
        """

        print("\nRisk distance:")
        print(self.risk["risk_distance"])

        print("\nRisk gradient:")
        print(self.risk["risk_gradient"])
