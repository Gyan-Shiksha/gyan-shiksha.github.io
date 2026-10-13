# જ્ઞાન શિક્ષા — Study Material માં પોતે નવી ફાઇલ કેવી રીતે ઉમેરવી

વેબસાઇટ: https://gyanshiksha.in/study-material.html

## 1. સૌથી સરળ પદ્ધતિ — GitHub માં ફોર્મ ભરીને પ્રકાશિત કરો

**સામાન્ય ઉપયોગ માટે HTML, JSON, કોડ કે ChatGPT ની જરૂર નથી.** આ લિંકથી સીધું owner-only publishing form ખોલો:

**https://github.com/Gyan-Shiksha/gyan-shiksha.github.io/actions/workflows/publish-material.yml**

1. પોતાની GitHub એકાઉન્ટથી Login કરો. Repository માં Workflow ચલાવવાની પરવાનગી હોવી જોઈએ.
2. ઉપરની લિંક ખોલો → જમણે **Run workflow** દબાવો → Branch **main** પસંદ કરો; પછી વિગતો ભરવાનું ફોર્મ દેખાશે.
3. નીચેના ખાના ભરો:
   - **title:** ગુજરાતી શીર્ષક (દા.ત. `ધોરણ 8 — ગુજરાતી પાઠ્યપુસ્તક`).
   - **standard:** `1` થી `12`, અથવા ચોક્કસ અભ્યાસક્રમ (દા.ત. `Teacher`, `GSET / સ્પર્ધાત્મક પરીક્ષા`). એકસરખું નામ રાખવું.
   - **subject:** વિષય (દા.ત. `ગુજરાતી`, `ગણિત`).
   - **category:** ઉપલબ્ધ પ્રકારમાંથી એક પસંદ કરો: `Textbook`, `Question Paper`, `Notes`, `Worksheet`, `PDF`, `Image`, `Presentation`, `Video`, `Audio`, `Other`.
   - **description:** ફાઇલ વિશે વિદ્યાર્થીઓને ઉપયોગી 20–500 અક્ષરની *સાચી* માહિતી.
   - **board:** વૈકલ્પિક; `GSEB`, `GSBSTB`, `HSC`, `SSC`, `GSET`, `Other`. ન લાગુ પડતું હોય તો ખાલી રાખો.
   - **year:** વૈકલ્પિક; ફાઇલની *સાચી આવૃત્તિનું વર્ષ*, દા.ત. `2026`. ફક્ત અપલોડની તારીખ પરથી વર્ષ ન લખો.
   - **url:** માત્ર એક ફાઇલની Viewer Share Link, જેમ કે `https://mega.nz/file/...` કે `https://drive.google.com/file/d/.../view`.
   - **rights_confirmed:** ફાઇલ શેર કરવા જરૂરી કાનૂની મંજૂરી અને Incognito Viewer ચકાસણી હોય **ત્યારે જ** True કરો.
4. છેલ્લે **Run workflow** દબાવીને Action શરૂ કરો.
5. Workflow માં લીલું **✓ Success** આવે તો નવી ફાઇલ `data/materials.json` માં ઉમેરાય છે. તે પછી **pages build and deployment** પણ સફળ થાય ત્યાં સુધી રાહ જુઓ.
6. વેબસાઇટના Study Material પેજને Refresh કરીને સામગ્રીના પ્રકાર, ધોરણ અને વિષયથી ચકાસો.

GitHub ના owner/repository write access વગર બીજા મુલાકાતીઓ આ Workflow ચલાવી શકતા નથી. આ જ સુરક્ષા છે: જાહેર વેબસાઇટ પર કોઈ પણ વ્યક્તિ પ્રકાશન કરી શકે એવું form મૂક્યું નથી.

## 2. MEGA/Drive ની સાચી Link લેવી

