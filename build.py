#!/usr/bin/env python3
"""Tiny page builder: shared header/footer + page bodies -> site/*.html. Run: python3 build.py"""
import pathlib
R = pathlib.Path(__file__).parent
FRAG = lambda n: (R / "legal" / f"{n}.frag").read_text()

HEAD = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="/assets/icons/favicon.ico">
<link rel="preload" href="/assets/fonts/Inter/Inter-roman-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/style.css">
</head>
<body>
<header class="site-header">
  <a class="brand" href="/"><img src="/assets/images/logo.png" alt="IGK Abwassertechnik" width="120" height="59"></a>
  <input type="checkbox" id="nav-toggle" class="nav-toggle" aria-label="Menü">
  <label for="nav-toggle" class="nav-burger" aria-hidden="true"><span></span></label>
  <nav>
    {nav}
    <a class="btn" href="tel:+4942984 10 42".replace(" ","")>Anrufen</a>
    <a class="btn" href="mailto:vertrieb@igk-abwassertechnik.de">Anfrage</a>
  </nav>
</header>
<main>
""".replace('tel:+4942984 10 42".replace(" ","")', 'tel:+494298410042"')

FOOT = """</main>
<footer class="site-footer">
  <div class="wrap footer-grid">
    <address>
      <strong>IGK Abwassertechnik GmbH</strong><br>
      Goebelstraße 38<br>28865 Lilienthal
    </address>
    <p>
      T <a href="tel:+494298410042">04298 41 0 42</a><br>
      <a href="mailto:info@igk-abwassertechnik.de">info@igk-abwassertechnik.de</a>
    </p>
    <p class="customers">
      <strong>Für Kunden</strong><br>
      <a href="#" target="_blank" rel="noopener">IGK Cloud &#8599;</a><!-- Platzhalter: Cloud-URL folgt (href="#" ersetzen) -->
    </p>
    <p class="social">
      <a href="https://de.linkedin.com/company/igk-abwassertechnik" rel="noopener">LinkedIn</a>
      <a href="https://instagram.com/igk_abwassertechnik" rel="noopener">Instagram</a>
      <a href="https://m.facebook.com/igk.abwassertechnik" rel="noopener">Facebook</a>
    </p>
  </div>
  <div class="wrap legal"><span>&copy; IGK Abwassertechnik GmbH</span><a href="/impressum.html">Impressum</a><a href="/agb.html">AGB</a><a href="/datenschutz.html">Datenschutz</a></div>
</footer>
</body>
</html>
"""

# --- Leistungsstruktur (intern: Bereiche Wasser / Kabelschutzrohre, je Gruppen -> Unterpunkte).
# Gleiche Namen = gleicher Inhalt: der Inhalt steht einmal (LEAF_PAGE / Platzhalter), die Seite wird je Bereich erzeugt, damit Navigation und Einordnung stimmen.
# Nummerierung und Buchstaben aus der Strukturvorlage nur intern, nicht auf der Seite.
LEAF_TITLES = {
    "spezialinspektion-360": "360-Grad-Spezialinspektion", "dreh-schwenkkopf-kamera": "Dreh-/Schwenkkopf-Kamera",
    "panorama-inspektion-360": "360-Grad-Panorama-Inspektion", "drohnenbefliegung": "Drohnenbefliegung",
    "molchung": "Molchung", "hochdruckspuelwagen": "Hochdruckspülwagen", "sehende-duese": "Sehende Düse",
    "wasserhoechstdruckfraesen": "Wasserhöchstdruckfräsen",
    "din-en-1610": "DIN EN 1610", "sonderpruefungen": "Sonderprüfungen", "hochdruckpruefungen": "Hochdruckprüfungen",
    "abscheider-generalinspektion": "Generalinspektion von Abscheidern",
    "rohrkalibrierung": "Kalibrierung", "deformationsmessung": "Deformationsmessung", "seileinzug": "Seileinzug",
    "schlauchliner": "Schlauchliner",
    "kurzliner": "Kurzliner", "edelstahlmanschette": "Edelstahlmanschette", "linerendmanschette": "Linerendmanschette",
    "hutprofil": "Hutprofil", "roboterfraesarbeiten": "Roboterfräsarbeiten",
}
LEAF_ICON = {s: s for s in LEAF_TITLES}  # Icon-Dateiname = Slug, außer:
LEAF_ICON.update({"wasserhoechstdruckfraesen": "reinigung", "rohrkalibrierung": "kalibrierung"})
GROUP_ICON = {"inspektion": "inspektion", "reinigung": "reinigung", "dichtheitspruefung": "messung", "kalibrierung": "kalibrierung", "seileinzug": "seileinzug", "sanierung": "pruefung"}
# Gruppe = (Schlüssel, Titel, Knoten). Knoten: Slug (Seite) oder (Slug-oder-Überschrift, [Knoten]). Knoten None = Gruppe ist selbst die Seite.
AREAS = {
    "wasser": {"title": "Wasser", "what": "Abwasser- und Regenwasserleitungen",
        "lead": "Inspektion, Reinigung, Dichtheitsprüfung, Kalibrierung und Sanierung von Abwasser- und Regenwasserleitungen.",
        "groups": [
            ("inspektion", "Inspektion", ["dreh-schwenkkopf-kamera", "panorama-inspektion-360", "drohnenbefliegung", "spezialinspektion-360"]),
            ("reinigung", "Reinigung", ["hochdruckspuelwagen", "sehende-duese", "molchung", "wasserhoechstdruckfraesen"]),
            ("dichtheitspruefung", "Dichtheitsprüfung", ["din-en-1610", "abscheider-generalinspektion", "hochdruckpruefungen", "sonderpruefungen"]),
            ("kalibrierung", "Kalibrierung", ["deformationsmessung", "rohrkalibrierung"]),
            ("sanierung", "Sanierung", [("Renovation", ["schlauchliner"]),
                                        ("Reparatur", ["kurzliner", "edelstahlmanschette", "linerendmanschette", "hutprofil"]),
                                        ("Robotertätigkeiten", ["roboterfraesarbeiten", "wasserhoechstdruckfraesen"])])]},
    "kabelschutzrohre": {"title": "Kabelschutzrohre", "what": "Kabelschutzrohre und Leerrohre",
        "lead": "Inspektion, Reinigung, Dichtheitsprüfung, Kalibrierung, Seileinzug und Sanierung von Kabelschutzrohren und Leerrohren.",
        "groups": [
            ("inspektion", "Inspektion", ["spezialinspektion-360", "dreh-schwenkkopf-kamera", "panorama-inspektion-360", "drohnenbefliegung"]),
            ("reinigung", "Reinigung", ["molchung", "hochdruckspuelwagen", "wasserhoechstdruckfraesen"]),
            ("dichtheitspruefung", "Dichtheitsprüfung", ["din-en-1610", "sonderpruefungen", "hochdruckpruefungen"]),
            ("kalibrierung", "Kalibrierung", ["rohrkalibrierung", "deformationsmessung"]),
            ("seileinzug", "Seileinzug", None),
            ("sanierung", "Sanierung", [("Renovation", ["schlauchliner"]), ("Reparatur", ["kurzliner", "edelstahlmanschette", "linerendmanschette"]),
                                        ("Robotertätigkeiten", ["roboterfraesarbeiten", "wasserhoechstdruckfraesen"])])]},
}
gp = lambda a, g: f"{a}-{g[0]}"  # Seiten-Slug einer Gruppe (bei Seileinzug: der Seite selbst)
lp = lambda a, s: f"{a}-{s}"      # Seiten-Slug eines Unterpunkts im Bereich a
def leaves(nodes):
    for n in nodes:
        s, kids = (n, None) if isinstance(n, str) else n
        if s in LEAF_TITLES: yield s
        if kids: yield from leaves(kids)
GROUPPAGES = {gp(a, g): (a, g) for a, d in AREAS.items() for g in d["groups"] if g[2] is not None}
CRUMBS = {}  # (Bereich, Unterpunkt) -> [Gruppen]
for a, d in AREAS.items():
    for g in d["groups"]:
        for s in ([g[0]] if g[2] is None else leaves(g[2])):
            CRUMBS.setdefault((a, s), []).append(g)
AREA_TILE = {"wasser": ("wasser", "Abwasser- und Regenwasserleitungen."), "kabelschutzrohre": ("kabelschutzrohre", "Kabelschutzrohre und Leerrohre.")}
cards = '<ul class="cards cards-services cards-two">' + "".join(
    f'<li class="card"><span class="ico"><img src="/assets/icons/{AREA_TILE[a][0]}.svg" alt="" width="40" height="40"></span>'
    f'<h3><a href="/{a}.html">{d["title"]}</a></h3><p>{AREA_TILE[a][1]}</p></li>' for a, d in AREAS.items()) + "</ul>"

TEAM = [
    ("Thorbjoern_Roessner", "Ing. Thorbjörn Rössner", "Geschäftsführender Gesellschafter · Zertifizierter Kanalsanierungsberater", "Kalkulation, Angebotserstellung und Projektleitung Sanierung"),
    ("Christina_Roessner", "Christina Rössner", "Assistenz der Geschäftsführung", "Marketing & Personal"),
    ("Sabine_Oelmeyer", "Sabine Oelmeyer", "Buchhaltung", "Rechnungswesen & kaufmännische Abwicklung"),
    ("Baule", "Frank Baule", "Projektleitung", "Dokumentation & Disposition"),
]
team = "".join(
    f'<li class="person"><img src="/assets/team/{f}.jpg" alt="{n}" loading="lazy"><h3>{n}</h3><p><strong>{r}</strong><br>{d}</p></li>'
    for f, n, r, d in TEAM)

INDEX = f"""<section class="hero">
  <div class="wrap">
    <h1>Rohr-, Kanal- und Kabelschutzrohr-Dienstleistungen für Kommunen, Industrie und Privat</h1>
  </div>
</section>
<section id="leistungen" class="wrap section">
  <h2>Leistungen</h2>
  {cards}
