# NEXAH Mathematical Foundations and Glossary

Kanonische Fassung seit: 2026-09-17

Letzte kanonische Erweiterung: 2026-09-30

Fassungsstand: `V2_TRANSITION_ARCHITECTURE_REGISTRY`

Dokumenttyp: mathematische Grundordnung und Glossar

Status: `CANONICAL_RESEARCH_GLOSSARY / NO_NEW_THEORY_CLAIM`

Owner: `NEXAH/RESEARCH/FOUNDATION`
Operational effect: `NONE`

Provenienz: Diese gepflegte Research-Fassung wurde aus dem datierten,
hash-gebundenen Mission-Control-Return
`MISSION_CONTROL_ROEDELHEIM_ORIENTATION_RETURN_2026-09-16/11_NEXAH_MATHEMATICAL_FOUNDATIONS_BASELINE.md`
übernommen. Der historische Snapshot bleibt unverändert; spätere begriffliche
Pflege erfolgt ausschließlich hier.

## 1. Zweck und Grenze

Dieses Dokument fixiert zuerst die Mathematik. Es enthält keine Farbenlehre,
Wahrnehmungspsychologie, Kunstgeschichte, Genealogie oder physikalische
Deutung. Diese Gebiete dürfen später an klar definierte mathematische Objekte
angebunden werden, aber nicht deren Definition ersetzen.

Die Leitfrage lautet:

> Welche mathematischen Objekte, Abbildungen und erhaltenen oder verlorenen
> Eigenschaften liegen in einer NEXAH-Darstellung tatsächlich vor?

### 1.1 Registrierungsstatus

Jeder neu aufgenommene Ausdruck muss mindestens einer der folgenden Klassen
zugeordnet werden:

```text
DEFINITION            exakt deklarierter Begriff oder Operator
DERIVED_QUANTITY      aus Definitionen berechnete Größe
DIAGNOSTIC            beschreibende, nicht allein bestätigende Auswertung
EMPIRICAL_RESULT      reproduzierbares Resultat mit gebundenem Datensatz
RESEARCH_HYPOTHESIS   prüfbare, noch nicht bestätigte Verbindung
VISUAL_MNEMONIC       kontrollierte Bild- oder Orientierungsbezeichnung
OPEN_BRIDGE           noch nicht validierter Übergang zwischen Ebenen
```

Eine Bezeichnung darf mehrere Rollen besitzen, sofern jede Rolle separat
ausgewiesen wird. Insbesondere wird eine Visualisierung nicht durch ihre
Aufnahme in dieses Glossar zu einem empirischen Resultat.

## 2. Minimale Grundregel

Keine mathematische Aussage ohne:

```text
Objekt + Definitionsbereich + Abbildung + Vergleichsregel + Gültigkeitsgrenze
```

Insbesondere gilt:

```text
Bezeichnung != mathematisches Objekt
Bildähnlichkeit != Isomorphie
gleicher Wert != gleicher Generator
gleiche Darstellung != gleiche Transformationsgeschichte
sichtbare Schleife != Windungszahl
Rastergröße != topologische Eigenschaft
```

## 3. Grundobjekte

### 3.1 Träger oder Quellraum

Ein Träger `X` ist die deklarierte Menge der zulässigen Zustände oder Objekte.
Beispiele sind eine endliche Punktmenge, ein Zahlenregister, `R^2`, `C`, ein
Graph, eine geordnete Sequenz oder ein Parameterraum.

Ein gebundenes Quellobjekt ist ein bestimmtes `x in X` zusammen mit seiner
Identität, Version, den Parametern und gegebenenfalls dem Zeitpunkt.

### 3.2 Relation

Eine Relation `R` zwischen Mengen `X` und `Y` ist eine Teilmenge

```text
R subseteq X x Y.
```

Sie sagt, welche Paare miteinander verbunden sind. Eine Relation muss weder
eindeutig noch umkehrbar noch kausal sein.

### 3.3 Funktion und Operator

Eine Funktion

```text
F: D subseteq X -> Y
```

weist jedem zulässigen Eingang aus `D` genau einen Ausgang in `Y` zu. Ein
NEXAH-Operator ist eine solche Abbildung nur dann, wenn Ein- und Ausgang,
Parameter, Randfälle und Kompositionsregel erklärt sind.

Ein Pfeil, ein Verb oder eine visuelle Ähnlichkeit ist noch kein Operator.

### 3.4 Darstellung

Eine Darstellung ist ein mathematisches oder rechnerisches Objekt `Y`, das
durch eine deklarierte Abbildung aus einer Quelle entsteht:

```text
y = O(x).
```

Die Darstellung kann die Quelle vollständig, teilweise oder mehrdeutig
abbilden.

### 3.5 Identität und Adresse

Identität beantwortet, welches Objekt vorliegt. Eine Adresse gibt an, wo oder
unter welchem Index es in einer Darstellung gefunden wird. Eine Änderung der
Adresse muss keine Änderung des Objekts sein; identische Werte können aus
verschiedenen Objekten oder Generatoren entstehen.

### 3.6 Relationsobjekt, Meta-Relation und Generationsebene

Eine getypte Relation kann selbst als Objekt einer weiteren, ausdrücklich
deklarierten Relation behandelt werden. Der GEN01-Crosswalk verwendet dafür
lokal:

```text
mathcal G_0 = getypte Quellobjekte
mathcal G_1 = Relationen aus G_0, als getypte Objekte gespeichert
mathcal G_2 = eine Meta-Ebene von Relationen zwischen G_1-Objekten
```

T5 bezeichnet in diesem Crosswalk den Lift `Relation -> Objekt`, T6 die
Bildung einer Relation zwischen solchen Relationsobjekten und T7 den
Darstellungs- und Rückvergleich. Die getestete Rekursion endet bei
`mathcal G_2`; eine weitere Ebene wird nicht stillschweigend angenommen.

Der Wert eines Relationsobjekts ist nicht seine vollständige Geschichte. Für
eine Endpoint-Projektion

```text
pi(h) = result_value
```

können verschiedene getypte Historien dasselbe Bild besitzen. GEN01 zeigte
dies konstruktiv in einem eingefrorenen History-Raum, während vollständige
Records Operand, Operator, Ordnung, Parent und Generation unter den getesteten
Darstellungswechseln exakt erhielten.

`mathcal G_0/mathcal G_1/mathcal G_2` ist damit ein validierter case-lokaler
Crosswalk, keine global kanonische NEXAH-Notation. Er ist insbesondere von
`G2/G3/GR`, `G-01...G-06`, Gridauflösungen und der Dreifachrelation
`G=A intersect B intersect C` zu unterscheiden.

GEN02 prüfte die strukturelle Übertragbarkeit dieses Crosswalks über vier
eingefrorene Relationsfamilien: gerichtete Nachfolge, symmetrische Äquivalenz,
rollengetypte Inzidenz und ternäre Schnittbildung als Holdout. Ein gemeinsamer
Feldvertrag für G0-, G1- und G2-Records blieb ohne Schemaänderung erhalten;
T7 gab die vollständigen Records exakt zurück und T6-Metarelationen waren aus
ihren referenzierten G1-Records reproduzierbar.