- MEGA માં ચોક્કસ PDF/ફાઇલ → **Get link**, આખી individual-file link Copy કરો; `#` પછીનો File Key પણ લિંકનો જ ભાગ છે. MEGA **ફોલ્ડર** Share Link ન આપો.
- Drive માં ચોક્કસ ફાઇલનું Viewer Link લો. આખા ફોલ્ડરનું Sharing Public કરવાની જરૂર નથી.
- નવી Incognito/Private browser window માં Link ખોલો: માત્ર ઇચ્છિત ફાઇલ દેખાય, કોઈ ખાનગી ફોલ્ડર/વિદ્યાર્થીનું નામ નહીં અને Viewer યોગ્ય કામ કરે.
- માત્ર Link મળવાથી કૉપિરાઇટ મંજૂરી મળી જાય એવું નથી. આપણી પાસે અધિકાર, અધિકૃત લાઇસન્સ અથવા લેખિત મંજૂરી હોય ત્યારે જ Publish કરો.

## 3. સાઇટમાં કેવી રીતે દેખાશે

- નવી મંજૂર ફાઇલ પછી `બધું જુઓ`માં દેખાય છે.
- ઉપરનું **પુસ્તક / પ્રશ્નપત્ર / અન્ય PDF** વગેરે બટન પસંદ કરતાં **ધોરણ, વિષય અને વર્ષના Dropdown પણ એ જ પ્રકારની ફાઇલોમાંથી** બને છે.
- એક પેજ પર મહત્તમ **6** કાર્ડ; નવી ફાઇલો વધે તેમ પેજ નંબર આપમેળે વધશે.
- હાલમાં કોઈ ચોક્કસ પ્રકારની ફાઇલ ન હોય તો તેનો બટન દેખાતો નથી; તે પ્રકારની પ્રથમ ફાઇલ પ્રકાશિત થયા પછી બટન દેખાશે.
- Year ખાલી હોય તો તે પુસ્તક માટે Edition Year Filter લાગુ નહીં પડે; Upload Date ને Year ગણતા નથી.

## 4. ભૂલ આવે તો શું કરવું

- `duplicate file URL`: એ લિંક પહેલેથી સાઇટમાં છે. ફરી ઉમેરવાની જરૂર નથી.
- `folder` અથવા `unsafe link`: MEGA / Drive ની *વ્યક્તિગત* ફાઇલની HTTPS લિંક આપો.
- `INPUT_DESCRIPTION`: ઓછામાં ઓછાં 20 અક્ષરો લખો; માત્ર શીર્ષક પૂરતું નથી.
- `INPUT_BOARD` અથવા `INPUT_YEAR`: મંજૂર બોર્ડ/સાચું 20XX વર્ષ લખો અથવા ખાલી રાખો.
- Workflow નિષ્ફળ થાય તો લાલ **Run → Logs** ખોલીને Error વાંચો; સફળ થયા વિના પ્રકાશિત થયું છે એવું માનશો નહીં.
- GitHub Pages નો Deploy હજી ચાલુ હોય તો થોડીવાર પછી Refresh કરો.

## 5. ઘણી ફાઇલો એકસાથે ઉમેરવી (Advanced)

એક-એક ફાઇલ માટે ઉપરનું GitHub ફોર્મ સૌથી સરળ અને સલામત છે. ઘણાં પુસ્તકો માટે કમ્પ્યુટર પર `tools/import_materials_csv.py` દ્વારા મંજૂર CSV Import કરી શકો છો, પણ તેમાં GitHub branch/PR અને QAનું જ્ઞાન જરૂરી છે. આ Advanced વિકલ્પ છે; CSVને જાહેર GitHub repo માં Upload ન કરશો.

**નોંધ:** Workflow માત્ર ઉપલબ્ધ ફાઇલની લિંક અને આપેલી વિગતો ચકાસે છે; MEGA ની અંદર જઈને PDF નો વિષય અથવા કૉપિરાઇટ તે જાતે સાબિત કરી શકતું નથી. સાચી વિષય–લિંક ગોઠવણી માટે સામગ્રી ઉમેરનારની ચકાસણી જરૂરી છે. Google AdSense ને આ કામગીરી સાથે કોઈ સંબંધ નથી.
