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
    <a href="/#leistungen">Leistungen</a>
    <a href="/rohrtechnik.html">Rohrtechnik</a>
    <a href="/karriere.html">Karriere</a>
    <a href="/ansprechpartner.html">Ansprechpartner</a>
    <a class="btn" href="tel:+4942984 10 42".replace(" ","")>Anrufen</a>
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
      F 04298 41 0 44<br>
      <a href="mailto:info@igk-abwassertechnik.de">info@igk-abwassertechnik.de</a>
    </p>
    <p class="social">
      <a href="https://de.linkedin.com/company/igk-abwassertechnik" rel="noopener">LinkedIn</a>
      <a href="https://instagram.com/igk_abwassertechnik" rel="noopener">Instagram</a>
      <a href="https://m.facebook.com/igk.abwassertechnik" rel="noopener">Facebook</a>
    </p>
  </div>
  <div class="wrap legal"><span>&copy; IGK Abwassertechnik GmbH</span><a href="/impressum.html">Impressum</a><a href="/datenschutz.html">Datenschutz</a></div>
</footer>
</body>
</html>
"""

SERVICES = [
    ("inspektion", "Inspektion", "Kanal- und Rohrinspektion mit Kameratechnik."),
    ("reinigung", "Reinigung", "Saugen, Spülen und Fräsen von Rohren und Kanälen."),
    ("messung", "Dichtheitsprüfung", "Prüfung von Rohr- und Kanalnetzen auf Dichtheit."),
    ("pruefung", "Sanierung", "Sanierung schadhafter Rohre und Kanäle."),
]
cards = "".join(
    f'<li class="card"><span class="ico"><img src="/assets/icons/{i}.svg" alt="" width="40" height="40"></span><h3>{t}</h3><p>{d}</p></li>'
    for i, t, d in SERVICES)
cards += '<li class="card"><span class="ico"><img src="/assets/icons/inspektion.svg" alt="" width="40" height="40"></span><h3><a href="/rohrtechnik.html">Rohrtechnik</a></h3><p>Kabelschutzrohre: Molchreinigung, Druckprüfung, Kalibrierung, Seileinzug.</p></li>'

TEAM = [
    ("Thorbjoern_Roessner", "Ing. Thorbjörn Rössner", "Geschäftsführender Gesellschafter · Zertifizierter Kanalsanierungsberater", "Kalkulation, Angebotserstellung und Projektleitung Sanierung"),
    ("Christina_Roessner", "Christina Rössner", "Assistenz der Geschäftsführung", "Marketing & Personal"),
    ("Sabine_Oelmeyer", "Sabine Oelmeyer", "Buchhaltung", "Rechnungswesen & kaufmännische Abwicklung"),
    ("Baule", "Frank Baule", "Projektleitung", "Dokumentation & Disposition"),
    ("Jelena_Prange", "Jelena Prange", "Assistenz der Projektleitung", "Projektorganisation & -abwicklung"),
]
team = "".join(
    f'<li class="person"><img src="/assets/team/{f}.jpg" alt="{n}" loading="lazy"><h3>{n}</h3><p><strong>{r}</strong><br>{d}</p></li>'
    for f, n, r, d in TEAM)

INDEX = f"""<section class="hero">
  <div class="wrap">
    <h1>Rohr- und Kanaldienstleistungen für Kommunen, Industrie und Privat</h1>
    <p>Damit die Rohre unter unseren Straßen sauber und dicht sind.</p>
    <p><a class="btn" href="tel:+494298410042">04298 41 0 42</a> <a class="btn ghost" href="mailto:info@igk-abwassertechnik.de">E-Mail schreiben</a></p>
  </div>
</section>
<section id="leistungen" class="wrap section">
  <h2>Leistungen</h2>
  <ul class="cards">{cards}</ul>
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


# --- Rohrtechnik (Kabelschutzrohre): Übersicht + 3 Unterseiten. Texte aus hexbee.de/rohrtechnik adaptiert, Entwurf -> Kunde bestätigt.
import re
TEL = re.search(r'href="(tel:[^"]+)"', FOOT).group(1)
MAIL = "info@igk-abwassertechnik.de"
R_NAV = [("rohrtechnik", "Übersicht"), ("druckpruefung", "Druckprüfung"), ("kalibrierung", "Kalibrierung"), ("kamerabefahrung", "Kamerabefahrung")]

def r_hero(h1, lead, bullets, active, cta):
    nav = "".join(f'<a href="/{k}.html"' + (' aria-current="page"' if k == active else "") + f">{t}</a>" for k, t in R_NAV)
    li = "".join(f"<li>{b}</li>" for b in bullets)
    return (f'<div class="subnav" role="navigation" aria-label="Rohrtechnik"><div class="wrap">{nav}</div></div>\n'
            f'<section class="hero"><div class="wrap"><h1>{h1}</h1><p>{lead}</p><ul class="ticks">{li}</ul>'
            f'<p><a class="btn" href="#anfrage">{cta}</a> <a class="btn ghost" href="{TEL}">Anrufen</a></p></div></section>\n')