Diese Übertragbarkeit betrifft den **Recordvertrag**, nicht eine gemeinsame
Semantik. Jede Familie behielt einen expliziten semantischen Validator. Ein
ungetypter Endpoint, eine bloße Teilnehmermenge oder eine generische
Provenienzhülle ist kein vollständiges Relationsobjekt, wenn Relationstyp,
Rollen, Richtung oder Payload fehlen. Der Befund validiert weder beliebige
Relationsfamilien noch den `n+1`-Binder oder eine Ebene oberhalb von
`mathcal G_2`.

## 4. Raum, Frame und Messung

### 4.1 Anchor

Ein Anchor `A` ist eine persistente Referenzidentität. Er kann einen Ursprung
oder Referenzpunkt festlegen, bestimmt allein aber weder Richtung noch
Händigkeit noch Maßstab.

### 4.2 Frame

Ein Frame ergänzt den Anchor um eine Basis, Richtung, Orientierung und die zur
Messung benötigte Struktur. Im einfachsten euklidischen Fall:

```text
F = (A, e_1, ..., e_n, metric).
```

### 4.3 Koordinaten

Koordinaten sind Zahlen, die ein Objekt relativ zu einem Frame beschreiben.
Sie sind nicht das Objekt selbst. Bei einem Framewechsel können sich die
Koordinaten ändern, obwohl die geometrische Beziehung erhalten bleibt.

### 4.4 Metrik

Eine Metrik `d` legt fest, wie Abstände verglichen werden. Ohne deklarierte
Metrik sind Aussagen wie nah, fern, Zentrum oder kleinster Fehler
unterbestimmt.

Die euklidische Metrik ist ein wichtiger Standardfall, aber nicht automatisch
für Graphen, gekrümmte Räume oder gemischte Datentypen geeignet.

### 4.5 Winkel und Orthogonalität

Winkel und Rechtwinkligkeit benötigen eine geeignete metrische beziehungsweise
innere-Produkt-Struktur. Sie sind keine rein graphischen Eigenschaften.

## 5. Transformationen und Erhaltung

### 5.1 Translation, Rotation und Spiegelung

Im euklidischen Raum erhalten Translationen, Rotationen und Spiegelungen
Abstände und Winkelbeträge. Spiegelungen kehren die Orientierung beziehungsweise
Händigkeit um.

Horizontale, vertikale und diagonale Spiegelungen gehören derselben Klasse
euklidischer Isometrien an, sind aber verschiedene Abbildungen mit
verschiedenen Fixgeraden.

### 5.2 Skalierung

Eine gleichmäßige positive Skalierung erhält Winkel und skaliert Längen. Eine
anisotrope Skalierung kann Winkel und euklidische Abstände verändern.

### 5.3 Affine Abbildungen

Affine Abbildungen erhalten insbesondere Geraden, Kollinearität und
Parallelität. Allgemeine affine Scherungen erhalten nicht notwendig Längen,
Winkel oder Rechtwinkligkeit.

### 5.4 Invariante und Equivarianz

Eine Größe `I` ist unter einer Transformationsklasse `G` invariant, wenn

```text
I(g x) = I(x)  for all admissible g in G.
```

Eine Darstellung ist equivariant, wenn eine Transformation der Quelle einer
deklarierten Transformation ihrer Darstellung entspricht:

```text
O(g x) = rho(g) O(x).
```

Eine Invariante besitzt erst Inhalt, wenn Objekt, Transformationsklasse und
Vergleichsregel feststehen.

## 6. Schnitt, Projektion und Mehrdeutigkeit

### 6.1 Cut

Ein Cut ist eine deklarierte Auswahl, Einschränkung oder partielle Beobachtung.
Er verändert nicht notwendig die Quelle; er bestimmt, welcher Teil in die
Darstellung eingeht.

### 6.2 Projektion

Eine Projektion oder allgemeine Beobachtungsabbildung

```text
P: X -> Y
```

kann verschiedene Quellobjekte auf denselben Ausgang abbilden. Dann ist `P`
nicht injektiv und die Quelle aus `y` allein nicht eindeutig rekonstruierbar.

### 6.3 Faser und Rekonstruktionsmenge

Die zu einer Beobachtung `y` kompatiblen Quellen bilden die Faser

```text
P^(-1)(y) = {x in X : P(x)=y}.
```

In einem endlichen registrierten Modell ist dies die Rekonstruktionsmenge.
Mehrere Ansichten verengen sie durch Schnitt:

```text
Theta_(A,B) = Theta_A intersection Theta_B.
```

Eine kleinere Rekonstruktionsmenge bedeutet mehr Unterscheidungsinformation,
aber nicht automatisch eine besondere physikalische Kopplung der Ansichten.

### 6.4 Verlust, Zusatz und Unbestimmtheit

Für einen Darstellungswechsel werden vier Fälle getrennt:

- erhalten oder invariant;
- verloren;
- durch die Darstellung hinzugefügt;
- unaufgelöst oder nicht entscheidbar.

`UNKNOWN` ist weder null noch falsch.

## 7. Graph, Raster und Einbettung

### 7.1 Graph

Ein Graph bestimmt Knoten und Kanten. Ohne zusätzliche Attribute bestimmt er
keine euklidischen Positionen, Längen oder Winkel.

### 7.2 Einbettung

Eine Einbettung weist Graphknoten Positionen in einem Raum zu. Derselbe Graph
kann verschieden eingebettet werden und dabei dieselbe Adjazenz, aber andere
sichtbare Winkel und Distanzen besitzen.

### 7.3 Raster

Ein Raster ist ein diskreter Adress- und Darstellungsraum. Seine Auflösung,
Parität, Mittelzelle und Randbehandlung beeinflussen die Darstellung.

```text
Rastergröße != Windungszahl
Rastergröße != Primzahlinvariante
Rasterbild != Quelle
```

Ein ungerades `n x n`-Raster besitzt eine eindeutige Mittelzelle. Ein gerades
Raster besitzt stattdessen eine zentrale Naht oder einen zentralen Block.

### 7.4 Relation–Transition Trace Grid

**Relation–Transition Trace Grid**, kurz `RTTG`, ist der kanonische neutrale
Name für das historisch als `Ghostgrid` bezeichnete NEXAH-Konzept. Die
deutsche Arbeitsbezeichnung lautet **Relations-, Übergangs- und Spurengitter**.

Ein RTTG ist kein unsichtbares physikalisches Medium. Es ist eine deklarierte
Familie von Darstellungs- oder Adressräumen zusammen mit Abbildungen zwischen
ihnen und einem Register der dabei erhaltenen, verlorenen, hinzugefügten oder
unaufgelösten Relationen:

```text
RTTG = (
  G_i,
  T_(i->j),
  relation ledger,
  transition ledger,
  trace and residual ledger,
  provenance
).
```

Dabei sind:

- `G_i` die einzelnen Raster-, Ebenen-, Träger- oder Darstellungsräume;
- `T_(i->j)` die deklarierten Schnitte, Projektionen, Quotienten,
  Verfeinerungen, Faltungen oder anderen Ebenenwechsel;
- das Relationsregister die expliziten Korrespondenzen zwischen Elementen oder
  Regionen verschiedener Ebenen;
