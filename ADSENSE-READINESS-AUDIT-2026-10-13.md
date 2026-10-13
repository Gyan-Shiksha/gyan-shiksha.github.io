# AdSense readiness audit — 13 October 2026

**Status: NOT READY TO APPLY. No AdSense application or ad script deployment was made.**
This is a repository review, not a live-browser, legal, security or AdSense account certification.

## Evidence reviewed
- `LAUNCH-CHECKLIST.md`: outstanding mobile, quiz, PageSpeed, Search Console and copyright checks.
- `QA-REPORT.md` (7 Oct): historical work and manual steps; prior fixes are not proof of current production results.
- `index.html`, `about.html`, `contact.html`, `privacy.html`, `disclaimer.html`, `editorial-policy.html`, `quiz.html`, `study-material.html`, `robots.txt`, `sitemap.xml`, `_config.yml`.
- `data/materials.json`: 14 entries, most hosted externally, marked `rights_verified: true`. The flag records an assertion, **not independent licence evidence**.
- `assets/js/analytics.js`: GA4 gtag initialisation with measurement ID; actual runtime collection/consent not independently verified.
- Editorial dashboard: publication approval is separate from rights and live-file access verification.

## 1. Content and rights: BLOCKED pending evidence
- Verify licence/permission, redistribution terms, original author/publisher, provenance and public access for **each** item in materials.json, including teachers' textbooks and HSC papers. Do not assume public access means permission.
- Verify ambiguous BA/SP titles against the actual PDF and distinguish older papers from latest official notices.
- Add original commentary, solved examples and learning context on high-traffic educational content; assess duplicate/thin and automatically generated pages manually.
- Confirm exact update dates and official sources for news/jobs. Remove or clearly date expired notices.
- Any specific unlicensed item: remove the link from the public catalogue after verification; do not make unsupported allegations or alter rights flags without evidence.

## 2. Technical QA: NEEDS LIVE TEST
- Test production URL, HTTP errors, external PDF links, responsive layout, keyboard accessibility, JS console and load times on phone and desktop.
- Test a full Quiz Saathi attempt and authorised, restricted Google Sheets output. Quiz currently opens an external script.google.com web application, so end-to-end review must include its own page and data-processing configuration.
- Run PageSpeed Insights for Home, Quiz and Blog; inspect Search Console coverage, canonical URLs and submitted sitemap.
- Inspect analytics and third-party requests in real browser. Source meta CSP does not prove production response security headers.
- `robots.txt` allows all agents and references sitemap; existence does not certify successful indexing.
- Check that no ads are placed near quiz/games controls. None added in this PR.

## 3. Privacy and AdSense: PENDING
- Privacy page describes GA4, Google Apps Script/Sheets, student/school names, game localStorage, future advertising and contact; this PR adds a learner-safety notice.
- Verify real data access restrictions, retention period, deletion handling and permissions with the service owner; DO NOT expose the sheet.
- Review applicable children's privacy, age treatment, regional consent obligations and whether the site is directed at children. Configure certified consent solution where required **before** relevant ad serving.
- Do not add an AdSense publisher ID or ads.txt from an assumed value. Obtain real account details, then validate CSP/ad tags/consent and disclosure.
- Review account ownership, age eligibility and invalid-traffic safeguards before applying.
- No AdSense application, advertising tags, publisher IDs, payment settings or account actions performed.

## Changes proposed in this branch
1. `privacy.html`: minor-facing safety guidance with contact route; existing site policy remains intact.
2. `study-material.html`: transparent external-source/update/rights reporting note.
3. This evidence-based audit and hold checklist.

## Release gate
- [ ] File-by-file rights documentation assessed and questionable items corrected
- [ ] Original content quality sampled and strengthened
- [ ] Production mobile/desktop QA including quiz and external PDFs passes
- [ ] Search Console, performance and accessibility verified
- [ ] Student-data storage, access, retention and deletion checks completed
- [ ] Applicable consent and child-directed treatment reviewed
- [ ] Actual AdSense publisher details supplied when needed
- [ ] PR reviewed and explicitly merged; **only then** consider application

References: https://support.google.com/adsense/answer/10502938 ; https://support.google.com/adsense/answer/1348695 ; https://support.google.com/adsense/answer/13554116
