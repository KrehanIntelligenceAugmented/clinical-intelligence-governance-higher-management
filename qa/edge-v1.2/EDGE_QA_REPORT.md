# Abnahmebericht — Edge-tauglicher Präsentationsableger v1.2

**Stand:** 16. August 2026
**Fassung:** `docs/presentation-v1.2/index.html`
**Grundlage:** `Clinical_Intelligence_Governance_FINAL_2026-08-16.html`
**Fallback-Fassung:** unverändert unter `docs/index.html`

---

## 1. Ursache der Edge-Darstellungsfehler

Die bisherige Fassung war keine Präsentation, sondern eine lange Webseite mit
Scroll-Rasterung:

- Jede Folie war ein Dokumentfluss-Element mit `min-height: 100vh`.
- Die Navigation arbeitete mit `scrollIntoView()`.
- Die Steuerleiste lag als `position: fixed` über dem Dokument.

Daraus folgten drei Fehlermechanismen, die in Edge besonders sichtbar wurden:

**Erstens: `100vh` ist nicht die nutzbare Höhe.** Edge zieht Adressleiste,
Favoritenleiste und bei Windows zusätzlich die Anzeigeskalierung ab. War der
Folieninhalt auch nur wenige Pixel höher als der reale Viewport, entstand
Dokument-Scrolling.

**Zweitens: Sobald gescrollt wurde, war die Folie keine geschlossene Seite
mehr.** Zwei Folien waren gleichzeitig angeschnitten sichtbar, und die fest
positionierte Steuerleiste lag über dem Inhalt statt darunter.

**Drittens: `scroll-snap-type: proximity` rastet nur in der Nähe ein.**
Zwischen den Rastpunkten entstanden die unharmonischen Scrollbewegungen. Der
Folienwechsel war eine Scrollbewegung, keine Präsentationsgeste.

Verstärkend kam hinzu, dass die Schriftgrößen über `clamp()` mit `vw`-Anteilen
gesetzt waren. Bei Zoom oder abweichender Fenstergröße änderten sich die
Textgrößen, dadurch die Folienhöhe, dadurch das Scrollverhalten.

---

## 2. Geänderte technische Architektur

| | vorher | jetzt |
|---|---|---|
| Folienanordnung | Dokumentfluss untereinander | absolut gestapelt, `position: absolute; inset: 0` |
| Sichtbarkeit | alle im Fluss | genau eine mit `.is-active`, übrige `visibility: hidden` |
| Navigation | `scrollIntoView()` | Klassenwechsel mit Kreuzblende |
| Dokumenthöhe | wächst mit der Folienzahl | `html, body { height: 100%; overflow: hidden }` |
| Folienmaß | fließend, viewportabhängig | feste Bühne 1920 × 1080, proportional skaliert |
| Schriftgrößen | `clamp()` mit `vw` | auf die Entwurfsbreite eingefroren, mit der Bühne skaliert |
| Steuerleiste | `fixed` über dem Inhalt | Deckbereich endet oberhalb der Leiste |
| Schriften | absolute Mac-Pfade | drei WOFF2-Dateien mit relativen Pfaden |

### Fit-to-Viewport

Ein Skalierungsfaktor `k = min(vw / 1920, verfügbareHöhe / 1080)` wird als
CSS-Variable gesetzt; die Bühne trägt `transform: translate(-50%, -50%)
scale(k)` in klassischer Schreibweise, nicht als einzelne
`translate`-Eigenschaft. Der Faktor ist auf 0,12 bis 1,6 begrenzt.

Die verfügbare Höhe ergibt sich aus der **gemessenen** Höhe der Steuerleiste,
nicht aus einem angenommenen Wert — sie ändert sich mit Browserzoom und
Anzeigeskalierung. Neuberechnet wird bei `resize`, `orientationchange`,
`fullscreenchange`, über einen `ResizeObserver` auf dem Wurzelelement, über
`visualViewport.resize` und nach `document.fonts.ready`.

### Edge-kritische CSS-Eigenschaften

`color-mix()` wurde durch statische Farbwerte ersetzt (`#171d24` für die
Leiste, `#0a0d11` für das Overlay). Einzelne `translate`-Eigenschaften wurden
durch klassische `transform`-Syntax ersetzt. `100dvh` wird nicht mehr
benötigt, da die Höhe zur Laufzeit gemessen wird.

