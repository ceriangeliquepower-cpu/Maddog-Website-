"""
Site-wide SEO audit for the Maddog Performance Institute (gym) and Maddog
Performance Health & Wellness (wellness) sites — two businesses, one repo.

Scans every top-level .html page (skipping *-TEMPLATE.html files, which
aren't live pages) against the rules in CLAUDE.md, plus a few checks that
came out of issues actually found this session (brand-name cross-
contamination between the two businesses, LocalBusiness schema gaps).

Some of these pages are multi-MB base64-heavy files (events.html, index.html,
wellness.html, wellness-blog.html) — this script reads them as plain text via
normal Python file I/O (fine, no LLM context involved) but NEVER prints
matched content that could contain base64 (image src values, etc.) — only
short fields (titles, counts, booleans) reach stdout/the report.

Writes a full Markdown report to seo-audit-report.md in the project root
and prints a short summary to stdout. Run with no arguments.

Usage:
    py .claude/skills/maddog-seo-audit/scripts/audit_pages.py
"""
import os
import re
import sys
from datetime import date

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PAGES_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '..', '..'))
SITEMAP_PATH = os.path.join(PAGES_DIR, 'sitemap.xml')
ROBOTS_PATH = os.path.join(PAGES_DIR, 'robots.txt')
REPORT_PATH = os.path.join(PAGES_DIR, 'seo-audit-report.md')

TEMPLATE_FILES = {'blog-TEMPLATE.html', 'wellness-blog-TEMPLATE.html'}
GYM_NAME = 'Maddog Performance Institute'
WELLNESS_NAME = 'Maddog Performance Health & Wellness'
BAD_BRAND_PATTERNS = [r'\bMad\s+Dog\b', r'\bMadDog\b', r'\bMADDOG\b']


def classify(filename):
    return 'wellness' if filename.startswith('wellness') else 'gym'


def is_blog_page(filename, business):
    if business == 'gym':
        return filename.startswith('blog-')
    return filename.startswith('wellness-blog-') and filename != 'wellness-blog.html'


def find(pattern, content, flags=0):
    m = re.search(pattern, content, flags)
    return m.group(1).strip() if m else None


def count(pattern, content, flags=0):
    return len(re.findall(pattern, content, flags))


