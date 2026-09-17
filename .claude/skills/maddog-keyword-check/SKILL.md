---
name: maddog-keyword-check
description: Check how Maddog actually ranks in Google for its target search terms — organic position, AI Overview mentions, and Local Map Pack position — via live Google searches in the Browser pane, cross-referenced against real Search Console demand data. Also covers extracting competitors' own target keywords (title/meta/headings/sitemap) directly from their sites — free, no Keyword Planner/Ahrefs access needed. Use when the user asks "how do we rank for X", "check our keyword rankings", "run the keyword check", "what keywords are competitors using", wants to add new keywords or competitors to track, or asks what people are actually searching for. Not for finding NEW keyword ideas from scratch (that's ordinary research) — this is for re-running the established process against the tracked list in reference/keyword-list.md and reference/competitors.md.
---

# Maddog Keyword Rank Check

Live-search-driven process (no script — this needs a real Google search and a real Search Console session, both via the Browser pane). Two parts: (1) live-search rank checking, (2) real-demand cross-reference against Search Console. Always do both — they answer different questions and the second one has repeatedly overturned assumptions from the first.

## 1. The candidate keyword list

Lives in `reference/keyword-list.md`, grouped by discipline/category. This is the source of truth — when the user gives you new terms to track, add them there first (in the matching category, following the existing lower-case phrasing style), then check only the new ones rather than re-running everything, unless the user asks for a full re-run.

## 2. Live-search rank check (organic / AI Overview / Map Pack)

For each term, navigate the Browser pane to `https://www.google.com/search?q=<term with +>` and read the page text. Batch 3-4 searches per `browser_batch` call (navigate + get_page_text, repeated) — this is far more efficient than one call per search.

For each result, extract:
- **Organic rank** — the position of any `maddogperformance.co.za` URL in the plain web results (ignore Instagram/Facebook/Fresha listings when judging Maddog's own rank, but note strong non-Maddog competitors that outrank it).
- **AI Overview** — if Google shows an AI Overview block, does it name Maddog specifically? Note which competitors it names alongside, if any.
- **Local Map Pack** — if a "Local results / Places / Map" block appears, what position is Maddog's GBP in (look for "You manage this Business Profile" to identify it), and who's ahead of it?

**Known caveat — always state this when reporting results:** AI Overviews and Map Packs do not trigger consistently. Re-running the identical query minutes apart can show/hide them, because both are sensitive to the searcher's geolocation and this Browser pane has no stable Ballito GPS signal (it's a cloud environment). Treat "not shown" as "not reliably tested here," not "confirmed absent" — if anything, the user's own phone searches are a more trustworthy signal for local/Maps visibility than this tool's checks. Similarly, generic "near me" queries (no "ballito" in the term) consistently resolve to Durban/Umhlanga businesses in this environment — that's this session's location inference, not necessarily what a phone physically in Ballito would see. Organic rank is the most trustworthy of the three signals since it's the least location-personalized.

## 3. Cross-reference against real Search Console demand

This is the step that matters most and is easy to skip — don't skip it. A term ranking #1 in step 2 can still have zero real searchers behind it; GSC's query list is the only way to know.

1. Navigate to `https://search.google.com/search-console/performance/search-analytics?resource_id=https%3A%2F%2Fwww.maddogperformance.co.za%2F` (this is a **URL-prefix property**, not a domain property — using `sc-domain:maddogperformance.co.za` as the resource_id fails with "you don't have access to this property"; if that happens, navigate to `https://search.google.com/search-console` first, read the account's actual resource_id from the page links, and use that).
2. Switch to the **Queries** tab (should be default), open the "Rows per page" control near the bottom and select **500** so the whole table loads in one page — the query for row-count is a listbox, not a native `<select>`, so `form_input` fails on it; click it open then click the "500" option.
3. Run `get_page_text` — this returns all ~400+ rows as one long concatenated string (`query` + `clicks` + `impressions` + `CTR%` + `position`, no delimiters between fields, so read numbers carefully — e.g. `boxing gym ballito4508%1.7` = clicks 4, impressions 50, CTR 8%, position 1.7).
4. Cross-reference every term in `reference/keyword-list.md` against this table. Most will have **zero rows** — that's expected and important, not a bug: it means nobody searched that exact phrase in the last 3 months, regardless of how well Maddog would rank if they did.
5. Separately note the genuine **top real queries** in the table (highest impressions/clicks) even if they weren't on the candidate list — this has repeatedly surfaced real opportunities the hypothesis-driven list missed (e.g. branded terms, the person's own name, short generic "gym ballito"-type phrasing, and even signal for a discipline not yet offered, like early "wrestling gyms near me" impressions before any wrestling content existed).

