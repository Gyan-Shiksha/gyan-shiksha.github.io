# જ્ઞાન શિક્ષા — Copyright અને Quiz Data Privacy પુરાવા સમીક્ષા

**તારીખ:** 26 ઑક્ટોબર 2026  
**સ્થિતિ:** પ્રારંભિક ટેક્નિકલ/સ્રોત તપાસ પૂર્ણ; Publisher-specific permission અને Apps Scriptના વાસ્તવિક storage rules બાકી.  
**આ રિપોર્ટ AdSense approval, કાનૂની પરવાનગી અથવા Privacy certification નથી.**

## 1. વાસ્તવિક મટીરિયલ કૅટલોગ

| વર્ગ | રેકોર્ડ | પ્રકાશક ઓળખવાની સ્થિતિ |
|---|---:|---|
| Textbook | 131 | `board=GSEB` હોવું પ્રકાશક અથવા કૉપિરાઇટ અધિકારધારકનો પુરાવો નથી |
| Question Paper | 89 | 35 `SSC` અને 54 `HSC`, મૂળ બોર્ડના publication pages ચકાસવા |
| અન્ય PDF | 2 | GSET અભ્યાસક્રમ અને નવી શિક્ષણ નીતિ — મૂળ દસ્તાવેજ તથા તેનો અધિકારધારક અલગ ચકાસવો |
| **કુલ** | **222** | મૂળ સરકારી publication URL catalogમાં **0** |

- `221` ફાઇલ-લિંક્સ `mega.nz` પર અને `1` `drive.google.com` પર છે.
- Ownerના નિવેદન પ્રમાણે PDF સરકારી વેબસાઇટ પરથી ડાઉનલોડ કરીને પોતાના MEGA/Drive પર ફરી અપલોડ કરેલી છે. આ સ્રોત સમજાવે છે, પણ પુનઃવિતરણની મંજૂરી આપતું પુરાવું નથી.
- `rights_verified=true` સર્વ 222 રેકોર્ડમાં છે; **આ flagને licence evidence માની શકાય નહીં.**
- કોઈ ફાઇલ માટે copyright violation સાબિત થયેલું નથી; કોઈ ફાઇલ ડિલીટ / અનલિંક કરવામાં આવી નથી.

## 2. પ્રાથમિક સત્તાવાર સ્રોત અને શું ખરેખર જાણીએ છીએ

1. **ગુજરાત રાજ્ય શાળા પાઠ્યપુસ્તક મંડળ:** અધિકૃત Textbook page મળી — https://gsstb.gujarat.gov.in/gsstb/Textbook . આ પેજ પાઠ્યપુસ્તકોનું પ્રવેશદ્વાર છે; સમગ્ર PDF પોતે MEGA પર ફરી અપલોડ કરવાનો સ્પષ્ટ ખુલ્લો લાઇસન્સ આ તપાસમાં મળ્યો નથી. **ફાઇલવાર સ્રોત અને મંજૂરી બાકી.**
2. **GSEB/SSC/HSC પ્રશ્નપત્રો:** `SSC` અને `HSC` tags દર્શાવે છે કે તે પરીક્ષા પ્રકાર છે. મૂળ Board exam PDFના canonical public page, publication date, upload/re-host rights ચકાસવા. `result.gseb.org` પર Copyright notice છે, પરંતુ તે સમસ્ત PDFના પુનઃવિતરણ માટે પરવાનગી આપતું પુરાવું નથી.
3. **ભારત સરકાર Copyright Office:** પાઠ્યપુસ્તકો literary worksમાં સમાવેશ થાય છે; માત્ર મફતમાં ડાઉનલોડ થઈ શકે એટલું reuse licence નથી. https://ipindia.gov.in/basics-of-copyright
4. **Google Publisher Policy:** Copyright ભંગ કરતી સામગ્રી સાથે Google જાહેરાતો મંજૂર નથી. https://support.google.com/adsense/answer/10502938
5. અન્ય સરકારી વિભાગની copyright/terms policy પ્રકાશકની ચોક્કસ રચનાને લાગુ પડે છે, દરેક વિભાગની દરેક PDF પર આપમેળે નહીં. એ બાબત માટે કોઈ એક સામાન્ય ખુલ્લું સરકારી લાઇસન્સ અનુમાનથી લાગુ ન કરવું.

## 3. Publisher Rights Review કાર્ય

