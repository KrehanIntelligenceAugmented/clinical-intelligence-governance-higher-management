# -*- coding: utf-8 -*-
"""Erzeugt den Edge-tauglichen Praesentationsableger v1.2.

Grundlage ist die verbindliche Endfassung. Der Inhalt jedes <section
class="screen"> wird unveraendert uebernommen. Ersetzt werden ausschliesslich:

  · die Praesentationsschicht (Layout, Navigation, Uebergaenge),
  · die Schriftbindung (WOFF2 mit relativen Pfaden statt lokaler Mac-Pfade),
  · viewportabhaengige CSS-Einheiten innerhalb der Buehne.

Kernproblem der bisherigen Fassung
----------------------------------
Die Folien lagen als Fluss im Dokument (`min-height:100vh` plus
`scroll-snap`), die Navigation arbeitete mit `scrollIntoView()`. In Edge
haengt die tatsaechliche Viewporthoehe von Adress- und Favoritenleiste,
Browserzoom und Windows-Anzeigeskalierung ab. Sobald der Inhalt hoeher wurde
als der reale Viewport, entstand Dokument-Scrolling: mehrere Folien
gleichzeitig sichtbar, die feste Steuerleiste ragte in den Inhalt.

Loesung
-------
Echter Praesentationsmodus: `html`/`body` auf Viewportgroesse begrenzt, alle
Folien absolut gestapelt, genau eine aktiv. Jede Folie liegt auf einer Buehne
mit fester Entwurfsgroesse 1920 x 1080 und wird als Ganzes proportional in
den verfuegbaren Bereich skaliert. Damit ist die Darstellung unabhaengig von
Fensterhoehe, Zoom und Anzeigeskalierung.
"""

import hashlib
import io
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
SRC = ("/Users/Ingomar/Desktop/Higher Management/"
       "Berichte und Präsentationen für das Higher Management/"
       "Clinical_Intelligence_Governance_FINAL_2026-08-16.html")
OUT = os.path.join(REPO, "docs", "presentation-v1.2", "index.html")

DESIGN_W, DESIGN_H = 1920.0, 1080.0
BAR_RESERVE = 62          # Hoehe der Steuerleiste, bleibt inhaltsfrei


# ==========================================================================
def freeze_viewport_units(css):
    """vw/vh/dvh in der Buehne auf die Entwurfsgroesse einfrieren.

    Innerhalb der Buehne darf keine Groesse mehr vom realen Viewport
    abhaengen, sonst waere die Skalierung nicht mehr proportional.
    """
    def vw(m):
        return "%.4gpx" % (float(m.group(1)) * DESIGN_W / 100.0)

    def vh(m):
        return "%.4gpx" % (float(m.group(1)) * DESIGN_H / 100.0)

    css = re.sub(r"(-?[\d.]+)dvh\b", vh, css)
    css = re.sub(r"(-?[\d.]+)vh\b", vh, css)
    css = re.sub(r"(-?[\d.]+)vw\b", vw, css)
    return css


def strip_rules(css, selectors):
    """Regeln der alten Praesentationsschicht entfernen."""
    for sel in selectors:
        css = re.sub(r"(?m)^\s*" + re.escape(sel) + r"\s*\{[^}]*\}\s*", "", css)
    return css


