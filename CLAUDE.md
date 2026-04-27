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
