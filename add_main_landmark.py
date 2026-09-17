"""One-time fix: wrap page content in a <main> landmark (found missing via Lighthouse, 2026-09-17).
Gym-site pages only — wellness pages use a different template (w-footer, no site-nav-mobile)
and need separate verification before touching.

Anchor points, verified consistent across all 33 gym pages before running:
  - opening <main>: right before the first <section after id="siteNavMob"
  - closing </main>: right before <footer class="site-footer">
"""
import re

FILES = """index.html amanda.html athletes.html coaches.html training.html recovery.html events.html contact.html booking.html
training-mma-ballito.html training-bjj-ballito.html training-kids-bjj-ballito.html training-kickboxing-ballito.html training-boxing-ballito.html training-womens-boxing-ballito.html training-kids-boxing-ballito.html training-olympic-boxing-ballito.html training-bootcamp-ballito.html training-powerlifting-ballito.html training-personal-training-ballito.html
blog-mma-training-ballito.html blog-bjj-beginners-ballito.html blog-youth-mma-training-ballito.html blog-powerlifting-women-ballito.html blog-cold-plunge-sauna-ballito.html blog-amanda-kobus-coach-ballito.html blog-robin-jj-williams-physio-ballito.html blog-efc-134-amanda-lino-title-defence.html blog-efc-134-amanda-lino-vs-juliet-chukwu.html blog-womens-self-defence-workshop-ballito.html blog-womens-self-defence-workshop-recap-ballito.html blog-ballito-community-raises-funds-st-lukes.html blog-genesis-athlete-recovery-ballito.html""".split()

def patch(fname):
    with open(fname, 'r', encoding='utf-8') as f:
        text = f.read()

    navmob_idx = text.find('id="siteNavMob"')
    if navmob_idx == -1:
        return 'NO_NAVMOB'

    section_idx = text.find('<section', navmob_idx)
    if section_idx == -1:
        return 'NO_SECTION_AFTER_NAVMOB'

    footer_idx = text.find('<footer class="site-footer">')
    if footer_idx == -1:
        return 'NO_FOOTER'
    if footer_idx < section_idx:
        return 'FOOTER_BEFORE_SECTION (unexpected order)'

    if '<main' in text:
        return 'ALREADY_HAS_MAIN'

    new_text = (
        text[:section_idx]
        + '<main id="main-content">\n'
        + text[section_idx:footer_idx]
        + '</main>\n\n'
        + text[footer_idx:]
    )

    with open(fname, 'w', encoding='utf-8') as f:
        f.write(new_text)
    return 'PATCHED'

if __name__ == '__main__':
    for fname in FILES:
        print(f'{fname}: {patch(fname)}')