def sec(h2, body, alt=False):
    return f'<section class="section{" alt" if alt else ""}"><div class="wrap prose">\n<h2>{h2}</h2>\n{body}\n</div></section>\n'

def ul(items): return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"
def steps(items): return '<ol class="steps">' + "".join(f"<li><h3>{h}</h3><p>{d}</p></li>" for h, d in items) + "</ol>"
def tbl(head, rows, cap=""):
    return ("<div class=\"tbl\"><table><thead><tr>" + "".join(f"<th>{c}</th>" for c in head) + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table></div>"
            + (f'<p class="note">{cap}</p>' if cap else ""))
def faq(items): return "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in items)
def request(h2, extra=""):
    return (f'<section class="section alt" id="anfrage"><div class="wrap prose"><h2>{h2}</h2>\n'
            "<p>Wir melden uns mit Rückfragen oder mit Machbarkeit und Angebot.</p>\n<h3>Für ein Angebot brauchen wir</h3>\n"
            + ul(["Rohrwerkstoff, Außendurchmesser und Wanddicke oder SDR", "Anzahl und Länge der Rohrzüge",
                  "bei Kalibrierung das gewünschte Kalibermaß oder die vorgesehene Belegung",
                  "bei Druckprüfung Prüfverfahren und Prüfdruck, falls vorgegeben",
                  "bei Seileinzug Seilart und Durchmesser, falls vorgegeben", "Ort und geplanter Zeitraum",
                  "ob die Trasse abschnittsweise freigegeben wird"])
            + f'\n<p>Liegt ein Leistungsverzeichnis vor, reicht der Auszug mit den betreffenden Positionen. Schicken Sie ihn per E-Mail an <a href="mailto:{MAIL}">{MAIL}</a>.</p>\n'
            f'<p><a class="btn" href="{TEL}">04298 41 0 42</a> <a class="btn" href="mailto:{MAIL}">E-Mail schreiben</a></p>\n</div></section>\n')

ORDER = steps([
    ("Reinigen", "Schaumstoffmolch mit Druckluft, so oft, bis er sauber austritt. Ohne Wasser, damit das Rohr trocken bleibt."),
    ("Druckprüfen", 'Dichtheitsprüfung mit Luft, Prüfverfahren und Prüfdruck nach Vorgabe des Auftraggebers. <a href="/druckpruefung.html">Mehr zur Druckprüfung</a>'),
    ("Kalibrieren", 'Kalibrierdorn mit Treibmolch, Nachweis der Profilfreiheit nach vereinbartem Kalibermaß. <a href="/kalibrierung.html">Mehr zur Kalibrierung</a>'),
    ("Seileinzug", "Zugseil am Treibmolch, im selben Durchgang wie die Kalibrierung. Beide Enden gekennzeichnet."),
    ("Kamerabefahrung (optional)", 'Wenn sichtbar werden soll, wie das Rohr innen aussieht. <a href="/kamerabefahrung.html">Mehr zur Kamerabefahrung</a>'),
])
ORDER_TXT = ("<p>Gereinigt wird zuerst. Ein Dorn, der an einem Sandpolster stehen bleibt, liefert einen Befund, der keiner ist, und eine Blase dichtet auf Sediment nicht ab.</p>"
    "<p>Die Einbauanleitung A 535b des Kunststoffrohrverbands sieht die Kalibrierung „nach Abschluss der Dichtheitsprüfung“ vor. Das Zugseil ziehen wir ebenfalls erst nach der Druckprüfung ein, weil ein Seil im Rohr die Abdichtung der Prüfblase stören würde.</p>"
    "<p>Verlangt Ihr Leistungsverzeichnis, vor der Druckprüfung zu kalibrieren, laufen Kalibrierung und Seileinzug in getrennten Durchgängen.</p>")
NOT = lambda keine, own: (f"<h3>Keine Aussage zu</h3>{ul(keine)}"
    "<p>Die Kalibrierung weist den freien Querschnitt nach. Ob das Rohr dicht ist, zeigt die Druckprüfung. Die Molchreinigung trägt Material aus, bis der Molch sauber austritt. Keine dieser Leistungen ersetzt eine der anderen.</p>")
INSPEKT_LINK = '<p>Ob an Muffen oder Rohrwand ein sichtbarer Schaden vorliegt, zeigt eine <a href="/kamerabefahrung.html">Kamerabefahrung</a>.</p>'