### Entfernte Reflow-Media-Queries

Ein Befund aus der Prüfung: Bei 1366 × 768 mit 125 % Zoom (CSS-Viewport
1093 × 614) griff `@media (max-width: 1100px)` und stellte die Anhangsfolien
auf eine Spalte um. Der Inhalt wurde dadurch höher als die Bühne und
abgeschnitten — betroffen waren Screen 08 und alle vier Anhangsfolien. Da die
Bühne immer 1920 breit ist und als Ganzes skaliert wird, dürfen
viewportabhängige Umbrüche nicht mehr greifen. Alle `max-width`-Media-Queries
wurden daher aus der Bühnenschicht entfernt. `prefers-reduced-motion` bleibt.

---

## 3. Ist der Inhalt nachweislich unverändert?

**Ja.** Nachgewiesen über einen Inhaltsfingerabdruck: Je `<section
class="screen">` wird der sichtbare Text von Auszeichnung befreit, in
Unicode-Normalform NFC überführt, in der Weißraumfolge normalisiert und als
SHA-256 gebildet. Der Gesamtfingerabdruck verkettet ID und Hash aller Screens.

```
vorher   9815fffe6bbd9acc959efc2ce20dfac0dffba74217c8823960d432d57dd85685
nachher  9815fffe6bbd9acc959efc2ce20dfac0dffba74217c8823960d432d57dd85685
```

- Screens: 19 vor und nach der Umstellung (15 Hauptteil einschließlich
  Startfolie, 4 Anhang Q1–Q4)
- SVG-Grafiken: 15 vor und nach der Umstellung
- Reihenfolge und IDs identisch: `s00`–`s14`, `sQ1`–`sQ4`
- Abweichende Screens: keine

Belege: `FINGERPRINT_VORHER.json`, `FINGERPRINT_NACHHER.json`,
Werkzeug `fingerprint.py`.

Ergänzt wurden ausschließlich technische Bedienelemente: `aria-label` an den
Pfeilschaltflächen, `aria-expanded`/`aria-controls` an der Übersichtstaste,
`role="dialog"` und `aria-modal` am Overlay, `type="button"` an allen
Schaltflächen.

---

## 4. Welche Edge-Version wurde geprüft?

**Keine.** Microsoft Edge ist auf diesem Rechner nicht installiert, und es
steht weder Playwright noch npx zur Verfügung, um Edge zu beschaffen. Die
Prüfung erfolgte im Chromium-basierten Browser dieser Umgebung.

Das ist aussagekräftig, aber nicht gleichwertig: Edge verwendet dieselbe
Blink-Engine und dasselbe Layoutmodell wie Chromium. Die beschriebenen
Fehlermechanismen — Viewporthöhe, Zoom, Anzeigeskalierung — sind damit
reproduzierbar. Nicht abgedeckt sind Edge-spezifische Oberflächenelemente und
das reale Zusammenspiel mit der Windows-Anzeigeskalierung.

**Ein manueller Edge-Abnahmeschritt ist daher vorgesehen**, siehe Abschnitt 9.

---

## 5. Auflösungen und Zoomstufen

| Test | CSS-Viewport | Skala | 19 Screens |
|---|---|---|---|
| 1920 × 1080 · 100 % | 1920 × 1080 | 0,933 | bestanden |
| 1536 × 864 · 100 % | 1536 × 864 | 0,733 | bestanden |
| 1536 × 864 · 125 % Zoom | 1229 × 691 | 0,573 | bestanden |
| 1366 × 768 · 100 % | 1366 × 768 | 0,644 | bestanden |
| 1366 × 768 · 125 % Zoom | 1093 × 614 | 0,502 | bestanden |
| 1280 × 720 · 100 % | 1280 × 720 | 0,600 | bestanden |
| Fenster mit Adress- und Favoritenleiste | 1536 × 722 | 0,602 | bestanden |
| iPhone Hochformat | 375 × 812 | 0,195 | bestanden |
| iPhone Querformat | 812 × 375 | 0,281 | bestanden |

