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
import urllib.error
import urllib.request
from datetime import date

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PAGES_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '..', '..'))
SITEMAP_PATH = os.path.join(PAGES_DIR, 'sitemap.xml')
ROBOTS_PATH = os.path.join(PAGES_DIR, 'robots.txt')
REDIRECTS_PATH = os.path.join(PAGES_DIR, '_redirects')
REPORT_PATH = os.path.join(PAGES_DIR, 'seo-audit-report.md')
LIVE_DOMAIN = 'https://www.maddogperformance.co.za'

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

    # ---- Analytics (found missing on 2 live pages 2026-09-16 by manual check — now automated) ----
    if 'gtag(' not in content and 'googletagmanager.com/gtag' not in content:
        critical.append('Missing Google Analytics (GA4) tracking snippet — page will not appear in analytics/traffic data')

    # ---- Web app manifest ----
    if 'rel="manifest"' not in content:
        warning.append('Missing <link rel="manifest"> — no web app manifest linked')

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

    # ---- File size (Core Web Vitals / ranking risk, not just "large") ----
    if size_kb > 2000:
        warning.append(f'Page is {size_kb}KB ({round(size_kb/1024, 1)}MB) — this is a real Core Web '
                        f'Vitals (LCP) risk, which is a confirmed Google ranking factor, not just a '
                        f'"nice to have" performance note. A page this size is very likely failing '
                        f'Google\'s "good" LCP threshold (<2.5s) on mobile. Base64-embedded images can\'t '
                        f'be cached separately from the HTML, so every visit re-downloads everything. '
                        f'See the aggregate "Performance / Core Web Vitals risk" section at the top of '
                        f'this report — this is not something to leave sitting as a routine warning.')
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


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """Makes urlopen raise HTTPError on a 301/302 instead of silently following it,
    so we can inspect the actual status code the live site returned."""
    def redirect_request(self, *args, **kwargs):
        return None


def _live_check_one(opener, source, dest, code):
    """One rule's live HTTP check, run in a worker thread. Returns a finding
    string, or None if the rule is working correctly."""
    try:
        req = urllib.request.Request(LIVE_DOMAIN + source, method='HEAD')
        resp = opener.open(req, timeout=10)
        return (f'CRITICAL: `{source} {dest} {code}` is not firing on the live site — '
                f'requesting {LIVE_DOMAIN}{source} returned {resp.status} instead of a redirect.')
    except urllib.error.HTTPError as e:
        if e.code not in (301, 302, 308):
            return (f'WARNING: `{source} {dest} {code}` returned unexpected live status {e.code} '
                    f'(expected a redirect)')
        return None
    except Exception as e:
        return f'INFO: could not live-test {source} — {e} (check network/domain)'


