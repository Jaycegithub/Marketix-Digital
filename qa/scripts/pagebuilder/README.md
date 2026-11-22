# Service / industry page builder (Nov 2026)

Builds a page from a Google Doc (HTML export) using the Shopify SEO page (2627) layout, the AI SEO (2666) process
section and the SEO Agency Sydney (1295) case-study block. Hero form = SEO Form - General (template 1176).

Auth: `lv.py` sends no credentials – the cloud session's network proxy injects the WordPress application password
(saved as a network secret for marketixdigital.com.au). Never put the password in these files.

Steps (work in a scratch folder, e.g. `scratchpad/newpages/` with `icons/` and `docs/` subfolders; `lv.py` in `../live/`):
1. Export each doc as HTML (Drive `download_file_content`, `text/html`) to `docs/<n>.html`.
2. `python3 -I parse_doc.py docs/<n>.html <n>.json`
3. Fetch `src_2627.json`, `src_2666.json`, `src_1295.json` (`wp/v2/pages/<id>?context=edit`) and `pagemeta.json`
   (template + Astra/Elementor meta of 2627).
4. `python3 icons/resolve_icons.py <n>.json …` – reuses matching `marketix-glyph-*.svg`, uploads new ones, writes
   `icons/icons.json` and `media.json`.
5. `python3 -I build.py <n>` → `out_<n>.json`; create a password-protected preview `zz-preview-<n>` (password `mxprev`).
6. `node measure.js <n>` → `heights_<n>.json`; rebuild (the heights go into each section's `/*mx-cis*/` CSS), then
   delete and recreate the preview so Elementor generates fresh CSS.
7. `node textcheck.js <n>` (only the Business Goals chain line may be "missing" – it renders as chips),
   `node axe.js <n>`, `node shots.js zz-preview-<n> shots/<n>`.
8. Publish: slug from the doc's Landing Page URL, parent 2669 for /industries/, Rank Math meta via
   `rankmath/v1/updateMeta`; remove the path from Rank Math redirect 10 (`qa/rankmath-rule10-industries-pattern.txt`).
