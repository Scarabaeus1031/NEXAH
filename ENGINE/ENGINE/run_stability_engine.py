import os
import numpy as np
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


# ---------------------------------------------------
# setup visuals directory
# ---------------------------------------------------

VISUAL_DIR = "ENGINE/visuals"

os.makedirs(VISUAL_DIR, exist_ok=True)


def save_current_plot(name):
    path = os.path.join(VISUAL_DIR, name)
    plt.savefig(path, dpi=200, bbox_inches="tight")
    print("saved:", path)


# ---------------------------------------------------
# 1 landscape
# ---------------------------------------------------

print("\nGenerating stability landscape...")

gen = StabilityLandscapeGenerator(size=80)

X, Y, Z = gen.generate(peaks=3)

plt.figure(figsize=(8,6))
plt.contourf(X, Y, Z, levels=40, cmap="viridis")
plt.title("Stability Landscape")
plt.xlabel("Axis X")
plt.ylabel("Axis Y")
save_current_plot("01_landscape.png")
plt.close()


# ---------------------------------------------------
# 2 gradient field
# ---------------------------------------------------

print("Computing gradient field...")

grad = StabilityGradientField(X, Y, Z)

grad.plot()

save_current_plot("02_gradient_field.png")
plt.close()


# ---------------------------------------------------
# 3 hessian field
# ---------------------------------------------------

print("Computing Hessian field...")

hessian = StabilityHessianField(X, Y, Z)

hessian.plot()

save_current_plot("03_hessian_field.png")
plt.close()


# ---------------------------------------------------
# 4 critical points
# ---------------------------------------------------

print("Finding critical points...")

crit = StabilityCriticalPoints(X, Y, Z)

maxima, minima, saddles = crit.compute()

crit.plot(maxima, minima, saddles)

save_current_plot("04_critical_points.png")
plt.close()


# ---------------------------------------------------
# 5 basin segmentation
# ---------------------------------------------------

print("Segmenting basins...")

basin = BasinTransitionGraph

basin_seg = BasinTransitionGraph

seg = BasinTransitionGraph

# segmentation module
from ENGINE.analysis.stability_basin_segmentation import StabilityBasinSegmentation

basin_seg = StabilityBasinSegmentation(X, Y, Z, maxima)

basin_map = basin_seg.compute()

basin_seg.plot(basin_map)

save_current_plot("05_basin_segmentation.png")
plt.close()


# ---------------------------------------------------
# 6 basin transition graph
# ---------------------------------------------------

print("Computing basin transitions...")

btg = BasinTransitionGraph(basin_map, maxima)

edges = btg.compute()

btg.plot(edges)

save_current_plot("06_basin_transition_graph.png")
plt.close()


# ---------------------------------------------------
# 7 metastability
# ---------------------------------------------------

print("Computing metastability...")

meta = MetastabilityMap(X, Y, Z, basin_map, maxima, edges)

transitions = meta.compute()

meta.plot(transitions)

save_current_plot("07_metastability_map.png")
plt.close()


# ---------------------------------------------------
# 8 global structure
# ---------------------------------------------------

print("Building global stability structure...")

global_struct = GlobalStabilityStructure(
    X,
    Y,
    Z,
    maxima,
    minima,
    saddles,
    edges
)

global_struct.plot()

save_current_plot("08_global_structure.png")
plt.close()


# ---------------------------------------------------
# 9 phase portrait
# ---------------------------------------------------

print("Computing phase portrait...")

phase = StabilityPhasePortrait(X, Y, Z)

phase.plot()

save_current_plot("09_phase_portrait.png")
plt.close()


# ---------------------------------------------------
# 10 information geometry
# ---------------------------------------------------

print("Computing information geometry...")

info = StabilityInformationGeometry(X, Y, Z)

info.plot()

save_current_plot("10_information_geometry.png")
plt.close()


# ---------------------------------------------------
# 11 morse complex
# ---------------------------------------------------

print("Computing Morse complex...")

morse = StabilityMorseComplex(X, Y, Z, maxima, minima, saddles)

morse.plot()

save_current_plot("11_morse_complex.png")
plt.close()


print("\nENGINE RUN COMPLETE")
print("Visuals saved in:", VISUAL_DIR)
