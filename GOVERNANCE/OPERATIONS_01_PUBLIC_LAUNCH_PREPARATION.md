# OPERATIONS 01 — Public Launch Preparation

**Stand:** 21. Juli 2026  
**Geltungsbereich:** NEXAH Framework, ORION, NEXAH Experience und die derzeit
öffentlich sichtbaren historischen Repositorien  
**Entscheidung:** **HOLD — noch nicht öffentlich freigeben**

## 1. Auftrag und Bewertungsmaßstab

Dieser Bericht prüft die Publikationsreife des bestehenden Ökosystems. Er
ändert weder Verfassung noch Architektur, Semantik oder Implementierung.

Die Bewertung folgt der Governance-Hierarchie:

```text
Verfassung
    ↓
Governance
    ↓
Architektur
    ↓
Repository-Dokumentation
    ↓
Implementierung
    ↓
Abgeleitete Artefakte
```

Ein öffentlicher Start ist erst verantwortbar, wenn der öffentliche Zustand
dieselbe Geschichte erzählt wie der lokal geprüfte kanonische Zustand.

Prioritäten:

- **P0 — vor Launch erforderlich:** verhindert Vertrauen, Rechtsklarheit,
  Reproduzierbarkeit oder einen sicheren Einstieg.
- **P1 — nach Launch empfohlen:** verbessert Wartbarkeit und Zusammenarbeit,
  ist aber kein unmittelbarer Publikationsblocker.
- **P2 — später:** sinnvolle Weiterentwicklung ohne Bedeutung für den ersten
  öffentlichen Start.

## 2. Executive Summary

NEXAH ist **inhaltlich und architektonisch weit genug für die Vorbereitung
eines öffentlichen Starts**, aber **operativ noch nicht launchbereit**.

Positiv verifiziert wurden:

- die deutsche Ecosystem Constitution v1.0 ist lokal angenommen und
  kanonisch;
- das NEXAH Framework besteht lokal seine vollständige Testsuite;
- ORION besteht lokal seine Tests und seine Architekturprüfungen;
- die Experience erzeugt 195 statische Seiten, besteht Typ-, Test- und
  Linkprüfungen und enthält die vorgesehenen öffentlichen Räume;
- Kontakt, Datenschutz und Impressum sind angelegt;
- Experience, Framework, ORION, Library und Living Atlas behalten ihre
  getrennten Verantwortlichkeiten.

Der Launch wird derzeit durch fünf Gruppen von P0-Punkten blockiert:

1. **Öffentliche Erreichbarkeit:** `nexah.de` und `www.nexah.de` sind noch
   nicht als ein belastbarer kanonischer HTTPS-Einstieg nachgewiesen. Beim
   Review trat ein Zertifikatsfehler auf. Die Domain-Korrektur wird bewusst
   separat durchgeführt.
2. **Governance-Veröffentlichung:** Constitution v1.0, Governance Index und
   Adoption Report existieren lokal, sind im öffentlichen NEXAH-Repository
   aber noch nicht verfügbar.
3. **Öffentliche Repository-Gesundheit:** Der letzte geprüfte öffentliche
   NEXAH-CI-Lauf ist rot, obwohl die Tests lokal bestehen. Dieser Unterschied
   muss erklärt und durch einen grünen Lauf auf dem zu veröffentlichenden
   Stand geschlossen werden.
4. **Release- und Versionsklarheit:** Framework-Version `0.7.0`, Tags bis
   `v1.0.0` und die letzte GitHub Release `v0.5.0` erzählen drei verschiedene
   Geschichten. ORION und Experience besitzen noch keinen öffentlichen,
   reproduzierbaren Repository-Baseline-Stand.
5. **Rechtliche und operative Fakten:** Hosting-Anbieter, Serverstandort,
   Log-Empfänger und Log-Aufbewahrungsdauer sowie gegebenenfalls
   Umsatzsteuer-ID und Datenschutzbeauftragte müssen bestätigt werden.

Die Empfehlung lautet deshalb: **kontrollierter Launch nach einer kurzen
P0-Bereinigungsphase; kein stiller Soft Launch im aktuellen Zustand.**

