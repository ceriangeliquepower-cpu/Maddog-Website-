"""
Rotate the featured post on events.html.

events.html has a single "featured post" block near the top of the page
(the .hero-featured / .hero-feat-body markup) plus a separate grid of
.blog-card entries further down ("previous posts"). This script:

  1. Reads whatever is CURRENTLY featured (tag, title, date, excerpt, href,
     photo) and turns it into a new .blog-card entry in the grid.
  2. Replaces the featured block with the NEW post's details.

It operates on the raw file directly (never loads the multi-hundred-KB
base64 image data through an LLM context window — events.html is ~3MB and a
naive read of it will blow past normal tool limits). A backup is written to
events.html.bak before every write.

Usage:
    py scripts/rotate_featured_post.py \
        --new-tag "BJJ" \
        --new-title "Is Brazilian Jiu Jitsu Good for Beginners?" \
        --new-date-iso 2026-09-03 \
        --new-excerpt "A short teaser sentence or two." \
        --new-href blog-new-slug-ballito.html \
        --new-image images/abcdef1234567890.jpg

    Add --dry-run to preview the change without writing anything.
"""
import argparse
import base64
import io
import os
import re
import sys
from datetime import datetime

from PIL import Image

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PAGES_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '..', '..'))
DEFAULT_EVENTS_PATH = os.path.join(PAGES_DIR, 'events.html')


def extract(pattern, content, group=1, flags=0, label=''):
    m = re.search(pattern, content, flags)
    if not m:
        raise ValueError(f'Could not find expected pattern ({label or pattern}) in events.html — '
                          f'the featured-post markup may have changed. Stopping without writing anything.')
    return m.group(group)


