import { writeFileSync } from 'node:fs';
const [,,PORT,BASE,DIR]=process.argv;
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
async function cdp(u){const ws=new WebSocket(u);await new Promise((a,b)=>{ws.onopen=a;ws.onerror=b;});
 let id=0;const w=new Map();ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id&&w.has(m.id)){w.get(m.id)(m);w.delete(m.id);}};
 return{send:(me,p={})=>new Promise(r=>{const i=++id;w.set(i,r);ws.send(JSON.stringify({id:i,method:me,params:p}));})};}
const l=await(await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
const c=await cdp(l.find(t=>t.type==='page').webSocketDebuggerUrl);
await c.send('Page.enable');await c.send('Runtime.enable');
async function ev(x){const r=await c.send('Runtime.evaluate',{expression:x,returnByValue:true});return r.result.result?r.result.result.value:null;}
// anything on screen that is still invisible is a bug
const stuck = `(()=>{var bad=[];document.querySelectorAll('.rv *').forEach(function(e){
  var r=e.getBoundingClientRect();
  if(r.top<innerHeight-40 && r.bottom>40 && r.height>4 && getComputedStyle(e).opacity==='0') bad.push(e.className||e.tagName);
});return bad.slice(0,6).join(' | ')||'none';})()`;
for(const [page,y] of [['index',0],['index',1400],['index',3000],['built-industry',2200],['company',1600],['use-cases',1200]]){
  await c.send('Emulation.setDeviceMetricsOverride',{width:1440,height:950,deviceScaleFactor:1,mobile:false});
  await c.send('Page.navigate',{url:`${BASE}/${page}.html`});await sleep(1300);
  if(y) { await ev(`window.scrollTo({top:${y},behavior:'instant'})`); await sleep(1100); }
  console.log((page+' @'+y).padEnd(24), 'stuck invisible:', await ev(stuck));
}
await c.send('Page.navigate',{url:`${BASE}/index.html`});await sleep(1300);
await ev("window.scrollTo({top:1400,behavior:'instant'})"); await sleep(1100);
const r=await c.send('Page.captureScreenshot',{format:'png'});
writeFileSync(`${DIR}/rv-mid.png`,Buffer.from(r.result.data,'base64'));
process.exit(0);