- das Übergangsregister Quellebene, Zielebene, Operator, Parameter, Reihenfolge
  oder Zeitpunkt und die erzeugte Darstellung jedes Ebenenwechsels;
- das Spurenregister die nach einem Übergang noch sichtbaren oder
  rekonstruierbaren Wirkungen früherer Zustände und Relationen;
- das Residualregister die typisierten Abweichungen, Verluste,
  Mehrdeutigkeiten und offenen Fortsetzungen;
- die Provenienz die Herkunft und Reihenfolge der Konstruktion.

Die sichtbaren Linien eines RTTG können Kanten, Konstruktionslinien,
Urbildbeziehungen oder registrierte Korrespondenzen darstellen. Eine solche
Linie ist keine zusätzliche Zustandsvariable, solange sie nicht durch eine
explizite Regel dazu gemacht wird.

#### Gedächtnis

Das Gedächtnis des RTTG ist die bewahrte Transformationsgeschichte:

```text
Quelle -> Ebene -> Abbildung -> Spur -> Residual -> mögliche Fortsetzung.
```

„Gedächtnis“ bedeutet hier gespeicherte Relation, Adresse, Reihenfolge,
Parameter und Provenienz. Es behauptet weder Bewusstsein noch ein materielles
Gedächtnis.

#### Potential

Das relationale Potential eines RTTG ist zunächst die Menge der unter den
deklarierten Regeln zulässigen nächsten Verbindungen, Ansichten oder
Transformationen. Es ist keine physikalische potentielle Energie. Eine
Energieaussage benötigt zusätzlich eine definierte Größe `E`, Einheiten,
Messverfahren und Erhaltungs- oder Bilanzregel.

#### Beispiel 111×111 -> 11×11

Für Koordinaten `i,j in {0,...,110}` kann ein Ebenenwechsel durch

```text
q(i,j) = (i mod 11, j mod 11)
```

definiert werden. Das `11×11`-Raster ist dann ein Quotienten- oder
Klassifikationsraum des `111×111`-Rasters. Wegen

```text
111 = 10 * 11 + 1
```

besitzt bei dieser Indexierung die Restklasse `0` elf Vertreter, jede andere
Restklasse zehn. Die Urbildgrößen im zweidimensionalen Raster sind daher
`121`, `110` oder `100`. Diese Nichtgleichförmigkeit ist ein exakt
beschreibbarer Ebenen- beziehungsweise Diskretisierungsrest.

#### Verhältnis zu Fasern und Hopf

Für eine Abbildung `T: G_i -> G_j` ist das Urbild `T^(-1)(y)` die Faser einer
Beobachtung `y`. Beim endlichen RTTG kann sie eine diskrete Punktmenge sein. Bei
der klassischen Hopf-Faserung `S^3 -> S^2` ist jede Faser ein Kreis `S^1`.
Beide teilen die allgemeine Viele-zu-eins-Struktur; daraus folgt nicht, dass
ein RTTG selbst eine Hopf-Faserung besitzt. Dafür müssten Gesamt-, Basis- und
Faserraum sowie lokale Bündelstruktur ausdrücklich definiert und geprüft sein.

`Ghostgrid` bleibt als historischer Such- und Provenienzbegriff erhalten, ist
aber keine bevorzugte wissenschaftliche Bezeichnung.

### 7.5 3×3 und 11×11

Ein `3×3`-Raster ist der kleinste hier verwendete quadratische Rasterfall mit
expliziter Mittelzelle und acht Nachbarzellen. Ein `11×11`-Raster bietet eine
feinere Quantisierung, ohne dadurch eine andere Trägerart zu werden.

Der historische V27-`3×3`-Zustandskern ist ein Produkt zweier dreistufiger
Klassifikationen und kein geometrisches Naturgesetz:

```text
state = 3 * level + phase.
```

## 8. Endliche Arithmetik

### 8.1 Restklasse

Für Modul `m` gehören ganze Zahlen `a` und `b` zur selben Restklasse, wenn

```text
a congruent b (mod m).
```

Modulo-Klassen sind zyklische Adressen. Eine Restklasse ist keine räumliche
Windung und keine physikalische Phase, sofern keine zusätzliche Abbildung dies
definiert.

Beispiel:

```text
110 mod 11 = 0
111 mod 11 = 1
112 mod 11 = 2.
```

### 8.2 Chinesischer Restsatz

Der CRT beschreibt, wann kompatible Restklassen bezüglich teilerfremder Moduln
eindeutig zu einer Restklasse im Produktmodul zusammengesetzt werden können.
NEXAH verwendet den CRT als Standardwerkzeug für Adresszerlegung und
Rekonstruktion; er ist keine neue NEXAH-Mathematik.

### 8.3 Primzahl und Primindex

Eine Primzahl ist eine positive ganze Zahl größer als eins mit genau zwei
positiven Teilern. Ein Primindex ist ihre Position in der aufsteigenden
Primzahlfolge. Wert und Index bleiben getrennt:

```text
41 = P_13
97 = P_25
101 = P_26
103 = P_27
107 = P_28
109 = P_29
113 = P_30.
```

Lokale Gap-Muster dürfen beschrieben werden. Ein Zyklus, Flip oder musikalischer
Einsatz ist erst dann ein mathematischer Operator, wenn Auswahl- und
Fortsetzungsregel definiert sind.

### 8.4 Zahl, Ziffernfolge und Glyph

Der Zahlenwert, seine Primzahlposition, seine Restklasse, seine Dezimalschreibweise
und seine visuelle Form sind verschiedene Objekte. Konkatenation ist weder
Addition noch Multiplikation. Ein Palindrom ist zunächst eine Eigenschaft einer
gewählten Schreibweise und Basis.

### 8.5 Kubische Randpaare und Shadow Cube

Für eine ganze Zahl `n` wird das kubische Randtripel definiert als

```text
C_n   = n^3
S_n^- = n^3 - 1
S_n^+ = n^3 + 1.
```

Die beiden Randzweige sind durch die bekannten Faktorisierungen gebunden:

```text
n^3 - 1 = (n-1)(n^2+n+1)
n^3 + 1 = (n+1)(n^2-n+1).
```

`cube.boundary_pair(n) = (S_n^-, S_n^+)` bezeichnet dieses typisierte
Janus-Paar um den zentralen Würfel `C_n`. `Shadow Cube` darf als kontrolliertes
Mnemonic für dieses deklarierte Randpaar oder für ein ausdrücklich benanntes
modulares Bild verwendet werden. Der Ausdruck bezeichnet keine neue Zahlenart,
keinen zweiten physischen Würfel und kein verborgenes Feld.

Für `n=12` gilt exakt:

```text
12^3 - 1^3 = 1727 = 11 * 157
12^3         = 1728
12^3 + 1^3 = 1729 = 13 * 133 = 7 * 13 * 19
12^3 + 1^3 = 9^3 + 10^3.
```

Die Faktoren `11=12-1` und `13=12+1` folgen zwingend aus den beiden
Kubikfaktorisierungen und sind daher keine empirische Überraschung. Weiter ist
`133=7*19=(13-6)(13+6)`. Die zugehörigen modularen Randbilder lauten:

