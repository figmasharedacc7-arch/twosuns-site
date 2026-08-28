// Behaviour + real-device screenshot probe over CDP.
import { writeFileSync } from 'node:fs';
const PORT = process.argv[2] || '9333';
const BASE = process.argv[3];
const SHOTDIR = process.argv[4];
const sleep = ms => new Promise(r => setTimeout(r, ms));

async function cdp(url) {
  const ws = new WebSocket(url);
  await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });
  let id = 0; const waiters = new Map();
  ws.onmessage = ev => { const m = JSON.parse(ev.data);
    if (m.id && waiters.has(m.id)) { waiters.get(m.id)(m); waiters.delete(m.id); } };
  return { send: (method, params = {}) => new Promise(res => {
    const i = ++id; waiters.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); }),
    close: () => ws.close() };
}

const list = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
const c = await cdp(list.find(t => t.type === 'page').webSocketDebuggerUrl);
await c.send('Page.enable'); await c.send('Runtime.enable');

async function go(url, w, h, mobile) {
  await c.send('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: 1, mobile });
  await c.send('Page.navigate', { url });
  await sleep(1500);
}
async function ev(expr) {
  const r = await c.send('Runtime.evaluate', { expression: expr, returnByValue: true, awaitPromise: true });
  return r.result.result ? r.result.result.value : r.result;
}
async function shot(name) {
  const r = await c.send('Page.captureScreenshot', { format: 'png' });
  writeFileSync(`${SHOTDIR}/${name}`, Buffer.from(r.result.data, 'base64'));
}

// 1. Use case filter
await go(`${BASE}/use-cases.html`, 1400, 1000, false);
console.log('use-cases total cards      :', await ev(`document.querySelectorAll('#ucgrid .uc').length`));
console.log('counter text               :', await ev(`document.getElementById('uccount').textContent`));
await ev(`[...document.querySelectorAll('.uc-filter')].find(b=>b.textContent.trim()==='Horizon').click()`);
await sleep(300);
console.log('after Horizon filter       :', await ev(`[...document.querySelectorAll('#ucgrid .uc')].filter(c=>c.style.display!=='none').length`),
            '|', await ev(`document.getElementById('uccount').textContent`));
await ev(`[...document.querySelectorAll('.uc-filter')].find(b=>b.textContent.trim()==='Pulse').click()`);
await sleep(300);
console.log('after Pulse filter         :', await ev(`[...document.querySelectorAll('#ucgrid .uc')].filter(c=>c.style.display!=='none').length`));

// 2. Capabilities accordion
await go(`${BASE}/capabilities.html`, 1400, 1000, false);
console.log('accordion groups           :', await ev(`document.querySelectorAll('details.acc').length`));
console.log('bullets inside all groups  :', await ev(`document.querySelectorAll('details.acc .tick li').length`));
await ev(`document.querySelector('details.acc').open = true`);
await sleep(200);
console.log('first group opens          :', await ev(`document.querySelector('details.acc').open`));

// 3. Discuss form context capture
await go(`${BASE}/discuss.html?ask=Request+a+Product+Demonstration&from=platform.html`, 1400, 1100, false);
console.log('context chip visible       :', await ev(`getComputedStyle(document.getElementById('ctxchip')).display !== 'none'`));
console.log('context chip text          :', await ev(`document.getElementById('ctxchip').textContent`));
console.log('required fields present    :', await ev(`['name','company','job_title','email','area','message','attachment'].filter(n=>document.discussForm ? false : !!document.getElementById('discussForm').elements[n]).join(', ')`));
await shot('cdp-discuss-desktop.png');

// 4. Mobile nav toggle
await go(`${BASE}/index.html`, 390, 844, true);
console.log('mobile menu closed         :', await ev(`getComputedStyle(document.getElementById('navlinks')).display`));
await ev(`document.querySelector('.nav-toggle').click()`);
await sleep(300);
console.log('mobile menu after tap      :', await ev(`getComputedStyle(document.getElementById('navlinks')).display`),
            '| items:', await ev(`document.querySelectorAll('#navlinks a').length`));
await shot('cdp-mobile-menu.png');
await ev(`document.querySelector('.nav-toggle').click()`);
await sleep(200);
await shot('cdp-mobile-home.png');

await go(`${BASE}/use-cases.html`, 390, 900, true);
await shot('cdp-mobile-usecases.png');

c.close(); process.exit(0);
