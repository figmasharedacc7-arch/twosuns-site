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
for(const [w,h,mob,name] of [[1440,950,false,'herovid-desktop.png'],[390,860,true,'herovid-mobile.png']]){
  await c.send('Emulation.setDeviceMetricsOverride',{width:w,height:h,deviceScaleFactor:1,mobile:mob});
  await c.send('Page.navigate',{url:URL});await sleep(3600);
  console.log(name.padEnd(22),
    'video playing:', await ev("(()=>{var v=document.querySelector('.hero-vid video');return v&&v.readyState>=2&&!v.paused;})()"),
    '| doc', await ev('document.documentElement.scrollWidth'), 'vw', await ev('innerWidth'));
  const r=await c.send('Page.captureScreenshot',{format:'png'});
  writeFileSync(`${DIR}/${name}`,Buffer.from(r.result.data,'base64'));
}
process.exit(0);
