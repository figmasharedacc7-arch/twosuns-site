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
await c.send('Emulation.setDeviceMetricsOverride',{width:1440,height:1000,deviceScaleFactor:1,mobile:false});
await c.send('Page.navigate',{url:URL});await sleep(2500);
console.log('left edges of the accordion groups (should all match):');
console.log(' ', await ev(`JSON.stringify([...document.querySelectorAll('details.acc')].map(e=>Math.round(e.getBoundingClientRect().left)))`));
console.log('widths:');
console.log(' ', await ev(`JSON.stringify([...document.querySelectorAll('details.acc')].map(e=>Math.round(e.getBoundingClientRect().width)))`));
console.log('transforms still applied:', await ev(`[...document.querySelectorAll('details.acc')].filter(e=>getComputedStyle(e).transform!=='none').length`));
console.log('containers left:', await ev(`JSON.stringify([...document.querySelectorAll('section .container')].map(e=>Math.round(e.getBoundingClientRect().left)))`));
for(const [y,name] of [[0,'cap-top.png'],[900,'cap-mid.png'],[2200,'cap-low.png']]){
  await ev(`window.scrollTo({top:${y},behavior:'instant'})`); await sleep(1100);
  const r=await c.send('Page.captureScreenshot',{format:'png'});
  writeFileSync(`${DIR}/${name}`,Buffer.from(r.result.data,'base64'));
}
console.log('doc',await ev('document.documentElement.scrollWidth'),'vw',await ev('innerWidth'));
process.exit(0);