# ==========================================================================
SHELL_CSS = """
/* ==================================================================
   Praesentationslaufzeit v1.2 — Edge-tauglich
   Genau eine Folie im Viewport, feste Buehne, proportionale Skalierung.
   ================================================================== */

@font-face { font-family:"Noto Sans"; font-weight:400; font-style:normal;
  font-display:swap; src:url("fonts/NotoSans-Regular.woff2") format("woff2"); }
@font-face { font-family:"Noto Sans"; font-weight:600 700; font-style:normal;
  font-display:swap; src:url("fonts/NotoSans-Bold.woff2") format("woff2"); }
@font-face { font-family:"DejaVu Sans Mono"; font-weight:400; font-style:normal;
  font-display:swap; src:url("fonts/DejaVuSansMono.woff2") format("woff2"); }

:root {
  --font-sans: "Noto Sans", "Segoe UI", Arial, sans-serif;
  --font-mono: "DejaVu Sans Mono", "Cascadia Mono", Consolas, monospace;
  --bar-bg: #171d24;              /* statischer Ersatz fuer color-mix() */
  --map-bg: #0a0d11;
}

html, body {
  height: 100%; max-height: 100%;
  margin: 0; padding: 0;
  overflow: hidden;               /* kein Dokument-Scrollen */
  background: var(--ink);
}
body { font-family: var(--font-sans); color: var(--text); }

/* --- Deck: alle Folien absolut gestapelt --------------------------- */
/* Der Deckbereich endet oberhalb der Steuerleiste. Dadurch kann die
   Leiste den Folieninhalt konstruktiv nicht ueberdecken. */
#deck { position: fixed; top: 0; right: 0; left: 0;
        bottom: calc(var(--barh, 62px) + 14px); overflow: hidden; }

.screen {
  position: absolute; top: 0; right: 0; bottom: 0; left: 0;
  display: block; min-height: 0; height: auto; padding: 0;
  border: 0 !important;
  opacity: 0; visibility: hidden; pointer-events: none;
  transition: opacity 200ms ease;
  z-index: 1;
}
.screen.is-active   { opacity: 1; visibility: visible; pointer-events: auto; z-index: 2;
                      transition: opacity 270ms ease; }
.screen.is-leaving  { opacity: 0; visibility: visible; z-index: 3;
                      transition: opacity 200ms ease; }

/* --- Buehne: feste Entwurfsgroesse, proportional skaliert ---------- */
.stage {
  position: absolute; top: 50%; left: 50%;
  width: 1920px; height: 1080px;
  transform: translate(-50%, -50%) scale(var(--k, 1));
  transform-origin: 50% 50%;
  display: grid; place-items: center;
  padding: 46px 64px;
  box-sizing: border-box;
  overflow: hidden;
}
.stage > .inner { width: 100%; max-width: 1560px; }
.screen--title .stage { place-items: center start; }

/* --- Steuerleiste: liegt ausserhalb der Buehnenflaeche ------------- */
.bar {
  position: fixed; left: 50%; bottom: 12px; transform: translateX(-50%);
  z-index: 60;
  display: flex; align-items: center; gap: 8px;
  background: var(--bar-bg); border: 1px solid var(--line);
  border-radius: 999px; padding: 6px 10px;
}
.bar__b {
  min-width: 44px; min-height: 44px;
  display: inline-flex; align-items: center; justify-content: center;
  border-radius: 999px; color: var(--muted); background: none; border: 0;
  font: inherit; cursor: pointer;
  transition: background 160ms ease, color 160ms ease;
}
.bar__b:hover { background: var(--panel-3); color: var(--text); }
.bar__b:focus-visible { outline: 2px solid var(--record); outline-offset: 2px; }
.bar__b[disabled] { opacity: .32; cursor: default; }
.bar__b[disabled]:hover { background: none; color: var(--muted); }
.bar__b--w { padding: 0 14px; font: 500 12px/1 var(--font-mono);
             letter-spacing: .1em; min-width: 0; }
.bar__pos { font: 500 14px/1 var(--font-mono); color: var(--faint);
            padding: 0 4px; white-space: nowrap; }
.bar__pos b { color: var(--text); font-weight: 600; }
.bar__pos i { font-style: normal; }
.bar__dots { display: flex; gap: 3px; padding: 0 8px;
             border-left: 1px solid var(--line); border-right: 1px solid var(--line); }
.bar__dots button { width: 15px; height: 5px; border-radius: 3px; border: 0;
                    background: var(--panel-3); cursor: pointer; padding: 0;
                    transition: background 160ms ease, height 160ms ease; }
.bar__dots button:hover { background: var(--muted); }
.bar__dots button.is-on { background: var(--record); height: 8px; }
.bar__dots button:focus-visible { outline: 2px solid var(--record); outline-offset: 2px; }

/* Die Quellenzeile bekommt eine eigene volle Zeile unter den Chips.
   Mit Quellenschluesseln wird sie laenger; nebeneinander wuerde sie in
   drei schmale Zeilen brechen. */
.foot { row-gap: 6px; }
.foot__src { flex: 1 1 100%; order: 9; }
.foot__no { order: 8; margin-left: auto; }

/* --- Uebersicht: echtes modales Overlay ---------------------------- */
[hidden] { display: none !important; }
.map {
  position: fixed; top: 0; right: 0; bottom: 0; left: 0;
  z-index: 200; overflow: auto; background: var(--map-bg);
  padding: 40px clamp(20px, 4vw, 56px);
}
.map__in { max-width: 1560px; margin: 0 auto; display: grid; gap: 24px; }
.map__x { position: fixed; right: 22px; top: 18px; z-index: 201;
          min-width: 44px; min-height: 44px; font-size: 26px; line-height: 1;
          color: var(--muted); background: none; border: 0; cursor: pointer; }
.map__x:hover { color: var(--text); }
.map__x:focus-visible { outline: 2px solid var(--record); outline-offset: 2px; }

/* --- Bewegung ------------------------------------------------------ */
@media (prefers-reduced-motion: reduce) {
  .screen, .screen.is-active, .screen.is-leaving { transition: none !important; }
}
"""

