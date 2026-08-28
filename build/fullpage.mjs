import { writeFileSync } from 'node:fs';
const [,,PORT,BASE,DIR]=process.argv;
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
async function cdp(u){const ws=new WebSocket(u);await new Promise((a,b)=>{ws.onopen=a;ws.onerror=b;});
 let id=0;const w=new Map();ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id&&w.has(m.id)){w.get(m.id)(m);w.delete(m.id);}};
 return{send:(me,p={})=>new Promise(r=>{const i=++id;w.set(i,r);ws.send(JSON.stringify({id:i,method:me,params:p}));})};}
const l=await(await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
const c=await cdp(l.find(t=>t.type==='page').webSocketDebuggerUrl);
await c.send('Page.enable');await c.send('Runtime.enable');
const pages=['index','platform','capabilities','built-industry','use-cases','company','discuss'];
await c.send('Emulation.setDeviceMetricsOverride',{width:1440,height:1200,deviceScaleFactor:1,mobile:false});
for(const p of pages){
  await c.send('Page.navigate',{url:`${BASE}/${p}.html`});
  await sleep(2600);
  // nudge lazy backgrounds into view
  await c.send('Runtime.evaluate',{expression:"window.scrollTo(0,document.body.scrollHeight);"});
  await sleep(900);
  await c.send('Runtime.evaluate',{expression:"window.scrollTo(0,0);"});
  await sleep(700);
  const h=(await c.send('Runtime.evaluate',{expression:'document.body.scrollHeight',returnByValue:true})).result.result.value;
  const r=await c.send('Page.captureScreenshot',{format:'jpeg',quality:82,captureBeyondViewport:true,
    clip:{x:0,y:0,width:1440,height:Math.min(h,14000),scale:0.26}});
  writeFileSync(`${DIR}/page-${p}.jpg`,Buffer.from(r.result.data,'base64'));
  console.log(p.padEnd(16), h+'px tall');
}
process.exit(0);
