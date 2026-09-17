# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Project

Static HTML website for **Maddog Performance Institute** — MMA gym + recovery/wellness centre in Ballito, KZN, South Africa.

- **Live domain:** maddogperformance.co.za — DNS is live on Netlify DNS (nameservers point to Netlify, not the registrar/cPanel)
- **Hosting:** Netlify — all HTML files drop into the same folder, all relative links work as-is
- **Redirects:** `_redirects` (no extension — `_redirects.txt` is a stale unused file, do not edit it) maps clean URLs, `.html → clean-URL` canonicalization (every such rule needs the force flag — see Hard-Won Rule #9), and a few one-off 301s. Verify any change live — see Hard-Won Rule #9.

---

## Architecture

This is a **zero-build, zero-dependency** static site. There is no npm, no bundler, no framework, no server. Every page is a single fully self-contained `.html` file.

**Images are base64-embedded** (PIL-compressed JPEG) directly inside each HTML file. There are no external image files or CDN references. Files are large as a result (up to 7MB per page).

**Fonts** load from Google Fonts CDN (Bebas Neue + Barlow Condensed). This is the only external dependency.

**Photo upload slots** use a browser-side `swapPhoto(slotId)` + `FileReader` API pattern — clicking a `.photo-slot` element opens a file picker, compresses the image, and injects a new base64 `src` into the slot's `<img>`. The `.loaded` class is toggled to reveal the uploaded image and hide the placeholder overlay.

**Saving** is done via `savePage()` which serialises `document.documentElement.outerHTML` into a Blob and triggers a download of the updated HTML file with the new images baked in.

**Testing:** Open any `.html` file directly in a browser (no server needed). All functionality must work via `file://` protocol.

---

## Design System — Non-Negotiable

```
Colors (CSS variables):
  --black:     #080808   ← primary background
  --deep:      #0F0F0F   ← section alternation
  --card:      slightly lighter black for card surfaces
  --gold:      #C9A84C   ← all accents, labels, borders
  --white:     #F5F0E8   ← body text
  --white-dim: dimmed variant of --white for secondary text

Fonts:
  Headings:  'Bebas Neue', sans-serif
  Body:      'Barlow Condensed', sans-serif

Brand name:  "Maddog"  ← always, no exceptions
             NEVER: "Mad Dog" / "MadDog" / "MADDOG" in body copy
```

Section labels use `font-size:9px; font-weight:700; letter-spacing:.35em; text-transform:uppercase; color:var(--gold)`.

---

## Hard-Won Technical Rules

These bugs have already been fixed. Do not revert them.

1. **Never use `*{max-width:100%}` inside media queries** — kills the hero banner animation.
2. **All `.reveal` elements must have `.visible` pre-applied** — scroll-trigger JS is unreliable in standalone files; opacity defaults to 0.
3. **Use inline styles for persistent overrides** — when stylesheet cascade fights you, inline styles on the element win.
4. **Never add `z-index` to hero sections** — causes stacking context conflict with the credential strip.
5. **Hero needs `padding-top`, not `margin-top`** — `margin-top` gets clipped by `overflow:hidden`.
6. **Credential strip: no `position` or `z-index`** — plain block flow only.
7. **`.cred-scroll` must have `width:max-content`** — never override this in media queries.
8. **All images must be base64-embedded** — no `<img src="path/to/file.jpg">` ever. Use PIL-compressed JPEG data URIs.
9. **Every `_redirects` rule whose source path matches a real file in this repo needs the force flag (`!`)** — e.g. `/amanda.html /amanda 301!`, not `301`. Netlify silently skips an unforced redirect rule when a file exists at that exact path, and every `.html` page here IS such a file. This caused a 13-day incident (Sept 2026) where 30 committed, deployed redirect rules did nothing, stalling 41 pages out of Google's index — see `_redirects` for the current state and [[project_redirect_indexing_fix]] in memory for the full story. **Never trust a redirect rule because it's committed or deployed — verify it live** with `curl -I <url>` (expect `301`/`302`, not `200`) or run `py .claude/skills/maddog-seo-audit/scripts/audit_pages.py`, which live-tests every rule automatically. Do this after touching `_redirects` for any reason, and after adding any new page.
10. **Every `swapPhoto()` implementation must compress via canvas before storing — never store the raw `FileReader.readAsDataURL()` result directly.** Discovered 2026-09-17: the wellness pages and `coaches.html` had a canvas resize+compress step (max 1200px long edge, JPEG quality 0.78, target ≤200KB) but the other 32 gym-site pages were still storing the raw, uncompressed upload straight into `window._photoStore` and the page's `<img src>` — meaning any photo uploaded through those pages could add several MB of uncompressed base64 to that page, silently undoing the Core Web Vitals image-migration work. Fixed by porting the compression step to all 32 remaining pages (see `add_photo_compression.py`, kept for reference). **Any new page built from a template must be checked for this** — grep the page for `function swapPhoto` and confirm `canvas` appears in it before considering a new page done. See also [[photo_workflow]] in memory for the separate (and still-manual) "Save Page download → replace project file → push" step this doesn't change.
11. **Netlify serves every file in this repo root as a live, downloadable URL unless a `_redirects` rule blocks it — internal files are public by default, not private by default.** This site has no build step (`publish = "."` in `netlify.toml`), so any doc, script, or SQL file committed to git becomes servable the moment it's pushed, whether or not any page links to it. Discovered 2026-09-17: `CLAUDE.md`, internal handoff docs (`GO_LIVE_CHECKLIST.md`, `SESSION_HANDOFF.md`, `MADDOG_CLAUDE_CODE_HANDOFF.md`), dev scripts (`.py`/`.ps1`), Supabase SQL migrations, the old `stripped/` working-copy folder, and even `hooks/pre-push` had all been publicly downloadable for an unknown period — some had a `_redirects` block rule that *looked* correct but was silently broken by the exact same missing-force-flag bug as Rule #9 above. Fixed by adding force-flagged 404 rules for every internal file/folder (see `_redirects`, the "Block public access to internal tooling" section). **Whenever a new internal file is added to the repo root** (a script, a doc, a report, anything that isn't meant to be a live page), add a matching forced 404 rule to `_redirects` in the same commit, and verify it live with `curl -I <url>` — don't assume a rule works because it's there; Rule #9's lesson applies here too.