RT_UEBERSICHT = (
    r_hero("Rohrservice an Kabelschutzrohren", "Molchreinigung, Druckprüfung, Kalibrierung und Seileinzug vor dem Kabelzug.",
           ["Protokoll je Rohrzug", "Zugseil im selben Durchgang wie die Kalibrierung", "Kamerabefahrung auf Wunsch"], "rohrtechnik", "Rohrservice anfragen")
    + sec("Vier Leistungen am Rohrzug", "<p>Wir reinigen Kabelschutzrohre und Leerrohre, prüfen sie mit Luft auf Dichtheit, weisen die Profilfreiheit nach und ziehen das Zugseil ein. Einzeln oder im selben Einsatz, mit Protokoll je Rohrzug.</p>" + ORDER)
    + sec("Reihenfolge und Abstimmung", ORDER_TXT, alt=True)
    + sec("Was welche Leistung nachweist", "<p>Die Kalibrierung weist den freien Querschnitt nach.</p><p>Ob das Rohr dicht ist, zeigt die Druckprüfung.</p><p>Die Molchreinigung trägt Material aus, bis der Molch sauber austritt.</p><p><strong>Keine dieser Leistungen ersetzt eine der anderen.</strong></p>")
    + request("Rohrservice anfragen"))

RT_DRUCK = (
    r_hero("Druckprüfung von Kabelschutzrohren", "Dichtheitsprüfung mit Luft nach DIN EN 1610, mit aufgezeichnetem Druckverlauf.",
           ["Verfahren LC oder LD nach DIN EN 1610", "Druckverlauf aufgezeichnet", "Protokoll je Prüfabschnitt"], "druckpruefung", "Druckprüfung anfragen")
    + sec("Wann druckgeprüft wird", "<p>Ein Leerrohr soll trocken und frei bleiben, bis das Kabel kommt. Durch eine undichte Muffe können Wasser und Boden eindringen. Die Druckprüfung zeigt, ob der Rohrzug dicht ist, und das Ergebnis steht je Prüfabschnitt im Protokoll.</p>"
        + tbl(["Anlass", "Warum"], [
            ["Nach der Verlegung, vor dem Verfüllen des Grabens", "Die Einbauanleitung A 535a des Kunststoffrohrverbands sieht die Prüfung abschnittsweise und vor dem Verfüllen vor. Die Muffen sind dann noch zugänglich."],
            ["Als Abnahmeprüfung nach dem Verfüllen", "Nachweis am fertigen Rohrzug, bevor die Anlage übergeben wird."],
            ["Vor dem Kabeleinzug oder Kabeleinblasen", "Nachweis, dass kein Wasser und kein Boden in den Rohrzug eindringen können."],
            ["Bei Übernahme einer fremd verlegten Anlage", "Ein Nachweis durch Dritte vor der Abnahme."],
            ["Bei Bestandsrohren vor einer Neubelegung", "Der Zustand ist unbekannt."]]))
    + sec("Rohrzug verschließen, Luft aufbringen, Druckverlauf messen",
        "<p>Wir verschließen den Rohrzug an beiden Enden, bringen Luft auf den vereinbarten Prüfdruck und messen den Druck über die festgelegte Prüfzeit. Bleibt der Druckabfall unter dem zulässigen Wert, ist der Prüfabschnitt dicht.</p>"
        "<p>Geprüft wird nach <strong>DIN EN 1610</strong>, in der Regel mit Verfahren LC oder LD, sonst nach der Vorgabe in Ihrem Leistungsverzeichnis. Ein elektronisches Prüfgerät zeichnet den Druckverlauf auf und erstellt das Protokoll.</p>"
        + steps([("Prüfabschnitt und Prüfvorgabe festlegen", "In der Regel ein Rohrzug von Schacht zu Schacht. Prüfverfahren und Prüfdruck lassen wir uns vor dem ersten Prüfabschnitt schriftlich bestätigen."),
                 ("Rohrzug reinigen", "Ist der Rohrzug nicht gereinigt, molchen wir ihn vorher."),
                 ("Beide Enden verschließen", "Mit Prüfblasen oder mechanischen Rohrverschlüssen, passend zum Innendurchmesser und zum Prüfdruck."),
                 ("Anfangsdruck aufbringen", "Etwa zehn Prozent über dem Prüfdruck. Die Prüfzeit beginnt erst, wenn der Druck gleichmäßig verläuft."),
                 ("Prüfzeit messen", "Auf Prüfdruck absenken, die Prüfzeit nach Norm einhalten, den Druckabfall mit dem zulässigen Wert vergleichen.")])
        + "<h3>Wenn der Druck stärker abfällt als zulässig</h3><p>Zuerst prüfen wir Verschlüsse und Anschlüsse und wiederholen die Prüfung. Bleibt der Druckabfall zu hoch, wird der Prüfabschnitt als nicht bestanden dokumentiert und Ihnen gemeldet.</p>" + INSPEKT_LINK, alt=True)
    + sec("Ein Protokoll je Prüfabschnitt, mit Druckverlauf",
        "<p>Das Protokoll ist eine Grundlage für die Freigabe zum Kabelzug.</p><h3>Im Protokoll steht</h3>"
        + ul(["Protokollnummer, ausführender Betrieb, Baustelle, Auftraggeber, Bauleiter und Prüfer", "Prüfart (Vorprüfung oder Abnahmeprüfung), Prüfverfahren und Prüfdruck",
              "Rohrwerkstoff, Rohrtyp, Rohrkennung, Länge, Start- und Zielschacht", "Messgerät mit Messbereich, Seriennummer und Kalibrierdatum",
              "Beginn und Ende der Prüfung, Dauer von Beruhigungszeit und Prüfzeit", "Druck nach Beruhigungszeit und nach Prüfzeit, zulässiger und gemessener Druckabfall",
              "Ergebnis und Druckverlauf", "Unterschrift"])
        + "<h3>Rohrnummerierung</h3><p>Vor Arbeitsbeginn legen wir mit Ihnen fest, wie die Rohre an beiden Enden des Rohrzugs nummeriert werden, mit Blickrichtung und Nullpunkt.</p>")
    + sec("Prüfdruck und zulässiger Druckabfall",
        "<p>DIN EN 1610 kennt vier Verfahren für die Prüfung mit Luft. Sie unterscheiden sich im Prüfdruck und im zulässigen Druckabfall, die Prüfzeit hängt außerdem vom Durchmesser ab.</p>"
        "<p>Für Kabelschutzrohre nennen die Einbauanleitungen <strong>A 535a</strong> und <strong>A 535b</strong> des Kunststoffrohrverbands einen Prüfdruck von 200 mbar mit Luft, die Einbauanleitung des Rohrherstellers Schöngen dazu einen zulässigen Druckabfall von 15 mbar. Das entspricht <strong>Verfahren LD</strong>.</p>"
        + tbl(["Verfahren", "Prüfdruck", "zulässiger Druckabfall", "Prüfzeit"], [["LA", "10 mbar", "2,5 mbar", "5 min"], ["LB", "50 mbar", "10 mbar", "4 min"], ["LC", "100 mbar", "15 mbar", "3 min"], ["LD", "200 mbar", "15 mbar", "1,5 min"]],
              "Luftprüfung nach DIN EN 1610, Prüfzeiten für DN 100 bis DN 200, Rohre aus Kunststoff. Für andere Durchmesser gelten die Werte nach Tabelle 3 der Norm.")
        + "<p>Die Baufachlichen Richtlinien Abwasser des Bundes weisen darauf hin, dass die hohe Messempfindlichkeit von LA und LB bei Störungen von außen zu Messungenauigkeiten führen kann. Sie empfehlen für die Prüfung mit Luft ausschließlich LC oder LD.</p>", alt=True)
    + sec("Was die Druckprüfung nachweist und was nicht", NOT(["freiem Querschnitt und Verformung", "Sauberkeit des Rohres", "Lage einer Undichtheit", "Lagegenauigkeit des Rohres", "Werkstoffzustand"], ""))
    + sec("In dieser Reihenfolge arbeiten wir", ORDER + ORDER_TXT, alt=True)
    + sec("Was Sie bereitstellen", "<p>Damit der Termin hält, muss vorab Folgendes geklärt sein.</p>" + ul([
        "Prüfverfahren und Prüfdruck vorgegeben oder freigegeben", "Rohrwerkstoff, Außendurchmesser und Wanddicke bekannt",
        "Angabe, ob vor dem Verfüllen oder als Abnahmeprüfung nach dem Verfüllen geprüft wird", "Rohrzug gereinigt, oder die Reinigung ist mitbeauftragt",
        "Rohrenden an beiden Seiten zugänglich, offen und entgratet", "befahrbare Aufstellfläche für die Luftversorgung am Startende",
        "eindeutige Rohrnummerierung an beiden Enden, oder die Kennzeichnung ist mitbeauftragt", "Ihre Freigabe, falls in Schächte eingestiegen werden muss"]))
    + sec("Leistungsverzeichnis und Vergabe", "<p>Leistungsverzeichnisse im Kabelleitungstiefbau verweisen für die Dichtheitsprüfung meist auf DIN EN 1610. Im STLB-Bau steht eine Position dazu im Leistungsbereich 009 Entwässerungskanalarbeiten, Abrechnungseinheit ist der Meter.</p>", alt=True)
    + sec("Fragen zur Druckprüfung", faq([
        ("Welches Prüfverfahren ist das richtige?", "Das, was Ihr Leistungsverzeichnis vorgibt. Die Einbauanleitungen für Kabelschutzrohre nennen 200 mbar Prüfdruck bei 15 mbar zulässigem Druckabfall, das entspricht Verfahren LD. Ohne Vorgabe prüfen wir nach LC oder LD."),
        ("Gilt DIN EN 1610 überhaupt für Kabelschutzrohre?", "Formal nicht, sie ist eine Abwassernorm. Die Rohrhersteller verweisen in ihren Einbauanleitungen für Kabelschutzrohre trotzdem auf sie. Wir prüfen mit den Parametern dieser Norm, sofern Sie nichts anderes vorgeben.")]))
    + request("Druckprüfung anfragen"))

