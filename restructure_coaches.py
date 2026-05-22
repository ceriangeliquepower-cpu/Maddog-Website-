"""
restructure_coaches.py
Restructures coaches.html:
1. Adds .af-grid--rev CSS class for criss-cross reversal
2. Applies af-grid--rev to Wren's section (photo right, text left)
3. Inserts Robin JJ Williams as 3rd featured section (photo left)
4. Moves coach cards grid to bottom (after Robin)
Order: Amanda → Wren (reversed) → Robin → Coaches grid → Philosophy
5. Adds Robin to JSON-LD and credential strip
"""
import re

fpath = r"C:\Users\HP\Desktop\Maddog Web design pages\coaches.html"

with open(fpath, 'r', encoding='utf-8') as f:
    content = f.read()

original = content

# ─────────────────────────────────────────────────────────────────
# 1. Add .af-grid--rev CSS before the closing </style> of the main
#    style block (the one that contains .af-grid definition)
# ─────────────────────────────────────────────────────────────────
rev_css = """
/* ── CRISS-CROSS: reverse col order without reordering HTML ── */
.af-grid--rev{direction:rtl}
.af-grid--rev>*{direction:ltr}
.af-grid--rev .af-text{border-left:none!important;border-right:3px solid var(--gold)!important}
@media(max-width:1024px){
  .af-grid--rev{direction:ltr!important}
  .af-grid--rev .af-text{border-right:none!important;border-top:3px solid var(--gold)!important}
}
"""

# Insert before the last </style> in the head (the unified text system block)
insert_before = "/* ═══════════════════════════════════════════════════\n   UNIFIED TEXT SYSTEM"
if insert_before in content:
    content = content.replace(insert_before, rev_css + insert_before, 1)
    print("OK: Added .af-grid--rev CSS")
else:
    print("WARN: Could not find CSS insertion point")

# ─────────────────────────────────────────────────────────────────
# 2. Define section markers
# ─────────────────────────────────────────────────────────────────
COACHES_COMMENT = '<!-- ══════════════════════════════════\n     SUPPORTING COACHES\n══════════════════════════════════ -->'
WREN_COMMENT    = '<!-- ══════════ WREN KOBUS — FEATURED ══════════ -->'
PHIL_COMMENT    = '<!-- ── COACHING PHILOSOPHY PILLARS ── -->'

# ─────────────────────────────────────────────────────────────────
# 3. Split content into sections
# ─────────────────────────────────────────────────────────────────
# Split on COACHES_COMMENT
if COACHES_COMMENT not in content:
    print("ERROR: Could not find COACHES_COMMENT"); exit(1)
before_coaches, rest = content.split(COACHES_COMMENT, 1)

# Split rest on WREN_COMMENT
if WREN_COMMENT not in rest:
    print("ERROR: Could not find WREN_COMMENT"); exit(1)
coaches_raw, rest2 = rest.split(WREN_COMMENT, 1)

# Split rest2 on PHIL_COMMENT
if PHIL_COMMENT not in rest2:
    print("ERROR: Could not find PHIL_COMMENT"); exit(1)
wren_raw, phil_and_after = rest2.split(PHIL_COMMENT, 1)

print("OK: Split into sections")
print(f"  before_coaches: {len(before_coaches):,} chars")
print(f"  coaches_raw:    {len(coaches_raw):,} chars")
print(f"  wren_raw:       {len(wren_raw):,} chars")
print(f"  phil_and_after: {len(phil_and_after):,} chars")

# ─────────────────────────────────────────────────────────────────
# 4. Modify Wren section: add af-grid--rev class
# ─────────────────────────────────────────────────────────────────
wren_modified = wren_raw.replace(
    '<div class="af-grid">',
    '<div class="af-grid af-grid--rev">',
    1  # only first occurrence (the section grid)
)
if wren_modified == wren_raw:
    print("WARN: af-grid--rev NOT applied to Wren (pattern not found)")
else:
    print("OK: Applied af-grid--rev to Wren section")

