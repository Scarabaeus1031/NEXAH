import os
import matplotlib.pyplot as plt

from ENGINE.analysis.stability_landscape_generator import StabilityLandscapeGenerator
from ENGINE.analysis.stability_gradient_field import StabilityGradientField
from ENGINE.analysis.stability_hessian_field import StabilityHessianField
from ENGINE.analysis.stability_critical_points import StabilityCriticalPoints
from ENGINE.analysis.stability_basin_segmentation import StabilityBasinSegmentation
from ENGINE.analysis.basin_transition_graph import BasinTransitionGraph
from ENGINE.analysis.metastability_map import MetastabilityMap
from ENGINE.analysis.global_stability_structure import GlobalStabilityStructure
from ENGINE.analysis.stability_phase_portrait import StabilityPhasePortrait
from ENGINE.analysis.stability_information_geometry import StabilityInformationGeometry
from ENGINE.analysis.stability_morse_complex import StabilityMorseComplex

VISUAL_DIR = "ENGINE/visuals"
os.makedirs(VISUAL_DIR, exist_ok=True)

def save_plot(name):
    path = os.path.join(VISUAL_DIR, name)
    fig = plt.gcf()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    print("Saved:", path)

def main():

    print("\nRunning NEXAH Stability Engine\n")

    gen = StabilityLandscapeGenerator(size=80)
    X, Y, Z = gen.generate(peaks=3)

    plt.figure(figsize=(8,6))
    plt.contourf(X, Y, Z, levels=40, cmap="viridis")
    plt.title("Stability Landscape")
    save_plot("01_landscape.png")
    plt.close()

    plt.figure()
    grad = StabilityGradientField(X, Y, Z)
    grad.plot()
    save_plot("02_gradient_field.png")
    plt.close()

    plt.figure()
    hessian = StabilityHessianField(X, Y, Z)
    hessian.plot()
    save_plot("03_hessian_field.png")
    plt.close()

    plt.figure()
    crit = StabilityCriticalPoints(X, Y, Z)
    maxima, minima, saddles = crit.compute()
    crit.plot(maxima, minima, saddles)
    save_plot("04_critical_points.png")
    plt.close()

    plt.figure()
    seg = StabilityBasinSegmentation(X, Y, Z, maxima)
    basin_map = seg.compute()
    seg.plot(basin_map)
    save_plot("05_basin_segmentation.png")
    plt.close()

    plt.figure()
    btg = BasinTransitionGraph(basin_map, maxima)
    edges = btg.compute()
    btg.plot(edges)
    save_plot("06_basin_transition_graph.png")
    plt.close()

    plt.figure()
    meta = MetastabilityMap(X, Y, Z, basin_map, maxima, edges)
    transitions = meta.compute()
    meta.plot(transitions)
    save_plot("07_metastability_map.png")
    plt.close()

    plt.figure()
    global_struct = GlobalStabilityStructure(
        X, Y, Z, basin_map, maxima, minima, saddles, edges
    )
    global_struct.plot()
    save_plot("08_global_structure.png")
    plt.close()

    plt.figure()
    phase = StabilityPhasePortrait(X, Y, Z)
    phase.plot()
    save_plot("09_phase_portrait.png")
    plt.close()

    plt.figure()
    info = StabilityInformationGeometry(X, Y, Z)
    info.plot()
    save_plot("10_information_geometry.png")
    plt.close()

    plt.figure()
    morse = StabilityMorseComplex(X, Y, Z, maxima, minima, saddles)
    morse.plot()
    save_plot("11_morse_complex.png")
    plt.close()

    print("\nENGINE RUN COMPLETE")
    print("Visuals saved in:", VISUAL_DIR)

if __name__ == "__main__":
    main()
