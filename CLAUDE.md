# Marketix Digital – Elementor build conventions

The site is built on the dev WordPress install (dev.marketixdigital.com.au) with Elementor + Elementor Pro.
Follow these rules on every page you build or edit.

## Content
- **Content must match the live page (marketixdigital.com.au) exactly.** Don't add copy, section labels, buttons or paragraphs
  that the live page doesn't have, and don't drop any (including links like "Local SEO Agency" or "Get a proposal").
  Design changes are fine; wording changes are not. Before finishing a page, diff its visible text against the live page.

## Layout & spacing
- Top-level sections are boxed at **1400px**.
- **Padding standard (global, not optional)** – source: the client's "Padding Arrangement for creating page" Google Doc
  (1iYNxnni5XS89mHp5cFb9-SfxZRD90cNU2sg-f546Nh0). Identify the container hierarchy first, then apply:
  1. **Main section** (top-level container): always `100px 10px` (mobile keeps 40px top/bottom, 10px sides).
  2. **Flex/Grid parent whose child containers have NO background**: `5px 0 0 0`.
  3. **Flex/Grid parent whose child containers HAVE a background/image**: `10px` all sides. When a section's children are
     background cards, keep (or add) this 10px Flex/Grid wrapper inside the section – it's required, not redundant.
  4. **Section with ONLY ONE child container that has a background** (e.g. a CTA panel): add an **"Inner Content" container
     (`10px` padding)** inside the background container and put all the content in it; the inner container takes the panel's
     row/column layout. The background container keeps its background and its desktop design padding but gets no extra side
     padding on tablet/mobile (section 10 + inner 10 = 20px). Leaf containers inside the inner container get `0`.
  5. **Container with only direct content** (no nested containers): leave Elementor's default `10px` (remove custom padding).
  6. Containers with their own background/border/shadow (cards, panels) keep their own padding – don't override designs.
  - **No redundant wrappers:** don't put a single row/column wrapper whose children have no background inside a section –
    make the section itself the flexbox/grid. Only create extra containers when rules 3/4 require them.
    Script: `scratchpad/wp/v78/flatten.py`.
  - Edge cases: a plain leaf container sitting beside background cards inside a 10px parent gets `0`; a leaf container inside a
    "mixed" parent (content + containers, parent keeps default 10px) gets `0`; a widget placed directly in a section or in a
    `5px 0 0 0` parent gets `_padding: 0 10px 0 10px`. Template wrapper sections (e.g. Founder Video) stay at 0.
  - A column whose *parent* panel carries the background (e.g. the white form half of the Contact Us panel) is part of that
    panel's design: it keeps its design padding (56/48px, tablet 40px, mobile 30/20px), not the default 10px.
  - Remove tablet/mobile padding overrides on containers the rules set, so there's no double padding.
  - **Priority:** content must sit **20px** from the viewport edge on mobile and tablet, consistently across sections.
    Verify by measuring on a preview (390 / 768 / 1440px) before saving. Script: `scratchpad/wp/v78/padfix.py <page_id> dry|preview|save`.
- Use as few containers as possible. If something can be a single widget (Icon Box, Image, Heading), don't wrap it in a container.
- Adjacent sections must not share the same background. Alternate white (`White`), light blue (`Light Blue`) and dark navy (`Primary`);
  clients want dark blue sections used, not only white/light blue.

## Cards & grids
- **Buttons inside grid/row cards must line up.** When a grid (or row) of cards contains buttons or link-style actions
  ("View case study →", "Get Started"), give the widget directly above the action `_flex_size: grow` (Advanced → Layout → Size: Grow)
  so the actions sit at the same height in every card of a row. Keep the grid's items stretched (don't set align-items: center).