def html_escape_text(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def estimate_read_minutes(blog_path):
    if not os.path.isfile(blog_path):
        return 5  # fallback if the linked post file can't be found
    with open(blog_path, 'r', encoding='utf-8') as f:
        blog_content = f.read()
    body_match = re.search(r'<div class="article-body">(.*?)<div class="article-cta',
                            blog_content, re.DOTALL)
    if not body_match:
        return 5
    text_only = re.sub(r'<[^>]+>', ' ', body_match.group(1))
    words = len(text_only.split())
    return max(3, round(words / 200))


def main():
    parser = argparse.ArgumentParser(description='Rotate the featured post on events.html.')
    parser.add_argument('--new-tag', required=True)
    parser.add_argument('--new-title', required=True)
    parser.add_argument('--new-date-iso', required=True, help='YYYY-MM-DD')
    parser.add_argument('--new-excerpt', required=True)
    parser.add_argument('--new-href', required=True, help='e.g. blog-new-slug-ballito.html')
    parser.add_argument('--new-image', required=True, help='e.g. images/abcdef1234567890.jpg (relative to project root)')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--events-file', default=DEFAULT_EVENTS_PATH,
                         help='Override the events.html path (used for testing against a scratch copy).')
    args = parser.parse_args()

    EVENTS_PATH = args.events_file

    if not os.path.isfile(EVENTS_PATH):
        print(f'ERROR: events.html not found at {EVENTS_PATH}', file=sys.stderr)
        sys.exit(1)

    with open(EVENTS_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # ---- 1. Extract the CURRENT featured post's fields ----
    old_tag = extract(r'<span class="hf-tag">(.*?)</span>', content, label='hf-tag')
    old_title = extract(r'<div class="hf-title">(.*?)</div>', content, flags=re.DOTALL, label='hf-title')
    old_date_iso = extract(r'<div class="hf-date"><time datetime="([^"]*)">', content, label='hf-date iso')
    old_excerpt = extract(r'<p class="hf-excerpt">(.*?)</p>', content, flags=re.DOTALL, label='hf-excerpt')
    old_href = extract(r'<a href="([^"]*)" class="btn btn-o btn-sm" style="margin-top:14px">Read Article</a>',
                        content, label='featured article link')

    img_match = re.search(r'<img id="featPhoto-img"[^>]*?>', content, re.DOTALL)
    if not img_match:
        raise ValueError('Could not find the featured photo <img> tag. Stopping without writing anything.')
    old_img_tag = img_match.group(0)
    src_match = re.search(r'src="([^"]*)"', old_img_tag, re.DOTALL)
    if not src_match:
        raise ValueError('Featured photo <img> has no src attribute — check it manually.')
    old_img_src = src_match.group(1)

    # The featured photo may be an old base64 data URI (legacy posts) or a
    # short images/HASH.jpg file path (posts promoted by this script since
    # the file-based convention took over) — handle both.
    if old_img_src.startswith('data:image/'):
        _, b64data = old_img_src.split(',', 1)
        img_bytes = base64.b64decode(b64data)
        old_w, old_h = Image.open(io.BytesIO(img_bytes)).size
    else:
        old_image_path = os.path.join(PAGES_DIR, old_img_src)
        if not os.path.isfile(old_image_path):
            raise ValueError(f'Featured photo file not found: {old_image_path}')
        old_w, old_h = Image.open(old_image_path).size

    old_date_obj = datetime.strptime(old_date_iso, '%Y-%m-%d')
    month_year = old_date_obj.strftime('%B %Y')
    read_min = estimate_read_minutes(os.path.join(PAGES_DIR, old_href))
    bc_date = f'{month_year} · {read_min} min read'

    slug = re.sub(r'^blog-', '', old_href)
    slug = re.sub(r'-ballito\.html$', '', slug)
    slug = re.sub(r'\.html$', '', slug)
    new_card_id = f'bp-{slug}'
    if re.search(rf'id="{re.escape(new_card_id)}"', content):
        new_card_id = f'{new_card_id}-{old_date_iso.replace("-", "")}'

    alt_text = html_escape_text(re.sub(r'<[^>]+>', '', old_title))

    demoted_card = (
        f'\n      <!-- POST: rotated from featured, {old_date_iso} -->\n'
        f'      <div class="blog-card" id="{new_card_id}">\n'
        f'        <div class="bc-img"><img src="{old_img_src}" alt="{alt_text}" '
        f'width="{old_w}" height="{old_h}" style="width:100%;height:100%;object-fit:cover" loading="lazy"></div>\n'
        f'        <div class="bc-body">\n'
        f'          <span class="bc-tag">{old_tag}</span>\n'
        f'          <div class="bc-title">{old_title}</div>\n'
        f'          <p class="bc-excerpt">{old_excerpt}</p>\n'
        f'          <div class="bc-date">{bc_date}</div>\n'
        f'          <div class="bc-edit-row">\n'
        f'            <a href="{old_href}" class="btn btn-o btn-sm">Read Full Article</a>\n'
        f'          </div>\n'
        f'        </div>\n'
        f'      </div>\n'
    )

    # ---- 2. Find the grid insertion point (top of the grid, not the bottom) ----
    # The grid must stay sorted newest-first. The demoted post is always the second-most-
    # recent post at the moment of rotation (an even newer one just replaced it as
    # featured), so as long as the grid was already correctly sorted, inserting it right
    # after the grid opens keeps that order — inserting at the bottom (the old behavior)
    # broke sort order by dumping a fresh post below much older ones. See sort_events_grid.py
    # for a one-time/re-runnable fix if the grid's order ever needs re-establishing from scratch.
    grid_open_marker = '<div class="blog-grid" id="blogGrid" style="margin-top:6px">'
    grid_open_idx = content.find(grid_open_marker)
    if grid_open_idx == -1:
        raise ValueError('Could not find the blog-grid opening tag (id="blogGrid"). '
                          'The page structure may have changed — insert the new card manually.')
    insert_at = grid_open_idx + len(grid_open_marker)

    new_content = content[:insert_at] + demoted_card + content[insert_at:]

    # ---- 3. Overwrite the featured block with the NEW post ----
    new_title_esc = html_escape_text(args.new_title)
    new_excerpt_esc = html_escape_text(args.new_excerpt)
    new_date_obj = datetime.strptime(args.new_date_iso, '%Y-%m-%d')
    new_date_display = new_date_obj.strftime('%-d %B %Y') if os.name != 'nt' else new_date_obj.strftime('%#d %B %Y')

    # args.new_tag is NOT escaped — a caller may legitimately pass an HTML entity
    # (matches the wellness-side scripts' convention for tags like "IV Therapy &middot; Nutrition").
    new_content = re.sub(r'<span class="hf-tag">.*?</span>',
                          f'<span class="hf-tag">{args.new_tag}</span>',
                          new_content, count=1)
    new_content = re.sub(r'<div class="hf-title">.*?</div>',
                          f'<div class="hf-title">{new_title_esc}</div>',
                          new_content, count=1, flags=re.DOTALL)
    new_content = re.sub(r'<div class="hf-date"><time datetime="[^"]*">[^<]*</time> · Maddog Performance Institute</div>',
                          f'<div class="hf-date"><time datetime="{args.new_date_iso}">{new_date_display}</time> · Maddog Performance Institute</div>',
                          new_content, count=1)
    new_content = re.sub(r'<p class="hf-excerpt">.*?</p>',
                          f'<p class="hf-excerpt">{new_excerpt_esc}</p>',
                          new_content, count=1, flags=re.DOTALL)
    new_content = re.sub(r'<a href="[^"]*" class="btn btn-o btn-sm" style="margin-top:14px">Read Article</a>',
                          f'<a href="{args.new_href}" class="btn btn-o btn-sm" style="margin-top:14px">Read Article</a>',
                          new_content, count=1)
    new_content = re.sub(r'<img id="featPhoto-img"[^>]*?>',
                          f'<img id="featPhoto-img" src="{args.new_image}" alt="{new_title_esc}">',
                          new_content, count=1, flags=re.DOTALL)

    print(f'DEMOTED: "{old_title}" -> new grid card id="{new_card_id}" ({old_w}x{old_h}, {bc_date})')
    print(f'FEATURED NOW: "{args.new_title}" ({args.new_tag}, {args.new_date_iso})')

    if args.dry_run:
        print('\n--dry-run set: nothing written. Re-run without --dry-run to apply.')
        return

    backup_path = EVENTS_PATH + '.bak'
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Backup written: {backup_path}')

    with open(EVENTS_PATH, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'events.html updated ({len(new_content)} bytes).')


if __name__ == '__main__':
    main()
