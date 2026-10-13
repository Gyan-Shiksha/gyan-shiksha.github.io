# Gyan Shiksha — Study Material Page Audit (13 Oct 2026)

## Scope and evidence
- Source: `study-material.html`, `assets/js/material-library-v317.js`, `assets/css/material-library-v317.css`, `data/materials.json`, site QA checks and new real-data UI simulation.
- This report is a **code, catalogue, and GitHub CI** audit. A real remote browser screenshot/manual on-device test is **not** represented as completed. MEGA file contents/downloads and email form submissions were **not** independently tested.
- Public page: https://gyanshiksha.in/study-material.html

## Baseline catalogue findings
- JSON records: **144**, duplicate full file URLs: **0**.
- Categories: **131 Textbook**, **12 Question Paper**, **1 PDF**; zero live Notes, Worksheet, Image, Presentation, Video, Audio records. Previous landing-page wording implied these unavailable categories were already offered.
- Numeric grade distribution: Std 1 **2**, Std 2 **3**, Std 3 **0**, Std 4 **6**, Std 5 **6**, Std 6 **13**, Std 7 **13**, Std 8 **15**, Std 9 **9**, Std 10 **9**, Std 11 **26**, Std 12 **40**. Additionally teacher guide **1**, GSET **1**. Grade 12 includes **28 textbooks/lab manuals** and **12 HSC 2023 question papers**.
- All 144 records currently have `updated_at` fields. These are catalogue updates, **not** book edition dates; displaying one on every card was noisy and misleading as edition metadata.
- **5 descriptions/subjects remain provisional**: Std 1 file IDs `qn4iBSBK`, `eqRiHahY`; Std 2 file IDs `bmhC1YJC`, `qjxA1KKL`, `PrZXmJRC`. The user must provide covers or identifiable title/subject information to correct them; do not invent subjects.
- Std 3 **five** materials are staged, **not live** (GitHub draft PR #20); the five filenames were visible in screenshot, but individual MEGA URLs have not been confirmed as matched to those names.
- Std 12 file `book-147.pdf` is recorded in `.github/pending-materials/std12-book-147.json` and intentionally **not public** until its title/subject are identified.
- HSC 2023 question-paper labels `BA` and `SP` still reflect ambiguous source filenames; verify before expanding their full subject names.

## Layout/functional audit and actions
| Check | Before | Fix / retained guarantee |
|---|---|---|
| Long page | Four large unrelated study-guide cards **plus** duplicated request/share call-to-action cards after the catalogue | Remove repetitive guide and duplicate CTAs, retain core catalogue and both operational forms |
| Request/share forms | Both lengthy forms always open | Native `details/summary` accordions, closed initially; all form fields, rights consent and privacy text retained |
| Catalogue description | Cards display paragraphs and repeat upload date | Two-line description clamp; show grade, subject and actual edition year; omit repeated catalogue upload date and redundant GSEB board label |
| Filter consistency | Year select offered years from unrelated grades; subject included unrelated material types | Recompute available subjects by grade+type and years by grade+type+subject; clear invalid year/subject selection |
| Irrelevant category claim | Hero/SEO claimed photos, worksheets and notes even though feed has no such category entries | Describe only **available** textbooks, papers and PDFs; category buttons already hide absent categories |
| Large result set | Pagination is already 6 cards/page, but original smoke test used only 31 mock rows | Preserve numbered navigation and `Previous/Next` focus/scroll; add real-dataset 144-record integration test. Current full feed: **24 pages**. Std 12: **7 pages**; Std 11: **5 pages**. |
| Responsive | Three cards per desktop row, two per tablet, one per mobile | Keep breakpoints, compact card padding and adapt grid when year control is hidden |
| Student data / permissions | No changes intended | No Quiz, student-data handling, AdSense or MEGA URL changes |

## Verification contract
- PR QA must pass Jekyll build, site hooks/internal links, file URL/permissions tests and two material pagination tests (existing mock 31 + current real material feed).
- New real-feed test must exercise 6-card bound, first/last/direct-page/previous/next controls, Std 12 and Std 10 filters, year reset, subject/category cascading, search empty-state, reset and safe file opening in new tab.
- GitHub Pages post-merge build and deployment must succeed before the change is described as live.
- **Not covered:** visually reviewing a real mobile/browser screenshot, downloading/decrypting all 144 externally hosted resources, individually verifying publisher edition metadata, submitting forms or proving Google has indexed catalogue entries.

## Pending editorial work
1. Get exact cover/title+subject for the five Std 1–2 provisional listings.
2. Confirm Std 3 screenshot filename ↔ five MEGA link order and complete PR #20.
3. Identify Std 12 `book-147.pdf` and review the ambiguous HSC 2023 `BA`/`SP` source labels.
4. Manually spot-check several actual browsers/devices and individual download URLs; external MEGA availability isn't verified by GitHub QA.
