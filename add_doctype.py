"""One-time fix: prepend <!DOCTYPE html> to every page missing it (found via Lighthouse, 2026-09-17 — was triggering quirks mode on all 53 pages)."""
import glob

files = [f for f in glob.glob('*.html') if 'TEMPLATE' not in f]
patched = 0
skipped = 0
for fname in files:
    with open(fname, 'r', encoding='utf-8') as f:
        text = f.read()
    if text.lstrip().lower().startswith('<!doctype'):
        skipped += 1
        continue
    with open(fname, 'w', encoding='utf-8') as f:
        f.write('<!DOCTYPE html>\n' + text)
    patched += 1

print(f'Patched: {patched}, already had doctype: {skipped}, total: {len(files)}')
