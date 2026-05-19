# Maddog Performance Institute — Go-Live Guide

> Everything you need to do when you're ready to point the domain and launch all three platforms live.
> Complete these steps in order.

---

## What You Have

| Platform | What it is | Current URL |
|----------|-----------|-------------|
| **Website** | Static HTML site (13 pages) | Netlify preview only |
| **Client Portal** | Member app — bookings, check-in, profile | `maddog-client-portal.vercel.app` |
| **Admin Control Centre** | Staff dashboard — bookings, members, deals | `maddog-control-centre.vercel.app` |

**Target URLs after go-live:**

| Platform | Live URL |
|----------|----------|
| Website | `https://www.maddogperformance.co.za` |
| Client Portal | `https://portal.maddogperformance.co.za` |
| Admin | `https://admin.maddogperformance.co.za` |

---

## Hosting Decision — Netlify (Website) + Vercel (Backend & Apps)

**Recommendation: Keep the website on Netlify (free) and the backend + client app on Vercel (paid).**

| Platform | Hosts | Cost |
|----------|-------|------|
| **Netlify** | Website only (static HTML) | Free — commercial use allowed |
| **Vercel Pro** | Backend + Client Portal + Admin Control Centre | ~R370/month ($20 USD) |
| **Supabase** | Database (bookings, members, services) | Free to start — upgrade when needed (~R460/month) |
| **Domain renewal** | maddogperformance.co.za | ~R150–200/year |
| **Total to launch** | | **~R370/month** |
| **Total when scaling** | | **~R830/month** |

### Why not put everything on Vercel?
You can — but the website is pure HTML with zero compute, so paying for Vercel Pro just to host it adds no benefit. Netlify's free tier is excellent and explicitly allows commercial static sites.

### Want to switch the website to Vercel later?
**Easy. Zero downtime. 15 minutes.**
1. Connect the GitHub repo to Vercel (click Import Project)
2. Add `maddogperformance.co.za` as a custom domain in Vercel
3. Create a `vercel.json` file in the repo (Claude does this — just ask)
4. Update 2 DNS records at the registrar
5. Delete the site from Netlify

DNS propagation is gradual — traffic shifts slowly, the site is never down.

### Will backend changes show on the website if they're on different platforms?
**Yes — the browser handles all connections, not the servers.**

When someone opens the booking page their browser:
- Loads the HTML from Netlify
- Queries Supabase directly for services/prices (updates instantly)
- Calls Vercel backend functions for payments (PayFast ITN etc.)

Netlify and Vercel never talk to each other. The only requirement is that your Vercel backend has **CORS configured** to allow requests from `maddogperformance.co.za` — one line of config your backend developer adds when setting up the API.

| Type of change | Reflects on website? |
|----------------|----------------------|
| Price updated in Supabase | ✅ Instantly — no deployment needed |
| New service added in Supabase | ✅ Instantly |
| Backend logic updated on Vercel | ✅ Instantly |
| New HTML page or content change | Push to GitHub → live in 60 seconds |

---

## Step 1 — Point the Website to Netlify

Do this in your **domain registrar** (wherever you bought `maddogperformance.co.za` — GoDaddy, Namecheap, Afrihost, etc.)

Add these DNS records:

| Type | Name | Value |
|------|------|-------|
| A | `@` | `75.2.60.5` |
| CNAME | `www` | `stellar-biscochitos-7f6a1c.netlify.app` |

Then in **Netlify**:
1. Go to your site → **Domain settings**
2. Click **Add custom domain**
3. Enter `maddogperformance.co.za` and `www.maddogperformance.co.za`
4. Netlify will auto-provision an SSL certificate (free HTTPS)

> DNS propagation takes 15 minutes to 24 hours. Usually under 1 hour.

---

## Step 2 — Add Custom Domain for the Client Portal

