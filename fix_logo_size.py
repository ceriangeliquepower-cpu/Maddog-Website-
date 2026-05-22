"""
fix_logo_size.py — straightforward string replacements
Nav logo: CSS rule .site-nav-logo img height 54px -> 44px
CTA icon: inline style height:16px -> 44px, height="16" -> height="44"
"""
import os

folder = r"C:\Users\HP\Desktop\Maddog Web design pages"
html_files = [f for f in os.listdir(folder) if f.endswith(".html")]

replacements = [
    # CSS rule controlling nav logo height
    ("height:54px!important;width:auto!important;display:block!important",
     "height:44px!important;width:auto!important;display:block!important"),
    # Inline style on CTA small icon
    ('style="height:16px;width:auto;display:inline-block;vertical-align:middle;margin-right:6px;opacity:.9;"',
     'style="height:44px;width:auto;display:inline-block;vertical-align:middle;margin-right:6px;opacity:.9;"'),
    # height attribute on CTA icon
    ('width="28" height="16"',
     'width="28" height="44"'),
]

updated = 0
for fname in sorted(html_files):
    fpath = os.path.join(folder, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    original = content
    for old, new in replacements:
        content = content.replace(old, new)
    if content != original:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"OK: {fname}")
        updated += 1
    else:
        print(f"SKIP: {fname}")

print(f"\nDone. {updated} files updated.")
