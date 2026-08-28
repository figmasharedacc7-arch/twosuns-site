import { writeFileSync } from 'node:fs';
const [,,PORT,URL,DIR]=process.argv;
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
async function cdp(u){const ws=new WebSocket(u);await new Promise((a,b)=>{ws.onopen=a;ws.onerror=b;});
 let id=0;const w=new Map();ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id&&w.has(m.id)){w.get(m.id)(m);w.delete(m.id);}};
 return{send:(me,p={})=>new Promise(r=>{const i=++id;w.set(i,r);ws.send(JSON.stringify({id:i,method:me,params:p}));})};}
const l=await(await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
const c=await cdp(l.find(t=>t.type==='page').webSocketDebuggerUrl);
await c.send('Page.enable');await c.send('Runtime.enable');
async function ev(x){const r=await c.send('Runtime.evaluate',{expression:x,returnByValue:true});
  return r.result.result?r.result.result.value:null;}
await c.send('Emulation.setDeviceMetricsOverride',{width:1440,height:1000,deviceScaleFactor:1,mobile:false});
await c.send('Page.navigate',{url:URL});await sleep(2600);
await ev("document.querySelector('.a2wrap').scrollIntoView({block:'center'})");
await sleep(3200);   // let Ray finish typing and the auto-advance start
console.log('typed question   :', await ev("document.getElementById('a2ask').textContent.trim()"));
console.log('answer revealed  :', await ev("getComputedStyle(document.getElementById('a2ans')).opacity"));
console.log('focused layer    :', await ev("(document.querySelector('.a2.on')||{}).dataset ? document.querySelector('.a2.on').dataset.layer : 'none'"));
await sleep(200);
let r=await c.send('Page.captureScreenshot',{format:'png'});
writeFileSync(`${DIR}/pilot-auto.png`,Buffer.from(r.result.data,'base64'));
// click a selector and confirm it focuses
await ev("[...document.querySelectorAll('.a2key')].find(b=>b.dataset.key==='horizon').click()");
await sleep(700);
console.log('after clicking Horizon :', await ev("document.querySelector('.a2.on').dataset.layer"),
            '| dimmed others:', await ev("document.querySelectorAll('.a2.dim').length"));
r=await c.send('Page.captureScreenshot',{format:'png'});
writeFileSync(`${DIR}/pilot-horizon.png`,Buffer.from(r.result.data,'base64'));
console.log('doc width', await ev("document.documentElement.scrollWidth"), 'vw', await ev("window.innerWidth"));
process.exit(0);
