# Gyan Shiksha — News / Jobs Publishing (ગુજરાતી)

**મુખ્ય સિદ્ધાંત:** ખાનગી Google Sheetમાં Draft, Review અને Approved બધું રહી શકે; જાહેર વેબસાઇટ પર ફક્ત સત્તાવાર સ્ત્રોતથી ચકાસેલી Approved નોંધો જ જાય. કોઈ Private Sheet અથવા Google Tokenને Public GitHubમાં કદી મૂકશો નહીં.

## 1. Editorial Google Sheet

https://docs.google.com/spreadsheets/d/1oxTXnrTCqbSQTtyO-428jhq-mk-LhhweWcSYAyHjmq8/edit

Tabs:
- `News`: date, title, category, summary, source_url, pdf_url, status, editorial_notes, last_verified
- `Jobs`: date, title, category, summary, source_url, pdf_url, deadline, status, editorial_notes, last_verified
- `Materials`: separate validated file-sharing workflow; existing 14 published files are untouched by this importer
- `Instructions`: editorial handbook

સૌપ્રથમ શાળા, શિક્ષણ વિભાગ અથવા પરીક્ષા બોર્ડની **સત્તાવાર જાહેરાત** વાંચો. `summary`માં વિદ્યાર્થીઓએ શું જાણવું અને આગળ શું કરવું તે પોતાની ગુજરાતી ભાષામાં સમજાવો. ફક્ત કૉપી કરેલા નોટિસથી પેજ ભરશો નહીં.

Status `Draft` → `Review` → `Approved` કરો. `last_verified`માં ખરેખર જે દિવસે અધિકૃત સ્ત્રોત ફરી જોયો તે દિવસ YYYY-MM-DDમાં ભરો. `Published` જૂની પ્રકાશિત નોંધોના ટ્રેકિંગ માટે સ્વીકારાય છે.

## 2. Approval પછી publish કરવાની રીત

આ Workflow માટે હાલ **Automatic Publisher ચાલુ નથી**. એ જાણી-જોઈને રાખેલી સુરક્ષા છે: અચકાસેલી ભરતી/અફવા તાત્કાલિક જાહેર ન થાય.

વિકલ્પ A (સૌથી સરળ): ChatGPTને કહો: "Editorial Sheetના News/Jobsમાં Approved નોંધો ચકાસીને નવા Repositoryમાં PR બનાવો." Connected Google Driveથી Notes વાંચીને GitHubમાં તે જ ચકાસેલી Public Fields મૂકવામાં આવશે. મંજૂરી વગર વ્યક્તિગત અથવા Draft નોંધો Public ન કરવી.

વિકલ્પ B (કોડ દ્વારા):
1. Google Sheetમાં `News` અથવા `Jobs` Tab ખોલો.
2. **File → Download → Comma Separated Values (.csv)**. સાચા Tabનો CSV ખાનગી કમ્પ્યુટરમાં રાખો.
3. નવા Gyan-Shiksha repositoryનું સ્થાનિક checkout ખોલો, Python 3.10+થી:
   - `python3 tools/import_editorial_csv.py --feed news --csv /private/News.csv` (Dry Run)
   - `python3 tools/import_editorial_csv.py --feed news --csv /private/News.csv --write`
   - `python3 tools/import_editorial_csv.py --feed jobs --csv /private/Jobs.csv --write`
4. `git diff data/news.json data/jobs.json`થી ફેરફારો વાંચો; સત્તાવાર Links, Dates અને Summary ફરી ચકાસો.
5. અલગ Branchમાં PR બનાવી GitHub QA સફળ થયા પછી Merge કરો.

**ખાસ ધ્યાન:** CSV અથવા Google Sheet ક્યારેય Public GitHub Repositoryમાં Commit કે Publish to Web ન કરવી. આ Importerમાંથી માત્ર title, date, category, original summary, source_url, pdf_url, deadline અને Approved Status જાહેર JSONમાં જાય છે; ખાનગી `editorial_notes` કે `last_verified`નો અંદરના સંપાદકીય અભ્યાસ માટે ઉપયોગ થાય છે, પરંતુ Public JSONમાં કૉપી થતો નથી.

## 3. Publishing Gate

- `Draft` અને `Review` જાહેર નથી થતા.
- Date YYYY-MM-DD જ જોઈએ; ખોટી તારીખ નકારી કાઢાય.
- છેલ્લી અધિકૃત ચકાસણી 45 દિવસથી જૂની હશે તો ફરી સ્રોત તપાસવો પડે.
- Jobsની સમાપ્ત થઈ ગયેલી deadlineવાળી નવી નોંધ પ્રકાશિત નહીં થાય.
- HTTPS Source અને અર્થપૂર્ણ મૂળ Gujarati summary ફરજિયાત.
- પહેલાંથી પ્રકાશિત નોંધો Importer ભૂલથી દૂર કરતું નથી.
- Default Dry Run છે; `--write` સિવાય ફાઇલ બદલાતી નથી.
- `tools/check_public_feeds.py` અને GitHub CI જાહેર JSONમાં ખોટી નોંધ રોકે છે.
- News/Jobsના પેજ હાલમાં `noindex` છે; તથ્યચકાસેલા પૂરતા ઉપયોગી અપડેટ્સ થયા પછી SEO Visibility અલગ PRમાં ચકાસવું.

## 4. AdSense અને Traffic

ભ્રામક શીર્ષકો, અફવા, બિનઅધિકૃત પરીક્ષાની તારીખો, નકલ કરેલા પરિપત્રો, ભરેલા Keyword Lists અથવા Artificial Clicksથી દૂર રહેવું. વિદ્યાર્થીઓ માટે સાચું માર્ગદર્શન, કોઈ પગલું બાકી હોય તો તેની સૂચના, અને સત્તાવાર Link મૂલ્યવાન છે. AdSense મંજૂરી અથવા કોઈ આવકની ગેરંટી નથી.

Board verification: https://www.gseb.org/
Google Search helpful content: https://developers.google.com/search/docs/fundamentals/creating-helpful-content
AdSense Program Policies: https://support.google.com/adsense/answer/48182