Je Auflösung wurde **jede der 19 Folien einzeln** geprüft auf: genau ein
sichtbarer Screen, Bühne vollständig im Viewport, Bühne oberhalb der
Steuerleiste, keine Überschneidung zwischen Leiste und Inhalt, kein
Inhaltsobjekt außerhalb der Bühne, kein Dokument-Scrollen. Das sind 171
Einzelprüfungen. Messwerte in `MESSWERTE.json`.

Die 125-%-Zoomstufen wurden über den entsprechend verkleinerten CSS-Viewport
nachgebildet — das ist genau der Effekt, den Browserzoom und Windows-
Anzeigeskalierung auf das Layout haben.

---

## 6. Überlagerungen und abgeschnittene Elemente

- Kopf-, Fuß- und Aussageelemente über alle 19 Folien: **0 Kollisionen**
- Inhaltsobjekte außerhalb der Bühnenfläche: **0** in allen neun
  Auflösungen
- Screen 11: keine Überlappung zwischen „Evaluation:" und „Delir" —
  geometrisch gegen die SVG-Textknoten geprüft
- Konsolenfehler: **0** · HTTP-404: **0** · externe Ressourcen: **0**
- Schriften: drei WOFF2 relativ eingebunden, `document.fonts.ready` erfüllt,
  aktive Familie „Noto Sans"; keine `/Users/`-, `file://`- oder
  localhost-Referenz im Dokument

---

## 7. Verhalten der Übersicht

| Prüfpunkt | Ergebnis |
|---|---|
| geschlossen | `hidden` gesetzt, `display: none` über `[hidden] { display: none !important }` |
| geöffnet | `position: fixed`, `z-index: 200`, deckt den Viewport vollständig |
| Deck während der Anzeige | `aria-hidden="true"`, Folien nicht bedienbar |
| Schließen mit Escape | funktioniert |
| Layoutsprung beim Schließen | keiner, da das Overlay nie Platz im Fluss belegt |
| Auswahl einer Folie | Overlay schließt, Wechsel per Kreuzblende, Hash aktualisiert |
| Elemente ragen in Folien | nein, das Overlay ist vollflächig oder gar nicht vorhanden |

Geprüftes Beispiel: Sprung auf Screen 11 aus der Übersicht → aktiv `s11`,
Übersicht geschlossen, Adresszeile `#s11`.

---

## 8. Dauer und Verhalten der Überblendung

- Ausblenden: 200 ms
- Einblenden: 270 ms
- gemessene Gesamtdauer eines Wechsels: **528 ms**
- 100 ms nach Auslösung: abgehende Folie bei Opazität 0,42, ankommende bei
  0,00 → **keine gleichzeitig lesbaren Texte**
- reine Opazitätsüberblendung, kein Zoom, kein Versatz, kein Scrollen
- `prefers-reduced-motion: reduce` schaltet auf sofortigen Wechsel

Mehrfachauslösung: Sechs schnelle Klicks ab der Startfolie landen auf Screen
06, fünf schnelle Tastendrücke auf Screen 05. Eingaben summieren sich also
korrekt, statt verworfen zu werden; dabei ist zu jedem Zeitpunkt genau eine
Folie sichtbar. Zwischenschritte werden übersprungen, nur der letzte Wechsel
wird animiert.

Die folieninternen Aufbauanimationen (`data-step`) bleiben erhalten. Sie
werden beim Aktivieren der Folie ausgelöst und laufen nach der Einblendung —
Folienwechsel und Aufbau stören einander nicht.

---

## 9. Verbleibende Einschränkungen

**1. Kein Test im echten Microsoft Edge.** Siehe Abschnitt 4. Der manuelle
Abnahmeschritt:

1. Neue URL in Edge öffnen.
2. `F11` für Vollbild, dann mit den Pfeiltasten durch alle 19 Folien.
3. Zoom mit `Strg` und `+`/`−` auf 125 % und zurück auf 100 % — die Folie
   muss dabei vollständig sichtbar bleiben.
4. Fenster nicht maximiert, mit sichtbarer Favoritenleiste.
5. Prüfen: immer genau eine Folie, keine vertikale Bildlaufleiste, die
   Steuerleiste liegt unterhalb des Inhalts.
