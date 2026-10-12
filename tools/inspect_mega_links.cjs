/* Inspect filenames and sizes of MEGA public file URLs, WITHOUT downloading PDFs.
 * Usage: node tools/inspect_mega_links.cjs tools/pending-hsc-2023-links.txt
 * Note: these links are public by design; do not use for private files.
 */
const fs = require('node:fs');
const crypto = require('node:crypto');
const https = require('node:https');

const input = process.argv[2];
if (!input || !fs.existsSync(input)) { console.error('Provide a newline-delimited file of public MEGA file links.'); process.exit(2); }
const lines = fs.readFileSync(input, 'utf8').split(/\r?\n/).map(x=>x.trim()).filter(Boolean);
const b64 = x => Buffer.from(x.replace(/-/g,'+').replace(/_/g,'/'), 'base64');

function query(handle) {
  return new Promise((resolve,reject)=>{
    const data = JSON.stringify([{a:'g',g:1,p:handle}]);
    const req = https.request('https://g.api.mega.co.nz/cs?id=271828', {
      method:'POST',
      headers:{'Content-Type':'application/json','Content-Length':Buffer.byteLength(data)}
    }, r=>{
      let out='';
      r.setEncoding('utf8');
      r.on('data',b=>out+=b);
      r.on('end',()=>{
        try {
          if(r.statusCode!==200)throw Error('HTTP '+r.statusCode);
          const parsed=JSON.parse(out);
          const item=Array.isArray(parsed)?parsed[0]:parsed;
          if(!item || !item.at)throw Error('MEGA API returned '+JSON.stringify(item).slice(0,110));
          resolve(item);
        } catch(e){ reject(e); }
      });
    });
    req.on('error',reject);req.setTimeout(12000,()=>req.destroy(new Error('Timeout')));
    req.end(data);
  });
}

function fileName(item, encodedKey) {
  const key = b64(encodedKey);
  if(key.length!==32)throw Error('Invalid MEGA file key: '+key.length);
  const aesKey=Buffer.alloc(16);
  for(let i=0;i<16;i++)aesKey[i]=key[i]^key[i+16];
  const decipher=crypto.createDecipheriv('aes-128-cbc', aesKey, Buffer.alloc(16));
  decipher.setAutoPadding(false);
  const dec = Buffer.concat([decipher.update(b64(item.at)),decipher.final()]);
  const plaintext=dec.toString('utf8').split('\0')[0];
  if(!plaintext.startsWith('MEGA'))throw Error('Could not decrypt MEGA attributes');
  const obj=JSON.parse(plaintext.slice(4));
  if(!obj.n)throw Error('MEGA filename not found');
  return obj.n;
}
(async()=>{
  let failed=0;
  for(let i=0;i<lines.length;i++){
    try{
      const u=new URL(lines[i]);
      if(u.protocol!=='https:'||u.hostname!=='mega.nz'||!/^\/file\/[A-Za-z0-9_-]+$/.test(u.pathname))throw Error('Not an individual file link');
      const item=await query(u.pathname.split('/')[2]);
      const filename=fileName(item,u.hash.slice(1));
      console.log('FILE_METADATA',JSON.stringify({index:i+1,name:filename,size:item.s,handle:u.pathname.split('/')[2]}));
    }catch(e){failed++;console.log('FILE_METADATA_ERROR',JSON.stringify({index:i+1,error:String(e)}));}
  }
  console.log('META_TOTAL',JSON.stringify({count:lines.length,failed}));
  if(failed)process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1;});