```text
12^3 congruent -1 (mod 7, 13, 19)
12^3 congruent +1 (mod 11, 157).
```

In der kubischen Identität wird `1^3` geschrieben. Zwar gilt numerisch
`1^1=1^3=1`, aber `1^1` bewahrt den Typ der Summe beziehungsweise Differenz
zweier Kuben nicht. Die bekannte Taxicab-Darstellung von 1729 und das kubische
Randpaar sind exakte Standardmathematik. Sie begründen ohne eine zusätzliche,
vorab deklarierte Abbildung weder eine physikalische Kopplung noch eine
Bevorzugung von 11 in kontinuierlichen Messdaten.

### 8.6 Shadow-Cube-Lift und Informationsgrenze

Für einen Restzustand `r in Z/qZ` kann ein modularer Shadow-Cube-Lift als

```text
chi_q(r) = (r^3-1, r^3, r^3+1) mod q
```

definiert werden. Dies ist eine deterministische Merkmalsabbildung. Sie kann
Nachbarschaften, Symmetrien, Kompression oder einen modulübergreifenden
Vergleich anders darstellen, enthält innerhalb eines festen Moduls aber keine
Information, die nicht bereits in `r` enthalten war:

```text
chi_q(r) is a function of r
=> no within-modulus information gain over the full residue state.
```

Ein beobachteter Vorteil des Lifts kann daher ein Vorteil der Repräsentation,
Regularisierung oder Übertragung sein. Er ist nicht ohne Weiteres ein neuer
arithmetischer Informationskanal. Ein Bezug zwischen einem kubischen
Randfaktor und einem empirisch auffälligen Modul muss vor der Auswertung
deklariert werden; eine nachträgliche Zuordnung ist explorativ.

### 8.7 Prime-indexed prime und Index-Re-entry

`P_n` bezeichnet die `n`-te Primzahl. Da `P_n` für jedes zulässige `n` prim
ist, bezeichnet **prime-indexed prime** keinen neuen Primzahltyp, sondern die
zusätzliche Indexbedingung

```text
n is prime and P_n is the n-th prime.
```

Der historische Ausdruck `prime-prime` wird nur in diesem typisierten Sinn
geführt. Die Eigenschaft hängt vollständig von der Primalität des Index `n`
ab.

Ein **Prime-Index-Re-entry** in einem lokalen Dreierfenster bezeichnet

```text
n-1 prime,
n composite,
n+1 prime.
```

Der mittlere Index ist dann die zusammengesetzte Unterbrechung zwischen zwei
prime-indexed primes. Dies ist eine Indexraum-Eigenschaft und keine Aussage
über die Primwertlücken `P_n-P_(n-1)` oder `P_(n+1)-P_n`.

Numerische Gleichheit zwischen einem Index und einem Primwert, etwa
`I_7=P_4=7`, bewahrt nicht die Generatoridentität. In Formeln muss deshalb
kenntlich bleiben, ob eine Zahl als Index, Primwert oder Restadresse verwendet
wird.

## 9. Ordnung, Bahn und Dynamik

### 9.1 Sequenz und Pfad

Eine Sequenz besitzt eine Reihenfolge. Zwei Pfade mit denselben Zuständen, aber
anderer Reihenfolge sind nicht derselbe Pfad.

### 9.2 Iteration und Orbit

Für eine Abbildung `f: X -> X` ist der Orbit von `x_0` die Folge

```text
x_0, f(x_0), f^2(x_0), ...
```

Eine Projektion des Orbits ist nicht der vollständige Zustandsraum.

### 9.3 Periode und Rückkehr

Eine exakte Periode `k` erfüllt `f^k(x)=x`. Eine Rückkehr in einer Darstellung
kann dagegen auftreten, obwohl Quelle, Geschichte oder nicht beobachtete
Koordinaten nicht zurückgekehrt sind.

```text
return of representation != reset of complete state
```

### 9.4 Windungszahl

Eine Windungszahl benötigt eine geschlossene orientierte Kurve und einen
Referenzpunkt außerhalb der Kurve. Sie ist eine topologische Größe. Ein
sichtbarer Loop, ein Q11-Raster oder elf Phasenklassen bestimmen allein keine
Windungszahl.

### 9.5 Mandelbrot und Julia

Für

```text
f_c(z)=z^2+c
```

ist `c` der Parameter und `z` der dynamische Zustand. Ein endliches
Escape-Time-Bild ist eine numerische Darstellung unter Fenster, Raster,
Iterationsgrenze und Escape-Radius. Es ist nicht die exakte Julia-Menge.

Die unterstützte NEXAH-Kette lautet:

```text
Parameter -> Dynamik -> endliches Feld -> Beobachtung -> Rekonstruktionsmenge.
```

### 9.6 Übergangszählung und Übergangsmatrix

Für eine beobachtete Zustandsfolge `x_0,...,x_T` auf einer endlichen Menge `X`
ist die Übergangszählung

```text
N_ij = #{t : x_t=i and x_(t+1)=j}.
```

Eine geglättete zeilenstochastische Übergangsmatrix kann durch

```text
P_ij = (N_ij + alpha_ij) / sum_k (N_ik + alpha_ik)
```

definiert werden. Datenausschnitt, Zustandsalphabet, Glättung, Randbehandlung
und Zeitrichtung gehören zur Definition. Eine Übergangsmatrix beschreibt
bedingte Häufigkeiten erster Ordnung; sie ist weder automatisch kausal noch
eine vollständige Dynamik.

### 9.7 Stationäre Verteilung, Verkehr und gerichteter Strom

Eine stationäre Verteilung `pi` erfüllt

```text
pi P = pi,  sum_i pi_i = 1.
```

Der stationäre gerichtete Kantenstrom wird definiert als

```text
J_ij = pi_i P_ij - pi_j P_ji,
```

und ist antisymmetrisch. Ein symmetrischer Verkehrsoperator kann beispielsweise
aus den Summen der beiden stationären Richtungsflüsse gebildet werden. Verkehr
und Strom sind verschiedene Objekte: hoher Verkehr kann bei verschwindendem
Netto-Strom auftreten. `Drift`, `transport` oder `circulation` dürfen nur auf
eine erklärte Strom-, Inkrement- oder Bilanzgröße bezogen werden.

### 9.8 Spektrum, Eigenraum und Spektralsubraum

Das Spektrum eines Operators ist die Multimenge seiner Eigenwerte. Ein
Eigenvektor ist bei einfachen Eigenwerten mindestens bis auf Skalierung und
Vorzeichen unbestimmt; bei mehrfachen oder nahen Eigenwerten kann eine ganze
Basis innerhalb eines invarianten Subraums rotieren. Daher gilt:

```text
stable spectrum != stable eigenvector coordinates
stable subspace != stable hard partition
```

Ein Vergleich spektraler Darstellungen muss die relevante Gauge-Freiheit
berücksichtigen, beispielsweise durch Projektoren, kanonische Winkel oder eine
orthogonale Procrustes-Ausrichtung.

### 9.9 Gauge und gauge-invarianter Vergleich

`Gauge` bezeichnet hier eine Darstellungsfreiheit, durch die verschiedene
Koordinatenbasen dasselbe mathematische Objekt repräsentieren. Für zwei
orthonormale Basen `U` und `V` desselben `k`-dimensionalen Subraums kann