RT_KALIB = (
    r_hero("Kalibrierung von Kabelschutzrohren", "Nachweis der Profilfreiheit vor dem Kabelzug, nach vereinbartem Kalibermaß.",
           ["Kalibermaß nach Vorgabe des Auftraggebers", "Protokoll je Rohrzug", "Zugseil auf Wunsch im selben Durchgang"], "kalibrierung", "Kalibrierung anfragen")
    + sec("Wann kalibriert wird", "<p>Nach dem Verlegen und Verfüllen kann ein Rohr verformt sein, eine Muffe verschoben oder Material im Rohr festsitzen. Die Kalibrierung weist nach, dass der freie Querschnitt über die ganze Länge mindestens dem vereinbarten Maß entspricht. Das Ergebnis steht je Rohrzug im Protokoll, bevor das Kabel kommt.</p>"
        + tbl(["Anlass", "Warum"], [
            ["Nach Verlegung und Verfüllung der Leerrohranlage", "Bodenverdichtung kann das Rohr verformen oder die Muffen verschieben."],
            ["Vor dem Kabeleinzug oder Kabeleinblasen", "Nachweis, dass der Querschnitt im Kalibermaß für das vorgesehene Kabel frei ist."],
            ["Nach einer Spülbohrung oder Querung", "Die Zugkräfte beim Einziehen des Rohres können es ovalisieren."],
            ["Bei Übernahme einer fremd verlegten Anlage", "Ein Nachweis durch Dritte vor der Abnahme."],
            ["Bei Bestandsrohren vor einer Neubelegung", "Der Zustand ist unbekannt."]]))
    + sec("Kalibrierdorn mit Treibmolch, geschoben mit Druckluft",
        "<p>Wir führen einen Kalibrierdorn mit festem Durchmesser durch den Rohrzug. Der Dorn liegt lose im Rohr und dichtet nicht ab, deshalb läuft hinter ihm ein beschichteter Treibmolch, den die Druckluft schiebt. Kommt der Dorn am anderen Ende an, ist die Profilfreiheit nachgewiesen.</p>"
        "<p>Wir kalibrieren Kabelschutzrohre und Leerrohre aus Kunststoff, etwa PE-HD, PVC-U und PP. Dorn und Treibmolch wählen wir passend zu Innendurchmesser und Kalibermaß.</p>"
        + steps([("Kalibermaß festlegen", "Schriftlich und vor dem ersten Durchgang."), ("Rohrzug reinigen", "Ist der Rohrzug nicht gereinigt, molchen wir ihn vor dem Kalibrieren."),
                 ("Dorn und Treibmolch koppeln", "Der Dorn läuft vorn, der Treibmolch dahinter. Soll ein Zugseil eingezogen werden, hängt es am Treibmolch."),
                 ("Mit Druckluft einschießen", "Wir bauen den Druck langsam auf. Steigt er weiter und tritt am Zielende keine Luft aus, steckt der Dorn, und wir brechen ab."),
                 ("Dorn am Zielende prüfen", "Riefen oder Abrieb am Dorn halten wir im Protokoll als Hinweis fest. Das Ergebnis bleibt durchgängig, der Hinweis zeigt aber, dass der Dorn unterwegs angelegen hat.")])
        + "<h3>Wenn der Dorn nicht durchkommt</h3><p>Bleibt der Dorn stecken, lassen wir den Druck ab und erhöhen ihn nicht. Der Rohrzug wird als nicht durchgängig dokumentiert und Ihnen gemeldet, das weitere Vorgehen stimmen wir mit Ihnen ab.</p><p>Woran es liegt, zeigt eine <a href=\"/kamerabefahrung.html\">Kamerabefahrung</a>.</p>", alt=True)
    + sec("Ein Protokoll je Rohrzug, mit eindeutiger Aussage",
        "<p>Das Protokoll ist eine Grundlage für die Freigabe zum Kabelzug. Deshalb steht darin, ob der Rohrzug durchgängig ist oder nicht.</p><h3>Im Protokoll steht</h3>"
        + ul(["Bauvorhaben, Auftraggeber, ausführender Betrieb, Datum, Uhrzeit und Bearbeiter", "Rohrkennung nach dem vereinbarten Schema, Anfang und Ende des Abschnitts, Länge laut Unterlagen des Auftraggebers",
              "Werkstoff, Außendurchmesser, Wanddicke und Innendurchmesser", "Kalibermaß, Kaliberlänge und Anteil am Innendurchmesser", "Verfahren (Druckluft mit Treibmolch)",
              "Ergebnis und Zustand des Dorns nach dem Durchgang", "bei Seileinzug Seilart, eingezogene Länge und Kennzeichnung beider Enden", "Unterschrift"])
        + "<h3>Rohrnummerierung</h3><p>Vor Arbeitsbeginn legen wir mit Ihnen fest, wie die Rohre an beiden Enden des Rohrzugs nummeriert werden, mit Blickrichtung und Nullpunkt.</p>")
    + sec("Das Kalibermaß ist eine Vereinbarung",
        "<p>Das Kalibermaß richtet sich nach dem Kabel, das später eingezogen wird. Die Einbauanleitung A 535b des Kunststoffrohrverbands für PE-HD-Kabelschutzrohre der Telekommunikation nennt dafür keine Zahl. Sie verlangt, das Kaliber „in Abhängigkeit der vorgesehenen Belegung des Kabelschutzrohres mit dem Auftraggeber abzustimmen“. Fast wortgleich steht das in der Einbauanleitung des Rohrherstellers Schöngen für Kabelschutzrohre aus PVC-U, PE-HD und PP.</p>"
        "<p>Die Handreichung des Bundesministeriums für Digitales und Verkehr zur Qualitätssicherung beim Glasfaserausbau nennt rund 85 Prozent des Rohrinnendurchmessers. Ist die ZTV TK Netz 40 oder ein anderes Regelwerk Vertragsgrundlage, gilt das Maß aus Ihren Vertragsunterlagen.</p>"
        "<p>Das Maß entscheidet, was als Befund gilt. Bei 141 mm Innendurchmesser liegen zwischen einem Kaliber von 80 und einem von 90 Prozent rund 14 mm. Das Maß, mit dem wir rechnen, steht deshalb im Angebot.</p>"
        + tbl(["Außen-Ø × Wand", "Innen-Ø", "80 %", "85 %", "90 %"], [["110 × 3,2", "103,6", "82,9", "88,1", "93,2"], ["110 × 5,3", "99,4", "79,5", "84,5", "89,5"], ["110 × 10,0", "90,0", "72,0", "76,5", "81,0"],
              ["160 × 9,5", "141,0", "112,8", "119,9", "126,9"], ["200 × 9,6", "180,8", "144,6", "153,7", "162,7"], ["225 × 10,8", "203,4", "162,7", "172,9", "183,1"], ["250 × 12,5", "225,0", "180,0", "191,3", "202,5"]],
              "Rechenbeispiele, alle Maße in mm, Kalibermaße auf 0,1 mm gerundet."), alt=True)
    + sec("Was die Kalibrierung nachweist und was nicht", NOT(["Dichtheit", "Lagegenauigkeit des Rohres", "Biegeradien der Trasse und Zugkräfte beim späteren Kabelzug", "Werkstoffzustand", "Ablagerungen, an denen der Dorn vorbeikommt", "Lage und Aussehen einer Engstelle"], ""))
    + sec("In dieser Reihenfolge arbeiten wir", ORDER + ORDER_TXT, alt=True)
    + sec("Was Sie bereitstellen", "<p>Damit der Termin hält, muss vorab Folgendes geklärt sein.</p>" + ul([
        "Kalibermaß schriftlich vorgegeben oder freigegeben", "Rohrwerkstoff und Innendurchmesser bekannt, aus Außendurchmesser und Wanddicke oder aus dem Datenblatt",
        "Rohrzug gereinigt, oder die Reinigung ist mitbeauftragt", "Rohrenden an beiden Seiten zugänglich und offen", "befahrbare Aufstellfläche für unseren Kompressor am Startende",
        "eindeutige Rohrnummerierung an beiden Enden, oder die Kennzeichnung ist mitbeauftragt", "Ihre Freigabe, falls in Schächte eingestiegen werden muss"]))
    + sec("Leistungsverzeichnis und Vergabe",
        "<p>Die Leistung fällt unter die Position „Kalibrieren – Kabelkanalanlagen“ im STLB-Bau (Ausgabe 2026-04), Leistungsbereich 051 Kabelleitungstiefbauarbeiten, Kennung 3711. Als Beispieltext nennt die Position „Kalibrieren der Kabelkanalanlage zur Beurteilung der Profilfreiheit, mit Kalibermolch, Kabelschutzrohr aus PVC-U, DN 100, Zugang vom Schacht“. Abrechnungseinheit ist der Meter.</p>"
        "<p>Der Beispieltext nennt kein Kalibermaß, es sollte deshalb in der Leistungsbeschreibung ausdrücklich festgelegt sein.</p>"
        "<p>Die ATV DIN 18322 führt in Abschnitt 4.2 das „Kalibrieren und Reinigen bestehender Rohrstrecken“ als Besondere Leistung. Das Kalibrieren sollte deshalb als eigene Position ausgeschrieben sein.</p>", alt=True)
    + sec("Fragen zur Kalibrierung", faq([
        ("Welches Kalibermaß gilt?", "Das, was mit dem Auftraggeber vereinbart wird. Die Einbauanleitung A 535b des Kunststoffrohrverbands und die des Rohrherstellers Schöngen nennen kein festes Maß, sie verlangen eine Abstimmung nach der vorgesehenen Belegung. Die Handreichung des Bundesministeriums für Digitales und Verkehr zur Qualitätssicherung beim Glasfaserausbau nennt rund 85 Prozent des Rohrinnendurchmessers."),
        ("Ersetzt die Kalibrierung eine Kamerabefahrung?", "Nein. Die Kalibrierung sagt, ob ein Körper mit dem vereinbarten Durchmesser durch den Rohrzug kommt. Wo eine Engstelle liegt und wie sie aussieht, zeigt erst die Kamerabefahrung. Die Dichtheit weist keine der beiden nach, dafür ist die Druckprüfung da."),
        ("Kann das Zugseil im selben Durchgang eingezogen werden?", "Ja, auf Wunsch. Das Seil hängt am Treibmolch hinter dem Dorn, beide Enden werden gesichert und mit der Rohrnummer gekennzeichnet. Seilart und Durchmesser richten sich nach Ihrer Vorgabe. Soll der Rohrzug auch druckgeprüft werden, machen wir die Druckprüfung vorher.")]))
    + request("Kalibrierung anfragen"))

