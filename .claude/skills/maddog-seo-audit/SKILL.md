---
name: maddog-seo-audit
description: Run a site-wide SEO health check across both Maddog sites (Performance Institute gym + Performance Health & Wellness) — checks every page against CLAUDE.md's SEO rules, sitemap coverage, brand-name consistency between the two businesses, schema completeness, AND live-tests every `_redirects` rule against the real production domain (catches redirects that are committed but silently not working — see CLAUDE.md Hard-Won Rule #9). Use when the user asks to "check our SEO", "run an SEO audit", "site health check", "check the redirects", "check indexing", references "SEO Round 2", or wants to know what's missing/broken across the site — including after adding any new page or touching `_redirects`, per CLAUDE.md's "After Adding Any New Page" section. Not for a single new blog post — that's covered by each blog skill's own pre-publish checklist.
---

# Maddog SEO Audit

Read-only site-wide scan. Never modifies a live page — only reads pages and writes a new report file. Covers both businesses in one pass (gym pages and wellness pages need different checks in a few places — different LocalBusiness schema type, different canonical brand name — the script already knows the difference).

## 1. Run the scan

```bash
py .claude/skills/maddog-seo-audit/scripts/audit_pages.py
```

Scans every top-level `.html` file in the project root (skipping `*-TEMPLATE.html` files, which aren't live pages), plus **live-tests every `_redirects` rule** and **every internal `<a href>` link** against the real production domain (`https://www.maddogperformance.co.za`) — not just checking the file/markup exists, actually requesting each URL and confirming it does what it's supposed to. Writes the full findings to `seo-audit-report.md` in the project root and prints a short summary — total counts, sitemap gaps, and the top ~15 critical findings — to the terminal.

Safe to re-run any time; it overwrites `seo-audit-report.md` each run and never touches the pages it's scanning. Takes ~20-25s (the live checks run in parallel, but there's more of them now). Add `--skip-live` to skip the network calls (offline, or if you just need the static page checks).

There are two fast standalone modes for scripting/hooks, neither writes the report file:
- `--check-redirects` — only the live redirect check (~5-10s).
- `--check-critical` — every check (pages + sitemap + robots + live redirects + live internal links), but only CRITICAL-severity findings are printed/considered (warnings/info need human judgment, not something a hook should block on) — exits nonzero if anything critical is found. Takes ~15-25s.

The repo's `hooks/pre-push` hook calls `--check-critical` automatically on **every push** (not conditional on which files changed — the point is nothing slips through, not just redirects). One-time setup per clone: `git config core.hooksPath hooks`. See CLAUDE.md Hard-Won Technical Rule #9 and the "After Adding Any New Page" section for the full story.

## 2. Sanity-check findings before reporting them as fact

The script is a set of pattern-matching heuristics, not a real HTML/schema validator — it will occasionally be wrong. Two known false-positive shapes were already found and fixed during development (training-page sitemap URLs use a `/training/...` redirect rewrite the script now accounts for; a stylized nav logo reading "MADDOG" is excluded from the brand-name check since that's a wordmark, not body copy). But new false positives are possible, especially around:

- **Alt-text counts** — regex approximations, not a real DOM parse. If a finding here looks surprising, open the actual page section it's about (via `Grep`, not a bulk `Read` — see §3) and confirm before reporting it to the user as fact. (Internal *link resolution* — whether a link's target actually returns 200 — is no longer a regex approximation; it's a real live HTTP check, see below.)
- **File size warnings — do NOT treat these as routine.** Flags pages over 2MB as a **Core Web Vitals / Google ranking risk** (LCP is a confirmed ranking factor), surfaced in its own top-of-report "Performance / Core Web Vitals risk" section and in the stdout summary — not buried as one of many per-page warnings. This used to be under-communicated (labeled as a generic "warning, batch it later" item) and that was wrong; a 3-7MB page is a real, current ranking problem, not a someday cleanup task. It's still not something the pre-push hook auto-blocks on, because fixing it site-wide means deciding whether to move off base64-inline images — an architecture call for the user to make deliberately, not something to silently force via a failing push.
- **"Wellness page identifies as [gym name]"** — checks JSON-LD `name`/`author` fields and meta `content=` attributes specifically, not just any mention of the gym's name (the wellness footer legitimately links back to the gym site — "Maddog Performance (Main Site)" — that's intentional cross-linking, not a bug, and the check is scoped to avoid flagging it). If this fires, it means the wrong business's name ended up in structured data or a meta tag, which does need fixing.

## 3. Investigating a specific finding further

Several scanned pages are large, base64-heavy files (`events.html` ~3MB, `index.html` ~4.8MB, `wellness.html` ~3.3MB, `wellness-blog.html` ~900KB) — the same files the blog-creation skills already learned to never bulk-`Read`. If you need to look closer at a finding on one of these pages, use `Grep` with context lines (which auto-truncates long matched lines) rather than `Read`, exactly as documented in `maddog-new-blog-post`'s SKILL.md §6. Smaller individual pages (most blog posts, service pages) are safe to `Read` normally.

## 4. Presenting results

The user is non-technical — translate findings into plain language, not jargon. Group by what actually matters to them:

- **Critical** findings are things actively broken or wrong (missing schema entirely, wrong business name in structured data, a real brand-spelling mistake in visible copy, a broken redirect, a 404'ing internal link) — these are worth fixing.
- **Warning** findings are usually lower-stakes (meta description a bit long, a missing OG tag) and fine to batch into a cleanup pass — **except the "Performance / Core Web Vitals risk" section**, which is also a warning-severity finding but is NOT lower-stakes: it's a real, current Google ranking factor. Always call this out explicitly and separately when presenting results, don't let it blend into "the usual warnings, nothing urgent."
- **Info** findings are things to sanity-check, not necessarily fix (an ambiguous brand-name match, a cross-site link worth confirming is intentional).

Don't dump the raw report file at the user — summarize the shape of it (counts, the handful of findings that actually need a decision from them) and offer to read out or act on specific ones. If they want to act on a finding, that's a separate, deliberate edit — this skill only diagnoses, it doesn't fix anything automatically.

## 5. What's actually checked

See `reference/rules.md` for the full list of checks and which CLAUDE.md rule each one traces back to — useful if a finding needs justifying, or if CLAUDE.md's SEO rules change and the script needs updating to match.
