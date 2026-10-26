# Marketix Digital – Elementor build conventions

The site is built on the dev WordPress install (dev.marketixdigital.com.au) with Elementor + Elementor Pro.
Follow these rules on every page you build or edit.

## Layout & spacing
- Top-level sections are boxed at **1400px**. Section padding: 100px top/bottom (40px on mobile), 10px left/right.
- On mobile every section's content sits **20px** from the screen edge. Work out nested padding so it adds up to 20px
  (e.g. section 10px + inner container 10px → deeper containers get 0px). Never zero a parent container's padding blindly.
- Use as few containers as possible. If something can be a single widget (Icon Box, Image, Heading), don't wrap it in a container.
- Adjacent sections must not share the same background. Alternate white (`White`), light blue (`Light Blue`) and dark navy (`Primary`);
  clients want dark blue sections used, not only white/light blue.

## Cards & grids
- **Buttons inside grid/row cards must line up.** When a grid (or row) of cards contains buttons or link-style actions
  ("View case study →", "Get Started"), give the widget directly above the action `_flex_size: grow` (Advanced → Layout → Size: Grow)
  so the actions sit at the same height in every card of a row. Keep the grid's items stretched (don't set align-items: center).
- Card style: white background, 1px `border black` border, 16px radius, soft shadow; 32px padding (20px mobile).

## Widgets & icons
- **No HTML widgets.** Build everything with native Elementor widgets.
- Icons are SVG files in the Media Library (`marketix-glyph-<name>.svg`, white line glyphs). The gradient tile is CSS:
  Icon Box → View **Stacked**, Secondary colour white, CSS class `mx-gradient-icon` (rules live in Site Settings → Custom CSS).
  Icon List chips use the class `mx-gradient-chip`.
- Prefer icons + normal-weight text over old raster icon images. New illustrations should be on-brand SVGs (`marketix-illus-*.svg`).
- Never put invented statistics in illustrations or copy.

## Typography & colour (global styles)
- Section label: `Top title` + Secondary colour. H2: `Secondary` typography + Primary colour. Body: `Text` + Text colour.
- Card titles: `Heading 20` (bold, ID 380c6e8) in Primary.

## Reusable templates (Templates → Saved Templates)
- Forms: **Book A Strategy Call Form** (hero) and **Contact Us Form** (footer) – templates contain only the form; card text stays on the page.
- **Featured In The Media**, **Reviews Section**, **Our Approach Section**.
- Case study cards (grid + "View All Case Studies" button; section heading stays on the page):
  **Case Studies - True Protein, Total Image Group, Snap Shades** (eCommerce, Enterprise) and
  **Case Studies - Uno Home Loans, True Protein, Circles Life** (Sydney).
- Client logo grids must match "Featured In The Media": 6 columns, white bordered cells ~102px tall.
- "Book A Strategy Call" buttons link to `/request-an-investment-briefing/`.

## Working safely
- Before saving a page, re-fetch it and confirm `modified` hasn't changed (the user edits in Elementor too).
- Preview drafts/changes on a temporary password-protected copy, then delete it. Clear Elementor's CSS cache after saving.
