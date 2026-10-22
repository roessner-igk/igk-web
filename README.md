# IGK Abwassertechnik – website rebuild
Plain HTML + CSS, served by Caddy in a container (same setup as web-cv).
- `site/` – deployed root (`assets/style.css`, images, icons, team, Inter font)
- `build.py` – generates the 4 pages from shared header/footer; `content/*.frag` = legal text. Run `python3 build.py`
- `original/` – raw mirror of old TYPO3 site (reference only, not in image)
- `Dockerfile`, `Caddyfile`, `k8s/deployment.yaml`, `.github/workflows` – CI builds `ghcr.io/<owner>/<repo>`
- Local test: `docker build -t igk . && docker run --rm -p 8089:80 igk`
