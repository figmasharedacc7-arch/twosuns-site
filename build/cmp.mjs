import { writeFileSync } from 'node:fs';
const [,,PORT,URL,DIR]=process.argv;
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
async function cdp(u){const ws=new WebSocket(u);await new Promise((a,b)=>{ws.onopen=a;ws.onerror=b;});
 let id=0;const w=new Map();ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id&&w.has(m.id)){w.get(m.id)(m);w.delete(m.id);}};
 return{send:(me,p={})=>new Promise(r=>{const i=++id;w.set(i,r);ws.send(JSON.stringify({id:i,method:me,params:p}));})};}
const l=await(await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
const c=await cdp(l.find(t=>t.type==='page').webSocketDebuggerUrl);
await c.send('Page.enable');await c.send('Runtime.enable');
await c.send('Emulation.setDeviceMetricsOverride',{width:1440,height:980,deviceScaleFactor:1,mobile:false});
await c.send('Page.navigate',{url:URL});await sleep(2600);
for(const [sel,out] of [[".imgsec-mat","cmp-a.png"],[".grid3","cmp-b.png"]]){
  await c.send('Runtime.evaluate',{expression:`document.querySelector('${sel}').scrollIntoView({block:'start'})`});
  await sleep(900);
  const r=await c.send('Page.captureScreenshot',{format:'png'});
  writeFileSync(`${DIR}/${out}`,Buffer.from(r.result.data,'base64'));console.log('shot',out);
}
process.exit(0);