def audit_one_page(path, business):
    filename = os.path.basename(path)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    size_kb = round(os.path.getsize(path) / 1024, 1)
    critical, warning, info = [], [], []

    # ---- Title ----
    title = find(r'<title>(.*?)</title>', content, re.DOTALL)
    if not title:
        critical.append('Missing <title>')
    elif len(title) > 65:
        warning.append(f'<title> is {len(title)} chars (target ~60) — "{title[:70]}..."')

    # ---- Meta description ----
    meta_desc = find(r'<meta name="description" content="(.*?)">', content, re.DOTALL)
    if not meta_desc:
        critical.append('Missing <meta name="description">')
    elif not (140 <= len(meta_desc) <= 165):
        warning.append(f'Meta description is {len(meta_desc)} chars (target 150-160)')

    # ---- Canonical ----
    canonical = find(r'<link rel="canonical" href="([^"]*)">', content)
    if not canonical:
        critical.append('Missing <link rel="canonical">')
    elif canonical.endswith('.html'):
        warning.append(f'Canonical URL still has .html extension: {canonical}')

    # ---- OG / Twitter ----
    for tag in ['og:type', 'og:title', 'og:description', 'og:url', 'og:site_name']:
        if f'property="{tag}"' not in content:
            warning.append(f'Missing meta property="{tag}"')
    if 'name="twitter:card"' not in content:
        warning.append('Missing twitter:card meta tag')

    # ---- Robots / geo ----
    if 'name="robots" content="index, follow"' not in content:
        warning.append('Missing or non-standard robots meta tag')
    if 'name="geo.region"' not in content:
        info.append('Missing geo.region meta tag')

    # ---- LocalBusiness-family JSON-LD ----
    has_local_business = bool(re.search(
        r'"@type":\s*"(SportsActivityLocation|MedicalBusiness|ExerciseGym|LocalBusiness)"', content))
    if not has_local_business:
        critical.append('No LocalBusiness-family JSON-LD (SportsActivityLocation/MedicalBusiness/ExerciseGym) found')

    # ---- Blog-specific schema ----
    if is_blog_page(filename, business):
        if '"@type": "Article"' not in content and '"@type":"Article"' not in content:
            critical.append('Blog page missing Article JSON-LD')
        if 'BreadcrumbList' not in content:
            critical.append('Blog page missing BreadcrumbList JSON-LD')

    # ---- Brand name cross-contamination ----
    for pat in BAD_BRAND_PATTERNS:
        matches = list(re.finditer(pat, content))
        # A match immediately bounded by > and < with nothing else (e.g. "...>MADDOG</span>...")
        # is almost always a stylized nav/footer logotype, not body copy — CLAUDE.md's rule
        # is specifically about body copy. Flag those separately at lower severity.
        logotype_only = all(
            content[max(0, m.start() - 1):m.start()] == '>' and
            content[m.end():m.end() + 1] == '<'
            for m in matches
        ) if matches else False
        if matches and logotype_only:
            info.append(f'Brand spelling matching /{pat}/ found, but only inside what looks like a '
                        f'standalone logo/wordmark span (e.g. ">MADDOG<") — verify it is not body copy')
        elif matches:
            critical.append(f'Forbidden brand spelling found matching /{pat}/ (must be "Maddog")')
    if business == 'wellness' and GYM_NAME in content:
        # The gym is legitimately referenced from wellness pages in a few ways that are
        # NOT bugs: footer cross-links, and nested JSON-LD objects like an Event's
        # "location" for a genuinely joint event held at the gym's premises. Only flag
        # it when the gym's name is the value of a top-level business-identity field:
        # og:site_name, or a JSON-LD object whose OWN @type is the LocalBusiness family
        # (i.e. this page's own SportsActivityLocation/MedicalBusiness/ExerciseGym block
        # claiming to BE the gym), not any "name" field nested somewhere else in the graph.
        is_own_identity = f'content="{GYM_NAME}"' in content or re.search(
            r'"@type":\s*"(SportsActivityLocation|MedicalBusiness|ExerciseGym|LocalBusiness)"\s*,\s*"name":\s*"'
            + re.escape(GYM_NAME) + '"', content)
        if is_own_identity:
            critical.append(f'Wellness page identifies itself as "{GYM_NAME}" (wrong business) somewhere in schema/meta')
        else:
            info.append(f'"{GYM_NAME}" appears on this page — checked, looks like a legitimate cross-business '
                        f'reference (event location, footer link, etc.), not a self-identity bug — verify if unsure')
    if business == 'gym' and WELLNESS_NAME in content:
        info.append(f'Gym page references "{WELLNESS_NAME}" — confirm this is an intentional cross-link, not a copy-paste')

    # ---- Headings ----
    h1_count = count(r'<h1[\s>]', content)
    if h1_count == 0:
        critical.append('No <h1> found')
    elif h1_count > 1:
        warning.append(f'{h1_count} <h1> tags found — should be exactly 1')

    # ---- Images: alt text coverage (approximate — counts only, never prints image data) ----
    img_tags = re.findall(r'<img\b[^>]*>', content, re.DOTALL)
    empty_alt = sum(1 for tag in img_tags if re.search(r'alt=""', tag))
    missing_alt = sum(1 for tag in img_tags if 'alt=' not in tag)
    if empty_alt or missing_alt:
        warning.append(f'{empty_alt + missing_alt} of {len(img_tags)} <img> tags have empty/missing alt text '
                        f'(some empty alt may be intentionally decorative — verify)')

    # ---- File size (performance/SEO signal) ----
    if size_kb > 2000:
        warning.append(f'Page is {size_kb}KB — likely base64-embedded images bloating load time; '
                        f'consider migrating to images/ file-based references')
    elif size_kb > 800:
        info.append(f'Page is {size_kb}KB — on the larger side, worth checking for embedded base64 images')

    return {
        'file': filename,
        'business': business,
        'size_kb': size_kb,
        'title': title,
        'critical': critical,
        'warning': warning,
        'info': info,
    }


def audit_sitemap():
    findings = []
    if not os.path.isfile(SITEMAP_PATH):
        return ['sitemap.xml not found'], set()
    with open(SITEMAP_PATH, 'r', encoding='utf-8') as f:
        sitemap_content = f.read()
    sitemap_slugs = set(re.findall(
        r'<loc>https://www\.maddogperformance\.co\.za/([^<]*)</loc>', sitemap_content))
    sitemap_slugs = {s.rstrip('/') for s in sitemap_slugs}
    sitemap_slugs.discard('')  # homepage root
    return findings, sitemap_slugs


