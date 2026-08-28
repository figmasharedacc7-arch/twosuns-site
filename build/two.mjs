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
await c.send('Emulation.setDeviceMetricsOverride',{width:1440,height:1400,deviceScaleFactor:1,mobile:false});
await c.send('Page.navigate',{url:URL});await sleep(2800);
console.log(await ev(`(()=>{
  const S=[...document.querySelectorAll('section')];
  const shift=S.find(s=>s.textContent.includes('Enterprise software is evolving'));
  const arch=S.find(s=>s.querySelector('.arch3'));
  const box=e=>{const r=e.getBoundingClientRect();return {h:Math.round(r.height)};};
  const gap=(a,b)=>Math.round(b.getBoundingClientRect().top-a.getBoundingClientRect().bottom);
  return JSON.stringify({
    shiftHeight: box(shift).h,
    shiftPaddingBottom: getComputedStyle(shift).paddingBottom,
    archHeight: box(arch).h,
    archPaddingTop: getComputedStyle(arch).paddingTop,
    headingToBand: gap(arch.querySelector('.section-heading'), arch.querySelector('.arch3-band')),
    bandToRay: gap(arch.querySelector('.arch3-band'), arch.querySelector('.a3-ray')),
    rayToButton: gap(arch.querySelector('.a3-ray'), arch.querySelector('.btn-ghost')),
    buttonToEnd: Math.round(arch.getBoundingClientRect().bottom - arch.querySelector('.btn-ghost').getBoundingClientRect().bottom)
  },null,1);})()`));
await ev("document.querySelector('section:has(.stmt)') && document.querySelectorAll('section')[1].scrollIntoView({block:'start'})");
await sleep(1000);
const r=await c.send('Page.captureScreenshot',{format:'png'});
writeFileSync(`${DIR}/two-sections.png`,Buffer.from(r.result.data,'base64'));
process.exit(0);
