"""
NEXAH Resilience Pattern Detector

Analyzes stored experiments and detects structural resilience patterns.
"""

from ENGINE.results_store import load_all_results


class ResiliencePatternDetector:

    def __init__(self):

        self.results = load_all_results()

    def analyze(self):

        print("\nAnalyzing experiment results\n")

        if not self.results:
            print("No results found.")
            return

        resilience_scores = []

        for r in self.results:

            if "resilience" in r and "resilience_score" in r["resilience"]:
                resilience_scores.append(r["resilience"]["resilience_score"])

        if not resilience_scores:
            print("No resilience scores detected.")
            return

        avg = sum(resilience_scores) / len(resilience_scores)

        print("Experiments analyzed:", len(resilience_scores))
        print("Average resilience score:", round(avg, 3))
        print("Best resilience score:", round(max(resilience_scores), 3))
        print("Worst resilience score:", round(min(resilience_scores), 3))

        return {
            "experiments": len(resilience_scores),
            "average_resilience": avg,
            "best_resilience": max(resilience_scores),
            "worst_resilience": min(resilience_scores),
        }


def run_pattern_detection():

    detector = ResiliencePatternDetector()

    summary = detector.analyze()

    return summary


if __name__ == "__main__":

    run_pattern_detection()
