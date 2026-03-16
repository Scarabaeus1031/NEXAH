# NEXAH Prototypen – Katalog

Dieser Ordner enthält die **ersten konkreten Mini-Anwendungen** (Prototypen), die mit NEXAH gebaut werden.

Alle Prototypen nutzen die **kernel_bridge.py** aus structured_oscillator_networks (Vortex-Metriken, Chimera-Status, Frustration-Score usw.).

Ziel: Aus abstrakter Theorie & Experimenten werden **echte, nutzbare Beispiele** („Häuser“).

## Übersicht der Prototypen

### 1. Lorenz Navigation Demo
**Ordner:** prototypes/lorenz  
**Beschreibung:** Chaos als navigierbare Regime-Landschaft (Attractor-Reconstruction, Basin-Boundaries, Resilience)  
**Bridge-Nutzung:** Vortex-Metriken, Chimera-Status, Frustration-Score  
**Running:**  
```bash
python -m APPLICATIONS.prototypes.lorenz.run_navigation_demo
```
Status: Bereits vorhanden – wird erweitert2. Power-Grid Blackout-RisikoOrdner: prototypes/power_grid (neu)
Beschreibung: Blackout-Risiko durch Frustration & Vortex in Phase-Sync von Stromnetzen
Bridge-Nutzung: Frustration-Score, Vortex-Metriken
Running:  bash

python -m APPLICATIONS.prototypes.power_grid.run_blackout_risk

Status: In Planung – PyPSA/MATPOWER-Adapter vorhanden3. Ökosystem KipppunktOrdner: prototypes/ecosystem (neu)
Beschreibung: Partielle Collapse (Chimera) & Resonanz in Predator-Prey / Ökosystemen
Bridge-Nutzung: Chimera-Status, Resonance-Score, Frustration
Running:  bash

python -m APPLICATIONS.prototypes.ecosystem.run_kipppunkt_analysis

Status: In Planung – einfaches Modell4. Finanz-Markt Crash-IndikatorOrdner: prototypes/finance (neu)
Beschreibung: Crash-Vorhersage durch Delayed Sync & Defekte in Markt-Phasen
Bridge-Nutzung: Frustration-Score, Vortex-Metriken
Running:  bash

python -m APPLICATIONS.prototypes.finance.run_crash_risk

Status: In Planung – Polygon-Daten möglichWeitere Ideen (zukünftig)Supply-Chain Cascade-Risiko
Klimakipppunkte (AMOC, Permafrost)
Neuronales Netz-Kollaps (AI-Instabilität)
Cyber-Physical Systems (IoT-Netze)

Jeder Prototyp folgt dem gleichen Muster:System-Simulation (PyPSA, Lotka-Volterra, Polygon usw.)
Phase-History extrahieren
Bridge für Metriken nutzen
Risiko & Navigation auswerten


