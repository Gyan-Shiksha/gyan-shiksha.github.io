# જ્ઞાન શિક્ષા — Universal Material Library (અનુકૂળ અને સુરક્ષિત વ્યવસ્થા)

વેબસાઇટ: https://gyanshiksha.in/study-material.html

## આ પેજ કોઈ એક ધોરણ કે વિષય માટે નથી

કોઈપણ ધોરણ (1–12), College, Competitive Exams, Teachers અથવા સામાન્ય શૈક્ષણિક વિષય માટે PDF, ફોટો/ચાર્ટ, નોંધો, Worksheets, પ્રશ્નપત્રો, Textbooks (અધિકૃત), Presentation, Video, Audio અને અન્ય વ્યક્તિગત ફાઇલો પ્રકાશિત કરી શકાય છે.

- `data/materials.json`ની તમામ મંજૂર ફાઇલો શરૂઆતમાં જ દેખાય છે.
- ફાઇલો ઘણી થઈ જાય ત્યારે પ્રકારના બટન, ધોરણ, વિષય અને વૈકલ્પિક નામથી Search દ્વારા સરળતાથી જોઈ શકાય છે.
- ખાલી સૂચિ હોય તો ખોટા Download બટનો કે અનાવશ્યક Filters દેખાતા નથી.
- એક પણ ફાઇલનું મૂળ Drive/MEGA મુખ્ય ફોલ્ડર જાહેર થતું નથી.
- પૂર્ણ Gujarati Study Guides અને Material Request/Contribute Forms યથાવત્ છે.

## સૌથી સરળ: GitHubમાં નવી PDF / ફોટો મૂકવો (HTML લખવું નહીં)

