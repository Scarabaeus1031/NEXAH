import numpy as np
import matplotlib.pyplot as plt

from nexah_kernel.regime.regime_detector import RegimeDetector
from nexah_kernel.regime.regime_graph import RegimeGraph
from nexah_kernel.navigation.navigator import Navigator


# ---------------------------------------------------------
# synthetic system
# ---------------------------------------------------------

def simulate():

    x = 0
    y = 0

    states = []

    for t in range(100):

        x += np.random.normal(0, 0.2)
        y += np.random.normal(0, 0.2)

        if t > 60:
            x += np.random.normal(0, 1.0)
            y += np.random.normal(0, 1.0)

        states.append((x, y))

    return np.array(states)


states = simulate()

# ---------------------------------------------------------
# regime detection
# ---------------------------------------------------------

detector = RegimeDetector()

regimes = []

window = 10

for i in range(len(states)):

    if i < window:
        regimes.append("UNKNOWN")
        continue

    series = states[i-window:i,0]
    regime = detector.detect(series)

    regimes.append(regime)


# ---------------------------------------------------------
# regime graph
# ---------------------------------------------------------

graph = RegimeGraph()

graph.add_regime("STABLE")
graph.add_regime("OSCILLATORY")
graph.add_regime("CHAOTIC")

graph.add_transition("STABLE","OSCILLATORY")
graph.add_transition("OSCILLATORY","CHAOTIC")

navigator = Navigator(graph)


# ---------------------------------------------------------
# visualization
# ---------------------------------------------------------

colors = {
    "UNKNOWN":"gray",
    "STABLE":"green",
    "OSCILLATORY":"orange",
    "CHAOTIC":"red"
}

plt.figure(figsize=(8,6))

for i in range(len(states)-1):

    r = regimes[i]
    c = colors.get(r,"gray")

    plt.plot(
        states[i:i+2,0],
        states[i:i+2,1],
        color=c
    )

plt.title("NEXAH Regime Map Navigation")
plt.xlabel("state x")
plt.ylabel("state y")

plt.show()


# ---------------------------------------------------------
# navigation example
# ---------------------------------------------------------

print("\nReachable regimes from STABLE:")
print(navigator.reachable_regimes("STABLE"))
