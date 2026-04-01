# NEXAH / power_systems / stability_field_dynamics / iee_core_geometry

**Mathematical and Geometrical Foundations of the Instrument**

Dieser Ordner enthält die mathematischen und geometrischen Grundlagen des NEXAH-Instruments.

### Kernstrukturen
- **Phi–π–√2 Resonance** (Resonanz als Treiber)
- **5-Phi States + 5-Mode Drive** (Regulator + Drive-Modi)
- **Core Geometry als Vessel / Regime ODE**
- **Root Resonance Maps** (Phi-Pi-√2 Sphere, Root2025 etc.)

Diese Foundations sind direkt in den Field Layer und die Navigation integriert.

### Wichtige Erkenntnisse aus der 2D-Entwicklung (v13–v3.8)
- **Phi** ist der **echte Regulator** (startet bei 0, steigt stufenweise)
- **Q** wirkt als **Verstärker der Geometrie** (ab ~1.28 entsteht Band, ab ~1.5+ der Dolphin-Flip)
- **c(t)** zeigt klare **Dämpfungen/Lücken** → Regime-Übergänge
- **Phase Portrait** entwickelt sich von nested Möbius → Doppeltorus → Whale-Arc → Peitschen-Geometrie mit diskreten **Trauben/Perlen** (9 Grapes am Ende)
- **Diskrete Impulse** zwischen den Perlen (Herzschlag / Lymph-Effekt)
- **Selbstähnlichkeit**: Die große Form (Whale-Arc, Brezel) wiederholt sich im Kleinen als cp’s
- **Dolphin-Flip**: Der Moment, in dem Rotation + Counter-Rotation in eine Richtung kippen
- **Atem des Grids**: Das gesamte Feld pulsiert kontinuierlich

**Nächstes Ziel:** Übergang zur 3D Polar Grid mit Phi–π–√2 als dritter Dimension.

### Folder Structure
- `phi_geometry/`      → Resonance Maps, Spirals, 3×3 Interference
- `core_odes/`         → Alle Regime-ODEs (v13–v3.8 + IEEE-Integration)
- `resonance_maps/`    → Root2025_Final_Resonance_Map, Phi-Pi-Sphere etc.
