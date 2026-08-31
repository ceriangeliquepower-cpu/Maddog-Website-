# Pre-publish checklist — new gym blog post

Run through this before telling the user the post is ready. It's the blog-specific subset of CLAUDE.md's site-wide rules — check the file itself against each line, don't just skim.

## Brand
- [ ] "Maddog" used throughout — no "Mad Dog", "MadDog", "MADDOG" anywhere in title, body, alt text, or JSON-LD
- [ ] User's original content meaning/facts preserved — only brand-name, typo, and light tone edits made
- [ ] No invented experiential detail — every claim of something that happened is either from the user's own content or explicitly flagged to them as an inference, not stated as fact

## SEO — head block
- [ ] `<title>` ≤60 chars, primary keyword near the front, ends "| Maddog Performance Institute | Ballito KZN"
- [ ] `<meta name="description">` is 150–160 chars, reads as a real sentence, includes the primary keyword
- [ ] `<link rel="canonical">` points to the extension-less URL matching the sitemap pattern
- [ ] OG tags (`og:type=article`, `og:title`, `og:description`, `og:url`, `og:site_name`) all updated, not left as template defaults
- [ ] Twitter card tags updated to match
- [ ] `robots` = `index, follow`, geo tags present
- [ ] Article JSON-LD: `headline`, `description`, `datePublished`, `dateModified`, `mainEntityOfPage`, `image` all filled in (not template placeholders)
- [ ] BreadcrumbList JSON-LD: position 3 has the real title and real URL
- [ ] LocalBusiness (`SportsActivityLocation`) JSON-LD block added — template doesn't ship one by default, see `reference/localbusiness-jsonld.json`

## Semantic HTML / headings
- [ ] Exactly one `<h1>` (the hero title)
- [ ] `<h2>` for main sections, `<h3>` only nested under an `<h2>` — no skipped levels
- [ ] Lists use `<ul>`/`<ol>`, not manual dash/bullet characters in `<p>` tags

## Images
- [ ] Blog post's hero photo went through `optimize_photo.py --type hero` — not base64, not an unresized original
- [ ] `width`/`height` in the blog post's own hero `<img>` match what the script reported, not guessed values
- [ ] Every `<img>` has a real, descriptive `alt` — never empty for a content photo
- [ ] Blog post hero image (above the fold) has **no** `loading="lazy"`
- [ ] Raw original stayed in `raw-photos/` — nothing large/unresized got written into `images/`
- [ ] Crop checked via a real local server (`maddog-static` preview, not a direct `file://` open) on every place the photo appears with `object-fit:cover` (post hero, events.html featured banner, index.html homepage card) — no faces/people cut off; `object-position` tuned per-spot if needed

## Internal linking
- [ ] At least 2 internal links to other real pages on the site, contextually relevant to the topic (not just the footer nav)
- [ ] `sitemap.xml` has a new `<url>` entry, extension-less, in the Blog Articles section
- [ ] `sitemap.xml`'s existing `/events` entry `lastmod` bumped to today

## Featured-post rotation (events.html)
- [ ] Confirmed the target `blog-[slug]-ballito.html` filename didn't already exist before writing (no silent overwrite of an existing post)
- [ ] `events.html` was never bulk-`Read` or hand-edited — the rotation went through `scripts/rotate_featured_post.py`
- [ ] Script's `DEMOTED:` and `FEATURED NOW:` output lines checked and both look right (correct old post demoted, correct new post now featured)
- [ ] `events.html.bak` no longer exists (cleaned up after the write was verified) as a rollback point
- [ ] Nothing touched the `.event-card` (upcoming live events) section further down the same file
- [ ] The `.blog-card` grid is still sorted newest-first after the rotation (spot-check the demoted post landed at the top of the grid, not the bottom)

## Homepage rotation (index.html)
- [ ] `index.html` was never bulk-`Read` or hand-edited — the rotation went through `scripts/rotate_homepage_posts.py`
- [ ] Script's `DROPPED FROM HOMEPAGE:`, `SHIFTED TO SLOT 2:`, and `NEW SLOT 1:` output lines checked and all three look right
- [ ] `index.html.bak` no longer exists (cleaned up after the write was verified)
- [ ] The dead `BLOG_POSTS` JS array further down `index.html` was left alone (it doesn't render anything, not worth touching)

## Accessibility
- [ ] Colour contrast unaffected — don't introduce new inline colours outside the existing CSS variables
- [ ] Any new interactive element (if the topic needed one) is a real `<button>`/`<a>`, not a `<div onclick>`

## Mobile
- [ ] No new fixed pixel widths introduced that could cause horizontal scroll — content only, template CSS already handles this
- [ ] If the article body contains anything beyond plain text/lists/quotes, sanity-check it doesn't overflow at 375px

## Workflow
- [ ] File saved to the main project folder (`C:\Users\HP\Desktop\Maddog Web design pages\`), not a worktree
- [ ] The new file was created by duplicating `blog-TEMPLATE.html` (`cp` or equivalent), never hand-retyped — spot check `.nav-has-dropdown`/`.nav-drop-menu` CSS is present in the `<style>` block if there's any doubt
- [ ] Nothing has been committed or pushed — confirmed local-only in the summary given to the user