SHELL_JS = r"""
(function () {
  'use strict';
  var deck   = document.getElementById('deck');
  var all    = Array.prototype.slice.call(deck.querySelectorAll('.screen'));
  var rail   = all.filter(function (s) { return s.getAttribute('data-rail') === '1'; });
  var dots   = Array.prototype.slice.call(document.querySelectorAll('#dots button'));
  var posn   = document.getElementById('posn');
  var prevB  = document.getElementById('prevb');
  var nextB  = document.getElementById('nextb');
  var map    = document.getElementById('map');
  var mapBtn = document.getElementById('mapbtn');

  var DESIGN_W = 1920, DESIGN_H = 1080;
  var barEl = document.querySelector('.bar');
  var OUT_MS = 200, IN_MS = 270;
  var cur = 0, want = 0, busy = false, queued = null;

  var reduce = window.matchMedia &&
               window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- Fit to viewport ------------------------------------------- */
  function fit() {
    /* Die Leistenhoehe wird gemessen, nicht angenommen: sie aendert sich
       mit Browserzoom und Windows-Anzeigeskalierung. */
    var barH = Math.round(barEl.getBoundingClientRect().height) || 56;
    document.documentElement.style.setProperty('--barh', barH + 'px');
    var vw = document.documentElement.clientWidth;
    var vh = document.documentElement.clientHeight;
    var avail = Math.max(200, vh - barH - 14);
    var k = Math.min(vw / DESIGN_W, avail / DESIGN_H);
    k = Math.max(0.12, Math.min(k, 1.6));
    for (var i = 0; i < all.length; i++) {
      var st = all[i].querySelector('.stage');
      if (!st) { continue; }
      st.style.setProperty('--k', k);
      innerFit(st);
    }
  }

  /* Feineinpassung je Folie.

     Die Buehne ist 1920 x 1080 gross. Ob der Folieninhalt darin Platz hat,
     haengt von der tatsaechlich geladenen Schrift ab: Ersatzschriften bauen
     anders als Noto Sans. Statt auf eine Metrik zu vertrauen, wird die
     benoetigte Hoehe gemessen und der Inhalt bei Bedarf proportional
     verkleinert. Dadurch kann nichts abgeschnitten werden. */
  function innerFit(st) {
    var inner = st.querySelector('.inner');
    if (!inner) { return; }
    inner.style.transform = '';
    var cs = getComputedStyle(st);
    var k = parseFloat(cs.getPropertyValue('--k')) || 1;
    var padT = parseFloat(cs.paddingTop) || 0;
    var room = DESIGN_H - 2 * padT;

    /* Die tatsaechliche Ausdehnung ueber alle Nachfahren messen: Kinder
       koennen ueber die .inner-Box hinauslaufen, ohne deren Hoehe zu
       veraendern. Gemessen wird im Bildschirmraum und durch den
       Buehnenfaktor auf Layoutpixel zurueckgerechnet. */
    var nodes = inner.querySelectorAll('*');
    var top = Infinity, bot = -Infinity;
    for (var i = 0; i < nodes.length; i++) {
      var b = nodes[i].getBoundingClientRect();
      if (!b.width && !b.height) { continue; }
      if (b.top < top) { top = b.top; }
      if (b.bottom > bot) { bot = b.bottom; }
    }
    if (!isFinite(top) || !isFinite(bot) || k <= 0) { return; }
    var need = (bot - top) / k;
    /* Acht Pixel Sicherheitsabstand, damit Rundungen bei der Skalierung
       nichts an den Buehnenrand druecken. */
    var target = room - 8;
    var s = (need > target) ? Math.max(0.70, target / need) : 1;
    inner.style.transformOrigin = '50% 50%';
    inner.style.transform = (s < 0.999) ? 'scale(' + s.toFixed(4) + ')' : '';
  }

  /* ---- Folienwechsel mit Kreuzblende ------------------------------ */
  function show(i, immediate) {
    i = Math.max(0, Math.min(all.length - 1, i));
    want = i;
    if (i === cur && all[cur].classList.contains('is-active')) { return; }
    if (busy) { queued = i; return; }
    busy = true;

    var from = all[cur], to = all[i];
    cur = i;
    updateChrome();

    function enter() {
      from.classList.remove('is-active', 'is-leaving');
      to.classList.add('is-active');
      to.classList.add('is-in');            /* interne Aufbauanimation */
      window.setTimeout(function () {
        busy = false;
        if (queued !== null) { var q = queued; queued = null; show(q); }
      }, immediate || reduce ? 0 : IN_MS);
    }

    if (immediate || reduce) {
      from.classList.remove('is-active', 'is-leaving');
      enter();
    } else {
      from.classList.add('is-leaving');
      from.classList.remove('is-active');
      window.setTimeout(enter, OUT_MS);
    }
  }

  function updateChrome() {
    var s = all[cur];
    posn.textContent = s.getAttribute('data-n');
    var k = rail.indexOf(s);
    for (var i = 0; i < dots.length; i++) {
      var on = (i === k - 1);
      dots[i].className = on ? 'is-on' : '';
      dots[i].setAttribute('aria-current', on ? 'true' : 'false');
    }
    prevB.disabled = (cur === 0);
    nextB.disabled = (cur === all.length - 1);
    if (s.id && history.replaceState) {
      history.replaceState(null, '', '#' + s.id);
    }
  }

  /* ---- Uebersicht -------------------------------------------------- */
  function setMap(on) {
    var open = (on === undefined) ? map.hidden : on;
    map.hidden = !open;
    deck.setAttribute('aria-hidden', open ? 'true' : 'false');
    mapBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    if (open) { map.focus(); }
  }

  function fullscreen() {
    if (document.fullscreenElement) {
      if (document.exitFullscreen) { document.exitFullscreen(); }
    } else if (document.documentElement.requestFullscreen) {
      document.documentElement.requestFullscreen();
    }
  }

  /* ---- Bedienung ---------------------------------------------------- */
  /* Navigation rechnet ab dem zuletzt angeforderten Ziel, damit sich
     schnelle Eingaben aufsummieren statt verworfen zu werden. */
  prevB.addEventListener('click', function () { show(want - 1); });
  nextB.addEventListener('click', function () { show(want + 1); });
  for (var d = 0; d < dots.length; d++) {
    (function (b) {
      b.addEventListener('click', function () { show(all.indexOf(rail[+b.getAttribute('data-go')])); });
    })(dots[d]);
  }
  mapBtn.addEventListener('click', function () { setMap(); });
  document.getElementById('mapx').addEventListener('click', function () { setMap(false); });
  document.getElementById('fsbtn').addEventListener('click', fullscreen);

  var links = Array.prototype.slice.call(map.querySelectorAll('a[href^="#"]'));
  for (var l = 0; l < links.length; l++) {
    (function (a) {
      a.addEventListener('click', function (e) {
        e.preventDefault();
        var t = document.getElementById(a.getAttribute('href').slice(1));
        setMap(false);
        if (t) { show(all.indexOf(t)); }
      });
    })(links[l]);
  }

  document.addEventListener('keydown', function (e) {
    if (e.metaKey || e.ctrlKey || e.altKey) { return; }
    var k = e.key;
    if (k === 'Escape') {
      if (!map.hidden) { e.preventDefault(); setMap(false); }
      else if (document.fullscreenElement) { e.preventDefault(); fullscreen(); }
      return;
    }
    if (k === 'o' || k === 'O') { e.preventDefault(); setMap(); return; }
    if (k === 'f' || k === 'F') { e.preventDefault(); fullscreen(); return; }
    if (!map.hidden) { return; }
    if (k === 'ArrowRight' || k === 'PageDown' || k === ' ' || k === 'Spacebar') {
      e.preventDefault(); show(want + 1);
    } else if (k === 'ArrowLeft' || k === 'PageUp') {
      e.preventDefault(); show(want - 1);
    } else if (k === 'Home') {
      e.preventDefault(); show(0);
    } else if (k === 'End') {
      e.preventDefault(); show(all.length - 1);
    }
  });

  window.addEventListener('hashchange', function () {
    var t = document.getElementById(location.hash.slice(1));
    if (t && all.indexOf(t) > -1) { show(all.indexOf(t)); }
  });

  /* ---- Neuberechnung bei jeder Groessenaenderung -------------------- */
  window.addEventListener('resize', fit);
  window.addEventListener('orientationchange', fit);
  document.addEventListener('fullscreenchange', fit);
  if (window.ResizeObserver) {
    new ResizeObserver(fit).observe(document.documentElement);
  }
  if (window.visualViewport) {
    window.visualViewport.addEventListener('resize', fit);
  }

  /* ---- Start -------------------------------------------------------- */
  fit();
  var start = 0;
  if (location.hash) {
    var t0 = document.getElementById(location.hash.slice(1));
    if (t0 && all.indexOf(t0) > -1) { start = all.indexOf(t0); }
  }
  cur = start; want = start;
  all[start].classList.add('is-active', 'is-in');
  updateChrome();

  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(function () {
      fit();
      window.setTimeout(fit, 60);
      window.__fontsReady = true;
    });
  } else {
    window.__fontsReady = true;
  }
  window.__deck = {
    fit: fit, show: show, count: all.length,
    active: function () { return all[cur].id; }
  };
}());
"""


