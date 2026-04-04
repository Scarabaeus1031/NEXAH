import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Dual Dyad Werte (aus deinem Barycentric Wheel)
dyad_data = np.array([
    [0.63, 0.64, 0.83, 0.84],   # Haupt-Dyad
    [0.279, 0.628, 0.429, 0.537], # Lambda-Phi-Pi Offsets
    [0.213, 0.537, 0.729, 1.0]    # Kaprekar + Cube-Verbindungen
])

labels_rows = ['63:64', '0.279/0.628', 'Kaprekar']
labels_cols = ['A', 'φ', 'π', 'E']

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(dyad_data, annot=True, fmt='.3f', cmap='plasma', 
            xticklabels=labels_cols, yticklabels=labels_rows, 
            cbar_kws={'label': 'Resonance Strength'}, ax=ax)

ax.set_title('Navigation Heatmap – Dual Dyad (63:64 | 83:84) Horizontal', fontsize=16, pad=20)
ax.set_xlabel('Λ – φ – π – E  (Spiral Zones)')
ax.set_ylabel('Resonance Layer')

plt.tight_layout()
plt.savefig("nav_heatmap_dual_dyad_horizontal.png", dpi=300)
print("📸 Horizontale Dual-Dyad Heatmap gespeichert")
plt.show()
