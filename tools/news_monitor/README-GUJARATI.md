# જ્ઞાન શિક્ષા — ખાનગી ઇમેલ મોનીટર

આ પાઇલટ બે ભાગમાં ચાલે છે: GitHub દર અડધા કલાકે સત્તાવાર પાનાં તપાસીને એલર્ટની નોંધ બનાવે છે; તમારા Google એકાઉન્ટનું ખાનગી Apps Script દર પાંચ મિનિટે તે નોંધ વાંચીને જ્ઞાન શિક્ષાના Gmailમાં એલર્ટ મોકલે છે.

**Web app deployment, “Anyone” permission, SMTP password અથવા GitHubમાં private relay keyની જરૂર નથી.** Google script ફક્ત તમારા accountમાં time triggerથી ચાલે છે. જૂનું mail_relay.gs અને manual deliver command legacy છે; હાલનો scheduled workflow તેમનો ઉપયોગ કરતો નથી.

Admin panel, publishing Google Sheet, data/news.json, quiz અને WhatsAppમાં આ કોડ લખતો નથી. અધ્યાપક સાથીની profile disabled છે; તેનું Sheet/sending/live integration મુલતવી છે.

## તૈયાર ક્ષમતાઓ

- GSEBના પસંદ કરેલા News Highlights વિભાગની તપાસ.
- SEB Notice Boardમાંથી school-scholarship સૂચનાઓ; TET/TAT જેવી શિક્ષક પરીક્ષા બહાર.
- પ્રથમ baseline વખતે જૂની સૂચનાઓ મોકલાતી નથી; પછી NEW/UPDATED alerts.
- એડમિન માટે A–K field-wise values અને અલગ WhatsApp post.
- G છેલ્લી તારીખ ખાલી; H Draft; I આપોઆપ; Jની નોંધ public postમાં નહીં.
- મૂળ notice date વિશ્વસનીય રીતે ન મળે તો D ખાલી રહે છે. C માટે મૂળ headline આધારિત ગુજરાતી સારાંશ મળે છે; PDFનાં બધા તથ્યોનો OCR/AI સારાંશ આ પાઇલટ નથી.
- દરેક sourceના તાજેતરના 12 PDFsમાંથી દરેક ચક્રે 2નું rotationમાં hash check. માત્ર metadata બદલાયું હોય તો પણ UPDATED થઈ શકે છે, તેથી સમીક્ષા કરવી.
- state અને notifications અલગ news-monitor-state branchમાં; official-source public data જ. State gzip+base64 wrapperમાં છે જેથી કદ ઓછું રહે.
- Google script ખાનગી sequence cursor રાખે છે. વારંવાર pollingથી એ જ સંદેશ ફરી નહીં મોકલાય. Send નિષ્ફળ જાય અથવા quota ન હોય તો cursor આગળ નથી વધતો.
- Google script GitHubના stale heartbeat માટે પણ જાણ કરે છે; એક incident માટે વારંવાર સંદેશ નહીં.
- notification feedમાં 90 દિવસનું catch-up window છે; Google mailer 90 દિવસથી વધુ બંધ રહે તો જૂનાં notifications ચૂકી શકે છે.

## સ્ત્રોતો

| સ્ત્રોત | હાલની સ્થિતિ |
| --- | --- |
| GSEB News Highlights | પાઇલટમાં સક્રિય |
| SEB school scholarship notices | પાઇલટમાં સક્રિય |
| GCERT | તપાસ વખતે HTTP 503; હજી disabled |
| સમગ્ર શિક્ષા / UDISE+ | notification section અને extraction હજી verified નથી |

આ સંપૂર્ણ source coverage નથી. નવા સ્ત્રોતો ઉમેરતાં તેમની official URL, section, keywords અને પરીક્ષણ અલગથી કરવું. પસંદ કરેલો section ગાયબ થાય તો આખું page મોનીટર કરવાનું fallback નથી.

## એક વખતનું Google setup

1. જ્ઞાન શિક્ષાના Gmailમાં અલગ standalone Apps Script project રાખો. હાલમાં બનાવેલો Mail Relay project પણ વાપરી શકાય; એ જ projectના Code.gsમાં **pull_mailer.gs**નો આખો કોડ મૂકો.
2. setupGyanPullMailer Run કરો. GYAN_ALERT_TO તમારા જ્ઞાન શિક્ષાના Gmail તરફ છે તે ખાતરી કરો. Secret અથવા public deployment બનાવવાના નથી.
3. પ્રથમ GitHub baseline ઉપલબ્ધ થયા પછી startGyanPullMailer Run કરો. તે દર પાંચ મિનિટે એક private trigger સ્થાપે છે અને તરત પહેલી તપાસ પણ કરે છે.
4. Executionsમાં Completed જુઓ અને Gmailમાં સ્પષ્ટ setup-test alert મળ્યો છે તે ચકાસો.
5. GitHub schedule main branchમાં આ workflow આવ્યા પછી દર અડધા કલાકે ચાલે છે. Manual Runમાં dry_run=true ફક્ત preview કરે છે.

પહેલાના signed-relay setupમાંથી private properties રહેલી હોય તો હાલનું pull script તેમનો ઉપયોગ કરતું નથી. હાલના live admin/quiz Apps Scriptને બદલવાનું નથી.

## ચકાસણી

~~~bash
python3 -m pip install -r tools/news_monitor/requirements.txt
python3 -m unittest discover -s tools/news_monitor -p 'test_*.py' -v
node tools/news_monitor/test_pull_mailer.cjs
python3 tools/news_monitor/monitor.py scan --state /tmp/gyan-monitor/state.json --dry-run
~~~

Python tests baseline, filtering, updates, PDF checks, admin format અને state persistence તપાસે છે. Node tests compression, ordering, cursor, duplicate suppression, quota, retry, brand isolation, watchdog અને trigger તપાસે છે. Mock tests ખરેખર ઇમેલ મોકલતાં નથી.

## રોજની કામગીરી

નવું એલર્ટ મળે → મૂળ સૂચના વાંચો → જ્ઞાન શિક્ષાના adminમાં values પેસ્ટ કરો → યોગ્ય પ્રકાશન તારીખ પસંદ કરો → Approved કરો. WhatsApp postનો અલગ ભાગ તમારી ચેનલમાં પેસ્ટ કરો. Jની આંતરિક નોંધ public postમાં ન મૂકો.

મોનીટર લગભગ દર 30 મિનિટે અને mail check લગભગ દર 5 મિનિટે થાય છે. Scheduler/networkના કારણે વધુ સમય લાગી શકે છે; તાત્કાલિક deliveryનો SLA નથી. પ્રતિ ચક્ર 20 સુધી સંદેશ મોકલાય છે અને MailApp quota તપાસાય છે.

મૂળ HTML/APIથી સાઇટ પર update આવીને polling પહેલાં દૂર થઈ જાય તો તે ચૂકી શકે છે. CAPTCHA, JavaScript-only પાનાં, scan PDFs અને નવા selectors માટે અલગ adapter જરૂરી હોઈ શકે. Google/GitHubની મફત શરતો બદલાઈ શકે છે.

સંદર્ભ: [GitHub schedules](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule), [GitHub billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions), [Apps Script quotas](https://developers.google.com/apps-script/guides/services/quotas).