# ─────────────────────────────────────────────────────────────────
# 5. Build Robin JJ Williams featured section
# ─────────────────────────────────────────────────────────────────
robin_section = """
<!-- ══════════ ROBIN JJ WILLIAMS — FEATURED ══════════ -->
<section class="amanda-feature" style="background:var(--deep)">
  <div class="si">
    <div class="sec-label">Sports Physiotherapist</div>
    <div class="af-grid">

      <!-- PHOTO -->
      <div class="af-photo">
        <div class="photo-slot" id="robin-p" onclick="swapPhoto('robin-p')" style="height:100%;min-height:580px">
          <div class="gc tl"></div><div class="gc br"></div>
          <img src="" alt="Robin JJ Williams, Sports Physiotherapist at Maddog Performance Institute" width="600" height="800" loading="lazy">
          <div class="slot-overlay"><span class="slot-icon">\U0001f5bc</span><span class="slot-label">Robin Photo</span></div>
          <div class="slot-hint">Click to upload photo</div>
        </div>
      </div>

      <!-- TEXT -->
      <div class="af-text">
        <span class="af-role">Sports Physiotherapist</span>
        <div class="af-name" contenteditable="true">Robin JJ Williams</div>
        <div class="af-stats">
          <div class="af-stat"><div class="af-stat-n">10+</div><div class="af-stat-l">Yrs Pro Sport</div></div>
          <div class="af-stat"><div class="af-stat-n">MSc</div><div class="af-stat-l">UCT Masters</div></div>
          <div class="af-stat"><div class="af-stat-n">4</div><div class="af-stat-l">Pro Teams</div></div>
          <div class="af-stat"><div class="af-stat-n">Physio</div><div class="af-stat-l">Sports Specialist</div></div>
        </div>
        <div class="af-quote" contenteditable="true">"Quality over Quantity — injuries are temporary hurdles, where successful outcomes are easily obtainable if identified and managed properly."</div>
        <div class="cred-pills">
          <span class="cpill">Stormers</span>
          <span class="cpill">Zebre Parma, Italy</span>
          <span class="cpill">SARU U17/U18</span>
          <span class="cpill">The Sharks</span>
        </div>
        <div class="af-specs">
          <span class="spec-tag">Sports Physiotherapy</span>
          <span class="spec-tag">Concussion Prevention</span>
          <span class="spec-tag">Rehabilitation</span>
          <span class="spec-tag">Pro Rugby Teams</span>
          <span class="spec-tag">Adolescent Sport</span>
        </div>
        <div class="af-actions">
          <a href="contact.html#form" class="btn btn-g">Book With Robin</a>
        </div>
      </div>

    </div>
  </div>
</section>

"""

print("OK: Robin section built")

# ─────────────────────────────────────────────────────────────────
# 6. Reassemble content
# ─────────────────────────────────────────────────────────────────
content = (
    before_coaches +
    WREN_COMMENT + wren_modified +
    robin_section +
    COACHES_COMMENT + coaches_raw +
    PHIL_COMMENT + phil_and_after
)

print("OK: Reassembled content")

# ─────────────────────────────────────────────────────────────────
# 7. Update JSON-LD: add Robin to employee list
# ─────────────────────────────────────────────────────────────────
robin_jsonld = '    {"@type":"Person","name":"Robin JJ Williams","jobTitle":"Sports Physiotherapist","description":"10+ years in professional sport. Teams: Stormers, Zebre Parma, SARU U17/U18, The Sharks. Currently completing MSc at UCT in concussion prevention in adolescent rugby."}'
old_employee_end = '    {"@type":"Person","name":"Tristan","jobTitle":"Personal Trainer"}\n  ]'
new_employee_end = (
    '    {"@type":"Person","name":"Tristan","jobTitle":"Personal Trainer"},\n' +
    robin_jsonld + '\n  ]'
)
if old_employee_end in content:
    content = content.replace(old_employee_end, new_employee_end, 1)
    print("OK: Updated JSON-LD with Robin")
else:
    print("WARN: Could not update JSON-LD (pattern not found)")

# ─────────────────────────────────────────────────────────────────
# 8. Update credential strip: add Robin item
# ─────────────────────────────────────────────────────────────────
robin_cred = '    <div class="cred-item">Robin JJ Williams · Sports Physiotherapist</div>\n'
# Insert after Wren's cred item
wren_cred_pattern = '<div class="cred-item">Wren Kobus · Strength &amp; Conditioning / Registered Nurse</div>'
if wren_cred_pattern in content:
    content = content.replace(
        wren_cred_pattern,
        wren_cred_pattern + '\n' + robin_cred.strip(),
        1
    )
    print("OK: Added Robin to credential strip")
else:
    print("WARN: Could not add Robin to credential strip (Wren pattern not found)")
    # Try a fallback
    wren_cred_alt = 'Wren Kobus'
    idx = content.find('class="cred-item">Wren Kobus')
    if idx != -1:
        end_idx = content.find('</div>', idx) + 6
        content = content[:end_idx] + '\n    ' + robin_cred.strip() + content[end_idx:]
        print("OK: Added Robin to credential strip (fallback method)")

# ─────────────────────────────────────────────────────────────────
# 9. Write file
# ─────────────────────────────────────────────────────────────────
if content != original:
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK: coaches.html written successfully")
else:
    print("WARN: No changes were made")
