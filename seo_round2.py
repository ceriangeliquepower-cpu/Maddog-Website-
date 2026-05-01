import os, re

BASE = r'C:\Users\HP\Desktop\Maddog Web design pages\.claude\worktrees\priceless-bardeen-61b48b'
BASE_URL = 'https://www.maddogperformance.co.za'

BLOG_DATA = [
    {
        'file': 'blog-cold-plunge-sauna-ballito.html',
        'breadcrumb_name': 'Cold Plunge & Sauna Recovery Ballito',
        'date_modified': '2026-04-01',
        'needs_date_modified': True,
    },
    {
        'file': 'blog-bjj-beginners-ballito.html',
        'breadcrumb_name': 'BJJ Classes for Beginners in Ballito',
        'date_modified': '2026-04-01',
        'needs_date_modified': True,
    },
    {
        'file': 'blog-powerlifting-women-ballito.html',
        'breadcrumb_name': 'Powerlifting for Women in Ballito KZN',
        'date_modified': '2026-04-01',
        'needs_date_modified': True,
    },
    {
        'file': 'blog-iv-drip-therapy-ballito.html',
        'breadcrumb_name': 'IV Drip Therapy Ballito KZN',
        'date_modified': '2026-04-01',
        'needs_date_modified': True,
    },
    {
        'file': 'blog-mma-training-ballito.html',
        'breadcrumb_name': 'How to Start MMA Training in Ballito',
        'date_modified': '2026-04-01',
        'needs_date_modified': True,
    },
    {
        'file': 'blog-efc-134-amanda-lino-vs-juliet-chukwu.html',
        'breadcrumb_name': 'EFC 134: Amanda Lino Defends World Title',
        'date_modified': '2026-05-01',
        'needs_date_modified': False,  # already has it
    },
    {
        'file': 'blog-ballito-community-raises-funds-st-lukes.html',
        'breadcrumb_name': "When Ballito Showed Up: R53,000 for St Luke's",
        'date_modified': '2026-03-25',
        'needs_date_modified': False,  # already has it
    },
]

for blog in BLOG_DATA:
    path = os.path.join(BASE, blog['file'])
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Add dateModified to Article JSON-LD if needed
    if blog['needs_date_modified']:
        # Insert after datePublished line
        html = html.replace(
            '"datePublished": "' + blog['date_modified'] + '",\n  "url"',
            '"datePublished": "' + blog['date_modified'] + '",\n  "dateModified": "' + blog['date_modified'] + '",\n  "url"'
        )

    # 2. Build BreadcrumbList JSON-LD block
    page_url = BASE_URL + '/' + blog['file']
    breadcrumb_script = '''\n<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type":"ListItem","position":1,"name":"Home","item":"https://www.maddogperformance.co.za/"},
    {"@type":"ListItem","position":2,"name":"News & Events","item":"https://www.maddogperformance.co.za/events.html"},
    {"@type":"ListItem","position":3,"name":"''' + blog['breadcrumb_name'] + '''","item":"''' + page_url + '''"}
  ]
}
</script>'''

    # 3. Insert breadcrumb AFTER the first closing </script> tag in <head>
    # (the Article JSON-LD block)
    # Find the first </script> occurrence
    first_close = html.find('</script>')
    if first_close != -1:
        # Check we haven't already added it
        if 'BreadcrumbList' not in html:
            html = html[:first_close + len('</script>')] + breadcrumb_script + html[first_close + len('</script>'):]

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Updated: {blog["file"]}')

print('\nAll blog pages updated.')
