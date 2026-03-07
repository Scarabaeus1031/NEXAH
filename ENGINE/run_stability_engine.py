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
from ENGINE.analysis.stability_persistence_homology import StabilityPersistenceHomology
from ENGINE.analysis.stability_eigenmodes import StabilityEigenmodes
from ENGINE.analysis.stability_koopman_operator import StabilityKoopmanOperator
from ENGINE.analysis.stability_lyapunov_spectrum import StabilityLyapunovSpectrum
from ENGINE.analysis.stability_diffusion_map import StabilityDiffusionMap
from ENGINE.analysis.stability_wasserstein_geometry import StabilityWassersteinGeometry
from ENGINE.analysis.stability_topological_skeleton import StabilityTopologicalSkeleton

plt.style.use("dark_background")

VISUAL_DIR = "ENGINE/visuals"
os.makedirs(VISUAL_DIR, exist_ok=True)

def save_plot(name):

    path = os.path.join(VISUAL_DIR, name)

    fig = plt.gcf()
    fig.patch.set_alpha(0)

    plt.savefig(
        path,
        dpi=200,
        bbox_inches="tight",
        transparent=True,
        facecolor=fig.get_facecolor()
    )

    print("Saved:", path)

def main():

    print("\nRunning NEXAH Stability Engine\n")

    gen = StabilityLandscapeGenerator(size=80)
    X, Y, Z = gen.generate(peaks=3)

    plt.figure(figsize=(8,6))
    plt.contourf(X, Y, Z, 40, cmap="viridis")
    plt.title("Stability Landscape")
    save_plot("01_landscape.png")
    plt.close()

    grad = StabilityGradientField(X, Y, Z)
    grad.plot()
    save_plot("02_gradient_field.png")
    plt.close()

    hessian = StabilityHessianField(X, Y, Z)
    hessian.plot()
    save_plot("03_hessian_field.png")
    plt.close()

    crit = StabilityCriticalPoints(X, Y, Z)
    maxima, minima, saddles = crit.compute()
    crit.plot(maxima, minima, saddles)
    save_plot("04_critical_points.png")
    plt.close()

    seg = StabilityBasinSegmentation(X, Y, Z, maxima)
    basin_map = seg.compute()
    seg.plot(basin_map)
    save_plot("05_basin_segmentation.png")
    plt.close()

    btg = BasinTransitionGraph(basin_map, maxima)
    edges = btg.compute()
    btg.plot(edges)
    save_plot("06_basin_transition_graph.png")
    plt.close()

    meta = MetastabilityMap(X, Y, Z, basin_map, maxima, edges)
    transitions = meta.compute()
    meta.plot(transitions)
    save_plot("07_metastability_map.png")
    plt.close()

    global_struct = GlobalStabilityStructure(X, Y, Z, basin_map, maxima, minima, saddles, edges)
    global_struct.plot()
    save_plot("08_global_structure.png")
    plt.close()

    phase = StabilityPhasePortrait(X, Y, Z)
    phase.plot()
    save_plot("09_phase_portrait.png")
    plt.close()

    info = StabilityInformationGeometry(X, Y, Z)
    info.plot()
    save_plot("10_information_geometry.png")
    plt.close()

    morse = StabilityMorseComplex(X, Y, Z, maxima, minima, saddles)
    morse.plot()
    save_plot("11_morse_complex.png")
    plt.close()

    tda = StabilityPersistenceHomology(X, Y, Z)
    features = tda.compute()
    tda.plot_persistence_diagram(features)
    save_plot("12_persistence_diagram.png")
    plt.close()

    tda.plot_persistence_barcodes(features)
    save_plot("13_persistence_barcodes.png")
    plt.close()

    tda.plot_landscape_features(features)
    save_plot("14_persistent_features.png")
    plt.close()

    eig = StabilityEigenmodes(X, Y, Z)
    eigvals, modes = eig.compute()
    eig.plot(modes)
    save_plot("15_eigenmodes.png")
    plt.close()

    koop = StabilityKoopmanOperator(X, Y, Z)
    koopvals, koopvecs = koop.compute()
    koop.plot_spectrum(koopvals)
    save_plot("16_koopman_spectrum.png")
    plt.close()

    lyap = StabilityLyapunovSpectrum(X, Y, Z)
    lyapunov = lyap.compute()
    lyap.plot(lyapunov)
    save_plot("17_lyapunov_spectrum.png")
    plt.close()

    diff = StabilityDiffusionMap(X, Y, Z)
    diffvals, diffvecs = diff.compute()
    diff.plot(diffvecs)
    save_plot("18_diffusion_map.png")
    plt.close()

    X2, Y2, Z2 = gen.generate(peaks=3)
    wass = StabilityWassersteinGeometry(Z, Z2)
    distance = wass.compute()
    print(f"Wasserstein distance between landscapes: {distance:.6f}")
    wass.plot()
    save_plot("19_wasserstein_geometry.png")
    plt.close()

    skel = StabilityTopologicalSkeleton(X, Y, Z, maxima, minima, saddles)
    paths = skel.compute()
    skel.plot(paths)
    save_plot("20_topological_skeleton.png")
    plt.close()

    print("\nENGINE RUN COMPLETE")
    print("Visuals saved in:", VISUAL_DIR)

if __name__ == "__main__":
    main()

