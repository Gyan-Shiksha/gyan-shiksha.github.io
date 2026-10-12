# Gyan Shiksha — અભ્યાસ સામગ્રી લાઇબ્રેરી (અદ્યતન ગોઠવણી)

**મુખ્ય સિદ્ધાંત:** ખાનગી Google Drive/MEGAના Master Folder જાહેર કરવા નહીં. વિદ્યાર્થીઓને માત્ર મંજૂર કરેલી ચોક્કસ Fileની Viewer Link બતાવવી.

## હાલ શું તૈયાર છે?
- `study-material.html`: ધોરણ 10 અને 12, વિષય પ્રમાણે અભ્યાસ માર્ગદર્શન, Search અને Filters, Material Request અને Contribute Form.
- `assets/js/material-library-v317.js`: `data/materials.json`માંથી માત્ર `Approved` ફાઇલો વાંચે છે; Drive/MEGA Folder Links અસ્વીકાર્ય છે.
- `tools/check_public_feeds.py`: વ્યક્તિગત ફાઇલને બદલે Folder URL હોય તો GitHub QA નિષ્ફળ થશે.
- `data/materials.json`: હજી ખાલી છે. ચકાસેલી ફાઇલ વગર નકલી Material બતાવશો નહીં.
- Live Quiz માટે જુદું Apps Script backend છે અને તે બદલવામાં આવ્યું નથી.

## ફાઇલ કઈ રીતે ઉમેરશો?
1. Google Drive/MEGAના મુખ્ય Folderને `Restricted` કરો.
2. પોતાની અથવા યોગ્ય પ્રકાશન-મંજૂરી ધરાવતી ચોક્કસ PDF / Docs ફાઇલ પસંદ કરો.
3. તે ફાઇલની જ `Anyone with the link → Viewer` Permission રાખો (જ્યારે જાહેર ઍક્સેસ ઇચ્છતા હોવ).
4. Incognito વિન્ડોમાં File Link ખૂલે છે અને Master Folder ખૂલતું નથી તેની ચકાસણી કરો.
5. ખાનગી Google Sheetના Materials ટૅબમાં title, standard (10/12), subject, category, description, URL, date વગેરે ભરો.
6. સંપાદકીય ચકાસણી બાદ Approved કરો; ફક્ત મંજૂર Public Details GitHubના `data/materials.json`માં પ્રકાશિત કરો.

Google Sheet: https://docs.google.com/spreadsheets/d/1oxTXnrTCqbSQTtyO-428jhq-mk-LhhweWcSYAyHjmq8/edit

**મહત્વપૂર્ણ:** આ Sheet હજી GitHub સાથે Automatic Syncમાં નથી. Sheetનું Save/Approve કરતાં જ Live Page બદલાતું નથી. Public JSONમાં મંજૂર Entry લખવાનો અલગ Publish Step જરૂરી છે. Quiz Backend Sheetને આ માટે ન બદલવી.

વિગતવાર Content/News/Jobs/AdSense SOP: `EDITORIAL-PUBLISHING-PLAN.md`.

## Embed કેમ નહીં?
માત્ર Iframe Embedથી Drive/MEGAની Permission બદલાતી નથી. ઉપરાંત અન્યની ફાઇલ/કન્ટેન્ટને પોતાની નવી માહિતી વિના Embed કરીને બનાવેલા પેજ Google AdSenseની Replicated Content અથવા Low-value Content નીતિ માટે જોખમી હોઈ શકે છે. તેથી પોતાની સમજણ અને સચોટ સૂચિ સાથે ફાઇલ-લેવલ વ્યવસ્થા શ્રેષ્ઠ.

## ફોર્મ
આ Pageના Request/Contribute Formsને અગાઉનું `assets/js/forms-v316.js` હેન્ડલ કરે છે. Apps Script End-to-End Email Confirmation અલગથી ટેસ્ટ કરવાની જરૂર છે. ટેસ્ટમાં કોઈ વિદ્યાર્થીની ખાનગી વિગતોનો ઉપયોગ કરશો નહીં.
