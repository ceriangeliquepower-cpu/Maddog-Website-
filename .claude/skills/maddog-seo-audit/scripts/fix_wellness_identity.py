"""
Fix the two unambiguous "wrong business identity" bugs on wellness pages:
og:site_name meta tag and the footer copyright line both sometimes say
"Maddog Performance Institute" (the gym) instead of the wellness business.

Deliberately narrow — only touches these two exact, unambiguous patterns.
Does NOT touch body copy, FAQ text, cred-strip items, or image alt text,
because some of those are legitimate cross-business mentions (e.g. "R650
for Maddog Performance Institute athletes" is describing a real gym-member
discount, not a bug) and need a human/Claude judgment call per occurrence,
not a blanket find-replace.

Usage:
    py scripts/fix_wellness_identity.py FILE1.html FILE2.html ...
    py scripts/fix_wellness_identity.py FILE.html --dry-run
"""
import argparse
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PAGES_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '..', '..'))

OLD_OG = '<meta property="og:site_name" content="Maddog Performance Institute">'
NEW_OG = '<meta property="og:site_name" content="Maddog Performance Health & Wellness">'

OLD_FOOTER_VARIANTS = [
    '<p>&copy; 2026 Maddog Performance Institute &middot; All Rights Reserved</p>',
    '<p>© 2026 Maddog Performance Institute · All Rights Reserved</p>',
]
NEW_FOOTER = '<p>&copy; 2026 Maddog Performance Health &amp; Wellness &middot; All Rights Reserved</p>'


def main():
    parser = argparse.ArgumentParser(description='Fix og:site_name and footer copyright on wellness pages.')
    parser.add_argument('files', nargs='+', help='Target .html filenames (relative to project root)')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    for filename in args.files:
        path = os.path.join(PAGES_DIR, filename) if not os.path.isabs(filename) else filename
        if not os.path.isfile(path):
            print(f'SKIP (not found): {filename}', file=sys.stderr)
            continue

        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        changes = []
        if OLD_OG in content:
            content = content.replace(OLD_OG, NEW_OG)
            changes.append('og:site_name')

        for variant in OLD_FOOTER_VARIANTS:
            if variant in content:
                content = content.replace(variant, NEW_FOOTER)
                changes.append('footer copyright')
                break

        if not changes:
            print(f'NO MATCH (already fixed or different pattern — check manually): {filename}')
            continue

        print(f'{"[dry-run] " if args.dry_run else ""}{filename}: fixed {", ".join(changes)}')

        if args.dry_run:
            continue

        with open(path, 'r', encoding='utf-8') as f:
            original = f.read()
        backup_path = path + '.bak'
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)


if __name__ == '__main__':
    main()