- પ્રાથમિક બેચ: 131 Textbooks → શીર્ષક/ધોરણ/પ્રકાશક/મૂળ official URL અને શું PDFને બીજી જગ્યાએ ફરી અપલોડ કરી શકાય તે તપાસો.
- બીજી બેચ: 89 SSC/HSC પ્રશ્નપત્રો → અધિકૃત original exam paper link, વર્ષ/વિષય/માધ્યમ ચકાસો.
- છેલ્લી બેચ: 2 અન્ય PDFs → સાચા પ્રકાશક/પરવાનગીનું દસ્તાવેજીકરણ.
- નવી Rights CSV: GitHub Actions → Website QA → Artifacts → `material-rights-review`. Column `official_copyright_policy_url`, `original_official_source_url`, `right_to_link_or_redistribute`, `external_link_or_uploaded_copy`, `review_decision` સમીક્ષા પછી ભરો; પુરાવા વગર `APPROVED` લખશો નહીં.
- જ્યાં માલિકીની ફરી-હોસ્ટિંગની મંજૂરી ન મળી હોય ત્યાં પ્રકાશકનું મૂળ અધિકૃત Download URL પ્રાથમિક વિકલ્પ રાખવો. કૉપિરાઇટ ધારક/સ્થાનિક કાનૂની માર્ગદર્શનના આધારે જરૂરી મંજૂરી લેવી.

## 4. Quiz Saathi: ખાનગી Back-end ડેટા અંગે વાસ્તવિક તપાસ

26 ઑક્ટોબરે Connected Google Driveના `Quiz Application Backend - Smart School` (Google Sheet)માં નીચેની **read-only** તપાસ થઈ:

- `Student_Scores` ટેબ હાજર છે અને અંદર પહેલાથી ભરાયેલા વિદ્યાર્થી/શાળા-ઓળખ ધરાવતા રેકોર્ડ જોવા મળ્યા. **કોઈ વિદ્યાર્થીનું નામ, સંપર્ક કે પરિણામ આ જાહેર રિપોર્ટમાં મૂક્યું નથી.**
- Drive permission metadataમાં `owner` અને `writer` પ્રકારના બે user permissions જોવા મળ્યા. Returned permission listમાં `anyone` / `domain` public reader જણાયો નહીં. આ માત્ર તે ક્ષણનો file-level permission snapshot છે; Apps Script/અન્ય export, backend endpoints, અથવા future sharingનું સંપૂર્ણ સુરક્ષા પ્રમાણપત્ર નથી.
- `Student_Scores`માં અગાઉના રેકોર્ડ છે તેનો અર્થ **વાસ્તવિક નામ-શાળાની વિગતો ઓછામાં ઓછા ભૂતકાળમાં સેવ થયેલી છે**. માત્ર UIમાં દેખાડી અને ક્યારેય સેવ ન કરાતી નથી એવું કહી શકાય નહીં.
- સાચા નવા Quiz Submit વખતે કઈ fields લખાય છે, retention/delete policy, access boundary, તથા કાનૂની minors/guardian પ્રક્રિયા જાણવા Apps Scriptનો મૂળ source અને deployment permissions તપાસવા પડશે.
- Existing `Questions_Bank`, `Student_Scores`, `Settings`, `Quiz_Admin_Audit` વગેરે Sheets અથવા Quiz Apps Scriptમાં કોઈ write/edit/delete કરવામાં આવ્યું નથી.

### Pending Privacy Backend Decisions

1. જરૂરી હોય તે સિવાય નામ/શાળા ફરજિયાત ન રાખવા; વાસ્તવિક પરીક્ષાનો અનુભવ UIમાં અલ્પકાલિક nicknameથી પૂરો કરી શકાય કે નહીં તે નિર્ણય લેવો.
2. જો વ્યક્તિગત નામ/શાળા/સ્કોરનો ઉપયોગ ન થતો હોય તો નવા attemptમાં તે fields Google Sheetsમાં ન મોકલવા; માત્ર અનામી attempt ID અથવા aggregate score રાખવા માટે code design કરવો.
3. હાલના Student_Scores રેકોર્ડનો સંગ્રહ સમય અને access/correction/removal પ્રક્રિયા નક્કી કરવી; permission અને owner મંજૂરી વગર કોઈ record દૂર ન કરવો.
4. Students/child-directed ad treatment બાબતે AdSense account અને applicable privacy/consent requirements review કરવી. Googleના current age-treatment guidance: https://support.google.com/adsense/answer/9007197

## 5. AdSense Submission સ્થિતિ

- GitHub QA, Sitemap, Contact/About/Privacy મૂળભૂત ટેક્નિકલ તૈયારી ઉપલબ્ધ છે.
- **અરજી હજી કરી નથી.** આ રિપોર્ટ copyright/legal entitlement અથવા live quiz data policy પ્રમાણિત કરતો નથી.
- AdSense code, `ads.txt` અથવા publisher ID અણધારી રીતે ઉમેરવા નહીં. વાસ્તવિક AdSense accountની verified વિગતો જરૂરી.
- Ownerની અંતિમ અરજી મંજૂરી પહેલા proof-based rights review અને real Backend behaviourની ચકાસણી વધુ યોગ્ય છે.
