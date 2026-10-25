const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const zlib = require('node:zlib');
let props={},sent=[],quota=100,busy=false,failSend=false,triggers=[];
let state={schema:1,notification_sequence:0,outbox:{},last_run:new Date().toISOString()};
const context={console,
  Session:{getEffectiveUser:()=>({getEmail:()=> 'owner@example.test'})},
  PropertiesService:{getScriptProperties:()=>({getProperty:k=>props[k],setProperty:(k,v)=>{props[k]=v;},deleteProperty:k=>{delete props[k];}})},
  LockService:{getScriptLock:()=>({tryLock:()=>!busy,releaseLock:()=>{}})},
  MailApp:{getRemainingDailyQuota:()=>quota,sendEmail:m=>{if(failSend)throw new Error('delivery failed');sent.push(m);}},
  UrlFetchApp:{fetch:()=>({getResponseCode:()=>200,getContentText:()=>JSON.stringify({encoding:'gzip+base64',data:zlib.gzipSync(JSON.stringify(state)).toString('base64')})})},
  Utilities:{base64Decode:s=>Array.from(Buffer.from(s,'base64')),newBlob:(b,type)=>{assert.equal(type,'application/x-gzip','Apps Script ungzip requires a gzip content type');return Buffer.from(b);},ungzip:b=>({getDataAsString:()=>zlib.gunzipSync(b).toString('utf8')})},
  ScriptApp:{getProjectTriggers:()=>[],newTrigger:handler=>({timeBased:()=>({everyMinutes:minutes=>({create:()=>triggers.push({handler,minutes})})})})}
};
vm.createContext(context); vm.runInContext(fs.readFileSync(path.join(__dirname,'pull_mailer.gs'),'utf8'),context);
context.setupGyanPullMailer(); assert.equal(sent.length,0); assert.equal(props.GYAN_ALERT_TO,'owner@example.test');
function event(n,brand='gyan_shiksha'){return {id:String(n).padStart(64,'a'),brand,sequence:n,subject:'પરીક્ષણ '+n,body:'Body '+n};}
state.outbox={two:event(2),one:event(1)};state.notification_sequence=2;
context.pullGyanAlerts(); assert.deepEqual(sent.map(x=>x.subject),['પરીક્ષણ 1','પરીક્ષણ 2']);assert.equal(props.GYAN_NOTIFICATION_CURSOR,'2');
context.pullGyanAlerts();assert.equal(sent.length,2,'repeated polling must not resend');
state.outbox.three=event(3);state.notification_sequence=3;quota=0;context.pullGyanAlerts();assert.equal(props.GYAN_NOTIFICATION_CURSOR,'2');
quota=100;failSend=true;assert.throws(()=>context.pullGyanAlerts());assert.equal(props.GYAN_NOTIFICATION_CURSOR,'2');
failSend=false;context.pullGyanAlerts();assert.equal(sent.length,3);assert.equal(props.GYAN_NOTIFICATION_CURSOR,'3');
state.outbox.four=event(4,'adhyapak_saathi');state.notification_sequence=4;context.pullGyanAlerts();assert.equal(sent.length,3,'deferred brand must not send');
state.last_run='2020-01-01T00:00:00Z';context.pullGyanAlerts();context.pullGyanAlerts();assert.equal(sent.length,4,'one stale incident alert');
state.last_run=new Date().toISOString();context.pullGyanAlerts();context.pullGyanAlerts();assert.equal(sent.length,5,'one recovery alert');
context.startGyanPullMailer();assert.equal(triggers[0].handler,'pullGyanAlerts');assert.equal(triggers[0].minutes,5);
assert.equal(sent[0].to,'owner@example.test');
state.notification_sequence=0;assert.throws(()=>context.pullGyanAlerts(),/sequence was reset/);
console.log('Private pull mailer: compression, sequence ordering, duplicate suppression, quota, retry, brand isolation, watchdog and five-minute trigger passed.');
