import matplotlib.pyplot as plt


class PolicyScoreboard:
    """
    Rank and visualize policy benchmark results.
    """

    def __init__(self, benchmark_results):
        self.benchmark_results = benchmark_results

    def rank_by_average_stability(self):
        """
        Return policies ranked by average stability.
        """

        valid = {
            name: metrics
            for name, metrics in self.benchmark_results.items()
            if metrics is not None
        }

        ranked = sorted(
            valid.items(),
            key=lambda item: item[1]["average_stability"],
            reverse=True
        )

        return ranked

    def print_ranking(self):
        """
        Print ranking table.
        """

        ranked = self.rank_by_average_stability()

        print("\nNEXAH POLICY SCOREBOARD\n")
        print("-" * 40)

        for i, (name, metrics) in enumerate(ranked, start=1):
            print(
                f"{i}. {name:22} "
                f"| avg={metrics['average_stability']:.2f} "
                f"| min={metrics['min_stability']:.2f} "
                f"| max={metrics['max_stability']:.2f} "
                f"| len={metrics['trajectory_length']}"
            )

    def plot(self, title="NEXAH Policy Scoreboard"):
        """
        Plot average stability for each policy.
        """

        ranked = self.rank_by_average_stability()

        names = [name for name, _ in ranked]
        scores = [metrics["average_stability"] for _, metrics in ranked]

        plt.figure(figsize=(10, 6))
        plt.bar(names, scores)

        plt.ylabel("Average Stability")
        plt.title(title)
        plt.xticks(rotation=15)

        for i, score in enumerate(scores):
            plt.text(i, score + 0.05, f"{score:.2f}", ha="center")

        plt.tight_layout()
        plt.show()
