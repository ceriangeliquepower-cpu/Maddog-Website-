---
name: maddog-new-blog-post
description: Create a new SEO-optimized blog post for the Maddog Performance Institute gym site (not the wellness site) using blog-TEMPLATE.html, add its card to events.html, and register it in sitemap.xml. Use when the user gives a blog topic or pasted content and asks for a new gym blog article, or says things like "write a blog post about X" or "new blog for the gym".
---

# Maddog Gym Blog Post Creator

Builds one new `blog-[slug]-ballito.html` file from `blog-TEMPLATE.html`, features it on `events.html`, promotes it into the homepage's "Latest from Maddog" section on `index.html`, registers it in `sitemap.xml`, and runs it through the site's SEO/brand checklist. This skill is scoped to **Maddog Performance Institute** (the gym) only — it does not touch the wellness site (`wellness-blog*.html`, `wellness-blog.html`). If the user asks for a wellness post, say this skill doesn't cover that yet rather than improvising.

## 0. Ground rules (non-negotiable)

- Edit files directly in `C:\Users\HP\Desktop\Maddog Web design pages\` — never a worktree copy.
- **Never run `git commit` or `git push`.** When the files are written, report what changed and that it's local-only, then stop and wait for the user to explicitly say "push it" / "commit it". Confirming the content is not the same as confirming the push.
- Brand name is always **"Maddog"** — never "Mad Dog", "MadDog", or "MADDOG". Fix this in any pasted content before it goes in the file.
- Never rewrite the user's supplied content's meaning — light edits only (brand-name fix, typos, Maddog voice/tone), keep their facts and structure.
- **Never state or imply something happened that isn't confirmed.** This shipped as a real bug once: a recap post said attendees "left with" a recovery session that was actually only a take-home voucher, and a since-caught draft invented "several women had already messaged to book." If you're inferring a detail from a related page (e.g. what an earlier pre-event post promised) rather than from what the user told you happened, either phrase it as what was *offered*, not what *occurred*, or flag the inference to the user explicitly and ask before publishing it as fact. When in doubt, cut the specific claim rather than guess.

## 1. Gather inputs

Ask for whatever isn't already given:

1. **Topic / content** — plain text (not a `.docx`; those are binary, ask for pasted text instead if that's what they offer)
2. **Filename slug** — becomes `blog-[slug]-ballito.html`. Lowercase, hyphens, always ends `-ballito.html` for local SEO. Derive a sensible slug from the topic if not given, and confirm it.
3. **Category tag** — one or two words, Title Case, matching the existing vocabulary already used on cards in `events.html` (e.g. "Training", "Recovery", "Youth & Family", "BJJ", "Community"). Coin a new one only if nothing existing fits.
4. **Hero/card photo** — see §4b. Ask whether the photo is already sitting in `raw-photos/` (the user's drop folder) or still needs to be added there.
5. **Published date** — default to today's date (from system context) unless told otherwise.

Don't block on minor gaps — make a reasonable call (e.g. read time, exact meta description wording) and let the user correct it when they review.

## 2. Read the template fresh

Always `Read` `blog-TEMPLATE.html` at the start of the task rather than relying on memory of its structure — it may have changed since. It supplies the full nav, credential strip, article CSS, footer, and WhatsApp float.

**Never hand-type any part of the nav or head — always duplicate the file, then edit.** This is not optional style guidance: it shipped as a real bug once. The nav contains a large embedded logo image and a `.nav-has-dropdown`/`.nav-drop-menu` CSS block that makes the Training/Recovery dropdowns hide until hovered; reconstructing the nav "close enough" from memory produced a page with the logo missing and the dropdowns rendered permanently expanded across the top of the page. The safe procedure:

1. Duplicate the whole template to the new filename first, byte-for-byte, before making any content changes — `cp blog-TEMPLATE.html blog-[slug]-ballito.html` in Bash, or the equivalent in Python. Never use `Write` to reconstruct the template's content from what you read.
2. Only then fill in placeholders (§3) using targeted `Edit` calls against the new file. Every `BLOG_*` token is a short, unique string that never sits inside the embedded base64, so this is safe without ever needing to read the huge nav-logo line into context — search for the tokens with `Grep`, edit them with `Edit`.

If you ever do need to check the nav/dropdown CSS is intact (e.g. after a manual edit elsewhere in the head), verify `.nav-has-dropdown`, `.nav-drop-menu`, and `.nav-drop-chevron` rules are present in the file's `<style>` block — their absence is exactly what caused the bug.

## 3. Fill every placeholder

The template marks fields with `BLOG_*` uppercase placeholders. Replace all of these:

| Placeholder | Rule |
|---|---|
| `BLOG_TITLE` (in `<title>`) | ≤60 chars, primary keyword first, ends "\| Maddog Performance Institute \| Ballito KZN" |
| `BLOG_META_DESCRIPTION` | 150–160 chars, includes the primary keyword, reads as a real sentence (used in `<meta description>`, OG, Twitter) |
| `BLOG_FILENAME` | the slug from §1, no `.html` extension in URLs used inside JSON-LD/canonical (site strips it via Netlify redirects — but the **file itself** is still saved as `.html`; only the URL strings inside `<link rel=canonical>`, OG/Twitter `og:url`, and JSON-LD `@id`/`item`/`mainEntityOfPage` use the extension-less form, matching `sitemap.xml`'s pattern) |
| `BLOG_DATE_ISO` | today's date as `YYYY-MM-DD`, used for both `datePublished` and `dateModified` |
| `BLOG_CATEGORY` (hero tag) | the category from §1 |
| `BLOG_FULL_TITLE` (`<h1>`) | can be slightly longer/more natural than the `<title>` tag version |
| Breadcrumb JSON-LD `position:3` | `name` = the H1 title, `item` = full canonical URL (extension-less) |
| Hero meta line | month + year (e.g. "August 2026") and an honest read-time estimate: word count of the article body ÷ 200, rounded, minimum 3 min |

Also add a **LocalBusiness JSON-LD block** — the template does not currently ship one, but CLAUDE.md requires it on every page. Insert the block from `reference/localbusiness-jsonld.json` as a third `<script type="application/ld+json">` alongside the Article and BreadcrumbList blocks already in the template.

## 4. Article body

Replace the placeholder `<h2>SECTION_HEADING_1</h2>` block with the user's actual content, using:

- `<h2>` for main sections, `<h3>` for sub-sections — sequential, never skip a level (the page's only `<h1>` is the hero title)
- `<p>` for paragraphs, `<ul>` for bullet lists (template's `<ul>` styling is already bullet-icon based, don't add manual bullet characters)
- `.pull-quote` div for a standout quote if the content has one worth pulling out (optional, not required)
- `.internal-link` class on any inline link to another page on the site — include **at least 2** internal links somewhere in the article body or CTA (site rule: every page must link to 2+ others). See `reference/internal-links.md` for a ready mapping of topic → good link targets rather than picking arbitrary pages each time.
- Leave the existing `.article-cta` block at the end as-is unless the topic calls for a different CTA (e.g. linking to `recovery.html` instead of `booking.html` for a recovery-topic post).

## 4b. Hero photo

Do **not** use the template's click-to-upload `.photo-slot` / `swapPhoto()` pattern — that live-photo-editing mechanism was removed site-wide (see commit "Remove live photo editing site-wide"). Use a plain file-based image instead, produced by the project's `optimize_photo.py` script — never embed base64, and never hand-copy a phone photo straight into `images/` unresized.

**Workflow:**

1. The user drops their raw, unedited photo into `raw-photos/` (gitignored — this folder never gets pushed or deployed, it's just a local staging area) and tells you the filename. If they haven't done this yet, ask them to and wait.
2. Run the optimizer from the project root:
   ```bash
   py optimize_photo.py "raw-photos/THEIR_FILENAME.jpg" --type hero
   ```
   One run, one preset (max 1600px wide, ≤200KB) — this same output is used for both the blog post's own hero banner (this section) and the events.html featured-post photo (§6), so there's no need to generate a separate card-sized variant. (`optimize_photo.py`'s `--type card` preset still exists for one-off use if you're ever adding a card image outside the featured-rotation flow, but the standard new-post path doesn't need it.)
3. The script prints the output filename (a content hash, e.g. `images/e8f56b6e3945721c.jpg`) — that's already saved into `images/`. Use that exact path in the `<img src>`, and reuse it again in §6's `--new-image` argument.
4. If the user provides the same photo for a future post too, don't re-run the optimizer — reuse the filename it already produced (check `images/` first if you suspect it might already exist).

**Resulting markup:**

```html
<img src="images/HASH.jpg" alt="DESCRIPTIVE ALT TEXT" width="WIDTH" height="HEIGHT" style="width:100%;height:100%;object-fit:cover">
```

Use the actual `width`/`height` the script reports (from its "Dimensions:" line) — don't guess or reuse a placeholder value, mismatched dimensions cause layout shift.

- **Known inconsistency, already understood, not something to fix here:** some existing blog cards in `events.html` still have big base64 `data:image/jpeg;base64,...` strings baked into their `<img src>` from before the `images/` convention and this optimizer existed. Don't copy that pattern for new posts, and don't "fix" old ones as a side effect of this skill — that's a separate cleanup job if the user ever wants it.
- Always write a real, descriptive `alt` (never `alt=""` for a content photo).
- The hero image loads above the fold — do **not** add `loading="lazy"` to it.

**Check the crop before calling it done.** Every placement here uses `object-fit:cover`, which crops to fill the box — for a group/people photo, the default center crop can easily cut faces off the top or bottom (this shipped once: a group photo's hero and homepage-card crops both showed mostly ceiling, cutting the people off at eye level). After wiring the photo into the post, the featured slot, and the homepage card:

1. Preview with a real local server, not a direct `file://` open — `preview_start` with the `maddog-static` config in `.claude/launch.json` (`py serve.py`, port 3000). A direct `file://` navigate in the Browser pane renders as a static snapshot and relative image paths won't load, so you can't actually see the crop that way.
2. Look at the hero banner and the card thumbnail. If a face or important part of the photo is cut off, add `object-position:center Y%` inline on that specific `<img>` (already an established per-photo convention elsewhere on this site — search for `object-position` in other pages for examples) — a higher `Y` shows more of the bottom of the source image, a lower `Y` shows more of the top. Tune by eye, re-screenshot, repeat.
3. This applies separately to every place the same photo appears with `cover` cropping (post hero, `events.html` featured banner, `index.html` homepage card) — a fix in one spot doesn't carry to the others, each `<img>` needs its own `object-position` if needed.