## 3. Public Launch Checklist

### 3.1 Vor dem Launch erforderlich

| Bereich | Prüfung | Status | Erforderliche Maßnahme |
|---|---|---:|---|
| Website | Kanonischer Host (`nexah.de` oder `www.nexah.de`) festgelegt | Offen | Einen Host festlegen; den anderen dauerhaft darauf umleiten. |
| Website | HTTPS-Zertifikat für Apex- und WWW-Domain gültig | Blockiert | DNS, Zertifikat und Redirect getrennt vom Repository korrigieren und danach extern prüfen. |
| Website | Produktions-Build reproduzierbar | Bestanden | Bestehenden `pnpm verify`-Nachweis auf dem Release-Kandidaten wiederholen. |
| Website | Interne Links | Bestanden | 195 erzeugte HTML-Seiten ohne defekte interne Links; vor Deployment erneut prüfen. |
| Website | Canonical, robots und Sitemap | Vorhanden | Nach Festlegung des Hosts gegen die reale Produktions-URL prüfen. |
| Recht | Impressum vorhanden | Teilweise | Register- und Betreiberangaben final bestätigen; USt-IdNr./W-IdNr. angeben oder den Platzhalter entfernen, falls nicht einschlägig. |
| Recht | Datenschutz vorhanden | Teilweise | Hosting-Fakten, Serverstandort, Empfänger und Log-Frist ergänzen; DSB-Angabe bestätigen oder als nicht einschlägig entfernen. |
| Recht | Kontaktseite ohne versteckte Datenerhebung | Bestanden | `contact@nexah.de` vor Launch auf Empfang und Zuständigkeit testen. |
| Governance | Constitution v1.0 öffentlich erreichbar | Blockiert | Kanonische deutsche Fassung samt Governance Index publizieren. |
| Governance | Repository-Verantwortungen stimmen mit der Verfassung überein | Bestanden lokal | Öffentliche READMEs auf denselben Stand bringen. |
| Framework | Vollständige lokale Tests | Bestanden | 302 Tests bestanden; Warnungen dokumentieren, aber sie blockieren den Launch nicht. |
| Framework | Öffentliche CI auf Release-Kandidat grün | Blockiert | Fehler des letzten öffentlichen Laufs reproduzieren, beheben oder als Umgebungsabweichung erklären; danach grünen Lauf verlangen. |
| Framework | Version, Tag und Release eindeutig | Blockiert | Einen aktuellen Baseline-Namen festlegen und `0.7.0`, `v1.0.0` und Release `v0.5.0` konsistent erklären. Keine Tags umdeuten. |
| Framework | GitHub-Metadaten führen zum richtigen Einstieg | Blockiert | Falsches Homepage-Ziel auf eine reale kanonische Seite ändern. |
| ORION | Tests und Architekturchecks | Bestanden | 75 Tests bestanden, 1 Integrationstest übersprungen. |
| ORION | Development Release Gate | Blockiert | Erwarteten Core-Pin aktualisieren oder Workspace auf den erwarteten Stand bringen; verbundenen Core sauber halten. |
| ORION | Öffentliche, unveränderliche Baseline | Offen | Vor öffentlicher Referenz Remote, Lizenz, sauberen Commit und reproduzierbare Revision herstellen. |
| Experience | Statischer Build, Typen, Tests, Links | Bestanden | 53 Tests, Astro-Check und Build mit 195 Seiten bestanden. |
| Experience | Öffentliche, unveränderliche Baseline | Blockiert | Repository initial committen, lizenzieren, Remote und minimale CI festlegen. |
| Experience | Abhängige Revisionen nachvollziehbar | Teilweise | Exakte ORION- und Framework/Library-Revisionen für den Build dokumentieren. |
| Navigation | Website ↔ GitHub ↔ Dokumentation | Teilweise | Einen eindeutigen Repository-Einstieg in Laboratory/About und einen Rückweg zu `nexah.de` im Framework-README sicherstellen. |
| Historie | Historische Repositorien erscheinen nicht als aktuelle Autorität | Blockiert | Klare historische Banner setzen und historische Repositorien aus der primären Launch-Navigation bzw. den Pins nehmen. |
| Lizenzierung | Jeder zu veröffentlichende Code- und Inhaltskörper besitzt eine klare Lizenz | Teilweise | ORION und Experience lizenzieren; NEXAH-Dualität von Code- und Dokumentlizenz prominent erklären. |

