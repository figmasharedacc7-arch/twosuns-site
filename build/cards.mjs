import { writeFileSync } from 'node:fs';
const [,,PORT,URL,DIR]=process.argv;
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
async function cdp(u){const ws=new WebSocket(u);await new Promise((a,b)=>{ws.onopen=a;ws.onerror=b;});
 let id=0;const w=new Map();ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id&&w.has(m.id)){w.get(m.id)(m);w.delete(m.id);}};
 return{send:(me,p={})=>new Promise(r=>{const i=++id;w.set(i,r);ws.send(JSON.stringify({id:i,method:me,params:p}));})};}
const l=await(await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
const c=await cdp(l.find(t=>t.type==='page').webSocketDebuggerUrl);
await c.send('Page.enable');await c.send('Runtime.enable');
for(const [w,h,mob,y,out] of [[1440,1050,false,"document.querySelector('.grid3').scrollIntoView({block:'start'})","cards-desktop.png"],
                              [1440,1050,false,"window.scrollTo(0,document.querySelector('.grid3').offsetTop+560)","cards-desktop2.png"],
                              [390,860,true,"document.querySelector('.grid3').scrollIntoView({block:'start'})","cards-mobile.png"]]){
  await c.send('Emulation.setDeviceMetricsOverride',{width:w,height:h,deviceScaleFactor:1,mobile:mob});
  await c.send('Page.navigate',{url:URL});await sleep(2400);
  await c.send('Runtime.evaluate',{expression:y});await sleep(900);
  const r=await c.send('Page.captureScreenshot',{format:'png'});
  writeFileSync(`${DIR}/${out}`,Buffer.from(r.result.data,'base64'));console.log('shot',out);
}
process.exit(0);
