# web-igk – IGK Abwassertechnik website

Static business site for IGK Abwassertechnik GmbH (Lilienthal). Plain HTML + CSS, no framework, no npm.
Served by Caddy in a container; deployed to Kubernetes via Flux.

- Review URL: https://igk.cluster.heyna.cloud
- Repo: `SamHeyna/web-igk` · Image: `ghcr.io/samheyna/web-igk:latest`

## Pages
`/` Start (zwei Kacheln: Wasser, Kabelschutzrohre) → `/wasser`, `/kabelschutzrohre` (Ebene 2: Gruppen als Kacheln) → Gruppenseiten `/<bereich>-<gruppe>` (Ebene 3: Unterpunkte als Icon-Kacheln) → Unterpunktseiten `/<bereich>-<unterpunkt>` · `/karriere` (embedded Personio job portal) · `/ansprechpartner` · `/impressum` · `/datenschutz`

Struktur steht in `build.py` (`AREAS`, `LEAF_TITLES`). Gleiche Namen = gleicher Inhalt: der Inhalt steht einmal (`LEAF_PAGE` bzw. Platzhalter), `build.py` erzeugt die Seite je Bereich, damit Navigation (oben rechts: „Leistungen“ + der andere Bereich) und Einordnung stimmen. Nummerierung/Buchstaben der Strukturvorlage nur intern. Unterpunkte ohne Text sind Platzhalter mit `noindex` (`NOINDEX`). Icons je Unterpunkt: `site/assets/icons/<slug>.svg` (selbst gezeichnet, ersetzbar). `build.py` löscht veraltete `site/*.html`.

## Layout
| Path | Purpose |
|---|---|
| `build.py` | Generates all `site/*.html` from shared header/footer + page bodies (Python stdlib only) |
| `legal/*.frag` | Impressum / Datenschutz body text, inserted verbatim |
| `site/` | Deployed web root. **Generated HTML + hand-edited `assets/`** |
| `site/assets/style.css` | The only stylesheet |
| `site/assets/{images,icons,team,fonts}` | Images, SVG icons, staff photos, Inter font |
| `Dockerfile`, `Caddyfile` | `caddy:2-alpine`, serves `/srv`, gzip/zstd, security headers, clean URLs |
| `.github/workflows/docker-publish.yml` | Push to `main` builds and pushes multi-arch image to GHCR |
| `k8s/` | Reference copy of the manifests (live copy: `home-cluster` repo) |

## Edit workflow
1. Edit text/structure in `build.py` (or `legal/*.frag`), styling in `site/assets/style.css`.
2. `python3 build.py` – regenerates `site/*.html`. **Commit the generated HTML too.**
3. Preview: `docker build -t web-igk . && docker run --rm -p 8089:80 web-igk` → http://localhost:8089
4. Push to `main`. CI builds the image; Flux rolls it out (image digest is picked up automatically).

Never edit `site/*.html` by hand; it is overwritten by `build.py`.

## Open points before go-live
- Kabelschutzrohr-Seiten (`kabelschutzrohre`, `din-en-1610`, `kalibrierung`, `dreh-schwenkkopf-kamera`) mirror structure and headings of hexbee.de/rohrtechnik, /kabelschutzrohr-druckpruefung, /kabelschutzrohr-kalibrierung, /rohrinspektion; texts adapted to IGK, no images/form. Left out: ROHRBLICK/Windenkamera product data, HGÜ reference, Haftpflicht/DSGVO claims, Oldenburg/"bundesweit". Client must confirm IGK offers all services (esp. Seileinzug, Kamerabefahrung), norm refs, STLB/Kalibertabelle, and that hexbee texts may be reused (copyright).
- Seite `sehende-duese` (Reinigung unter optischer Kontrolle) ist sinngemäß nach canal-control.de/…/die-sehende-duese adaptiert, ohne Bilder, Zahlen (DN-Bereich, Reichweite), Ansprechpartner und Firmenaussagen. Kunde muss bestätigen, dass IGK diese Technik (lenkbare Spüleinheit mit Kamera) anbietet, die Leistungsmerkmale stimmen und der Begriff „sehende Düse“ genutzt werden darf; Texte vor Go-live auf Eigenständigkeit prüfen.
- Seite `wasserhoechstdruckfraesen` (Höchstdruck-Wasserstrahlen) ist inhaltlich neu formuliert nach canal-control.de/…/wasserhoechstdruck, ohne Bilder, Nennweiten, Haltungslängen, Geschwindigkeits-/Kostenvergleich und Ansprechpartner. Kunde muss bestätigen, dass IGK Wasserstrahl-Roboter mit Kamera und Kaltschneiden anbietet, welche Einsatzgrenzen gelten und ob der Abtrag der genannten Materialien (u. a. Liner, Beton, Stahl) stimmt.
- Icons (u. a. `wasser`, `kabelschutzrohre`, `kalibrierung`, `seileinzug` und alle Unterpunkte) sind selbst gezeichnet, Ersatz durch Originalgrafiken möglich – client must confirm.
- Bereichs- und Gruppentexte (Startseite, `wasser`, `kabelschutzrohre`) und hero subline are drafted – client must confirm.
- Bestehende Texte `din-en-1610` und `kalibrierung` sind kabelschutzrohr-spezifisch, die Seiten gelten laut Struktur auch für Wasser: inhaltlich anpassen. Alte URLs (`/rohrtechnik`, `/druckpruefung`, `/inspektion`, `/reinigung`, `/hochdruck`, `/din-en-1610` …) leitet der `Caddyfile` weiter, GitHub Pages nicht. Pro Bereich eigene Seiten mit gleichem Inhalt: bei echten Texten Canonical/Duplicate Content bedenken.
- Team photos and video poster are low-res thumbnails from the old TYPO3 site; request originals.
- Impressum still cites "§ 5 TMG" (now DDG) – legal review needed. Datenschutz does not mention Personio (embedded on `/karriere`) – legal review needed.
- Personio iframe has fixed height; fallback link exists for Personio outages.
- Site is currently public and indexable on the review host; add `X-Robots-Tag: noindex` in `Caddyfile` for review, remove for production.
- Old site had no ingress/domain setup for production: see `AGENTS.md` → "Go-live".

## GitHub Pages
Source: Settings → Pages → branch `main`, folder `/docs`. `build.py` writes `docs/` (copy of `site/`, root paths prefixed `/igk-web`). Commit `docs/` with `site/`.
- Interim: https://roessner-igk.github.io/igk-web/
- Custom domain: add file `CNAME` (repo root, one line: domain), run `python3 build.py` (no prefix then), set domain in Settings → Pages, point DNS (CNAME `www` → `roessner-igk.github.io`, apex A records per GitHub docs).

- AGB: Seite `/agb.html` (Link im Footer zwischen Impressum und Datenschutz) ist ein Platzhalter mit noindex. Den AGB-Text liefert der Kunde; er kommt nach `legal/agb.frag`, danach `agb` aus `NOINDEX` in `build.py` entfernen.
