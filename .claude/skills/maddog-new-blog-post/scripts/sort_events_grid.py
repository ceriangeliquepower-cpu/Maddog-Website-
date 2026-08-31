"""
One-time (and re-runnable) date sort for the .blog-card grid on events.html.

Parses each card's bc-date field (either "Month Year · N min read" or
"DD Month Year" — both formats exist in the wild on this grid) and
reorders the cards newest-first. Cards with only a month/year (no day)
sort as if on the 1st of that month; ties are broken by keeping each
card's existing relative order (stable sort), since there's no finer
date information to go on.

Never touches the .event-card entries further down the file (a separate
section for upcoming live events) — only the blog-card grid.

Usage:
    py scripts/sort_events_grid.py [--dry-run] [--events-file PATH]
"""
import argparse
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PAGES_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '..', '..'))
DEFAULT_EVENTS_PATH = os.path.join(PAGES_DIR, 'events.html')

MONTHS = {m: i + 1 for i, m in enumerate([
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
])}


def parse_date(bc_date_text):
    # "25 March 2026" (day month year)
    m = re.match(r'(\d{1,2})\s+(\w+)\s+(\d{4})', bc_date_text)
    if m and m.group(2) in MONTHS:
        return (int(m.group(3)), MONTHS[m.group(2)], int(m.group(1)))
    # "August 2026 · 7 min read" (month year only)
    m = re.match(r'(\w+)\s+(\d{4})', bc_date_text)
    if m and m.group(1) in MONTHS:
        return (int(m.group(2)), MONTHS[m.group(1)], 1)
    raise ValueError(f'Could not parse date from bc-date text: {bc_date_text!r}')


def main():
    parser = argparse.ArgumentParser(description='Sort the events.html blog-card grid by date, newest first.')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--events-file', default=DEFAULT_EVENTS_PATH)
    args = parser.parse_args()

    EVENTS_PATH = args.events_file
    if not os.path.isfile(EVENTS_PATH):
        print(f'ERROR: events.html not found at {EVENTS_PATH}', file=sys.stderr)
        sys.exit(1)

    with open(EVENTS_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    card_open_re = re.compile(r'<div class="blog-card" id="([^"]+)">')
    card_opens = list(card_open_re.finditer(content))
    if not card_opens:
        raise ValueError('No .blog-card entries found. Stopping without writing anything.')

    cards = []
    for i, m in enumerate(card_opens):
        card_id = m.group(1)
        block_start = m.start()
        # Preceding HTML comment (e.g. "<!-- POST 3 -->"), if present, travels with the card.
        comment_m = re.search(r'<!--[^>]*-->\s*$', content[:block_start])
        if comment_m and (block_start - comment_m.end()) < 20:
            block_start = comment_m.start()

        date_m = re.compile(r'<div class="bc-date">(.*?)</div>').search(content, m.end())
        if not date_m:
            raise ValueError(f'No bc-date found for card {card_id}. Stopping without writing anything.')
        sort_key = parse_date(date_m.group(1))

        # Card ends at the next card's start (or the grid's closing boundary for the last one).
        next_start = card_opens[i + 1].start() if i + 1 < len(card_opens) else None
        cards.append({'id': card_id, 'sort_key': sort_key, 'start': block_start, '_open_end': m.end(), '_next_start': next_start})

    # Resolve each card's raw text block using the next card's (or boundary's) start.
    boundary_re = re.compile(r'</div>\s*</div>\s*</div>\s*</section>\s*<section class="events-sec" id="events">')
    boundary_match = boundary_re.search(content)
    if not boundary_match:
        raise ValueError('Could not find the blog-grid closing boundary. Stopping without writing anything.')

    grid_end = boundary_match.start()
    for i, card in enumerate(cards):
        end = card['_next_start'] if card['_next_start'] is not None else grid_end
        # Trim back to before the next card's leading comment/whitespace, matching how
        # that next card's own `start` was computed (avoid duplicating the comment).
        if card['_next_start'] is not None:
            next_card_start = cards[i + 1]['start']
            end = next_card_start
        card['text'] = content[card['start']:end]

    grid_start = cards[0]['start']

    ordered = sorted(range(len(cards)), key=lambda i: cards[i]['sort_key'], reverse=True)
    new_order_ids = [cards[i]['id'] for i in ordered]
    current_order_ids = [c['id'] for c in cards]

    if new_order_ids == current_order_ids:
        print('Grid is already correctly sorted by date — nothing to do.')
        return

    print('New order (newest first):')
    for i in ordered:
        c = cards[i]
        print(f'  {c["sort_key"]}  {c["id"]}')

    new_grid_text = ''.join(cards[i]['text'] for i in ordered)
    new_content = content[:grid_start] + new_grid_text + content[grid_end:]

    if args.dry_run:
        print('\n--dry-run set: nothing written. Re-run without --dry-run to apply.')
        return

    backup_path = EVENTS_PATH + '.bak'
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Backup written: {backup_path}')

    with open(EVENTS_PATH, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'events.html updated ({len(new_content)} bytes).')


if __name__ == '__main__':
    main()
