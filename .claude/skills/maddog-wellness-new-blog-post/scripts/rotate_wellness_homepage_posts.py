"""
Rotate the two "From The Blog" teaser cards on wellness.html's homepage.

Mirrors the gym site's rotate_homepage_posts.py exactly, same behavior:
every new wellness post takes slot 1, whatever was in slot 1 shifts to
slot 2, and whatever was in slot 2 drops off the homepage teaser (it's not
lost — it's still on wellness-blog.html's Insights grid and in
sitemap.xml, it just stops being one of the two promoted on the homepage).

wellness.html's teaser section uses the site's whole-card-is-a-link markup
(<a class="blog-card">...) rather than index.html's nc-cat/nc-title
structure, so this is a separate script, not a shared one — but the
mechanism is identical. Operates on the raw file directly; wellness.html
is ~3MB+ of base64 image data, so this never bulk-reads it.

Usage:
    py scripts/rotate_wellness_homepage_posts.py \
        --new-tag "IV Therapy &middot; Nutrition" \
        --new-title "New Post Title" \
        --new-excerpt "One to two sentence hook." \
        --new-href wellness-blog-new-slug.html \
        --new-image images/abcdef1234567890.jpg

    Add --dry-run to preview without writing anything.
"""
import argparse
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PAGES_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '..', '..'))
DEFAULT_WELLNESS_PATH = os.path.join(PAGES_DIR, 'wellness.html')


def extract(pattern, content, group=1, flags=0, label=''):
    m = re.search(pattern, content, flags)
    if not m:
        raise ValueError(f'Could not find expected pattern ({label or pattern}) in wellness.html — '
                          f'the blog-teaser markup may have changed. Stopping without writing anything.')
    return m.group(group)


def html_escape_text(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def extract_card(content, search_from=0):
    """Extract one <a class="blog-card">...</a> block starting from search_from.
    Returns the extracted fields plus the end position of the whole card."""
    card_start = content.find('<a href="', search_from)
    href_match = re.match(r'<a href="([^"]*)" class="blog-card">', content[card_start:card_start + 200])
    if not href_match:
        raise ValueError('Could not find a <a href="..." class="blog-card"> opening tag. Stopping without writing anything.')
    href = href_match.group(1)

    # Search from card_start using the pos argument rather than slicing a substring —
    # slicing risks truncating mid-base64 before the tag's closing '>' is reached.
    img_match = re.compile(r'<img[^>]*?>', re.DOTALL).search(content, card_start)
    if not img_match:
        raise ValueError(f'Could not find the <img> tag for card linking to {href}.')
    img_tag = img_match.group(0)
    img_abs_start = img_match.start()
    img_abs_end = img_match.end()

    src = extract(r'src="([^"]*)"', img_tag, flags=re.DOTALL, label='card img src')
    alt_m = re.search(r'alt="([^"]*)"', img_tag, re.DOTALL)
    alt = alt_m.group(1) if alt_m else ''

    after_img = content[img_abs_end:img_abs_end + 2000]
    tag = extract(r'<div class="blog-card-tag">(.*?)</div>', after_img, label='blog-card-tag')
    title = extract(r'<h2 class="blog-card-title">(.*?)</h2>', after_img, flags=re.DOTALL, label='blog-card-title')
    excerpt = extract(r'<p class="blog-card-excerpt">(.*?)</p>', after_img, flags=re.DOTALL, label='blog-card-excerpt')

    card_end = content.find('</a>', img_abs_end) + len('</a>')

    return {'href': href, 'src': src, 'alt': alt, 'tag': tag, 'title': title,
            'excerpt': excerpt, 'card_start': card_start, 'card_end': card_end}


def build_card(href, img_src, alt, tag, title, excerpt):
    return (
        f'\n      <a href="{href}" class="blog-card">\n'
        f'        <div class="blog-card-img">\n'
        f'          <img src="{img_src}" alt="{alt}" loading="lazy">\n'
        f'        </div>\n'
        f'        <div class="blog-card-body">\n'
        f'          <div class="blog-card-tag">{tag}</div>\n'
        f'          <h2 class="blog-card-title">{title}</h2>\n'
        f'          <p class="blog-card-excerpt">{excerpt}</p>\n'
        f'          <span class="blog-card-link">Read Article &rarr;</span>\n'
        f'        </div>\n'
        f'      </a>\n'
    )


def main():
    parser = argparse.ArgumentParser(description='Rotate the two homepage "From The Blog" teaser cards on wellness.html.')
    parser.add_argument('--new-tag', required=True)
    parser.add_argument('--new-title', required=True)
    parser.add_argument('--new-excerpt', required=True)
    parser.add_argument('--new-href', required=True, help='e.g. wellness-blog-new-slug.html')
    parser.add_argument('--new-image', required=True, help='e.g. images/abcdef1234567890.jpg (relative to project root)')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--wellness-file', default=DEFAULT_WELLNESS_PATH,
                         help='Override the wellness.html path (used for testing against a scratch copy).')
    args = parser.parse_args()

    WELLNESS_PATH = args.wellness_file

    if not os.path.isfile(WELLNESS_PATH):
        print(f'ERROR: wellness.html not found at {WELLNESS_PATH}', file=sys.stderr)
        sys.exit(1)

    with open(WELLNESS_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    grid_marker = '<div class="w-blog-teaser-grid">'
    grid_idx = content.find(grid_marker)
    if grid_idx == -1:
        raise ValueError('Could not find <div class="w-blog-teaser-grid"> on wellness.html — '
                          'the homepage teaser section may have changed. Stopping without writing anything.')
    grid_start = grid_idx + len(grid_marker)

    slot1 = extract_card(content, grid_start)
    slot2 = extract_card(content, slot1['card_end'])

    grid_close = content.find('</div>', slot2['card_end'])
    if grid_close == -1:
        raise ValueError('Could not find the closing </div> of the teaser grid. Stopping without writing anything.')

    new_title_esc = html_escape_text(args.new_title)
    new_excerpt_esc = html_escape_text(args.new_excerpt)
    new_alt = html_escape_text(re.sub(r'<[^>]+>', '', args.new_title))

    # args.new_tag is NOT escaped — the wellness site's two-part tag convention
    # ("IV Therapy &middot; Nutrition") relies on passing real HTML entities
    # through as-is, matching prepend_wellness_blog_card.py's same convention.
    card1 = build_card(args.new_href, args.new_image, new_alt, args.new_tag, new_title_esc, new_excerpt_esc)
    card2 = build_card(slot1['href'], slot1['src'], slot1['alt'], slot1['tag'], slot1['title'], slot1['excerpt'])

    new_content = content[:grid_start] + card1 + card2 + '    ' + content[grid_close:]

    print(f'DROPPED FROM HOMEPAGE: "{slot2["title"]}" (still reachable via wellness-blog.html and sitemap.xml)')
    print(f'SHIFTED TO SLOT 2: "{slot1["title"]}"')
    print(f'NEW SLOT 1: "{args.new_title}"')

    if args.dry_run:
        print('\n--dry-run set: nothing written. Re-run without --dry-run to apply.')
        return

    backup_path = WELLNESS_PATH + '.bak'
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Backup written: {backup_path}')

    with open(WELLNESS_PATH, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'wellness.html updated ({len(new_content)} bytes).')


if __name__ == '__main__':
    main()
