const [,,PORT,URL]=process.argv;
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
async function cdp(u){const ws=new WebSocket(u);await new Promise((a,b)=>{ws.onopen=a;ws.onerror=b;});
 let id=0;const w=new Map();ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id&&w.has(m.id)){w.get(m.id)(m);w.delete(m.id);}};
 return{send:(me,p={})=>new Promise(r=>{const i=++id;w.set(i,r);ws.send(JSON.stringify({id:i,method:me,params:p}));})};}
const l=await(await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
const c=await cdp(l.find(t=>t.type==='page').webSocketDebuggerUrl);
await c.send('Page.enable');await c.send('Runtime.enable');
await c.send('Emulation.setDeviceMetricsOverride',{width:1440,height:950,deviceScaleFactor:1,mobile:false});
await c.send('Page.navigate',{url:URL});await sleep(3200);
const r=await c.send('Runtime.evaluate',{returnByValue:true,expression:`
 (()=>{const q=s=>document.querySelector(s);
  const box=e=>e?{h:Math.round(e.getBoundingClientRect().height),top:Math.round(e.getBoundingClientRect().top),
                  pos:getComputedStyle(e).position}:null;
  return JSON.stringify({
    hero:box(q('.hero')), vid:box(q('.hero-vid')), video:box(q('.hero-vid video')),
    grid:box(q('.hero-grid')), sunvis:box(q('.sun-visual')), twins:box(q('.twin-suns')),
    rays:box(q('.sun-rays-svg')), copy:box(q('.hero-eyebrow'))
  },null,1);})()`});
console.log(r.result.result.value);
process.exit(0);