**In Vercel:**
1. Log in at [vercel.com](https://vercel.com)
2. Click the **maddog-client-portal** project
3. Go to **Settings → Domains**
4. Type `portal.maddogperformance.co.za` → click **Add**
5. Vercel will show you a CNAME record — it will say something like `cname.vercel-dns.com`

**In your domain registrar DNS:**

| Type | Name | Value |
|------|------|-------|
| CNAME | `portal` | `cname.vercel-dns.com` |

6. Go back to Vercel → wait for the green **Valid Configuration** tick
7. Vercel auto-provisions SSL — portal is now live at `https://portal.maddogperformance.co.za`

---

## Step 3 — Add Custom Domain for the Admin Control Centre

**In Vercel:**
1. Click the **maddog-control-centre** project
2. Go to **Settings → Domains**
3. Type `admin.maddogperformance.co.za` → click **Add**

**In your domain registrar DNS:**

| Type | Name | Value |
|------|------|-------|
| CNAME | `admin` | `cname.vercel-dns.com` |

4. Wait for the green **Valid Configuration** tick in Vercel

---

## Step 4 — Tell Claude to Update the Check-In URL (CODE CHANGE)

Once `portal.maddogperformance.co.za` is confirmed live, send this message to Claude:

> "The portal is now live at portal.maddogperformance.co.za — please update the check-in URL in the code and push to GitHub."

Claude will change one line in `Dashboard.jsx` from:
```
https://maddog-client-portal.vercel.app/checkin
```
to:
```
https://portal.maddogperformance.co.za/checkin
```

⚠️ **Do NOT print or install the gym QR code until this step is done.** The QR code URL must match the live domain.

---

## Step 5 — Generate and Install the Gym QR Code

After Step 4 is done and the code is pushed:

1. Go to any free QR generator — e.g. [qr-code-generator.com](https://www.qr-code-generator.com)
2. Enter the URL: `https://portal.maddogperformance.co.za/checkin`
3. Download as SVG or high-res PNG
4. Print and mount in the gym — near the entrance or front desk

Members scan it → they're auto-checked in instantly (as long as they're logged into the portal app).

---

## Step 6 — Switch PayFast to Live Credentials

Currently the payment system uses PayFast **sandbox** (test mode). Before taking real payments you must swap these credentials.

**Where to get your live credentials:**
1. Log in to your PayFast merchant account at [payfast.io](https://www.payfast.io)
2. Go to **Settings → Integration** → copy your live:
   - Merchant ID
   - Merchant Key
   - Passphrase

**Tell Claude:**
> "Here are my live PayFast credentials — Merchant ID: XXXX, Merchant Key: XXXX, Passphrase: XXXX. Please update the payment code and push to GitHub."

Claude will update `/api/payfast-payment.js` and `/api/payfast-notify.js` with your live credentials.

⚠️ Test one real payment after switching to confirm the full flow works (booking → PayFast → confirmation → Supabase updated).

---

## Step 7 — Claim Your Google Business Profile

This is the **single biggest local SEO action** you can take. Do it immediately after DNS is live.

1. Go to [business.google.com](https://business.google.com)
2. Search for "Maddog Performance Institute Ballito"
3. Claim the listing (you'll need to verify via phone or postcard)
4. Fill in:
   - Business name: **Maddog Performance Institute**
   - Category: **Martial arts school** + **Gym** + **Wellness centre**
   - Address: 22 Sandra Road, Balvista Centre, Ballito, KZN
   - Phone: +27 63 442 1690
   - Website: `https://www.maddogperformance.co.za`
   - Hours: Mon–Thu 05:30–20:00 / Fri 05:30–18:00 / Sat 07:00–13:00 / Sun Closed
5. Add photos (exterior, gym floor, recovery suite)
6. Ask your first 10 members to leave Google reviews — this is critical for ranking

---

## Step 8 — Submit to Google Search Console

1. Go to [search.google.com/search-console](https://search.google.com/search-console)
2. Add property → enter `https://www.maddogperformance.co.za`
3. Verify ownership (add the TXT record Google gives you to your DNS — same place you did Step 1)
4. Go to **Sitemaps** → submit: `https://www.maddogperformance.co.za/sitemap.xml`

Google will start crawling and indexing all 13 pages within 24–72 hours.

---

## Post-Launch Checklist

- [ ] Step 1 — Website DNS pointing to Netlify
- [ ] Step 2 — `portal.maddogperformance.co.za` live on Vercel
- [ ] Step 3 — `admin.maddogperformance.co.za` live on Vercel
- [ ] Step 4 — Check-in URL updated in code (Claude does this)
- [ ] Step 5 — Gym QR code printed and installed
- [ ] Step 6 — PayFast switched to live credentials
- [ ] Step 7 — Google Business Profile claimed and filled
- [ ] Step 8 — Google Search Console connected + sitemap submitted

---

## Ongoing After Launch

| Task | Who |
|------|-----|
| Upload practitioner photos | Admin → Control Centre → Practitioners |
| Add member profiles | Admin → Control Centre → Members |
| Add/manage services | Admin → Control Centre → Bookings → Services |
| Create deals | Admin → Control Centre → Deals |
| Add Amanda's remaining fight results | Claude (provide opponent, event, method, round, result) |
| Add coach credentials (Lucky, Winston, Tristan) | Claude (provide the text) |
| Confirm training prices (18 slots showing POA) | Decide: publish or keep as enquire |
| SEO Round 2 | Claude — AggregateRating schema, BreadcrumbList, internal links |

---

## Key Credentials & Accounts to Have Ready

| What | Where |
|------|-------|
| Domain registrar login | Wherever you bought `maddogperformance.co.za` |
| Netlify login | [netlify.com](https://netlify.com) |
| Vercel login | [vercel.com](https://vercel.com) |
| Supabase login | [supabase.com](https://supabase.com) — project: mthjfihctiluqllpegnr |
| PayFast merchant account | [payfast.io](https://www.payfast.io) |
| GitHub login | [github.com/ceriangeliquepower-cpu](https://github.com/ceriangeliquepower-cpu) |
| Google account (for Search Console + Business) | Any Google account you control |

---

*Guide last updated: May 2026. Contact Claude Code with any questions — provide this file for context.*
