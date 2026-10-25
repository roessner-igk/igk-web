# AGENTS.md – rules for AI agents and new maintainers

Static site. Keep it that way: **plain HTML + CSS, Python stdlib only, no JS framework, no npm, no new dependencies.**
Read `README.md` first for layout and workflow.

## Hard rules
1. Edit `build.py` / `legal/*.frag` / `site/assets/*`, then run `python3 build.py`. Never hand-edit `site/*.html`.
2. Commit generated `site/*.html` with its source change.
3. Do not rewrite `legal/*.frag` (Impressum, Datenschutz) without the client/lawyer; they are copied verbatim from the old site.
4. Never invent business facts (services, numbers, names, certifications, opening hours). Flag drafted copy instead.
5. No secrets in the repo. Registry pull secret lives in the cluster (ExternalSecret), not here.
6. Third-party embeds load only after user consent (YouTube: click-to-load, `youtube-nocookie.com`). Personio iframe on `/karriere` is the one embed; do not add trackers/analytics/web fonts from CDNs (fonts are local).
7. Keep accessibility: alt texts, `lang="de"`, focus-visible, `prefers-reduced-motion`, iframe `title`.
8. Do not push to `main` unless asked; push triggers a production-relevant image build.

## Verify before handing back
```
python3 build.py
docker build -t web-igk . && docker run -d --rm --name web-igk -p 8089:80 web-igk
for p in / /karriere /ansprechpartner /impressum /datenschutz /assets/style.css; do curl -s -o /dev/null -w "$p %{http_code}\n" localhost:8089$p; done
curl -s -o /dev/null -w "404 check %{http_code}\n" localhost:8089/nope   # expect 404
docker stop web-igk
```

## Deployment (current: review host)
- CI: `.github/workflows/docker-publish.yml` → `ghcr.io/samheyna/web-igk:latest` + `sha-<short>` (private package).
- Cluster: Kubernetes context `home-cluster`, GitOps repo `SamHeyna/home-cluster`, path `clusters/home-cluster/apps/staticweb/` (`deployment-igk-website.yaml` = IngressRoute + Service + Deployment, `imagepolicy-igk-website.yaml` = Flux image scan with digest reflection).
- Rollout after push: wait for CI, Flux ImageRepository scans hourly (force: annotate `imagerepository/igk-website` and `imagepolicy/igk-website` in ns `staticweb` with `reconcile.fluxcd.io/requestedAt=<ts>`), Flux commits the new digest.
- Always use `kubectl --context=home-cluster`; never other contexts.
- Review host: `igk.cluster.heyna.cloud` (Traefik IngressRoute, entrypoint `websecure`, rate-limit middleware, public).
- `k8s/` in this repo is a reference copy; the `home-cluster` repo is the source of truth.

## Go-live (next step, not done yet)
1. Decide production domain (e.g. `igk-abwassertechnik.de`) and where DNS is managed; client must repoint DNS.
2. Add production host to the IngressRoute `Host(...)` match (keep or drop the review host); confirm a TLS certificate path for that host (cert-manager had no working ClusterIssuer when checked; verify how existing public hosts like `cv.heyna.cloud` get TLS and copy that).
3. Replicas 2 with podAntiAffinity (see `cv-heyna-website` in the same directory) instead of 1.
4. Remove/adjust review-only points listed in `README.md` → "Open points before go-live" (noindex, legal text review, content confirmation).
5. Add `www` → apex redirect and redirects for old TYPO3 URLs if any should survive (old site had `/ansprechpartner.html`, `/impressum.html`, `/datenschutz.html`; Caddy serves these paths).
6. Verify with `curl -I` for 200 + valid TLS, then monitor.
