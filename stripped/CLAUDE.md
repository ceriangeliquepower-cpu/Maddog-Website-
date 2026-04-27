# Maddog Performance Institute — Claude Code Handoff

> This document is a complete project handoff for Claude Code to continue building the Maddog Performance Institute website. Read this fully before touching any file.

---

## Project Overview

**Client:** Amanda "Maddog" Lino  
**Business:** MMA Gym + Recovery/Wellness Centre  
**Location:** 22 Sandra Rd, Balvista Centre, Ballito, KZN  
**Live domain:** maddogperformance.co.za *(still showing "Coming Soon" — DNS not yet pointed to Netlify)*  
**Netlify preview:** https://69d75b86a9622c318e399025--stellar-biscochitos-7f6a1c.netlify.app/  
**Contact:** +27 63 442 1690 | info@maddogperformance.co.za  
**Instagram:** @amanda_maddog_lino

---

## Design System — NON-NEGOTIABLE

```
Colors:
  Background:   #080808 (primary black)
  Surface:      #0F0F0F (deep black)
  Accent/Gold:  #C9A84C
  Text:         #F5F0E8 (off-white)

Fonts:
  Headings:     Bebas Neue
  Body:         Barlow Condensed

Brand name rule:
  ALWAYS: "Maddog" — lowercase d
  NEVER:  "Mad Dog" / "MadDog" / "MADDOG" in body copy
```

---

## Critical Technical Rules

These are hard-won fixes. Do NOT undo them.

1. **Never use `*{max-width:100%}` in media queries** — kills the hero banner animation
2. **All `reveal` class elements must have `visible` pre-applied** — opacity is 0 by default; scroll-trigger JS is unreliable in standalone files
3. **Inline styles beat stylesheet cascade** — use inline styles on HTML elements for persistent overrides when stylesheet fixes fail
4. **Never add `z-index` to hero sections** — causes stacking context conflicts with the credential strip
5. **Hero needs `padding-top` not `margin-top`** — margin causes overflow:hidden clipping
6. **Credential strip: no `position` or `z-index`** — plain block flow only
7. **`cred-scroll` must have `width:max-content`** — never override in media queries
8. **All files are self-contained** — all photos must be base64-embedded (PIL-compressed JPEG). No external asset dependencies ever.

---

## Core Technical Pattern Per Page

```
- PIL-compressed base64 JPEG images per slot
- swapPhoto(slotId) via FileReader API for click-to-upload
- .loaded class toggling to reveal uploaded images
- savePage() via document.documentElement.outerHTML → Blob download
```

---

## File Status

### 13 Total Files — All COMPLETE as of handoff

**Core Pages (8):**

| File | Status |
|------|--------|
| index.html | ✅ Complete |
| amanda.html | ✅ Complete |
| athletes.html | ✅ Complete |
| coaches.html | ✅ Complete |
| training.html | ✅ Complete |
| recovery.html | ✅ Complete |
| events.html | ✅ Complete |
| contact.html | ✅ Complete |

**Blog Pages (5) — all linked from events.html:**

| File | Status |
|------|--------|
| blog-cold-plunge-sauna-ballito.html | ✅ Complete |
| blog-bjj-beginners-ballito.html | ✅ Complete |
| blog-powerlifting-women-ballito.html | ✅ Complete |
| blog-iv-drip-therapy-ballito.html | ✅ Complete |
| blog-mma-training-ballito.html | ✅ Complete |

> All 13 files drop into the same Netlify folder. All relative links work correctly as-is.

---

## Outstanding Work — Priority Order

### 1. Dedicated Pricing Page (NEW FILE)

**File to create:** `pricing.html`

**Decision already made:** Build a dedicated pricing page AND update `recovery.html` with key prices (combination approach).

**Sections to include (in this order):**

#### IV Therapy — GET DRIPPED Menu

*FOUNDATION LAUNCH PRICING* (use this language — intentional urgency positioning)

**Core Protocols:**
| Treatment | Description | Price |
|-----------|-------------|-------|
| HYDRATE | Rehydrate. Restore. Reset. | R865 |
| RECOVER | Reduce soreness. Restore energy. | R1,080 |
| RESET | Calm. Clarity. Nervous system support. | R1,080 |
| REBOOT | Feel human again. | R1,080 |
| INFLAMMATION SUPPORT | Reduce. Repair. Recover. | R696 |

**Performance & Immunity:**
| Treatment | Description | Price |
|-----------|-------------|-------|
| PERFORMANCE | Energy. Endurance. Output. | R1,296 |
| IMMUNITY | Strengthen. Defend. Recover. | R1,196 |
| DETOX (ADVANCED) | Deep cleanse. Cellular reset. | R1,296 |

**Aesthetic & Wellness:**
| Treatment | Description | Price |
|-----------|-------------|-------|
| GLOW | Brighten. Detox. Radiate. | R1,440 |

