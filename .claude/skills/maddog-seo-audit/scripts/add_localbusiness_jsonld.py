"""
Insert a LocalBusiness-family JSON-LD block into pages that are missing one
(SEO audit finding: "No LocalBusiness-family JSON-LD found").

Anchors on the closing </script> tag of the page's BreadcrumbList JSON-LD
block (every affected page has one — only the business-identity block was
missing) and inserts the new block immediately after it, before the
<link rel="preconnect"...> that follows. Skips any file that already has a
SportsActivityLocation/MedicalBusiness/LocalBusiness block, so it's safe to
re-run. Writes a .bak backup of each file before writing.

Usage:
    py scripts/add_localbusiness_jsonld.py --jsonld-file path/to/block.json FILE1.html FILE2.html ...
    py scripts/add_localbusiness_jsonld.py --jsonld-file ... FILE.html --dry-run
"""
import argparse
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PAGES_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '..', '..'))


def main():
    parser = argparse.ArgumentParser(description='Insert LocalBusiness-family JSON-LD into pages missing it.')
    parser.add_argument('--jsonld-file', required=True, help='Path to the JSON-LD block to insert (raw JSON, no <script> wrapper)')
    parser.add_argument('files', nargs='+', help='Target .html filenames (relative to project root)')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    with open(args.jsonld_file, 'r', encoding='utf-8') as f:
        jsonld_body = f.read().strip()

    script_block = f'<script type="application/ld+json">\n{jsonld_body}\n</script>\n'

    for filename in args.files:
        path = os.path.join(PAGES_DIR, filename) if not os.path.isabs(filename) else filename
        if not os.path.isfile(path):
            print(f'SKIP (not found): {filename}', file=sys.stderr)
            continue

        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        if re.search(r'"@type":\s*"(SportsActivityLocation|MedicalBusiness|LocalBusiness)"', content):
            print(f'SKIP (already has LocalBusiness-family JSON-LD): {filename}')
            continue

        m = re.search(r'"@type":\s*"BreadcrumbList".*?</script>\s*', content, re.DOTALL)
        if not m:
            print(f'SKIP (no BreadcrumbList anchor found — insert manually): {filename}', file=sys.stderr)
            continue

        insert_at = m.end()
        new_content = content[:insert_at] + script_block + content[insert_at:]

        print(f'{"[dry-run] " if args.dry_run else ""}INSERTED into {filename} ({len(script_block)} bytes)')

        if args.dry_run:
            continue

        backup_path = path + '.bak'
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)


if __name__ == '__main__':
    main()
