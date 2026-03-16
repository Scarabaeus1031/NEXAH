import numpy as np


class PolicyBenchmark:
    """
    Evaluate different policy trajectories using stability metrics.
    """

    def __init__(self, risk_map):
        self.risk_map = risk_map

    def evaluate(self, trajectory):
        """
        Compute stability metrics for a single trajectory.
        """

        values = []

        for state in trajectory:
            if state in self.risk_map:
                values.append(self.risk_map[state])

        if not values:
            return None

        values = np.array(values)

        metrics = {
            "average_stability": float(np.mean(values)),
            "min_stability": float(np.min(values)),
            "max_stability": float(np.max(values)),
            "trajectory_length": len(values)
        }

        return metrics

    def compare(self, trajectories):
        """
        Compare multiple trajectories.
        """

        results = {}

        for name, trajectory in trajectories.items():

            metrics = self.evaluate(trajectory)

            results[name] = metrics

        return results

    def print_report(self, trajectories):

        results = self.compare(trajectories)

        print("\nNEXAH POLICY BENCHMARK\n")
        print("-" * 40)

        for name, metrics in results.items():

            if metrics is None:
                print(f"{name}: no valid data")
                continue

            print(f"\nPolicy: {name}")
            print(f"Average Stability : {metrics['average_stability']:.2f}")
            print(f"Minimum Stability : {metrics['min_stability']:.2f}")
            print(f"Maximum Stability : {metrics['max_stability']:.2f}")
            print(f"Trajectory Length : {metrics['trajectory_length']}")