**NAD+ Signature Protocols** *(Administered slowly for optimal absorption)*
- NAD+ ENERGY — Cellular energy and fatigue support — R2,016 (single) | Packages via consultation
- NAD+ COGNITIVE — Focus. Mental clarity. Brain optimisation — R2,016 (single) | Packages via consultation
- NAD+ PERFORMANCE — Recovery. Output. Athletic support — R2,016 (single) | Packages via consultation
- NAD+ ANTI-AGING — Longevity. Cellular repair. Vitality — R2,016 (single) | Packages via consultation

**Bespoke IV Optimisation:**
- Fully customised IV therapy — consultation + personalised formulation + targeted dosing
- From R1,000+

**Add-Ons:** Glutathione / Vitamin C Boost / B12 Injection / L-Carnitine / CoQ10 — From R150–R700

**Protocol Packages:**
- 4 Sessions: From R4,176
- 6 Sessions: From R6,120
- 8 Sessions: From R7,920

---

#### Contrast Therapy

**Post-Training Recovery Access** *(Available to all training clients)*:
| Service | Price |
|---------|-------|
| Ice Bath (Post Training) | R80 |
| Sauna (Post Training) | R170 |
| Full Contrast Therapy — Infrared Sauna + Ice Bath (45 min) | R250 |

**General Contrast Therapy Pricing:**
| Service | Price |
|---------|-------|
| Contrast Access Self-Guided — Sauna + Ice Bath (45 min) | R270 |
| Structured Contrast Session — Guided protocol with timing and coaching (60 min) | R350 |
| Premium Recovery Session — Contrast + IV Therapy Jet Fuel Nano (75 min) | R850 |

---

#### Athlete Memberships

| Tier | Price | Inclusions |
|------|-------|------------|
| ATHLETE BASIC | R850/month | 4 Contrast Sessions/month, priority booking, recovery environment access |
| ATHLETE PERFORMANCE | R1,500/month | 8 Contrast Sessions/month, discounted add-ons, priority booking, performance recovery support |
| ATHLETE ELITE | R3,000+/month | Unlimited Contrast Therapy, priority booking, discounted IV therapy, discounted peptide support (via consultation), integrated recovery system |

---

#### Slimming Clinic — Medical Weight Management & Body Optimisation

| Service | Price |
|---------|-------|
| Doctor Assessment & Consultation (online or in-person) | R900 |
| Slimming Consultation | R500 |
| Weekly Slimming Injections | R300–R700/week |
| InBody Consultation (full analysis + interpretation + goal alignment) | R350 |
| InBody Test Only (quick scan) | R150 |

**Small print:** *All treatments are administered following consultation and are tailored to individual medical and wellness needs.*

---

#### Peptide Therapy

No prices shown — enquiry-only. Display as:
- Prescribed by in-house medical doctor
- Individually tailored and monitored
- Dispensed via SAPHRA-approved compounding pharmacies
- Contact required to begin assessment

---

### 2. recovery.html Updates (EXISTING FILE)

Add the following two NEW sections to `recovery.html`, matching existing CSS class patterns exactly:

**Section A: Slimming Clinic**
- Doctor consultation R900, Slimming consultation R500
- Weekly injections R300–R700/week
- InBody tracking R350 / test-only R150
- "Foundation Launch Pricing" badge
- Bottom line: *All treatments are administered following consultation and are tailored to individual medical and wellness needs.*

**Section B: Aesthetic & Wellness (IV)**
- GLOW treatment R1,440
- Bespoke IV Optimisation from R1,000+
- Add-ons from R150–R700
- Link to full pricing page

**Existing sections to update with prices:**
- Contrast Therapy section: add post-training prices (R80 / R170 / R250) and general prices (R270 / R350 / R850)
- Athlete Memberships: already may be present — confirm tiers are populated with above data

> IMPORTANT: Study `recovery.html` existing HTML structure and CSS class patterns BEFORE writing any new section code. Match exactly.

---

### 3. SEO Round 2 (NOT YET DONE)

Apply to all relevant files:

- [ ] AggregateRating / Review schema (enables star ratings in Google SERPs)
- [ ] BreadcrumbList schema on all 5 blog pages
- [ ] Internal linking: `recovery.html` → cold plunge + IV blog pages; `training.html` → BJJ + MMA blog pages; `index.html` → all 5 blogs
- [ ] `sitemap.xml` — currently missing all 5 blog page URLs. Generate and add.
- [ ] Google Business Profile — not yet claimed (single biggest local ranking lever — flag this to client)

---

### 4. DNS Configuration

- Point `maddogperformance.co.za` DNS from current "Coming Soon" host → Netlify
- Standard Netlify DNS setup: A record + CNAME
- Once live, Google indexing begins immediately

---

## Content Populated — Reference Data

