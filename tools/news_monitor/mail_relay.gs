/** Install in a NEW standalone Apps Script project, never the live admin project. */
function setupGyanRelay() {
  var props = PropertiesService.getScriptProperties();
  var address = Session.getEffectiveUser().getEmail();
  if (!address) throw new Error('Run setup as the owner of the Gyan Shiksha Gmail.');
  if (!props.getProperty('GYAN_ALERT_TO')) props.setProperty('GYAN_ALERT_TO', address);
  if (!props.getProperty('GYAN_RELAY_SECRET')) {
    props.setProperty('GYAN_RELAY_SECRET', Utilities.getUuid() + Utilities.getUuid());
  }
  console.log('Relay properties created. Check GYAN_ALERT_TO in Project Settings. No email sent.');
}

function relayJson_(object) {
  return ContentService.createTextOutput(JSON.stringify(object)).setMimeType(ContentService.MimeType.JSON);
}

function relayEqual_(a, b) {
  var mismatch = a.length ^ b.length;
  for (var i = 0; i < a.length; i++) mismatch |= a.charCodeAt(i) ^ (b.charCodeAt(i) || 0);
  return mismatch === 0;
}

function doPost(e) {
  var lock;
  try {
    if (!e || !e.postData || e.postData.contents.length > 70000) return relayJson_({ok:false, error:'invalid_request'});
    var request = JSON.parse(e.postData.contents);
    var stamp = String(request.timestamp || '');
    if (!/^\d{10,11}$/.test(stamp) || Math.abs(Date.now() / 1000 - Number(stamp)) > 600) return relayJson_({ok:false, error:'expired_request'});
    if (typeof request.payload !== 'string' || request.payload.length > 50000) return relayJson_({ok:false, error:'invalid_payload'});
    var props = PropertiesService.getScriptProperties();
    var secret = props.getProperty('GYAN_RELAY_SECRET');
    var to = props.getProperty('GYAN_ALERT_TO');
    if (!secret || !to || /[,;\r\n]/.test(to)) return relayJson_({ok:false, error:'not_configured'});
    var bytes = Utilities.computeHmacSha256Signature(stamp + '\n' + request.payload, secret, Utilities.Charset.UTF_8);
    var signature = bytes.map(function(b) { return ('0' + (b & 255).toString(16)).slice(-2); }).join('');
    if (!relayEqual_(signature, String(request.signature || ''))) return relayJson_({ok:false, error:'unauthorized'});
    var message = JSON.parse(request.payload);
    if (message.brand !== 'gyan_shiksha' || !/^[a-f0-9]{64}$/.test(message.id || '')) return relayJson_({ok:false, error:'invalid_brand_or_id'});
    if (typeof message.subject !== 'string' || message.subject.length > 1500 || /[\r\n]/.test(message.subject) || typeof message.body !== 'string' || message.body.length > 45000) return relayJson_({ok:false, error:'invalid_message'});
    lock = LockService.getScriptLock();
    if (!lock.tryLock(10000)) return relayJson_({ok:false, error:'busy'});
    var key = 'SENT_' + message.id;
    if (props.getProperty(key)) return relayJson_({ok:true, duplicate:true});
    if (MailApp.getRemainingDailyQuota() < 1) return relayJson_({ok:false, error:'email_quota'});
    MailApp.sendEmail({to:to, subject:message.subject, body:message.body, name:'જ્ઞાન શિક્ષા એલર્ટ'});
    props.setProperty(key, String(Date.now()));
    // Bounded idempotency journal; runner retains delivered IDs for 180 days.
    var all = props.getProperties();
    var cutoff = Date.now() - 45 * 24 * 3600 * 1000;
    Object.keys(all).forEach(function(k) { if (k.indexOf('SENT_') === 0 && Number(all[k]) < cutoff) props.deleteProperty(k); });
    return relayJson_({ok:true});
  } catch (error) {
    // Never return private credentials or the message body to an unauthenticated caller.
    return relayJson_({ok:false, error:'relay_error'});
  } finally {
    if (lock && lock.hasLock()) lock.releaseLock();
  }
}

function doGet() {
  return relayJson_({service:'Gyan Shiksha mail relay', writes_to_website:false});
}

/** Run AFTER the first successful baseline. Independent of the GitHub scheduler. */
function enableGyanWatchdog() {
  var props = PropertiesService.getScriptProperties();
  props.setProperty('GYAN_WATCHDOG_ENABLED', 'true');
  ScriptApp.getProjectTriggers().forEach(function(t) {
    if (t.getHandlerFunction() === 'checkGyanMonitorHeartbeat') ScriptApp.deleteTrigger(t);
  });
  ScriptApp.newTrigger('checkGyanMonitorHeartbeat').timeBased().everyMinutes(30).create();
  console.log('Independent heartbeat check enabled. No publishing Sheet is accessed.');
}

function checkGyanMonitorHeartbeat() {
  var props = PropertiesService.getScriptProperties();
  if (props.getProperty('GYAN_WATCHDOG_ENABLED') !== 'true') return;
  var to = props.getProperty('GYAN_ALERT_TO');
  if (!to || /[,;\r\n]/.test(to) || MailApp.getRemainingDailyQuota() < 1) return;
  var healthy = false;
  var detail = '';
  try {
    var response = UrlFetchApp.fetch('https://raw.githubusercontent.com/Gyan-Shiksha/gyan-shiksha.github.io/news-monitor-state/tools/news_monitor/runtime-state.json', {muteHttpExceptions:true});
    if (response.getResponseCode() !== 200) throw new Error('state_unavailable');
    var state = JSON.parse(response.getContentText());
    var stamp = Date.parse(state.last_run || '');
    healthy = Number.isFinite(stamp) && Date.now() - stamp < 90 * 60 * 1000 && stamp <= Date.now() + 10 * 60 * 1000;
    detail = healthy ? 'મોનીટરની છેલ્લી કામગીરી સમયસર નોંધાઈ છે.' : 'છેલ્લા 90 મિનિટમાં મોનીટરની નવી નોંધ મળી નથી. GitHub Actions અને મોનીટરનું state તપાસો.';
  } catch (error) {
    detail = 'મોનીટરની સ્થિતિ વાંચી શકાઈ નથી. આ નેટવર્ક/સેવા અથવા મોનીટરની સમસ્યા હોઈ શકે છે. GitHub Actions તપાસો.';
  }
  var alerted = props.getProperty('GYAN_WATCHDOG_ALERTED') === 'true';
  if (!healthy && !alerted) {
    MailApp.sendEmail({to:to, subject:'[જ્ઞાન શિક્ષા] મોનીટરની કામગીરી તપાસો', body:detail, name:'જ્ઞાન શિક્ષા મોનીટર'});
    props.setProperty('GYAN_WATCHDOG_ALERTED', 'true');
  } else if (healthy && alerted) {
    MailApp.sendEmail({to:to, subject:'[જ્ઞાન શિક્ષા] મોનીટરની કામગીરી ફરી સમયસર', body:detail, name:'જ્ઞાન શિક્ષા મોનીટર'});
    props.deleteProperty('GYAN_WATCHDOG_ALERTED');
  }
}
