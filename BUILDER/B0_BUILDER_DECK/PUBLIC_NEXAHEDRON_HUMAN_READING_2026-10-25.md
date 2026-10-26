# Public · NEXAHEDRON Human Reading Bauplan

Stand: 25. Oktober 2026
Status: `CONCEPT_FREEZE / LOCAL ONLY / NO PUBLIC RELEASE / REUSE EXISTING SOURCES`

## Public design decision

NEXAHEDRON wird als geführte Human View gebaut, nicht als zweites Science Desk
und nicht als Sammlung aller vorhandenen HTML-Flächen. Der bestehende starke
Einstieg bleibt. Darunter entsteht eine klare Leseroute mit wenigen Räumen,
einem sichtbaren Fortschritt und einem verlässlichen Return.

Dieser Plan erzeugt keine neue Navigator-Identität, Relation, Study, Finding
oder Veröffentlichung. Er ordnet vorhandene Quellen und beschreibt einen
späteren lokalen Build Cut.

## Eine Route, klare Räume

```text
START
  -> READ
  -> LIGHT
       Dark Room
       Rainbow / Purple Rain
       Newton / Goethe / Leibniz
       Black Sun / Big Moon
       Light Return
  -> LOOK
       Diamond Lens
       optional: Look Again
  -> WORLD
       One Pulse / Game of Worlds
       Living Interior
  -> DOORS
       Books / series / further routes
  -> RETURN TO HUMAN
```

Nur der gewählte Raum öffnet seine Tiefe. Die obere Streckenleiste zeigt Ort,
Fortschritt und Return. Ein Sprung in ein Spiel oder eine Bench darf den
Lesepfad nicht ersetzen.

## Public game-window contract

NEXAHEDRON zeigt **keine vollständige Arcade**. Die Arcade ist Inventar und
Werkstattfläche für Builder. Im Human View werden vorhandene Spiele einzeln und
redaktionell begründet geöffnet:

1. höchstens drei kuratierte Fortsetzungen gleichzeitig sichtbar;
2. ein Satz erklärt, warum dieses Erlebnis an dieser Stelle folgt;
3. immer nur ein Game-/Experience-Fenster ist offen;
4. `Close & Return` bringt Fokus und Scrollposition zum auslösenden Einstieg
   zurück;
5. `Reset` innerhalb eines Spiels ist niemals der Return aus dem Fenster;
6. technische Varianten, Bench-Metadaten und Vollinventar bleiben im Builder.

Erster Public Cut: `One Pulse`, `The Living Interior` und ein ruhiger Reader.
`Look Again` bleibt eine freiwillige LOOK-Vertiefung. Die große Arcade wird
nicht aus der Consumer-Hauptstrecke verlinkt.

LIGHT verwendet nach der Rainbow-Light-Basistour einen **Two-door cut**:
`Seeing Light` öffnet `Rainbow / Purple Rain`, `Understanding Light` öffnet die
`Newton / Leibniz / Goethe Observer Lens`. Erst nach der Rückkehr wird `Black
Sun / Big Moon` als freiwillige tiefere Tür angeboten. Jede dieser Türen nutzt
dasselbe `Close & Return`-Fenster; keine ersetzt den Hauptpfad zu LOOK.

## Was wohin gehört

| Objekt | Rolle im Human Reading | Entscheidung |
|---|---|---|
| Dark Room | Anfang der LIGHT-Route | bleibt erster Licht-Raum |
| Rainbow / Purple Rain | Licht wird als veränderliche Erscheinung erfahrbar | in LIGHT führen |
| Newton / Goethe / Leibniz | verschiedene Beobachter- und Beschreibungsweisen | nach der ersten Erfahrung |
| Black Sun / Big Moon | starker visueller Gegenraum | freiwillige zweite Tiefe nach einer LIGHT-Tür |
| Neon / Trap Door | Seitentür / Überraschung | optional, nicht Hauptpfad |
| Diamond Lens | derselbe Carrier, andere deklarierte Ansicht | primärer LOOK-Raum |
| Look Again game | spielerischer Vorher-/Nachher-Vergleich | sekundär; nicht am Ende des Dark Room erzwingen |
| One Pulse / Game of Worlds | LIFE, Rhythmus und World Building | nach LOOK als WORLD öffnen |
| Living Interior | vertiefender begehbarer Welt-Raum | WORLD-Folge, nicht Einstiegsseite |
| Rödelheim Observatory | kein NEXAHEDRON-Hauptraum | Scarabæus-Haus; eigene spätere Tour über M-ROO02; release-gated |

