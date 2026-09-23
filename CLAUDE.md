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

**Images are file references, not base64** (migrated 2026-09-17) — every `<img src>` points to `/images/<content-hash>.{jpg,png}`, PIL-compressed before upload. This section used to say base64-embedded; that was the original architecture but is no longer true and this note replaces the stale claim per the "Keep This File Honest" section below. Images are served with long-lived immutable caching (`Cache-Control: max-age=31536000, immutable` in `_headers`, added 2026-09-17) since content-hash filenames never change under the same name — see Image Optimisation Rules.

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
8. **~~All images must be base64-embedded~~ — SUPERSEDED 2026-09-17.** Images were migrated to file references (`/images/<hash>.{jpg,png}`) for Core Web Vitals — this rule is kept struck through, not deleted, so nobody re-reads an old note and reverts the migration. Current rule: images are content-hash-named files with long-lived caching, never base64 — see Architecture and Image Optimisation Rules.
9. **Every `_redirects` rule whose source path matches a real file in this repo needs the force flag (`!`)** — e.g. `/amanda.html /amanda 301!`, not `301`. Netlify silently skips an unforced redirect rule when a file exists at that exact path, and every `.html` page here IS such a file. This caused a 13-day incident (Sept 2026) where 30 committed, deployed redirect rules did nothing, stalling 41 pages out of Google's index — see `_redirects` for the current state and [[project_redirect_indexing_fix]] in memory for the full story. **Never trust a redirect rule because it's committed or deployed — verify it live** with `curl -I <url>` (expect `301`/`302`, not `200`) or run `py .claude/skills/maddog-seo-audit/scripts/audit_pages.py`, which live-tests every rule automatically. Do this after touching `_redirects` for any reason, and after adding any new page.
10. **Every `swapPhoto()` implementation must compress via canvas before storing — never store the raw `FileReader.readAsDataURL()` result directly.** Discovered 2026-09-17: the wellness pages and `coaches.html` had a canvas resize+compress step (max 1200px long edge, JPEG quality 0.78, target ≤200KB) but the other 32 gym-site pages were still storing the raw, uncompressed upload straight into `window._photoStore` and the page's `<img src>` — meaning any photo uploaded through those pages could add several MB of uncompressed base64 to that page, silently undoing the Core Web Vitals image-migration work. Fixed by porting the compression step to all 32 remaining pages (see `add_photo_compression.py`, kept for reference). **Any new page built from a template must be checked for this** — grep the page for `function swapPhoto` and confirm `canvas` appears in it before considering a new page done. See also [[photo_workflow]] in memory for the separate (and still-manual) "Save Page download → replace project file → push" step this doesn't change.
11. **Netlify serves every file in this repo root as a live, downloadable URL unless a `_redirects` rule blocks it — internal files are public by default, not private by default.** This site has no build step (`publish = "."` in `netlify.toml`), so any doc, script, or SQL file committed to git becomes servable the moment it's pushed, whether or not any page links to it. Discovered 2026-09-17: `CLAUDE.md`, internal handoff docs (`GO_LIVE_CHECKLIST.md`, `SESSION_HANDOFF.md`, `MADDOG_CLAUDE_CODE_HANDOFF.md`), dev scripts (`.py`/`.ps1`), Supabase SQL migrations, the old `stripped/` working-copy folder, and even `hooks/pre-push` had all been publicly downloadable for an unknown period — some had a `_redirects` block rule that *looked* correct but was silently broken by the exact same missing-force-flag bug as Rule #9 above. Fixed by adding force-flagged 404 rules for every internal file/folder (see `_redirects`, the "Block public access to internal tooling" section). **Whenever a new internal file is added to the repo root** (a script, a doc, a report, anything that isn't meant to be a live page), add a matching forced 404 rule to `_redirects` in the same commit, and verify it live with `curl -I <url>` — don't assume a rule works because it's there; Rule #9's lesson applies here too.
12. **Netlify's own post-processing rewrites deployed HTML — never compare live-fetched HTML byte-for-byte against source when verifying a push.** Discovered 2026-09-17 during verification of an accessibility fix: the live page reorders attributes, converts double quotes to single quotes, and rewrites internal `.html` links to clean paths (`href="page.html"` → `href='/page'`). A verification script searching for `aria-label="..."` (double quotes, matching the source) found nothing and looked like the fix hadn't deployed — it had; the search pattern was wrong, not the site. **When verifying live content, check for the presence of the actual text/attribute value, not the exact quote style or attribute order from source**, or use a count/substring check instead of an exact string match.
13. **Images need an explicit long-lived `Cache-Control` header — Netlify does not add one automatically just because filenames are content-hashed.** Discovered 2026-09-17: every image had been served with `max-age=0, must-revalidate` (forces a revalidation round-trip on every load) since `_headers` was created in May — invisible while images were base64-embedded (no separate image requests existed), but a real, growing cost once the base64→file-reference migration made every photo its own HTTP request. Fixed with a `/images/*` block in `_headers` setting `public, max-age=31536000, immutable` (safe because a changed photo always gets a new content-hash filename). **Any new static asset directory added to this site should get the same treatment** — check `_headers` before assuming Netlify's defaults are sufficient.
14. **An apostrophe inside a double-quoted HTML attribute can survive source review but break live.** Discovered 2026-09-21: `aria-label="Read more: Women's Self-Defence..."` was perfectly valid source HTML, but Netlify's post-processing (see Rule #12) mishandled the apostrophe while normalizing quote style, inserting a literal backslash that isn't valid HTML escaping — the browser then terminated the attribute early and turned the rest of the words into bogus boolean attributes, silently gutting the aria-label on the live site only. Same root cause hit a `photo-slot` `aria-label` on `athletes.html`. **The robust fix isn't escaping the apostrophe — it's not depending on `aria-label` to carry meaning the visible text doesn't already have.** Prefer descriptive visible link/button text over generic text + a descriptive `aria-label`; where an `aria-label` on its own is unavoidable (e.g. a `role="button"` photo-slot), avoid apostrophes in it (rephrase rather than escape).
15. **Never stack a CSS `opacity` on top of `var(--white-dim)` (or any already-translucent color) for "extra" de-emphasis — it compounds multiplicatively and can silently fail WCAG contrast.** Discovered 2026-09-21: 28 instances across 7 pages combined `color:var(--white-dim)` (already ~60% alpha) with an additional `opacity:.3`–`.6` on the same element, producing effective contrast as low as **1.56:1** against a 4.5:1 requirement — small, easy-to-miss text (blog dates, footnotes, photo-slot labels) that looked intentionally subtle in the design but was actually close to invisible to real users. `--white-dim` alone already gives ~6.5:1 on this site's dark backgrounds, which is sufficient de-emphasis on its own. If a design genuinely needs it dimmer than that, introduce a new named color token at a checked contrast ratio — don't stack `opacity`.
16. **A Netlify deploy can fail for account-level reasons that have nothing to do with the code being pushed.** Discovered 2026-09-21: a push failed with `Failed retrieving extensions for site ...: Unexpected status code 403 from fetching extensions`, during the "Reading and parsing configuration files" stage — before Netlify even looked at any pushed file. This is a Netlify account/integration auth issue, not a bug in `netlify.toml`, `_redirects`, `_headers`, or any HTML. **When a deploy fails, don't assume the just-pushed changes caused it** — check the deploy log's actual stage/error first (click "Maximize log" for the real terminal output; the AI-generated "Why did it fail?" summary is often unhelpful/undecodable). If the failure is pre-build/pre-config-parse and unrelated to file content, it's almost certainly account-side (billing, integrations needing reauthorization) — a plain "Retry" (not "without cache") is the first thing to try, since it isn't a caching issue.

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