def audit_robots():
    findings = []
    if not os.path.isfile(ROBOTS_PATH):
        findings.append('robots.txt not found')
        return findings
    with open(ROBOTS_PATH, 'r', encoding='utf-8') as f:
        robots_content = f.read()
    if 'Disallow: /' in robots_content and 'Disallow: /\n' in robots_content.replace('\r\n', '\n'):
        findings.append('robots.txt appears to block the whole site')
    if 'sitemap' not in robots_content.lower():
        findings.append('robots.txt does not reference the sitemap')
    return findings


def main():
    html_files = sorted(
        f for f in os.listdir(PAGES_DIR)
        if f.endswith('.html') and f not in TEMPLATE_FILES
    )

    results = []
    for filename in html_files:
        business = classify(filename)
        path = os.path.join(PAGES_DIR, filename)
        results.append(audit_one_page(path, business))

    sitemap_findings, sitemap_slugs = audit_sitemap()
    robots_findings = audit_robots()

    missing_from_sitemap = []
    for r in results:
        slug = r['file'][:-5]  # strip .html
        # Training discipline pages are served at pretty /training/... URLs via a
        # _redirects rewrite (training-mma-ballito.html -> /training/mma-ballito) —
        # the sitemap correctly lists the pretty form, not the flat filename.
        if slug.startswith('training-') and slug != 'training':
            slug = 'training/' + slug[len('training-'):]
        if slug not in sitemap_slugs and slug != 'index':
            missing_from_sitemap.append(r['file'])

    total_critical = sum(len(r['critical']) for r in results)
    total_warning = sum(len(r['warning']) for r in results)
    total_info = sum(len(r['info']) for r in results)

    # ---- Write full Markdown report ----
    lines = []
    lines.append(f'# SEO Audit Report — {date.today().isoformat()}')
    lines.append('')
    lines.append(f'Pages scanned: {len(results)} ({sum(1 for r in results if r["business"] == "gym")} gym, '
                 f'{sum(1 for r in results if r["business"] == "wellness")} wellness)')
    lines.append(f'Findings: **{total_critical} critical**, **{total_warning} warning**, {total_info} info')
    lines.append('')

    lines.append('## Site-wide')
    lines.append('')
    if missing_from_sitemap:
        lines.append(f'- **CRITICAL**: {len(missing_from_sitemap)} page(s) missing from sitemap.xml: '
                     + ', '.join(missing_from_sitemap))
    else:
        lines.append('- All pages present in sitemap.xml')
    for f in sitemap_findings:
        lines.append(f'- **CRITICAL**: {f}')
    for f in robots_findings:
        lines.append(f'- **WARNING**: {f}')
    lines.append('')

    lines.append('## Per-page findings')
    lines.append('')
    for r in results:
        if not (r['critical'] or r['warning'] or r['info']):
            continue
        lines.append(f'### {r["file"]} ({r["business"]}, {r["size_kb"]}KB)')
        if r['title']:
            lines.append(f'*Title: {r["title"]}*')
        lines.append('')
        for msg in r['critical']:
            lines.append(f'- **CRITICAL**: {msg}')
        for msg in r['warning']:
            lines.append(f'- **WARNING**: {msg}')
        for msg in r['info']:
            lines.append(f'- INFO: {msg}')
        lines.append('')

    clean_pages = [r['file'] for r in results if not (r['critical'] or r['warning'] or r['info'])]
    if clean_pages:
        lines.append('## Clean pages (no findings)')
        lines.append('')
        lines.append(', '.join(clean_pages))
        lines.append('')

    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    # ---- Short stdout summary ----
    print(f'Scanned {len(results)} pages. Critical: {total_critical}  Warning: {total_warning}  Info: {total_info}')
    print(f'Full report: {REPORT_PATH}')
    if missing_from_sitemap:
        print(f'Missing from sitemap: {", ".join(missing_from_sitemap)}')
    print()
    print('Top critical findings:')
    shown = 0
    for r in results:
        for msg in r['critical']:
            if shown >= 15:
                break
            print(f'  {r["file"]}: {msg}')
            shown += 1
        if shown >= 15:
            break
    if total_critical > shown:
        print(f'  ...and {total_critical - shown} more critical findings — see {REPORT_PATH}')


if __name__ == '__main__':
    main()
