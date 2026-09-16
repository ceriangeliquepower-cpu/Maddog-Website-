# SEO Audit Report — 2026-09-16

Pages scanned: 53 (34 gym, 19 wellness)
Findings: **0 critical**, **53 warning**, 23 info

## Performance / Core Web Vitals risk

**10 of 53 pages are over 2MB** (32.5MB combined). Google uses Core Web Vitals (LCP, INP, CLS) as a direct ranking factor. Pages this size, especially with images inline as base64 rather than separately-cacheable files, are very likely failing the "good" LCP threshold on mobile. This is a real ranking lever, not a routine cleanup item — it just isn't something a hook can safely auto-block on, since fixing it site-wide is an architecture decision (base64-inline vs. file-referenced images), not a one-line fix.

- `index.html` — 4596.4KB (4.5MB)
- `athletes.html` — 4161.3KB (4.1MB)
- `training-kickboxing-ballito.html` — 3972.6KB (3.9MB)
- `recovery.html` — 3818.6KB (3.7MB)
- `wellness.html` — 3503.2KB (3.4MB)
- `amanda.html` — 3067.3KB (3.0MB)
- `events.html` — 2968.9KB (2.9MB)
- `training.html` — 2935.8KB (2.9MB)
- `training-womens-boxing-ballito.html` — 2227.7KB (2.2MB)
- `training-personal-training-ballito.html` — 2068.7KB (2.0MB)

## Site-wide

- All pages present in sitemap.xml

## Redirects (`_redirects`) — live-tested against https://www.maddogperformance.co.za

- All checked redirect rules are correctly enforced

## Internal links — every internal href live-tested against https://www.maddogperformance.co.za

- Every internal link found across all pages resolves to a live 200

## Per-page findings

### amanda.html (gym, 3067.3KB)
*Title: Amanda 'Maddog' Lino | 2x EFC World Champion | Maddog*

- **WARNING**: 1 of 26 <img> tags have empty/missing alt text (some empty alt may be intentionally decorative — verify)
- **WARNING**: Page is 3067.3KB (3.0MB) — this is a real Core Web Vitals (LCP) risk, which is a confirmed Google ranking factor, not just a "nice to have" performance note. A page this size is very likely failing Google's "good" LCP threshold (<2.5s) on mobile. Base64-embedded images can't be cached separately from the HTML, so every visit re-downloads everything. See the aggregate "Performance / Core Web Vitals risk" section at the top of this report — this is not something to leave sitting as a routine warning.

### athletes.html (gym, 4161.3KB)
*Title: Fight Team &amp; Members | Maddog | Ballito*

- **WARNING**: 1 of 32 <img> tags have empty/missing alt text (some empty alt may be intentionally decorative — verify)
- **WARNING**: Page is 4161.3KB (4.1MB) — this is a real Core Web Vitals (LCP) risk, which is a confirmed Google ranking factor, not just a "nice to have" performance note. A page this size is very likely failing Google's "good" LCP threshold (<2.5s) on mobile. Base64-embedded images can't be cached separately from the HTML, so every visit re-downloads everything. See the aggregate "Performance / Core Web Vitals risk" section at the top of this report — this is not something to leave sitting as a routine warning.

### blog-amanda-kobus-coach-ballito.html (gym, 390.8KB)
*Title: Amanda Kobus: Strength Coach and Nurse Practitioner | Maddog*

- **WARNING**: 1 of 3 <img> tags have empty/missing alt text (some empty alt may be intentionally decorative — verify)

### blog-ballito-community-raises-funds-st-lukes.html (gym, 374.9KB)
*Title: When Ballito Showed Up: R53,000 for St Luke’s | Maddog*

- **WARNING**: 1 of 3 <img> tags have empty/missing alt text (some empty alt may be intentionally decorative — verify)

### blog-bjj-beginners-ballito.html (gym, 299.2KB)
*Title: BJJ Classes for Beginners in Ballito KZN | Maddog*

- **WARNING**: 1 of 3 <img> tags have empty/missing alt text (some empty alt may be intentionally decorative — verify)

### blog-cold-plunge-sauna-ballito.html (gym, 324.7KB)
*Title: Cold Plunge &amp; Sauna Recovery Ballito | Maddog*

- **WARNING**: 1 of 3 <img> tags have empty/missing alt text (some empty alt may be intentionally decorative — verify)

### blog-efc-134-amanda-lino-title-defence.html (gym, 255.1KB)
*Title: Amanda Lino Defends EFC Flyweight Title at EFC 134 | Maddog*