</section>
<section class="section alt">
  <div class="wrap split">
    <div>
      <h2>Gemeinsam unterwegs</h2>
      <p>Damit die Rohre unter unseren Straßen sauber und dicht sind, wird gesaugt, gespült und Kanäle frei gefräst. Zwanzig Jahre sind Holger Plug und Marko Koch bereits im Abwasser-Bereich im Einsatz, für die RTL Nord-Rubrik „Kim kommt rum“ durfte Kim die Abwassertechnik in Stade einen Tag begleiten und mit anpacken.</p>
    </div>
    <figure class="video" id="video">
      <img src="/assets/images/video-poster.jpg" alt="Vorschaubild: Regionalreporterin Kim unterwegs mit der Kanalreinigung in Stade" loading="lazy">
      <button type="button" data-yt="_mxT_luLteM">&#9654; Video abspielen</button>
      <figcaption>Mit einem Klick auf dieses Video akzeptieren Sie den Datenaustausch mit YouTube. Lesen Sie dazu auch unsere <a href="/datenschutz.html">Datenschutzbestimmungen</a>.</figcaption>
    </figure>
  </div>
</section>
<section class="wrap section cta">
  <h2>Karriere bei IGK</h2>
  <p>Werden Sie Teil unseres Teams.</p>
  <a class="btn" href="/karriere.html">Offene Stellen</a>
</section>
<script>
document.querySelector('[data-yt]').addEventListener('click', e => {{
  const f = document.createElement('iframe');
  f.src = 'https://www.youtube-nocookie.com/embed/' + e.target.dataset.yt + '?autoplay=1';
  f.allow = 'autoplay; encrypted-media; picture-in-picture'; f.allowFullscreen = true;
  f.title = 'Regionalreporterin Kim unterwegs mit der Kanalreinigung in Stade';
  document.getElementById('video').replaceChildren(f);
}});
</script>
"""

ANSPRECH = f"""<section class="wrap section">
  <h1>Ansprechpartner</h1>
  <p>Sie erreichen uns unter der Telefonnummer <a href="tel:+494298410042">04298 41 0 42</a> oder per E-Mail an <a href="mailto:info@igk-abwassertechnik.de">info@igk-abwassertechnik.de</a></p>
  <ul class="team">{team}</ul>
</section>
"""

KARRIERE = """<section class="wrap wide section">
  <h1>Karriere</h1>
  <p>Aktuelle Stellenangebote der IGK Abwassertechnik GmbH. Die Bewerbung läuft über unser Karriereportal bei Personio.</p>
  <iframe class="jobs" src="https://igk.jobs.personio.de/?display=de" title="Offene Stellen bei IGK Abwassertechnik" loading="lazy"></iframe>
  <p class="note">Wird die Ansicht nicht geladen? <a href="https://igk.jobs.personio.de/" rel="noopener">Stellenportal in neuem Tab öffnen</a>.</p>