```text
U and VQ,  Q in O(k),
```

dieselbe Unterraumstruktur beschreiben. Aussagen über Stabilität sollen daher
nach Möglichkeit auf Projektoren, Unterraumwinkel oder nach deklarierter
Ausrichtung aufbauen und nicht auf ungeklärten Einzelkoordinaten.

### 9.10 Harte Sheets und Soft Memberships

Ein **Sheet** ist im gegenwärtigen NEXAH-Forschungsgebrauch eine deklarierte
Aggregation von Zuständen, die aus einer Ähnlichkeits-, Operator- oder
Clusteringregel gewonnen wird. Eine harte Sheet-Abbildung hat die Form

```text
s: X -> {1,...,K}.
```

Eine Soft Membership ordnet dagegen Gewichte zu:

```text
w: X -> Delta^(K-1),  sum_k w_k(x)=1.
```

Sheets sind abgeleitete Darstellungen, keine vorausgesetzten materiellen
Schichten. Ihre Anzahl, Identifizierbarkeit, zeitliche Stabilität und
Label-Invarianz müssen separat geprüft werden. Eine stabile Matrix oder ein
stabiler Subraum erzwingt keine stabile harte Sheet-Partition.

### 9.11 Regime und Basin

Ein Regime ist eine unter einer festgelegten Regel zusammengefasste Menge von
Zuständen oder Sheets. Ein Basin im dynamischen Sinn benötigt zusätzlich eine
Dynamik und ein Attraktionsziel. Deshalb darf eine farbige Region einer
Partition nur dann `basin` heißen, wenn ihre Attraktionseigenschaft definiert
und geprüft ist; andernfalls ist `regime` oder `region` der neutrale Begriff.

### 9.12 Phase als projektionsinduzierte Koordinate

Für eine zweidimensionale Beobachtung `(x(t),y(t))` relativ zu einem erklärten
Ursprung kann eine Kreisphase definiert werden als

```text
theta(t) = atan2(y(t), x(t)) in (-pi,pi].
```

Für einen Restzustand `r in Z/qZ` ist die rohe modulare Kreisadresse

```text
theta_raw(r) = 2*pi*r/q  mod 2*pi.
```

Beide Größen sind Koordinaten einer gewählten Abbildung. Sie sind nicht ohne
zusätzliche Messdefinition physische Observablen und nicht automatisch
systemübergreifend äquivalent. Ursprung, Projektion, Orientierung, Skalierung
und Branch-Cut gehören zur Spezifikation.

### 9.13 Spektrale Phase

Seien `u_1,u_2` zwei Koordinaten eines deklarierten zweidimensionalen
Operatorsubspaceraums. Dann kann eine spektrale Phase definiert werden durch

```text
z(x) = u_1(x) + i*u_2(x),
theta_spec(x) = arg z(x).
```

Da die Basis `(u_1,u_2)` innerhalb ihres Subraums rotieren oder gespiegelt
werden kann, ist `theta_spec` erst nach einer Gauge-Regel zwischen Fits
vergleichbar. Die Stabilität des Subraums, die Stabilität der ausgerichteten
Phase und die Stabilität daraus abgeleiteter Events sind drei getrennte
Prüfgegenstände.

### 9.14 Zirkuläres Inkrement, Unwrapping, Drift und Winding

Das branch-invariante zirkuläre Phaseninkrement ist

```text
delta_theta_t = Arg(exp(i*(theta_(t+1)-theta_t))).
```

Ein Unwrapping erzeugt daraus unter einer erklärten Fortsetzungsregel eine
reellwertige Sequenz `theta_unwrapped(t)`. Es ist nicht eindeutig, wenn Sprünge
oder Abtastlücken die verwendete Regel verletzen. Mittlere Drift und endliche
Winding-Rate können beispielsweise definiert werden als

```text
mu_delta = mean(delta_theta_t),
w_T = (theta_unwrapped(T)-theta_unwrapped(0)) / (2*pi*T).
```

Diese Größen sind Diagnosen einer orientierten Phase. Eine topologische
Windungszahl im strengen Sinn setzt die in Abschnitt 9.4 genannten Bedingungen
voraus. Nichtverschwindende Drift allein beweist weder Topologie noch einen
physischen Transportmechanismus.

### 9.15 Gate, Plateau, Change Point und Transition Event

Ein Gate ist eine vorab definierte Teilmenge oder Score-Region, in der ein
Transitionskriterium erfüllt wird. Allgemein:

```text
G_tau = {x : g(x) >= tau}
```

mit Score `g`, Schwelle `tau` und festgelegter Schwellenauswahl. Ein Plateau ist
ein Zeitintervall, in dem eine erklärte Änderungsgröße unter einer festen
Toleranz bleibt. Ein Change Point bezeichnet eine durch ein deklariertes
statistisches Verfahren erkannte Verteilungs- oder Parameteränderung.

Ein binäres Transition Event beziehungsweise historisch benanntes `IOTA` ist
eine abgeleitete Indikatorvariable. Wird seine Schwelle als Perzentil derselben
auszuwertenden Stichprobe gewählt, ist die Ereignisrate teilweise konstruiert.
Eine bestätigende Analyse benötigt eine auf Trainingsdaten eingefrorene Regel
und eine unabhängige Kalibrations- oder Testmenge.

### 9.16 Ereignisalphabet und Synchronisation

Ein Ereignisalphabet ist eine endliche, reproduzierbar anwendbare Menge von
Eventtypen. Cross-Modulus- oder Cross-System-Synchronisation benötigt zuerst
stabile Einzelalphabete oder eine direkt definierte kontinuierliche
Kopplungsstatistik. Instabile Clusterlabels dürfen nicht nachträglich als
synchrone Ereignisse interpretiert werden.

Für Phasen `theta_j(t)` ist der Kuramoto-Ordnungsparameter

```text
r(t) * exp(i*psi(t)) = (1/N) * sum_j exp(i*theta_j(t)),
0 <= r(t) <= 1.
```

Er misst momentane Phasenkohärenz der deklarierten Oszillatorpopulation. Ein
hohes `r(t)` beweist keine gemeinsame Ursache und überträgt sich nicht ohne
eine explizite Brückenabbildung auf Primrestfolgen oder chaotische Attraktoren.

### 9.17 Topologie aus Konnektivität: Aussagegrenze

Ein Graph besitzt kombinatorische Konnektivität. Eine Ring-, Torus- oder
Möbiusdarstellung kann dagegen bereits durch das gewählte Layout oder die
Einbettung vorgegeben sein. Eine Aussage über emergente Topologie benötigt ein
topologisches Objekt und eine layoutunabhängige Invariante, etwa Homologie,
Persistenz, Spektralfolgen mit bewiesener Zuordnung oder einen expliziten
Quotientenraum.

```text
circular layout != recovered circle topology
phase embedding != emergent torus
stable spectrum != identified topology
```

Die Kette `connectivity -> topology` ist daher eine Forschungshypothese, bis
die entsprechende Invariante samt Nullvergleich spezifiziert und bestanden
ist.

### 9.18 Nullmodell, Surrogat und eingeschränkter Nullraum