**Rewritten 2026-09-17, item 2 + items 9-11 updated 2026-09-21 after a full site audit closed out most of what item 2 used to list as open** (color contrast, heading order, `<main>` landmark, image delivery, hero preload coverage, JSON-LD gaps, several accessibility gaps — see item 2 and items 10-11 for what's still genuinely open vs. done). Verify against live state before trusting this list too, next time it's read — see the "Keep this file honest" section below.

1. **Search Console indexing queue** — 41 pages were stuck "discovered, not indexed" due to the redirect bug (fixed & live 2026-09-16, see [[project_redirect_indexing_fix]] in memory). **Checked the real Search Console indexing report directly on 2026-09-21** (not just counting submissions) — confirmed this is genuinely resolving, not stuck: 42 pages indexed at that point, 32 not indexed, of which 29 were the real tracked "Discovered – currently not indexed" issue (validation started exactly 16/09/2026, the day the fix went live — the other 3 "not indexed" were `.html` duplicate URLs correctly deferring to their clean-URL canonical, not a problem). Submitting via Search Console: Inspect URL (top search bar) → Request Indexing, one quota-limited batch (~10/day) at a time. **22 done so far, 9 still outstanding** — full checklist below, check items off here as they're submitted so this list stays the source of truth (not a separate memory file):

   **Still to submit (9):**
   - [ ] `https://www.maddogperformance.co.za/wellness-inbody-scan-ballito`
   - [ ] `https://www.maddogperformance.co.za/wellness-nad-iv-ballito`
   - [ ] `https://www.maddogperformance.co.za/wellness-personal-training-ballito`
   - [ ] `https://www.maddogperformance.co.za/wellness-pricing`
   - [ ] `https://www.maddogperformance.co.za/wellness-recovery`
   - [ ] `https://www.maddogperformance.co.za/wellness-blog`
   - [ ] `https://www.maddogperformance.co.za/wellness-blog-iv-therapy`
   - [ ] `https://www.maddogperformance.co.za/wellness-blog-physiotherapy`
   - [ ] `https://www.maddogperformance.co.za/wellness-blog-womens-wellness-day-recap`

   **Already submitted (22):** `/training`, `/training/personal-training-ballito`, `/training/mma-ballito`, `/training/bjj-ballito`, `/training/kickboxing-ballito`, `/training/boxing-ballito`, `/training/kids-bjj-ballito`, `/wellness-body`, `/wellness-iv`, `/wellness-physiotherapy-ballito`, `/amanda`, `/athletes`, `/coaches`, `/booking`, `/recovery`, `/wellness-cold-plunge-ballito`, `/wellness-infrared-sauna-ballito`, `/training/bootcamp-ballito`, `/training/kids-boxing-ballito`, `/training/olympic-boxing-ballito`, `/training/powerlifting-ballito` (11 submitted 2026-09-21), `/training/womens-boxing-ballito`, `/blog-amanda-kobus-coach-ballito`, `/blog-bjj-beginners-ballito`, `/blog-cold-plunge-sauna-ballito`, `/blog-iv-drip-therapy-ballito`, `/blog-mma-training-ballito`, `/blog-powerlifting-women-ballito`, `/blog-robin-jj-williams-physio-ballito`, `/blog-womens-self-defence-workshop-recap-ballito`, `/blog-youth-mma-training-ballito`, `/wellness-contact` (11 more submitted 2026-09-23). Only the wellness pages/blog posts remain — one more day's quota should clear the list.

   Resubmitting an already-done URL is harmless (Google's own message: doesn't change queue position), so if it's ever unclear which were done, just continue down the unchecked list rather than trying to figure out exactly where you left off.
2. **Core Web Vitals — mobile LCP, major batch fixed & pushed 2026-09-21, not yet re-measured.** Font-loading fix pushed 2026-09-17 took mobile LCP from 10.2s → 5.0s. On 2026-09-21, a full audit + fix pass closed out nearly everything that was previously listed here as open:
   - **Image delivery — done.** 23 images recompressed (up to 2.5MB → under 200KB each, 9.6MB→3.75MB total), 8 sponsor-logo images resized from up to 1920px down to a sensible 240px (838KB→81KB), a mis-lazy-loaded nav logo fixed, `width`/`height` added to 221 `<img>` tags, `loading="lazy"` added to 50 verified below-the-fold images, 31 now-orphaned image files removed. ~106 other unreferenced files remain in `/images/` (including a 26MB `amanda-promo.mp4`) that predate this session — not touched, no context on their origin, worth a deliberate cleanup pass later (see item 10 below).
   - **Hero preload — extended from 4 pages to 28** (all 11 training-discipline pages, athletes, contact, events, wellness.html, + 9 wellness sub-pages). Still not on the 14 gym blog posts or 6 wellness blog posts — deliberately deprioritized, their header banners are smaller (~260px) so the LCP impact is much lower; see item 10 below.
   - **Color-contrast issue — found and fixed.** Root cause: 28 instances across 7 pages stacking a CSS `opacity` on top of `var(--white-dim)`, compounding to as low as 1.56:1 (see Hard-Won Rule #15).
   - **Heading-order issue — found and fixed.** Root cause: footer column titles used `<h4>` directly after the page's last `<h2>`, skipping `<h3>`, on 33 pages — fixed by promoting to `<h3>` with the matching CSS selector updated in the same change (zero visual impact).
   - **`<main>` landmark — fully done, all 53 pages.** The "gym-only, wellness deferred" note above turned out to be based on a wrong assumption — a proper audit found only 3 pages were actually missing it (`blog-iv-drip-therapy-ballito.html`, `wellness-blog.html`, `wellness-contact.html`), not ~19-20. All 3 fixed.
   - 5 hero images found incorrectly marked `loading="lazy"` (delaying LCP) and fixed; `aria-expanded` added to the mobile nav hamburger on 22 pages that were missing it; 3 unlabeled newsletter email inputs labeled.
   - **Not yet done:** re-run a live Lighthouse/PageSpeed mobile test on the homepage to see the actual new LCP number — PageSpeed's API was still hard-blocked (zero quota) as of 2026-09-21, so this needs either that quota to free up or a manual paste from the user like the last two rounds.
3. **E-E-A-T content pass** — credit named coaches (not just "Maddog Marketing") on posts where their specific expertise is the point; state credentials/issuing bodies in text, never raw ID numbers (see Content Gaps below).
4. **Federation/affiliation content** (MMASA etc.) — awaiting client-confirmed details, see Content Gaps below. Specific backlink target already identified: MMA South Africa's affiliated-gyms directory (mma-sa.co.za/affiliated_gyms) lists KZN gyms but not Maddog — pursue getting listed there once affiliation is confirmed, see [[project_mmasa_affiliation_opportunity]] in memory.
5. **Content-Security-Policy header** — deliberately not added yet; needs a careful resource-by-resource audit first given how much inline script/style and third-party embedding this site does. Other security headers already live.
6. **Local SEO / backlinks** — site currently has 1 external backlink total. Client-side relationship work (asking sponsor/partner businesses to link back), not something fixable from the codebase.
7. **Keyword ranking gaps identified (2026-09-17 live-search audit)** — see [[project_keyword_ranking_audit]] in memory for full results. Two actionable patterns: (a) **wellness GBP has far fewer reviews than the gym's GBP** and this is likely suppressing Local Map Pack visibility for sauna/cold-plunge/IV-drip/NAD/body-composition searches even where on-site content already ranks #1 organically — completing the wellness GBP (client doing manually, see [[project_wellness_gbp_incomplete]]) is probably the single highest-leverage fix available; (b) **bootcamp ballito / fitness bootcamp ballito** is a real content/backlink gap — Maddog has `training-bootcamp-ballito.html` but doesn't rank competitively against Fit24, F45, Ballito Fitness Village, HIITMANN, Grit Factory. Named competitors worth tracking: **Ringside Boxing Gym** (beats Maddog on pure boxing terms), **CombatCoaching.com** (new, beats Maddog on self-defence terms), **Grit Factory** (dominant on personal-training terms), **Kico Life / IVology / The IV Bar** (dominant on several wellness terms).
8. **Personal training — tracked ranking priority (client request, 2026-09-17), partially addressed.** Was weak: Maddog sits ~#6-7 organically on "personal trainer ballito" / "personal training ballito" / "personal training classes ballito" / "personal training studio ballito", behind **Grit Factory** (#1 on all of them — one strong benefit-led page + reviews, not content depth, so beatable). Full competitor breakdown in [[project_personal_training_competitor_audit]] in memory. `training-personal-training-ballito.html` strengthened and **pushed live 2026-09-17**: sharpened title/meta/H1 to cover the weak exact-match phrases, and — since client confirmed **Amanda "Maddog" Lino is also a personal trainer at Maddog** — added a full second-coach section for her plus a matching FAQ/schema entry, resolving the "female personal trainer ballito" gap. Still open: no neurodiversity/special-needs coaching angle (Launch Lifestyle owns this — only add if Maddog genuinely offers/wants to offer it, don't claim it speculatively); no visible testimonials section despite schema claiming 5.0★/8 reviews (need real client quotes to add honestly). Rankings haven't been re-checked since the push — worth a `maddog-keyword-check` re-run once enough time has passed for Google to re-crawl.
9. **Google Business Profile — Products section, partially updated (2026-09-17).** Full GBP audit + fix status tracked in [[feedback_gbp_weekly_check_reminder]] in memory (this is a "check every week" item, not a one-time task). As of last check: gym's "Personal Training" product relabeled with clear per-session pricing (done), wellness added Ice Bath as its own product (done). Still outstanding: **Olympic Boxing** not listed as a gym product despite having its own page; **Infrared Sauna** and **wellness Personal Training/Strength & Nutrition Coaching** not listed as separate wellness products — these two directly target the weak "sauna ballito" ranking, highest priority of what's left. Also unconfirmed: a wellness profile edit was showing "under review" as of 2026-09-17 — check it actually went live.
10. **LocalBusiness JSON-LD gaps — closed 2026-09-21.** `geo` added to 12 blog pages + 6 more; `image`/`priceRange`/`openingHours` added to coaches/booking/recovery/contact/training/wellness-contact/wellness-pricing; `og:locale`/`og:image` fixed on 8 blog pages; `amanda.html`/`athletes.html` linked to the main business entity via `@id` rather than stuffing LocalBusiness-only fields (`openingHours`, `priceRange`) into their `Person`/`SportsTeam` schemas, which would have been semantically wrong. A pre-existing, unrelated bug found in passing: `amanda.html`'s `Person` schema `image` field pointed at a file (`images/amanda-lino.jpg`) that never existed — fixed to point at her real photo.
11. **Image cleanup, deliberately deferred from the 2026-09-21 batch:**
    - Hero preload on the 14 gym blog posts + 6 wellness blog posts (lower priority than the main pass, see item 2 above)
    - ~106 unreferenced files still in `/images/` (including a 26MB promo video) that predate this session — need someone with the actual history/context to confirm what's safe to delete, since blind deletion of unknown content is exactly the kind of thing to not do without knowing what it is

---

## Content Gaps (Awaiting Client)

- Amanda's 6 remaining pro fight results (opponent, event, method, round, result)
- Coach credentials: Luckymore Hamadziripi, Coach Marcele, York Lawrence (formal certs, if not already on-site — verify against current `coaches.html` before asking the client again)
- **Wren's SANC registration number — will NOT be published.** Explicit client decision (2026-09-17): raw registration/certification numbers are never to appear on the site — risk of the number being lifted and used to impersonate/duplicate the credential elsewhere. Bridge instead by stating the credential + issuing body in text only (e.g. "SANC-registered nurse") — the registration status itself is the trust signal Google/visitors need, not the number. This applies to any coach's future certification numbers too, not just Wren's.
- **Exception: Dr. Deo du Plessis's HPCSA registration number and practice number ARE approved to stay public** on `recovery.html`. Found during the 2026-09-21 audit (same general category as the Wren rule above — raw ID numbers), flagged to the client, and explicitly approved to leave as-is rather than redact. Don't re-flag or "fix" this one again — it's a deliberate, confirmed exception, not an oversight.
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

- Images are **content-hash-named files in `/images/`**, referenced by full URL (`https://www.maddogperformance.co.za/images/<hash>.{jpg,png}`) — never base64 (this line used to say base64-embedded; stale, fixed 2026-09-21, see Architecture and Hard-Won Rule #8).
- Compress with PIL before uploading (target ≤ 200KB per image at quality 72–82, max 1200px long edge). Never embed/upload a raw uncompressed PNG or high-res JPEG — always run through PIL first.
- **Match the resize target to the actual display size, not a blanket default.** Discovered 2026-09-21: 8 sponsor-logo images were serving up to 1920×1920px into an 80×80px display slot — well under the 200KB byte-size target so earlier compression passes never flagged them, but still ~750KB of pure waste. Before compressing, check the image's actual CSS display container (not just its byte size) and size to roughly 3x that for retina, not the general 1200px default.
- Every `<img>` must have a descriptive `alt` attribute — never `alt=""` for content images. Decorative images only may use `alt=""`.
- Include `width` and `height` attributes on every `<img>`, matching the real file's pixel dimensions, to prevent layout shift (CLS).
- Use `loading="lazy"` on all images that are below the fold.
- Hero / above-the-fold images must NOT have `loading="lazy"` — they must load immediately. This includes secondary hero-adjacent images (e.g. a multi-photo hero mosaic) even when they aren't the primary preloaded LCP candidate — check the element's actual CSS section/position, not just whether it has `fetchpriority`, before assuming an image low in the DOM order is safe to lazy-load. A blog post's own header/banner image counts as its hero too, even though it's smaller (~260px) than a full page hero.
- Use `object-fit: cover` + explicit dimensions on photo slots to prevent reflow.
- **Local `file://` testing cannot verify a new or renamed image before it's pushed.** Every `<img src>` is a full `https://www.maddogperformance.co.za/...` URL, not a relative path — so opening a local `.html` file still fetches images from the live internet, not from the PC's own `/images/` folder. If a page references a newly-added or newly-renamed image that hasn't been pushed yet, it will show broken locally even though the code is correct, while the live site (still on the old, unpushed version) keeps loading its old images fine. This is expected, not a bug — it resolves the moment both the HTML and the image files are pushed together. Local testing is still reliable for everything else (layout, text, structure).

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
