/* E2E-Beweisfuehrung: Karten-Screenshots.
   Fuer jede Originalkarte wird nach dem Session-Start der tatsaechlich
   gerenderte Frame aus dem WebGL-Puffer gelesen (readPixels), auf
   Sichtbarkeit geprueft und als PNG unter ci-screenshots/ gespeichert.
   Die CI committet diese Bilder ins Repository.
   Grund: Headless-Screenshots zeigen WebGL-Inhalte unter SwiftShader
   oft als leere Flaeche (Kompositing-Artefakt); der Pufferinhalt ist
   die direkte Wahrheit ueber das gezeichnete Bild. */
const { test, expect } = require('@playwright/test');
const fs = require('fs');
const path = require('path');

const KARTEN = ['tutorial', 'warehouse', 'school', 'minipark', 'funpark'];

const JS_ERROR_NOISE = /swiftshader|groupmarker|automatic fallback|falling back to/i;

function attachErrors(collector, page) {
  page.on('pageerror', e => collector.push('pageerror: ' + (e.message || e)));
  page.on('console', m => {
    if (m.type() === 'error' && !JS_ERROR_NOISE.test(m.text())) collector.push('console: ' + m.text());
  });
}

/* Wird vor dem Laden der Seite injiziert: verpackt requestAnimationFrame
   und kann auf Zuruf den Frame-Puffer des Spiels (oder Builders) lesen,
   wenden, skalieren und als PNG-Daten-URL bereitstellen. */
const HOOK = () => {
  window.__ps99 = { wantShot: false, done: false, sel: 'game', dataUrl: null, stats: null, error: null };
  const orig = window.requestAnimationFrame.bind(window);
  window.requestAnimationFrame = cb => orig(t => {
    cb(t);
    const st = window.__ps99;
    if (!st || !st.wantShot) return;
    st.wantShot = false;
    try {
      const c = st.sel === 'game' ? document.getElementById('game') : document.querySelector(st.sel);
      if (!c) { st.error = 'Canvas nicht gefunden: ' + st.sel; st.done = true; return; }
      const gl = c.getContext('webgl2') || c.getContext('webgl') || c.getContext('experimental-webgl');
      if (!gl || gl.isContextLost()) { st.error = 'Kein lebender WebGL-Kontext'; st.done = true; return; }
      const w = gl.drawingBufferWidth, h = gl.drawingBufferHeight;
      const px = new Uint8Array(w * h * 4);
      gl.readPixels(0, 0, w, h, gl.RGBA, gl.UNSIGNED_BYTE, px);
      let lum = 0, dark = 0;
      const bins = new Set();
      for (let i = 0; i < px.length; i += 4) {
        const r = px[i], g = px[i + 1], b = px[i + 2];
        lum += 0.2126 * r + 0.7152 * g + 0.0722 * b;
        if (r + g + b < 24) dark++;
        bins.add(((r >> 4) << 8) | ((g >> 4) << 4) | (b >> 4));
      }
      const n = w * h;
      const stats = {
        breite: w, hoehe: h,
        meanLum: Math.round(lum / n * 10) / 10,
        darkFraction: Math.round(dark / n * 1000) / 1000,
        colorBins: bins.size
      };
      /* Zeilen wenden (readPixels-Origin ist unten links), dann skalieren */
      const cv = document.createElement('canvas');
      cv.width = w; cv.height = h;
      const ctx = cv.getContext('2d');
      const img = ctx.createImageData(w, h);
      const row = w * 4;
      for (let y = 0; y < h; y++) img.data.set(px.subarray(y * row, (y + 1) * row), (h - 1 - y) * row);
      ctx.putImageData(img, 0, 0);
      const zw = 640, zh = Math.max(1, Math.round(h * (zw / w)));
      const small = document.createElement('canvas');
      small.width = zw; small.height = zh;
      small.getContext('2d').drawImage(cv, 0, 0, zw, zh);
      st.dataUrl = small.toDataURL('image/png');
      st.stats = stats;
      st.done = true;
    } catch (e) { st.error = String((e && e.message) || e); st.done = true; }
  });
};

/* Aufnahme mit Wiederholung: falls ein Einzelbuffer gerade geleert war,
   nochmals probieren; das beste Bild zaehlt. */
async function capture(page, attempts = 8) {
  let best = null;
  for (let i = 0; i < attempts; i++) {
    await page.evaluate(() => { const st = window.__ps99; st.done = false; st.error = null; st.wantShot = true; });
    await page.waitForFunction(() => window.__ps99 && window.__ps99.done, null, { timeout: 10000 });
    const r = await page.evaluate(() => ({ dataUrl: window.__ps99.dataUrl, stats: window.__ps99.stats, error: window.__ps99.error }));
    if (r.error) throw new Error('Aufnahme fehlgeschlagen: ' + r.error);
    if (!r.stats) throw new Error('Aufnahme ohne Messwerte');
    if (!best || r.stats.colorBins > best.stats.colorBins) best = r;
    if (r.stats.colorBins > 40 && r.stats.meanLum > 6 && r.stats.darkFraction < 0.99) return r;
  }
  return best;
}

