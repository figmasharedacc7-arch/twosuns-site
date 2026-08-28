import { writeFileSync } from 'node:fs';
const [,,PORT,BASE,DIR]=process.argv;
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
async function cdp(u){const ws=new WebSocket(u);await new Promise((a,b)=>{ws.onopen=a;ws.onerror=b;});
 let id=0;const w=new Map();ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id&&w.has(m.id)){w.get(m.id)(m);w.delete(m.id);}};
 return{send:(me,p={})=>new Promise(r=>{const i=++id;w.set(i,r);ws.send(JSON.stringify({id:i,method:me,params:p}));})};}
const l=await(await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
const c=await cdp(l.find(t=>t.type==='page').webSocketDebuggerUrl);
await c.send('Page.enable');await c.send('Runtime.enable');
const jobs=[
 ['index.html',"document.querySelector('.imgsec').scrollIntoView({block:'start'})",'med-home-photo.png'],
 ['index.html',"document.querySelector('.vidband').scrollIntoView({block:'center'})",'med-home-video.png'],
 ['built-industry.html',"window.scrollTo(0,0)",'med-bi-hero.png'],
 ['built-industry.html',"document.querySelector('.vidband').scrollIntoView({block:'center'})",'med-bi-video.png'],
 ['platform.html',"document.querySelector('.imgsec-l').scrollIntoView({block:'start'})",'med-plat-left.png'],
 ['use-cases.html',"document.querySelector('.imgsec').scrollIntoView({block:'center'})",'med-uc-photo.png'],
];
await c.send('Emulation.setDeviceMetricsOverride',{width:1440,height:900,deviceScaleFactor:1,mobile:false});
for(const [p,scroll,out] of jobs){
  await c.send('Page.navigate',{url:`${BASE}/${p}`});await sleep(2200);
  await c.send('Runtime.evaluate',{expression:scroll});await sleep(900);
  const r=await c.send('Page.captureScreenshot',{format:'png'});
  writeFileSync(`${DIR}/${out}`,Buffer.from(r.result.data,'base64'));console.log('shot',out);
}
process.exit(0);
