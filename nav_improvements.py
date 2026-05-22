"""
nav_improvements.py
Applies 5 nav bar improvements across all HTML files:
1. Increase nav height 60px -> 72px (more breathing room)
2. Gold vertical divider between logo and nav links
3. Gold underline on active/hovered nav link (box-shadow, no layout shift)
4. Shrink CTA logo icon 44px -> 20px (proportional to button text)
5. border-radius:2px on CTA button (subtle polish)
"""
import os

folder = r"C:\Users\HP\Desktop\Maddog Web design pages"
html_files = [f for f in os.listdir(folder) if f.endswith(".html")]

# Applied in order — later steps can rely on earlier changes
replacements = [

    # ── 1. NAV HEIGHT: .site-nav ───────────────────────────────────────────
    (';height:60px !important}',
     ';height:72px !important}'),

    # ── 1b. NAV HEIGHT: .site-nav-inner ────────────────────────────────────
    ('padding:0 48px !important;height:60px !important;',
     'padding:0 48px !important;height:72px !important;'),

    # ── 1c. NAV LINKS line-height must match nav height ────────────────────
    ('line-height:60px !important',
     'line-height:72px !important'),

    # ── 1d. MOBILE MENU top position must match nav height ─────────────────
    ('top:60px !important',
     'top:72px !important'),

    # ── 3. ACTIVE LINK UNDERLINE: gold inset box-shadow (no layout shift) ──
    ('.site-nav-links a:hover,.site-nav-links a.sn-active{color:#C9A84C !important}',
     '.site-nav-links a:hover,.site-nav-links a.sn-active{color:#C9A84C !important;box-shadow:inset 0 -2px 0 #C9A84C !important}'),

    # ── 5. CTA BUTTON border-radius ────────────────────────────────────────
    ('text-decoration:none !important;white-space:nowrap !important;line-height:1.4 !important}',
     'text-decoration:none !important;white-space:nowrap !important;line-height:1.4 !important;border-radius:2px !important}'),

    # ── 4. CTA ICON SIZE: 44px -> 20px (inline style) ──────────────────────
    ('style="height:44px;width:auto;display:inline-block;vertical-align:middle;margin-right:6px;opacity:.9;"',
     'style="height:20px;width:auto;display:inline-block;vertical-align:middle;margin-right:8px;opacity:.85;"'),

    # ── 4b. CTA ICON height attribute ──────────────────────────────────────
    ('width="28" height="44"',
     'width="28" height="20"'),

    # ── 2. GOLD DIVIDER: insert before nav links div ────────────────────────
    # This <div class="site-nav-links"> only appears once per file in HTML
    ('<div class="site-nav-links">',
     '<div style="width:1px;height:28px;background:rgba(201,168,76,.35);'
     'flex-shrink:0;margin:0 16px 0 8px;"></div>\n  <div class="site-nav-links">'),
]

updated = 0
skipped = []

for fname in sorted(html_files):
    fpath = os.path.join(folder, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content
    for old, new in replacements:
        content = content.replace(old, new)
    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"OK: {fname}")
        updated += 1
    else:
        skipped.append(fname)
        print(f"SKIP: {fname}")

print(f"\nDone. {updated} updated, {len(skipped)} skipped.")
if skipped:
    print("Skipped:", skipped)