- **WARNING**: 1 of 3 <img> tags have empty/missing alt text (some empty alt may be intentionally decorative — verify)

### blog-efc-134-amanda-lino-vs-juliet-chukwu.html (gym, 357.2KB)
*Title: EFC 134: Amanda Lino vs Juliet Chukwu | Maddog*

- **WARNING**: 1 of 3 <img> tags have empty/missing alt text (some empty alt may be intentionally decorative — verify)

### blog-genesis-athlete-recovery-ballito.html (gym, 329.6KB)
*Title: GENESIS Recovery for Athletes Ballito | Maddog*

- **WARNING**: 1 of 3 <img> tags have empty/missing alt text (some empty alt may be intentionally decorative — verify)

### blog-iv-drip-therapy-ballito.html (gym, 251.6KB)
*Title: IV Drip Therapy Ballito KZN | Maddog Performance*

- **WARNING**: 1 of 3 <img> tags have empty/missing alt text (some empty alt may be intentionally decorative — verify)

### blog-mma-training-ballito.html (gym, 332.3KB)
*Title: How to Start MMA Training Ballito | Maddog KZN*

- **WARNING**: 1 of 3 <img> tags have empty/missing alt text (some empty alt may be intentionally decorative — verify)

### blog-powerlifting-women-ballito.html (gym, 333.4KB)
*Title: Powerlifting for Women Ballito KZN | Maddog*

- **WARNING**: 1 of 3 <img> tags have empty/missing alt text (some empty alt may be intentionally decorative — verify)

### blog-robin-jj-williams-physio-ballito.html (gym, 170.5KB)
*Title: Sports Physiotherapy Ballito | Robin JJ Williams | Maddog*

- **WARNING**: 1 of 3 <img> tags have empty/missing alt text (some empty alt may be intentionally decorative — verify)

### blog-womens-self-defence-workshop-ballito.html (gym, 254.9KB)
*Title: Women's Self-Defence Workshop Ballito | Maddog Safety Event*

- **WARNING**: 1 of 3 <img> tags have empty/missing alt text (some empty alt may be intentionally decorative — verify)

### blog-womens-self-defence-workshop-recap-ballito.html (gym, 60.1KB)
*Title: Women's Self-Defence Workshop Recap | Maddog Ballito*

- **WARNING**: 1 of 3 <img> tags have empty/missing alt text (some empty alt may be intentionally decorative — verify)

### blog-youth-mma-training-ballito.html (gym, 154.7KB)
*Title: Youth MMA, BJJ, Kickboxing &amp; Powerlifting Ballito | Maddog*

- **WARNING**: 1 of 3 <img> tags have empty/missing alt text (some empty alt may be intentionally decorative — verify)

### booking.html (gym, 89.5KB)
*Title: Book Online | Maddog Performance Institute | Ballito KZN*

- INFO: Brand spelling matching /\bMADDOG\b/ found, but only inside what looks like a standalone logo/wordmark span (e.g. ">MADDOG<") — verify it is not body copy

### coaches.html (gym, 1625.4KB)
*Title: Coaching Team | Maddog Performance Institute | Ballito KZN*

- **WARNING**: 1 of 11 <img> tags have empty/missing alt text (some empty alt may be intentionally decorative — verify)
- INFO: Page is 1625.4KB — on the larger side, worth checking for embedded base64 images

### contact.html (gym, 454.4KB)
*Title: Book A Free Trial | Maddog Performance Institute*

- **WARNING**: 1 of 3 <img> tags have empty/missing alt text (some empty alt may be intentionally decorative — verify)

### events.html (gym, 2968.9KB)
*Title: Events &amp; Fight Results | Maddog | Ballito*

- **WARNING**: 1 of 16 <img> tags have empty/missing alt text (some empty alt may be intentionally decorative — verify)
- **WARNING**: Page is 2968.9KB (2.9MB) — this is a real Core Web Vitals (LCP) risk, which is a confirmed Google ranking factor, not just a "nice to have" performance note. A page this size is very likely failing Google's "good" LCP threshold (<2.5s) on mobile. Base64-embedded images can't be cached separately from the HTML, so every visit re-downloads everything. See the aggregate "Performance / Core Web Vitals risk" section at the top of this report — this is not something to leave sitting as a routine warning.

### index.html (gym, 4596.4KB)
*Title: MMA Gym Ballito | Maddog Performance Institute*