# ==========================================================================
def fix_s11_card_height(doc):
    """Isolierte Layoutkorrektur auf Screen 11.

    Der letzte Aufzaehlungspunkt der mittleren Karte („paralleler Vergleich
    statt Umstellung") lief unter die Kartenunterkante. Ursache ist die
    Kartenhoehe von 210 Einheiten: Die fuenf Punkte belegen mit ihren
    Umbruechen rund 295 Einheiten ab Kartenoberkante bei y = 62.

    Korrigiert wird ausschliesslich die Hoehe der drei Karten — Hintergrund
    und farbige Kante — von 210 auf 270. Oberkanten, x-Positionen, Breiten,
    Abstaende, Texte, Textpositionen, Farben und Eckenradien bleiben
    unberuehrt. Zwischen Kartenunterkante (332) und Trennlinie (378) bleiben
    46 Einheiten.
    """
    m = re.search(r'<section[^>]*id="s11".*?</section>', doc, re.S)
    assert m, "Screen s11 nicht gefunden"
    block = m.group(0)
    pat = re.compile(r'(<rect[^>]*\by="62"[^>]*\b)height="210"')
    fixed, n = pat.subn(r'\1height="270"', block)
    assert n == 6, "Erwartet werden 6 Kartenrechtecke, gefunden: %d" % n
    return doc[:m.start()] + fixed + doc[m.end():]


