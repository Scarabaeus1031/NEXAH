# tools/resilience_architecture_evolver_plot.py

import sys
import os
import re
import matplotlib.pyplot as plt


LOG_FILE = "evolver_log.txt"


def parse_history(path):

    generations = []
    scores = []

    pattern = re.compile(r"generation=(\d+).*best_score=([0-9.]+)")

    with open(path, "r") as f:

        for line in f:

            match = pattern.search(line)

            if match:

                g = int(match.group(1))
                s = float(match.group(2))

                generations.append(g)
                scores.append(s)

    return generations, scores


def plot_history(generations, scores):

    plt.figure(figsize=(8,5))

    plt.plot(
        generations,
        scores,
        marker="o",
        linewidth=2
    )

    plt.xlabel("Generation")
    plt.ylabel("Best Resilience Score")

    plt.title("Resilience Architecture Evolution")

    plt.grid(True)

    plt.show()


def main():

    if not os.path.exists(LOG_FILE):

        print("\nNo evolver log found.")
        print("Run evolver with:")
        print("python tools/resilience_architecture_evolver.py | tee evolver_log.txt")

        return

    g, s = parse_history(LOG_FILE)

    if not g:

        print("No history data found in log.")
        return

    plot_history(g, s)


if __name__ == "__main__":

    main()
