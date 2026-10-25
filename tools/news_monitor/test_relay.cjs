const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
let sent = [], props = {}, quota = 100, busy = false, heartbeat = '';
const context = {
  console,
  Session: {getEffectiveUser: () => ({getEmail: () => 'owner@example.test'})},
  PropertiesService: {getScriptProperties: () => ({getProperty: k => props[k], setProperty: (k,v) => {props[k]=v;}, getProperties: () => ({...props}), deleteProperty: k => {delete props[k];}})},
  Utilities: {getUuid: () => crypto.randomUUID(), Charset: {UTF_8:'utf8'}, computeHmacSha256Signature: (value,secret) => Array.from(crypto.createHmac('sha256',secret).update(value).digest())},
  ContentService: {MimeType: {JSON:'application/json'}, createTextOutput: s => ({setMimeType: () => JSON.parse(s)})},
  MailApp: {getRemainingDailyQuota: () => quota, sendEmail: obj => {sent.push(obj);}},
  UrlFetchApp: {fetch: () => ({getResponseCode: () => 200, getContentText: () => JSON.stringify({last_run:heartbeat})})},
  ScriptApp: {getProjectTriggers: () => [], newTrigger: () => ({timeBased: () => ({everyMinutes: () => ({create: () => {}})})})},
  LockService: {getScriptLock: () => ({tryLock: () => !busy, hasLock: () => !busy, releaseLock: () => {}})}
};
vm.createContext(context);
vm.runInContext(fs.readFileSync(path.join(__dirname,'mail_relay.gs'),'utf8'), context);
context.setupGyanRelay();
assert.equal(sent.length,0,'setup must not send email');
assert.equal(props.GYAN_ALERT_TO,'owner@example.test');
function envelope(id='a'.repeat(64), overrides={}) {
  const message={id,brand:'gyan_shiksha',subject:'પરીક્ષણ',body:'Body',...overrides};
  const timestamp=String(Math.floor(Date.now()/1000));
  const payload=JSON.stringify(message);
  const signature=crypto.createHmac('sha256',props.GYAN_RELAY_SECRET).update(timestamp+'\n'+payload).digest('hex');
  return {timestamp,payload,signature};
}
function post(obj) {return context.doPost({postData:{contents:JSON.stringify(obj)}});}
assert.equal(post(envelope()).ok,true);
assert.equal(sent.length,1);
assert.equal(post(envelope()).duplicate,true);
assert.equal(sent.length,1,'retry must be idempotent');
const wrong=envelope('b'.repeat(64)); wrong.signature='0'.repeat(64);
assert.equal(post(wrong).error,'unauthorized');
const old=envelope('b'.repeat(64)); old.timestamp='1000000000';
assert.equal(post(old).error,'expired_request');
assert.equal(post(envelope('b'.repeat(64),{brand:'adhyapak_saathi'})).error,'invalid_brand_or_id');
assert.equal(post(envelope('b'.repeat(64),{to:'wrong@example.test'})).ok,true);
assert.equal(sent[1].to,'owner@example.test','caller cannot override the recipient');
quota=0;
assert.equal(post(envelope('c'.repeat(64))).error,'email_quota');
assert.equal(props['SENT_'+'c'.repeat(64)],undefined);
quota=100; busy=true;
assert.equal(post(envelope('c'.repeat(64))).error,'busy');
busy=false;
assert.equal(post(envelope('c'.repeat(64),{subject:'bad\nheader'})).error,'invalid_message');
assert.equal(post(envelope('c'.repeat(64))).ok,true);
assert.equal(sent.length,3);
assert.equal(context.doPost({postData:{contents:'bad json'}}).error,'relay_error');
context.enableGyanWatchdog();
heartbeat='2020-01-01T00:00:00Z';
context.checkGyanMonitorHeartbeat();
context.checkGyanMonitorHeartbeat();
assert.equal(sent.length,4,'stale heartbeat sends only one incident alert');
heartbeat=new Date().toISOString();
context.checkGyanMonitorHeartbeat();
context.checkGyanMonitorHeartbeat();
assert.equal(sent.length,5,'recovery sends exactly one message');
console.log('Relay: setup, HMAC, expiry, idempotency, recipient isolation, quota and invalid-input checks passed.');
console.log('Independent watchdog: stale heartbeat suppression and recovery passed.');