Ein Nullmodell beschreibt, welche Struktur unter einer Gegenhypothese erhalten
bleibt. Ein Surrogat ist eine daraus erzeugte Vergleichssequenz oder ein
Vergleichsoperator. Für Übergangsdaten sind unter anderem getrennt zu prüfen:

- Zustandshäufigkeit erhaltende Permutationen;
- Markov-Replays mit geschätztem `P`;
- Gap- oder Kovariaten-konditionierte Surrogate;
- Zeitumkehr zur Prüfung von Richtungseffekten;
- Label-Permutationen zur Prüfung der Einbettungsabhängigkeit.

Ein beobachteter Effekt besitzt nur Inhalt relativ zu der Struktur, die das
gewählte Nullmodell bereits bewahrt. Mehrere Nullfamilien beantworten
verschiedene Fragen und dürfen nicht als austauschbar behandelt werden.

### 9.19 Split-Half-Stabilität, Replay und Blindbereich

Split-Half-Stabilität vergleicht unabhängig geschätzte Objekte auf zwei
deklarierten Entwicklungsteilmengen. Ein Replay wiederholt die vollständige
Pipeline mit gebundenen Daten, Parametern, Seeds und Code. Ein identischer
Resultathash bestätigt deterministische Reproduzierbarkeit des berechneten
Ergebnisses, nicht dessen wissenschaftliche Wahrheit.

Ein Blindbereich ist ein vor der Modell- und Schwellenwahl zurückgehaltener
Datenabschnitt. Er bleibt blind, solange keine confirmatorische Regel
eingefroren ist. Ein Fail-Closed-Gate bedeutet, dass ein abhängiger Test bei
fehlender Zulassung nicht ausgeführt und kein ersatzweiser p-Wert erzeugt wird.

### 9.20 Prädiktiver Mehrwert

Prädiktiver Mehrwert ist eine held-out Verbesserung gegenüber einem vorab
festgelegten Basismodell unter derselben Bewertungsregel, beispielsweise
Log-Loss, Brier-Score oder proper scoring rule. Eine deterministische
Transformation bereits enthaltener Prädiktoren kann Regularisierung oder
Kompression verbessern, liefert aber nicht automatisch zusätzliche
Information. Sehr kleine Verbesserungen aus instabilen, nachträglich
selektierten Features gelten als diagnostisch, nicht als bestätigende Evidenz.

### 9.21 Unified Transition Architecture

`NEXAH Unified Transition Architecture` bezeichnet derzeit das folgende
typisierte Forschungsprogramm:

```text
source sequence
  -> transition operator
  -> spectrum / current / invariant subspace
  -> aligned phase coordinate
  -> phase increments / drift / winding diagnostics
  -> frozen gates or continuous coupling statistics
  -> connectivity analysis
  -> independently tested topology
  -> separately specified synchronization model.
```

Die Pfeile bezeichnen Arbeitsbrücken, keine bereits bewiesene universelle
Kausalkette. Insbesondere sind

```text
transitions -> universal phase,
phase -> physical transport,
connectivity -> topology,
topology -> synchronization
```

gegenwärtig `OPEN_BRIDGE / RESEARCH_HYPOTHESIS`, sofern sie nicht in einem
konkreten gebundenen Experiment separat operationalisiert werden.

### 9.22 Zyklus, Rekurrenz und Cycle Core

Ein gerichteter Zyklus in einem Graphen ist eine geschlossene Folge gerichteter
Kanten. Rekurrenz bezeichnet die Rückkehr eines Prozesses in einen Zustand
oder eine deklarierte Zustandsmenge; sie ist nicht identisch mit einem
einzelnen Graphzyklus.

`Cycle Core` bezeichnet in NEXAH eine abgeleitete Teilstruktur, die nach einer
erklärten Regel besonders viel zyklischen Verkehr oder rekurrente
Konnektivität trägt. Zulässige Regeln sind beispielsweise ein Schwellenwert
auf Zyklusgewichten, eine stark zusammenhängende Komponente oder eine
Optimierung in einem Zyklusraum. Ohne eine solche Regel ist der Cycle Core ein
`VISUAL_MNEMONIC`, kein eindeutiges mathematisches Objekt.

Eine Zerlegung

```text
flow = cycle component + residual or drift component
```

benötigt die Definition des Flussraums, einer inneren Produktstruktur und der
Projektoren oder Optimierungsregel. Eine visuell plausible Ringkomponente
allein beweist keine eindeutige Hodge- oder Zykluszerlegung.

### 9.23 Empirische Dichte, Feld und Flow

Eine empirische Dichte ist eine aus Stichproben geschätzte Verteilung und hängt
von Kernel, Bandbreite, Raster und Normierung ab. Ein Vektorfeld ist eine
Abbildung

```text
F: X -> T(X)
```

oder im euklidischen Fall `F: X -> R^d`. Ein kontinuierlicher Flow `Phi_t`
erfüllt eine Evolutionsregel, zum Beispiel

```text
d x(t)/dt = F(x(t)).
```

Eine geglättete Pfeildarstellung diskreter Übergänge ist zunächst ein
eingebettetes Übergangsfeld. Sie wird nicht allein durch Glättung zum
kontinuierlichen dynamischen Flow. Übergangsstrom, empirische Dichte,
Vektorfeld und Trajektorienflow sind deshalb getrennte Typen.

### 9.24 Coherence, Residence und Gate Score

`Coherence` ist kein skalenfreier Universalbegriff. Sie muss als konkrete
Ähnlichkeits-, Varianz-, Spektral- oder Phasengröße definiert werden. Eine
Residence-Größe misst die innerhalb einer Region verbrachte Zeit oder deren
normalisierten Anteil unter einer erklärten Segmentierung.

Ein zusammengesetzter Gate Score, etwa

```text
G(x) = (1-rho(x)) * (1-C(x)) * (1-R(x)),
```

ist nur definiert, wenn Dichte `rho`, Coherence `C`, Residence `R`, ihre
Normierung und ihre Gültigkeitsbereiche feststehen. Die Multiplikation dieser
Terme ist eine Modellentscheidung und kein allgemeiner mathematischer Satz.
`Low density`, `low coherence` und `low residence` sind unterscheidbare
Hypothesen über Übergangszonen.

### 9.25 Phase Mismatch, Activation und IOTA-Score

Ein Phase Mismatch ist eine erklärte Distanz zwischen einer beobachteten und
einer Referenzphase oder zwischen ihren Geschwindigkeiten. Für Kreisphasen ist
eine typische lokale Distanz

```text
M(theta,phi) = |Arg(exp(i*(theta-phi)))|.
```

Alternativ kann Mismatch auf geglätteten Phasengeschwindigkeiten beruhen; diese
Definition ist ein anderes Objekt. Filter, Fensterbreite und Randbehandlung
gehören zur Spezifikation.

Eine Activation ist eine Funktion, die Diagnosen in einen kontinuierlichen
Score oder ein binäres Event überführt. `IOTA` darf als historischer Name einer
solchen Transition-Activation geführt werden, besitzt aber keine einheitliche
Definition über Experimente hinweg. Jede Verwendung muss ihre konkrete Formel
und eingefrorene Schwelle angeben.

