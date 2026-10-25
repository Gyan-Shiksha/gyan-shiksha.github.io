# જ્ઞાન શિક્ષા — સમાચાર મોનીટર પાઇલટ

આ કોડ ફક્ત નવા/સુધારેલા સમાચારનો કોપી-પેસ્ટ એલર્ટ બનાવે છે. તે તમારા admin panel, Google Sheet, `data/news.json`, quiz અથવા WhatsAppમાં લખતો નથી. અધ્યાપક સાથીની મૂળ profile બંધ છે; તેનું sending, Sheet અને live integration મુલતવી છે.

## તૈયાર થયેલો ભાગ

- GSEBના `#nav-one` News Highlights વિભાગની પસંદગી; મેનુ/બેનર અવગણે છે.
- SEBના Notice Boardમાંથી શાળા-શિષ્યવૃત્તિ સંબંધિત સૂચનાઓ; TET/TAT જેવી શિક્ષક પરીક્ષાઓ કાઢી નાખે છે.
- પ્રથમ baselineમાં જૂની સૂચનાઓની ફક્ત નોંધ; ત્યાર પછી NEW/UPDATED એલર્ટ.
- A–K admin field mapping અને એ જ સમાચારની WhatsApp પોસ્ટ.
- G છેલ્લી તારીખ હંમેશાં ખાલી; H Draft; I આપોઆપ ભરવાનું હોવાથી ખાલી; Jની નોંધ જાહેર પોસ્ટમાં નહીં.
- D મૂળ પ્રકાશન તારીખ પાનામાંથી વિશ્વસનીય રીતે મળતી નથી ત્યારે ખાલી. તમારી સાઇટની યોગ્ય પ્રકાશન તારીખ તમે પસંદ કરો. મૂળ PDFના અંદરના તમામ તથ્યોની automatic Gujarati summary આ પાઇલટ કરતો નથી; C માટે મૂળ headline આધારિત સ્પષ્ટ ટૂંકો સારાંશ આપે છે.
- PDFના તાજેતરના 12 linksમાંથી દરેક ચક્રે 2ની rotationમાં file hash તપાસે છે. એ જ URL પર PDF બદલાય તો UPDATED; માત્ર metadata બદલાવ પણ હોઈ શકે તેથી સમીક્ષા જરૂરી. જૂના બધા PDF દર ચક્રે તપાસાતા નથી.
- durable baseline/outbox અલગ `news-monitor-state` branchમાં. ઇમેલ નિષ્ફળ જાય તો pending queue જળવાય છે.
- અલગ Apps Script watchdog 90 મિનિટથી heartbeat બાકી હોય ત્યારે જાણ કરે છે; એક incident માટે વારંવાર ઇમેલ નહીં.

## સ્ત્રોતોની સ્થિતિ

| સ્ત્રોત | સ્થિતિ |
| --- | --- |
| GSEB News Highlights | parser અને મૂળ HTML તપાસેલાં; પાઇલટમાં ચાલુ |
| SEB school scholarship notices | parser અને મૂળ HTML તપાસેલાં; પાઇલટમાં ચાલુ |
| GCERT | તપાસ વખતે HTTP 503; હાલ બંધ |
| સમગ્ર શિક્ષા / UDISE+ | વિભાગ અને extraction હજી ચકાસવાનાં; હાલ બંધ |

આ સંપૂર્ણ source coverage નથી. નવી સાઇટ માટે `sources.json`માં સત્તાવાર URL, પસંદ કરેલો section અને school scopeનું પરીક્ષણ કરીને ઉમેરવું. Section ન મળે તો આખા પાનાથી સમાચાર કાઢવાનું fallback નથી.

## એક વખત ઇમેલ જોડાણ

