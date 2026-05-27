"""
Extract base64-embedded images from all HTML files into images/ folder.
Handles both:
  - src="data:image/..."         (img tags)
  - url(data:image/...)           (CSS background-image, no quotes)
  - url('data:image/...')         (CSS background-image, single quotes)
  - url("data:image/...")         (CSS background-image, double quotes)
Deduplicates: same image data = same file referenced from multiple pages.
"""
import os
import base64
import hashlib

PAGES_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(PAGES_DIR, 'images')
os.makedirs(IMAGES_DIR, exist_ok=True)

SKIP_FILES = {'blog-TEMPLATE.html', 'Mad Dog I.V Bar & Recovery Lounge.html'}

html_files = sorted([
    f for f in os.listdir(PAGES_DIR)
    if f.endswith('.html') and f not in SKIP_FILES
])

hash_map = {}   # md5 -> filename  (deduplication across all pages)

def extract_one(content, marker_start, end_char):
    """
    From `content`, replace all occurrences of:
        <marker_start>data:image/TYPE;base64,DATA<end_char>
    with:
        <marker_start>images/HASH.EXT<end_char>
    Returns (new_content, changes_count).
    """
    parts = []
    pos = 0
    changes = 0

    while True:
        idx = content.find(marker_start + 'data:image/', pos)
        if idx == -1:
            parts.append(content[pos:])
            break

        parts.append(content[pos:idx + len(marker_start)])

        type_start = idx + len(marker_start) + len('data:image/')
        semicolon  = content.index(';', type_start)
        img_type   = content[type_start:semicolon].lower()
        if img_type == 'jpeg':
            img_type = 'jpg'

        # Only process base64-encoded images; skip URL-encoded SVGs etc.
        b64_marker_pos = content.find('base64,', semicolon)
        next_end_pos   = content.find(end_char, semicolon)
        if b64_marker_pos == -1 or b64_marker_pos > next_end_pos:
            # Not base64 — skip this match
            parts.append(content[idx + len(marker_start):idx + len(marker_start) + len('data:image/')])
            pos = idx + len(marker_start) + len('data:image/')
            continue

        b64_start = b64_marker_pos + len('base64,')
        b64_end   = content.index(end_char, b64_start)
        b64_data  = content[b64_start:b64_end]

        img_hash = hashlib.md5(b64_data.encode()).hexdigest()[:16]

        if img_hash in hash_map:
            filename = hash_map[img_hash]
        else:
            filename = f'{img_hash}.{img_type}'
            hash_map[img_hash] = filename
            img_bytes = base64.b64decode(b64_data)
            with open(os.path.join(IMAGES_DIR, filename), 'wb') as out:
                out.write(img_bytes)

        parts.append(f'images/{filename}')
        pos = b64_end       # end_char itself stays in place (consumed by next loop or appended above)
        changes += 1

    return ''.join(parts), changes


total_pages_changed = 0

for html_file in html_files:
    filepath = os.path.join(PAGES_DIR, html_file)
    with open(filepath, 'r', encoding='utf-8') as fh:
        content = fh.read()

    original_len = len(content)
    total_changes = 0

    # 1. src="data:image/..."
    content, n = extract_one(content, 'src="', '"')
    total_changes += n

    # 2. url(data:image/...)   — no quotes
    content, n = extract_one(content, 'url(', ')')
    total_changes += n

    # 3. url('data:image/...')  — single quotes (end_char is the single quote before ')')
    content, n = extract_one(content, "url('", "'")
    total_changes += n

    # 4. url("data:image/...")  — double quotes
    content, n = extract_one(content, 'url("', '"')
    total_changes += n

    if total_changes > 0:
        with open(filepath, 'w', encoding='utf-8') as fh:
            fh.write(content)
        saved_kb = (original_len - len(content)) / 1024
        print(f'UPDATED: {html_file}  ({total_changes} images, -{saved_kb:.0f} KB)')
        total_pages_changed += 1
    else:
        print(f'NO CHANGE: {html_file}')

print()
print(f'Unique image files in images/: {len(hash_map)}')
print(f'Pages changed: {total_pages_changed}')
