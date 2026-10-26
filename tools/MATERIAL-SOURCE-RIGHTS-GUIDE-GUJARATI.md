# જ્ઞાન શિક્ષા — સરકારી મટીરિયલના મૂળ સ્ત્રોત અને અધિકાર ચકાસણી

**તારીખ:** 26 ઑક્ટોબર 2026
**હેતુ:** AdSense પહેલાં કૉપિરાઇટ / સ્રોત પુરાવા ગોઠવવા; કાનૂની પ્રમાણપત્ર કે Google approval નથી.

## આજે મળેલી નોંધ
- `data/materials.json`માં **222 રેકોર્ડ**: 131 પાઠ્યપુસ્તક, 89 પ્રશ્નપત્ર, 2 અન્ય PDF.
- ફાઇલો ખોલવાની લિંક્સ **221 mega.nz** અને **1 drive.google.com** પર છે.
- `rights_verified: true` એ અગાઉ નોંધાયેલો ફ્લેગ છે; મૂળ સરકારી સ્ત્રોતનો દસ્તાવેજ કે પુનઃપ્રકાશનની પરવાનગી નથી.
- મૂળ સરકારી વેબસાઇટની URL/કૉપિરાઇટ નીતિ હાલમાં catalogમાં રેકોર્ડ કરવામાં આવી નથી. કોઈ લિંક આપમેળે ગેરકાયદેસર ગણાતી નથી; પ્રમાણની સમીક્ષા બાકી છે.

## કયા પુરાવા કામ આવે? (દરેક પ્રકાર / પ્રકાશક માટે)

1. **મૂળ સત્તાવાર પેજ:** પ્રશ્નપત્ર કે પુસ્તક જે સરકારી/બોર્ડની અધિકૃત વેબસાઇટ પર પ્રકાશિત થયું હોય તેની સાચી URL. MEGA/Drive ફાઇલ URL મૂળ પ્રકાશકની URL નથી.
2. **પ્રકાશક/અધિકારધારક:** GSEB, GCERT, NCERT કે અન્યની ખરેખર ઓળખ PDF અથવા અધિકૃત પેજમાંથી. શીર્ષક પરથી અંદાજ ન લગાવો.
3. **કૉપિરાઇટ શરતો:** એ જ સંબંધિત પ્રકાશકની Copyright/Terms/Open Licence ની સ્થાયી URL, ત્યાં લાગુ પડતું વર્ઝન/તારીખ અને સંક્ષિપ્ત સાર. અન્ય વિભાગની સરકારી Copyright Policy અહીં આપમેળે લાગુ પડતી નથી.
4. **શું કરવામાં આવ્યું છે:** માત્ર મૂળ અધિકૃત URL પર **લિંક**, કે PDFની **નકલ અપલોડ/રીહોસ્ટ** કરવામાં આવી છે? ફક્ત મફત ડાઉનલોડ થવાનું પુનર્વિતરણનું લાઇસન્સ નથી.
5. **ત્રીજા પક્ષની સામગ્રી:** Government site પર પણ તૃતીય-પક્ષ કૉપિરાઇટ / NCERT જેવી વિશેષ મર્યાદા હોય શકે છે.
6. **દસ્તાવેજિત નિર્ણય:** `OFFICIAL_DIRECT_LINK`, `REUSE_ALLOWED_WITH_ATTRIBUTION`, `WRITTEN_PERMISSION`, `RESTRICTED_REHOST`, અથવા `PENDING`. સંદિગ્ધ પુનઃપ્રકાશનની ફાઇલ માટે સત્તાવાર લિંક ઉપલબ્ધ હોય તો તે તરફ મોકલવાનું પ્રાધાન્ય આપવું.

## કાર્યપદ્ધતિ

1. GitHub Actions → **Gyan Shiksha Website QA** → **Artifacts** → `material-rights-review` ડાઉનલોડ કરો. CSVમાં દરેક 222 રેકોર્ડની row છે.
2. પહેલા **પ્રકાશક/વર્ગ** મુજબ સરકારી source તપાસો; એક જ નીતિ લાગુ પડે છે કે નહીં તે દરેક મટીરિયલના અધિકારધારક સાથે સરખાવો.
3. CSVના `original_official_source_url`, `publisher_board_or_department`, `official_copyright_policy_url`, `right_to_link_or_redistribute`, `external_link_or_uploaded_copy`, `third_party_copyright_exception_checked`, `review_decision` પૂર્ણ કરો.
4. પ્રમાણ તરીકે મૂળ વેબપેજ/PDF/કૉપિરાઇટ શરતોના date-સહિત screenshots અથવા link+retrieval date ખાનગી અધિકૃત ફોલ્ડરમાં રાખો. વ્યક્તિગત, અનધિકૃત PDF અથવા passwords GitHubના public repoમાં ન નાખો.
5. જ્યાં પરવાનગી અનિશ્ચિત હોય ત્યાં પહેલા યોગ્ય સત્તાવાર original link શોધો અથવા અધિકારધારક પાસેથી સ્પષ્ટ પરવાનગી લો. માત્ર checkbox અથવા `rights_verified` flagથી મંજૂરી ન માનો.
6. લેખોની મૂળ ગુજરાતી સમજૂતી, ઉકેલેલા દાખલા, પ્રકરણ આધારિત માર્ગદર્શન અને સાચા official source citations વધારતા રહો; માત્ર download links AdSense માટે પૂરતી મૂળ શૈક્ષણિક કિંમત સાબિત કરતી નથી.

## Search Console અને વિદ્યાર્થી ડેટા — બાકી માનવીય ચકાસણી

- `admin.html`માં Search Consoleની **authenticated link** છે, અંદર live Google Search Console API data embed નથી. Google accountમાં **Pages**, **Sitemaps**, **Performance** અલગથી તપાસો.
- Quiz Saathi હાલ બાહ્ય Google Apps Script પર ચાલે છે. વિદ્યાર્થીનું નામ/શાળાનું નામ માત્ર વાસ્તવિક પરીક્ષા જેવો અનુભવ આપવા માટે હોય તો backendની actual saving, access controls, retention/deletion પણ તદ્દન ચકાસો.
- બાળકો/વિદ્યાર્થીઓ માટે personalised ads અને consent સંબંધિત Google Publisher Policies અરજી પહેલાં અનુસરો; અજાણી publisher ID/ads.txt/AdSense tag ઉમેરશો નહીં.

## આધારો
- Google Publisher Policies: https://support.google.com/adsense/answer/10502938
- Google AdSense Program Policies: https://support.google.com/adsense/answer/48182
- Government of India Department of School Education Copyright Policy (દૃષ્ટાંત; બધા પ્રકાશકોને લાગુ પડતી મંજૂરી નથી): https://master-dsel-education.digifootprint.gov.in/policies/copyright-policy

**આ દસ્તાવેજ workflow માટે છે; 222 ફાઇલોની પરવાનગી ચકાસાઈ ગઈ એવો દાવો નથી.**
