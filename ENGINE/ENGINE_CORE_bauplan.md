# NEXAH Discovery Engine Core — Building Plan

**Status:** Planning  
**Ziel:** Ein kleines, stabiles, überschaubares **Herzstück** des gesamten NEXAH-Projekts  
**Zielgröße:** deutlich unter 1000 Zeilen Code (idealerweise 600–800 Zeilen)  
**Name:** Discovery Engine Core (oder NEXAH Kernel Core)

---

## Warum dieser Core existieren muss

Der aktuelle ENGINE-Ordner ist bereits sehr groß und enthält viele Experimente, Tools und Research-Module.  
Das ist gut für die Kreativität, aber schlecht für Stabilität und Übersichtlichkeit.

Wir brauchen ein **kleines, klares, stabiles Kernstück**, auf dem alles andere aufbaut – ähnlich wie der Linux-Kernel:

- Minimal
- Gut definiert
- Sehr stabil
- Alles andere (Spiral Coupling, Research, Navigator, Applications, Visuals…) baut darauf auf

---

## Was der Core tun soll (Minimalverantwortung)

Der Discovery Engine Core soll **nur** folgende 6 Dinge können:

1. Struktur extrahieren aus rohen Zeitreihen / Zustandssequenzen
2. Field aufbauen (kontinuierliche geometrische Repräsentation)
3. Grey Channel / Dual-Strand erkennen und extrahieren
4. Coherence messen (und damit Stabilität bewerten)
5. Elastic Axis / Span-Gurt identifizieren
6. Triple Spiral Coupling (Water–Mercury–Ferrofluid) als Operator anbieten + Switch-Verhalten unterstützen

Das ist alles.

---

## Was der Core nicht tun soll (bewusste Grenzen)

- Keine Visualisierung
- Keine RL / Policy-Optimierung
- Keine konkreten Anwendungen (IEEE, Lorenz, etc.)
- Keine Web-Explorer / Dashboards
- Keine großen Simulationen oder Experimente
- Keine Trigger-Matrix oder Action-Logik

Diese Dinge bleiben außerhalb des Cores (in research/, applications/, navigator/, spiral_coupling/ etc.).

---

## Geplante Ordnerstruktur

ENGINE/
└── discovery_engine/          ← neuer, kleiner Core
    ├── __init__.py            ← öffentliche API
    ├── core.py                ← Field, Grey Channel, Coherence, Axis
    ├── coupling.py            ← Triple Spiral Coupling + Elastic Dual Lock
    ├── switch.py              ← Switch Detection & Logic
    ├── types.py               ← klare Datentypen (Field, Strand, etc.)
    ├── metrics.py             ← Coherence, Pair Coupling Distance, etc.
    ├── utils.py               ← kleine Helfer (falls nötig)
    └── README.md              ← dieses Dokument

Ziel: Der gesamte Ordner bleibt überschaubar und gut wartbar.

---

## Öffentliche API (Vorschlag)

from nexah.discovery_engine import DiscoveryEngine

engine = DiscoveryEngine()

field = engine.extract_field(state_history)
channel = engine.detect_grey_channel(field)
strands = engine.split_dual_strands(channel)
coherence = engine.compute_coherence(field)
coupling = engine.apply_spiral_coupling(strands)   # Water-Mercury-Ferro
switch_map = engine.detect_switches(coupling)

Das soll die einzige Schnittstelle sein, die von außen benutzt wird.

---

## Nächste konkrete Schritte (To-Do)

1. Ordner ENGINE/discovery_engine/ anlegen
2. Minimale __init__.py mit der oben genannten API erstellen
3. core.py und coupling.py mit den wichtigsten Klassen füllen
4. Bestehenden spiral_coupling/-Code so umbauen, dass er auf dem neuen Core aufbaut
5. Andere Teile des Projekts (Navigator, Research, Applications) auf die neue API umstellen

---

## Philosophie dieses Cores

- Klein und fokussiert bleiben
- Stabilität vor neuen Features
- Klare Schnittstellen (andere Module dürfen nur über die API zugreifen)
- Alles, was experimentell oder anwendungs-spezifisch ist, bleibt draußen

Das wird dann wirklich das **Herzstück** von NEXAH – der Teil, auf den du immer vertrauen kannst.

---

**NEXAH Discovery Engine Core**

Das kleine, stabile Fundament, auf dem alles andere aufbaut.
