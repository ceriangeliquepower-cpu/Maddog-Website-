---
name: maddog-wellness-new-blog-post
description: Create a new SEO-optimized blog post for the Maddog Performance Health & Wellness site (IV therapy, recovery, physiotherapy, body composition, GENESIS/longevity — not the MMA gym) using wellness-blog-TEMPLATE.html, and add it to the top of the Insights grid on wellness-blog.html. Use when the user gives a topic and asks for a new wellness/recovery/IV blog article, or says things like "write a wellness blog post about X".
---

# Maddog Wellness Blog Post Creator

Builds one new `wellness-blog-[slug].html` file from `wellness-blog-TEMPLATE.html`, adds it to the top of the Insights grid on `wellness-blog.html`, and rotates it into the homepage teaser on `wellness.html`. This skill is scoped to **Maddog Performance Health & Wellness** (IV therapy, recovery, physio, body composition, GENESIS) only — it does not touch the gym site (`blog-*.html`, `events.html`, `index.html`). If the user asks for a gym/MMA/training post, use `maddog-new-blog-post` instead, not this one.

**Mirrors the gym skill's homepage behavior exactly.** The Insights grid on `wellness-blog.html` has no rotation logic — every new post just gets added to the top, older posts stay put. But `wellness.html` (the wellness homepage) **does** rotate, the same way `index.html`'s "Latest from Maddog" section does on the gym site: it has a two-card **"From The Blog" teaser section** (`id="blog-teaser"`, right before the final CTA), and **every new post automatically takes slot 1** — confirmed standing behavior, not something to ask about per post. Whatever was in slot 1 shifts to slot 2; whatever was in slot 2 drops off the homepage (it's not lost — still on `wellness-blog.html`'s grid and in `sitemap.xml`, just no longer one of the two promoted on the homepage). Handled by `scripts/rotate_wellness_homepage_posts.py`, run as part of §7b below.

## 0. Ground rules (non-negotiable)

- Edit files directly in `C:\Users\HP\Desktop\Maddog Web design pages\` — never a worktree copy.
- **Never run `git commit` or `git push`.** Report what changed and that it's local-only, then wait for explicit "push it" / "commit it".
- **Canonical brand name: "Maddog Performance Health & Wellness"** — confirmed with the user. Existing wellness content is inconsistent (variants found: "Maddog Health & Wellness", "Maddog Wellness", even "Maddog Performance Institute" — the gym's name — bled into a couple of spots by copy-paste, including once in `og:site_name`). Use the canonical form in JSON-LD `author`/`publisher`/`name` and in any full-name body reference. Shorter references like "Maddog Health & Wellness" in flowing body copy are fine (that's the dominant existing usage and reads naturally) — just never let the gym's name ("Maddog Performance Institute") leak into wellness content, and always use the full canonical form in structured data.
- Never rewrite the user's supplied content's meaning — light edits only (brand-name consistency, typos, tone), keep their facts and structure.
- **Never state or imply something happened that isn't confirmed.** This shipped as a real bug once: a recap post said attendees "left with" a recovery session that was actually only a take-home voucher, and a since-caught draft invented "several women had already messaged to book." If you're inferring a detail from a related page (e.g. what an earlier pre-event post promised) rather than from what the user told you happened, either phrase it as what was *offered*, not what *occurred*, or flag the inference to the user explicitly and ask before publishing it as fact. When in doubt, cut the specific claim rather than guess.

## 1. Gather inputs

Ask for whatever isn't already given:

1. **Topic / content** — plain text, not a `.docx`.
2. **Filename slug** — becomes `wellness-blog-[slug].html` (no `-ballito` suffix convention here — check existing files: `wellness-blog-iv-therapy.html`, `wellness-blog-cold-plunge.html`, etc. — short topic slug only). Derive from the topic if not given, confirm it.
3. **Category tag** — matches the existing style, which uses a two-part "Topic · Subtopic" format (e.g. "IV Therapy · Nutrition", "Recovery · Contrast Therapy", "Longevity · Neuro-Metabolic Health") — not a single word like the gym site's tags. Use `&middot;` for the separator (matches existing HTML entity usage).
4. **Hero photo** — see §3. Ask whether it's already in `raw-photos/` or still needs to be added there (same shared drop folder as the gym skill).
5. **Published date** — default to today unless told otherwise.

## 2. Read the template fresh

Always `Read` `wellness-blog-TEMPLATE.html` at the start of the task — don't rely on memory of its structure. It supplies the full nav, footer, WhatsApp float, and CSS (note: **light theme** — cream background `#F7F4EF`, dark text — this is the opposite of the gym site's dark theme, don't accidentally carry gym styling over).