async function speichern(shot, name) {
  const buf = Buffer.from(shot.dataUrl.split(',')[1], 'base64');
  fs.mkdirSync('ci-screenshots', { recursive: true });
  fs.writeFileSync(path.join('ci-screenshots', name + '.png'), buf);
  return { datei: 'ci-screenshots/' + name + '.png', bytes: buf.length, ...shot.stats };
}

function assertSichtbar(stats, kontext) {
  expect(stats.colorBins, kontext + ' muss sichtbaren, farbigen Inhalt zeigen: ' + JSON.stringify(stats)).toBeGreaterThan(40);
  expect(stats.meanLum, kontext + ' ist (nahezu) schwarz: ' + JSON.stringify(stats)).toBeGreaterThan(6);
  expect(stats.darkFraction, kontext + ' darf nicht fast vollstaendig schwarz sein: ' + JSON.stringify(stats)).toBeLessThan(0.99);
}

async function statusText(page) {
  return page.evaluate(() => {
    const el = Array.from(document.querySelectorAll('body > div'))
      .find(d => d.style.position === 'fixed' && d.style.left === '0px' && d.style.bottom === '0px');
    return el ? el.textContent : null;
  });
}

async function waitForStatus(page, timeout = 30000) {
  await page.waitForFunction(() => {
    const el = Array.from(document.querySelectorAll('body > div'))
      .find(d => d.style.position === 'fixed' && d.style.left === '0px' && d.style.bottom === '0px');
    return !!el && /^FPS \d+/.test(el.textContent);
  }, null, { timeout });
  return statusText(page);
}

const ergebnisse = [];

for (const map of KARTEN) {
  test(`Karte ${map} laedt und ist sichtbar (Screenshot als Beleg)`, async ({ page }) => {
    const errs = [];
    attachErrors(errs, page);
    await page.addInitScript(HOOK);
    await page.goto('/pro-skater-99.html');
    await expect(page.locator('#start')).toBeEnabled({ timeout: 60000 });
    /* Karte im Startmenue auswaehlen und Session starten */
    await page.locator(`[data-map="${map}"]`).click();
    await expect(page.locator(`[data-map="${map}"]`)).toHaveClass(/on/);
    await page.locator('#start').click();
    await expect(page.locator('#hud')).toBeVisible();
    const s = await waitForStatus(page);
    expect(/3D OK/.test(s), 'Statuszeile muss "3D OK" melden: ' + s).toBeTruthy();
    expect(/Draw [1-9]/.test(s), 'Es muessen Draw-Calls stattfinden: ' + s).toBeTruthy();
    await page.waitForTimeout(1500);
    /* Gerenderten Frame aufnehmen und pruefen */
    const shot = await capture(page);
    assertSichtbar(shot.stats, 'Karte ' + map);
    const info = await speichern(shot, map);
    ergebnisse.push(info);
    console.log('KARTEN-SCREENSHOT ' + map + ': ' + JSON.stringify(info));
    await test.info().attach('screenshot-' + map, { body: Buffer.from(shot.dataUrl.split(',')[1], 'base64'), contentType: 'image/png' });
    expect(errs, 'Keine unbehandelten JS-Fehler erlaubt').toEqual([]);
  });
}

test('Map-Builder-Demo-Karte laedt und ist sichtbar (Screenshot als Beleg)', async ({ page }) => {
  const errs = [];
  attachErrors(errs, page);
  await page.addInitScript(HOOK);
  await page.goto('/mapbuilder.html');
  await page.waitForSelector('#view canvas', { timeout: 30000 });
  await expect(page.locator('#stCount')).toHaveText(/[1-9]\d*/, { timeout: 15000 });
  await page.evaluate(() => { window.__ps99.sel = '#view canvas'; });
  await page.waitForTimeout(1000);
  const shot = await capture(page);
  assertSichtbar(shot.stats, 'Builder-Demo-Karte');
  const info = await speichern(shot, 'builder-demo');
  ergebnisse.push(info);
  console.log('KARTEN-SCREENSHOT builder-demo: ' + JSON.stringify(info));
  await test.info().attach('screenshot-builder-demo', { body: Buffer.from(shot.dataUrl.split(',')[1], 'base64'), contentType: 'image/png' });
  expect(errs, 'Keine unbehandelten JS-Fehler erlaubt').toEqual([]);
});

test.afterAll(() => {
  if (ergebnisse.length) console.log('KARTEN-SCREENSHOTS: ' + JSON.stringify(ergebnisse));
});
