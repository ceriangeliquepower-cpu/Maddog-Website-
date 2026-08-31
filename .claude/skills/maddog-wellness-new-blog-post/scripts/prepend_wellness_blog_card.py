"""
Add a new post to the top of the wellness Insights grid on wellness-blog.html.

Unlike the gym site, wellness-blog.html has no rotating "featured" slot and
wellness.html (the wellness homepage) has no blog-preview section at all —
it just links to wellness-blog.html. So there's nothing to rotate or demote:
every new post is simply inserted at the very top of the grid (newest first),
and older posts stay exactly where they are, forever, until the page is
pruned deliberately.

wellness-blog.html still carries base64 image data for its existing cards
(legacy, same situation as the gym site before its own convention changed),
so this operates on the raw file directly rather than through Read/Edit.

Usage:
    py scripts/prepend_wellness_blog_card.py \
        --new-tag "Recovery &middot; Contrast Therapy" \
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
DEFAULT_BLOG_PATH = os.path.join(PAGES_DIR, 'wellness-blog.html')


def html_escape_text(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def main():
    parser = argparse.ArgumentParser(description='Prepend a new card to the wellness Insights grid.')
    parser.add_argument('--new-tag', required=True, help='e.g. "IV Therapy &middot; Nutrition" (HTML entities allowed, not escaped further)')
    parser.add_argument('--new-title', required=True)
    parser.add_argument('--new-excerpt', required=True)
    parser.add_argument('--new-href', required=True, help='e.g. wellness-blog-new-slug.html')
    parser.add_argument('--new-image', required=True, help='e.g. images/abcdef1234567890.jpg (relative to project root)')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--blog-file', default=DEFAULT_BLOG_PATH,
                         help='Override the wellness-blog.html path (used for testing against a scratch copy).')
    args = parser.parse_args()

    BLOG_PATH = args.blog_file

    if not os.path.isfile(BLOG_PATH):
        print(f'ERROR: wellness-blog.html not found at {BLOG_PATH}', file=sys.stderr)
        sys.exit(1)

    with open(BLOG_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    if f'href="{args.new_href}"' in content:
        print(f'ERROR: a card linking to "{args.new_href}" already exists in wellness-blog.html — '
              f'refusing to insert a duplicate. Stopping without writing anything.', file=sys.stderr)
        sys.exit(1)

    anchor = '<div class="blog-grid">'
    idx = content.find(anchor)
    if idx == -1:
        raise ValueError('Could not find <div class="blog-grid"> in wellness-blog.html — '
                          'the page structure may have changed. Stopping without writing anything.')
    insert_at = idx + len(anchor)

    title_esc = html_escape_text(args.new_title)
    excerpt_esc = html_escape_text(args.new_excerpt)
    alt_text = html_escape_text(re.sub(r'<[^>]+>', '', args.new_title))

    new_card = (
        f'\n\n      <a href="{args.new_href}" class="blog-card">\n'
        f'        <div class="blog-card-img">\n'
        f'          <img src="{args.new_image}" alt="{alt_text}" loading="lazy">\n'
        f'        </div>\n'
        f'        <div class="blog-card-body">\n'
        f'          <div class="blog-card-tag">{args.new_tag}</div>\n'
        f'          <h2 class="blog-card-title">{title_esc}</h2>\n'
        f'          <p class="blog-card-excerpt">{excerpt_esc}</p>\n'
        f'          <span class="blog-card-link">Read Article &rarr;</span>\n'
        f'        </div>\n'
        f'      </a>'
    )

    new_content = content[:insert_at] + new_card + content[insert_at:]

    print(f'ADDED TO TOP OF INSIGHTS GRID: "{args.new_title}" -> {args.new_href}')

    if args.dry_run:
        print('\n--dry-run set: nothing written. Re-run without --dry-run to apply.')
        return

    backup_path = BLOG_PATH + '.bak'
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Backup written: {backup_path}')

    with open(BLOG_PATH, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'wellness-blog.html updated ({len(new_content)} bytes).')


if __name__ == '__main__':
    main()
