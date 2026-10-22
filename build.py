#!/usr/bin/env python3
"""Tiny page builder: shared header/footer + page bodies -> site/*.html. Run: python3 build.py"""
import pathlib
R = pathlib.Path(__file__).parent
FRAG = lambda n: (R / "content" / f"{n}.frag").read_text()

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

KARRIERE = """<section class="wrap section">
  <h1>Karriere</h1>
  <p>Aktuelle Stellenangebote der IGK Abwassertechnik GmbH. Die Bewerbung läuft über unser Karriereportal bei Personio.</p>
  <iframe class="jobs" src="https://igk.jobs.personio.de/?display=de" title="Offene Stellen bei IGK Abwassertechnik" loading="lazy"></iframe>
  <p class="note">Wird die Ansicht nicht geladen? <a href="https://igk.jobs.personio.de/" rel="noopener">Stellenportal in neuem Tab öffnen</a>.</p>
</section>
"""

legal = lambda h, n: f'<section class="wrap section prose">{FRAG(n)}</section>\n'

PAGES = {
    "index": ("IGK Abwassertechnik – Rohr- und Kanaldienstleistungen", "Rohr- und Kanaldienstleistungen für Kommunen, Industrie und Privat", INDEX),
    "karriere": ("Karriere – IGK Abwassertechnik GmbH", "Offene Stellen bei der IGK Abwassertechnik GmbH", KARRIERE),
    "ansprechpartner": ("Ansprechpartner – IGK Abwassertechnik GmbH", "Ihre Ansprechpartner bei der IGK Abwassertechnik GmbH", ANSPRECH),
    "impressum": ("Impressum – IGK Abwassertechnik GmbH", "Impressum der IGK Abwassertechnik GmbH", legal("", "impressum")),
    "datenschutz": ("Datenschutz – IGK Abwassertechnik GmbH", "Datenschutzerklärung der IGK Abwassertechnik GmbH", legal("", "datenschutz")),
}
for name, (t, d, body) in PAGES.items():
    (R / "site" / f"{name}.html").write_text(HEAD.format(title=t, desc=d) + body + FOOT)
print("built", list(PAGES))