</section>
"""

legal = lambda h, n: f'<section class="wrap section prose">{FRAG(n)}</section>\n'


# --- Rohrtechnik (Kabelschutzrohre): Übersicht + 3 Unterseiten. Struktur und Überschriften wie hexbee.de/rohrtechnik, Texte auf IGK angepasst.
# Entwurf: nicht übernommen wurden Marken/Gerätenamen, Gerätedaten, Referenzprojekt, Haftpflicht/DSGVO-Aussagen, Bilder, Formular. -> README "Open points".
import re
TEL = re.search(r'href="(tel:[^"]+)"', FOOT).group(1)
MAIL = "vertrieb@igk-abwassertechnik.de"  # Anfragen/Angebote
def r_hero(eyebrow, h1, lead, bullets, active, cta, how=None):
    li = "".join(f"<li>{x}</li>" for x in bullets)
    how = f' <a class="btn ghost" href="#{how}">So läuft es ab</a>' if how else ""
    return (SNAVM
            + f'<section class="hero"><div class="wrap"><p class="eyebrow">{eyebrow}</p><h1>{h1}</h1><p>{lead}</p>'
            f'<p><a class="btn" href="#anfrage">{cta}</a>{how}</p></div></section>\n'
            f'<section class="section ticks-sec"><div class="wrap prose"><ul class="ticks">{li}</ul></div></section>\n')

def sec(h2, body, alt=False, eyebrow="", id=""):
    i = f' id="{id}"' if id else ""
    e = f'<p class="eyebrow">{eyebrow}</p>' if eyebrow else ""
    return f'<section class="section{" alt" if alt else ""}"{i}><div class="wrap prose">\n{e}<h2>{h2}</h2>\n{body}\n</div></section>\n'

def ul(items): return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"
def steps(items): return '<ol class="steps">' + "".join(f"<li><h3>{h}</h3><p>{d}</p></li>" for h, d in items) + "</ol>"
def tbl(head, rows, cap=""):
    return ("<div class=\"tbl\"><table><thead><tr>" + "".join(f"<th>{c}</th>" for c in head) + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table></div>"
            + (f'<p class="note">{cap}</p>' if cap else ""))
def faq(items): return "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in items)
def cta_band(h2, text, btn):
    return ""  # Anfrage-Bänder entfallen (Anfrage über Button im Header)
    return (f'<section class="section"><div class="wrap prose"><h2>{h2}</h2><p>{text}</p>'
            f'<p><a class="btn" href="#anfrage">{btn}</a> <a class="btn" href="{TEL}">04298 41 0 42</a></p></div></section>\n')
def request(h2, intro, needs, note):
    return (f'<section class="section alt" id="anfrage"><div class="wrap prose"><p class="eyebrow">Anfrage</p><h2>{h2}</h2>\n<p>{intro}</p>\n<h3>Für ein Angebot brauchen wir</h3>\n'
            + ul(needs) + f'\n<p>{note} <a href="mailto:{MAIL}">{MAIL}</a>.</p>\n'
            f'<p><a class="btn" href="{TEL}">04298 41 0 42</a> <a class="btn" href="mailto:{MAIL}">E-Mail schreiben</a></p>\n</div></section>\n')

def _a(href, text, cur=False): return f'<a href="{href}"' + (' aria-current="page"' if cur else "") + f">{text}</a>"
SNAVM = "<!--SNAV-->"  # Platzhalter: wird je Seite durch snav() ersetzt
def snav(a, g=None, leaf=None):  # überall im Bereich gleich: Bereich + alle Gruppen; aktuelle Gruppe(n) markiert
    d = AREAS[a]
    here = [g] if g else (CRUMBS.get((a, leaf), []) if leaf else [])
    items = [_a(f"/{a}.html", d["title"], g is None and leaf is None)]
    for x in d["groups"]:
        cur = any(x is y for y in here)
        items.append(f'<a href="/{gp(a, x)}.html"' + (' aria-current="page"' if cur and (g is x or x[2] is None) else ' aria-current="true"' if cur else "") + f">{x[1]}</a>")
    return f'<div class="subnav" role="navigation" aria-label="Einordnung"><div class="wrap">{"".join(items)}</div></div>\n'

def tile(href, ico, title): return f'<li class="card"><span class="ico"><img src="/assets/icons/{ico}.svg" alt="" width="40" height="40"></span><h3><a href="{href}">{title}</a></h3></li>'
def grid(tiles):
    tiles = list(tiles)
    return f'<ul class="cards cards-services{" c2" if len(tiles) in (2, 4) else ""}">{"".join(tiles)}</ul>'
def area_cards(a):  # Ebene 2: nur die Überschriften der Gruppen
    d = AREAS[a]
    return sec(f"Leistungen im Bereich {d['title']}", grid(tile(f"/{gp(a, g)}.html", GROUP_ICON[g[0]], g[1]) for g in d["groups"]))
def group_body(a, g):  # Ebene 3: alle Unterpunkte der Gruppe in einem Raster (ohne Zwischenüberschriften)
    return sec("Leistungen", grid(tile(f"/{lp(a, s)}.html", LEAF_ICON[s], LEAF_TITLES[s]) for s in leaves(g[2])))

def contact(h2):
    return (f'<section class="section alt" id="anfrage"><div class="wrap prose"><p class="eyebrow">Anfrage</p><h2>{h2}</h2>\n<p>Schreiben Sie uns oder rufen Sie an.</p>\n'
            f'<p><a class="btn" href="{TEL}">04298 41 0 42</a> <a class="btn" href="mailto:{MAIL}">E-Mail schreiben</a></p>\n</div></section>\n')

NEEDS = ["Rohrwerkstoff, Außendurchmesser und Wanddicke oder SDR", "Anzahl und Länge der Rohrzüge",
         "bei Kalibrierung das gewünschte Kalibermaß oder die vorgesehene Belegung", "bei Druckprüfung Prüfverfahren und Prüfdruck, falls vorgegeben",
         "bei Seileinzug Seilart und Durchmesser, falls vorgegeben", "Ort und geplanter Zeitraum", "ob die Trasse abschnittsweise freigegeben wird"]
NOTE = "Wenn ein Leistungsverzeichnis vorliegt, reicht der Auszug mit den betreffenden Positionen. Schicken Sie ihn per E-Mail an"
REQ = lambda h2: request(h2, "Wir melden uns mit Rückfragen oder mit Machbarkeit und Angebot.", NEEDS, NOTE)

ORDER = steps([
    ("Reinigen", "Schaumstoffmolch mit Druckluft, so oft, bis er sauber austritt. Ohne Wasser, damit das Rohr trocken bleibt."),
    ("Dichtheitsprüfung", 'Dichtheitsprüfung mit Luft, Prüfverfahren und Prüfdruck nach Vorgabe des Auftraggebers. <a href="/L/din-en-1610.html">Zur Dichtheitsprüfung</a>'),
    ("Kalibrieren", 'Kalibrierdorn mit Treibmolch, Nachweis der Profilfreiheit nach vereinbartem Kalibermaß. <a href="/L/rohrkalibrierung.html">Zur Kalibrierung</a>'),
    ("Seileinzug", "Zugseil am Treibmolch, im selben Durchgang wie die Kalibrierung. Beide Enden gekennzeichnet."),
    ("Inspektion", 'Optional, wenn sichtbar werden soll, wie das Rohr innen aussieht. <a href="/L/dreh-schwenkkopf-kamera.html">Zur Inspektion</a>'),
])
ORDER_TXT = ("<p>Gereinigt wird zuerst. Ein Dorn, der an einem Sandpolster stehen bleibt, liefert einen Befund, der keiner ist, und eine Blase dichtet auf Sediment nicht ab.</p>"
    "<p>Die Einbauanleitung A 535b des Kunststoffrohrverbands sieht die Kalibrierung „nach Abschluss der Dichtheitsprüfung“ vor. Das Zugseil ziehen wir ebenfalls erst nach der Druckprüfung ein, weil ein Seil im Rohr die Abdichtung der Prüfblase stören würde.</p>"
    "<p>Verlangt Ihr Leistungsverzeichnis, vor der Druckprüfung zu kalibrieren, laufen Kalibrierung und Seileinzug in getrennten Durchgängen.</p>")
NOT = lambda keine: (f"<h3>Keine Aussage zu</h3>{ul(keine)}"
    "<p>Die Kalibrierung weist den freien Querschnitt nach.</p><p>Ob das Rohr dicht ist, zeigt die Druckprüfung.</p><p>Die Molchreinigung trägt Material aus, bis der Molch sauber austritt.</p><p><strong>Keine dieser Leistungen ersetzt eine der anderen.</strong></p>")
CAM = '<a href="/L/dreh-schwenkkopf-kamera.html">Inspektion</a>'
EYE = "Kabelschutzrohre · Leerrohranlagen"
NR = ("<h3>Rohrnummerierung</h3><p>Vor Arbeitsbeginn legen wir mit Ihnen fest, wie die Rohre an beiden Enden des Rohrzugs nummeriert werden, mit Blickrichtung und Nullpunkt.</p>")

RT_UEBERSICHT = (
    r_hero(EYE, "Rohrservice an Kabelschutzrohren", "Molchreinigung, Druckprüfung, Kalibrierung und Seileinzug vor dem Kabelzug.",
           ["Protokoll je Rohrzug", "Zugseil im selben Durchgang wie die Kalibrierung", "Inspektion auf Wunsch"], "kabelschutzrohre", "Rohrservice anfragen")
    + area_cards("kabelschutzrohre")
    + sec("Vier Leistungen am Rohrzug", "<p>Wir reinigen Kabelschutzrohre und Leerrohre, prüfen sie mit Luft auf Dichtheit, weisen die Profilfreiheit nach und ziehen das Zugseil ein. Einzeln oder im selben Einsatz, mit Protokoll je Rohrzug.</p>" + ORDER + ORDER_TXT)
    + sec("Was welche Leistung nachweist", "<p>Die Kalibrierung weist den freien Querschnitt nach.</p><p>Ob das Rohr dicht ist, zeigt die Druckprüfung.</p><p>Die Molchreinigung trägt Material aus, bis der Molch sauber austritt.</p><p><strong>Keine dieser Leistungen ersetzt eine der anderen.</strong></p>", alt=True)
    + f'<section class="section alt" id="anfrage"><div class="wrap prose"><p class="eyebrow">Anfrage</p><h2>Rohrservice anfragen</h2>\n<p>Schreiben Sie uns per E-Mail: <a class="btn" href="mailto:vertrieb@igk-abwassertechnik.de">vertrieb@igk-abwassertechnik.de</a></p>\n</div></section>\n')

RT_DRUCK = (
    r_hero("Rohre · Leitungen · Kanäle", "Druckprüfung von Rohrleitungen", "Dichtheitsprüfung mit Luft nach DIN EN 1610, mit aufgezeichnetem Druckverlauf.",
           ["Verfahren LC oder LD nach DIN EN 1610", "Druckverlauf aufgezeichnet", "Protokoll je Prüfabschnitt"], "din-en-1610", "Druckprüfung anfragen", how="verfahren")
    + sec("Wann druckgeprüft wird", "<p>Ein Rohr oder Kanal soll dicht sein, bevor es in Betrieb geht. Durch eine undichte Muffe oder Verbindung können Wasser und Boden ein- oder austreten. Die Druckprüfung zeigt, ob die Leitung dicht ist, und das Ergebnis steht je Prüfabschnitt im Protokoll.</p>"
        + tbl(["Anlass", "Warum"], [
            ["Nach der Verlegung, vor dem Verfüllen des Grabens", "Die Prüfung erfolgt abschnittsweise, die Muffen und Verbindungen sind dann noch zugänglich."],
            ["Als Abnahmeprüfung nach dem Verfüllen", "Nachweis an der fertigen Leitung, bevor die Anlage übergeben wird."],
            ["Vor der Inbetriebnahme oder vor dem Kabeleinzug", "Nachweis, dass die Leitung dicht ist und kein Wasser und kein Boden eindringen können."],
            ["Bei Übernahme einer fremd verlegten Anlage", "Ein Nachweis durch Dritte vor der Abnahme."],
            ["Bei Bestandsleitungen vor einer Neunutzung oder Neubelegung", "Der Zustand ist unbekannt."]]), eyebrow="Anlässe")
    + sec("Rohrzug verschließen, Luft aufbringen, Druckverlauf messen",
        "<p>Wir verschließen die Leitung an beiden Enden, bringen Luft auf den vereinbarten Prüfdruck und messen den Druck über die festgelegte Prüfzeit. Bleibt der Druckabfall unter dem zulässigen Wert, ist der Prüfabschnitt dicht.</p>"
        "<p>Geprüft wird nach <strong>DIN EN 1610</strong>, in der Regel mit Verfahren LC oder LD, sonst nach der Vorgabe in Ihrem Leistungsverzeichnis. Ein elektronisches Prüfgerät zeichnet den Druckverlauf auf und erstellt das Protokoll.</p>"
        + steps([("Prüfabschnitt und Prüfvorgabe festlegen", "In der Regel ein Rohrzug von Schacht zu Schacht. Prüfverfahren und Prüfdruck lassen wir uns vor dem ersten Prüfabschnitt schriftlich bestätigen."),
                 ("Leitung reinigen", "Ist die Leitung nicht gereinigt, reinigen wir sie vorher, bei Kabelschutzrohren durch Molchen."),
                 ("Beide Enden verschließen", "Mit Prüfblasen oder mechanischen Rohrverschlüssen, passend zum Innendurchmesser und zum Prüfdruck."),
                 ("Anfangsdruck aufbringen", "Etwa zehn Prozent über dem Prüfdruck. Die Prüfzeit beginnt erst, wenn der Druck gleichmäßig verläuft."),
                 ("Prüfzeit messen", "Auf Prüfdruck absenken, die Prüfzeit nach Norm einhalten, den Druckabfall mit dem zulässigen Wert vergleichen.")])
        + "<h3>Wenn der Druck stärker abfällt als zulässig</h3><p>Zuerst prüfen wir Verschlüsse und Anschlüsse und wiederholen die Prüfung. Bleibt der Druckabfall zu hoch, wird der Prüfabschnitt als nicht bestanden dokumentiert und Ihnen gemeldet.</p>"
        f"<p>Ob an Muffen oder Rohrwand ein sichtbarer Schaden vorliegt, zeigt eine {CAM}.</p>", alt=True, eyebrow="Verfahren", id="verfahren")
    + sec("Ein Protokoll je Prüfabschnitt, mit Druckverlauf",
        "<p>Das Protokoll ist eine Grundlage für Abnahme und Freigabe. Was das Prüfgerät nicht ausgibt, ergänzen wir auf einem Deckblatt.</p><h3>Im Protokoll steht</h3>"
        + ul(["Protokollnummer, ausführender Betrieb, Baustelle, Auftraggeber, Bauleiter und Prüfer", "Prüfart (Vorprüfung oder Abnahmeprüfung), Prüfverfahren und Prüfdruck",
              "Rohrwerkstoff, Rohrtyp, Rohrkennung, Länge, Start- und Zielschacht", "Messgerät mit Messbereich, Seriennummer und Kalibrierdatum",
              "Beginn und Ende der Prüfung, Dauer von Beruhigungszeit und Prüfzeit", "Druck nach Beruhigungszeit und nach Prüfzeit, zulässiger und gemessener Druckabfall",
              "Ergebnis und Druckverlauf", "Unterschrift"]) + NR, eyebrow="Ergebnis")
    + cta_band("Für die Anfrage genügen die Rohrdaten", "Prüfvorgabe, Zugang zu den Rohrenden und Freigabe der Trasse klären wir danach mit Ihnen.", "Druckprüfung anfragen")
    + sec("Prüfdruck und zulässiger Druckabfall",
        "<p>DIN EN 1610 kennt vier Verfahren für die Prüfung mit Luft. Sie unterscheiden sich im Prüfdruck und im zulässigen Druckabfall, die Prüfzeit hängt außerdem vom Durchmesser ab. Geprüft wird nach den Vorgaben Ihres Leistungsverzeichnisses, ohne Vorgabe in der Regel nach LC oder LD.</p>"
        "<p><strong>Bei Kabelschutzrohren</strong> nennen die Einbauanleitungen <strong>A 535a</strong> und <strong>A 535b</strong> des Kunststoffrohrverbands einen Prüfdruck von 200 mbar mit Luft, die Einbauanleitung des Rohrherstellers Schöngen dazu einen zulässigen Druckabfall von 15 mbar. Das entspricht <strong>Verfahren LD</strong>.</p>"
        + tbl(["Verfahren", "Prüfdruck", "zulässiger Druckabfall", "Prüfzeit"], [["LA", "10 mbar", "2,5 mbar", "5 min"], ["LB", "50 mbar", "10 mbar", "4 min"], ["LC", "100 mbar", "15 mbar", "3 min"], ["LD", "200 mbar", "15 mbar", "1,5 min"]],
              "Luftprüfung nach DIN EN 1610, Prüfzeiten für DN 100 bis DN 200. Prüfzeiten für Rohre aus Kunststoff. Für andere Durchmesser gelten die Werte nach Tabelle 3 der Norm.")
        + "<p>Die Baufachlichen Richtlinien Abwasser des Bundes weisen darauf hin, dass die hohe Messempfindlichkeit von LA und LB bei Störungen von außen zu Messungenauigkeiten führen kann. Sie empfehlen für die Prüfung mit Luft ausschließlich LC oder LD.</p>", alt=True, eyebrow="Prüfverfahren")
    + sec("Was die Druckprüfung nachweist und was nicht", NOT(["freiem Querschnitt und Verformung", "Sauberkeit des Rohres", "Lage einer Undichtheit", "Lagegenauigkeit des Rohres", "Werkstoffzustand"]), eyebrow="Abgrenzung")
    + sec("Bei Kabelschutzrohren: In dieser Reihenfolge arbeiten wir", ORDER + ORDER_TXT, alt=True, eyebrow="Reihenfolge")
    + sec("Was Sie bereitstellen", "<p>Damit der Termin hält, muss vorab Folgendes geklärt sein.</p>" + ul([
        "Prüfverfahren und Prüfdruck vorgegeben oder freigegeben", "Rohrwerkstoff, Nennweite bzw. Außendurchmesser und Wanddicke bekannt",
        "Angabe, ob vor dem Verfüllen oder als Abnahmeprüfung nach dem Verfüllen geprüft wird", "Leitung gereinigt, oder die Reinigung ist mitbeauftragt",
        "Leitungsenden bzw. Schächte an beiden Seiten zugänglich, offen und entgratet", "befahrbare Aufstellfläche für die Luftversorgung am Startende",
        "eindeutige Rohrnummerierung an beiden Enden, oder die Kennzeichnung ist mitbeauftragt", "Ihre Freigabe, falls in Schächte eingestiegen werden muss"]), eyebrow="Voraussetzungen")
    + sec("Leistungsverzeichnis und Vergabe", "<p>Leistungsverzeichnisse verweisen für die Dichtheitsprüfung meist auf DIN EN 1610. Im STLB-Bau steht eine Position dazu im Leistungsbereich 009 Entwässerungskanalarbeiten, Abrechnungseinheit ist der Meter.</p>", alt=True, eyebrow="Für Ausschreibende")
    + sec("Fragen zur Druckprüfung", faq([
        ("Welches Prüfverfahren ist das richtige?", "Das, was Ihr Leistungsverzeichnis vorgibt. Bei Kabelschutzrohren nennen die Einbauanleitungen 200 mbar Prüfdruck bei 15 mbar zulässigem Druckabfall, das entspricht Verfahren LD. Ohne Vorgabe prüfen wir nach LC oder LD."),
        ("Gilt DIN EN 1610 auch für Kabelschutzrohre?", "Formal nicht, sie ist eine Abwassernorm. Die Rohrhersteller verweisen in ihren Einbauanleitungen für Kabelschutzrohre trotzdem auf sie. Wir prüfen mit den Parametern dieser Norm, sofern Sie nichts anderes vorgeben."),
        ("Wird die Prüfung auch bezahlt, wenn die Leitung undicht ist?", "Ja. Vergütet wird die Prüfung, unabhängig vom Ergebnis."),
        ("Können wir das nicht selbst prüfen?", "Können Sie. Dann prüft allerdings derjenige, der verlegt hat, sein eigenes Werk. Wir halten das Ergebnis je Prüfabschnitt im Protokoll fest, mit Druckverlauf.")]), eyebrow="Häufige Fragen")
    + REQ("Druckprüfung anfragen"))

RT_KALIB = (
    r_hero(EYE, "Kalibrierung von Kabelschutzrohren", "Nachweis der Profilfreiheit vor dem Kabelzug, nach vereinbartem Kalibermaß.",
           ["Kalibermaß nach Vorgabe des Auftraggebers", "Protokoll je Rohrzug", "Zugseil auf Wunsch im selben Durchgang"], "kalibrierung", "Kalibrierung anfragen", how="verfahren")
    + sec("Wann kalibriert wird", "<p>Nach dem Verlegen und Verfüllen kann ein Rohr verformt sein, eine Muffe verschoben oder Material im Rohr festsitzen. Die Kalibrierung weist nach, dass der freie Querschnitt über die ganze Länge mindestens dem vereinbarten Maß entspricht. Das Ergebnis steht je Rohrzug im Protokoll, bevor das Kabel kommt.</p>"
        + tbl(["Anlass", "Warum"], [
            ["Nach Verlegung und Verfüllung der Leerrohranlage", "Bodenverdichtung kann das Rohr verformen oder die Muffen verschieben."],
            ["Vor dem Kabeleinzug oder Kabeleinblasen", "Nachweis, dass der Querschnitt im Kalibermaß für das vorgesehene Kabel frei ist."],
            ["Nach einer Spülbohrung oder Querung", "Die Zugkräfte beim Einziehen des Rohres können es ovalisieren."],
            ["Bei Übernahme einer fremd verlegten Anlage", "Ein Nachweis durch Dritte vor der Abnahme."],
            ["Bei Bestandsrohren vor einer Neubelegung", "Der Zustand ist unbekannt."]]), eyebrow="Anlässe")
    + sec("Kalibrierdorn mit Treibmolch, geschoben mit Druckluft",
        "<p>Wir führen einen Kalibrierdorn aus Polyamid mit festem Durchmesser durch den Rohrzug. Der Dorn liegt lose im Rohr und dichtet nicht ab, deshalb läuft hinter ihm ein beschichteter Treibmolch, den die Druckluft schiebt. Kommt der Dorn am anderen Ende an, ist die Profilfreiheit nachgewiesen.</p>"
        "<p>Wir kalibrieren Kabelschutzrohre und Leerrohre aus PE-HD, PVC-U und PP. Dorn und Treibmolch wählen wir passend zu Innendurchmesser und Kalibermaß.</p>"
        + steps([("Kalibermaß festlegen", "Schriftlich und vor dem ersten Durchgang."), ("Rohrzug reinigen", "Ist der Rohrzug nicht gereinigt, molchen wir ihn vor dem Kalibrieren."),
                 ("Dorn und Treibmolch koppeln", "Der Dorn läuft vorn, der Treibmolch dahinter. Soll ein Zugseil eingezogen werden, hängt es am Treibmolch."),
                 ("Mit Druckluft einschießen", "Wir bauen den Druck langsam auf. Steigt er weiter und tritt am Zielende keine Luft aus, steckt der Dorn, und wir brechen ab."),
                 ("Dorn am Zielende prüfen", "Riefen oder Abrieb am Dorn halten wir im Protokoll als Hinweis fest. Das Ergebnis bleibt durchgängig, der Hinweis zeigt aber, dass der Dorn unterwegs angelegen hat.")])
        + f"<h3>Wenn der Dorn nicht durchkommt</h3><p>Bleibt der Dorn stecken, lassen wir den Druck ab und erhöhen ihn nicht. Der Rohrzug wird als nicht durchgängig dokumentiert und Ihnen gemeldet, das weitere Vorgehen stimmen wir mit Ihnen ab.</p><p>Woran es liegt, zeigt eine {CAM}.</p>", alt=True, eyebrow="Verfahren", id="verfahren")
    + sec("Ein Protokoll je Rohrzug, mit eindeutiger Aussage",
        "<p>Das Protokoll ist eine Grundlage für die Freigabe zum Kabelzug. Deshalb steht darin, ob der Rohrzug durchgängig ist oder nicht.</p><h3>Im Protokoll steht</h3>"
        + ul(["Bauvorhaben, Auftraggeber, ausführender Betrieb, Datum, Uhrzeit und Bearbeiter", "Rohrkennung nach dem vereinbarten Schema, Anfang und Ende des Abschnitts, Länge laut Unterlagen des Auftraggebers",
              "Werkstoff, Außendurchmesser, Wanddicke und Innendurchmesser", "Kalibermaß, Kaliberlänge und Anteil am Innendurchmesser", "Verfahren (Druckluft mit Treibmolch)",
              "Ergebnis und Zustand des Dorns nach dem Durchgang", "bei Seileinzug Seilart, eingezogene Länge und Kennzeichnung beider Enden", "Unterschrift"]) + NR, eyebrow="Ergebnis")
    + cta_band("Für die Anfrage genügen die Rohrdaten", "Was für das Angebot noch fehlt, etwa Zugang zu den Rohrenden und Freigabe der Trasse, klären wir danach mit Ihnen.", "Kalibrierung anfragen")
    + sec("Das Kalibermaß ist eine Vereinbarung",
        "<p>Das Kalibermaß richtet sich nach dem Kabel, das später eingezogen wird. Die Einbauanleitung <strong>A 535b</strong> des Kunststoffrohrverbands für PE-HD-Kabelschutzrohre der Telekommunikation nennt dafür keine Zahl. Sie verlangt, das Kaliber „in Abhängigkeit der vorgesehenen Belegung des Kabelschutzrohres mit dem Auftraggeber abzustimmen“. Fast wortgleich steht das in der Einbauanleitung des Rohrherstellers Schöngen für Kabelschutzrohre aus PVC-U, PE-HD und PP.</p>"
        "<p>Die Handreichung des Bundesministeriums für Digitales und Verkehr zur Qualitätssicherung beim Glasfaserausbau nennt rund <strong>85 Prozent</strong> des Rohrinnendurchmessers. Ist die <strong>ZTV TK Netz 40</strong> oder ein anderes Regelwerk Vertragsgrundlage, gilt das Maß aus Ihren Vertragsunterlagen.</p>"
        "<p>Das Maß entscheidet, was als Befund gilt. Bei 141 mm Innendurchmesser liegen zwischen einem Kaliber von 80 und einem von 90 Prozent rund 14 mm. Das Maß, mit dem wir rechnen, steht deshalb im Angebot.</p>"
        + tbl(["Außen-Ø × Wand", "Innen-Ø", "80 %", "85 %", "90 %"], [["110 × 3,2", "103,6", "82,9", "88,1", "93,2"], ["110 × 5,3", "99,4", "79,5", "84,5", "89,5"], ["110 × 10,0", "90,0", "72,0", "76,5", "81,0"],
              ["160 × 9,5", "141,0", "112,8", "119,9", "126,9"], ["200 × 9,6", "180,8", "144,6", "153,7", "162,7"], ["225 × 10,8", "203,4", "162,7", "172,9", "183,1"], ["250 × 12,5", "225,0", "180,0", "191,3", "202,5"]],
              "Rechenbeispiele, alle Maße in mm. Kalibermaße auf 0,1 mm gerundet."), alt=True, eyebrow="Kalibermaß")
    + sec("Was die Kalibrierung nachweist und was nicht", NOT(["Dichtheit", "Lagegenauigkeit des Rohres", "Biegeradien der Trasse und Zugkräfte beim späteren Kabelzug", "Werkstoffzustand", "Ablagerungen, an denen der Dorn vorbeikommt", "Lage und Aussehen einer Engstelle"]), eyebrow="Abgrenzung")
    + sec("In dieser Reihenfolge arbeiten wir", ORDER + ORDER_TXT, alt=True, eyebrow="Reihenfolge")
    + sec("Was Sie bereitstellen", "<p>Damit der Termin hält, muss vorab Folgendes geklärt sein.</p>" + ul([
        "Kalibermaß schriftlich vorgegeben oder freigegeben", "Rohrwerkstoff und Innendurchmesser bekannt, aus Außendurchmesser und Wanddicke oder aus dem Datenblatt",
        "Rohrzug gereinigt, oder die Reinigung ist mitbeauftragt", "Rohrenden an beiden Seiten zugänglich und offen", "befahrbare Aufstellfläche für unseren Kompressor am Startende",
        "eindeutige Rohrnummerierung an beiden Enden, oder die Kennzeichnung ist mitbeauftragt", "Ihre Freigabe, falls in Schächte eingestiegen werden muss"]), eyebrow="Voraussetzungen")
    + sec("Leistungsverzeichnis und Vergabe",
        "<p>Die Leistung fällt unter die Position „Kalibrieren – Kabelkanalanlagen“ im <strong>STLB-Bau</strong> (Ausgabe 2026-04), Leistungsbereich 051 Kabelleitungstiefbauarbeiten, Kennung 3711. Als Beispieltext nennt die Position „Kalibrieren der Kabelkanalanlage zur Beurteilung der Profilfreiheit, mit Kalibermolch, Kabelschutzrohr aus PVC-U, DN 100, Zugang vom Schacht“. Abrechnungseinheit ist der Meter.</p>"
        "<p>Der Beispieltext nennt kein Kalibermaß, es sollte deshalb in der Leistungsbeschreibung ausdrücklich festgelegt sein.</p>"
        "<p>Die <strong>ATV DIN 18322</strong> führt in Abschnitt 4.2 das „Kalibrieren und Reinigen bestehender Rohrstrecken“ als Besondere Leistung. Das Kalibrieren sollte deshalb als eigene Position ausgeschrieben sein.</p>", alt=True, eyebrow="Für Ausschreibende")
    + sec("Fragen zur Kalibrierung", faq([
        ("Welches Kalibermaß gilt?", "Das, was mit dem Auftraggeber vereinbart wird. Die Einbauanleitung A 535b des Kunststoffrohrverbands und die des Rohrherstellers Schöngen nennen kein festes Maß, sie verlangen eine Abstimmung nach der vorgesehenen Belegung. Die Handreichung des Bundesministeriums für Digitales und Verkehr zur Qualitätssicherung beim Glasfaserausbau nennt rund 85 Prozent des Rohrinnendurchmessers."),
        ("Ersetzt die Kalibrierung eine Kamerabefahrung?", "Nein. Die Kalibrierung sagt, ob ein Körper mit dem vereinbarten Durchmesser durch den Rohrzug kommt. Wo eine Engstelle liegt und wie sie aussieht, zeigt erst die Kamerabefahrung. Die Dichtheit weist keine der beiden nach, dafür ist die Druckprüfung da."),
        ("Können wir das nicht selbst prüfen?", "Können Sie. Dann prüft allerdings derjenige, der verlegt hat, sein eigenes Werk. Wir halten das Ergebnis je Rohrzug im Protokoll fest."),
        ("Kann das Zugseil im selben Durchgang eingezogen werden?", "Ja, auf Wunsch. Das Seil hängt am Treibmolch hinter dem Dorn, beide Enden werden gesichert und mit der Rohrnummer gekennzeichnet. Seilart und Durchmesser richten sich nach Ihrer Vorgabe. Soll der Rohrzug auch druckgeprüft werden, machen wir die Druckprüfung vorher.")]), eyebrow="Häufige Fragen")
    + REQ("Kalibrierung anfragen"))

RT_KAMERA = (
    r_hero("Optische Inline-Inspektion · Rohre & Leitungen", "Inspektion",
           "<strong>Das ganze Rohr gesehen. Vom ersten bis zum letzten Meter.</strong> Wir befahren Rohre und Leitungen optisch. Vor dem Kabeleinzug als lückenloser Nachweis über die ganze Innenfläche. Nach einer auffälligen Druckprüfung als gezielte Ursachensuche, bei der wir die auffällige Stelle anfahren, statt die Trasse aufzugraben.",
           ["Befund metergenau verortet", "Live-Bild, Bewertung direkt vor Ort"], "dreh-schwenkkopf-kamera", "Leitung prüfen lassen", how="ablauf")
    + sec("Zwei Fragen, für die wir ins Rohr fahren.",
        "<p>Der eine Auftrag ist geplant, der andere kommt, wenn etwas nicht stimmt.</p>"
        '<ul class="cards"><li class="card"><p class="eyebrow">Nachweis</p><h3>Ist die Leitung in Ordnung?</h3><p>Vor dem Kabeleinzug, vor der Inbetriebnahme, für die Abnahme.</p><p>Wir fahren die komplette Länge ab und dokumentieren die Innenwand, so dass jede Schweißnaht und jede Auffälligkeit metergenau auffindbar bleibt.</p><p><strong>Lückenloser Sicht-Nachweis über die ganze Trasse</strong></p></li>'
        '<li class="card"><p class="eyebrow">Diagnose</p><h3>Warum hält die Leitung den Druck nicht?</h3><p>Nach einer auffälligen Druck- oder Dichtheitsprüfung.</p><p>Die Kamera fährt zentriert durch die Leitung, das Bild kommt live an die Oberfläche. Auffällige Stellen fahren wir gezielt an, bis der Befund eindeutig ist: eine nicht vollständig gesteckte Steckmuffe, stehendes Wasser, eingeschwemmtes Material.</p><p><strong>Lokalisierter Befund statt Aufgrabung auf Verdacht</strong></p></li></ul>', eyebrow="Zwei Anlässe")
    + sec("Lange Rohre kann man von innen nicht sehen. Bisher endete die Suche am Spaten.",
        "<p>Ob vor dem Kabeleinzug, vor der Inbetriebnahme oder bei der Zustandsbewertung: Sobald ein Rohr lang und eng ist, endet die Sichtprüfung. Kalibermolch und Druckprüfung sagen, <em>ob</em> der Querschnitt passt. Sie zeigen nicht, <strong>was</strong> und <strong>wo</strong> ein Problem sitzt.</p>"
        + steps([("Blind vor dem teuersten Schritt", "Kabeleinzug, Inbetriebnahme, Trägerstrang-Einzug: Jeder dieser Schritte ist teuer und schwer rückgängig zu machen. Ohne optische Prüfung passiert er ins Ungewisse."),
                 ("Die Prüfung sagt nur „undicht“", "Zeigt die Druck- oder Dichtheitsprüfung einen Abfall, steht der Befund fest, die Ursache nicht. Ohne Blick ins Rohr bleibt nur, den Abschnitt einzugrenzen und auf Verdacht aufzugraben.")])
        + "<h3>Aufgraben auf Verdacht ist teurer als einmal hineinzuschauen.</h3><p>Eine nachträgliche Aufgrabung, ein verkeiltes Kabel, eine undichte Verbindung nach der Inbetriebnahme: Der Blick ins Rohr kostet einen Bruchteil davon, vorher als Nachweis, hinterher als Diagnose.</p>", alt=True, eyebrow="Das Problem")
    + sec("Von der Befahrung zum Dossier.", steps([
        ("Befahrung", "Die Kamera wird mit der Seilwinde durch das Rohr gezogen. Für die Ursachensuche läuft das Bild live mit."),
        ("Aufnahme", "Die Kameras filmen durchgehend, LED-beleuchtet. Die Position kommt vom Weggeber. Wo die Schweißnähte im Rohr gekennzeichnet sind, dienen sie als zusätzlicher Kontrollpunkt."),
        ("Übergabe", "Sie erhalten die Aufnahmen als prüf- und teilbare Dokumentation, jede Auffälligkeit mit Positionsangabe, zur Weitergabe an Bauleitung und Auftraggeber.")]), eyebrow="Ablauf", id="ablauf")
    + sec("Die Prüfung sagt Ihnen, dass etwas nicht dicht ist. Sie sagt Ihnen nicht, wo.",
        "<p>Eine auffällige Druck- oder Dichtheitsprüfung liefert eine Zahl. Sie liefert keine Position und keine Ursache. Bleibt es beim Befund „undicht“, steht die Bauleitung vor der Frage, an welcher der vielen Steckmuffen sie den Bagger ansetzt. Genau diese Lücke schließen wir, mit einem Blick von innen, bevor der erste Meter geöffnet wird.</p>"
        + steps([("Einmal zentriert durch.", "Der Kamerakopf wird an der Winde durch die gesamte Leitung gezogen. Das Bild läuft live an der Oberfläche mit, auffällige Abschnitte werden im selben Moment markiert."),
                 ("Dann gezielt anschwenken.", "Die markierten Stellen fahren wir erneut an. Der Kopf ist dreh- und schwenkbar, Frontal- und Seitenkamera suchen die Steckmuffe ab, bis der Befund eindeutig benannt ist."),
                 ("Befund mit Meterangabe.", "Sie bekommen die Liste der Stellen, an denen sich das Öffnen lohnt, und die Abschnitte, an denen es sich erübrigt. Weil das Bild live anliegt, kann Ihre Bauleitung noch vor Ort entscheiden, statt auf einen Bericht zu warten.")])
        + "<h3>Was wir sehen — und was nicht.</h3><h4>Zuverlässig sichtbar</h4>" + ul(["Spitzende nicht bis zur Einstecktiefenmarkierung eingesteckt", "Spalt, Versatz oder Abwinkelung an der Steckmuffe",
              "Ablagerungen und eingedrungenes Bodenmaterial an der Rohrsohle", "Fremdkörper, Riefen, Deformation", "Zustand jeder Schweißnaht", "die Rohrwand unter klarem Wasser, die Kamera arbeitet auch getaucht"])
        + "<h4>Nicht sichtbar</h4>" + ul(["eine Undichtigkeit ohne Spur an der Innenwand", "ein Haarriss ohne Wassereintritt", "alles hinter trübem Wasser oder aufgewühltem Sediment", "Wandstärke und Materialkennwerte"])
        + "<p>Die Grenze ist die Sicht, nicht die Nässe: Wasser im Rohr stört uns nicht, solange es klar ist. Wir dokumentieren, was das Bild hergibt, und halten fest, welche Abschnitte beurteilbar waren und welche nicht. Wir ersetzen keine Druckprüfung, wir erklären ihr Ergebnis. Bleibt nach der Befahrung kein sichtbarer Befund, sagen wir das und empfehlen ein ergänzendes Verfahren.</p>", alt=True, eyebrow="Zweiter Anlass · Ursachensuche")
    + cta_band("Prüfung auffällig und die Trasse steht?", "Schildern Sie uns den Abschnitt. Wir sagen Ihnen im ersten Gespräch, ob eine Befahrung Ihre Frage beantwortet.", "Abschnitt schildern")
    + sec("Wo die Kamerabefahrung steht — und wo die anderen Verfahren stärker sind.",
        "<p>Die Kamerabefahrung ersetzt weder Kalibrierung noch Druckprüfung und misst keine Wandstärke. Ihr Beitrag ist ein anderer: die optische Sicht ins Rohr, mit Position.</p>"
        + tbl(["Kriterium", 'Kalibrierung (Festkaliber)', "Druckprüfung", "Kamerabefahrung"], [
            ["Optische Sicht", "keine", "keine", "ja"], ["Freier Querschnitt", "nachgewiesen", "keine Aussage", "sichtbare Engstellen"],
            ["Dichtheit", "keine Aussage", "nachgewiesen", "keine Aussage, aber sichtbare Ursachen"], ["Schaden lokalisierbar", "nur „klemmt“", "nur „undicht“", "ja, mit Positionsangabe"],
            ["Ergebnis", "Protokoll", "Protokoll mit Druckverlauf", "Aufnahmen und Befundliste"]]), eyebrow="Einordnung")
    + sec("Überall dort, wo lange Rohre von innen beurteilt werden müssen.",
        "<p>Für Netzbetreiber, Tiefbau- und HDD-Spezialisten, Versorger und Industrie. Immer dann, wenn eine Leitung zu lang und zu eng ist, um sie zu begehen, als Nachweis vor dem Einzug oder als Ursachensuche danach.</p>"
        '<ul class="cards"><li class="card"><p class="eyebrow">Strom · Netzbetreiber &amp; Tiefbau</p><h3>Kabelschutzrohre</h3><p>Stahl wie Kunststoff. Vorher Schweißnähte, Riefen vom Zugseil und Sauberkeit dokumentieren. Hinterher die Steckmuffen kontrollieren, wenn die Dichtheitsprüfung auffällig war.</p></li>'
        '<li class="card"><p class="eyebrow">Diagnose · nach auffälliger Prüfung</p><h3>Ursachensuche an Steckmuffen und Nähten</h3><p>Die Dichtheitsprüfung ist auffällig, die Trasse liegt bereits im Boden. Wir befahren die Leitung mit Live-Bild und schwenken jede auffällige Steckmuffe gezielt an, bis der Befund benannt und verortet ist.</p></li>'
        '<li class="card"><p class="eyebrow">Querungen · HDD &amp; grabenloser Bau</p><h3>Schutz- und Mantelrohre bei Querungen</h3><p>Horizontalspülbohrung unter Fluss, Straße oder Bahn. Dort sind die Rohrstücke vorab stumpf verschweißt und als Strang eingezogen. Nach dem Einzug verifizieren, dass der Strang unbeschädigt und frei ist, samt der Nähte, an die niemand mehr herankommt.</p></li>'
        '<li class="card"><p class="eyebrow">Gas · Wasser · Industrie</p><h3>Pre-Commissioning Neubauleitungen</h3><p>Vor der Inbetriebnahme Innenfläche und Schweißnähte über die ganze Länge dokumentieren, ohne Aufgrabung und prüffähig für die Abnahme.</p></li></ul>', alt=True, eyebrow="Anwendungsfelder")
    + sec("Was Auftraggeber vor der Beauftragung fragen.", faq([
        ("Welche Rohre und Längen sind möglich?", "Das richtet sich nach Werkstoff, Durchmesser, Länge und Ziel der Befahrung. Längere Trassen werden in Abschnitten an den vorhandenen Zugangspunkten befahren. Die Machbarkeit stimmen wir vorab ab."),
        ("Unsere Druckprüfung war auffällig. Finden Sie die Ursache?", "Das ist einer unserer beiden Standardfälle. Wir fahren die Leitung mit der Kamera ab, das Bild kommt live an die Oberfläche. Auffällige Stellen fahren wir gezielt an und schwenken darauf. Optisch erkennbare Ursachen wie eine nicht vollständig gesteckte Muffe, ein Spalt zwischen den Rohrenden, Wassereintritt, Fremdkörper oder eingeschwemmtes Material lassen sich so metergenau verorten, ohne die Trasse aufzugraben."),
        ("Findet die Kamera jede Undichtigkeit?", "Nein, und das sagen wir vorab. Wir sehen, was optisch sichtbar ist. Eine offene oder verschobene Muffe, ein Spalt, ein Riss, eindringendes Wasser oder Bodenmaterial sind zuverlässig erkennbar. Ein Haarriss in der Rohrwand, eine Undichtigkeit hinter der Dichtung oder eine Stelle, die unter stehendem Wasser liegt, kann eine Kamera dagegen nicht sicher zeigen. In solchen Fällen grenzen wir mit dem Bild den Bereich ein, statt ihn zu beweisen. Die abschließende Bewertung bleibt bei Ihrer Prüfstelle."),
        ("Funktioniert das auch bei Wasser oder Ablagerungen im Rohr?", "Ja. Stehendes Wasser und eingeschwemmtes Sediment gehören selbst zu den Befunden, die wir dokumentieren. Wasser allein ist kein Hindernis: Die Kamera arbeitet auch unter Wasser, und solange das Wasser klar ist, sehen wir die Rohrwand darunter. Die Grenze ist die Sicht, nicht die Nässe. Trübes Wasser oder aufgewühltes Sediment verdecken den Bereich. Ist die Leitung vorher gereinigt oder gemolcht worden, wird das Ergebnis deutlich aussagekräftiger. Ob sich eine Befahrung im vorliegenden Zustand lohnt, klären wir vorab am Telefon."),
        ("Misst die Kamerabefahrung auch Wandstärke oder Korrosion?", "Nein. Die Kamerabefahrung ist ein optisches Verfahren. Sie dokumentiert die sichtbare Innenfläche (Schweißnähte, Risse, Riefen, Verformung, Ablagerungen, Fremdkörper, Wassereintritt). Wandstärken- oder Metallverlust-Messung ist Sache anderer Messverfahren."),
        ("Ersetzt das die Kalibrierung oder Druckprüfung?", 'Nein. <a href="/L/rohrkalibrierung.html">Kalibrierung</a> und <a href="/L/din-en-1610.html">Druckprüfung</a> bleiben für Querschnitt und Dichtheit zuständig, beides übernehmen wir ebenfalls. Die Kamera zeigt Ihnen, wie es im Rohr tatsächlich aussieht, und verortet die Stelle.'),
        ("Welche Voraussetzungen muss die Leitung erfüllen?", "Die Leitung sollte außer Betrieb, befahrbar und im Wesentlichen frei von stehendem Wasser und losem Material sein, mit Zugang an den Rohrenden. Ist gemolcht oder gereinigt worden, ist das ideal. Die Machbarkeit, auch bei Bögen, stimmen wir vorab ab."),
        ("Was bekommen wir geliefert – in welchem Format?", "Sie erhalten die Aufnahmen der Fahrt samt der gezielten Schwenkaufnahmen je Fundstelle und eine Befundliste mit Positionsangabe. Was für Ihren Fall sinnvoll ist, klären wir vorab."),
        ("Gibt es ein Live-Bild während der Befahrung?", "Ja. Das Bild wird live übertragen, Befunde lassen sich direkt vor Ort mit Ihrer Bauleitung bewerten."),
        ("Passt die Dokumentation zu Normen und Abnahme?", "Kalibrierung und Druckprüfung laufen nach der in Ihrem Leistungsverzeichnis vereinbarten Prüfvorschrift, beides bieten wir ebenfalls an. Unsere Aufnahmen ergänzen sie um den lückenlosen Sicht-Nachweis, den eine Abnahmedokumentation neben dem Kalibrier- und Druckprotokoll üblicherweise verlangt. Format und Aufbau der Übergabe stimmen wir auf Ihren Abnahmeprozess ab."),
        ("Wie läuft eine Anfrage konkret ab?", "Sie schildern uns Leitungstyp, Trasse, Rohranzahl, Durchmesser und Termin. Wir prüfen die Machbarkeit und schicken ein konkretes Angebot.")]), alt=True, eyebrow="Häufige Fragen")
    + request("Ihre Leitung, geprüft und dokumentiert — bevor es teuer wird.", "Schildern Sie uns die Trasse. Wir melden uns mit Machbarkeit und Angebot.",
              ["Leitungstyp, Rohrtyp und Durchmesser", "Trasse und ungefähre Länge", "Anzahl der Rohre", "Worum geht es: Nachweis vor dem Kabeleinzug oder für die Abnahme, Diagnose nach auffälliger Prüfung, Zustandsbewertung oder noch unklar",
               "Anwendungsfeld, zum Beispiel Stromkabel-Schutzrohre, Mantelrohre und Querungen, Glasfaser- und Leerrohre, Industrie- und Prozessrohre", "Ort und geplanter Zeitraum"],
              "Ein kurzer Hinweis per E-Mail genügt, wenn noch nicht alles feststeht:"))

RT_REINIGUNG = (
    SNAVM + '<section class="hero"><div class="wrap"><p class="eyebrow">Kanalreinigung · Hausanschlussleitungen</p><h1>Reinigung unter optischer Kontrolle</h1>'
    '<p><strong>Reinigen und dabei zusehen.</strong> Eine lenkbare Spüleinheit mit Kamera im Spülkopf, die „sehende Düse“, verbindet Hochdruckreinigung und optische Inspektion in einem Arbeitsgang. So sehen wir während der Reinigung, was im Haupt- und im Anschlusskanal passiert.</p>'
    '<ul class="ticks"><li>Reinigungsergebnis direkt im Bild geprüft</li><li>Abbiegen in Anschlussleitungen vom Hauptkanal aus</li></ul>'
    '<p><a class="btn" href="#anfrage">Reinigung anfragen</a> <a class="btn ghost" href="#vorteile">Ihre Vorteile</a></p></div></section>\n'
    + sec("Hochdruckreinigung und Kamera in einem Spülkopf.",
        "<p>Die sehende Düse ist eine lenkbare Reinigungseinheit mit Kamera und LED-Beleuchtung im Spülkopf. Vom Hauptkanal aus lässt sie sich in verzweigte Hausanschlussleitungen steuern und reinigt dort unter Kamerabeobachtung. Wer die Düse führt, sieht sofort, was die Reinigung bewirkt hat.</p>"
        "<p>Das Bild zeigt außerdem den Zustand von Haupt- und Anschlusskanal. Trifft die Düse auf ein Hindernis, kann sie mit vermindertem Druck daran vorbeigeführt oder die Reinigung abgebrochen werden. Wo es der Befund verlangt, ist eine auf den Kanalzustand abgestimmte Inspektion möglich. Mehrfach verzweigte Netze lassen sich gezielt reinigen, und zwar mit größerer Reichweite als bei einer Lateralkamera-Befahrung.</p>",
        eyebrow="Das Verfahren")
    + sec("Was die Technik leistet.", ul([
        "Reinigung von Rohren und Kanälen unter direkter Kamerabeobachtung",
        "Abbiegen in Anschlussleitungen und Stutzen vom Hauptkanal aus, ohne das Grundstück zu betreten",
        "kontrolliertes Ausweichen bei Hindernissen im Kanal",
        "hochauflösende Videoaufzeichnung mit Texteinblendung und digitale Fotos",
        "Meterzähler für Haupt- und Anschlusskanal",
        "Ortung des gesamten Leitungsverlaufs",
        "Beleuchtung durch Hochleistungs-LEDs im Spülkopf",
        "wasserdichter, stoßfester Kamerakopf"])
        + "<p class=\"note\">Durchmesserbereich und Reichweite hängen von Leitung und Einsatz ab. Die Machbarkeit stimmen wir vorab mit Ihnen ab.</p>",
        alt=True, eyebrow="Leistungsmerkmale")
    + sec("Warum Reinigung unter Sicht sinnvoll ist.",
        '<ul class="cards"><li class="card"><h3>Schäden genau lokalisieren</h3><p>Das Live-Bild zeigt, wo Verstopfung oder Beschädigung sitzen. Wir gehen das Problem gezielt an und sparen Zeit und Aufwand.</p></li>'
        '<li class="card"><h3>Effizienter arbeiten</h3><p>Der Fortschritt ist in Echtzeit zu verfolgen, das Rohr wird nachweislich vollständig gereinigt. Wiederholte Reinigungsversuche und Ausfallzeiten werden seltener.</p></li>'
        '<li class="card"><h3>Schäden vermeiden</h3><p>Empfindliche Bereiche sind im Bild erkennbar und werden geschont. Das zählt vor allem bei alten oder bereits geschädigten Leitungen.</p></li>'
        '<li class="card"><h3>Arbeit nachweisen</h3><p>Bilder und Videos dokumentieren die ausgeführte Arbeit und den Zustand der Leitung.</p></li></ul>',
        eyebrow="Warum unter Sicht", id="vorteile")
    + sec("Was Sie davon haben.",
        '<ul class="cards"><li class="card"><h3>Transparenz</h3><p>Sie sehen, was in Ihrem Rohrsystem passiert, und können die ausgeführte Arbeit nachvollziehen.</p></li>'
        '<li class="card"><h3>Kosten im Griff</h3><p>Gezielte Reinigung der Problemstellen vermeidet unnötige Arbeiten und damit Kosten.</p></li>'
        '<li class="card"><h3>Dauerhafte Wirkung</h3><p>Eine gründliche Reinigung senkt das Risiko wiederkehrender Abflussprobleme, Blockaden und Notfälle.</p></li>'
        '<li class="card"><h3>Probleme früh erkennen</h3><p>Die Aufnahmen zeigen mögliche Schwachstellen, bevor sie zu einem Schaden werden.</p></li></ul>',
        alt=True, eyebrow="Ihre Vorteile")
    + sec("Reinigung und Inspektion aus einer Hand.",
        '<p>Zeigt die Reinigung einen Befund, der genauer untersucht werden soll, schließt sich die <a href="/L/dreh-schwenkkopf-kamera.html">Inspektion</a> an. Ob eine Leitung danach dicht ist, klärt die <a href="/L/din-en-1610.html">Dichtheitsprüfung</a>.</p>',
        eyebrow="Zusammenspiel")
    + request("Reinigung anfragen",
              "Schildern Sie uns die Leitung. Wir melden uns mit Rückfragen oder mit Machbarkeit und Angebot.",
              ["Art der Leitung: Hauptkanal, Hausanschluss oder verzweigtes Netz", "Werkstoff und Durchmesser, soweit bekannt",
               "Ungefähre Länge und Zugangspunkte, zum Beispiel Schächte", "Anlass: Verstopfung, Wartung, Vorbereitung einer Inspektion oder noch unklar",
               "Ort und gewünschter Zeitraum"],
              "Ein kurzer Hinweis per E-Mail genügt, wenn noch nicht alles feststeht:"))

RT_HOCHDRUCK = (
    SNAVM
    + '<section class="hero"><div class="wrap"><p class="eyebrow">Kanalreinigung · Spezialreinigung</p><h1>Höchstdruck-Wasserstrahlen</h1>'
    '<p><strong>Wenn Spülen nicht mehr reicht.</strong> Harte Ablagerungen, Einwüchse und Fremdkörper im Kanal tragen wir mit einem kamerageführten Wasserstrahl-Roboter ab, per Fernsteuerung und unter Live-Bild.</p>'
    '<ul class="ticks"><li>Druck und Fahrgeschwindigkeit am Roboter einstellbar</li><li>Live-Bild während des Abtrags</li><li>Auch zur Vorbereitung einer Sanierung</li></ul>'
    '<p><a class="btn" href="#anfrage">Einsatz anfragen</a> <a class="btn ghost" href="#was">Was sich entfernen lässt</a></p></div></section>\n'
    + sec("Normale Reinigung kommt an harten Belägen nicht weiter.",
        "<p>Saugen und Spülen lösen Sand, Schlamm und Fett. Verkrustungen, Kalk oder Beton im Rohr, Wurzeln, die sich in die Wand gearbeitet haben, oder ein alter Liner, der sich abgelöst hat, bleiben dabei sitzen. Dort setzt der Wasserstrahl-Roboter an.</p>"
        "<p>Der Roboter fährt in die Haltung, die Kamera zeigt live, was vor dem Strahlkopf liegt, und der Bediener steuert aus sicherer Entfernung. Druck und Fahrgeschwindigkeit stellt er auf den Belag und das Rohrmaterial ein, so dass die Rohrwand geschont wird und der Abtrag nur dort erfolgt, wo er nötig ist.</p>",
        eyebrow="Das Problem")
    + sec("Was sich mit dem Wasserstrahl entfernen lässt.", ul([
        "Inkrustationen, Kalk, Beton und Bitumen",
        "Wurzeleinwüchse und Fettablagerungen",
        "Fremdkörper im Rohr, zum Beispiel Reste von Linern sowie Stahl- und Stahlbetonteile",
        "Aufbereitung der Haltung vor dem Einzug eines Liners"])
        + "<p class=\"note\">Welche Nennweiten, Profile und Haltungslängen sich bearbeiten lassen, hängt vom Einzelfall ab. Das klären wir vorab mit Ihnen.</p>",
        alt=True, eyebrow="Anwendung", id="was")
    + sec("So läuft ein Einsatz ab.", steps([
        ("Haltung beurteilen", "Wir klären Profil, Material, Art des Belags und Zugang über die Schächte. Gibt es Aufnahmen aus einer Inspektion, nutzen wir sie."),
        ("Roboter einsetzen", "Der Roboter wird über den Schacht in die Haltung gebracht. Die Kamera liefert von Anfang an das Live-Bild."),
        ("Abtragen unter Sicht", "Druck und Fahrgeschwindigkeit passen wir am Belag an. Der Bediener sieht den Fortschritt und kann sofort nachregeln oder stoppen."),
        ("Ergebnis prüfen", "Am Ende ist die Haltung frei, auf Wunsch mit Aufnahmen als Nachweis, bevor es mit Sanierung oder Abnahme weitergeht.")]),
        eyebrow="Ablauf")
    + sec("Kaltschneiden ohne Wärmeeintrag.",
        "<p>Der Höchstdruck-Wasserstrahl trennt kalt. Es entsteht keine Wärme und kein Funkenflug, und das macht ihn für Bereiche interessant, in denen Hitze ein Risiko wäre, etwa bei explosionsgefährdeten oder sicherheitssensiblen Anlagen.</p>",
        alt=True, eyebrow="Besonderheit")
    + sec("Warum der Roboter statt Handarbeit.",
        '<ul class="cards"><li class="card"><h3>Gezielt statt grob</h3><p>Live-Bild und einstellbare Parameter erlauben einen Abtrag genau dort, wo er gebraucht wird.</p></li>'
        '<li class="card"><h3>Sicher für das Personal</h3><p>Die Fernsteuerung hält das Personal aus der Haltung heraus und senkt damit Gesundheitsrisiken.</p></li>'
        '<li class="card"><h3>Auch schwierig zugänglich</h3><p>Die mobile Technik erreicht Systeme, bei denen andere Verfahren an Platz oder Zugang scheitern.</p></li>'
        '<li class="card"><h3>Sauber getrennt</h3><p>Eingesetzt werden Wasser und Abrasivmittel, die sich getrennt auffangen und umweltgerecht entsorgen lassen.</p></li></ul>',
        eyebrow="Ihre Vorteile")
    + sec("Das richtige Verfahren für Ihre Haltung.",
        '<p>Ist die Leitung nur verschmutzt, genügt oft Saugen und Spülen. Müssen Anschlussleitungen gezielt unter Sicht gereinigt werden, hilft die <a href="/L/sehende-duese.html">Reinigung unter optischer Kontrolle</a>. Der Wasserstrahl-Roboter kommt dazu, wenn harte Beläge, Einwüchse oder Fremdkörper entfernt werden müssen. Danach folgt bei Bedarf die <a href="/L/dreh-schwenkkopf-kamera.html">Inspektion</a> oder die <a href="/L/din-en-1610.html">Dichtheitsprüfung</a>.</p>',
        alt=True, eyebrow="Einordnung")
    + request("Einsatz anfragen",
              "Schildern Sie uns die Haltung. Wir melden uns mit Rückfragen oder mit Machbarkeit und Angebot.",
              ["Art des Belags oder Hindernisses, soweit bekannt", "Profil, Werkstoff und Nennweite der Haltung",
               "Ungefähre Länge und Zugangspunkte, zum Beispiel Schächte", "Anlass: Reinigung, Vorbereitung einer Sanierung, Fremdkörper oder noch unklar",
               "vorhandene Inspektionsaufnahmen, falls vorhanden", "Ort und gewünschter Zeitraum"],
              "Ein kurzer Hinweis per E-Mail genügt, wenn noch nicht alles feststeht:"))

PAGES = {
    "kabelschutzrohre": ("Rohrservice an Kabelschutzrohren – IGK Abwassertechnik GmbH", "Molchreinigung, Druckprüfung, Kalibrierung und Seileinzug an Kabelschutzrohren und Leerrohren", RT_UEBERSICHT),
    "din-en-1610": ("Druckprüfung von Rohrleitungen – IGK Abwassertechnik GmbH", "Dichtheitsprüfung von Rohrleitungen und Kanälen mit Luft nach DIN EN 1610, mit Protokoll je Prüfabschnitt", RT_DRUCK),
    "kalibrierung": ("Kalibrierung von Kabelschutzrohren – IGK Abwassertechnik GmbH", "Nachweis der Profilfreiheit von Kabelschutzrohren vor dem Kabelzug", RT_KALIB),
    "dreh-schwenkkopf-kamera": ("Inspektion von Rohren und Leitungen – IGK Abwassertechnik GmbH", "Optische Inspektion von Rohren und Leitungen: Nachweis vor dem Kabeleinzug und Ursachensuche nach auffälliger Druckprüfung", RT_KAMERA),
    "sehende-duese": ("Reinigung unter optischer Kontrolle – IGK Abwassertechnik GmbH", "Reinigung von Rohren, Kanälen und Hausanschlussleitungen unter Kamerabeobachtung mit lenkbarer Spüleinheit", RT_REINIGUNG),
    "wasserhoechstdruckfraesen": ("Höchstdruck-Wasserstrahlen im Kanal – IGK Abwassertechnik GmbH", "Spezialreinigung von Kanälen mit kamerageführtem Wasserstrahl-Roboter: harte Beläge, Einwüchse und Fremdkörper entfernen", RT_HOCHDRUCK),
    "index": ("IGK Abwassertechnik – Rohr-, Kanal- und Kabelschutzrohr-Dienstleistungen", "Rohr-, Kanal- und Kabelschutzrohr-Dienstleistungen für Kommunen, Industrie und Privat", INDEX),
    "karriere": ("Karriere – IGK Abwassertechnik GmbH", "Offene Stellen bei der IGK Abwassertechnik GmbH", KARRIERE),
    "ansprechpartner": ("Ansprechpartner – IGK Abwassertechnik GmbH", "Ihre Ansprechpartner bei der IGK Abwassertechnik GmbH", ANSPRECH),
    "impressum": ("Impressum – IGK Abwassertechnik GmbH", "Impressum der IGK Abwassertechnik GmbH", legal("", "impressum")),
    "agb": ("AGB – IGK Abwassertechnik GmbH", "Allgemeine Geschäftsbedingungen der IGK Abwassertechnik GmbH", legal("", "agb")),
    "datenschutz": ("Datenschutz – IGK Abwassertechnik GmbH", "Datenschutzerklärung der IGK Abwassertechnik GmbH", legal("", "datenschutz")),
}

# Bereichs-, Gruppen- und Unterpunktseiten je Bereich aus der Struktur
PAGE_AREA = {}   # Seite -> Bereich (steuert die Navigation oben rechts)
NOINDEX = {"agb"}  # Platzhalter, bis der AGB-Text vorliegt
def fix(body, a, **kw):
    body = body.replace(SNAVM, snav(a, **kw))
    def rep(m):  # /L/<unterpunkt>.html -> Seite im selben Bereich, sonst im anderen
        t = m.group(1)
        for x in [a] + [y for y in AREAS if y != a]:
            if (x, t) in CRUMBS: return f"/{lp(x, t)}.html"
        return m.group(0)
    body = re.sub(r"/L/([a-z0-9-]+)\.html", rep, body)
    def lift(m):  # Aufzählung aus dem Header heraus, damit alle Header gleich hoch sind
        sec_h = m.group(1) + m.group(3) + "</div></section>"
        return sec_h + f'\n<section class="section ticks-sec"><div class="wrap prose">{m.group(2)}</div></section>'
    return re.sub(r'(<section class="hero"><div class="wrap">(?:(?!</section>).)*?)(<ul class="ticks">.*?</ul>)((?:(?!</section>).)*?)</div></section>', lift, body, flags=re.S)
LEAF_PAGE = {}
for old, new in [("din-en-1610", "din-en-1610"), ("kalibrierung", "rohrkalibrierung"), ("dreh-schwenkkopf-kamera", "dreh-schwenkkopf-kamera"),
                 ("sehende-duese", "sehende-duese"), ("wasserhoechstdruckfraesen", "wasserhoechstdruckfraesen")]:
    LEAF_PAGE[new] = PAGES.pop(old)
kt, kd, kbody = PAGES.pop("kabelschutzrohre")
PAGES["kabelschutzrohre"] = (kt, kd, fix(kbody, "kabelschutzrohre")); PAGE_AREA["kabelschutzrohre"] = "kabelschutzrohre"
PAGES["wasser"] = ("Wasser – IGK Abwassertechnik GmbH", "Abwasser- und Regenwasserleitungen: Inspektion, Reinigung, Dichtheitsprüfung, Kalibrierung und Sanierung",
    snav("wasser") + f'<section class="hero"><div class="wrap"><p class="eyebrow">Leistungen</p><h1>Wasser</h1><p>{AREAS["wasser"]["lead"]}</p></div></section>\n'
    + area_cards("wasser") + contact("Anfrage zu Wasser")); PAGE_AREA["wasser"] = "wasser"
for slug, (a, g) in GROUPPAGES.items():
    d = AREAS[a]
    PAGES[slug] = (f"{g[1]} – {d['title']} – IGK Abwassertechnik GmbH", f"{g[1]} für {d['what']} bei der IGK Abwassertechnik GmbH",
        snav(a, g=g) + f'<section class="hero"><div class="wrap"><p class="eyebrow">{d["title"]}</p><h1>{g[1]}</h1><p>Alle Leistungen im Bereich {g[1]} für {d["what"]}.</p></div></section>\n'
        + group_body(a, g) + contact(f"{g[1]} anfragen")); PAGE_AREA[slug] = a
for (a, s), crumbs in CRUMBS.items():
    t, d = LEAF_TITLES[s], AREAS[a]
    if s in LEAF_PAGE:
        ot, od, body = LEAF_PAGE[s]
        PAGES[lp(a, s)] = (f"{ot.split(' – ')[0]} – {d['title']} – IGK Abwassertechnik GmbH", od, fix(body, a, leaf=s))
    else:
        c = crumbs[0]; eb = d["title"] + ("" if c[2] is None else f" · {c[1]}")
        PAGES[lp(a, s)] = (f"{t} – {d['title']} – IGK Abwassertechnik GmbH", f"{t}: Beschreibung folgt",
            snav(a, leaf=s) + f'<section class="hero"><div class="wrap"><p class="eyebrow">{eb}</p><h1>{t}</h1><p>Die ausführliche Beschreibung dieser Leistung folgt in Kürze.</p>'
            f'<p><a class="btn" href="#anfrage">Anfrage stellen</a></p></div></section>\n' + contact(f"{t} anfragen"))
        NOINDEX.add(lp(a, s))
    PAGE_AREA[lp(a, s)] = a
def nav_for(name):
    L = '<a href="/#leistungen">Leistungen</a>'
    a = PAGE_AREA.get(name)
    others = "".join(f'\n    <a href="/{x}.html">{AREAS[x]["title"]}</a>' for x in AREAS if a and x != a)
    return L + others + '\n    <a href="/karriere.html">Karriere</a>\n    <a href="/ansprechpartner.html">Ansprechpartner</a>'
for name, (t, d, body) in PAGES.items():
    head = HEAD.format(title=t, desc=d, nav=nav_for(name))
    if name in NOINDEX: head = head.replace("</head>", '<meta name="robots" content="noindex">\n</head>')
    body = re.sub(r'<section[^>]*id="anfrage".*?</section>\n?', "", body, flags=re.S)  # Anfrage-Rubrik am Seitenende entfällt, Anfrage über Button oben
    body = body.replace('href="#anfrage"', f'href="mailto:{MAIL}"')
    body = re.sub(r'<a class="btn" href="mailto:' + re.escape(MAIL) + r'">[^<]*</a>\s*', "", body)  # keine Anfrage-Buttons im Inhalt
    body = re.sub(r'<p>\s*</p>\n?', "", body)
    (R / "site" / f"{name}.html").write_text(head + body + FOOT)
for f in (R / "site").glob("*.html"):  # veraltete Seiten entfernen
    if f.stem not in PAGES: f.unlink()
print("built", list(PAGES))

# GitHub Pages copy (main /docs). ponytail: prefix hardcoded; with custom domain add a CNAME file in repo root -> no prefix.
import re, shutil
BASE = "" if (R / "CNAME").exists() else "/igk-web"
shutil.rmtree(R / "docs", ignore_errors=True)
shutil.copytree(R / "site", R / "docs")
for f in (R / "docs").rglob("*"):
    if f.suffix in (".html", ".css"):
        s = f.read_text()
        s = re.sub(r'(href|src)="/(?!/)', rf'\1="{BASE}/', s).replace("url(/", f"url({BASE}/")
        f.write_text(s)
(R / "docs" / ".nojekyll").touch()
if BASE == "":
    shutil.copy(R / "CNAME", R / "docs" / "CNAME")
