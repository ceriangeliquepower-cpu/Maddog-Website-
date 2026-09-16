# What the audit checks, and why

Every check below traces back to a rule in `CLAUDE.md` unless marked otherwise. If CLAUDE.md's SEO section changes, update `scripts/audit_pages.py` to match — this file should stay in sync with the script, not drift into aspirational documentation.

| Check | Severity | Source |
|---|---|---|
| `<title>` present | Critical | CLAUDE.md SEO — Required on Every Page |
| `<title>` length >65 chars | Warning | CLAUDE.md SEO — 60 char target |
| `<meta name="description">` present | Critical | CLAUDE.md SEO — Required on Every Page |
| Meta description not 140–165 chars | Warning | CLAUDE.md SEO — 150–160 char target |
| `<link rel="canonical">` present | Critical | CLAUDE.md SEO — Required on Every Page |
| Canonical still has `.html` extension | Warning | Site uses clean URLs via Netlify — every other canonical omits it |
| Missing `og:type`/`og:title`/`og:description`/`og:url`/`og:site_name` | Warning | CLAUDE.md SEO — Open Graph block |
| Missing `twitter:card` | Warning | CLAUDE.md SEO — Twitter Card block |
| Missing/non-standard `robots` meta | Warning | CLAUDE.md SEO — Geo + Robots |
| Missing `geo.region` | Info | CLAUDE.md SEO — Geo + Robots |
| No LocalBusiness-family JSON-LD (`SportsActivityLocation`/`MedicalBusiness`/`LocalBusiness`) | Critical | CLAUDE.md SEO — "Every page must also include LocalBusiness JSON-LD" |
| Blog page missing `Article` JSON-LD | Critical | CLAUDE.md Google Crawlability — "Use Article JSON-LD on blog pages" |
| Blog page missing `BreadcrumbList` JSON-LD | Critical | CLAUDE.md Google Crawlability — "Use breadcrumb JSON-LD on all blog pages" |
| "Mad Dog" / "MadDog" / "MADDOG" found in body copy | Critical | CLAUDE.md Design System — "Brand name: Maddog, always, no exceptions" |
| Same match, but inside a standalone `>MADDOG<`-style span | Info | Judgment call — likely a stylized nav/footer wordmark, not body copy; the rule's intent is body copy |
| Wellness page's own schema/meta identifies it as "Maddog Performance Institute" (the gym) | Critical | Found this session — an existing bug (e.g. `og:site_name` on `wellness-blog-genesis-longevity.html`); confirmed with the user that the canonical wellness name is "Maddog Performance Health & Wellness" |
| Gym page mentions the wellness business name | Info | Not necessarily wrong (cross-links exist deliberately) — just worth a human glance |
| Zero or 2+ `<h1>` tags | Critical / Warning | CLAUDE.md Semantic HTML — "one `<h1>` per page" |
| `<img>` with empty or missing `alt` | Warning | CLAUDE.md Image Optimisation — "Every `<img>` must have a descriptive `alt`" |
| Page over 2MB / 800KB | Warning / Info | Not an explicit CLAUDE.md rule, but page weight is a **Core Web Vitals (LCP) ranking risk**, not just a generic performance note — surfaced in its own aggregate report section, not buried per-page. Base64-embedded images are the site's actual, observed cause. As of 2026-09-16, 10 of 53 pages are over 2MB (32.5MB combined) |
| Internal `<a href>` link doesn't resolve to a live 200 | Critical | Never checked before 2026-09-16 — a real gap. Live HTTP check (follows redirects) against every unique internal link target found across all pages |
| Page missing from `sitemap.xml` | Critical | CLAUDE.md Google Crawlability — "sitemap.xml must list all pages" |
| `robots.txt` blocks the site / doesn't reference the sitemap | Critical / Warning | CLAUDE.md Google Crawlability — "robots.txt must allow all crawlers" |
| `_redirects` rule's source path matches a real file but has no force flag (`!`) | Critical | CLAUDE.md Hard-Won Technical Rule #9 — Netlify silently skips the rule in this exact case |
| `_redirects` rule doesn't actually redirect when the real live URL is requested | Critical | Same rule — live HTTP check, catches this AND any other reason a rule could be dead, not just the force-flag case |
| `_redirects` rule returns a non-redirect, non-2xx status live | Warning | Same rule — something else may be wrong (e.g. destination page 404s) |

## Known limitations (not checked, or checked only approximately)

- **Internal link count (2+ per page)** — not currently checked at all. A reliable check needs real link-graph analysis (distinguishing body-content links from repeated nav/footer boilerplate across 50 pages), which regex can't do accurately. Worth a dedicated pass if it becomes a priority, rather than a noisy approximate check.
- **Heading hierarchy skips** (e.g. `<h2>` straight to `<h4>`) — only `<h1>` count is checked, not the full sequence. Worth adding if this turns out to be a real problem on the site.
- **AggregateRating accuracy** — the script doesn't verify `reviewCount` matches the real current review count (CLAUDE.md's Outstanding Work item #3 flags this was last known to be stale — schema showing 8 vs. 9 actual gym reviews). That's a factual data-freshness check, not a structural one — verify manually against Google Business Profile when it matters.
- **Google Business Profile claim status** — out of scope for a code-level scan; already resolved per project memory (both GBPs are claimed).
- **Actual Core Web Vitals measurement (real LCP/INP/CLS numbers)** — this script flags file size as a *proxy risk*, it does not run Lighthouse/PageSpeed Insights or measure real load timing. For real numbers, use Search Console's own Core Web Vitals report or pagespeed.web.dev against the live URL.
- **Google Analytics (GA4) presence** — not currently an automated check in this script (was manually verified once, 2026-09-16, and one gap found/fixed across 2 pages). Worth adding as a real check if it's happened once, it can happen again on a future new page.
- **Search Console's other reports** (Mobile Usability, Security Issues, Manual Actions, Links) — this skill only ever covers the Indexing/Pages report. Those others are separate, un-automated, manual checks — see `~/.claude/skills/site-launch-seo-check/reference/gsc-indexing-checklist.md` for the Indexing procedure; the others don't have a documented procedure yet.
- **Security headers** (CSP, X-Frame-Options, etc.) — not checked, not currently set on this site. Netlify supports these via `_headers` or `netlify.toml` if this becomes a priority.
- **Be explicit about this boundary when reporting "the audit passed"** — say what was checked, not just "everything's fine." A clean run of this script means these specific things are clean, not that literally everything about the site's SEO/ranking health is optimal (see the limitations above).