1. પોતાની Google Driveમાં PDF, ફોટો કે અન્ય ફાઇલ Upload કરો. આખું મુખ્ય Folder `Restricted` રાખો.
2. **માત્ર તે ચોક્કસ ફાઇલ** → Share → General Access → Anyone with link → **Viewer**. Folderને ક્યારેય Public ન કરો.
3. Copy Link લો. Example: `https://drive.google.com/file/d/<REAL_FILE_ID>/view?usp=sharing`. અહીંનું `<REAL_FILE_ID>` ફક્ત ઉદાહરણ છે; આ Link પબ્લિશ કરવા માટે નથી.
4. Browser Incognitoમાં Link ખોલીને ચકાસો કે માત્ર આ જ ફાઇલ ખુલતી હોય અને કોઈ Login વગર Viewer Preview દેખાય.
5. તમારી પાસે એ ફાઇલ પ્રકાશિત/શેર કરવાની કાયદેસર મંજૂરી હોવી જરૂરી છે. બીજાના કૉપિરાઇટવાળા PDF/ફોટાને મંજૂરી વિના શેર કરશો નહીં.
6. GitHubમાં [Publish verified study material Workflow](https://github.com/Gyan-Shiksha/gyan-shiksha.github.io/actions/workflows/publish-material.yml) ખોલો. **Run workflow** પસંદ કરો.
7. Title, Standard (ધોરણ 8, College, Teacher, Competitive, General વગેરે), Subject, Type (PDF / Image વગેરે), Description (ઓછામાં ઓછા 20 અક્ષર), Copy કરેલી File Link ભરો.
8. **Rights Confirmed** checkbox ચકાસીને **Run workflow** કરો.
9. GitHub Actions સુરક્ષા ચકાસીને ફાઇલનું Meta Data `data/materials.json`માં મૂકે છે. પછી GitHub Pages Deploy થાય છે. થોડા સમય પછી Material Page Refresh કરીને જુઓ.

આ Formનો ઉપયોગ GitHub Repositoryમાં Write Permission ધરાવતા માલિક/સંપાદક જ કરી શકે છે. જાહેર Material Page પર Admin Upload Button નહીં રાખ્યો, કારણ કે Static GitHub Pages પર સુરક્ષિત Authentication વગર કોઈપણ વ્યક્તિ Website JSON બદલવા માટે સમર્થ ન થવી જોઈએ.

### MEGA ફાઇલ માટે
- ફક્ત **વ્યક્તિગત ફાઇલ** (MEGA → Share → Get link)ની Link લો: `https://mega.nz/file/...`.
- `https://mega.nz/folder/...` આખા ફોલ્ડરની Link છે, તે સ્વીકારાશે નહીં.
- File Key ધરાવતી Link જેને મળશે તે ફાઇલ જોઈ શકશે; Embed અથવા Link છુપાવવાથી Private Access મળતી નથી.

### મુખ્ય નિયમો
- Sharing કરતી વખતે Visitorની Access માટે Public **Viewer** જરૂરી હોઈ શકે છે, પણ આ File ત્યારે અન્ય લોકો આગળ પણ Share કરી શકે છે. ફાઇલને ખરેખર Private રાખવી હોય તો તેને Website પર Public ન મૂકવી.
- Drive Folder, MEGA Folder, શંકાસ્પદ Website, `javascript:` Link અને નકલી Preview URL — બધું Software QA Reject કરશે.
- JSONમાં માત્ર `Approved` અને `rights_verified: true` ફાઇલો જ દેખાશે. Source URL અને Name પણ ચકાસાશે.
- ફાઇલનો સાચો Title/Description/Subject આપો; AdSense માટે ખોટાં Download બટન, Duplicate/Low-value Content અને કૉપિરાઇટ ભંગ ટાળો.
- Google Drive અથવા MEGA File Preview નવી Tabમાં ખુલશે. Browser જાતે Preview અથવા Download આપશે; અંદર Embed કરવાથી Permission સુરક્ષિત થતી નથી.

## બીજી રીત: ખાનગી Editorial Google Sheet

https://docs.google.com/spreadsheets/d/1oxTXnrTCqbSQTtyO-428jhq-mk-LhhweWcSYAyHjmq8/edit

Materials tabમાં લખો:
- `title`: સાચું નામ
- `standard`: કોઈપણ ધોરણ/શ્રેણી
- `subject`: કોઈપણ વિષય
- `category`: PDF, Image, Notes, Question Paper, Worksheet, Textbook, Presentation, Video, Audio અથવા Other
- `description`: ફાઇલનું 20+ અક્ષરનું મૂળ વર્ણન
- `url`: ચકાસેલી વ્યક્તિગત File Link
- `updated_at`: YYYY-MM-DD
- `status`: `Approved` ફક્ત સંપાદકીય તપાસ પછી
- `copyright_checked`: `Yes` / શેર કરવાની મંજૂરી ચકાસેલી
- `editorial_notes`: Private note, તેને Public JSONમાં ક્યારેય પ્રકાશિત ન કરવી.

**Sheet હાલ Website સાથે Auto-Sync નથી.** Sheetમાં Entry કરો અને ChatGPTમાં કહો “Materials Sheetમાંથી મંજૂર ફાઇલો GitHubમાં પબ્લિશ કરો”; Assistant Connected Drive અને GitHub મારફતે સુરક્ષા તપાસીને કોડમાં ફેરફાર કરી શકે છે. અથવા ઉપરના GitHub Actionથી સીધું Self-service Publish કરો.

## Existing Quiz, News અને Jobs

- Maths Quiz તથા તેની Apps Script/Google Sheet સાથે કોઈ ફેરફાર નથી.
- News/Jobsની Editing અલગ Sheetમાં ચાલે છે; અચકાસેલી Entries આપોઆપ પ્રકાશિત થતી નથી.
- જ્ઞાન શિક્ષાના મૂળ હેતુ મુજબ વિદ્યાર્થીઓને ઉપયોગી અને Original ગુજરાતી શૈક્ષણિક Context સાથે સામગ્રી આપવી.

## GitHub QA

- `tools/add_material.py`: માત્ર Approved file-level item publish, rights confirmation, duplicate check.
- `tools/check_public_feeds.py`: Universal standard, subject, file type, HTTPS safe provider, copyright approval.
- `tools/test_material_publication.py`: અલગ sandboxમાં Good/Bad/Folder/URL/Permission ટેસ્ટ.
- `tools/check_functional_site.py`: Rendered HTML, Browse/Filters અને Internal Navigation ચકાસે છે.