- **WARNING**: 1 of 25 <img> tags have empty/missing alt text (some empty alt may be intentionally decorative — verify)
- **WARNING**: Page is 4596.4KB (4.5MB) — this is a real Core Web Vitals (LCP) risk, which is a confirmed Google ranking factor, not just a "nice to have" performance note. A page this size is very likely failing Google's "good" LCP threshold (<2.5s) on mobile. Base64-embedded images can't be cached separately from the HTML, so every visit re-downloads everything. See the aggregate "Performance / Core Web Vitals risk" section at the top of this report — this is not something to leave sitting as a routine warning.

### recovery.html (gym, 3818.6KB)
*Title: Sports Recovery Suite Ballito | IV Drip Therapy | Maddog KZN*

- **WARNING**: 1 of 22 <img> tags have empty/missing alt text (some empty alt may be intentionally decorative — verify)
- **WARNING**: Page is 3818.6KB (3.7MB) — this is a real Core Web Vitals (LCP) risk, which is a confirmed Google ranking factor, not just a "nice to have" performance note. A page this size is very likely failing Google's "good" LCP threshold (<2.5s) on mobile. Base64-embedded images can't be cached separately from the HTML, so every visit re-downloads everything. See the aggregate "Performance / Core Web Vitals risk" section at the top of this report — this is not something to leave sitting as a routine warning.

### training-bjj-ballito.html (gym, 534.2KB)
*Title: BJJ Classes Ballito | Brazilian Jiu-Jitsu | Maddog*

- **WARNING**: 1 of 5 <img> tags have empty/missing alt text (some empty alt may be intentionally decorative — verify)

### training-bootcamp-ballito.html (gym, 631.6KB)
*Title: Bootcamp Classes Ballito | Maddog Performance Institute*

- **WARNING**: 1 of 5 <img> tags have empty/missing alt text (some empty alt may be intentionally decorative — verify)

### training-boxing-ballito.html (gym, 747.8KB)
*Title: Boxing Training Ballito | Maddog Performance Institute*

- **WARNING**: 1 of 5 <img> tags have empty/missing alt text (some empty alt may be intentionally decorative — verify)

### training-kickboxing-ballito.html (gym, 3972.6KB)
*Title: Kickboxing Classes Ballito | Maddog Performance Institute*

- **WARNING**: 1 of 5 <img> tags have empty/missing alt text (some empty alt may be intentionally decorative — verify)
- **WARNING**: Page is 3972.6KB (3.9MB) — this is a real Core Web Vitals (LCP) risk, which is a confirmed Google ranking factor, not just a "nice to have" performance note. A page this size is very likely failing Google's "good" LCP threshold (<2.5s) on mobile. Base64-embedded images can't be cached separately from the HTML, so every visit re-downloads everything. See the aggregate "Performance / Core Web Vitals risk" section at the top of this report — this is not something to leave sitting as a routine warning.

### training-kids-bjj-ballito.html (gym, 560.8KB)
*Title: Kids BJJ Classes Ballito | Maddog Performance Institute*

- **WARNING**: 1 of 5 <img> tags have empty/missing alt text (some empty alt may be intentionally decorative — verify)

### training-kids-boxing-ballito.html (gym, 1017.7KB)
*Title: Kids Boxing Classes Ballito | Maddog Performance Institute*

- **WARNING**: 1 of 5 <img> tags have empty/missing alt text (some empty alt may be intentionally decorative — verify)
- INFO: Page is 1017.7KB — on the larger side, worth checking for embedded base64 images

### training-mma-ballito.html (gym, 1786.3KB)
*Title: MMA Training Ballito | Maddog Performance Institute*

- **WARNING**: 1 of 5 <img> tags have empty/missing alt text (some empty alt may be intentionally decorative — verify)
- INFO: Page is 1786.3KB — on the larger side, worth checking for embedded base64 images

### training-olympic-boxing-ballito.html (gym, 741.9KB)
*Title: Olympic Boxing Ballito | Maddog Performance Institute*

- **WARNING**: 1 of 5 <img> tags have empty/missing alt text (some empty alt may be intentionally decorative — verify)

### training-personal-training-ballito.html (gym, 2068.7KB)
*Title: Personal Training Ballito | Maddog Performance Institute*

- **WARNING**: 1 of 7 <img> tags have empty/missing alt text (some empty alt may be intentionally decorative — verify)
- **WARNING**: Page is 2068.7KB (2.0MB) — this is a real Core Web Vitals (LCP) risk, which is a confirmed Google ranking factor, not just a "nice to have" performance note. A page this size is very likely failing Google's "good" LCP threshold (<2.5s) on mobile. Base64-embedded images can't be cached separately from the HTML, so every visit re-downloads everything. See the aggregate "Performance / Core Web Vitals risk" section at the top of this report — this is not something to leave sitting as a routine warning.