---

## Page Map

**53 live pages total** (last verified 2026-09-17 against the actual file listing — if this count doesn't match `ls *.html | grep -v TEMPLATE | wc -l`, this section has drifted again and needs re-syncing).

**Gym site — core (8):** `index.html` (homepage) · `amanda.html` (bio + fight record) · `athletes.html` (fighter roster) · `coaches.html` (coach profiles) · `training.html` (discipline hub) · `recovery.html` (recovery suite) · `events.html` (events + blog index) · `contact.html` · `booking.html`

**Gym site — training discipline pages (11, served at pretty `/training/...` URLs via `_redirects`):** `training-mma-ballito.html` · `training-bjj-ballito.html` · `training-kids-bjj-ballito.html` · `training-kickboxing-ballito.html` · `training-boxing-ballito.html` · `training-womens-boxing-ballito.html` · `training-kids-boxing-ballito.html` · `training-olympic-boxing-ballito.html` · `training-bootcamp-ballito.html` · `training-powerlifting-ballito.html` · `training-personal-training-ballito.html`

**Gym site — blog posts (9, linked from `events.html`):** `blog-mma-training-ballito.html` · `blog-bjj-beginners-ballito.html` · `blog-youth-mma-training-ballito.html` · `blog-powerlifting-women-ballito.html` · `blog-cold-plunge-sauna-ballito.html` · `blog-amanda-kobus-coach-ballito.html` · `blog-robin-jj-williams-physio-ballito.html` · `blog-efc-134-amanda-lino-title-defence.html` · `blog-efc-134-amanda-lino-vs-juliet-chukwu.html` · `blog-womens-self-defence-workshop-ballito.html` · `blog-womens-self-defence-workshop-recap-ballito.html` · `blog-ballito-community-raises-funds-st-lukes.html` · `blog-genesis-athlete-recovery-ballito.html`

**Wellness site — separate business, own site (see [[project_business_separation]] in memory), core (13):** `wellness.html` (homepage) · `wellness-iv.html` · `wellness-body.html` · `wellness-recovery.html` · `wellness-physiotherapy-ballito.html` · `wellness-inbody-scan-ballito.html` · `wellness-nad-iv-ballito.html` · `wellness-cold-plunge-ballito.html` · `wellness-infrared-sauna-ballito.html` · `wellness-pricing.html` · `wellness-personal-training-ballito.html` · `wellness-contact.html` · `wellness-blog.html` (index)

**Wellness site — blog posts (6):** `wellness-blog-iv-therapy.html` · `wellness-blog-physiotherapy.html` · `wellness-blog-cold-plunge.html` · `wellness-blog-genesis-longevity.html` · `wellness-blog-womens-self-defence.html` · `wellness-blog-womens-wellness-day-recap.html`

Full URL list (clean/pretty forms) is authoritative in `sitemap.xml` — cross-check there, not just this list, before assuming a page is missing or extra.

---

## Outstanding Work (Priority Order)

**Rewritten 2026-09-17 — the previous version of this list was entirely stale** (pricing.html was superseded by `wellness-pricing.html`, Slimming Clinic/contrast-therapy content is already live site-wide, AggregateRating schema is on 36 pages, BreadcrumbList is on every blog page, DNS has been live for a while). Verify against live state before trusting this list too, next time it's read — see the "Keep this file honest" section below.

1. **Search Console indexing queue** — 41 pages were stuck "discovered, not indexed" due to the redirect bug (fixed & live 2026-09-16, see [[project_redirect_indexing_fix]] in memory). Submitting via Search Console: Inspect URL (top search bar) → Request Indexing, one quota-limited batch (~10/day) at a time. **10 done so far, 31 still outstanding** — full checklist below, check items off here as they're submitted so this list stays the source of truth (not a separate memory file):

   **Still to submit (31):**
   - [ ] `https://www.maddogperformance.co.za/wellness-cold-plunge-ballito`
   - [ ] `https://www.maddogperformance.co.za/wellness-infrared-sauna-ballito`
   - [ ] `https://www.maddogperformance.co.za/amanda`
   - [ ] `https://www.maddogperformance.co.za/athletes`
   - [ ] `https://www.maddogperformance.co.za/coaches`
   - [ ] `https://www.maddogperformance.co.za/booking`
   - [ ] `https://www.maddogperformance.co.za/recovery`
   - [ ] `https://www.maddogperformance.co.za/training/bootcamp-ballito`
   - [ ] `https://www.maddogperformance.co.za/training/kids-boxing-ballito`
   - [ ] `https://www.maddogperformance.co.za/training/olympic-boxing-ballito`
   - [ ] `https://www.maddogperformance.co.za/training/powerlifting-ballito`
   - [ ] `https://www.maddogperformance.co.za/training/womens-boxing-ballito`
   - [ ] `https://www.maddogperformance.co.za/blog-amanda-kobus-coach-ballito`
   - [ ] `https://www.maddogperformance.co.za/blog-bjj-beginners-ballito`
   - [ ] `https://www.maddogperformance.co.za/blog-cold-plunge-sauna-ballito`
   - [ ] `https://www.maddogperformance.co.za/blog-iv-drip-therapy-ballito`
   - [ ] `https://www.maddogperformance.co.za/blog-mma-training-ballito`
   - [ ] `https://www.maddogperformance.co.za/blog-powerlifting-women-ballito`
   - [ ] `https://www.maddogperformance.co.za/blog-robin-jj-williams-physio-ballito`
   - [ ] `https://www.maddogperformance.co.za/blog-womens-self-defence-workshop-recap-ballito`
   - [ ] `https://www.maddogperformance.co.za/blog-youth-mma-training-ballito`
   - [ ] `https://www.maddogperformance.co.za/wellness-contact`
   - [ ] `https://www.maddogperformance.co.za/wellness-inbody-scan-ballito`
   - [ ] `https://www.maddogperformance.co.za/wellness-nad-iv-ballito`
   - [ ] `https://www.maddogperformance.co.za/wellness-personal-training-ballito`
   - [ ] `https://www.maddogperformance.co.za/wellness-pricing`
   - [ ] `https://www.maddogperformance.co.za/wellness-recovery`
   - [ ] `https://www.maddogperformance.co.za/wellness-blog`
   - [ ] `https://www.maddogperformance.co.za/wellness-blog-iv-therapy`
   - [ ] `https://www.maddogperformance.co.za/wellness-blog-physiotherapy`
   - [ ] `https://www.maddogperformance.co.za/wellness-blog-womens-wellness-day-recap`

   **Already submitted (10):** `/training`, `/training/personal-training-ballito`, `/training/mma-ballito`, `/training/bjj-ballito`, `/training/kickboxing-ballito`, `/training/boxing-ballito`, `/training/kids-bjj-ballito`, `/wellness-body`, `/wellness-iv`, `/wellness-physiotherapy-ballito`.

   Resubmitting an already-done URL is harmless (Google's own message: doesn't change queue position), so if it's ever unclear which were done, just continue down the unchecked list rather than trying to figure out exactly where you left off.
2. **Core Web Vitals — font-loading fix** — real PageSpeed data (2026-09-17) showed LCP of 10.2s on mobile even after the image-weight fix, caused by a render-blocking Google Fonts stylesheet. Fix built and verified locally across all 53 pages, not yet pushed — awaiting go-ahead.
3. **E-E-A-T content pass** — credit named coaches (not just "Maddog Marketing") on posts where their specific expertise is the point; state credentials/issuing bodies in text, never raw ID numbers (see Content Gaps below).
4. **Federation/affiliation content** (MMASA etc.) — awaiting client-confirmed details, see Content Gaps below. Specific backlink target already identified: MMA South Africa's affiliated-gyms directory (mma-sa.co.za/affiliated_gyms) lists KZN gyms but not Maddog — pursue getting listed there once affiliation is confirmed, see [[project_mmasa_affiliation_opportunity]] in memory.
5. **Content-Security-Policy header** — deliberately not added yet; needs a careful resource-by-resource audit first given how much inline script/style and third-party embedding this site does. Other security headers already live.
6. **Local SEO / backlinks** — site currently has 1 external backlink total. Client-side relationship work (asking sponsor/partner businesses to link back), not something fixable from the codebase.
7. **Keyword ranking gaps identified (2026-09-17 live-search audit)** — see [[project_keyword_ranking_audit]] in memory for full results. Two actionable patterns: (a) **wellness GBP has far fewer reviews than the gym's GBP** and this is likely suppressing Local Map Pack visibility for sauna/cold-plunge/IV-drip/NAD/body-composition searches even where on-site content already ranks #1 organically — completing the wellness GBP (client doing manually, see [[project_wellness_gbp_incomplete]]) is probably the single highest-leverage fix available; (b) **bootcamp ballito / fitness bootcamp ballito** is a real content/backlink gap — Maddog has `training-bootcamp-ballito.html` but doesn't rank competitively against Fit24, F45, Ballito Fitness Village, HIITMANN, Grit Factory. Named competitors worth tracking: **Ringside Boxing Gym** (beats Maddog on pure boxing terms), **CombatCoaching.com** (new, beats Maddog on self-defence terms), **Grit Factory** (dominant on personal-training terms), **Kico Life / IVology / The IV Bar** (dominant on several wellness terms).

---

## Content Gaps (Awaiting Client)

- Amanda's 6 remaining pro fight results (opponent, event, method, round, result)
- Coach credentials: Luckymore Hamadziripi, Coach Marcele, York Lawrence (formal certs, if not already on-site — verify against current `coaches.html` before asking the client again)
- **Wren's SANC registration number — will NOT be published.** Explicit client decision (2026-09-17): raw registration/certification numbers are never to appear on the site — risk of the number being lifted and used to impersonate/duplicate the credential elsewhere. Bridge instead by stating the credential + issuing body in text only (e.g. "SANC-registered nurse") — the registration status itself is the trust signal Google/visitors need, not the number. This applies to any coach's future certification numbers too, not just Wren's.
- **Federation/foundation affiliations (MMASA and others)** — client is confirming exact affiliation details themselves, to be added once provided. When ready: (1) add a real visible text mention of each affiliation (not just a logo — Google reads text, not images) with matching `alt` text on any badge/logo, (2) check whether the federation's own site/member-directory already lists Maddog back with a link — that external listing is worth more for authority than the claim living only on our own site.
- Training prices: 18 slots currently show POA
- Upcoming event venues + ticket links
- Photos: all pages have click-to-upload slots ready
- **New discipline in progress: Wrestling classes.** Client confirmed 2026-09-17 that Maddog is adding wrestling — no page/content exists yet (no `training-wrestling-ballito.html`). Target keywords already scoped in memory ([[project_keyword_candidate_list]]: wrestling ballito, wrestling classes ballito, wrestling gym near me, youth wrestling ballito, wrestling training ballito). Once client provides coach(es), schedule/pricing, and any credentials, build the page following the same pattern as the other 11 training-discipline pages, then run the full "After Adding Any New Page" workflow below (sitemap, redirects, SEO audit, GSC submission) and add it to the Page Map above.

---

## Keep This File Honest

This file went stale for months (Page Map listed 8 pages when the site had 53; Outstanding Work listed 4 items that were all already done; the redirects filename was wrong) because updating it was never part of finishing a task — only code/content changes were. Don't repeat that.

**Status-bearing sections that go stale** (re-check these after any substantial batch of work, not just when something happens to be noticed): Project intro (hosting/DNS facts), Page Map (page count + list), Outstanding Work, Content Gaps. **Not** status-bearing, safe to treat as durable: Design System, Hard-Won Technical Rules, Semantic HTML/SEO/Image/Accessibility/Performance/Crawlability/Mobile-First rules — those are standards, not a snapshot of current state, and don't need re-verifying just because time passed.

**When to check:** after finishing any multi-page batch of work (a new page type, a site-wide fix, a completed Outstanding Work item) — before calling the batch done, ask "does anything in the status-bearing sections above need updating to match what just happened," the same way `sitemap.xml` and the SEO audit already get checked per the "After Adding Any New Page" section below.

---

## Before Editing Any Page

1. Read the existing file's CSS class names and structure before writing new HTML — match exactly.
2. New sections must use existing CSS classes, not introduce new design patterns.
3. Deliver complete `.html` files, not partial snippets (unless explicitly asked for a snippet).

## After Adding Any New Page, or Touching `_redirects`

Do this before considering the work done — not optional, not "if there's time":

1. Add the new URL to `sitemap.xml`.
2. If the page needs a `.html → clean-URL` redirect, add the rule to `_redirects` **with the force flag** (see Hard-Won Rule #9 above).
3. Run `py .claude/skills/maddog-seo-audit/scripts/audit_pages.py` — it live-tests every redirect rule against the real production domain and flags sitemap gaps. Zero critical findings before moving on.
4. Once the page is live, manually submit it in Search Console (Inspect URL → Request Indexing) rather than waiting on natural crawl — see [[project_gsc_indexing_queue]] in memory for the exact click-path.

This whole loop is what `maddog-seo-audit` exists to make automatic — run it, don't just assume a committed change works. A `hooks/pre-push` git hook also runs the critical-findings check automatically on every push and blocks it if anything's broken (one-time setup per clone: `git config core.hooksPath hooks`) — this is a backstop, not a substitute for running the audit yourself during the work.

---

## Semantic HTML Rules

- Use correct landmark elements: `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<aside>`, `<footer>`.
- Every `<section>` must have a heading (`<h2>` or lower) — no headingless sections.
- Heading hierarchy must be sequential: one `<h1>` per page, then `<h2>`, `<h3>` — never skip levels.
- Use `<button>` for interactive controls, `<a>` only for navigation. Never use `<div onclick>` for buttons.
- Use `<ul>` / `<ol>` for lists of items — not `<div>` stacks.
- Use `<time datetime="...">` for dates and times.
- Use `<address>` for contact details in the footer.

---

## SEO — Required on Every Page

Every `.html` file must include all of the following in `<head>`:

```html
<!-- Primary -->
<title>Page Title | Maddog Performance Institute | Ballito KZN</title>
<meta name="description" content="150–160 char description with primary keyword.">
<link rel="canonical" href="https://www.maddogperformance.co.za/page.html">

<!-- Open Graph (Facebook / WhatsApp previews) -->
<meta property="og:type" content="website">
<meta property="og:title" content="Page Title | Maddog Performance Institute">
<meta property="og:description" content="Same as meta description.">
<meta property="og:url" content="https://www.maddogperformance.co.za/page.html">
<meta property="og:image" content="https://www.maddogperformance.co.za/og-image.jpg">
<meta property="og:site_name" content="Maddog Performance Institute">
<meta property="og:locale" content="en_ZA">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Page Title | Maddog Performance Institute">
<meta name="twitter:description" content="Same as meta description.">
<meta name="twitter:image" content="https://www.maddogperformance.co.za/og-image.jpg">

<!-- Geo + Robots -->
<meta name="robots" content="index, follow">
<meta name="geo.region" content="ZA-KZN">
<meta name="geo.placename" content="Ballito, KwaZulu-Natal">
```

Every page must also include **LocalBusiness JSON-LD** structured data. Minimum required fields: `@type`, `name`, `url`, `telephone`, `address`, `geo`, `openingHours`, `image`, `priceRange`.

---

## Image Optimisation Rules

- All images are **base64-embedded JPEG** — compress with PIL before embedding (target ≤ 200KB per image at quality 72–82).
- Never embed a raw uncompressed PNG or high-res JPEG — always run through PIL first.
- Every `<img>` must have a descriptive `alt` attribute — never `alt=""` for content images. Decorative images only may use `alt=""`.
- Include `width` and `height` attributes on every `<img>` to prevent layout shift (CLS).
- Use `loading="lazy"` on all images that are below the fold.
- Hero / above-the-fold images must NOT have `loading="lazy"` — they must load immediately.
- Use `object-fit: cover` + explicit dimensions on photo slots to prevent reflow.

---

## Accessibility Rules

- Colour contrast must meet WCAG AA: minimum 4.5:1 for body text, 3:1 for large text (18px+ bold or 24px+ normal).
- Every interactive element (`<a>`, `<button>`) must have a visible focus state — never `outline: none` without an alternative.
- All form inputs need a `<label>` associated via `for` / `id`.
- Every `<img>` needs a meaningful `alt` (see Image rules above).
- Navigation must be keyboard-accessible — tab order must follow visual order.
- Use `aria-label` on icon-only buttons (e.g. social media icons, WhatsApp float button).
- Use `aria-expanded` on toggle buttons (e.g. coach bio expand buttons).
- Hamburger menu must toggle `aria-expanded` and trap focus when open.
- Avoid `display:none` or `visibility:hidden` on content that screen readers need — use the visually-hidden pattern instead if required.

---

## Performance Best Practices

- **No render-blocking scripts** — all `<script>` tags go before `</body>`, never in `<head>` (except inline critical CSS).
- **Google Fonts** — use `rel="preconnect"` to `https://fonts.googleapis.com` and `https://fonts.gstatic.com`.
- **CSS animations** — use `will-change` only on actively animating elements (`.cred-scroll`). Remove after animation ends if possible.
- **JS ticker** — driven by CSS animation only, no `requestAnimationFrame` cloning loop (already fixed — do not revert).
- **savePage()** — uses `showSaveFilePicker` + Blob (not `encodeURIComponent` data URI) to avoid memory issues with large files.
- Avoid `@import` inside CSS — use `<link>` tags instead.
- Minimise repaints: prefer `transform` and `opacity` for animations over `top`/`left`/`width`.

---

## Google Crawlability Rules

- Every page must have a unique `<title>` and unique `<meta name="description">`.
- Internal links must use relative paths (`href="coaches.html"`) — they must all resolve correctly from the same folder.
- `sitemap.xml` must list all 13 pages + all 5 blog pages. Update it whenever a new page is added.
- `robots.txt` must allow all crawlers: `User-agent: * / Allow: /`.
- No `noindex` or `nofollow` on public pages.
- Use **breadcrumb JSON-LD** on all blog pages for rich results.
- Use **Article JSON-LD** on blog pages with `datePublished`, `dateModified`, `author`, `image`.
- Anchor text must be descriptive — never "click here" or "read more" without context.
- Every page must link back to at least 2 other internal pages (footer nav counts).
- `<link rel="canonical">` must match the exact live URL to prevent duplicate content issues.

---

## Mobile-First Design Rules

- Write base CSS for mobile (≤ 375px), then use `@media (min-width: …)` to scale up — not the reverse.
- Touch targets must be at least **44×44px** — applies to buttons, nav links, social icons, and phone numbers.
- Font sizes: minimum `14px` for body text on mobile, `11px` for labels/captions.
- Never use `px` for font sizes in media queries — use `clamp()` or relative units.
- The nav must collapse to a hamburger at ≤ 768px.
- No horizontal scroll at any viewport width — test at 320px, 375px, 390px, 428px.
- `overflow-x: hidden` on `body` for mobile — but never on `html` (breaks `position:sticky`).
- Tap-highlight should be suppressed on interactive elements: `-webkit-tap-highlight-color: transparent`.
- Use `env(safe-area-inset-bottom)` for bottom padding on pages with fixed bottom bars (save banner, WhatsApp float).
- Images must be responsive — use `width:100%; height:auto` or explicit `aspect-ratio` to prevent overflow.
