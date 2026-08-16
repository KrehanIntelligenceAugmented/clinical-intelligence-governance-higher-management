# Clinical Intelligence Governance — Präsentation für das Higher Management

**Verbindliche finale Präsentationsfassung · Stand 16. August 2026**

Ingomar Krehan · Stabsstelle Medizinische Entwicklung ·
Kepler Universitätsklinikum

Adressaten: Geschäftsführung Kepler Universitätsklinikum und
Oberösterreichische Gesundheitsholding.

---

## Die Präsentation

**→ [Präsentation öffnen](https://krehanintelligenceaugmented.github.io/clinical-intelligence-governance-higher-management/)**

15-minütiger strategischer Impulsvortrag. 14 Kernscreens, Redezeit 14:50,
zuzüglich vier Anhangsfolien, die außerhalb der Redezeit stehen und nicht im
Fortschrittsstrahl mitlaufen.

Bedienung: Pfeiltasten navigieren · `O` öffnet die Übersicht · `F` schaltet
auf Vollbild.

Die Seite ist eine eigenständige HTML-Datei mit eingebettetem CSS und
eingebetteten Vektorgrafiken. Sie lädt keine externen Skripte, Bibliotheken
oder Tracker.

---

## Inhaltlicher Aufbau

| | Screen | Kernaussage |
|---|---|---|
| 01 | Ausgangslage | KI kommt bereits — die Entscheidung ist, ob der Zufluss geordnet wird. |
| 02 | Ordnung | Werkzeuge werden nach klinischem Zweck geordnet, nicht nach Anbieter. |
| 03 | Layer 1 | Information, Prozesse und Wissen sind drei verbundene klinische Fähigkeiten. |
| 04 | Kognitive Last | Zu viel unverdichtete Information zum falschen Zeitpunkt ist ein klinisches Risiko. |
| 05 | Amplified Intelligence | Cognitive Offloading soll klinisches Denken ermöglichen, nicht ersetzen. |
| 06 | Evidenzlandkarte | Die Evidenz trägt, aber auf unterschiedlichen Wirkungsebenen. |
| 07 | Translationslücke | Systemleistung ist noch keine klinische Wirkung. |
| 08 | Research Loop | Außen die professionelle Wissensarbeit, innen der technische Ablauf. |
| 09 | AI Communication | Ein neues professionelles Skillset, mehr als Prompting. |
| 10 | Erster Implementierungsfall | Ein kontrollierter Pfad — nicht die Gesamtarchitektur. |
| 11 | Entry Use Case | Ein abgegrenzter Startpunkt erlaubt ein belastbares Urteil. |
| 12 | Anschlussarchitektur | Layer 2 und Layer 3 schließen an, sie führen nicht. |
| 13 | Management-Gate | Vor Skalierung braucht die Institution eigene Bewertungsfähigkeit. |
| 14 | Auftrag | Technologie beurteilen. Klinische Wirkung prüfen. Verantwortung behalten. |

Die Anhänge Q1 bis Q3 nennen zu jeder herangezogenen Arbeit, was sie zeigt und
was sie **nicht** zeigt. Q4 erklärt die verwendeten Begriffe.

---

## Repository-Struktur

```
docs/
  index.html      veröffentlichte Fassung
  robots.txt      sperrt Suchmaschinen aus
archive/
  Clinical_Intelligence_Governance_FINAL_2026-08-16.html
  Clinical_Intelligence_Governance_QA-Zwischenstand_2026-08-16.html
UNPUBLISH.md      Anleitung zum Zurückziehen der Veröffentlichung
```

GitHub Pages liefert ausschließlich `docs/` aus. Der Ordner `archive/` ist
nicht Teil der Website.

### Gesicherte Fassungen

| Datei | SHA-256 | Status |
|---|---|---|
| `archive/…_FINAL_2026-08-16.html` | `9a9faee63c5613caf6d3cea02fc66b60e2bdd3cd83cd3d7f2774ce7ba7d335b0` | **Verbindliche finale Präsentationsfassung.** Unverändert gesichert. |
| `docs/index.html` | `0d71c9dc1b49d6d8ff98207cbfa643a45b645eaa8a99935ccdf2b3115b3c82d2` | Ausgelieferte Fassung: die Endfassung zuzüglich zweier `robots`-Meta-Tags. Keine sichtbare Änderung. |
| `archive/…_QA-Zwischenstand_2026-08-16.html` | `a39d6431317dd20b605c7db4562da5e617558f0f02d337f61ddfe284223a4991` | Archivfassung zur Nachvollziehbarkeit. Nicht vortragen, nicht verlinken. |

Der QA-Zwischenstand entstand 100 Sekunden vor dem finalen Build. Einziger
Unterschied: Auf Screen 11 waren die Spaltenbreiten der drei Karten so
gesetzt, dass sich die Zeilen „Evaluation" und „Delir" überlappten. In der
finalen Fassung sind die Breiten korrigiert (linke Karte 350 → 326 Einheiten,
mittlere 320 → 296). Wortlaut, Farben und Typografie sind in beiden Fassungen
gleich.

**Der QA-Zwischenstand hat keine eigene Präsentations-URL.** GitHub Pages
liefert ausschließlich `docs/` aus.

Die ausgelieferte Fassung unterscheidet sich von der archivierten Endfassung
in genau zwei Zeilen: den `robots`-Meta-Tags `noindex, nofollow, noarchive`.
Sie sind nicht sichtbar und ändern weder Inhalt noch Gestaltung.

---

## Qualitätsstand

- Abnahmeskript: 59 von 59 Prüfungen bestanden
- Druckfassung: kein Textüberlauf, keine Kollisionen
- Lesbarkeit bei 1920 × 1080 gemessen: Folientitel 46,4 px, Fließtext in den
  Grafiken 24,7 px, Kurzquellenzeile 16,3 px — ausgelegt für einen 43- bis
  65-Zoll-Bildschirm aus zwei bis drei Metern Abstand
- Kodierung UTF-8, Normalform NFC
- Bewegung: einmaliger Aufbau je Screen; `prefers-reduced-motion` liefert die
  vollständige statische Fassung

### Bekannte Einschränkung

Die Endfassung bindet die Hausschriften über lokale Pfade ein. Auf dem Server
greifen diese nicht; die Darstellung fällt dort auf die Systemschrift zurück,
wodurch sich Zeilenumbrüche geringfügig verschieben können. Die Datei wurde
bewusst byte-identisch übernommen und dafür nicht verändert.

---

## Offener Punkt

Auf Screen 11 sind bewusst keine Leistungskennzahlen zum Entry Use Case
angegeben. Die betreffenden Werte sind im zugrunde liegenden Dossier nicht
belegt; das Produkt ist dort ausdrücklich als nicht unabhängig geprüft
geführt. Vor einer Verwendung ist die Primärquelle beizubringen. Die Werte
dürfen nicht als bereits belegter lokaler Patientennutzen dargestellt werden.

---

## Veröffentlichung

Die Seite ist vorübergehend öffentlich erreichbar, damit sie ohne Anmeldung
geöffnet werden kann. Sie ist über `noindex` und `robots.txt` von
Suchmaschinen ausgenommen; das ist keine Zugriffssperre.

Die Veröffentlichung wird nach der Präsentation zurückgezogen. Die Anleitung
dazu steht in [UNPUBLISH.md](UNPUBLISH.md).

---

© 2026 Ingomar Krehan. Alle Rechte vorbehalten. Siehe [RIGHTS.md](RIGHTS.md).