RT_KAMERA = (
    r_hero("Kamerabefahrung von Rohren und Leitungen", "Der Blick ins Rohr: als Nachweis vor dem Kabeleinzug und als Ursachensuche nach einer auffälligen Prüfung.",
           ["Befund mit Positionsangabe", "Live-Bild, Bewertung direkt vor Ort", "Aufnahmen zur Weitergabe an Bauleitung und Auftraggeber"], "kamerabefahrung", "Kamerabefahrung anfragen")
    + sec("Zwei Fragen, für die wir ins Rohr fahren",
        "<p>Kalibrierung und Druckprüfung sagen, ob der Querschnitt passt und ob das Rohr dicht ist. Sie zeigen nicht, <strong>was</strong> und <strong>wo</strong> ein Problem sitzt. Dafür befahren wir das Rohr mit der Kamera.</p>"
        '<ul class="cards"><li class="card"><h3>Nachweis: Ist die Leitung in Ordnung?</h3><p>Vor dem Kabeleinzug, vor der Inbetriebnahme, für die Abnahme. Die Innenwand wird über die gesamte Länge dokumentiert, Auffälligkeiten bleiben mit Positionsangabe auffindbar.</p></li>'
        '<li class="card"><h3>Diagnose: Warum hält die Leitung den Druck nicht?</h3><p>Nach einer auffälligen Druck- oder Dichtheitsprüfung. Auffällige Stellen fahren wir gezielt an, bis der Befund eindeutig ist, statt die Trasse auf Verdacht aufzugraben.</p></li></ul>')
    + sec("Warum der Blick ins Rohr sich lohnt",
        "<p>Sobald ein Rohr lang und eng ist, endet die Sichtprüfung. Ohne optische Prüfung passieren teure und schwer rückgängig zu machende Schritte wie Kabeleinzug oder Inbetriebnahme ins Ungewisse. Zeigt die Druckprüfung einen Abfall, steht der Befund fest, die Ursache nicht. Ohne Blick ins Rohr bleibt nur, den Abschnitt einzugrenzen und auf Verdacht aufzugraben.</p>"
        "<p>Eine nachträgliche Aufgrabung, ein verkeiltes Kabel oder eine undichte Verbindung nach der Inbetriebnahme kosten ein Vielfaches. Der Blick ins Rohr kostet einen Bruchteil davon, vorher als Nachweis, hinterher als Diagnose.</p>", alt=True)
    + sec("Ursachensuche nach auffälliger Prüfung",
        "<p>Eine auffällige Druck- oder Dichtheitsprüfung liefert eine Zahl, aber keine Position und keine Ursache. Bleibt es beim Befund „undicht“, steht die Bauleitung vor der Frage, an welcher Muffe sie den Bagger ansetzt. Diese Lücke schließen wir mit einem Blick von innen, bevor der erste Meter geöffnet wird.</p>"
        + steps([("Einmal zentriert durch", "Der Kamerakopf wird durch die Leitung gezogen. Das Bild läuft live an der Oberfläche mit, auffällige Abschnitte werden im selben Moment markiert."),
                 ("Dann gezielt anschwenken", "Die markierten Stellen fahren wir erneut an und untersuchen sie, bis der Befund eindeutig benannt ist."),
                 ("Befund mit Meterangabe", "Sie bekommen die Liste der Stellen, an denen sich das Öffnen lohnt, und die Abschnitte, an denen es sich erübrigt. Weil das Bild live anliegt, kann Ihre Bauleitung noch vor Ort entscheiden.")]))
    + sec("Was wir sehen – und was nicht",
        "<h3>Zuverlässig sichtbar</h3>" + ul(["Spitzende nicht bis zur Einstecktiefenmarkierung eingesteckt", "Spalt, Versatz oder Abwinkelung an der Steckmuffe",
              "Ablagerungen und eingedrungenes Bodenmaterial an der Rohrsohle", "Fremdkörper, Riefen, Deformation", "Zustand der Schweißnähte", "die Rohrwand unter klarem Wasser"])
        + "<h3>Nicht sichtbar</h3>" + ul(["eine Undichtigkeit ohne Spur an der Innenwand", "ein Haarriss ohne Wassereintritt", "alles hinter trübem Wasser oder aufgewühltem Sediment", "Wandstärke und Materialkennwerte"])
        + "<p>Die Grenze ist die Sicht, nicht die Nässe: Wasser im Rohr stört nicht, solange es klar ist. Wir dokumentieren, was das Bild hergibt, und halten fest, welche Abschnitte beurteilbar waren und welche nicht. Wir ersetzen keine Druckprüfung, wir erklären ihr Ergebnis. Bleibt nach der Befahrung kein sichtbarer Befund, sagen wir das und empfehlen ein ergänzendes Verfahren.</p>", alt=True)
    + sec("Was Sie bereitstellen und was Sie bekommen",
        "<p>Die Leitung sollte außer Betrieb, befahrbar und im Wesentlichen frei von stehendem Wasser und losem Material sein, mit Zugang an den Rohrenden. Ist vorher gemolcht und gereinigt worden, ist das Ergebnis deutlich aussagekräftiger. Die Machbarkeit, auch bei Bögen, stimmen wir vorab ab.</p>"
        "<p>Sie erhalten die Aufnahmen der Befahrung als prüf- und teilbare Dokumentation, jede Auffälligkeit mit Positionsangabe, zur Weitergabe an Bauleitung und Auftraggeber. Format und Aufbau der Übergabe stimmen wir auf Ihren Abnahmeprozess ab.</p>")
    + sec("Fragen zur Kamerabefahrung", faq([
        ("Ersetzt die Kamerabefahrung Kalibrierung oder Druckprüfung?", 'Nein. <a href="/kalibrierung.html">Kalibrierung</a> und <a href="/druckpruefung.html">Druckprüfung</a> bleiben für Querschnitt und Dichtheit zuständig, beides übernehmen wir ebenfalls. Die Kamera zeigt, wie es im Rohr tatsächlich aussieht, und verortet die Stelle.'),
        ("Gibt es ein Live-Bild während der Befahrung?", "Ja. Befunde lassen sich direkt vor Ort mit Ihrer Bauleitung bewerten."),
        ("Kann die Kamera alles erkennen?", "Nein, und das sagen wir vorab. Wir sehen, was optisch sichtbar ist. Eine offene oder verschobene Muffe, ein Spalt, ein Riss, eindringendes Wasser oder Bodenmaterial sind zuverlässig erkennbar. Ein Haarriss in der Rohrwand oder eine Stelle unter trübem Wasser lässt sich nicht sicher zeigen. In solchen Fällen grenzen wir mit dem Bild den Bereich ein, die abschließende Bewertung bleibt bei Ihrer Prüfstelle."),
        ("Wie läuft eine Anfrage ab?", "Sie schildern uns Leitungstyp, Trasse, Rohranzahl, Durchmesser und Termin. Wir prüfen die Machbarkeit und schicken ein konkretes Angebot.")]))
    + request("Kamerabefahrung anfragen"))

