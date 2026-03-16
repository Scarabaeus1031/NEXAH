"""
NEXAH Symmetry Graph – 3 Cycle Vortex Analysis
----------------------------------------------

Graph structure:

center node
17 spokes

Cycle layers:
C5  (pentagon)
C6  (hexagon A)
C6  (hexagon B)

Partition:
5 + 6 + 6 = 17

This version adds:

• phase assignment
• cycle detection
• vortex winding analysis
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import math

from core.symmetry_graph_vortex_detector import phase_winding


# -------------------------
# Build Graph
# -------------------------

def build_graph():

    G = nx.Graph()

    center = "center"
    G.add_node(center)

    spokes = [f"s{i}" for i in range(17)]

    for s in spokes:
        G.add_edge(center, s)

    pentagon = spokes[0:5]

    for i in range(5):
        G.add_edge(pentagon[i], pentagon[(i+1) % 5])

    hexagon1 = spokes[5:11]

    for i in range(6):
        G.add_edge(hexagon1[i], hexagon1[(i+1) % 6])

    hexagon2 = spokes[11:17]

    for i in range(6):
        G.add_edge(hexagon2[i], hexagon2[(i+1) % 6])

    return G


# -------------------------
# Layout
# -------------------------

def layout_graph(G):

    pos = {}

    center = "center"
    pos[center] = (0,0)

    radius = 3

    spokes = [n for n in G.nodes() if n != center]

    for i,node in enumerate(spokes):

        angle = 2 * math.pi * i / len(spokes)

        x = radius * math.cos(angle)
        y = radius * math.sin(angle)

        pos[node] = (x,y)

    return pos


# -------------------------
# Generate phases
# -------------------------

def generate_phases(G):

    theta = {}

    nodes = list(G.nodes())

    for i,node in enumerate(nodes):

        theta[node] = (2*np.pi*i)/len(nodes)

    return theta


# -------------------------
# Cycle analysis
# -------------------------

def analyze_cycles(G, theta):

    cycles = nx.cycle_basis(G)

    results = []

    for cycle in cycles:

        phase_list = np.array([theta[n] for n in cycle])

        w = phase_winding(phase_list, list(range(len(cycle))))

        results.append((cycle, w))

    return results


# -------------------------
# Draw graph
# -------------------------

def draw_graph(G, theta, results):

    pos = layout_graph(G)

    node_colors = [theta[n] for n in G.nodes()]

    plt.figure(figsize=(8,8))

    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=500,
        node_color=node_colors,
        cmap=plt.cm.hsv
    )

    nx.draw_networkx_edges(G,pos,width=1.8)
    nx.draw_networkx_labels(G,pos,font_size=9)

    for cycle, w in results:

        if abs(w) > 0.5:

            xs = [pos[n][0] for n in cycle]
            ys = [pos[n][1] for n in cycle]

            cx = np.mean(xs)
            cy = np.mean(ys)

            if w > 0:
                color = "red"
                label = "V"
            else:
                color = "blue"
                label = "A"

            plt.scatter(cx,cy,s=400,color=color,edgecolors="black",zorder=5)
            plt.text(cx,cy,label,color="white",ha="center",va="center")

    plt.title("NEXAH Symmetry Graph – Cycle Vortex Analysis")

    plt.axis("off")

    plt.tight_layout()

    plt.savefig("symmetry_graph_vortex_analysis.png",dpi=300)

    plt.show()


# -------------------------
# Run
# -------------------------

if __name__ == "__main__":

    G = build_graph()

    print("Nodes:",G.number_of_nodes())
    print("Edges:",G.number_of_edges())

    theta = generate_phases(G)

    results = analyze_cycles(G,theta)

    print("\nCycle analysis:")

    for cycle,w in results:

        print("cycle:",cycle,"winding:",round(w,3))

    draw_graph(G,theta,results)
