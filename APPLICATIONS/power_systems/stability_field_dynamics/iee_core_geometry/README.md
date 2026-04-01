cat > README.md << 'EOF'
# NEXAH / power_systems / stability_field_dynamics / iee_core_geometry

**Mathematische und geometrische Grundlagen des Instruments**

Hier liegen die neuen Core-Strukturen:
- Phi–π–√2 Resonance
- 5-Phi-Zustände + 5-Modi Drive
- Core Geometry als Vessel / Regime-ODE
- Root Resonance Maps

Diese Foundations werden direkt in den Field-Layer und die Navigation eingebaut.

### Ordnerstruktur

- `phi_geometry/`      → Resonance Maps, Spirals, 3×3 Interference
- `core_odes/`         → Regime-Navigationsgleichungen (ODEs)
- `resonance_maps/`    → Root2025_Final_Resonance_Map, Phi-Pi-Sphere etc.

Dieser Ordner ist das **mathematische Herz** des NEXAH-Instruments.
EOF

echo "✅ README.md wurde aktualisiert"
cat README.md
