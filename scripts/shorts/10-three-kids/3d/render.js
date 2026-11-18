// Render stacks.html frame by frame into an mp4.
// Usage: node render.js <out_dir> [seconds]
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const http = require('http');

const out = process.argv[2];
const secs = parseFloat(process.argv[3] || '5');
const query = process.argv[4] || '';
const FPS = 30;
fs.mkdirSync(out, { recursive: true });

const root = __dirname;
const server = http.createServer((req, res) => {
  const f = path.join(root, decodeURIComponent(req.url.split('?')[0]));
  if (!f.startsWith(root) || !fs.existsSync(f)) { res.writeHead(404); return res.end(); }
  const type = f.endsWith('.js') ? 'text/javascript' : 'text/html';
  res.writeHead(200, { 'Content-Type': type }); fs.createReadStream(f).pipe(res);
}).listen(0, async () => {
  const port = server.address().port;
  const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  page.on('console', m => console.log('page:', m.text()));
  page.on('pageerror', e => console.log('error:', e.message));
  await page.goto(`http://127.0.0.1:${port}/stacks.html?${query}`);
  await page.waitForFunction('window.ready === true', null, { timeout: 30000 });
  const n = Math.round(secs * FPS);
  for (let i = 0; i < n; i++) {
    const url = await page.evaluate(t => window.renderAt(t), i / FPS);
    fs.writeFileSync(path.join(out, `f${String(i).padStart(4, '0')}.jpg`), Buffer.from(url.split(',')[1], 'base64'));
  }
  await browser.close(); server.close();
  console.log('frames', n);
});
