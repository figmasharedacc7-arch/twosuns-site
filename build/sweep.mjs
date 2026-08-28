import { writeFileSync } from 'node:fs';
const [,,PORT,BASE,DIR]=process.argv;
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
async function cdp(u){const ws=new WebSocket(u);await new Promise((a,b)=>{ws.onopen=a;ws.onerror=b;});
 let id=0;const w=new Map();ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id&&w.has(m.id)){w.get(m.id)(m);w.delete(m.id);}};
 return{send:(me,p={})=>new Promise(r=>{const i=++id;w.set(i,r);ws.send(JSON.stringify({id:i,method:me,params:p}));})};}
const l=await(await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
const c=await cdp(l.find(t=>t.type==='page').webSocketDebuggerUrl);
await c.send('Page.enable');await c.send('Runtime.enable');
async function ev(x){const r=await c.send('Runtime.evaluate',{expression:x,returnByValue:true});return r.result.result?r.result.result.value:null;}
// the exact bug signature: has .in but is still invisible
const contradiction = `[...document.querySelectorAll('.rv .in')].filter(e=>getComputedStyle(e).opacity==='0').length`;
// and anything on screen still invisible
const stuck = `(()=>{var bad=[];document.querySelectorAll('.rv *').forEach(function(e){
  var r=e.getBoundingClientRect();
  if(r.top<innerHeight-40&&r.bottom>40&&r.height>4&&getComputedStyle(e).opacity==='0')bad.push((e.className||e.tagName).toString().slice(0,28));
});return bad.slice(0,4).join(' | ')||'none';})()`;
const pages=['index','platform','capabilities','built-industry','use-cases','company','discuss','privacy','terms'];
await c.send('Emulation.setDeviceMetricsOverride',{width:1440,height:1000,deviceScaleFactor:1,mobile:false});
let fails=0;
for(const p of pages){
  await c.send('Page.navigate',{url:`${BASE}/${p}.html`});await sleep(1600);
  const h=await ev('document.body.scrollHeight');
  let worst='none', contra=0;
  for(const frac of [0,0.25,0.5,0.75,0.95]){
    await ev(`window.scrollTo({top:${Math.round(h*frac)},behavior:'instant'})`);
    await sleep(950);
    const s=await ev(stuck); const k=await ev(contradiction);
    if(s!=='none') worst=s;
    contra+=k;
  }
  if(worst!=='none'||contra) fails++;
  console.log(p.padEnd(16), 'stuck:', worst.padEnd(30), 'class-but-invisible:', contra);
}
console.log('\npages with problems:', fails);
process.exit(0);
