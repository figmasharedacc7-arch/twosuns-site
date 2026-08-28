import { writeFileSync } from 'node:fs';
const [,,PORT,URL,DIR]=process.argv;
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
async function cdp(u){const ws=new WebSocket(u);await new Promise((a,b)=>{ws.onopen=a;ws.onerror=b;});
 let id=0;const w=new Map();ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id&&w.has(m.id)){w.get(m.id)(m);w.delete(m.id);}};
 return{send:(me,p={})=>new Promise(r=>{const i=++id;w.set(i,r);ws.send(JSON.stringify({id:i,method:me,params:p}));})};}
const l=await(await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
const c=await cdp(l.find(t=>t.type==='page').webSocketDebuggerUrl);
await c.send('Page.enable');await c.send('Runtime.enable');
async function ev(x){const r=await c.send('Runtime.evaluate',{expression:x,returnByValue:true});return r.result.result?r.result.result.value:null;}
await c.send('Emulation.setDeviceMetricsOverride',{width:1440,height:900,deviceScaleFactor:1,mobile:false});
await c.send('Page.navigate',{url:URL});await sleep(2600);
await ev("[...document.querySelectorAll('.section-tag')].find(e=>e.textContent.includes('shift')||e.textContent.includes('SHIFT')).closest('section').scrollIntoView({block:'start'})");
await sleep(1100);
console.log('section height :', await ev("[...document.querySelectorAll('.section-tag')].find(e=>e.textContent.toLowerCase().includes('shift')).closest('section').getBoundingClientRect().height"));
console.log('paragraphs     :', await ev("[...document.querySelectorAll('.section-tag')].find(e=>e.textContent.toLowerCase().includes('shift')).closest('section').querySelectorAll('p').length"));
console.log('text visible   :', await ev("[...document.querySelectorAll('.section-tag')].find(e=>e.textContent.toLowerCase().includes('shift')).closest('section').querySelectorAll('p')[0].getBoundingClientRect().width"));
console.log('opacity        :', await ev("getComputedStyle([...document.querySelectorAll('.section-tag')].find(e=>e.textContent.toLowerCase().includes('shift')).closest('section').querySelectorAll('p')[0]).opacity"));
const r=await c.send('Page.captureScreenshot',{format:'png'});
writeFileSync(`${DIR}/shift.png`,Buffer.from(r.result.data,'base64'));
process.exit(0);
