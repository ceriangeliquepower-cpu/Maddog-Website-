---
name: maddog-seo-audit
description: Run a site-wide SEO health check across both Maddog sites (Performance Institute gym + Performance Health & Wellness) — checks every page against CLAUDE.md's SEO rules, sitemap coverage, brand-name consistency between the two businesses, and schema completeness. Use when the user asks to "check our SEO", "run an SEO audit", "site health check", references "SEO Round 2", or wants to know what's missing/broken across the site. Not for a single new blog post — that's covered by each blog skill's own pre-publish checklist.
---

# Maddog SEO Audit

Read-only site-wide scan. Never modifies a live page — only reads pages and writes a new report file. Covers both businesses in one pass (gym pages and wellness pages need different checks in a few places — different LocalBusiness schema type, different canonical brand name — the script already knows the difference).

## 1. Run the scan

```bash
py .claude/skills/maddog-seo-audit/scripts/audit_pages.py
```

Takes no arguments, scans every top-level `.html` file in the project root (skipping `*-TEMPLATE.html` files, which aren't live pages). Writes the full findings to `seo-audit-report.md` in the project root and prints a short summary — total counts, sitemap gaps, and the top ~15 critical findings — to the terminal.

Safe to re-run any time; it overwrites `seo-audit-report.md` each run and never touches the pages it's scanning.

## 2. Sanity-check findings before reporting them as fact

The script is a set of pattern-matching heuristics, not a real HTML/schema validator — it will occasionally be wrong. Two known false-positive shapes were already found and fixed during development (training-page sitemap URLs use a `/training/...` redirect rewrite the script now accounts for; a stylized nav logo reading "MADDOG" is excluded from the brand-name check since that's a wordmark, not body copy). But new false positives are possible, especially around:

- **Internal link / alt-text counts** — these are regex approximations, not a real DOM parse. If a finding here looks surprising, open the actual page section it's about (via `Grep`, not a bulk `Read` — see §3) and confirm before reporting it to the user as fact.
- **File size warnings** — flags pages over 2MB (warning) or 800KB (info) as likely base64-bloated. This is a real performance/SEO concern (page speed is a ranking factor), but fixing it is a separate, larger job (migrating embedded images to `images/` file references) — don't treat "flagged as oversized" as something to fix inline during an audit read-out.
- **"Wellness page identifies as [gym name]"** — checks JSON-LD `name`/`author` fields and meta `content=` attributes specifically, not just any mention of the gym's name (the wellness footer legitimately links back to the gym site — "Maddog Performance (Main Site)" — that's intentional cross-linking, not a bug, and the check is scoped to avoid flagging it). If this fires, it means the wrong business's name ended up in structured data or a meta tag, which does need fixing.

## 3. Investigating a specific finding further

Several scanned pages are large, base64-heavy files (`events.html` ~3MB, `index.html` ~4.8MB, `wellness.html` ~3.3MB, `wellness-blog.html` ~900KB) — the same files the blog-creation skills already learned to never bulk-`Read`. If you need to look closer at a finding on one of these pages, use `Grep` with context lines (which auto-truncates long matched lines) rather than `Read`, exactly as documented in `maddog-new-blog-post`'s SKILL.md §6. Smaller individual pages (most blog posts, service pages) are safe to `Read` normally.

## 4. Presenting results

The user is non-technical — translate findings into plain language, not jargon. Group by what actually matters to them:

- **Critical** findings are things actively broken or wrong (missing schema entirely, wrong business name in structured data, a real brand-spelling mistake in visible copy) — these are worth fixing.
- **Warning** findings are real but lower-stakes (meta description a bit long, a missing OG tag) — worth batching into a cleanup pass, not urgent.
- **Info** findings are things to sanity-check, not necessarily fix (large file size, an ambiguous brand-name match, a cross-site link worth confirming is intentional).

Don't dump the raw report file at the user — summarize the shape of it (counts, the handful of findings that actually need a decision from them) and offer to read out or act on specific ones. If they want to act on a finding, that's a separate, deliberate edit — this skill only diagnoses, it doesn't fix anything automatically.

## 5. What's actually checked

See `reference/rules.md` for the full list of checks and which CLAUDE.md rule each one traces back to — useful if a finding needs justifying, or if CLAUDE.md's SEO rules change and the script needs updating to match.
