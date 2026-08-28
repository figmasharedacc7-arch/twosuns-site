// Real device-emulated layout probe over CDP (Node 24 has a built-in WebSocket).
const PORT = process.argv[2] || '9333';
const WIDTH = parseInt(process.argv[3] || '390', 10);
const HEIGHT = parseInt(process.argv[4] || '844', 10);
const MOBILE = WIDTH < 768;
const PAGES = process.argv.slice(5);

const sleep = ms => new Promise(r => setTimeout(r, ms));

async function cdp(url) {
  const ws = new WebSocket(url);
  await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });
  let id = 0;
  const waiters = new Map();
  ws.onmessage = ev => {
    const m = JSON.parse(ev.data);
    if (m.id && waiters.has(m.id)) { waiters.get(m.id)(m); waiters.delete(m.id); }
  };
  const send = (method, params = {}) => new Promise(res => {
    const i = ++id; waiters.set(i, res);
    ws.send(JSON.stringify({ id: i, method, params }));
  });
  return { send, close: () => ws.close() };
}

const MEASURE = `(() => {
  const vw = window.innerWidth;
  const over = [];
  document.querySelectorAll('body *').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width > 0 && r.right > vw + 1) {
      over.push((el.tagName.toLowerCase()) + (el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\\s+/).slice(0,2).join('.') : '') + ' right=' + Math.round(r.right));
    }
  });
  const nt = document.querySelector('.nav-toggle');
  return JSON.stringify({
    vw, docW: document.documentElement.scrollWidth, bodyW: document.body.scrollWidth,
    overflow: document.documentElement.scrollWidth > vw + 1,
    navToggleVisible: nt ? getComputedStyle(nt).display !== 'none' : null,
    navLinksVisible: (() => { const n = document.querySelector('.nav-links'); return n ? getComputedStyle(n).display !== 'none' : null; })(),
    offenders: over.slice(0, 8),
    h1: (document.querySelector('h1') || {}).textContent
  });
})()`;

const list = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
const target = list.find(t => t.type === 'page');
const c = await cdp(target.webSocketDebuggerUrl);
await c.send('Page.enable');
await c.send('Runtime.enable');
await c.send('Emulation.setDeviceMetricsOverride', {
  width: WIDTH, height: HEIGHT, deviceScaleFactor: 2, mobile: MOBILE
});
if (MOBILE) await c.send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });

for (const p of PAGES) {
  await c.send('Page.navigate', { url: p });
  await sleep(1400);
  const r = await c.send('Runtime.evaluate', { expression: MEASURE, returnByValue: true });
  const v = JSON.parse(r.result.result.value);
  const name = p.split('/').pop() || 'index.html';
  console.log(`${name.padEnd(22)} vw:${v.vw} doc:${v.docW} overflow:${v.overflow} toggle:${v.navToggleVisible} links:${v.navLinksVisible}`);
  if (v.offenders.length) v.offenders.forEach(o => console.log('    OVER >', o));
}
c.close();
process.exit(0);
