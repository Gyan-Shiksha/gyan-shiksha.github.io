/** Private scheduled mailer. No deployment, public endpoint or transferred key. */
function setupGyanPullMailer() {
  var p = PropertiesService.getScriptProperties();
  var owner = Session.getEffectiveUser().getEmail();
  if (!owner) throw new Error('Run as the Gyan Shiksha account owner.');
  if (!p.getProperty('GYAN_ALERT_TO')) p.setProperty('GYAN_ALERT_TO', owner);
  if (!p.getProperty('GYAN_NOTIFICATION_CURSOR')) p.setProperty('GYAN_NOTIFICATION_CURSOR', '0');
  console.log('Private mailer configured. No email sent.');
}

function startGyanPullMailer() {
  setupGyanPullMailer();
  ScriptApp.getProjectTriggers().forEach(function(t) {
    if (t.getHandlerFunction() === 'pullGyanAlerts' || t.getHandlerFunction() === 'checkGyanMonitorHeartbeat') ScriptApp.deleteTrigger(t);
  });
  ScriptApp.newTrigger('pullGyanAlerts').timeBased().everyMinutes(5).create();
  console.log('Private Gyan mail check enabled every five minutes.');
  pullGyanAlerts();
}

function readGyanState_() {
  var url = 'https://raw.githubusercontent.com/Gyan-Shiksha/gyan-shiksha.github.io/news-monitor-state/tools/news_monitor/runtime-state.json';
  var response = UrlFetchApp.fetch(url, {muteHttpExceptions:true});
  if (response.getResponseCode() !== 200) throw new Error('Monitor feed is not available: HTTP ' + response.getResponseCode());
  var state = JSON.parse(response.getContentText());
  if (state.encoding === 'gzip+base64') {
    state = JSON.parse(Utilities.ungzip(Utilities.newBlob(Utilities.base64Decode(state.data))).getDataAsString('UTF-8'));
  }
  if (state.schema !== 1 || !state.outbox || typeof state.notification_sequence !== 'number') throw new Error('Invalid monitor feed.');
  return state;
}

function pullGyanAlerts() {
  var lock = LockService.getScriptLock();
  if (!lock.tryLock(5000)) return;
  var p = PropertiesService.getScriptProperties();
  try {
    var to = p.getProperty('GYAN_ALERT_TO');
    if (!to || /[,;\r\n]/.test(to)) throw new Error('Configure the single Gyan recipient first.');
    var state = readGyanState_();
    p.setProperty('GYAN_LAST_CHECK', new Date().toISOString());
    p.deleteProperty('GYAN_LAST_ERROR');
    var cursor = Number(p.getProperty('GYAN_NOTIFICATION_CURSOR') || '0');
    if (state.notification_sequence < cursor) throw new Error('Monitor sequence was reset. Review the baseline before resetting the private cursor.');
    var events = Object.keys(state.outbox).map(function(k) { return state.outbox[k]; }).filter(function(e) {
      return e.brand === 'gyan_shiksha' && Number.isSafeInteger(e.sequence) && e.sequence > cursor;
    }).sort(function(a,b) { return a.sequence - b.sequence; });
    var sent = 0;
    for (var i = 0; i < events.length && sent < 20; i++) {
      var event = events[i];
      if (MailApp.getRemainingDailyQuota() < 1) break;
      if (!/^[a-f0-9]{64}$/.test(event.id || '') || typeof event.subject !== 'string' || /[\r\n]/.test(event.subject) || typeof event.body !== 'string') throw new Error('Invalid notification.');
      MailApp.sendEmail({to:to, subject:event.subject, body:event.body, name:'જ્ઞાન શિક્ષા એલર્ટ'});
      p.setProperty('GYAN_NOTIFICATION_CURSOR', String(event.sequence));
      sent++;
    }
    var heartbeat = Date.parse(state.last_run || '');
    var fresh = Number.isFinite(heartbeat) && Date.now() - heartbeat < 90 * 60 * 1000 && heartbeat <= Date.now() + 10 * 60 * 1000;
    var staleAlerted = p.getProperty('GYAN_MONITOR_STALE_ALERTED') === 'true';
    if (!fresh && !staleAlerted && MailApp.getRemainingDailyQuota() > 0) {
      MailApp.sendEmail({to:to, subject:'[જ્ઞાન શિક્ષા] મોનીટરની કામગીરી તપાસો', body:'છેલ્લા 90 મિનિટમાં મોનીટરની નવી કામગીરી નોંધાઈ નથી. GitHub Actions તપાસો.', name:'જ્ઞાન શિક્ષા મોનીટર'});
      p.setProperty('GYAN_MONITOR_STALE_ALERTED', 'true');
    } else if (fresh && staleAlerted && MailApp.getRemainingDailyQuota() > 0) {
      MailApp.sendEmail({to:to, subject:'[જ્ઞાન શિક્ષા] મોનીટર ફરી સમયસર કાર્યરત', body:'GitHub મોનીટરની નવી કામગીરી ફરી સમયસર નોંધાઈ છે.', name:'જ્ઞાન શિક્ષા મોનીટર'});
      p.deleteProperty('GYAN_MONITOR_STALE_ALERTED');
    }
    console.log('Private mail check complete; messages sent: ' + sent);
  } catch (error) {
    p.setProperty('GYAN_LAST_ERROR', String(error));
    console.error('Private mail check failed: ' + String(error));
    throw error;
  } finally {
    lock.releaseLock();
  }
}