## 4. Reporting results

Present as a table per category: Keyword | Organic | AI Overview | Map Pack, plus a separate short table for the GSC cross-reference (only terms with real impressions, plus the genuine top queries found along the way). Always restate the geolocation caveat from §2 when Map Pack/AI Overview data is involved. Call out explicitly: (a) any term with strong organic rank but zero real GSC demand — that's a "ranks well, nobody's asking" case, not wasted work, but not where to prioritize further content; (b) any term with real GSC demand but weak position — that's the highest-leverage list, prioritize those.

## 5. Save findings, every time

After presenting results, save them to memory (not just this chat) so the process compounds instead of resetting each session:
- Live-search rank findings → update/append to the `project_keyword_ranking_audit` memory.
- GSC demand cross-reference → update/append to the `project_gsc_real_demand_data` memory.
- If new terms were added to `reference/keyword-list.md`, mention that in the `project_keyword_candidate_list` memory pointer (that memory file should just point here now, not duplicate the list — this skill's reference file is the source of truth).

Update the "Last full run" date at the top of `reference/keyword-list.md` too, so the list's own staleness is visible directly in the repo, not just in memory.

## 6. Competitor keyword extraction (free — no Keyword Planner/Ahrefs needed)

When the user wants to know what keywords a specific competitor is targeting, don't reach for Google Keyword Planner (it shows ideas/volume for your own account, not a competitor's actual targeting, and this project has had repeated access friction with it anyway — see [[feedback...]] in memory if relevant). Instead pull it directly from the competitor's own site, which is free and more accurate:

1. Navigate to the competitor's homepage (or their most relevant service page) and run this in `javascript_tool`:
   ```js
   JSON.stringify({title: document.title, desc: document.querySelector('meta[name="description"]')?.content, h1: [...document.querySelectorAll('h1')].map(e=>e.textContent.trim()), h2: [...document.querySelectorAll('h2')].map(e=>e.textContent.trim())}, null, 1)
   ```
   This reveals exactly what keywords they deliberately chose to target — this same approach replaced repeated failed attempts to get into Google Keyword Planner for competitor research; it's free and gives real targeting data instead of volume estimates for an account that doesn't have any.
2. Navigate to `<their-domain>/sitemap.xml` (or `/sitemap_index.xml`, `/wp-sitemap.xml` for WordPress, or a Wix-style sitemap index with nested sitemaps like `booking-services-sitemap.xml`) and read the URL list — page slugs reveal their full keyword-to-page mapping. If the top-level sitemap is an index, follow it one level down to the actual page/post/service sitemap to get real URLs (a bare index file with no URLs isn't useful on its own).
3. For a site with many individually-named service pages (common on Wix wellness/spa sites), the URL slugs AND image `alt`/title attributes both carry keyword signal — e.g. Kico Life names ice bath pages by exact temperature (`ice-bath-ballito-5-c`, `-10-degrees`, `-12-degrees`) and NAD pages by dose/purpose, which is a real, copyable content-depth pattern.
4. Note the **structural pattern**, not just the keyword list — it's usually more actionable: a single strong benefit-led page (Grit Factory) means their edge is messaging + reviews, beatable with content; a large page-per-service-variant site (Kico Life, CombatCoaching) means their edge is content depth, harder to beat without matching that depth; a franchise template site (F45, Fit24) means their edge is brand/domain authority, not location-specific content.

Tracked competitors (by category) live in `reference/competitors.md` — check there first for what's already been pulled before re-fetching, and add newly-identified competitors there (anyone found beating Maddog on a tracked term during a rank check, per §2, belongs on this list).

Save findings to the relevant project memory (e.g. `project_personal_training_competitor_audit`, or create a new one per category) the same way rank-check results get saved in §5 — this is exactly the kind of finding that's expensive to re-derive and cheap to look up if written down.