- Card style: white background, 1px `border black` border, 16px radius, soft shadow; 32px padding (20px mobile).
- **Cards on dark navy sections** use the homepage "Selected Work" style instead of white: background `blue front bg`
  (#121F3D), border `border white`, hover border `Secondary`, titles `White`, body `white text`.

## Widgets & icons
- **No HTML widgets.** Build everything with native Elementor widgets.
- Icons are SVG files in the Media Library (`marketix-glyph-<name>.svg`, white line glyphs). The gradient tile is CSS:
  Icon Box → View **Stacked**, Secondary colour white, CSS class `mx-gradient-icon` (rules live in Site Settings → Custom CSS).
  Icon List chips use the class `mx-gradient-chip`.
- Prefer icons + normal-weight text over old raster icon images. New illustrations should be on-brand SVGs (`marketix-illus-*.svg`).
- Never put invented statistics in illustrations or copy.

## Typography & colour (global styles)
- Section label (only where the live page has one): `Top title` + Secondary colour. H2: `Secondary` typography + Primary colour. Body: `Text` + Text colour.
- Card titles: `Heading 20` (bold, ID 380c6e8) in Primary.

## Reusable templates (Templates → Saved Templates)
- Forms: **Book A Strategy Call Form** (ID 1176, hero) and **Contact Us Form** (ID 1178, footer) – templates contain only the form;
  card text stays on the page. Which hero form/text each page uses is set in the client's tracker sheet (column D):
  - **SEO Form - General** = template 1176 with the current card text – don't edit it.
  - **Search Intelligence Form** (ID 2906) and **Google Ads Form** (ID 2908, Adwords + PPC Agency Sydney) = own form templates
    whose fields match their docs exactly (placeholder "goals and challenges", revenue options as written in the docs).
  - **Digital PR Form** (ID 2903) = same, without the Annual Revenue field; its card has no footnote.
  - Always copy field labels, placeholders and dropdown options verbatim from the form doc, and verify the rendered form.
- **Featured In The Media**, **Reviews Section**, **Our Approach Section**.
- **Founder Video Section** (ID 2070): white section with a navy panel – heading, copy, callout and the founder YouTube video.
  Embed with a Template widget in a zero-padding wrapper container (as on the homepage); keep it next to non-white sections.
  **Founder Video Section - Light** (ID 2235): same content, Light Blue section with a white bordered panel – use it under
  navy heroes so dark doesn't follow dark (Sydney, Enterprise SEO, eCommerce SEO).
- Case study cards (grid + "View All Case Studies" button; section heading stays on the page):
  **Case Studies - True Protein, Total Image Group, Snap Shades** (eCommerce, Enterprise) and
  **Case Studies - Uno Home Loans, True Protein, Circles Life** (Sydney).
- **Areas We Service** (ID 2333): the whole areas block – label, H2, intro, "SEO Agency <City>" buttons and the branded
  Australia map (`marketix-illus-australia-map.svg`) with one pin per city. Hovering a button highlights its pin (Custom Code
  "Areas Map Pins", ID 2319, uses the `mx-area-btns` / `mx-area-map` / `mx-pin` classes). Embed with a Template widget inside
  the page's own section (the section keeps its background/padding); keep pin titles equal to the city names.
- Client logo grids must match "Featured In The Media": 6 columns, white bordered cells ~102px tall.
- "Book A Strategy Call" buttons link to `/request-an-investment-briefing/`.

## Working safely
- Before saving a page, re-fetch it and confirm `modified` hasn't changed (the user edits in Elementor too).
- Preview drafts/changes on a temporary password-protected copy, then delete it. Clear Elementor's CSS cache after saving.

## Tracking, schema & performance (Elementor → Custom Code)
- **2910 Tracking Tags** (site-wide, head): GSC meta + GA4 `G-FDJ8VGTY39`, GTM `GTM-WNVB8TQ`, Bing UET `283014674` (same IDs as live).
  The scripts load on the visitor's first interaction or 10s after load (keeps mobile PageSpeed green) – don't revert to eager loading.
- **Test tracking (dev only):** 2910 also loads test GTM containers `GTM-KKMXLBHX` + `GTM-T4CHD883` when the hostname starts
  with `dev.` (never on the live domain – don't write the dev domain into that check, Better Search Replace would rewrite it).
  Custom Code **3018** pushes dataLayer events `phone_click`, `email_click` and `form_submission` (form_name, form_page,
  form_page_title – sent on /thank-you/). GTM import file for the test container: `Marketix-DEV-GTM-import.json`.
- **2911** site-wide schema (Corporation/LocalBusiness/FAQ) and **2912** homepage schema – copied verbatim from live.
- **2914** homepage hero image preload (update it if the hero image changes). **2915** accessibility fixes (tap targets,
  loop list roles, menu-icon label, screen-reader text on "Read More").
- Elementor performance settings on: local Google Fonts, optimized image loading, lazy-load background images.
- **Mobile content-visibility** (Custom Code **2927**, head): on mobile, page sections from the 3rd onward (+ footer) get
  `content-visibility:auto` – cuts mobile TBT ~70–80%. It must stay in a **head** snippet (in body_end it does nothing).
  Excluded: case studies (`parent-pageid-1527`), `.hero-grid-overlay` sections and any section with the CSS class
  **`mx-no-cv`** (e.g. Digital PR "Original Research…"), because their images/overlays hang outside the section and would be
  clipped. Give `mx-no-cv` to any new section whose content overflows it.
  2927 also preloads the navy hero background `marketix-bg-navy-network-v2.svg` (the LCP element on most pages).
- **Contrast (Accessibility 100):** on Light Blue / `#F7F9FF` backgrounds use `#3962DE` for blue text (not Secondary
  `#3D68EA`, 4.37:1); on blue (Secondary) panels use White text, not `white text` (80% → 3.68:1); don't use `#8FA9FF` or
  `top title` `#6188FF` on white. Heading levels must not skip (H1 → H3); footer column titles are H2.
- **Images:** all PNG/JPG images used on the site were converted to WebP (≤1600px, q80) as new media items and every
  reference was switched (originals kept in the library; map in `scratchpad/live/perf/webp_map.json`). Upload new images
  as WebP and give every featured image alt text (= post title).
- Keep PageSpeed green: upload images as WebP (featured images ≤1200px wide), give image links alt text, keep 12–14px
  labels on Light Blue sections at `#3962DE` (Secondary `#3D68EA` fails contrast there), underline inline text links.
- **WP-Optimize** (configured, settings backup exported): page cache on (24h, scheduled preload), gzip on, static file
  headers 365 days, minify on for **JS only** (HTML minify off). **Keep WP-Optimize CSS processing OFF** – its merged CSS goes stale when
  Elementor regenerates CSS (pages lost styling: giant text). **Don't enable "Defer all JS" or JS merging** – tested: it
  breaks / delays the mobile menu popup. **Always purge the WP-Optimize page cache right after clearing Elementor's CSS cache** (cached HTML keeps pointing at the deleted
  `post-<id>.css` files: pages lose their styling and scroll sideways on mobile until purged). Purge the page cache after editing pages via the REST API
  (saves in the Elementor editor purge automatically). **2927** preloads the 4 Poppins woff2 files (update if Elementor
  regenerates its local fonts).

## Launch setup (pre go-live, Nov 2026)
- Form leads go to **hello@marketix.info** (form templates 1176, 1178, 782, 2903, 2906, 2908), with two internal addresses in
  BCC (Email action → BCC; keep them when editing forms). Every form's actions are
  email + save-to-database + **redirect to `/thank-you/`** (page 3012, noindex, copied from live). Tracking tags load
  immediately on all `/thank-you*` pages (2910), and Custom Code 3013 fires the Meta Pixel `Lead` event + `cg_convert` on
  /thank-you/ (as on live) - keep both for conversions. Download thank-you pages: `/thank-you-tradie-download/` (3016, its
  beacon.by link is dead on live too) and `/thank-you-7-killer-ways-to-get-more-calls/` (3017, PDF in the media library;
  old `/downloads/…pdf` URL redirects to it). All three are noindex.
- New pages need the Astra layout meta copied from an existing page (`ast-site-content-layout: full-width-container`,
  `site-sidebar-layout: no-sidebar`, `site-post-title: disabled`) or their sections render boxed.
- **Every page's contact section** (incl. the homepage) embeds the **Contact Us Form** template (1178) with a Template widget;
  each page keeps its own left-panel text. Don't put inline form widgets in contact sections.
- **404 page** = Theme Builder template **3023** ("404 Page", type error-404, condition Include → 404 Page): navy hero only
  (Error 404 label, H1, one line, Book A Strategy Call + Back to Home). Full-width CSS (`body.error404 …`) lives in 2915.
  Set Theme Builder conditions via REST `PUT elementor/v1/site-editor/templates-conditions/<id>` – that refreshes Elementor's
  conditions cache; writing `_elementor_conditions` meta (or PUT site-editor/templates/<id>) does not.
- **Category pages** (/insights/category/…) use the Theme Builder archive template **3005** (Insights hero + category pills +
  loop grid on the current query). Pill styles and the full-width fix live in Custom Code 2915. Posts per page = 9.
  Paginated category pages (`/page/2/`+) canonicalise to page 1: each category has Rank Math's canonical URL set to its
  page-1 URL (term meta `rank_math_canonical_url`, set via REST `POST rankmath/v1/updateMeta`). **Set it on every new category.**
- **Permanent redirects live in `.htaccess`** (edit via Rank Math → General Settings → Edit .htaccess; back up first), above
  `# BEGIN WordPress`, copy in `qa/htaccess-marketix-rules.txt`: one-hop HTTPS + non-www (Cloudflare-safe), `/blog/` →
  `/insights/`, `/blog/<slug>` → `/insights/<slug>/` (12 articles deleted on live → `/insights/`),
  `/blog/seo-statistics-australia-2020/` → `/insights/local-seo-statistics-101/`, `/seo-agency-sydney-old/`,
  the `/+61280338464` link artifact → `/`, the old `/mt-content/…pallet_racking…pdf` and `/Terms of Service.pdf` → new PDFs.
  Targets are relative so the block works on dev and production. Don't duplicate these in Rank Math.
- Rank Math → Redirections keeps `/insights/seo-statistics-australia-2020/` → `/insights/local-seo-statistics-101/`, the
  7 Killer Ways PDF 301, and the temporary rules below.
  Temporary **302 regex rules** for pages not yet rebuilt: the tracker's unbuilt
  service + city pages (11) → homepage; unbuilt industry pages (51, incl. eCommerce Brisbane/Melbourne, Fashion SEO) →
  `/industries/`; 19 other old pages (tradies, ad landing pages `-ga`, Central Coast, Wollongong…) → same path on
  old.marketixdigital.com.au. **When you build one of those pages, remove its path from its regex rule**, or the redirect
  hides the new page. Lists: `scratchpad/wp/v85/redirect_final.json`.
- Redirect destinations are stored with the dev domain; Better Search Replace (dev → main, all tables) at launch fixes them.
- Schema logo now lives in the media library (ID 2995), not on the old site's /mt-content/ path.
