# IEEE Test Systems in NEXAH

**Anwendung: Struktur-Extraktion und Navigation in realen Stromnetzen**

Dieser Ordner enthält die Integration der klassischen **IEEE Test Systems** (DER-Standard in der Power-Systems-Forschung) in das NEXAH-Framework.

### Warum IEEE Test Systems?

Die IEEE-Testnetze (14-bus, 30-bus, 57-bus, 118-bus etc.) sind weltweit der anerkannte Benchmark in der Energieforschung. Sie werden verwendet für:
- Stabilitätsanalysen
- Spannungskollaps-Studien
- Resilienz und Lastfluss-Berechnungen
- KI-gestützte Netzsteuerung

NEXAH nutzt diese etablierten Systeme, um zu zeigen:
- Wie aus realen physikalischen Netzen **Struktur extrahiert** werden kann
- Wie **Stabilitätslandschaften** entstehen
- Wie Agents ohne klassische Reward-Funktion in diesen Landschaften navigieren können

### Ziele dieses Use-Cases

1. IEEE-Netze als Graphen laden und in das NEXAH-Format bringen
2. Stabilitätslandschaften aus Last-/Erzeugungsvariationen erzeugen
3. Struktur (kritische Knoten, stabile Regionen, Übergänge) extrahieren
4. Multi-Agent-Navigation auf der Stabilitätslandschaft testen
5. Zeigen, dass NEXAH auf echten technischen Systemen funktioniert

### Aktueller Stand (März 2026)

- [ ] IEEE 14-bus Adapter + erste Stabilitätslandschaft
- [ ] IEEE 30-bus (folgt)
- [ ] IEEE 57-bus & 118-bus (geplant)
- [ ] Vergleich mit klassischen Power-Flow-Methoden

### Schnellstart

```bash
cd APPLICATIONS/power_systems/ieee_test_cases

# Einfache Demo starten (IEEE 14-bus)
python run_ieee_demo.py --system 14
```

### Weitere Optionen:

python run_ieee_demo.py --system 14 --plot
python run_ieee_demo.py --system 30


Nächste Schritte (Roadmap)

Grundlegender IEEE-Adapter (ieee_adapter.py)
Stabilitätslandschaft-Generator für Power Systems
Erste Multi-Agent-Navigation auf IEEE 14-bus
Erweiterung auf größere Netze (30-, 57-, 118-bus)
Vergleich mit klassischen Stabilitätsindizes (z. B. Voltage Stability Index)


Ziel dieses Anwendungsfalls:
NEXAH nicht nur auf abstrakte oder künstliche Systeme anzuwenden, sondern auf real anerkannte technische Benchmarks – und damit zu zeigen, dass die strukturelle Navigation auch in der Praxis relevant ist.