# ==========================================================================
def harmonize_references(doc):
    """Referenzharmonisierung mit dem KI-Strategiepapier KUK v1.1.

    Geaendert werden ausschliesslich Fusszeilen-Referenzen:

      · der Kapitelchip nennt Dokument, Kapitel und Seite der eingefrorenen
        Paginierung der Fassung v1.1,
      · der Aussagenchip wird beschriftet, damit keine Kennung allein steht,
      · jede Quelle in der Quellenzeile erhaelt ihren Quellenschluessel.

    Folieninhalt, Reihenfolge, Grafiken und Bedienung bleiben unberuehrt.
    """
    import sys as _sys
    _sys.path.insert(0, os.path.join(
        "/Users/Ingomar/Desktop/Higher Management/final-clinical-intelligence",
        "shared"))
    import content_core as CC

    # Eingefrorene Paginierung der Fassung v1.1 (siehe v1.1/PAGE_MAP.md)
    seite = {"01": 3, "02": 5, "03": 7, "04": 10, "05": 11, "06": 13, "07": 15,
             "08": 17, "09": 19, "10": 21, "11": 23, "12": 25, "13": 27,
             "14": 28}

    def kapitelchip(m):
        k = m.group(1)
        return ('<span class="chip">KI-STRATEGIEPAPIER KUK · KAP. %s · S. %d</span>'
                % (k, seite[k]))

    doc = re.sub(r'<span class="chip">KAPITEL (\d\d)</span>', kapitelchip, doc)
    doc = re.sub(r'<span class="chip">(S-\d\d(?:, S-\d\d)*)</span>',
                 r'<span class="chip">AUSSAGEN \1</span>', doc)

    # Quellenzeilen: jede bekannte Kurzform bekommt ihren Schluessel voran.
    paare = sorted(((CC.SOURCES[k]["kurz"], CC.QUELLEN_KEYS[k])
                    for k in CC.SOURCES), key=lambda x: -len(x[0]))

    def quellzeile(m):
        inner = m.group(1)
        for kurz, q in paare:
            if kurz in inner and (q + " ·") not in inner:
                inner = inner.replace(kurz, "%s · %s" % (q, kurz), 1)
        return '<span class="foot__src">QUELLEN &nbsp;%s</span>' % inner

    doc = re.sub(r'<span class="foot__src">(.*?)</span>', quellzeile, doc,
                 flags=re.S)
    return doc