### training-powerlifting-ballito.html (gym, 753.4KB)
*Title: Powerlifting Training Ballito | Maddog Performance Institute*

- **WARNING**: 1 of 5 <img> tags have empty/missing alt text (some empty alt may be intentionally decorative — verify)

### training-womens-boxing-ballito.html (gym, 2227.7KB)
*Title: Women's Boxing Ballito | Maddog Performance Institute*

- **WARNING**: 1 of 5 <img> tags have empty/missing alt text (some empty alt may be intentionally decorative — verify)
- **WARNING**: Page is 2227.7KB (2.2MB) — this is a real Core Web Vitals (LCP) risk, which is a confirmed Google ranking factor, not just a "nice to have" performance note. A page this size is very likely failing Google's "good" LCP threshold (<2.5s) on mobile. Base64-embedded images can't be cached separately from the HTML, so every visit re-downloads everything. See the aggregate "Performance / Core Web Vitals risk" section at the top of this report — this is not something to leave sitting as a routine warning.

### training.html (gym, 2935.8KB)
*Title: Training Ballito | MMA, BJJ, Boxing &amp; More | Maddog*

- **WARNING**: 1 of 14 <img> tags have empty/missing alt text (some empty alt may be intentionally decorative — verify)
- **WARNING**: Page is 2935.8KB (2.9MB) — this is a real Core Web Vitals (LCP) risk, which is a confirmed Google ranking factor, not just a "nice to have" performance note. A page this size is very likely failing Google's "good" LCP threshold (<2.5s) on mobile. Base64-embedded images can't be cached separately from the HTML, so every visit re-downloads everything. See the aggregate "Performance / Core Web Vitals risk" section at the top of this report — this is not something to leave sitting as a routine warning.

### wellness-blog-genesis-longevity.html (wellness, 198.6KB)
*Title: GENESIS™ Longevity Programme Ballito | Maddog Wellness*

- INFO: "Maddog Performance Institute" appears on this page — checked, looks like a legitimate cross-business reference (event location, footer link, etc.), not a self-identity bug — verify if unsure

### wellness-blog-womens-self-defence.html (wellness, 124.2KB)
*Title: Women's Wellness Day Ballito | Self-Defence &amp; Recovery*

- INFO: "Maddog Performance Institute" appears on this page — checked, looks like a legitimate cross-business reference (event location, footer link, etc.), not a self-identity bug — verify if unsure

### wellness-blog-womens-wellness-day-recap.html (wellness, 31.2KB)
*Title: Women's Wellness Day Ballito: Event Recap | Maddog Wellness*

- INFO: "Maddog Performance Institute" appears on this page — checked, looks like a legitimate cross-business reference (event location, footer link, etc.), not a self-identity bug — verify if unsure

### wellness-blog.html (wellness, 881.5KB)
*Title: Wellness Insights &amp; FAQ | Maddog Health &amp; Wellness*

- INFO: "Maddog Performance Institute" appears on this page — checked, looks like a legitimate cross-business reference (event location, footer link, etc.), not a self-identity bug — verify if unsure
- INFO: Page is 881.5KB — on the larger side, worth checking for embedded base64 images

### wellness-body.html (wellness, 728.6KB)
*Title: Slimming Clinic Ballito | InBody &amp; Peptide Therapy*

- **WARNING**: 1 of 6 <img> tags have empty/missing alt text (some empty alt may be intentionally decorative — verify)
- INFO: "Maddog Performance Institute" appears on this page — checked, looks like a legitimate cross-business reference (event location, footer link, etc.), not a self-identity bug — verify if unsure

### wellness-cold-plunge-ballito.html (wellness, 434.8KB)
*Title: Ice Bath Ballito | Cold Plunge Recovery Therapy*

- **WARNING**: 1 of 4 <img> tags have empty/missing alt text (some empty alt may be intentionally decorative — verify)
- INFO: "Maddog Performance Institute" appears on this page — checked, looks like a legitimate cross-business reference (event location, footer link, etc.), not a self-identity bug — verify if unsure

### wellness-contact.html (wellness, 48.1KB)
*Title: Contact Us | Maddog Health &amp; Wellness | Ballito KZN*

- INFO: "Maddog Performance Institute" appears on this page — checked, looks like a legitimate cross-business reference (event location, footer link, etc.), not a self-identity bug — verify if unsure

### wellness-inbody-scan-ballito.html (wellness, 223.8KB)
*Title: InBody Scan Ballito | Body Composition Testing*

