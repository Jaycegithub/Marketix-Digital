# Insights migration: marketixdigital.com.au → dev.marketixdigital.com.au

Per-post detail is in `insights-migration-checklist.csv`. Every exception, with the affected post, is in `migration-exceptions.json`.

## Reconciliation

| | Count |
|---|---|
| Source posts discovered (26 archive pages × 3 per page, cross-checked against category and tag archives and the breadcrumbs) | **76** |
| Posts on dev after migration | **76** (no duplicates, no extra posts) |
| Created | 73 |
| Existing dev posts updated in place (IDs 408, 410, 411: previously Gutenberg-block versions under suffixed slugs) | 3 |
| Skipped / failed | 0 / 0 |
| Images transferred (323 unique; 3 existing dev copies reused after a pixel comparison) | 323 / 323, plus 1 PDF |
| Content check (text ≥ 99.5 % identical; H2/H3/H4, tables, rows, list items, images and bold counts all equal) | 76 / 76 pass |
| Broken dev links or images (62 dev links, 311 images checked) | 0 |

Out of scope: 12 older `/blog/` posts are still in the stale 2024 sitemap but now return 404 on the live site. These are `seo-gurus-are-annoying`, `history-of-seo`, `common-seo-mistakes`, `understanding-entity-seo`, `guaranteed-seo-services`, `what-is-seo-management`, `local-seo-ranking-factors`, `cheap-vs-affordable-seo-services`, `taylor-swift-…`, `how-to-seo-your-tiktok-videos-correctly`, `were-hiring-…` and `addressing-duplicate-content-issues-in-seo`.

## Categories and tags

These were created on dev with the same names and slugs (the source has no parent categories and no descriptions). Counts on dev match the source exactly:

| Term | Posts |
|---|---|
| Category: SEO | 50 |
| Category: Statistics | 16 |
| Category: Press Release | 3 |
| Category: AIO | 1 |
| Category: Report | 1 |
| Category: Research | 1 |
| Tag: SEO | 34 |
| Tag: Statistics | 3 |

Rank Math primary category is set on every categorised post.

4 posts have no category on the live site, so WordPress puts them in **Uncategorized**:
- `tiktok-statistics-…`
- `101-essential-email-statistics-for-businesses`
- `marketix-leaders-quadrant-on-clutch`
- `trending-google-searches-scott-morrison-vs-anthony-albanese-…`

## Fields and limitations

- **Dates:** the source only shows a date (DD.MM.YYYY) with no time, so posts are published at 00:00 on that date. The dev site timezone is UTC, and I didn't change it. The source shows no modified date anywhere, so WordPress's modified date is the same as the publication date.
- **Author:** "Shoaib Mughal" on the source. Dev only has one user, `admin`, so the posts are assigned to it. Creating a user or changing the admin display name would be a site change; it needs your approval.
- **Excerpts:** 28 posts have a manual excerpt on the source and it was migrated. The other 48 have none, so WordPress generates one automatically.
- **SEO (Rank Math):** set per post:
  - SEO title: the exact source `<title>`, including a duplicated "| Marketix Digital" on the pallet-racking post.
  - Meta description.
  - OG title and description.
  - OG image.

  Not migrated, because the source doesn't use them: focus keyword, robots, Twitter fields and post schema (the source schema is site-wide Corporation / LocalBusiness / FAQPage, not per post).
  - **Missing descriptions:** 12 posts have no meta description on the source, so Rank Math generates one. For `b2b-marketing-statistics` that generated description is a blank space.
  - **Social images skipped:** Rank Math ignores 2 OG images below Facebook's 200 px minimum, on `best-online-directories…` and `how-to-write-seo-brief…`.
- **Canonical:** not set, so Rank Math uses each dev URL. The source canonical is recorded in the CSV. The source post `navigating-the-seo-implications-of-site-migrations` has a canonical pointing to its old `/blog/` URL.
- **⚠ Dev indexing:** dev currently outputs `index, follow` site-wide. I didn't change it; please decide the dev noindex policy.
- **URLs:** slugs match the source, but dev permalinks are `/%postname%/`, not `/insights/%postname%/`. There is no `/insights/` archive page on dev (`page_for_posts` = 0). I didn't change either, because they are global settings.
- **Editor:** the content is plain classic HTML with no block markup and no Elementor data. The Classic Editor plugin isn't installed, so WordPress opens it as a single "Classic" block. Install the Classic Editor plugin if you want the classic editing screen.

## Formatting conversions

- **Moto text and images:** clean HTML headings, paragraphs, lists, tables and images, with alignment, alt text and titles kept.
- **Buttons:** links with inline styles that copy the source button colours (orange, navy, green or white pill).
- **Formula embeds:** the raw HTML is kept (in the Australian eCommerce report).
- **CTA banner:** the Moto banner in `ai-seo-pricing-in-australia` is rebuilt as an inline-styled `<div>`.
- **Videos:** the 2 YouTube videos (in `local-seo-statistics-101` and `tiktok-statistics…`) are embedded as WordPress oEmbed URLs.
- **PDF download:** the pallet-racking report PDF is in the dev Media Library and its link is updated.

## Needs review

1. **30 popup buttons in 29 posts** ("Get Your SEO Proposal", "Get In Touch" and similar). On the live site they open Moto popup forms #19 or #21, which don't exist on dev. They are kept as `href="#"` with `data-source-popup` set. Decide where they should go (for example /request-an-investment-briefing/).
2. **2 contact forms are not migrated** (Moto forms need a WordPress form plugin). An HTML comment marks where each one was:
   - `impact-of-covid-19-on-tradies`: Name, Website, Email, Phone.
   - `impact-of-covid-19-on-tradies-in-australia-may-2020`: Name, Email, Website, Message.
3. **112 links to 28 pages that aren't on dev yet** (service pages, calculators, case studies, industries) point to the production URLs.
4. **1 broken source link:** `marketing-for-tradies-original` (404 on the live site too), in `tiktok-statistics…`.
5. **Links rewritten:** links between posts and to pages that already exist on dev now point to dev (62 unique URLs). External links are unchanged.