### 3.2 Nach dem Launch empfohlen

- **P1:** Branch Rulesets für `main` mit erforderlicher CI und Review einführen.
- **P1:** Issue Templates, Pull-Request-Vorlage und `CODEOWNERS` in allen aktiv
  entwickelten öffentlichen Repositorien angleichen.
- **P1:** Security- und Dependency-Updates sichtbar betreiben.
- **P1:** Repository-Beschreibungen, Topics und Social Preview konsistent
  kuratieren.
- **P1:** Für große Repositorien Clone-Hinweise und einen flachen Clone-Weg
  dokumentieren; Asset-Auslagerung nur als eigene spätere Migration prüfen.
- **P1:** Entscheiden, ob GitHub Discussions einen realen moderierten Zweck
  erfüllt. Nicht allein der Vollständigkeit wegen aktivieren.
- **P1:** Einen regelmäßigen Link-, Build-, Domain- und Zertifikatscheck in
  Operations verankern.

### 3.3 Spätere Verbesserungen

- **P2:** Eine mögliche GitHub-Organisation erst nach stabiler öffentlicher
  Verantwortung und mehreren Mitwirkenden erneut bewerten.
- **P2:** Field Letters erst als öffentlichen Navigationspunkt aufnehmen, wenn
  ein kanonischer Publikationsort und mindestens ein belastbarer Inhalt
  existieren.
- **P2:** Die drei Governance-Diagramme als kanonische NEXAH Plates realisieren.
- **P2:** Historische Großbestände langfristig in klar ausgewiesene Archive
  überführen, ohne Geschichte umzuschreiben.

## 4. GitHub Readiness Report

### 4.1 Repository Readiness Matrix

