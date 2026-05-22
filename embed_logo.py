"""
embed_logo.py
- Strips black background from MD LOGO New.png
- Compresses it
- Embeds as base64 into all 13 HTML files:
  1. Replaces the existing nav logo src
  2. Adds small logo icon before "Book Free Trial" button
"""

import os, re, base64
from PIL import Image
from io import BytesIO

# ── STEP 1: Load logo and remove black background ──────────────────────────
logo_path = r"C:\Users\HP\Desktop\DIGITAL - RGB\PNG\MD LOGO New.png"
img = Image.open(logo_path).convert("RGBA")

pixels = img.load()
w, h = img.size

for y in range(h):
    for x in range(w):
        r, g, b, a = pixels[x, y]
        # If pixel is dark (black background), make transparent
        if r < 40 and g < 40 and b < 40:
            pixels[x, y] = (0, 0, 0, 0)

# ── STEP 2: Crop to tight bounding box (remove transparent padding) ─────────
img = img.crop(img.getbbox())

# ── STEP 3: Resize to a sensible nav height (original is ~1358x770) ─────────
# Target height 108px (2x for retina) — width scales proportionally
target_h = 108
ratio = target_h / img.height
target_w = int(img.width * ratio)
img_resized = img.resize((target_w, target_h), Image.LANCZOS)

# ── STEP 4: Save as compressed PNG and get base64 ───────────────────────────
buf = BytesIO()
img_resized.save(buf, format="PNG", optimize=True)
buf.seek(0)
b64 = base64.b64encode(buf.read()).decode()
data_uri = f"data:image/png;base64,{b64}"
print(f"Logo base64 length: {len(b64):,} chars (~{len(b64)//1024}KB)")

# ── STEP 5: Find all HTML files ──────────────────────────────────────────────
folder = r"C:\Users\HP\Desktop\Maddog Web design pages"
html_files = [f for f in os.listdir(folder) if f.endswith(".html")]
print(f"Found {len(html_files)} HTML files")

# ── STEP 6: Patterns to find and replace ────────────────────────────────────

# Pattern A: existing nav logo <img> tag inside .site-nav-logo anchor
# Replaces whatever src is currently there with new base64
logo_img_pattern = re.compile(
    r'(<a[^>]+class="site-nav-logo"[^>]*>\s*)<img[^>]+>',
    re.DOTALL
)
logo_img_replacement = (
    r'\1<img src="' + data_uri + r'" alt="Maddog Performance Institute" '
    r'width="' + str(target_w // 2) + r'" height="54" '
    r'style="height:54px;width:auto;display:block;">'
)

# Pattern B: Book Free Trial button — add small logo icon before the <a> tag
# Matches: <div class="site-nav-cta"><a href="...">Book Free Trial</a></div>
cta_pattern = re.compile(
    r'(<div class="site-nav-cta">)(<a [^>]+>Book Free Trial</a></div>)',
    re.DOTALL
)
small_logo_img = (
    '<img src="' + data_uri + '" alt="" '
    'width="28" height="16" '
    'style="height:16px;width:auto;display:inline-block;vertical-align:middle;margin-right:6px;opacity:.9;">'
)
cta_replacement = r'\1' + small_logo_img + r'\2'

# ── STEP 7: Apply to all files ───────────────────────────────────────────────
updated = 0
skipped = []

for fname in sorted(html_files):
    fpath = os.path.join(folder, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    # Replace nav logo
    content = logo_img_pattern.sub(logo_img_replacement, content)

    # Add small logo before Book Free Trial
    content = cta_pattern.sub(cta_replacement, content)

    if content != original:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  OK: {fname}")
        updated += 1
    else:
        skipped.append(fname)
        print(f"  SKIP: {fname}")

print(f"\nDone. {updated} files updated, {len(skipped)} skipped.")
if skipped:
    print("Skipped files:", skipped)