## Reader takeaway

Die Route soll nicht möglichst viele Artefakte zeigen. Sie soll einen
verständlichen inneren Ablauf tragen:

1. **Attention** — wahrnehmen, was da ist und welcher Rahmen gesetzt wurde.
2. **Orientation** — Quelle, Position, Ausschnitt und Veränderung erkennen.
3. **Distinction** — Welt, Ansicht und Relation nicht verwechseln.
4. **Clear Mind** — Unterschied, Unsicherheit und Rest aushalten, ohne sie
   vorschnell zu schließen.
5. **Human Return** — mit einer besseren Frage, einem Widerspruch, einer
   Entscheidung oder `noch nicht` zurückkehren.

Kurz: **Der Unterschied wird lesbar.** Das ist ein Gestaltungsziel, keine
behauptete Human-Utility-Wirkung.

## Book feature grammar

Die Library bleibt ein Modul, nicht der ganze Einstieg. Pro Feature wird nur
ein Buch geöffnet:

```text
POSTER / COVER
  -> WHY READ
  -> ONE SCENE OR CHAPTER
  -> READER
  -> VISIBLE RETURN
```

Geeignete erste Features:

- **The Visitor's Guide** — Einstieg, Orientierung und Räume;
- **The NEXAH Language Book** — Context and Cases; Unterschiede lesen;
- **The Operator's Handbook** — Projection und Observer;
- **The Wonder Operator** — Attention, Spiel, Staunen und Clear Mind.

Kein Katalogdump, keine sieben gleichwertigen Türen und keine rein dekorative
Buchfläche. Cover, ein konkreter Grund zum Lesen und ein klarer Rückweg genügen.

## Build sequence

### WP0 · Route freeze

- vorhandene Human-View-Quellen und Anker bestätigen;
- LIGHT, LOOK und WORLD sauber trennen;
- Look Again aus dem erzwungenen Dark-Room-Ende lösen;
- Hauptpfad auf höchstens drei primäre Entscheidungen pro Raum begrenzen.

### WP1 · Local projection

- vorhandenen NEXAHEDRON-Einstieg behalten;
- Streckenleiste `START / READ / LIGHT / LOOK / WORLD / DOORS / RETURN` bauen;
- Räume progressiv öffnen und wieder schließen;
- Wechsel zwischen Räumen ohne langen Rückscroll ermöglichen.
- vorhandene Games in ein begrenztes Fenster mit `Close & Return` einbetten;
- Fokus und Leseposition nach dem Schließen wiederherstellen.

### WP2 · Feature rooms

- LIGHT als geführte visuelle Folge;
- LOOK mit Diamond Lens als Hauptinstrument;
- WORLD erst nach LOOK mit One Pulse und Living Interior;
- genau ein Book Feature als Muster bauen, bevor weitere Serien folgen.

### WP3 · Acceptance

- Desktop, 390 px, Tastatur, Reduced Motion und Missing Source;
- Quelle, View und Return in jedem geöffneten Raum sichtbar;
- kein toter schwarzer Frame;
- keine Bench als Consumer-Hauptansicht;
- externe oder tiefe Fenster schließen oder zur Route zurückführen können.

### WP4 · Owner / release gate

- lokale Abnahme und Screenshot-Receipt;
- Builder Return an Mission Control;
- erst danach Entscheidung über NEXAHEDRON-Deployment und nexah.de-Tür.

## Acceptance questions

Nach der Route kann eine neue Leserin oder ein neuer Leser in eigenen Worten
sagen:

- Was blieb gleich?
- Was wurde verändert?
- Was ist Quelle, was ist Ansicht?
- Warum kann eine zweite Ansicht wichtig sein?
- Wie komme ich zurück?
- Was macht NEXAH hier: nicht antworten, sondern Unterschiede lesbar machen.

## Boundaries

- keine neue Source-Graph-Identität oder Relation;
- keine wissenschaftliche Autorität aus einer Human-View-Komposition;
- keine öffentliche Aktivierung aus diesem Plan;
- `M-ROO02` bleibt `READY_NOT_ACTIVE`; Build und Veröffentlichung bleiben
  nicht autorisiert;
- keine stillschweigende Vermischung von NEXAHEDRON, nexah.de, Science Lab,
  Builder Desk und Scarabæus;
- jedes tiefe Fenster behält Quelle, Rolle, Grenze und Return.

## Desk placement

