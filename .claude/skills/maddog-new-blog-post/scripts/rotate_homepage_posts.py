"""
Rotate the two "Latest from Maddog" blog cards on index.html.

index.html has a two-card preview block (blog1, blog2) near the bottom —
marked in the HTML with "UPDATE CONTENT when a newer blog is published"
comments, confirming this was always meant to be kept current by hand. This
script automates that:

  1. Whatever is currently in slot 1 shifts down into slot 2.
  2. Whatever was in slot 2 is dropped from the homepage entirely (it's not
     lost — it's still reachable via events.html's blog grid and sitemap.xml,
     it just stops being one of the two promoted on the homepage).
  3. The NEW post takes slot 1.

Like rotate_featured_post.py, this operates on the raw file directly and
never loads the file's multi-hundred-KB base64 image data through an LLM
context window — index.html is ~4.8MB. A backup is written to
index.html.bak before every write.

Usage:
    py scripts/rotate_homepage_posts.py \
        --new-cat "BJJ" \
        --new-title "Is Brazilian Jiu Jitsu Good for Beginners?" \
        --new-text "A short teaser sentence or two." \
        --new-href blog-new-slug-ballito.html \
        --new-image images/abcdef1234567890.jpg

    Add --dry-run to preview the change without writing anything.
"""
import argparse
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PAGES_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '..', '..'))
DEFAULT_INDEX_PATH = os.path.join(PAGES_DIR, 'index.html')


def extract(pattern, content, group=1, flags=0, label=''):
    m = re.search(pattern, content, flags)
    if not m:
        raise ValueError(f'Could not find expected pattern ({label or pattern}) in index.html — '
                          f'the homepage blog-preview markup may have changed. Stopping without writing anything.')
    return m.group(group)


def html_escape_text(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def extract_card(content, img_id, search_from=0):
    img_re = re.compile(rf'<img loading="lazy" id="{img_id}-img"[^>]*?>', re.DOTALL)
    m = img_re.search(content, search_from)
    if not m:
        raise ValueError(f'Could not find the {img_id}-img <img> tag. Stopping without writing anything.')
    img_tag = m.group(0)
    src = extract(r'src="([^"]*)"', img_tag, flags=re.DOTALL, label=f'{img_id} src')
    alt_match = re.search(r'alt="([^"]*)"', img_tag, re.DOTALL)
    alt = alt_match.group(1) if alt_match else ''

    after = content[m.end():]
    cat = extract(r'<div class="nc-cat">(.*?)</div>', after, label=f'{img_id} nc-cat')
    title = extract(r'<div class="nc-title">(.*?)</div>', after, flags=re.DOTALL, label=f'{img_id} nc-title')
    text = extract(r'<p class="nc-text">(.*?)</p>', after, flags=re.DOTALL, label=f'{img_id} nc-text')
    href = extract(r'<a href="([^"]*)" class="blog-read-more">Read More</a>', after, label=f'{img_id} href')

    return {'src': src, 'alt': alt, 'cat': cat, 'title': title, 'text': text, 'href': href, 'tag_end': m.end()}


def build_card(comment, img_id, img_src, alt, cat, title, text, href):
    return (
        f'\n      <!-- {comment} -->\n'
        f'      <div class="blog-card">\n'
        f'        <div class="nc-img">\n'
        f'          <div class="photo-slot loaded" id="{img_id}">\n'
        f'            <img loading="lazy" id="{img_id}-img" src="{img_src}" alt="{alt}">\n'
        f'          </div>\n'
        f'        </div>\n'
        f'        <div class="nc-body">\n'
        f'          <div class="nc-cat">{cat}</div>\n'
        f'          <div class="nc-title">{title}</div>\n'
        f'          <p class="nc-text">{text}</p>\n'
        f'          <a href="{href}" class="blog-read-more">Read More</a>\n'
        f'        </div>\n'
        f'      </div>\n'
    )


def main():
    parser = argparse.ArgumentParser(description='Rotate the two homepage "Latest from Maddog" blog cards.')
    parser.add_argument('--new-cat', required=True)
    parser.add_argument('--new-title', required=True)
    parser.add_argument('--new-text', required=True, help='Short teaser paragraph (nc-text)')
    parser.add_argument('--new-href', required=True, help='e.g. blog-new-slug-ballito.html')
    parser.add_argument('--new-image', required=True, help='e.g. images/abcdef1234567890.jpg (relative to project root)')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--index-file', default=DEFAULT_INDEX_PATH,
                         help='Override the index.html path (used for testing against a scratch copy).')
    args = parser.parse_args()

    INDEX_PATH = args.index_file

    if not os.path.isfile(INDEX_PATH):
        print(f'ERROR: index.html not found at {INDEX_PATH}', file=sys.stderr)
        sys.exit(1)

    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # ---- 1. Extract current slot 1 and slot 2 ----
    blog1 = extract_card(content, 'blog1')
    blog2 = extract_card(content, 'blog2', search_from=blog1['tag_end'])

    # ---- 2. Build the new two-card block ----
    new_title_esc = html_escape_text(args.new_title)
    new_text_esc = html_escape_text(args.new_text)
    # args.new_cat is NOT escaped — a caller may legitimately pass an HTML entity
    # (matches the wellness-side scripts' convention for tags like "IV Therapy &middot; Nutrition").
    new_cat_esc = args.new_cat
    new_alt = html_escape_text(re.sub(r'<[^>]+>', '', args.new_title))

    card1 = build_card('Blog Post 1 — UPDATE CONTENT when a newer blog is published',
                        'blog1', args.new_image, new_alt, new_cat_esc, new_title_esc, new_text_esc, args.new_href)
    card2 = build_card('Blog Post 2 — UPDATE CONTENT when a newer blog is published',
                        'blog2', blog1['src'], blog1['alt'], blog1['cat'], blog1['title'], blog1['text'], blog1['href'])

    # ---- 3. Replace the whole two-card block ----
    boundary_re = re.compile(r'<!-- Blog Post 1.*?</div>\s*</div>\s*</div>\s*</section>', re.DOTALL)
    boundary_match = boundary_re.search(content)
    if not boundary_match:
        raise ValueError('Could not find the homepage blog-preview block boundary (from "<!-- Blog Post 1" '
                          'to the closing </section>). The page structure may have changed — update manually.')

    replacement = card1 + card2 + '    </div>\n  </div>\n</section>'
    new_content = content[:boundary_match.start()] + replacement + content[boundary_match.end():]

    print(f'DROPPED FROM HOMEPAGE: "{blog2["title"]}" (still reachable via events.html and sitemap.xml)')
    print(f'SHIFTED TO SLOT 2: "{blog1["title"]}"')
    print(f'NEW SLOT 1: "{args.new_title}"')

    if args.dry_run:
        print('\n--dry-run set: nothing written. Re-run without --dry-run to apply.')
        return

    backup_path = INDEX_PATH + '.bak'
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Backup written: {backup_path}')

    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'index.html updated ({len(new_content)} bytes).')


if __name__ == '__main__':
    main()
