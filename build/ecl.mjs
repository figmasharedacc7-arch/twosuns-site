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
for(const [w,h,mob,name] of [[1440,1000,false,'ecl-desktop.png'],[1024,900,false,'ecl-tablet.png'],[390,860,true,'ecl-mobile.png']]){
  await c.send('Emulation.setDeviceMetricsOverride',{width:w,height:h,deviceScaleFactor:1,mobile:mob});
  await c.send('Page.navigate',{url:URL});await sleep(2400);
  const sel = w>860 ? '.ecl' : '.ecl-fallback';
  await ev(`document.querySelector('${sel}').scrollIntoView({block:'center'})`);
  await sleep(800);
  const r=await c.send('Page.captureScreenshot',{format:'png'});
  writeFileSync(`${DIR}/${name}`,Buffer.from(r.result.data,'base64'));
  console.log(name, 'doc', await ev('document.documentElement.scrollWidth'), 'vw', await ev('innerWidth'),
    '| diagram visible:', await ev(`getComputedStyle(document.querySelector('.ecl')).display !== 'none'`),
    '| fallback visible:', await ev(`getComputedStyle(document.querySelector('.ecl-fallback')).display !== 'none'`));
}
process.exit(0);