Der vollständige Website- und Leseroutenbericht liegt im **Public Desk**. Der
Build Desk hält nur einen Status-Pointer auf dieses Vorhaben. Umsetzung,
technische Checks und Receipts können später als begrenzte Work Packages in
Build erscheinen; die öffentliche Dramaturgie bleibt hier.

## Authoritative returns

- Mission Control: `00_OVERVIEW/HUMAN_VIEW.md`
- Mission Control: `MISSIONS/M-PUB01_NEXAH_PUBLIC_FIELD.md`
- Mission Control: `MISSIONS/M-ROO02_ONE_FIELD_MANY_CUTS.md`
- A0 Human View: `A0_NEXAH_APERTURE_JOURNEY.html`
- A0 inventory: `A0_TOURS.html`
- archived source draft: `DRAFTS/A0_HUMAN_BOOK_DRAFT.html`
- book catalog: `NEXAH-Experience/src/data/library/books.ts`

## Builder Return · Local navigation orientation · 26 October 2026

**Classification:** `PRESENTATION_ACCESSIBILITY_RETURN / NO_NEW_FINDING`
**Identity:** reuses `BOOK-A0_NEXAH_APERTURE_JOURNEY` and the existing
NEXAHEDRON Human View, Arcade, O·PIUM Club and C Connect routes. No new
Navigator identity, relation, Study, Family or vocabulary term was created.

The local NEXAHEDRON shell now provides two distinct navigation layers:

1. the global Flagship line `Human View / Arcade / Club / To NEXAH`, with the
   existing C Connect orb placed beside the active room and Scarabæus retained
   as the separate workshop return;
2. the route-local Human line `Start / Lesen / Light / Look / Türen / Return`.

The active room is exposed semantically with `aria-current`, repeated in the
frame title and visible descriptor, and marked visually on both sides of the
shell. Human View uses cyan, Arcade gold and Club/C Connect pink. Reduced
Motion removes the pulse while preserving the static active-state contrast.
The surrounding header frame remains unchanged.

The Human route also has a visible stop/return after the three curated doors;
internal Builder language was removed from that public exit. These changes
alter navigation, orientation, presentation and accessible state only. Glow,
colour, placement and wording are not evidence and establish no Human utility.

### Pre-deployment verification

- NEXAHEDRON production build: `PASS`;
- targeted foundation/navigation tests: `11/11 PASS`;
- browser checks: Human View, Arcade and Club resolve to their existing
  sources; active descriptor, active Flagship, moving orb and frame title
  agree;
- Source Graph validator: `PASS` (`329/29` base, `332/32` composed);
- at this checkpoint, no deployment, publication, push or outreach had yet
  been performed; the later release custody return below supersedes only that
  operational status.

### Science and paper boundary check

- A0 Science Desk currentness remains unchanged: the existing Human Journey
  record already classifies the route as a demonstrator with Browser, Mobile
  and Human-Utility acceptance open and explicitly records no new scientific
  finding;
- `32_A0_FINDINGS_AND_PAPER_WORKSPACE_2026-10-11.md`: **not affected**;
- Mathfield navigation, source walk and returns: **not affected**;
- Mission Control visible release currentness: **updated by the later release
  custody return below**;
- `PORTFOLIO_TRUTH.json`: **not affected**, because no scientific state,
  active research priority, source identity or claim state changed.

### Release custody return · 26 October 2026

The Human Owner authorized the bounded NEXAHEDRON update. The implementation
is no longer a local-only working cut:

- feature source: NEXAHEDRON `main` revision
  `a10a88a7694fa8ef9d31acc3841637cb1e0fb827`;
- CI-policy correction: NEXAHEDRON `main` revision
  `0d38155d2f0d8a477dc36cd39b07050df06444fe`;
- GitHub foundation run: `40251344693`, `SUCCESS`;
- Cloudflare Worker: `nexahedron`;
- deployed Worker version:
  `366bee0e-ba7f-4d8e-98fd-601437c1a0a4`;
- public route: <https://nexahedron.com/>.

The public root, `/about`, the canonical A0 journey and the Scarabæus image
were checked on the domain after deployment. Internal A0 Science Desk,
Builder and Contact Bench probes remain unavailable from their denied public
paths. The deployment changes presentation, reader guidance and public route
composition only. It creates no finding, paper state, mathematical result,
Navigator identity, source relation or scientific publication.

Rollback remains the preceding Cloudflare Worker deployment recorded in the
worker history. The quarantined Finder-style duplicate files remain outside
the public bundle and were not deleted.
