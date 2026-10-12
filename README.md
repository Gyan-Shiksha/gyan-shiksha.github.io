# Gyan Shiksha V3

## Scope
Gujarati Medium, Std. 6–12 only.
Special focus: Std. 10 and Std. 12 Board Exam.

## Technology
- HTML5
- Custom CSS (responsive UI/UX)
- Vanilla JavaScript
- SVG
- Python development scripts (`tools/`) for validation/build tasks
- GitHub Pages deployment

## Important
GitHub Pages does not execute PHP or Python on the server.
PHP/Python can be used for local/build automation or later on a backend host, but the live GitHub Pages website remains static.

## AdSense
The current launch build contains **no AdSense script, publisher ID or visible ad placeholders**.
Real ad code should be added only after AdSense approval/site setup and a final policy/privacy review. Keep Quiz iframe/Focus Mode ad-free unless the production configuration is separately reviewed.

## V3.1 Improvements
- Removed placeholder Gyan Shiksha email until domain setup
- Added client-side section search
- Improved mobile menu accessibility and body scroll handling
- Moved first AdSense placeholder below useful Quick Access content
- Added mobile/performance CSS refinements
- Added robots meta to indexable pages

## Current Home Page
The grade row and subject row have been intentionally removed.
Homepage now uses:
1. Hero + site search
2. Quick Access
3. Board Exam Focus / Practice Tools / Study Guidance
4. Footer

Only live/useful sections are promoted. Study Material and Updates remain `noindex` until real content is ready.

## V3.2
- Expanded Board Exam page with useful evergreen preparation guidance
- Expanded Study Material page with resource-library and learning-flow structure
- Added AdSense placeholders only after meaningful content blocks
- Marked unfinished content pages `noindex,follow` until real content is added
- Removed fake placeholder email from shared utility bars

## V3.3
- Integrated existing Google Apps Script Quiz Saathi web app into `quiz.html`
- Added full-screen fallback link
- Updated CSP `frame-src` for Google Apps Script
- Added privacy guidance before the embedded quiz
- Reserved AdSense space after the quiz instead of near answer controls
- Quiz page is now indexable because it provides functional learning content

Quiz Web App:
`https://script.google.com/macros/s/AKfycbxM88Z2cZ1gVuXFU22R1ebiKmZywSqxPyr_VY669V_scB0eEdahGdSsRJn4AVzqQY4LXQ/exec`

## V3.4
- Kept existing Quiz Saathi student/school information flow unchanged
- Added `quiz-player.html` so Focus Mode stays on a Gyan Shiksha URL
- Removed the visible direct Google Apps Script full-screen link from the Quiz page
- Updated Privacy Policy to disclose current Quiz Saathi data collection/storage flow
- Google Apps Script remains the backend inside an iframe; the browser address stays on Gyan Shiksha

## V3.5
- Added functional browser-based educational games with three modes
- Games page is now indexable and stores only local best scores
- Converted Blog from placeholders into three original evergreen study guides
- Added individual indexable article pages for board planning, revision and self-test guidance
- Improved Updates page but kept it `noindex` until verified current updates are available
- Sitemap generator now excludes pages marked `noindex`
- Search index now includes the new study-guidance articles

## V3.6
- Pre-approval AdSense cleanup: reserved ad containers are hidden until real AdSense approval/code is added
- Removed the ad placeholder from the embedded Quiz page
- Expanded About, Contact, Terms, Disclaimer and Editorial Policy for production trust
- Temporary contact email is configured until a dedicated Gyan Shiksha domain mailbox is created
- Added PWA/mobile manifest
- Added `.well-known/security.txt`
- Added Unsplash preconnect on pages that use remote images
- Reduced hero image delivery size
- Added async image decoding for lazy-loaded images
- 404 page is explicitly `noindex`

## V3.7
- Removed remaining demo-style cards from the Home page
- Expanded Study Plan into a useful indexable guide
- Expanded FAQ with practical site/quiz/privacy/board questions
- Marked Study Material `noindex,follow` until real notes/resources are available
- Added root `security.txt` fallback because hidden `.well-known` folders may not upload through every browser workflow
- Rebuilt sitemap after indexability changes

## V3.8 Launch Candidate
- Primary navigation now promotes only live/useful sections
- Study Material and Updates stay available for development but are not promoted/indexed yet
- Removed every pre-approval Advertisement placeholder from production HTML
- Tightened CSP so only Quiz pages may frame Google Apps Script
- Improved game localStorage resilience and locks mode switching during a round
- Added three more original educational guides: Answer Writing, Maths Practice, Exam Week
- Synchronized OpenGraph metadata and mobile manifest links
- Added a stronger launch validator for sitemap/indexability/navigation/ad-placeholder checks

## V3.9 Professional QA
- Corrected remaining homepage/footer claims so the public site promotes only live resources
- Made Home feature rows fully clickable and improved internal linking
- Fixed heading hierarchy and several accessibility details
- Improved menu keyboard behavior, search keyboard navigation and search coverage
- Improved game ARIA state/progress behavior and private-mode storage resilience
- Tightened CSP permissions; Google iframe access remains limited to Quiz pages
- Lazy-loads the embedded Quiz on the standard Quiz page and removes unnecessary iframe permissions
- Expanded Privacy Policy for browser localStorage, hosting/services and third-party media
- Added article breadcrumbs, related-guide links, author/review metadata
- Added raster social-sharing image, Twitter cards, PWA raster icons and app shortcuts
- Removed unnecessary third-party preconnects and added image dimensions to reduce layout shift
- Added a noindex Security page plus standard `.well-known/security.txt`
- Expanded the launch validator with SEO, CSP, social metadata, content-integrity and accessibility-oriented checks
- Added `QA-REPORT.md` and `tools/update_base_url.py` for the future custom-domain migration

### Manual repository cleanup still recommended
The GitHub repository description still references old Psychology/TAT content and the repository is still a fork. These are repository-level settings, not website-code defects.

## V3.10 Professional UX Polish
- Refined navigation hierarchy and made Quiz the primary action
- Replaced generic stock thumbnails on Home/Blog with branded visual blocks
- Kept the approved Home hero image while reducing unnecessary third-party image requests
- Improved Blog card consistency, visual identity and reading hierarchy
- Made Quiz Focus Mode the clearest primary start action while preserving the inline quiz
- Improved Games start state, mobile nav overlay and hover/focus behavior
- Kept the patch focused on live UX without changing policy/content architecture


## Independent Gyan Shiksha domain and Markdown blog (Oct 2026)
- Primary domain: https://gyanshiksha.in; canonical, social and sitemap URL settings migrated.
- Add a Markdown article in _posts/YYYY-MM-DD-slug.md using layout: post; see BLOG-PUBLISHING.md.
- GitHub Pages/Jekyll generates the HTML and blog listing; old seven article URLs remain unchanged.
- The shared new-post template is _layouts/post.html. Do not create .nojekyll.
- Static sitemap source is generated by python tools/build_sitemap.py; Jekyll inserts new post URLs at deployment.
