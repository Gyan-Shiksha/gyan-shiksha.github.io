# Gyan Shiksha — Content, News/Jobs અને Material Publishing SOP

Updated: 2026-10-12. Public website: https://gyanshiksha.in

## 1. મુખ્ય શૈક્ષણિક પ્રાથમિકતા
- ધોરણ 10: અંગ્રેજી (Reading, Grammar, Writing), ગણિત (worked examples, concept clarity, error-log practice), વિજ્ઞાન (diagrams, concepts and reasoning)
- ધોરણ 12: અંગ્રેજી (Writing/Reading) અને સંબંધિત streamsના ગણિત/વિજ્ઞાન વિષયો. વિદ્યાર્થીનું Stream અને સત્તાવાર Chapter List ખાતરી કર્યા વગર ખોટા પ્રકરણનો દાવો ન કરવો.
- Learning priorities: original Gujarati explanation, fully checked worked examples and MCQs, meaningful diagrams, accessible images with alt text, revision prompts and relevant internal links.
- વર્તમાન GSEB syllabus / textbook chapter referencesને સત્તાવાર સ્રોતથી ચકાસ્યા વગર "2026 latest" તરીકે મૂકવું નહીં.

## 2. Live News, Jobs અને Materials કઈ રીતે ચાલે છે?

Website source:
- `data/news.json` → `updates.html` અને Home News block.
- `data/jobs.json` → `jobs.html` અને Home Jobs block.
- `data/materials.json` → `study-material.html` filtered file-level Library.
- `assets/js/feeds.js` અને `assets/js/material-library-v317.js` Approved entries જ બતાવે છે.

**હાલ News અને Jobsના JSON ફીડ ખાલી છે; Materialsમાં ચકાસણીથી પ્રકાશિત વ્યક્તિગત ફાઇલ નોંધો છે.** ફ્રન્ટએન્ડ તૈયાર છે, LIVE News પબ્લિશિંગ/Pull From Sheet હજી લાગુ નથી. News/Jobs પેજમાં `noindex` છે; ખરેખર original verified entries પ્રકાશિત થયા પછી તેનું Indexing અને Navbar visibility ફરી ચકાસવું.

Editorial Sheet (restricted; not published to web):
https://docs.google.com/spreadsheets/d/1oxTXnrTCqbSQTtyO-428jhq-mk-LhhweWcSYAyHjmq8/edit

Tabs: **News**, **Jobs**, **Materials**, **Instructions**.

Workflow: Draft → Review → Approved → (manual/publishing job) website JSON update. Sheetમાં Approved કરવું માત્રેથી live update થતો નથી. Site administrator records ચકાસીને publish કરાવે ત્યારે જ Repoમાં મંજૂર Public Data Commit કરવું.

### News editorial checklist
1. Date (YYYY-MM-DD), title, category, original Gujarati summary (why it matters / what students should do), official source URL, optional PDF URL.
2. Board exams, timetables, fees, circulars અને scholarships માટે GSEB/SEB/GSERC/Govt official noticesથી fact-check.
3. Sourceમાંથી લાંબી નકલ નહીં; ચકાસેલી માહિતી, સંદર્ભ, તથ્ય અને સ્પષ્ટ Source Citation.
4. “Breaking/Live” લખતાં પહેલાં માહિતી સચોટ અને તાજેતરની હોવી જોઈએ.
5. ખોટી/જૂની ખબર કે તાત્કાલિક Placeholder બહાર ન મૂકવો.

### Jobs checklist
1. Official advertisement source, exact deadline, eligibility, process and source link.
2. Expired vacancies remove or mark expired; Do not claim any official affiliation.
3. Review before public status Approved; publish only original verified short summaries.

### Materials checklist
1. **મુખ્ય Drive/MEGA folderનો Link ક્યારેય Siteમાં Public ન મૂકવો.**
2. Owner accountમાં Master folder Restricted રાખવો. Public delivery માટે ફક્ત વ્યક્તિગત PDF/Docs ફાઇલની Reader link Share કરવી.
3. User's own or permitted/copyright-safe resource only. Never upload copyrighted textbook scans without permission.
4. Each data entry: title, standard (10/12), subject, category, unique direct file URL, updated_at, status=Approved.
5. Use browser Incognito to verify each individual file opens; changing the HTML or adding iframe doesn't change Google Drive permissions.
6. If not approved, material stays unpublished. Only curated, authorised file records should be publicly listed; do not add fake file links.

Example `data/materials.json` row (**template, NOT actual data**):
```json
{
  "title": "દાખલાનું સાચું નામ",
  "standard": "10",
  "subject": "ગણિત",
  "category": "Notes",
  "description": "ફાઇલમાં શું મળશે તેની સાચી માહિતી",
  "url": "https://drive.google.com/file/d/REPLACE_REAL_FILE_ID/view",
  "updated_at": "2026-10-12",
  "status": "Approved"
}
```
Do not commit this example to the feed, as it is not a real verified file.

## 3. AdSense-ready Editorial Standards
- Google Publisher Policies: useful and original publisher-content, truthful navigation and download links, no mass-produced low-value articles, no copied official pages.
- No guaranteed approval, earnings, ranking or AI-detector results.
- AI drafting is not a substitute for human subject review and fact checking. Don't add false author biographies or pretend human verification happened.
- Images: local optimized SVG graphics with specific useful alt text, not unauthorized stock images. Keep the content itself substantial.
- When AdSense is approved, place compliant ad units separately from download buttons, quiz answers and navigation.
- Do not claim Exam Board/Govt affiliation.

## 4. Remaining configuration
- Sheet created for editorial use and shared with official Gyan Shiksha email. Confirm editing access and eventual ownership in the official Google account.
- Private CSV-to-JSON publishing tool `tools/import_editorial_csv.py` and tests are available. Automatic sheet polling is not yet enabled; see `EDITORIAL-CSV-PUBLISHING.md`. Do not expose Google tokens in the public repository.
- Add real vetted News/Jobs/Material rows; then publish and verify both responsive HTML and official source links.
- Confirm master Drive folder General Access is Restricted; independently review MEGA public folder share setting.
- Quiz existing backend remains unchanged; maths questions already present per site owner. Verify by actually running the quiz, including answer accuracy.
- Review images/content for each future post and ensure current curriculum matches latest board.
