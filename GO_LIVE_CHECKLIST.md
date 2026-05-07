# Maddog Performance Institute — Go-Live Checklist

Everything on this list must be completed before the site goes live under `maddogperformance.co.za`.

---

## 1. FORMSPREE — Assessment Form Emails

**What it does:** Connects the Recovery Assessment form on `pricing.html` to the gym's inbox. When a client submits the form, an email lands at info@maddogperformance.co.za automatically.

**Cost:** Free (up to 50 submissions/month on free plan)

**Steps to activate:**
1. Go to [formspree.io](https://formspree.io) and create a free account
2. Create a new form — name it "Maddog Recovery Assessment"
3. Set the notification email to: **info@maddogperformance.co.za**
4. Copy your Form ID (looks like: `xyzabcde`)
5. Tell Claude: "My Formspree ID is `xyzabcde`"
6. Claude replaces `YOUR_FORM_ID` in `pricing.html` with your real ID — done

**File to update:** `pricing.html`
**Current placeholder:** `action="https://formspree.io/f/YOUR_FORM_ID"`

---

## 2. PAYFAST — Online Payment Buttons

**What it does:** Allows clients to pay for recovery protocols (IV drips, contrast sessions, etc.) directly from the pricing page. Redirects to PayFast's secure hosted checkout.

**Cost:** R99/month + ~3.5% + R2 per transaction

**Supported payment methods:** Visa, Mastercard, Instant EFT, SnapScan, Zapper, Mobicred

**Steps to activate:**
1. Confirm with the client: **Do they want PayFast on the site? Do they already have a PayFast merchant account?**
2. If no account: register at [payfast.co.za](https://www.payfast.co.za) — takes ~2 business days to verify
3. Once account is active, share with Claude:
   - Merchant ID
   - Merchant Key
   - Whether to use sandbox (test) or live mode
4. Claude builds the PayFast payment buttons for each protocol with correct amounts
5. Test all buttons in sandbox mode before going live

**Protocols that will have Pay Now buttons:**
- IV Drip Therapy (per protocol — Hydrate R865, Recover R1080, etc.)
- Contrast Therapy sessions
- Slimming Clinic consultations
- InBody tests

**Protocols that stay as Enquire Only (no payment button):**
- Peptide Therapy (requires consultation first)
- Athlete Memberships (requires consultation first)
- NAD+ packages (via consultation)

**File to update:** `pricing.html`
**Current state:** Placeholder "Book & Reserve Your Session" buttons with `<!-- PAYFAST INTEGRATION NOTE -->` comments throughout

---

## 3. SITEMAP.XML — Search Engine Visibility

**What it does:** Tells Google every page on the site so all pages get indexed and appear in search results.

**Current sitemap is missing:**
- `pricing.html` (new page)
- All 7 blog pages

**Steps to activate:**
1. Tell Claude: "Update the sitemap"
2. Claude adds all missing pages to `sitemap.xml` with correct `<lastmod>` dates
3. Once domain is live, submit sitemap to Google Search Console at: `https://www.maddogperformance.co.za/sitemap.xml`

**File to update:** `sitemap.xml`

---

## 4. DNS — Pointing the Domain to the Hosting Platform

**What it does:** Makes `maddogperformance.co.za` load your website instead of showing a blank page or error.

**The client already has the domain.** It just needs to be pointed at Netlify or Vercel.

**Decision needed first:** Netlify or Vercel? (Recommendation: Netlify — better for this site)

**Steps for Netlify:**
1. Log into Netlify dashboard
2. Go to Site Settings → Domain Management → Add custom domain
3. Type: `maddogperformance.co.za`
4. Netlify will show you two DNS records to add (an A record and a CNAME)
5. Log into the domain registrar (wherever the domain was purchased — e.g. Afrihost, Domains.co.za, GoDaddy)
6. Add those two records in the DNS settings
7. Wait 15 minutes to 24 hours for propagation
8. Netlify automatically issues a free SSL certificate (the padlock in the browser)

**Steps for Vercel:**
1. Log into Vercel dashboard → Project Settings → Domains
2. Add `maddogperformance.co.za`
3. Vercel provides DNS records — add them at your domain registrar
4. SSL is handled automatically

**Important:** Once the domain is live, the Formspree form login (OAuth) will work properly — this is a prerequisite for CMS setup.

---

## 5. CMS — Content Management System

**What it does:** Gives the Maddog team a login panel at `maddogperformance.co.za/admin` where they can update blog posts, prices, fighter records, and events — without touching code.

**Prerequisite:** DNS must be live first (domain must be pointing to the hosting platform).

**Recommended approach:** Netlify CMS (free, built into Netlify)

**What the CMS will manage:**
- Blog posts (add new articles, edit existing)
- Upcoming events
- Fighter records and bios
- Prices (if set up as editable fields)

**Steps to activate:**
1. DNS must be live (see step 4 above)
2. Tell Claude: "Ready to set up the CMS"
3. Claude configures Netlify CMS in one session:
   - Adds `admin/index.html` and `admin/config.yml` to the project
   - Sets up collections for blogs, events, fighters
   - Configures Netlify Identity for secure login
4. Team member logs in at `maddogperformance.co.za/admin`
5. Full content management — no coding required

**Cost:** Free on Netlify

---

## 6. SISTER AMANDA KOBUS PHOTO

**What it does:** Her professional photo appears on the clinician card on `pricing.html`.

**Steps:**
1. Open `pricing.html` from the Desktop folder
2. Find the clinician section — there is a dark photo slot labelled "Upload Sister Amanda's Photo"
3. Click the slot — upload her photo
4. Click "Save & Download Page" (gold banner at bottom)
5. Replace the `pricing.html` file in the Desktop folder with the downloaded file

**Her SANC registration number** is also still a placeholder `[To be updated]` in both `pricing.html` and `recovery.html`.

---

## 7. CONTENT STILL AWAITING FROM CLIENT

These are gaps in the site content that need real information before going live:

| Item | Page | Status |
|------|------|--------|
| Amanda's 6 remaining pro fight results | `amanda.html` | Awaiting client |
| Coach credentials — Lucky, Winston, Tristan | `coaches.html` | Awaiting client |
| Sister Amanda Kobus SANC registration number | `pricing.html`, `recovery.html` | Awaiting client |
| Training prices (18 slots showing POA) | `training.html` | Awaiting client |
| Upcoming event venues + ticket links | `events.html` | Awaiting client |
| PayFast merchant account confirmation | `pricing.html` | Awaiting client decision |

---

## RECOMMENDED GO-LIVE ORDER

| Step | Action | Who |
|------|--------|-----|
| 1 | Upload Sister Amanda's photo on pricing.html | You |
| 2 | Create Formspree account + give ID to Claude | You + Claude |
| 3 | Update sitemap.xml | Claude |
| 4 | Fill in outstanding client content (table above) | Client |
| 5 | Confirm PayFast decision | Client |
| 6 | Point DNS to Netlify/Vercel | You + domain registrar |
| 7 | Test all pages on live domain | You + Claude |
| 8 | Set up CMS | Claude |
| 9 | Activate PayFast buttons (if confirmed) | Claude |
| 10 | Submit sitemap to Google Search Console | You |

---

*Last updated: May 2026*
*Maintained by Claude Code — Maddog Performance Institute project*
