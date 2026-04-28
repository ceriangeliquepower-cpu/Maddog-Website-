# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Project

Static HTML website for **Maddog Performance Institute** — MMA gym + recovery/wellness centre in Ballito, KZN, South Africa.

- **Live domain:** maddogperformance.co.za (DNS not yet pointed to Netlify)
- **Netlify preview:** https://69d75b86a9622c318e399025--stellar-biscochitos-7f6a1c.netlify.app/
- **Hosting:** Netlify — all 13 HTML files drop into the same folder, all relative links work as-is
- **Redirects:** `_redirects.txt` maps `/` → `/index.html 200`

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

---

## Page Map

| File | Purpose |
|------|---------|
| `index.html` | Homepage |
| `amanda.html` | Amanda Lino bio + fight record |
| `athletes.html` | Fighter roster |
| `coaches.html` | Coach profiles |
| `training.html` | Class schedule + disciplines |
| `recovery.html` | Recovery suite — IV therapy, sauna, cold plunge, peptides |
| `events.html` | Events + blog index |
| `contact.html` | Contact page |
| `blog-*.html` (×5) | SEO blog articles, all linked from `events.html` |

---

## Outstanding Work (Priority Order)

1. **`pricing.html`** — New file. Full pricing for IV therapy, contrast therapy, athlete memberships, slimming clinic, peptide therapy (enquiry only). See `MADDOG_CLAUDE_CODE_HANDOFF.md` for complete price tables and exact copy.
2. **`recovery.html` updates** — Add Slimming Clinic section + Aesthetic & Wellness IV section; populate contrast therapy prices (R80/R170/R250 post-training, R270/R350/R850 general); confirm athlete membership tiers are populated.
3. **SEO Round 2** — AggregateRating schema, BreadcrumbList on blog pages, internal linking, `sitemap.xml` (missing blog URLs), Google Business Profile (not yet claimed).
4. **DNS** — Point `maddogperformance.co.za` to Netlify (A record + CNAME).

---

## Content Gaps (Awaiting Client)

- Amanda's 6 remaining pro fight results (opponent, event, method, round, result)
- Coach credentials: Lucky, Winston, Tristan (formal certs); Wren's SANC registration number
- Training prices: 18 slots currently show POA
- Upcoming event venues + ticket links
- Photos: all pages have click-to-upload slots ready

---

## Before Editing Any Page

1. Read the existing file's CSS class names and structure before writing new HTML — match exactly.
2. New sections must use existing CSS classes, not introduce new design patterns.
3. Deliver complete `.html` files, not partial snippets (unless explicitly asked for a snippet).

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