### Amanda Lino
- Born: 15 Aug 1990, Ballito KZN
- Started MMA: 2011 (originally to get fit), went 6-0 amateur
- IMMAF Featherweight World Champion 2014 — Las Vegas (defeated Sweden + USA via KO/TKO)
- Turned pro 2015 — first-round TKO over Stephanie Quaile, EFC 38
- Inaugural EFC Women's Flyweight Champion 2017 — defeated Jacqui Trosee via armbar, EFC 60
- EFC Bantamweight Champion — first South African female double-division champion
- 2024: Head coach, Team South Africa, IMMAF Africa Championships, Windhoek, Namibia
- BJJ Brown Belt, European NAGA Women's Absolute Champion
- ⚠️ Fight record incomplete — 6 remaining pro fights still need: opponent, event, method, round, result

### Fighters (athletes.html)
- Blaise Khors: 2-0, Age 17, MMA, KZN Team — Lights Out 2: TKO R2 1:13 vs Troy Muller
- Travis Andrews: 1-1, Age 14, MMA, KZN Team — Lights Out 2: Won via illegal sub R1 2:15 vs O'Neil Naicker
- Luke de Beer: 5-6, Age 17, MMA, SA Team
- Travis Cuthbert: 0-0, Age 18, MMA, SA Team — IMMAF World Bronze Abu Dhabi 2025
- Joshua de Beer: 5-2, Age 19, MMA, SA Team
- Lucky Hamadziripi: 6-1, Age 29, MMA
- Circuits: EFC (Amanda), IMMAF / MFC / VERSUS (junior fighters)

### Coaches (coaches.html)
- Amanda Lino: Head Coach & Founder — full bio populated ✅
- Lucky Hamadziripi: MMA & Kickboxing Coach — ⚠️ credentials still placeholder
- Wren Kobus: S&C / Powerlifting / Nurse Practitioner — Proteas Master 1 U69 2025, KZNPLF Record Holder, SAPF Provincial Rep, Director KZN Powerlifting Association — ⚠️ SANC registration number missing
- Winston: Boxing Coach, 10+ years — ⚠️ formal credentials still placeholder
- Tristan: Personal Trainer — ⚠️ credentials still placeholder

### Sponsors
- Mozambik: mozambik.co.za
- Concha Café & Bakery: concha.co.za
- Conchilla: conchilla.co.za
- Fiamma Grill: fiammagrill.co.za
- ScoutNet: scoutnet.co.za

### Lights Out 2 Results (28/03/2026)
- Travis Andrews WIN — Illegal Submission R1 2:15 vs O'Neil Naicker
- Blaise Khors WIN — TKO R2 1:13 vs Troy Muller
- Nicole Tome Alves WIN — Split Decision vs Linda Baraza

### Class Schedule (training.html)
- Mon/Wed: 10:00 MMA Pro · 17:00 Kickboxing · 18:00 BJJ
- Tue/Thu: 05:30 Boxing Fitness · 10:00 MMA Pro · 17:00 MMA Basics · 18:00 MMA Advanced
- Fri: 10:00 MMA Pro · 17:00 Open Mat
- Sat: 09:00 Open Mat

---

## Content Still Needed from Client

| Gap | Detail |
|-----|--------|
| Amanda fight record | 6 remaining pro fights — opponent, event, method, round, result |
| Coach credentials | Lucky, Winston, Tristan formal certifications; Wren SANC number |
| Training prices | 18 slots currently showing POA — decide: show or enquire |
| Upcoming events | Venues and ticket links (currently "TBC") |
| Photos | All pages have click-to-upload slots ready — client uploads directly |

---

## SEO Round 1 — Status (All Complete)

| Signal | Status |
|--------|--------|
| Title tags ≤60 chars | ✅ All 8 pass |
| Meta descriptions 130–160 chars | ✅ All 8 pass |
| H1 contains primary keyword | ✅ All 8 pass |
| Canonical tags | ✅ All 8 pass |
| Schema markup | ✅ All 8 pass |
| Brand name consistent | ✅ Zero violations |

### Keyword Strategy

**Win Now (low competition):** MMA gym Ballito, BJJ Ballito, personal trainer Ballito, sports recovery Ballito, IV drip therapy Ballito, infrared sauna Ballito, fight gym Ballito

**Build Toward (medium):** BJJ KZN North Coast, MMA training KZN, cold plunge therapy KZN, corporate wellness KZN

**Long-Term via Blog:** MMA gym South Africa, best MMA gym KZN, IV drip therapy SA

---

## Hosting

- Platform: Netlify
- All 13 HTML files are self-contained — drop in same folder, all links work
- Once DNS is pointed, Google indexes immediately
- Google Business Profile must be claimed and optimised before SEO Round 2 is worth doing

---

## How to Work on This Project

1. **Study before you edit.** Always read the existing file structure and CSS class patterns before writing any new HTML/CSS.
2. **Match the design system exactly.** Every new section must use existing class patterns — no new design patterns.
3. **Inline styles for overrides.** When stylesheet cascade fails, inline styles on the element are the established fix.
4. **Test self-contained.** Open the file directly in a browser with no server. It must work.
5. **Deliver as standalone files.** Every output is a complete `.html` file — never partial snippets unless explicitly asked.

---

*Handoff prepared for Claude Code continuation. All decisions documented. Start with the pricing page — `pricing.html` — then the `recovery.html` updates.*
