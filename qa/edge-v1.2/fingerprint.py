# -*- coding: utf-8 -*-
"""Inhaltsfingerabdruck einer Deck-HTML.

Erfasst je .screen den normalisierten sichtbaren Text als SHA-256, dazu
Reihenfolge, IDs und die Anzahl visueller Elemente. Damit laesst sich
beweisen, dass eine Umstellung der Praesentationstechnik den Inhalt
nicht veraendert hat.
"""
import hashlib
import html
import json
import re
import sys
import unicodedata


def screens(doc):
    doc = re.sub(r"<script\b.*?</script>", "", doc, flags=re.S | re.I)
    doc = re.sub(r"<style\b.*?</style>", "", doc, flags=re.S | re.I)
    out = []
    for m in re.finditer(r'<section\b([^>]*)>(.*?)</section>', doc, re.S):
        attrs, body = m.group(1), m.group(2)
        sid = re.search(r'id="([^"]+)"', attrs)
        out.append((sid.group(1) if sid else "?", body))
    return out


def norm(s):
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = unicodedata.normalize("NFC", s)
    return re.sub(r"\s+", " ", s).strip()


def fingerprint(path):
    doc = open(path, encoding="utf-8").read()
    fp = {"datei": path.split("/")[-1], "screens": []}
    for sid, body in screens(doc):
        t = norm(body)
        fp["screens"].append({
            "id": sid,
            "sha256": hashlib.sha256(t.encode("utf-8")).hexdigest(),
            "zeichen": len(t),
            "svg": len(re.findall(r"<svg\b", body)),
            "auszug": t[:70],
        })
    fp["anzahl_screens"] = len(fp["screens"])
    fp["svg_gesamt"] = sum(s["svg"] for s in fp["screens"])
    fp["reihenfolge"] = [s["id"] for s in fp["screens"]]
    fp["gesamt_sha256"] = hashlib.sha256(
        "".join(s["id"] + s["sha256"] for s in fp["screens"]).encode()).hexdigest()
    return fp


if __name__ == "__main__":
    print(json.dumps(fingerprint(sys.argv[1]), ensure_ascii=False, indent=1))
