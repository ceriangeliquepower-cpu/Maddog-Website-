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
| Page over 2MB / 800KB | Warning / Info | Not an explicit CLAUDE.md rule, but page weight is a real performance-SEO signal, and base64-embedded images are the site's actual, observed cause (`events.html`, `index.html`, `wellness.html`, `wellness-blog.html` are all multi-hundred-KB-to-multi-MB for exactly this reason) |
| Page missing from `sitemap.xml` | Critical | CLAUDE.md Google Crawlability — "sitemap.xml must list all pages" |
| `robots.txt` blocks the site / doesn't reference the sitemap | Critical / Warning | CLAUDE.md Google Crawlability — "robots.txt must allow all crawlers" |

## Known limitations (not checked, or checked only approximately)

- **Internal link count (2+ per page)** — not currently checked at all. A reliable check needs real link-graph analysis (distinguishing body-content links from repeated nav/footer boilerplate across 50 pages), which regex can't do accurately. Worth a dedicated pass if it becomes a priority, rather than a noisy approximate check.
- **Heading hierarchy skips** (e.g. `<h2>` straight to `<h4>`) — only `<h1>` count is checked, not the full sequence. Worth adding if this turns out to be a real problem on the site.
- **AggregateRating accuracy** — the script doesn't verify `reviewCount` matches the real current review count (CLAUDE.md's Outstanding Work item #3 flags this was last known to be stale — schema showing 8 vs. 9 actual gym reviews). That's a factual data-freshness check, not a structural one — verify manually against Google Business Profile when it matters.
- **Google Business Profile claim status** — out of scope for a code-level scan; already resolved per project memory (both GBPs are claimed).
