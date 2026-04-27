# Maddog Performance Institute — Session Handoff

> Paste this file into a new Claude Code or Claude web chat to resume exactly where we left off.

---

## Project Snapshot

**Client:** Amanda "Maddog" Lino — MMA Gym + Recovery/Wellness Centre, Ballito KZN  
**GitHub repo:** https://github.com/ceriangeliquepower-cpu/Maddog-Website-.git  
**Netlify preview:** https://69d75b86a9622c318e399025--stellar-biscochitos-7f6a1c.netlify.app/  
**Live domain:** maddogperformance.co.za (DNS not yet pointed to Netlify)  
**Local files:** `C:\Users\HP\Desktop\Maddog Web design pages\`  
**All 14 HTML files** are self-contained — no build step, no server needed. Open directly in browser.

---

## Design System — Non-Negotiable

```
Colors:
  --black:  #080808   primary background
  --deep:   #0F0F0F   section alternation
  --gold:   #C9A84C   all accents
  --white:  #F5F0E8   body text

Fonts:  Bebas Neue (headings) · Barlow Condensed (body)
Brand:  Always "Maddog" — never "Mad Dog" / "MadDog" / "MADDOG"
```

---

## All Files — Current Status

| File | Status | Notes |
|------|--------|-------|
| index.html | ✅ Updated this session | Corporate + Recovery Suite restructured to mod-block layout |
| amanda.html | ✅ Updated this session | CTA changed, 8 sponsor cards with logo upload slots |
| athletes.html | ✅ Updated this session | 8 sponsor cards with logo upload slots |
| coaches.html | ✅ Updated | Ticker fixed to 70s / Bebas Neue 14px / ◆ separator |
| training.html | ✅ Complete | |
| recovery.html | ✅ Complete | Has 4 links to maddog-pricing.html (not yet created) |
| events.html | ✅ Complete | |
| contact.html | ✅ Complete | |
| pricing.html | ⚠️ Needs rename/rebuild | Currently contains recovery suite content — see below |
| blog-cold-plunge-sauna-ballito.html | ✅ Complete | Ticker fixed |
| blog-bjj-beginners-ballito.html | ✅ Complete | Ticker fixed |
| blog-powerlifting-women-ballito.html | ✅ Complete | Ticker fixed |
| blog-iv-drip-therapy-ballito.html | ✅ Complete | Ticker fixed |
| blog-mma-training-ballito.html | ✅ Complete | Ticker fixed |

---

## What Was Done This Session (in order)

### 1. index.html — Corporate & Recovery Suite Restructure
- **Replaced** the old `.corp-section` / `.pt-section` layout with the `mod-block` mirror pattern from recovery.html
- **Corporate Wellness:** full-bleed photo LEFT / gold-bordered text panel RIGHT (`mod-grid`)
- **Recovery Suite:** text panel LEFT / photo slot RIGHT (`mod-grid rev` with `direction:rtl`)
- **Base64 photo preserved** in the Corporate slot (corpPhoto)
- **Added mod-block CSS** + mobile stacking at 900px
- **Fixed sec-label:** replaced `mod-tag` (gold-background pill) with `sec-label` (plain gold text) to match all other home page sections

### 2. index.html — Hero CTA
- "Book Free Trial" → **"Explore Recovery"** linking to `recovery.html`

### 3. amanda.html — Bottom CTA
- "Book Your Free Trial" → **"Explore Recovery"** linking to `recovery.html`

### 4. amanda.html — Sponsor Section
- Added 3 new placeholder sponsor cards: **Ramessur**, **Coco de Mer**, **ATeam**
- Total now: 8 cards in a 4×2 grid
- **Replaced all 8 emoji placeholders** with click-to-upload logo slots (`swapLogo()`)
- Logo slots: full card width × 120px tall
- Sponsor names: locked to full white with CSS specificity override

### 5. athletes.html — Sponsor Section (mirrors Amanda exactly)
- Added **Ramessur**, **Coco de Mer**, **ATeam** placeholder cards
- Replaced all 8 `sponsor-logo-wrap` emojis with upload slots
- Same CSS, same `swapLogo()` function, same white name colour override

### 6. Credential Strip Ticker — All Pages Fixed
- Speed: `70s` linear infinite
- Font: `Bebas Neue` 14px, letter-spacing `.14em`
- Separator: `◆` at 7px, opacity .4

---

## Sponsor Cards — Current State

All 8 sponsors appear on both `amanda.html` and `athletes.html`:

| Sponsor | URL | Status |
|---------|-----|--------|
| Mozambik | https://www.mozambik.co.za/ | ✅ Live link |
| Concha Café & Bakery | http://concha.co.za/ | ✅ Live link |
| Conchilla | https://conchilla.co.za/ | ✅ Live link |
| Fiamma Grill | https://www.fiammagrill.co.za/ | ✅ Live link |
| ScoutNet | https://scoutnet.co.za/ | ✅ Live link |
| Coco de Mer | `href="#"` placeholder | ⏳ Need real URL + description |
| Ramessur | `href="#"` placeholder | ⏳ Need real URL + description |
| ATeam | `href="#"` placeholder | ⏳ Need real URL + description |

**Logos:** All 8 cards have click-to-upload slots. Client clicks the slot, selects a PNG/JPG, then hits Save Page to bake it in.

---

## Outstanding Work — Priority Order

### 1. Pricing Pages (TWO separate files needed)

**`pricing.html`** — MMA / Personal Training / some Recovery pricing  
- 18 training slots currently show "POA" — client needs to decide: show prices or enquire-only  
- No work done on this yet

**`maddog-pricing.html`** — Recovery Suite full pricing menu  
- The current `pricing.html` file actually contains the recovery suite content  
- It needs to be **renamed to `maddog-pricing.html`**  
- recovery.html already has 4 links pointing to `maddog-pricing.html` — will work once renamed  

### 2. Sponsor Cards — Fill in Placeholders
- Add real URLs and descriptions for: Coco de Mer, Ramessur, ATeam
- Coco de Mer website confirmed: `cocodemer.co.za` — 4-star boutique hotel in Ballito, Afro-Bali design, eco-forest overlooking Indian Ocean, features Fiamma Grill restaurant, spa, events
- Ramessur and ATeam: client to provide URLs and business descriptions

### 3. recovery.html Updates (from original handoff — not yet done)
- Add **Slimming Clinic** section (prices: R900 / R500 / R300–R700/week / R350 / R150)
- Add **Aesthetic & Wellness IV** section (GLOW R1,440 / Bespoke from R1,000+ / Add-ons R150–R700)
- Update Contrast Therapy prices: post-training R80/R170/R250, general R270/R350/R850
- Confirm Athlete Membership tiers are populated

### 4. SEO Round 2 (not yet done)
- AggregateRating / Review schema
- BreadcrumbList on all 5 blog pages
- Internal linking (recovery.html → blog pages, training.html → blog pages, index.html → all blogs)
- sitemap.xml — missing all 5 blog URLs
- Google Business Profile — not yet claimed (biggest local ranking lever)

### 5. DNS
- Point `maddogperformance.co.za` to Netlify (A record + CNAME)

---

## Technical Patterns — Key Rules

1. **Never `*{max-width:100%}` in media queries** — kills hero animation
2. **All `.reveal` elements need `.visible` pre-applied** — scroll JS unreliable in file://
3. **Inline styles beat cascade** — use on the element when stylesheet fights you
4. **Never z-index on hero sections** — stacking context conflict with credential strip
5. **Hero: `padding-top` not `margin-top`** — margin gets clipped by overflow:hidden
6. **`.cred-scroll` must have `width:max-content`** — never override in media queries
7. **All images base64-embedded** — no external image files ever
8. **Duplicate CSS in some files** — later definition wins; use specificity override when needed

---

## mod-block Pattern (used in recovery.html and now index.html)

```css
.mod-block{padding:72px 0}
.mod-grid{display:grid;grid-template-columns:1fr 1fr;gap:0;min-height:500px;align-items:stretch}
.mod-grid.rev{direction:rtl}          /* reverses column order visually */
.mod-grid.rev > *{direction:ltr}
.mod-photo .photo-slot{height:100%;min-height:440px}
.mod-text{padding:64px 60px;display:flex;flex-direction:column;justify-content:center}
/* Photo LEFT, text RIGHT: use mod-grid, put photo first in DOM */
/* Text LEFT, photo RIGHT: use mod-grid rev, put photo first in DOM */
```

---

## swapLogo Pattern (added to amanda.html and athletes.html)

```javascript
function swapLogo(slotId) {
  var inp = document.createElement('input');
  inp.type = 'file'; inp.accept = 'image/*';
  inp.onchange = function(e) {
    var file = e.target.files[0]; if (!file) return;
    var reader = new FileReader();
    reader.onload = function(ev) {
      var img = document.getElementById(slotId + '-img');
      img.src = ev.target.result;
      img.style.display = 'block';
      document.getElementById(slotId).classList.add('loaded');
    };
    reader.readAsDataURL(file);
  };
  inp.click();
}
```

Logo slot HTML pattern:
```html
<div class="sponsor-logo-slot" id="logo-NAME" onclick="event.preventDefault();swapLogo('logo-NAME')" title="Click to upload NAME logo">
  <img id="logo-NAME-img" src="" alt="NAME Logo" style="display:none;width:100%;height:100%;object-fit:contain;padding:6px">
  <div class="logo-hint">
    <span style="font-size:20px;opacity:.3">&#128444;</span>
    <span style="font-size:7px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--gold-dim)">Upload Logo</span>
  </div>
</div>
```

---

## Content Still Needed from Client

| Gap | Detail |
|-----|--------|
| Amanda fight record | 6 remaining pro fights — opponent, event, method, round, result |
| Coach credentials | Lucky, Winston, Tristan formal certs; Wren SANC registration number |
| Training prices | 18 slots POA — show or enquire? |
| Sponsor details | Ramessur and ATeam — website URLs and business descriptions |
| Upcoming events | Venues and ticket links (currently "TBC") |
| Photos | All pages have click-to-upload slots — client uploads directly |

---

## Git Status

- Branch: `main`
- Remote: `https://github.com/ceriangeliquepower-cpu/Maddog-Website-.git`
- All changes from this session are committed and pushed
- Latest commit: Athletes sponsor section mirror

---

*Last updated: April 2026 — paste this file into a new Claude chat to resume.*