6. Übersicht mit `O` öffnen und schließen.

**2. Typografische Abweichungen.** Die Bühne skaliert; bei kleinen Fenstern
werden Texte entsprechend klein. Das ist gewollt und ersetzt das frühere
Abschneiden. Auf einem Telefon im Hochformat ist die Folie bei Skala 0,195
zwar vollständig, aber nur eingeschränkt lesbar — die Präsentation ist für
Bildschirm und Beamer ausgelegt, das Telefon dient der Kontrolle.

**3. Keine Screenshot-Dateien im Bericht.** Die Prüfung erfolgte interaktiv im
Browser; diese Umgebung kann Browser-Screenshots nicht auf die Festplatte
schreiben. Als maschinenlesbarer Beleg dienen stattdessen `MESSWERTE.json`
mit allen Geometriedaten je Auflösung sowie die beiden
Fingerabdruckdateien. Visuell einzeln kontrolliert wurden: Startfolie,
Screen 03 (drei Säulen), Screen 08 (Research Loop), Screen 11 (Entry Use
Case), Anhang Q1 sowie die Übersicht.

**4. Die Fallback-Fassung bleibt unverändert.** `docs/index.html` und die
bisherige URL sind nicht angefasst worden.


---

## 10. Nachtrag: Prüfung der veröffentlichten Fassung

Die folgenden Werte stammen aus der **live abgerufenen** Seite unter
`https://krehanintelligenceaugmented.github.io/clinical-intelligence-governance-higher-management/presentation-v1.2/`,
nicht aus der lokalen Datei.

| Auflösung | 19 Screens |
|---|---|
| 1920 × 1080 · 100 % | bestanden |
| 1366 × 768 · 125 % Zoom (CSS 1093 × 614) | bestanden |
| Fenster mit Adress- und Favoritenleiste, 1536 × 722 | bestanden |
| iPhone Hochformat 375 × 812 | bestanden |

- Kreuzblende live gemessen: **604 ms**; 100 ms nach Auslösung abgehende
  Folie bei Opazität 0,20, ankommende bei 0,00 — keine lesbare Überlagerung
- Sechs schnelle Klicks → Screen 06, fünf Tastendrücke → Screen 05
- Tastatur: rechts, links, PageDown, PageUp, Leertaste, Home, End korrekt
- Randzustände: auf der ersten Folie „zurück" deaktiviert, auf der letzten
  „vor" deaktiviert
- Übersicht: `position: fixed`, `z-index: 200`, volldeckend, Deck
  `aria-hidden="true"`; Sprung auf Screen 11 setzt aktiv `s11` und Hash `#s11`
- Konsolenfehler: 0 · Schriften geladen, aktive Familie „Noto Sans"
- `robots`: `noindex, nofollow, noarchive`

### Drei Befunde, die erst im Verlauf sichtbar wurden

**1. Reflow-Media-Queries.** Bei 125 % Zoom griff `@media (max-width: 1100px)`
und stellte die Anhangsfolien auf eine Spalte um; Screen 08 und alle vier
Anhangsfolien wurden angeschnitten. Behoben durch Entfernen der
`max-width`-Media-Queries aus der Bühnenschicht.

**2. Schriftmetrik.** Nach dem Laden der echten Noto-Sans-WOFF2 liefen die
Anhangsfolien Q1 und Q3 um 24 beziehungsweise 39 Pixel über die Bühne — lokal
war das nicht aufgefallen, weil dort noch die Ersatzschrift maß. Behoben durch
eine Feineinpassung je Folie: Die tatsächliche Ausdehnung aller Nachfahren
wird gemessen und der Inhalt bei Bedarf proportional verkleinert, mit acht
Pixeln Sicherheitsabstand. Live wirksam: Q1 bei Faktor 0,9408, Q3 bei 0,9109,
alle übrigen Folien ohne Verkleinerung.

**3. Eingabepufferung.** Sechs schnelle Klicks führten zunächst nur zwei
Folien weiter. Die Navigation rechnet jetzt ab dem zuletzt angeforderten Ziel,
sodass sich Eingaben aufsummieren.

Der Inhaltsfingerabdruck blieb über alle drei Korrekturen unverändert
(`9815fffe…85685`).
