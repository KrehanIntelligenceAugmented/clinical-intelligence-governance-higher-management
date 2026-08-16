# Veröffentlichung zurückziehen

Diese Anleitung nimmt die Präsentation vollständig vom Netz. Nichts davon
läuft automatisch — die Abschaltung wird ausdrücklich von Ihnen ausgelöst.

Alle Befehle im Repository-Verzeichnis ausführen. Falls `gh` das
Konfigurationsverzeichnis nicht findet, vorher setzen:

```bash
export GH_CONFIG_DIR=/tmp/claude-501/ghconfig
```

## Variante A — schnellste Abschaltung, Repository bleibt

Nimmt die Website sofort offline. Das Repository und beide Archivfassungen
bleiben erhalten.

```bash
gh api -X DELETE repos/KrehanIntelligenceAugmented/clinical-intelligence-governance-higher-management/pages
```

Die URL liefert danach 404. Die Auslieferung kann bis zu etwa zehn Minuten
nachhängen, weil das GitHub-CDN zwischenspeichert.

## Variante B — zusätzlich das Repository privat schalten

Entzieht auch dem Repository selbst die Öffentlichkeit.

```bash
gh api -X DELETE repos/KrehanIntelligenceAugmented/clinical-intelligence-governance-higher-management/pages
gh repo edit KrehanIntelligenceAugmented/clinical-intelligence-governance-higher-management --visibility private --accept-visibility-change-consequences
```

## Variante C — vollständig entfernen

Löscht das Repository unwiderruflich. Nur ausführen, wenn eine lokale Kopie
gesichert ist.

```bash
gh repo delete KrehanIntelligenceAugmented/clinical-intelligence-governance-higher-management --yes
```

Die lokale Sicherung liegt unabhängig davon unter
`Berichte und Präsentationen für das Higher Management/`.

## Prüfen, ob die Abschaltung gegriffen hat

```bash
curl -s -o /dev/null -w "%{http_code}\n" \
  https://krehanintelligenceaugmented.github.io/clinical-intelligence-governance-higher-management/
```

Erwartet wird `404`. Solange `200` zurückkommt, ist noch der CDN-Cache aktiv.

## Hinweis

Der `noindex`-Hinweis und die `robots.txt` verhindern die Aufnahme in
Suchmaschinen, sind aber **keine Zugriffssperre**. Solange die Seite online
ist, kann sie jede Person mit der URL ohne Anmeldung öffnen. Wer die Seite
bereits geöffnet oder gespeichert hat, behält seine Kopie auch nach der
Abschaltung.
