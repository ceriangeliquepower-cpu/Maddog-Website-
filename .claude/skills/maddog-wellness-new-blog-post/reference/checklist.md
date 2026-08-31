# Pre-publish checklist — new wellness blog post

Run through this before telling the user the post is ready.

## Brand
- [ ] "Maddog Performance Health & Wellness" used in full in JSON-LD `author`/`publisher`/`name`; "Maddog Health & Wellness" acceptable in flowing body copy
- [ ] The gym's name ("Maddog Performance Institute") does NOT appear anywhere in this file, including `og:site_name` (a bug found on at least one existing wellness page — don't repeat it)
- [ ] User's original content meaning/facts preserved — only brand-consistency, typo, and light tone edits made
- [ ] No invented experiential detail — every claim of something that happened is either from the user's own content or explicitly flagged to them as an inference, not stated as fact

## SEO — head block
- [ ] `<title>` ends "| Maddog Wellness" (not the gym's longer suffix)
- [ ] `<meta name="description">` 150–160 chars, includes primary keyword
- [ ] `<link rel="canonical">` extension-less, matches sitemap pattern
- [ ] OG tags updated (`og:type=article`, title, description, url) — `og:site_name` correctly says "Maddog Performance Health & Wellness"
- [ ] Twitter card tags updated
- [ ] Article JSON-LD: headline, description, dates, url all filled in (not template placeholders)
- [ ] BreadcrumbList JSON-LD: position 3 has the real title and URL; position 1 points to `/wellness` (not gym root `/`)
- [ ] MedicalBusiness JSON-LD present (template ships it by default) — confirm it wasn't accidentally deleted

## Semantic HTML / headings
- [ ] Exactly one `<h1>` (hero title)
- [ ] `<h2>` main sections, `<h3>` nested under `<h2>` only — no skipped levels
- [ ] Lists use `<ul>`/`<li>`, not manual bullets in `<p>` tags

## Images
- [ ] Hero photo went through `optimize_photo.py --type hero` — not base64, not an unresized original
- [ ] The same optimized image is referenced in both `.hero-blur-bg` (CSS background) and `.article-hero-img` (`<img src>`) — one file, two placements
- [ ] `width`/`height` on `.article-hero-img` match what the optimizer reported
- [ ] Real, descriptive `alt` text (never empty for a content photo)
- [ ] `wellness-blog.html` card image uses the same file path, not base64, `loading="lazy"` (it's below the fold there — unlike the post's own hero, which should NOT be lazy)
- [ ] Crop checked via a real local server (`maddog-static` preview, not a direct `file://` open) on both `object-fit:cover` card placements (wellness-blog.html Insights card, wellness.html homepage teaser card) — no faces/people cut off; `object-position` tuned per-spot if needed

## Internal linking
- [ ] At least 2 internal links, contextually relevant — see `reference/internal-links.md`
- [ ] "Read Next" block filled with 2 genuinely relevant related posts/pages, not left as placeholders
- [ ] `sitemap.xml` has a new `<url>` entry, extension-less, in the "Wellness Blog & New Pages" section
- [ ] `sitemap.xml`'s existing `/wellness-blog` entry `lastmod` bumped to today

## CTA correctness
- [ ] CTA box text ends with the real address ("22 Sandra Road, Balvista Centre, Ballito, KZN"), tailored to the topic
- [ ] `WBLOG_WHATSAPP_QUERY` filled identically in both the CTA box's WhatsApp button and the floating WhatsApp button — don't leave one as a placeholder while filling the other

## File safety
- [ ] Confirmed the target `wellness-blog-[slug].html` filename didn't already exist before writing
- [ ] `wellness-blog.html` was never bulk-`Read` or hand-edited — the card insert went through `scripts/prepend_wellness_blog_card.py`
- [ ] Script's `ADDED TO TOP OF INSIGHTS GRID:` output line checked and correct
- [ ] `wellness-blog.html.bak` no longer exists (cleaned up after the write was verified) as a rollback point

## Homepage teaser rotation (wellness.html)
- [ ] `wellness.html` was never bulk-`Read` or hand-edited — the rotation went through `scripts/rotate_wellness_homepage_posts.py`
- [ ] Script's `DROPPED FROM HOMEPAGE:`, `SHIFTED TO SLOT 2:`, and `NEW SLOT 1:` output lines checked and all three look right
- [ ] If the write failed with an OS-level error, verified the real file wasn't left truncated (compared against `.bak`) before retrying
- [ ] `wellness.html.bak` no longer exists (cleaned up after the write was verified)

## Accessibility / Mobile
- [ ] Colour contrast unaffected — no new inline colours outside the existing CSS variables (note: this site is **light theme**, don't carry over gym dark-theme colours)
- [ ] No new fixed pixel widths that could cause horizontal scroll

## Workflow
- [ ] File saved to the main project folder, not a worktree
- [ ] The new file was created by duplicating `wellness-blog-TEMPLATE.html` (`cp` or equivalent), never hand-retyped
- [ ] Nothing committed or pushed — confirmed local-only in the summary given to the user