# ==========================================================================
def build():
    doc = io.open(SRC, encoding="utf-8").read()

    # --- 1. Bestandteile der Quelle unveraendert entnehmen -------------
    css = re.search(r"<style>(.*?)</style>", doc, re.S).group(1)
    sections = re.findall(r"<section\b[^>]*>.*?</section>", doc, re.S)
    assert len(sections) == 19, "Erwartet werden 19 Screens, gefunden: %d" % len(sections)
    bar = re.search(r'<div class="bar".*?</div>\s*(?=<div class="map")', doc, re.S).group(0)
    mapblk = re.search(r'<div class="map" id="map" hidden>.*?id="mapx"[^>]*>.*?</button>\s*</div>',
                       doc, re.S).group(0)

    # --- 2. Buehne um den Folieninhalt legen, Inhalt unangetastet ------
    staged = []
    for s in sections:
        head = re.match(r"<section\b[^>]*>", s).group(0)
        body = s[len(head):-len("</section>")]
        staged.append(head + '<div class="stage">' + body + "</div></section>")

    # --- 3. Alte Praesentationsschicht aus dem CSS entfernen -----------
    css = re.sub(r"@font-face\s*\{[^}]*\}", "", css)
    css = strip_rules(css, [
        "html", "body", ".screen", ".screen+.screen", ".screen + .screen",
        ".bar", ".bar__b", ".bar__b--w", ".bar__pos", ".bar__pos b",
        ".bar__pos i", ".bar__dots", ".bar__dots button",
        ".bar__dots button:hover", ".bar__dots button.is-on",
        ".map", ".map__in", ".map__x", ".screen--appendix",
        ".screen--title", "*",
    ])
    css = re.sub(r"@media\s*print\s*\{(?:[^{}]|\{[^{}]*\})*\}", "", css)
    # Reflow-Media-Queries entfernen: Die Buehne ist immer 1920 breit. Wuerden
    # sie greifen, brechen sie das Layout nach dem realen Viewport um — genau
    # dieser Effekt liess Folien bei 125 % Zoom aus der Buehne laufen.
    css = re.sub(r"@media\s*\([^)]*max-width[^)]*\)\s*\{(?:[^{}]|\{[^{}]*\})*\}",
                 "", css)
    css = freeze_viewport_units(css)
    css = css.replace("color-mix(in srgb, var(--panel) 90%, transparent)", "#171d24")
    css = css.replace("color-mix(in srgb,var(--panel) 90%,transparent)", "#171d24")
    css = css.replace("color-mix(in srgb, var(--ink) 96%, transparent)", "#0a0d11")
    css = css.replace("color-mix(in srgb,var(--ink) 96%,transparent)", "#0a0d11")

    # --- 4. Steuerleiste mit Schaltflaechen und Beschriftung ------------
    bar = bar.replace('<button class="bar__b" data-step="-1" aria-label="Zurück">',
                      '<button class="bar__b" id="prevb" type="button" aria-label="Vorige Folie">')
    bar = bar.replace('<button class="bar__b" data-step="1" aria-label="Vor">',
                      '<button class="bar__b" id="nextb" type="button" aria-label="Nächste Folie">')
    bar = bar.replace('<button class="bar__b bar__b--w" id="mapbtn">',
                      '<button class="bar__b bar__b--w" id="mapbtn" type="button" '
                      'aria-expanded="false" aria-controls="map">')
    bar = bar.replace('<button class="bar__b bar__b--w" id="fsbtn">',
                      '<button class="bar__b bar__b--w" id="fsbtn" type="button">')
    mapblk = mapblk.replace('<div class="map" id="map" hidden>',
                            '<div class="map" id="map" hidden role="dialog" '
                            'aria-modal="true" aria-label="Folienübersicht" tabindex="-1">')

    title = re.search(r"<title>(.*?)</title>", doc, re.S).group(1)
    desc = re.search(r'<meta name="description" content="([^"]*)"', doc).group(1)

    html = (
        '<!doctype html>\n<html lang="de"><head>\n'
        '<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, '
        'viewport-fit=cover">\n'
        '<title>' + title + '</title>\n'
        '<meta name="author" content="Ingomar Krehan">\n'
        '<meta name="description" content="' + desc + '">\n'
        '<meta name="robots" content="noindex, nofollow, noarchive">\n'
        '<meta name="googlebot" content="noindex, nofollow, noarchive">\n'
        '<meta name="color-scheme" content="dark">\n'
        '<style>\n' + css + "\n" + SHELL_CSS + '\n</style>\n'
        '</head>\n<body class="ci-space">\n'
        '<main id="deck">\n' + "\n".join(staged) + "\n</main>\n\n"
        + bar + "\n" + mapblk + "\n"
        '<script>\n' + SHELL_JS + '\n</script>\n'
        '</body></html>\n'
    )

    html = fix_s11_card_height(html)
    html = harmonize_references(html)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    io.open(OUT, "w", encoding="utf-8").write(html)
    return OUT, hashlib.sha256(html.encode("utf-8")).hexdigest()


if __name__ == "__main__":
    p, h = build()
    print("geschrieben:", os.path.relpath(p, REPO))
    print("SHA-256    :", h)
    print("Groesse    : %d kB" % (os.path.getsize(p) // 1024))