| Repository / Bestand | Verfassungsrolle | Öffentlich | Reife | Hauptbefund | Launch-Rolle |
|---|---|---:|---:|---|---|
| [`Scarabaeus1031/NEXAH`](https://github.com/Scarabaeus1031/NEXAH) | Framework definiert; hält derzeit auch kanonische Governance und Library Registry | Ja | Gelb | Gute Community-Grundlage und lokale Tests; öffentliche Governance veraltet, CI rot, Release-Signale widersprüchlich, Repository sehr groß | Technischer und dokumentarischer Hub nach P0-Bereinigung |
| ORION (lokal) | Navigiert deterministisch; besitzt Reports, Validation und LYRA innerhalb seiner Grenze | Nein / kein Remote | Gelb | Architektur- und Testsuite gesund; Arbeitsbaum umfangreich unfertig, keine Lizenz, Release Gate blockiert | Nach Framework-Baseline als Entwicklungs-/Architektur-Baseline publizieren |
| NEXAH Experience (lokal) | Präsentiert und navigiert; besitzt temporären Interaktionszustand | Nein / kein Remote | Gelb | Vollständiger statischer Build; Repository besitzt noch keinen ersten Commit, keine Lizenz und keine CI | Öffentlicher Website-Quellstand nach ORION-Revisionierung und Domain-Fix |
| [`Scarabaeus1033/NEXAH-CODEX`](https://github.com/Scarabaeus1033/NEXAH-CODEX) | Historischer Forschungsbestand | Ja | Rot für Launch, Gelb als Archiv | Sehr groß; veraltete bzw. weitreichende Themen/Claims; Pages-Builds fehlerhaft; keine eindeutige Lizenz | Nicht als kanonischen Einstieg bewerben; als historisch kennzeichnen und prüfen |
| [`Scarabaeus1031/Scarabaeus1033-Archive`](https://github.com/Scarabaeus1031/Scarabaeus1033-Archive) | Historisches Archiv | Ja | Gelb als Archiv | Der Name sagt Archiv, GitHub-Status jedoch nicht; geringe Community-Vollständigkeit | Banner, Provenienz und Archivstatus klären; nicht pinnen |
| [`Scarabaeus1033/Scarabaeus1033-System-v1.0`](https://github.com/Scarabaeus1033/Scarabaeus1033-System-v1.0) | Historisches Systemartefakt | Ja, archiviert | Grün als historischer Snapshot | Technisch archiviert, aber ohne klaren Lizenznachweis | Als unveränderlichen historischen Snapshot belassen; nicht als aktuelle Architektur darstellen |

### 4.2 Standards nach aktivem Repository

| Standard | NEXAH | ORION | Experience | Bewertung |
|---|---:|---:|---:|---|
| Klare README | Ja, öffentlich noch nicht auf Governance-v1.0-Stand | Ja, lokal | Ja, lokal | P0: öffentliche Fassungen synchronisieren |
| LICENSE | Apache-2.0 plus Dokumentlizenzen | Fehlt | Fehlt | P0 für ORION und Experience |
| CONTRIBUTING | Ja | Ja | Fehlt | P0/P1: Experience benötigt zumindest einen klaren Status- und Beitragsweg |
| CODE_OF_CONDUCT | Ja | Fehlt | Fehlt | P1, sofern Beiträge geöffnet werden; vor aktivem Community-Aufruf ergänzen |
| SECURITY | Ja | Fehlt | Fehlt | P0 vor öffentlichem Software-Release |
| CHANGELOG | Kein eindeutiger aktueller öffentlicher Release-Verlauf | Ja | Fehlt | P0 für Baselines und Versionsklarheit |
| Issue Templates | Öffentlich nicht vollständig erkennbar | ADR/Research lokal | Fehlt | P1 |
| PR Template | Ja | Ja | Fehlt | P1 |
| CI | Vorhanden, letzter geprüfter Lauf rot | Lokal vorhanden | Fehlt | P0 |
| Tags / Releases | Tags und Paketversion widersprechen Release-Stand | Noch keine stabile Veröffentlichung | Keine | P0: Release-Erzählung festlegen |
| Branch-Schutz | Nicht nachgewiesen | Nicht anwendbar ohne Remote | Nicht anwendbar ohne Remote | P1 |

### 4.3 Öffentliche Metadaten und Sichtbarkeit

**P0-Korrekturen:**

- Die Homepage-Angabe des öffentlichen NEXAH-Repositories verweist auf einen
  nicht vorhandenen Pfad unter einem anderen Account. Sie muss auf
  `https://nexah.de`, die kanonische Governance-Seite oder die tatsächlich
  öffentliche Dokumentation zeigen.
- Das öffentliche README bezeichnet die Verfassung noch als Kandidat. Lokal ist
  Constitution v1.0 bereits angenommen. Erst die Publikation des lokalen
  Governance-Stands beseitigt diesen Widerspruch.
- Der letzte geprüfte öffentliche Workflow-Lauf des NEXAH-Repositories ist
  fehlgeschlagen. Ein lokaler grüner Test ersetzt keinen grünen CI-Nachweis für
  den veröffentlichten Commit.
- Historische Repositorien sind auf beiden persönlichen Profilen prominent
  angeheftet. Für den Launch sollten ausschließlich aktuelle kanonische
  Einstiege gepinnt sein.

**P1-Kuration:**

- Topics sollen die heutige Verantwortung benennen, nicht historische
  Forschungsansprüche fortschreiben.
- Repository-Beschreibungen sollen zwischen Framework, Navigation, Experience
  und Archiv unterscheiden.
- NEXAH ist mit ungefähr 1,9 GB und NEXAH-CODEX mit ungefähr 2,2 GB sehr groß.
  Das ist kein Grund für eine riskante History-Umschreibung vor Launch, aber ein
  deutlicher Wartungs- und Onboarding-Hinweis.

## 5. Ecosystem Navigation Review

### 5.1 Empfohlener öffentlicher Weg

```text
nexah.de
    ├── Visitor Guide / Library / Living Atlas / Laboratory
    └── Laboratory oder About
            ↓
      kanonisches GitHub-Repository
            ↓
      Governance → Architektur → Repository-Dokumentation
            ↓
      Research und Contribution
```

Dieser Weg ist absichtlich **kein Kreis aus gleichrangigen Plattformen**.
Jeder Ort führt zu seiner eigenen kanonischen Verantwortung und verweist für
andere Verantwortungen weiter.

### 5.2 Befunde

- **Website → GitHub:** Der Laboratory-Raum stellt bereits den plausibelsten
  technischen Übergang dar. Dieser Übergang sollte eindeutig beschriftet sein;
  GitHub muss nicht die globale Hauptnavigation dominieren.
- **GitHub → Website:** Das Framework-README benötigt nach dem Domain-Fix einen
  sichtbaren Rückweg zur öffentlichen Experience.
- **Library und Living Atlas:** Sie bleiben Räume der Experience mit eigener
  redaktioneller Autorität. GitHub darf ihre Inhalte dokumentieren, aber nicht
  ihre Bedeutung neu definieren.
- **Are.na:** Kann als externer visueller Forschungs- oder Sammlungsraum
  referenziert werden. Es darf nicht als unmarkierte kanonische Quelle für
  Framework-Semantik erscheinen.
- **Field Letters / Substack:** Derzeit wurde kein belastbarer öffentlicher
  kanonischer Einstieg nachgewiesen. Deshalb vorerst nicht in die primäre
  Launch-Navigation aufnehmen.
- **Contribution:** Der aktuelle Weg über das Framework-Repository ist
  ausreichend, sofern README, CONTRIBUTING und aktive Arbeitsorte konsistent
  benannt werden.

### 5.3 Vermeidbare Sackgassen

1. Falsche GitHub-Homepage-Angabe.
2. Öffentliche Verfassungslinks, die noch auf Kandidatenmaterial oder nicht
   publizierte Dateien zeigen.
3. Historische Repositorien ohne gut sichtbaren Archivhinweis.
4. Field-Letters-Verweise ohne kanonischen Zielort.
5. Website-Domain mit Zertifikats- oder Host-Konflikt.

## 6. Branding- und Terminologieprüfung

| Begriff | Kanonische öffentliche Bedeutung | Launch-Prüfung |
|---|---|---|
| NEXAH | Ökosystem; das Framework definiert seinen Orientierungsraum | Nicht als Synonym für jedes Repository verwenden |
| NEXAH Framework | Definiert Begriffe, Strukturen und Grenzen | Im Framework-README explizit benennen |
| OLS | Spezifiziert die formale Ordnung innerhalb des Frameworks | Nur ausschreiben, wo neue Leser den Kontext benötigen |
| Kernel | Führt deterministische Verträge aus | Nicht mit ORION oder dem gesamten Framework gleichsetzen |
| ORION | Navigiert deterministisch und berichtet Grenzen, Evidenz und Provenienz | Nicht als Chat, Website oder universelle AI darstellen |
| LYRA | Deterministische Sprachgrenze innerhalb der ORION-Verantwortung | Nicht als separates Produkt bewerben |
| Experience | Präsentiert Räume, Navigation und temporären Zustand | Nicht als Autorität für Framework- oder ORION-Semantik darstellen |
| Library | Erinnert; besitzt Publikationen und ihre kanonischen Metadaten | Nicht als ORION-Evidenz oder Empfehlungssystem darstellen |
| Living Atlas | Besitzt kuratierte, explizite Relationen | Keine inferred oder semantisch automatisch erzeugten Kanten behaupten |
| Research | Erforscht und darf offen oder vorläufig bleiben | Evidenzstatus und kanonische Grenzen sichtbar halten |
| Constitution | Höchste Governance; deutsche v1.0 ist kanonisch | Öffentlich publizieren und nicht in READMEs wiederholen |

## 7. Public Release Roadmap

### Phase A — P0-Bereinigung

1. Kanonischen Domain-Host festlegen; DNS, Zertifikat und permanente
   Weiterleitung reparieren.
2. Fehlende rechtliche und Hosting-Fakten bestätigen und Platzhalter
   beseitigen.
3. Constitution v1.0, Governance Index und Adoption Report in NEXAH
   veröffentlichungsfähig machen.
4. NEXAH-CI auf demselben Commit grün ausführen; öffentliche README- und
   Metadatenfehler korrigieren.
5. Framework-Versionsgeschichte erklären und einen neuen Baseline-Namen
   bestimmen, ohne alte Tags umzudeuten.
6. ORION-Arbeitsbaum konsolidieren, Core-Pin und Release Gate reparieren,
   Lizenz/Security ergänzen und eine unveränderliche Baseline bestimmen.
7. Experience initialisieren, lizenzieren, CI ergänzen und die exakten
   Eingangsrevisionen des statischen Builds protokollieren.

### Phase B — Veröffentlichungsreihenfolge

1. **Constitution v1.0** als Governance-Baseline. Empfohlen ist ein eindeutig
   benannter Governance-Release wie `constitution-v1.0`, damit er nicht mit
   Softwareversionen konkurriert.
2. **NEXAH Framework Baseline** nach grüner CI und geklärter Versionshistorie.
3. **ORION Architecture Baseline** als klar markierte Entwicklungsbaseline,
   nicht als Behauptung vollständiger Transformation-Ausführung.
4. **NEXAH Experience Alpha** mit reproduzierbarem statischem Build und
   festgehaltenen Eingangsrevisionen.
5. **Öffentlicher Start von `nexah.de`** erst nach finalem Domain-, Rechts-,
   Link- und Smoke-Test.

### Phase C — Unmittelbar nach Launch

1. Branch Rulesets und erforderliche Checks aktivieren.
2. Profile und Pins auf die aktuellen kanonischen Einstiege reduzieren.
3. Community-Einstieg beobachten und CONTRIBUTING/Issues nur anhand realer
   Fragen verfeinern.
4. Domain, Zertifikat, Builds und externe Links regelmäßig prüfen.

### Phase D — Später

- Historische Großbestände kuratieren und gegebenenfalls archivieren.
- Field Letters mit einem kanonischen Publikationsort eröffnen.
- Organisationsmigration nur bei realem Kollaborations- und Rechtebedarf.
- Governance-Diagramme als dauerhafte Plates realisieren.

## 8. Community Onboarding Review

| Frage eines neuen Besuchers | Aktuelle Antwort | Bewertung | Notwendige Verbesserung |
|---|---|---:|---|
| Was ist NEXAH? | Website und lokales Framework-README erklären den Orientierungsansatz | Gut lokal | Öffentliche README- und Website-Versionen synchronisieren |
| Wo beginne ich? | Experience bietet Home, Visitor Guide und fünf Räume | Gut | Domain-Erreichbarkeit herstellen |
| Wie ist es organisiert? | Constitution und Governance Index beantworten dies lokal | Blockiert öffentlich | Constitution v1.0 publizieren und einmal prominent verlinken |
| Wie kann ich beitragen? | NEXAH besitzt CONTRIBUTING; Experience/ORION sind noch nicht öffentlich vorbereitet | Teilweise | Aktive Arbeitsorte und akzeptierte Beitragsarten je Repository benennen |
| Wo findet aktive Arbeit statt? | Derzeit über mehrere lokale und öffentliche Zustände verteilt | Unklar | Pro Repository Status, Reife und aktuellen Arbeitsort im README nennen |
| Was ist kanonisch? | Governance ist lokal eindeutig | Unklar öffentlich | Kanonische/abgeleitete/historische Banner publizieren |

### Minimaler öffentlicher Einstieg

Ein neuer Besucher sollte ohne Architekturstudium folgende Reihenfolge erkennen:

1. **NEXAH ist ein Ort für Orientierung.**
2. **Die Experience ist der öffentliche Eingang.**
3. **Library, Living Atlas und Laboratory besitzen unterschiedliche Aufgaben.**
4. **GitHub zeigt Governance, Architektur, Forschung und Implementierung.**
5. **CONTRIBUTING erklärt, wo Beiträge wirklich willkommen sind.**

Nicht erforderlich ist, dass ein Besucher ORION, OLS oder den Kernel auf der
Startseite versteht.

## 9. Visual Strategy

Für die öffentliche Governance sind später genau drei kanonische visuelle
Begleiter sinnvoll:

1. **Constitutional Houses** — Zuständigkeiten und Autorität.
2. **Simplified Ecosystem** — Verständnis in weniger als einer Minute.
3. **Governance Hierarchy** — Verfassung bis abgeleitete Artefakte.

Bis SVG-Quellen und daraus erzeugte PNG-Dateien geprüft vorliegen, bleiben die
semantischen Diagramme in der Constitution die maßgebliche Quelle. Plates sind
visuelle Begleiter, keine konkurrierende Autorität. Eine Plate-Überarbeitung ist
nicht Teil dieses Launch-Reviews.

## 10. Verifikation

### Lokal ausgeführt

| Bestand | Befehl | Ergebnis |
|---|---|---|
| NEXAH Framework | `python -m pytest -q` | **302 bestanden**, 164 Warnungen |
| ORION | `make test` | **75 bestanden**, 1 übersprungen |
| ORION | `make release-check` | **fehlgeschlagen**: verbundener Core-Pin weicht ab und Core-Arbeitsbaum ist nicht sauber; übrige Architektur-/Boundary-/Plate-Prüfungen bestanden |
| Experience | `pnpm verify` | **bestanden**: ORION-Artefakt erzeugt, Astro 0 Fehler/Warnungen/Hinweise, 53 Tests, 195 Seiten, keine defekten internen Links |

### Öffentlich geprüft

- Repository-Metadaten, Tags, Releases, Branch-Status, Community-Dateien,
  Workflow-Status und Profil-Pins der vier bekannten öffentlichen
  Repositorien.
- Der letzte geprüfte öffentliche NEXAH-Workflow war fehlgeschlagen.
- Der Aufruf von `https://nexah.de` führte während des Reviews zu
  `ERR_CERT_COMMON_NAME_INVALID`; dieser Befund wird nach der separaten
  Domain-Korrektur neu geprüft.

### Nicht ausgeführt

- Kein Deployment.
- Kein Push und kein Commit.
- Keine Änderung an DNS, Zertifikaten, GitHub-Einstellungen, Sichtbarkeit,
  Releases oder Tags.
- Keine rechtliche Einzelfallprüfung durch eine qualifizierte Rechtsberatung.

## 11. Final Go / Hold Assessment

### Entscheidung: HOLD

Die Architektur ist nicht der Blocker. Die Experience ist nicht der Blocker.
Der Blocker ist die Differenz zwischen einem gut geprüften lokalen System und
einem noch widersprüchlichen öffentlichen Betriebszustand.

### Go-Kriterien

Ein **GO** ist angemessen, sobald alle folgenden Bedingungen gleichzeitig
erfüllt sind:

- [ ] `nexah.de` und `www.nexah.de` ergeben einen einzigen gültigen
  HTTPS-Einstieg mit korrekter Weiterleitung.
- [ ] Alle rechtlich erforderlichen Betreiber- und Hosting-Fakten sind ohne
  Platzhalter veröffentlicht.
- [ ] Constitution v1.0 und Governance Index sind öffentlich erreichbar.
- [ ] Der NEXAH-Release-Kandidat besitzt grüne öffentliche CI.
- [ ] Framework-Version, Tag und Release-Bedeutung sind dokumentiert und
  widerspruchsfrei.
- [ ] ORION und Experience besitzen saubere, lizenzierte und referenzierbare
  Baselines, sofern sie beim Launch öffentlich verlinkt werden.
- [ ] Öffentliche README-, Repository-Metadaten und Pins führen ausschließlich
  zu aktuellen oder klar als historisch markierten Orten.
- [ ] Der finale Produktions-Smoke-Test bestätigt Navigation, Legal Links,
  Canonical URL, Sitemap und Kontaktweg.

Sind diese Punkte erfüllt, empfiehlt Operations einen **kleinen, kontrollierten
öffentlichen Start** statt eines großen Produkt-Launches. NEXAH sollte zunächst
als belastbarer öffentlicher Ort erscheinen; Community- und Feature-Wachstum
folgen erst aus realer Nutzung.

