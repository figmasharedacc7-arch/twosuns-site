import { writeFileSync } from 'node:fs';
const [,,PORT,BASE,DIR]=process.argv;
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
async function cdp(u){const ws=new WebSocket(u);await new Promise((a,b)=>{ws.onopen=a;ws.onerror=b;});
 let id=0;const w=new Map();ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id&&w.has(m.id)){w.get(m.id)(m);w.delete(m.id);}};
 return{send:(me,p={})=>new Promise(r=>{const i=++id;w.set(i,r);ws.send(JSON.stringify({id:i,method:me,params:p}));})};}
const l=await(await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
const c=await cdp(l.find(t=>t.type==='page').webSocketDebuggerUrl);
await c.send('Page.enable');await c.send('Runtime.enable');
await c.send('Emulation.setDeviceMetricsOverride',{width:1440,height:1100,deviceScaleFactor:1,mobile:false});
for(const [file,tag] of [['built-industry','locked'],['built-industry-alt','functional']]){
  await c.send('Page.navigate',{url:`${BASE}/${file}.html`});await sleep(2800);
  await c.send('Runtime.evaluate',{expression:"window.scrollTo(0,document.body.scrollHeight)"}); await sleep(900);
  await c.send('Runtime.evaluate',{expression:"window.scrollTo(0,0)"}); await sleep(700);
  const h=(await c.send('Runtime.evaluate',{expression:'document.body.scrollHeight',returnByValue:true})).result.result.value;
  const full=await c.send('Page.captureScreenshot',{format:'jpeg',quality:84,captureBeyondViewport:true,
    clip:{x:0,y:0,width:1440,height:Math.min(h,14000),scale:0.3}});
  writeFileSync(`${DIR}/pal-full-${tag}.jpg`,Buffer.from(full.result.data,'base64'));
  // the six area headers, where the difference actually matters
  await c.send('Runtime.evaluate',{expression:"document.querySelectorAll('.area-sec')[1].scrollIntoView({block:'start'})"});
  await sleep(700);
  let r=await c.send('Page.captureScreenshot',{format:'png'});
  writeFileSync(`${DIR}/pal-areas-${tag}.png`,Buffer.from(r.result.data,'base64'));
  // and the diagram
  await c.send('Runtime.evaluate',{expression:"document.querySelector('.ecl').scrollIntoView({block:'center'})"});
  await sleep(700);
  r=await c.send('Page.captureScreenshot',{format:'png'});
  writeFileSync(`${DIR}/pal-ecl-${tag}.png`,Buffer.from(r.result.data,'base64'));
  console.log(tag.padEnd(11), h+'px');
}
process.exit(0);