### 9.26 Manifold, Off-Manifold und strukturbewusste Kontrolle

Eine Mannigfaltigkeit benötigt eine topologische und gegebenenfalls glatte
Struktur; eine gezeichnete Kurve oder Punktwolke ist nicht automatisch eine
identifizierte Mannigfaltigkeit. `Off-manifold` bezeichnet eine Abweichung nur
relativ zu einer erklärten Referenzmenge und Metrik, beispielsweise

```text
d_M(x) = inf_{y in M} d(x,y).
```

Eine Kontrollpolitik wählt Eingriffe in Abhängigkeit von Zustand,
Beobachtung oder Schätzung. `Phase-aware` oder `structure-aware control`
bezeichnet eine Politik, die entsprechende registrierte Features verwendet.
Ein gezeichneter Zielpfad ist noch kein Kontrollnachweis. Erforderlich sind
Systemdynamik, zulässige Eingriffe, Kostenfunktion, Baselines, Störungen und
held-out Erfolgsmaße.

### 9.27 Cross-System-Brücke

Diskrete Restfolgen, kontinuierliche chaotische Systeme und gekoppelte
Oszillatoren besitzen unterschiedliche Träger und Dynamiken. Dass in allen
drei Klassen eine Kreisphase konstruiert werden kann, liefert eine gemeinsame
Vergleichssprache, aber noch keine Isomorphie oder gemeinsame Ursache.

Eine belastbare Cross-System-Brücke muss mindestens angeben:

```text
source spaces
observation maps
phase gauges
time parametrization
dimensionless comparison statistic
null family
domain of claimed transfer.
```

Bis dahin bedeutet `unified` eine vereinheitlichte Analysesprache und ein
Forschungsprogramm, nicht eine bewiesene universelle Dynamik.

## 10. QRT als endlicher Demonstrator

Im geborgenen QRT-Demonstrator ist ein siebenstelliger Carrier definiert:

```text
X = [A B C D E F X]
  -> Q: deklarierter Cut
  -> T: Frame- oder Prefix-Flip
  -> R: inverse Ausrichtung und Adressabgleich
  -> Vergleich von X' mit X.
```

Dies ist ein endlicher Transformations- und Rückkehrdemonstrator. Es ist kein
Ersatz für den Chinesischen Restsatz und kein universeller Operator.

Der erhaltene Kernsatz lautet:

```text
SAME_OUTPUT != SAME_GENERATOR
NUMERICAL_CLOSURE != INFORMATIONAL_CLOSURE
```

## 11. Empirisches Ergebnisregister: PMR01/PMR01A/PMR01B/PMR01C

Die PMR-Piloten vom 2026-09-30 werden mit folgender Aussagegrenze registriert:

```text
PMR01:
  hard residue sheets              NOT STABLE PANEL-WIDE
  dependent synchronization test   NOT RUN / FAIL-CLOSED

PMR01A:
  global transition spectra        STRONGLY SPLIT-HALF STABLE
  normalized directional current   STRONGLY SPLIT-HALF STABLE
  low-dimensional subspaces        SUPPORTED FOR A SUBSET
  thresholded soft events           STABLE ONLY FOR q=17,29
  dependent synchronization test   NOT RUN / FAIL-CLOSED

PMR01B:
  gauge-aligned phase stability    SUPPORTED FOR 6 OF 10 MODULI
  all constrained nulls            PASSED BY 4 OF 10 MODULI
  full intersection                q=17,41 ONLY; 5 REQUIRED
  F3-to-F4 panel bridge             NOT ESTABLISHED / FAIL-CLOSED
  topology and synchronization     NOT RUN

PMR01C:
  nominal held-out log-loss gain   POSITIVE FOR 10 OF 10 MODULI
  positive 99% bootstrap lower     10 OF 10 MODULI
  spectral phase-label specificity q=13,17 ONLY; 5 REQUIRED
  panel incremental utility        NOT ESTABLISHED / FAIL-CLOSED
  blind, topology, synchronization NOT RUN
```

Damit ist als Entwicklungsergebnis zulässig:

> Das gegenwärtig stabilere PMR-Objekt liegt näher am Übergangsoperator,
> Spektrum, Strom oder Subraum als an einer harten Sheet-Partition oder einem
> panelweit stabilen binären Ereignisalphabet.

Nicht zulässig sind daraus Aussagen über Primzahlresonanz, physikalische
Mechanismen, universelle Phase, Cross-Modulus-Synchronisation oder emergente
Topologie. Die in einzelnen Piloten zugelassenen Moduli, darunter `17,29` in
PMR01A, `17,41` in PMR01B und `13,17` in PMR01C, sind diagnostische
Entwicklungsergebnisse und keine nachträglich freigegebenen confirmatorischen
Ziele. Der PMR01C-Gewinn ist zudem als Repräsentations- oder
Regularisierungseffekt begrenzt, weil beliebig permutierte Phasenlabels den
Gewinn panelweit reproduzierten oder übertrafen.

### 11.1 PIR01 Prime-Index-Re-entry-Census

PIR01 registriert eine getrennte F2-Arithmetikbeobachtung. Im exakt
enumerierten Register der ersten `1,000,000` Primindizes gilt:

```text
P_n = 2n+1                                      at n={5,6}
P_n = 2n+1 plus prime-index re-entry            at n={6}
P_(2n+1) = n(n+1)-1                             at n={6}
P_(3n) = P_(n+2)+n(n+1)                         at n={2,3,5,6}
complete frozen conjunction                     at n={6}
```

Für `n=6` ergibt sich damit exakt:

```text
P_6  = 13 = 6+7,
P_13 = 41 = 6*7-1,
P_18 = 61 = P_8+6*7 = 19+42.
```

Diese endliche Eindeutigkeit gilt im deklarierten Register. Die Regeln wurden
nach Beobachtung des Falls gebildet; deshalb folgt daraus weder ein p-Wert noch
eine globale Eindeutigkeit, ein neuer Primzahlsatz oder eine Erklärung der
PMR-Zulassungen.

## 12. Residual und Rückvergleich

Für Quelle `x`, Beobachtung `y=O(x)` und Rekonstruktion `x_hat=R(y)` benötigt
ein numerischer Rest eine deklarierte Metrik:

```text
r = d(x, x_hat).
```

Daneben kann ein struktureller Rest bestehen: verlorene Ordnung, unbekannte
Generatoridentität, fehlende Region oder nicht rekonstruierbare Provenienz.

Ein Rest ist daher immer typisiert:

```text
numerisch | strukturell | außerhalb der Unterstützung | unaufgelöst
```

Er ist nicht automatisch Messfehler, Substanz oder neue Physik.

## 13. Mathematischer NEXAH-Kern

Die derzeit belastbare Architektur lautet:

```text
TRÄGER / QUELLE
  -> RELATION / CONSTRAINT
  -> FRAME / ADRESSE
  -> TRANSFORMATION ODER PROJEKTION
  -> BEOBACHTUNG
  -> FASER / MEHRDEUTIGKEIT
  -> ZWEITE ANSICHT / BINDUNG
  -> REKONSTRUKTION ODER ENTHALTUNG
  -> REST / PROVENIENZ / RÜCKVERGLEICH
```