PAGES = {
    "rohrtechnik": ("Rohrservice an Kabelschutzrohren – IGK Abwassertechnik GmbH", "Molchreinigung, Druckprüfung, Kalibrierung und Seileinzug an Kabelschutzrohren und Leerrohren", RT_UEBERSICHT),
    "druckpruefung": ("Druckprüfung von Kabelschutzrohren – IGK Abwassertechnik GmbH", "Dichtheitsprüfung von Kabelschutzrohren mit Luft nach DIN EN 1610, mit Protokoll je Prüfabschnitt", RT_DRUCK),
    "kalibrierung": ("Kalibrierung von Kabelschutzrohren – IGK Abwassertechnik GmbH", "Nachweis der Profilfreiheit von Kabelschutzrohren vor dem Kabelzug", RT_KALIB),
    "kamerabefahrung": ("Kamerabefahrung von Rohren – IGK Abwassertechnik GmbH", "Kamerabefahrung als Nachweis vor dem Kabeleinzug und zur Ursachensuche nach auffälliger Prüfung", RT_KAMERA),
    "index": ("IGK Abwassertechnik – Rohr- und Kanaldienstleistungen", "Rohr- und Kanaldienstleistungen für Kommunen, Industrie und Privat", INDEX),
    "karriere": ("Karriere – IGK Abwassertechnik GmbH", "Offene Stellen bei der IGK Abwassertechnik GmbH", KARRIERE),
    "ansprechpartner": ("Ansprechpartner – IGK Abwassertechnik GmbH", "Ihre Ansprechpartner bei der IGK Abwassertechnik GmbH", ANSPRECH),
    "impressum": ("Impressum – IGK Abwassertechnik GmbH", "Impressum der IGK Abwassertechnik GmbH", legal("", "impressum")),
    "datenschutz": ("Datenschutz – IGK Abwassertechnik GmbH", "Datenschutzerklärung der IGK Abwassertechnik GmbH", legal("", "datenschutz")),
}
for name, (t, d, body) in PAGES.items():
    (R / "site" / f"{name}.html").write_text(HEAD.format(title=t, desc=d) + body + FOOT)
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