1. જ્ઞાન શિક્ષાના Gmailથી [Google Apps Script](https://script.google.com/home)માં **નવો standalone project** બનાવો. હાલના live admin/quiz Apps Scriptમાં આ કોડ પેસ્ટ ન કરવો, કારણ કે તેમાં પોતાનું `doPost` છે.
2. `mail_relay.gs`નો કોડ પેસ્ટ કરો. `setupGyanRelay` Run કરીને જરૂરી Google permissions આપો. આ setup પોતે ઇમેલ મોકલતું નથી.
3. Project Settings → Script Propertiesમાં `GYAN_ALERT_TO` જ્ઞાન શિક્ષાનું જ Gmail છે તે જુઓ. `GYAN_RELAY_SECRET` આપમેળે બનશે. તે ફક્ત તમારા accountsમાં રાખો; ચેટ/Sheet/public repositoryમાં મૂકશો નહીં.
4. Deploy → New deployment → Web app. Execute as: **Me**. Access: **Anyone**. આ endpoint દરેક સંદેશ પર ગુપ્ત HMAC signature ચકાસે છે; અનધિકૃત request ઇમેલ મોકલી શકતી નથી.
5. GitHub repository Settings → Secrets and variables → Actions → Secretsમાં બે secrets ઉમેરો:
   - `GYAN_RELAY_URL`: Web appની `/exec` URL.
   - `GYAN_RELAY_SECRET`: ઉપરનો generated secret.
6. Workflow main branchમાં આવ્યા પછી Actions → Gyan Shiksha News Monitor → Run workflow. પહેલા `dry_run=true` રાખો: પાનાં વાંચશે, state બદલશે નહીં અને ઇમેલ મોકલશે નહીં.
7. સાચા પ્રથમ baseline માટે એક વખત `dry_run=false` ચલાવો. સફળ baseline પછી જૂની newsનો flood આવવો ન જોઈએ.
8. GitHub Actions Variablesમાં `GYAN_MONITOR_ENABLED=true` ઉમેરો. પછી schedule સામાન્ય રીતે દર અડધા કલાકે ચાલશે. GitHubનો ચોક્કસ સમયનો SLA નથી.
9. પ્રથમ સફળ baseline પછી Apps Scriptમાં `enableGyanWatchdog` એક વખત Run કરો. તે અલગ દર 30 મિનિટે heartbeat તપાસ સ્થાપે છે. main workflow અટકે તો પણ આ તપાસ સ્વતંત્ર રહી શકે છે.

GitHub connectorમાંથી Apps Script project બનાવી/deploy કરી શકાતો નથી અને GitHub secrets લખવાની ક્ષમતા પણ આ સત્રમાં નથી. તેથી ઉપરનાં owner-account પગલાં કર્યા વગર ઇમેલ સેવા ચાલુ થઈ છે એવો દાવો કરવો નહીં. credentials મળ્યા નથી એટલે અહીં actual inbox delivery પરીક્ષણ થયું નથી.

## લોકલ તપાસ

```bash
python3 -m pip install -r tools/news_monitor/requirements.txt
python3 -m unittest discover -s tools/news_monitor -p 'test_*.py' -v
node tools/news_monitor/test_relay.cjs
python3 tools/news_monitor/monitor.py scan --state /tmp/gyan-monitor/state.json --dry-run --no-pdf
```

`--dry-run` remote sources વાંચે છે પરંતુ baseline/outbox file સાચવતો નથી. `--output /tmp/gyan-monitor/preview.json`થી સંચાલક માટેની preview અલગ ફાઇલમાં લખી શકાય; તેને public websiteમાં આપોઆપ મૂકશો નહીં. tests fixture/mockથી email બનાવવાની પ્રક્રિયા ચકાસે છે અને ખરેખર email મોકલતાં નથી.

## કામગીરી અને મર્યાદા

- recipient ફક્ત private relay Script Propertiesમાંથી લેવાય છે; caller કોઈ બીજા emailને override કરી શકતો નથી. બંને brandનાં messages ભળતા નથી.
- Manual dispatchનું default dry-run છે. Schedule repository variable વડે બંધ છે જ્યાં સુધી તમે explicit enable ન કરો.
- state branchને delete ન કરવી: baseline ગુમાય તો પ્રથમ baseline ફરી બનશે. existing branchમાં state file ગાયબ/ખરાબ હોય તો job fail થાય છે, મૌન reset નથી.
- stateમાં ફક્ત સત્તાવાર સમાચારની hashes, public-source drafts અને health છે; recipient/secret નથી. Private applicant, વિદ્યાર્થી કે login data આ પાઇલટમાં નથી.
- email quota મળે તો queue રાહ જોશે; કોઈ paid fallback નથી. દુર્લભ send-success/ack-write failureમાં duplicate શક્ય છે.
- Apps Script response ખોવાય તો relayની durable receipt retryને duplicate sendથી બચાવે છે. MailApp પોતે send સ્વીકારે અને receipt store થાય તે વચ્ચે સંપૂર્ણ exactly-onceની ગેરંટી શક્ય નથી.
- scheduled workflows delay/drop થઈ શકે અને public repository inactivityથી બંધ પડી શકે. state commits વાસ્તવિક monitoring record છે; watchdog stale સ્થિતિ જણાવે છે. બધા providers એકસાથે બંધ પડે તો deliveryની ગેરંટી નથી.
- મોટા archive, CAPTCHA, JavaScript-only sites અને scan-PDF/OCR માટે અલગ verified adapter જરૂરી હોઈ શકે. એ ક્ષમતાઓ હાલ સક્રિય હોવાનું માનવું નહીં.
- સમાચાર વાંચવા/હટાવવા વચ્ચેના polling gapમાં આવતી અને દૂર થતી સૂચના ચૂકી શકે છે. મૂળ સૂચના વાંચીને જ Approved કરો.

સંબંધિત અધિકૃત મર્યાદાઓ: [GitHub schedules](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule), [GitHub billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions), [Apps Script quotas](https://developers.google.com/apps-script/guides/services/quotas).