## 5. Write the file

**Before writing, check the target filename doesn't already exist** (`Glob` for `blog-[slug]-ballito.html` or just try a `Read` and expect it to fail) — a slug collision would silently overwrite an existing post. If it exists, stop and confirm with the user rather than picking a different slug yourself.

Write the completed HTML to `C:\Users\HP\Desktop\Maddog Web design pages\blog-[slug]-ballito.html`. Deliver the complete file, not a snippet.

## 6. Feature the new post on events.html — read this section carefully, `events.html` is not a normal file

`events.html` is **~3MB**, almost entirely base64 image data. A plain `Read` of any range containing an image line will blow past the tool's token cap (confirmed: a 30-line slice once measured at 446,899 tokens). Never bulk-read or hand-edit it.

**Every new post automatically becomes the featured post** at the top of `events.html` (the `.hero-featured` / `.hero-feat-body` block shown at the very top of the page) — this is the confirmed, standing behavior, not something to ask about per post. Whatever was featured before it automatically moves down into the `.blog-card` grid ("previous posts") below. This whole rotation is handled by one script — `scripts/rotate_featured_post.py` — which was built and tested specifically because this file is too large and base64-heavy to safely hand-edit with `Read`/`Edit` (it extracts and relocates the old featured photo's data entirely within the script process, never through the LLM context).

Run it from the project root once the new post's file is written and its hero photo is optimized (§4b):

```bash
py .claude/skills/maddog-new-blog-post/scripts/rotate_featured_post.py \
  --new-tag "CATEGORY" \
  --new-title "FULL TITLE" \
  --new-date-iso YYYY-MM-DD \
  --new-excerpt "One to two sentence hook for the featured preview." \
  --new-href blog-[slug]-ballito.html \
  --new-image images/HASH.jpg
```

- `--new-image` is the `--type hero` output from §4b (same photo used for the blog post's own hero banner) — the featured slot on events.html is a similar wide banner, so reuse it rather than generating a third variant.
- It prints a `DEMOTED:` line (what got moved into the grid, and its new card id) and a `FEATURED NOW:` line — check both before reporting the task done.
- It writes an automatic `events.html.bak` backup before touching the real file, and refuses to run (raises an error, writes nothing) if the featured-block markup doesn't match what it expects — if that happens, stop and report the exact error rather than trying to patch around it.
- Add `--dry-run` first if you want to preview the demoted card / featured fields without writing anything.
- Never target the `.event-card` entries further down the same file (`<section class="events-sec" id="events">`) — those are upcoming live events, unrelated to blog posts, and this script doesn't touch them.
- **The `.blog-card` grid must stay sorted newest-first, always.** The script inserts the demoted card at the *top* of the grid (right after it opens), not the bottom — a real bug that shipped once (a fresh August post landed below a March one) before being caught and fixed. The top-insertion is correct *as long as the grid was already sorted* going in, since the demoted post is always the second-most-recent at the moment of rotation. If the grid's order ever looks wrong for any other reason, use `scripts/sort_events_grid.py` (parses every card's `bc-date`, re-sorts newest-first, safe to re-run any time) rather than hand-fixing it.

## 6b. Refresh the homepage's "Latest from Maddog" section — same treatment, different file

`index.html` (~4.8MB, same base64-heavy situation) has its own always-current section: two blog cards near the bottom, marked in the HTML with `<!-- Blog Post 1/2 — UPDATE CONTENT when a newer blog is published -->`. **The homepage always shows the 2 most recent posts** — confirmed standing behavior, run this every time, not something to ask about per post.

```bash
py .claude/skills/maddog-new-blog-post/scripts/rotate_homepage_posts.py \
  --new-cat "CATEGORY" \
  --new-title "FULL TITLE" \
  --new-text "One to two sentence teaser for the homepage card." \
  --new-href blog-[slug]-ballito.html \
  --new-image images/HASH.jpg
```

- Same `--new-image` as §6 (the `--type hero` output) — one photo, reused across the blog post, the featured slot, and this card.
- Behavior: slot 1's current post shifts down into slot 2; whatever was in slot 2 is dropped from the homepage (not deleted — it's still on `events.html`'s grid and in `sitemap.xml`, it just stops being one of the two promoted here); the new post takes slot 1.
- Prints `DROPPED FROM HOMEPAGE:`, `SHIFTED TO SLOT 2:`, and `NEW SLOT 1:` — check all three.
- Same safety model as §6: automatic `index.html.bak` backup before writing, refuses to run rather than guess if the markup doesn't match what it expects, `--dry-run` and `--index-file` (for testing against a scratch copy) both supported.
- **Ignore the `BLOG_POSTS` JS array further down `index.html`** — it's declared but never actually read/rendered by anything on the page (verified dead code, likely an abandoned earlier design). Don't update it as part of this workflow; it has no effect on what visitors see.

## 7. Update sitemap.xml

`sitemap.xml` is small and plain text — normal `Read`/`Edit` is fine here, no special handling needed.

Add one `<url>` entry in the "Blog Articles" section:

```xml
<url><loc>https://www.maddogperformance.co.za/blog-[slug]-ballito</loc><lastmod>YYYY-MM-DD</lastmod><changefreq>weekly</changefreq><priority>0.7</priority></url>
```

Note the URL has **no `.html` extension** — every existing sitemap entry follows this pattern (Netlify serves clean URLs). `changefreq` is `weekly` for a brand-new post (drop to `monthly` isn't needed until it's older), `priority` `0.7` matches the existing blog article entries (`0.8` is reserved for posts tied to a live event/promo).

Also bump the `<lastmod>` on the existing `/events` entry (currently near the top of the "Core Pages" section) to today's date — its content just changed too, and a stale `lastmod` there undersells the update to crawlers.

## 8. Pre-publish checklist

Before reporting the task done, run through `reference/checklist.md`. Don't skip it — it's the same checklist a human editor would use before hitting publish.

## 9. Report back

Summarize: filename created, events.html featured post rotated (§6), homepage "Latest from Maddog" rotated (§6b), sitemap.xml updated, and explicitly state **these changes are local only and nothing has been pushed**. Wait for the user's go-ahead before touching git.
