import { writeFileSync } from 'node:fs';
const [,,PORT,BASE,DIR]=process.argv;
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
async function cdp(u){const ws=new WebSocket(u);await new Promise((a,b)=>{ws.onopen=a;ws.onerror=b;});
 let id=0;const w=new Map();ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id&&w.has(m.id)){w.get(m.id)(m);w.delete(m.id);}};
 return{send:(me,p={})=>new Promise(r=>{const i=++id;w.set(i,r);ws.send(JSON.stringify({id:i,method:me,params:p}));})};}
const l=await(await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
const c=await cdp(l.find(t=>t.type==='page').webSocketDebuggerUrl);
await c.send('Page.enable');await c.send('Runtime.enable');
await c.send('Emulation.setDeviceMetricsOverride',{width:1400,height:1000,deviceScaleFactor:1,mobile:false});
const jobs=[
 ['index.html',"document.querySelector('.arch').scrollIntoView({block:'center'})",'sec-arch.png'],
 ['capabilities.html',"document.querySelectorAll('details.acc')[0].open=true;document.querySelectorAll('details.acc')[0].scrollIntoView({block:'start'})",'sec-acc.png'],
 ['use-cases.html',"document.querySelector('#ucgrid').scrollIntoView({block:'start'})",'sec-uc.png'],
 ['company.html',"document.querySelectorAll('.people')[0].scrollIntoView({block:'start'})",'sec-people.png'],
 ['built-industry.html',"document.querySelector('.grid3').scrollIntoView({block:'start'})",'sec-areas.png'],
];
for(const [p,scroll,out] of jobs){
  await c.send('Page.navigate',{url:`${BASE}/${p}`});await sleep(1500);
  await c.send('Runtime.evaluate',{expression:scroll});await sleep(700);
  const r=await c.send('Page.captureScreenshot',{format:'png'});
  writeFileSync(`${DIR}/${out}`,Buffer.from(r.result.data,'base64'));
  console.log('shot',out);
}
process.exit(0);
