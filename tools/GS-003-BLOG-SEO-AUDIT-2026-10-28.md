# GS-003 — Gujarati Blog and SEO Improvement Report
Date: 2026-10-28
Status: PROPOSED CHANGES / NOT MERGED
Repository: Gyan-Shiksha/gyan-shiksha.github.io
Branch: audit-gs003-blog-seo-2026-10-28

## Scope and permissions
The owner requested independent progress on blog publishing, SEO and site quality while preparing an AdSense application. To protect the live site, all changes are on a separate branch for review. No production deployment, account application, ad tag, ads.txt or changes to the Quiz / private student data are in this branch.

## Changes
1. `_posts/2026-10-28-std10-trigonometry-ratios.md`: original Gujarati Std 10 trigonometry lesson. Includes definitions, 3-4-5 and 5-12-13 worked examples, common misconceptions, four questions, checked solutions and relevant internal article links.
2. `assets/img/blog-trigonometry.svg`: original vector illustration, labelled for a 3-4-5 right triangle.
3. `_layouts/post.html`: image alt fallback supports per-post `image_alt`; post CSS, JS, logo and manifest paths use root-relative URLs; dynamically displays up to three same-category related posts with a relevant fallback.
4. This implementation / audit note.

## Source checks
- Blog index iterates `site.posts` and will show the new article after a successful Jekyll deployment.
- `_config.yml` defines `permalink: /blog-:title.html`; expected article URL: `/blog-std10-trigonometry-ratios.html`.
- `sitemap.xml` iterates `site.posts`; new URL expected in the rendered sitemap.
- `tools/check_posts.py` requires valid YAML front matter, original explanatory text, three or more headings, practice, and an existing image.
- `.github/workflows/site-qa.yml` runs Jekyll build, link tests, SEO and functional checks on pull requests.

## Important limitations
- Remote desktop/mobile browsers and PageSpeed, Search Console indexing, external PDF access, and actual quiz storage/data-sharing flows have NOT been verified in this task.
- No AdSense account access/authorised submission mechanism is available, and no application has been submitted.
- The owner stated permissions are held for the PDF materials. For audit readiness, retain publisher/licence, scope of re-hosting and ad-supported use, and file mapping as evidence; do not change `rights_verified` on the basis of a general statement alone.
- Existing reports dated 2026-10-26 identify unfinished private quiz Apps Script storage/access/retention review. A GitHub code review does not certify that service.
- Per-article social previews still use a shared Open Graph PNG; this change does not assert that SVG assets are supported by social media previews.

## Acceptance tests
- [ ] GitHub Pull Request `Gyan Shiksha Website QA` workflow passes.
- [ ] Check rendered article, image, nav and related links on real desktop and mobile.
- [ ] Confirm published sitemap and canonical URLs after merging.
- [ ] Confirm official teaching/terminology reference against current applicable curriculum.
- [ ] Verify AdSense applicant account eligibility and correct site setup within the account.
- [ ] Verify rights evidence and live quiz data flow before claiming policy readiness.

## Decision
Code changes are limited, reversible and proposed through PR. **Do not claim AdSense approval or live testing. Do not merge without owner review.**