**Duplicate the file, never hand-type the nav/head.** The gym skill's equivalent step shipped a real bug from doing this by hand once (a reconstructed nav was missing the CSS that hides its dropdown menus, so they rendered permanently expanded). This wellness template's nav logo is plain text, not an embedded image, so the risk is lower here — but the discipline is the same and cheaper to just follow: `cp wellness-blog-TEMPLATE.html wellness-blog-[slug].html` (or the Python equivalent) before any content edits, then fill placeholders (§3) with targeted `Edit` calls against the new file, never a from-scratch `Write`.

## 3. Fill every placeholder

The template marks fields with `WBLOG_*` placeholders:

| Placeholder | Rule |
|---|---|
| `WBLOG_TITLE` (`<title>`) | ends "\| Maddog Wellness" (shorter suffix than the gym site's) |
| `WBLOG_META_DESCRIPTION` | 150–160 chars, primary keyword included |
| `WBLOG_FILENAME` | the slug from §1, extension-less in canonical/OG/JSON-LD URLs (file itself is still `.html`) |
| `WBLOG_DATE_ISO` / `WBLOG_DATE_DISPLAY` | `YYYY-MM-DD` and e.g. "August 2026" |
| `WBLOG_CATEGORY` (`bh-tag`) | the category from §1 |
| `WBLOG_FULL_TITLE` | H1 — can be more natural/longer than the `<title>` version |
| `WBLOG_READ_MINUTES` | word count of the article body ÷ 200, rounded, minimum 3 |
| `WBLOG_CTA_TEXT` | 1–2 sentences tailored to the topic, ending with the address (matches existing pattern: "...starts with a single consultation at Maddog Health & Wellness in Ballito. 22 Sandra Road, Balvista Centre, Ballito, KZN.") |
| `WBLOG_WHATSAPP_QUERY` | URL-encoded short message about the topic, e.g. `Hi%2C%20I%27d%20like%20to%20find%20out%20more%20about%20TOPIC` — used in both the CTA box and the floating WhatsApp button, keep them identical |
| `WBLOG_RELATED_HREF_1/2`, `WBLOG_RELATED_LABEL_1/2` | 2 relevant related posts/pages for the "Read Next" block — see `reference/internal-links.md` |

The template already ships a correct **MedicalBusiness JSON-LD block** (unlike the gym template, which was missing LocalBusiness schema entirely) — leave its content as-is, it doesn't need per-post editing beyond what's already templated.

## 4. Article body

Replace the placeholder `<h2>SECTION_HEADING_1</h2>` block with the user's content:

- `<h2>` main sections, `<h3>` sub-sections, `<p>` paragraphs, `<ul>`/`<li>` lists — sequential heading levels, one `<h1>` only (the hero title).
- `.pull-quote` div available for a standout quote (optional).
- At least 2 internal links somewhere in the body or CTA — see `reference/internal-links.md`. The template's "Read Next" block at the end already provides 2 by default; add more inline in the body if it fits naturally, don't force it.
- Existing posts also use `.stats-strip` (a 4-cell stat row) and `.service-grid` (2-column feature cards) for richer layouts — these are optional flourishes for content that suits them (e.g. a programme with clear pillars/stats), not required for every post. Don't force them onto content that doesn't naturally fit that shape.

## 5. Hero photo

Same optimizer as the gym skill, same shared `raw-photos/` drop folder:

```bash
py optimize_photo.py "raw-photos/THEIR_FILENAME.jpg" --type hero
```

Unlike the gym site, the wellness hero uses **one photo in two places at once** — a blurred, zoomed backdrop (`.hero-blur-bg`, CSS `background-image`) behind a full, uncropped foreground image (`.article-hero-img`, `object-fit:contain`, not cropped like the gym's banner). Use the same `images/HASH.jpg` output for both `WBLOG_IMAGE_HASH` occurrences in the template (the `background-image: url(...)` and the `<img src=...>`) — no need for a second variant. Get `WBLOG_IMAGE_WIDTH`/`WBLOG_IMAGE_HEIGHT` from the optimizer's reported dimensions.

**Known inconsistency, not something to fix here:** existing wellness posts and the wellness-blog.html grid still carry base64-embedded images from before this convention. Don't copy that pattern for new posts.

**Check the crop on the two card placements before calling it done.** The post's own hero uses `object-fit:contain` (shows the whole photo, no cropping risk), but the `wellness-blog.html` Insights card (§7) and the `wellness.html` homepage teaser card (§7b) both use `object-fit:cover` via `.blog-card-img img`, which crops to fill the box — for a group/people photo this can cut faces off (shipped once on the gym site: a group photo's cropped placements both showed mostly ceiling, people cut off at eye level). After running §7 and §7b:

1. Preview with a real local server, not a direct `file://` open — `preview_start` with the `maddog-static` config in `.claude/launch.json`. A direct `file://` navigate renders as a static snapshot in the Browser pane and relative image paths won't load.
2. Check both card thumbnails. If a face or important part of the photo is cut off, add `object-position:center Y%` inline on that specific `<img>` — a higher `Y` shows more of the bottom of the source image, lower shows more of the top. Fix each placement separately; tuning one doesn't carry to the other.

## 6. Write the file

Check the target filename doesn't already exist first (a slug collision would silently overwrite a post). Write to `C:\Users\HP\Desktop\Maddog Web design pages\wellness-blog-[slug].html`, complete file, not a snippet.

## 7. Add the card to wellness-blog.html — same file-size caution as the gym scripts

`wellness-blog.html` is ~900KB, base64-heavy from its existing cards. Use the tested script rather than hand-editing:

```bash
py .claude/skills/maddog-wellness-new-blog-post/scripts/prepend_wellness_blog_card.py \
  --new-tag "CATEGORY (with &middot; if two-part)" \
  --new-title "FULL TITLE" \
  --new-excerpt "One to two sentence hook." \
  --new-href wellness-blog-[slug].html \
  --new-image images/HASH.jpg
```

- Reuse the same `--type hero` optimizer output from §5 — one photo across the post's own hero and this card.
- Simply inserts the new card at the top of the grid (newest first) — no rotation, no demotion, nothing else changes. Refuses to run (writes nothing) if a card with that `--new-href` already exists, or if the page structure doesn't match what it expects — report the error rather than working around it.
- Writes an automatic `wellness-blog.html.bak` backup before writing. `--dry-run` and `--blog-file` (for testing against a scratch copy) both supported.
- Prints `ADDED TO TOP OF INSIGHTS GRID:` — check it before reporting done.

## 7b. Rotate the homepage teaser on wellness.html

`wellness.html` is several MB of base64 image data, same caution as every other large page on this site. Use the tested script:

```bash
py .claude/skills/maddog-wellness-new-blog-post/scripts/rotate_wellness_homepage_posts.py \
  --new-tag "CATEGORY (with &middot; if two-part)" \
  --new-title "FULL TITLE" \
  --new-excerpt "One to two sentence hook." \
  --new-href wellness-blog-[slug].html \
  --new-image images/HASH.jpg
```

- Same `--new-image` as §7 — one photo across the post's own hero, the Insights grid card, and this homepage card.
- Prints `DROPPED FROM HOMEPAGE:`, `SHIFTED TO SLOT 2:`, and `NEW SLOT 1:` — check all three.
- Same safety model as the other rotation scripts: automatic `wellness.html.bak` backup, refuses to run rather than guess if the teaser markup doesn't match what it expects, `--dry-run` and `--wellness-file` (for scratch-copy testing) both supported.
- **If the write itself fails with an OS-level file error** (seen once: a transient Windows file lock, likely antivirus or a sync service momentarily holding the file), the backup will still have been written successfully just before it — check the real file wasn't left truncated by comparing it against the `.bak` before doing anything else, restore from the `.bak` if it was, then simply retry the same command. Don't skip the verification step even though the retry is usually all that's needed.
- `--new-tag` (and `--new-cat`/`--new-tag` on the gym scripts) is passed through **unescaped** — pass real HTML entities like `&middot;` directly, don't double-escape them.

## 8. Update sitemap.xml

Add one `<url>` entry in the "Wellness Blog & New Pages" section:

```xml
<url><loc>https://www.maddogperformance.co.za/wellness-blog-[slug]</loc><lastmod>YYYY-MM-DD</lastmod><changefreq>weekly</changefreq><priority>0.7</priority></url>
```

Also bump the existing `/wellness-blog` entry's `<lastmod>` to today (its content changed too).

## 9. Pre-publish checklist

Run through `reference/checklist.md` before reporting done.

## 10. Report back

Summarize: filename created, card added to wellness-blog.html, homepage teaser rotated on wellness.html, sitemap.xml updated, and state explicitly that **nothing has been pushed**. Wait for the user's go-ahead before touching git.