Diese Architektur verbindet bekannte Mathematik. Ihre derzeitige
NEXAH-spezifische Leistung ist die typisierte Komposition, nicht ein neuer
allgemeiner Satz.

## 14. Was als exakt gilt

Zum bestehenden exakten Bestand gehören unter anderem:

- standardmäßige euklidische Transformationsinvarianten;
- endliche Identifizierbarkeits- und Projektionskollisionen;
- exakte Restklassen- und CRT-Berechnungen;
- exakte kubische Randpaare `n^3 plus/minus 1` und ihre Standardfaktorisierungen;
- deklarierte endliche QRT-Cut/Flip/Return-Abläufe;
- konkrete modulare Orbit- und Periodenzerlegungen;
- bekannte gcd-Identitäten für `10^n-1` und die parity-gesteuerte `+1`-Variante;
- reproduzierte endliche Julia-Escape-Arrays in einem gebundenen Fall;
- exakte, lokal definierte Graph-, Raster- und Adressabbildungen.
- deklarierte endliche Übergangszählungen und zeilenstochastische Operatoren;
- algebraisch definierte stationäre Ströme und Gauge-invariante
  Unterraumvergleiche;
- reproduzierbare PMR01/PMR01A-Pipelineausführungen mit identischen
  Resultathashes.

Diese Resultate sind gültig, auch wenn die zugrunde liegenden allgemeinen
Sätze bekannt sind.

## 15. Was offen bleibt

Noch nicht vorhanden sind:

- ein neuer allgemeiner NEXAH-Satz;
- eine universelle Geometrie aller historischen Darstellungen;
- eine bewiesene gemeinsame Struktur hinter ähnlichen Bildern verschiedener
  Fachgebiete;
- ein vollständig spezifizierter allgemeiner Kompositionskalkül;
- ein nichttrivialer Vorteil des Mehransichten-Binders gegenüber gewöhnlicher
  zusätzlicher Information;
- ein allgemeiner stabiler Aggregator außerhalb des euklidischen gewichteten
  Mittels;
- ein bewiesener Zusammenhang zwischen Primzahlmustern, Musiknotation und
  physikalischer Dynamik.
- eine projektionsunabhängige universelle Phase über diskrete, kontinuierliche
  und gekoppelte Systeme;
- ein panelweit stabiles PMR-Sheet- oder Transition-Event-Alphabet;
- ein confirmatorischer Nachweis von Cross-Modulus-Synchronisation;
- eine layoutunabhängig rekonstruierte Torus-, Möbius- oder andere globale
  Topologie aus den PMR-Übergangsdaten;
- ein empirischer Informationsgewinn des Shadow-Cube-Lifts über den
  vollständigen Restzustand innerhalb eines festen Moduls.

## 16. Reihenfolge für das Grundlagenwerk

Die mathematische Schule wird in dieser Reihenfolge aufgebaut:

1. Menge, Element, Identität und Typ;
2. Relation, Funktion und partieller Operator;
3. Punkt, Linie, Winkel, Dreieck und euklidischer Raum;
4. Anchor, Frame, Koordinate und Metrik;
5. Transformation, Gruppe, Invariante und Equivarianz;
6. Cut, Projektion, Faser und Rekonstruktion;
7. Graph, Raster, Einbettung und Auflösung;
8. Zahl, Schreibweise, Restklasse, Primzahl und CRT;
9. Sequenz, Pfad, Iteration, Orbit und Windungszahl;
10. Übergangsoperator, stationärer Verkehr und gerichteter Strom;
11. Spektrum, Unterraum, Gauge und Stabilitätsvergleich;
12. Phase, zirkuläres Inkrement, Drift und Winding-Diagnostik;
13. Sheets, Regime, Gates, Events und Ereignisalphabet;
14. Nullmodell, Replay, Blindbereich und prädiktiver Vergleich;
15. Konnektivität, Topologie und Synchronisation;
16. Residual, Rückkehr, Provenienz und Vergleich;
17. erst danach: Farbe, Licht, Wahrnehmung und historische Genealogie.

## 17. Parkgrenze

Die folgenden Themen sind wichtig, gehören aber nicht in diese erste
mathematische Fixierung:

- Sehen als aktiver und interaktiver Prozess;
- Licht, Nebel, Schatten und atmosphärische Streuung;
- Farbwahrnehmung und Mustererkennung;
- Leonardo, Goethe, Leibniz oder die Frankfurter Schule;
- Kunst-, Wissenschafts- und Ideengeschichte;
- die alltagssprachliche Gleichsetzung von Sichtbarkeit und Wahrheit.

Sie werden später als eigene Beobachtungs-, Wahrnehmungs- oder
Genealogieschichten an die mathematischen Definitionen angebunden. Sie werden
nicht verworfen und nicht vorzeitig vermischt.

## 18. Provenienz der V2-Erweiterung

Die Definitionen und Aussagegrenzen der Erweiterung vom 2026-09-30 wurden
gegen folgende gebundene Quellen geprüft:

```text
RESEARCH/FINDINGS/TRANSITION_PHASE_DYNAMICS/phase_definition.md
RESEARCH/FINDINGS/TRANSITION_PHASE_DYNAMICS/PHASE_UNIFICATION_SUMMARY.md

NEXAH_PMR01_CROSS_MODULUS_STRUCTURAL_TRANSITION_PREDICTION_2026-09-30
scientific result hash:
d6571fd06fbf0f85f282b89f5c74e65abdb30dba0844eddf6b9b9fe08008c30f

NEXAH_PMR01A_CYCLE_SPECTRUM_SOFT_MEMBERSHIP_STABILITY_2026-09-30
scientific result hash:
2d3cf88de2986aad19de85b201359a58a5992b3b4deb079f2a6df88c35c84ea8

NEXAH_PMR01B_GAUGE_INVARIANT_SPECTRAL_PHASE_2026-09-30
scientific result hash:
f9ea79476ea51b6b9f67ba0c1b9e04e8951642779910599db7ca33824e7b9029

NEXAH_PMR01C_INCREMENTAL_SPECTRAL_PHASE_UTILITY_2026-09-30
scientific result hash:
8850a0b78830472bae92521cfb54df4d13552351756dfb40c117d53147770150

NEXAH_PIR01_PRIME_INDEX_REENTRY_MOTIF_2026-09-30
scientific result hash:
6094963ee23de2d3a70f5f54882074e32febfaed8316461d2549a493ae3b9cf2

NEXAH_GEN01_RELATION_OBJECT_GENERATION_PRESERVATION_2026-09-30
scientific result hash:
b14595f8b7c798538900de0bdb6b49b9bd715a530a205984c9f01d448f0d3ae6

NEXAH_GEN02_HETEROGENEOUS_RELATION_FAMILY_TRANSFER_2026-09-30
scientific result hash:
02317b749d8c9a7abe6b9cdd74310fee99fda4ebd954d7140457c9d3f895ed50
```

Historische Diagramme und System-Overview-Grafiken dienen als
Orientierungsquellen und `VISUAL_MNEMONIC`. Wo deren Pfeilketten über die oben
registrierten Definitionen hinausgehen, bleiben sie `OPEN_BRIDGE` und werden
nicht als eigenständiger Beleg verwendet.