- **WARNING**: 1 of 4 <img> tags have empty/missing alt text (some empty alt may be intentionally decorative — verify)
- INFO: "Maddog Performance Institute" appears on this page — checked, looks like a legitimate cross-business reference (event location, footer link, etc.), not a self-identity bug — verify if unsure

### wellness-infrared-sauna-ballito.html (wellness, 346.4KB)
*Title: Infrared Sauna Ballito | Recovery &amp; Wellness*

- **WARNING**: 1 of 4 <img> tags have empty/missing alt text (some empty alt may be intentionally decorative — verify)
- INFO: "Maddog Performance Institute" appears on this page — checked, looks like a legitimate cross-business reference (event location, footer link, etc.), not a self-identity bug — verify if unsure

### wellness-iv.html (wellness, 283.4KB)
*Title: IV Drip Therapy Ballito | Myers Cocktail, NAD+ &amp; More*

- **WARNING**: 1 of 4 <img> tags have empty/missing alt text (some empty alt may be intentionally decorative — verify)
- INFO: "Maddog Performance Institute" appears on this page — checked, looks like a legitimate cross-business reference (event location, footer link, etc.), not a self-identity bug — verify if unsure

### wellness-nad-iv-ballito.html (wellness, 315.5KB)
*Title: NAD+ IV Therapy Ballito | Longevity &amp; Anti-Ageing*

- **WARNING**: 1 of 4 <img> tags have empty/missing alt text (some empty alt may be intentionally decorative — verify)
- INFO: "Maddog Performance Institute" appears on this page — checked, looks like a legitimate cross-business reference (event location, footer link, etc.), not a self-identity bug — verify if unsure

### wellness-personal-training-ballito.html (wellness, 1137.1KB)
*Title: Strength &amp; Nutrition Coaching Ballito | Maddog Wellness*

- INFO: "Maddog Performance Institute" appears on this page — checked, looks like a legitimate cross-business reference (event location, footer link, etc.), not a self-identity bug — verify if unsure
- INFO: Page is 1137.1KB — on the larger side, worth checking for embedded base64 images

### wellness-physiotherapy-ballito.html (wellness, 952.1KB)
*Title: Sports Physiotherapy Ballito | Injury Assessment &amp; Rehab*

- **WARNING**: 1 of 9 <img> tags have empty/missing alt text (some empty alt may be intentionally decorative — verify)
- INFO: "Maddog Performance Institute" appears on this page — checked, looks like a legitimate cross-business reference (event location, footer link, etc.), not a self-identity bug — verify if unsure
- INFO: Page is 952.1KB — on the larger side, worth checking for embedded base64 images

### wellness-pricing.html (wellness, 127.2KB)
*Title: Wellness Pricing Ballito | IV Therapy &amp; Recovery*

- **WARNING**: 1 of 3 <img> tags have empty/missing alt text (some empty alt may be intentionally decorative — verify)
- INFO: "Maddog Performance Institute" appears on this page — checked, looks like a legitimate cross-business reference (event location, footer link, etc.), not a self-identity bug — verify if unsure

### wellness-recovery.html (wellness, 380.9KB)
*Title: Contrast Therapy Ballito | Cold Plunge &amp; Infrared Sauna*

- **WARNING**: 1 of 4 <img> tags have empty/missing alt text (some empty alt may be intentionally decorative — verify)
- INFO: "Maddog Performance Institute" appears on this page — checked, looks like a legitimate cross-business reference (event location, footer link, etc.), not a self-identity bug — verify if unsure

### wellness.html (wellness, 3503.2KB)
*Title: Wellness Clinic Ballito | IV Drip, Recovery &amp; Slimming*

- **WARNING**: 11 of 38 <img> tags have empty/missing alt text (some empty alt may be intentionally decorative — verify)
- **WARNING**: Page is 3503.2KB (3.4MB) — this is a real Core Web Vitals (LCP) risk, which is a confirmed Google ranking factor, not just a "nice to have" performance note. A page this size is very likely failing Google's "good" LCP threshold (<2.5s) on mobile. Base64-embedded images can't be cached separately from the HTML, so every visit re-downloads everything. See the aggregate "Performance / Core Web Vitals risk" section at the top of this report — this is not something to leave sitting as a routine warning.
- INFO: "Maddog Performance Institute" appears on this page — checked, looks like a legitimate cross-business reference (event location, footer link, etc.), not a self-identity bug — verify if unsure

## Clean pages (no findings)

wellness-blog-cold-plunge.html, wellness-blog-iv-therapy.html, wellness-blog-physiotherapy.html
