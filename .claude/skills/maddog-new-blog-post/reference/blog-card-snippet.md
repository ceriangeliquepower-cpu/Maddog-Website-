# events.html blog card markup

**Not the normal path anymore.** Every new post now goes through the featured slot first (SKILL.md §6, via `scripts/rotate_featured_post.py`), which builds and inserts its own demoted-card markup automatically — you shouldn't need to hand-write a card for a brand-new post. Keep this reference only for the rare manual-fallback case (the script errors out and needs a human-guided fix, or the user explicitly asks for a card without going through the featured rotation).

Insert a new block like this among the other `.blog-card` divs in `events.html` (they sit before the `.event-card` entries further down the file — don't confuse the two, they use different classes and layouts).

```html
<!-- POST [N] -->
<div class="blog-card" id="bp[N]">
  <div class="bc-img">
    <img src="images/FILENAME.jpg" alt="DESCRIPTIVE ALT TEXT" width="WIDTH" height="HEIGHT" style="width:100%;height:100%;object-fit:cover" loading="lazy">
  </div>
  <div class="bc-body">
    <span class="bc-tag">CATEGORY</span>
    <div class="bc-title">FULL TITLE</div>
    <p class="bc-excerpt">One to two sentence hook — a question or a promise, not a restatement of the meta description.</p>
    <div class="bc-date">Month Year · N min read</div>
    <div class="bc-edit-row">
      <a href="blog-[slug]-ballito.html" class="btn btn-o btn-sm">Read Full Article</a>
    </div>
  </div>
</div>
```

Notes:

- `id="bp[N]"` — check the highest existing `bp` number in the file first (search for `id="bp` — as of the last time this was checked, entries ran `bp1` through `bp8` plus a few named ids like `bp-genesis`, `bp-community-stlukes`; don't assume the count, re-check every time).
- This markup uses a plain `<img src="images/...">` — the output of `optimize_photo.py --type card` — rather than the `photo-slot` / base64 pattern some older cards still carry. See SKILL.md §4b for why — the live-upload mechanism was removed site-wide, so new cards shouldn't reintroduce it, and unoptimized images slow the page down.
- `loading="lazy"` is correct here since blog cards sit below the fold on `events.html` — this is a below-the-fold card image, unlike the blog post's own hero image which must NOT be lazy-loaded.
- Use the exact `WIDTH`/`HEIGHT` that `optimize_photo.py --type card` reported for this image — don't hardcode a fixed size, `object-fit:cover` handles the crop-to-fit regardless of the source aspect ratio.