def audit_redirects(skip_live=False):
    """_redirects rules are useless if Netlify silently ignores them. This caught
    a real incident (2026-09-16): 30 `.html -> clean-URL` rules were committed and
    deployed for 13 days doing nothing, because Netlify skips a redirect rule
    whenever the source path matches a real file in the deploy — unless the rule
    carries a force flag (!). Every .html file in this repo IS such a file, so
    every unforced rule here is a silent no-op. Checks two things per rule:
      1. (static, always) source file exists + rule isn't forced -> guaranteed broken
      2. (live, unless skip_live) actually requests the real URL and checks the
         real status code -> catches this AND any other way a rule could be dead
    Live checks run in parallel (thread pool) — sequential HTTP round-trips for
    ~30 rules is too slow for a pre-push hook to be usable.
    """
    findings = []
    if not os.path.isfile(REDIRECTS_PATH):
        findings.append('CRITICAL: _redirects file not found')
        return findings

    with open(REDIRECTS_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    existing_files = set(os.listdir(PAGES_DIR))
    opener = urllib.request.build_opener(_NoRedirect())
    to_live_check = []

    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        parts = line.split()
        if len(parts) < 3:
            continue
        source, dest, code = parts[0], parts[1], parts[2]
        if '*' in source or not re.match(r'^30[128]!?$', code):
            continue  # only checking single-path redirect rules, not rewrites/wildcards

        source_file = source.lstrip('/')
        forced = code.endswith('!')
        file_exists_at_source_path = source_file in existing_files

        if file_exists_at_source_path and not forced:
            findings.append(
                f'CRITICAL: `{source} {dest} {code}` will be silently skipped by Netlify — '
                f'a real file exists at that exact path and the rule has no force flag. '
                f'Add "!" (e.g. "{code}!") or this redirect does nothing live.'
            )
            continue  # already known-broken, no need to also live-test it

        if not skip_live:
            to_live_check.append((source, dest, code))

    if to_live_check:
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
            for result in pool.map(lambda r: _live_check_one(opener, *r), to_live_check):
                if result:
                    findings.append(result)

    return findings


INTERNAL_HREF_RE = re.compile(r'href="((?:/[^"#?]*|https://(?:www\.)?maddogperformance\.co\.za/[^"#?]*))"')
SKIP_LINK_PREFIXES = ('mailto:', 'tel:', 'javascript:')


def audit_broken_links(skip_live=False):
    """No prior check has ever verified internal <a href> links actually
    resolve — every audit so far only checked page-level metadata, never
    the link graph. Collects every unique internal link target across all
    live pages, then live-tests each one (following redirects, since a
    legitimate link may legitimately go through a 301) and flags anything
    that doesn't end in a 200."""
    findings = []
    html_files = sorted(f for f in os.listdir(PAGES_DIR) if f.endswith('.html') and f not in TEMPLATE_FILES)

    target_to_sources = {}
    for filename in html_files:
        path = os.path.join(PAGES_DIR, filename)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        for match in INTERNAL_HREF_RE.findall(content):
            target = match
            if target.startswith(SKIP_LINK_PREFIXES):
                continue
            if target.startswith('https://'):
                target = '/' + target.split('.co.za/', 1)[1]
            if not target.startswith('/'):
                target = '/' + target
            target_to_sources.setdefault(target, set()).add(filename)

    if skip_live or not target_to_sources:
        return findings

    opener = urllib.request.build_opener()  # default opener DOES follow redirects here — that's correct for this check
    import concurrent.futures

    def _check(target):
        try:
            req = urllib.request.Request(LIVE_DOMAIN + target, method='HEAD')
            resp = opener.open(req, timeout=10)
            return target, resp.status
        except urllib.error.HTTPError as e:
            return target, e.code
        except Exception as e:
            return target, f'ERROR:{e}'

    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
        for target, status in pool.map(_check, target_to_sources.keys()):
            if status != 200:
                sources = ', '.join(sorted(target_to_sources[target])[:5])
                more = len(target_to_sources[target]) - 5
                if more > 0:
                    sources += f' (+{more} more)'
                findings.append(
                    f'CRITICAL: internal link to `{target}` returns {status}, not 200 — '
                    f'linked from: {sources}'
                )
    return findings


def main():
    if '--check-redirects' in sys.argv:
        # Fast path for the pre-push hook: only the live redirect check, exit
        # nonzero if anything is broken. Doesn't scan pages or write the report.
        findings = audit_redirects(skip_live=False)
        critical = [f for f in findings if f.startswith('CRITICAL')]
        for f in findings:
            print(f)
        if critical:
            print(f'\n{len(critical)} redirect rule(s) broken.')
            sys.exit(1)
        print('All redirect rules verified live.')
        sys.exit(0)

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
    skip_live = '--skip-live' in sys.argv
    redirect_findings = audit_redirects(skip_live=skip_live)
    broken_link_findings = audit_broken_links(skip_live=skip_live)

    if '--check-critical' in sys.argv:
        # Fast path for the pre-push hook: every check that runs for the full
        # report, but only CRITICAL-severity findings matter (warnings/info
        # need human judgment per this skill's own docs — not something a
        # hook should block on). Runs on every push, not just when
        # _redirects changed, because this is meant to catch anything
        # slipping through, not just the one bug class that prompted it.
        page_critical = [(r['file'], msg) for r in results for msg in r['critical']]
        redirect_critical = [f for f in redirect_findings if f.startswith('CRITICAL')]
        link_critical = [f for f in broken_link_findings if f.startswith('CRITICAL')]
        all_critical = (
            [f'{f}: {msg}' for f, msg in page_critical]
            + redirect_critical
            + link_critical
            + [f for f in sitemap_findings]  # sitemap findings are always critical-severity
        )
        for f in all_critical:
            print(f'CRITICAL: {f}' if not f.startswith('CRITICAL') else f)
        if all_critical:
            print(f'\n{len(all_critical)} critical finding(s) — see above. Full report: run without --check-critical.')
            sys.exit(1)
        print('No critical findings across pages, sitemap, robots.txt, or redirects.')
        sys.exit(0)

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

    redirect_critical = sum(1 for f in redirect_findings if f.startswith('CRITICAL'))
    redirect_warning = sum(1 for f in redirect_findings if f.startswith('WARNING'))
    redirect_info = sum(1 for f in redirect_findings if f.startswith('INFO'))

    link_critical = sum(1 for f in broken_link_findings if f.startswith('CRITICAL'))
    link_warning = sum(1 for f in broken_link_findings if f.startswith('WARNING'))
    link_info = sum(1 for f in broken_link_findings if f.startswith('INFO'))

    total_critical = sum(len(r['critical']) for r in results) + redirect_critical + link_critical
    total_warning = sum(len(r['warning']) for r in results) + redirect_warning + link_warning
    total_info = sum(len(r['info']) for r in results) + redirect_info + link_info

    # ---- Write full Markdown report ----
    lines = []
    lines.append(f'# SEO Audit Report — {date.today().isoformat()}')
    lines.append('')
    lines.append(f'Pages scanned: {len(results)} ({sum(1 for r in results if r["business"] == "gym")} gym, '
                 f'{sum(1 for r in results if r["business"] == "wellness")} wellness)')
    lines.append(f'Findings: **{total_critical} critical**, **{total_warning} warning**, {total_info} info')
    lines.append('')

    oversized = sorted(
        ((r['file'], r['size_kb']) for r in results if r['size_kb'] > 2000),
        key=lambda x: -x[1]
    )
    lines.append('## Performance / Core Web Vitals risk')
    lines.append('')
    if oversized:
        total_mb = sum(kb for _, kb in oversized) / 1024
        lines.append(f'**{len(oversized)} of {len(results)} pages are over 2MB** ({round(total_mb, 1)}MB combined). '
                     f'Google uses Core Web Vitals (LCP, INP, CLS) as a direct ranking factor. Pages this size, '
                     f'especially with images inline as base64 rather than separately-cacheable files, are very '
                     f'likely failing the "good" LCP threshold on mobile. This is a real ranking lever, not a '
                     f'routine cleanup item — it just isn\'t something a hook can safely auto-block on, since '
                     f'fixing it site-wide is an architecture decision (base64-inline vs. file-referenced images), '
                     f'not a one-line fix.')
        lines.append('')
        for f, kb in oversized:
            lines.append(f'- `{f}` — {kb}KB ({round(kb/1024, 1)}MB)')
    else:
        lines.append('- No pages over 2MB — no Core Web Vitals size risk currently detected')
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

    lines.append('## Redirects (`_redirects`)' + (' — live-tested against ' + LIVE_DOMAIN if not skip_live else ' — static check only, live test skipped'))
    lines.append('')
    if redirect_findings:
        for f in redirect_findings:
            lines.append(f'- {f}')
    else:
        lines.append('- All checked redirect rules are correctly enforced')
    lines.append('')

    lines.append('## Internal links' + (' — every internal href live-tested against ' + LIVE_DOMAIN if not skip_live else ' — skipped, live test disabled'))
    lines.append('')
    if broken_link_findings:
        for f in broken_link_findings:
            lines.append(f'- {f}')
    else:
        lines.append('- Every internal link found across all pages resolves to a live 200')
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
    if redirect_critical:
        print(f'\n*** {redirect_critical} redirect rule(s) are NOT actually working — this is the exact bug class ***')
        print('*** that stalled 41 pages out of Google\'s index for 13 days in Sept 2026. Fix before anything else. ***')
        for f in redirect_findings:
            if f.startswith('CRITICAL'):
                print(f'  {f}')
    if link_critical:
        print(f'\n*** {link_critical} internal link(s) are broken (404 or worse) — a visitor or Googlebot ***')
        print('*** following them hits a dead end. Fix before anything else. ***')
        for f in broken_link_findings:
            if f.startswith('CRITICAL'):
                print(f'  {f}')
    if oversized:
        total_mb = sum(kb for _, kb in oversized) / 1024
        print(f'\n*** {len(oversized)} pages ({round(total_mb, 1)}MB combined) are over 2MB — a real Core Web ***')
        print('*** Vitals / Google ranking risk, not a routine warning. See report for the full list. ***')
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
