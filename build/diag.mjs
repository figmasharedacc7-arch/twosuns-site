const [,,PORT,URL]=process.argv;
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
async function cdp(u){const ws=new WebSocket(u);await new Promise((a,b)=>{ws.onopen=a;ws.onerror=b;});
 let id=0;const w=new Map();ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id&&w.has(m.id)){w.get(m.id)(m);w.delete(m.id);}};
 return{send:(me,p={})=>new Promise(r=>{const i=++id;w.set(i,r);ws.send(JSON.stringify({id:i,method:me,params:p}));})};}
const l=await(await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
const c=await cdp(l.find(t=>t.type==='page').webSocketDebuggerUrl);
await c.send('Page.enable');await c.send('Runtime.enable');await c.send('Log.enable');
c.send('Runtime.consoleAPICalled');
async function ev(x){const r=await c.send('Runtime.evaluate',{expression:x,returnByValue:true});
  return r.result.exceptionDetails ? 'THREW: '+r.result.exceptionDetails.text : (r.result.result?r.result.result.value:null);}
await c.send('Emulation.setDeviceMetricsOverride',{width:1440,height:1000,deviceScaleFactor:1,mobile:false});
await c.send('Page.navigate',{url:URL});await sleep(2500);
await ev("window.scrollTo({top:900,behavior:'instant'})"); await sleep(1400);
console.log('accordion opacity :', await ev(`JSON.stringify([...document.querySelectorAll('details.acc')].slice(0,4).map(e=>getComputedStyle(e).opacity))`));
console.log('accordion .in     :', await ev(`[...document.querySelectorAll('details.acc')].filter(e=>e.classList.contains('in')).length`));
console.log('accordion rects   :', await ev(`JSON.stringify([...document.querySelectorAll('details.acc')].slice(0,4).map(e=>{var r=e.getBoundingClientRect();return [Math.round(r.top),Math.round(r.height)];}))`));
console.log('section heading in:', await ev(`[...document.querySelectorAll('.section-heading')].map(e=>e.classList.contains('in'))`));
console.log('page JS errors    :', await ev("window.__err || 'none captured'"));
