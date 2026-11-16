/* E2E-Tests: PRO SKATER 99 (pro-skater-99.html)
   Läuft headless in Chromium; WebGL kommt in der CI über SwiftShader.

   Das Spiel bringt eigene Diagnose-Elemente mit (siehe Spiel-Quelltext):
   - Statuszeile unten links, einmal pro Sekunde aktualisiert:
     "FPS n | 3D OK | Draw n | Leinwand WxH | Kamera x y z"
   - Rote Fehlerleiste oben, sobald ein unbehandelter JS-Fehler auftritt.
   Beide Elemente haben bewusst keine ID; sie werden hier über ihren
   Inline-Style identifiziert. */
const { test, expect } = require('@playwright/test');

/* Harmlose Meldungen von Chromium im Software-Rendering, die wir ignorieren */
const JS_ERROR_NOISE = /swiftshader|groupmarker|automatic fallback|falling back to/i;

function attachErrors(collector, page) {
  page.on('pageerror', e => collector.push('pageerror: ' + (e.message || e)));
  page.on('console', m => {
    if (m.type() === 'error' && !JS_ERROR_NOISE.test(m.text())) collector.push('console: ' + m.text());
  });
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

function parseStatus(t) {
  const fps = /FPS (\d+)/.exec(t || '');
  const draw = /Draw (\d+)/.exec(t || '');
  const cam = /Kamera (-?[\d.]+) (-?[\d.]+) (-?[\d.]+)/.exec(t || '');
  return {
    text: t,
    ok: /3D OK/.test(t || ''),
    fps: fps ? Number(fps[1]) : -1,
    draw: draw ? Number(draw[1]) : -1,
    cam: cam ? [Number(cam[1]), Number(cam[2]), Number(cam[3])] : null
  };
}

/* WebGL-Kontext eines Canvas prüfen (three.js nutzt bevorzugt WebGL2) */
async function canvasAlive(page, selector) {
  return page.evaluate(sel => {
    const c = document.querySelector(sel);
    if (!c) return false;
    const gl = c.getContext('webgl2') || c.getContext('webgl') || c.getContext('experimental-webgl');
    return !!gl && !gl.isContextLost();
  }, selector);
}

/* HUD und Diagnose-Overlays ausblenden, damit das Bild nur die 3D-Szene zeigt */
async function hideOverlays(page) {
  return page.evaluate(() => {
    const hidden = [];
    const hud = document.getElementById('hud');
    if (hud) { hidden.push(hud); hud.style.display = 'none'; }
    for (const d of Array.from(document.querySelectorAll('body > div'))) {
      const fixed = d.style.position === 'fixed';
      const status = fixed && d.style.left === '0px' && d.style.bottom === '0px';
      const errBar = fixed && d.style.top === '0px' && d.style.left === '0px' && d.style.right === '0px';
      if (status || errBar) { hidden.push(d); d.style.display = 'none'; }
    }
    return hidden.length;
  });
}

/* Bildschirmfoto auswerten: mittlere Helligkeit und Anzahl unterschiedlicher
   Farbtoene (quantisiert auf 4096 Bins). Ein schwarzer Bildschirm (das
   bekannte Fehlerbild auf Mobil-Geräten) liefert nahezu keine Bins. */
async function sceneStats(page) {
  const shot = await page.screenshot();
  return page.evaluate(async b64 => {
    const img = new Image();
    img.src = 'data:image/png;base64,' + b64;
    await img.decode();
    const cv = document.createElement('canvas');
    cv.width = img.width; cv.height = img.height;
    const ctx = cv.getContext('2d');
    ctx.drawImage(img, 0, 0);
    const d = ctx.getImageData(0, 0, cv.width, cv.height).data;
    let lum = 0, dark = 0;
    const bins = new Set();
    for (let i = 0; i < d.length; i += 4) {
      const r = d[i], g = d[i + 1], b = d[i + 2];
      lum += 0.2126 * r + 0.7152 * g + 0.0722 * b;
      if (r + g + b < 24) dark++;
      bins.add(((r >> 4) << 8) | ((g >> 4) << 4) | (b >> 4));
    }
    const n = d.length / 4;
    return {
      breite: img.width, hoehe: img.height,
      meanLum: Math.round(lum / n * 10) / 10,
      darkFraction: Math.round(dark / n * 1000) / 1000,
      colorBins: bins.size
    };
  }, shot.toString('base64'));
}

async function startSession(page) {
  await page.goto('/pro-skater-99.html');
  await page.locator('#start').click();
  await expect(page.locator('#hud')).toBeVisible();
}

test('Startmenü: Seite lädt ohne JS-Fehler, 3D-Grafik wird bereit', async ({ page }) => {
  const errs = [];
  attachErrors(errs, page);
  await page.goto('/pro-skater-99.html');
  await expect(page.locator('#menu')).toBeVisible();
  /* Der Start-Button wird erst aktiv, wenn three.js geladen und der
     WebGL-Kontext initialisiert ist. Er bleibt bei einem Init-Fehler
     dauerhaft deaktiviert ("3D-START FEHLGESCHLAGEN ..."). */
  await expect(page.locator('#start')).toBeEnabled({ timeout: 60000 });
  await expect(page.locator('#start')).toHaveText('SESSION STARTEN');
  /* Es gibt auswählbare Karten im Menü */
  const chips = await page.locator('.chip:not(.soon)').count();
  expect(chips, 'Das Startmenü muss Karten anbieten').toBeGreaterThan(0);
  expect(errs, 'Keine unbehandelten JS-Fehler im Startmenü erlaubt').toEqual([]);
});

test('Karte lädt und ist sichtbar: Szene rendert, kein schwarzer Bildschirm', async ({ page }) => {
  const errs = [];
  attachErrors(errs, page);
  await startSession(page);
  /* Szene einige Sekunden rendern lassen, dann den Zustand prüfen */
  const s = parseStatus(await waitForStatus(page));
  expect(s.ok, 'Statuszeile muss "3D OK" melden: ' + s.text).toBeTruthy();
  expect(s.draw, 'Es müssen Draw-Calls stattfinden: ' + s.text).toBeGreaterThan(0);
  expect(await canvasAlive(page, '#game'), 'WebGL-Kontext des Hauptspiels muss leben').toBeTruthy();
  await expect(page.locator('#ctxlost'), 'Kontextverlust-Overlay darf nicht erscheinen').toBeHidden();
  await page.waitForTimeout(2000);
  /* Sichtbarkeit der Karte: HUD und Diagnose ausblenden und das
     tatsächliche Bild der 3D-Szene vermessen */
  await hideOverlays(page);
  const stats = await sceneStats(page);
  expect(stats.colorBins, 'Die Karte muss sichtbaren, farbigen Inhalt zeigen: ' + JSON.stringify(stats)).toBeGreaterThan(40);
  expect(stats.meanLum, 'Der Bildschirm darf nicht (nahezu) schwarz sein: ' + JSON.stringify(stats)).toBeGreaterThan(6);
  expect(stats.darkFraction, 'Fast alle Pixel dürfen nicht schwarz sein: ' + JSON.stringify(stats)).toBeLessThan(0.99);
  expect(errs).toEqual([]);
  await test.info().attach('screenshot-karte', { body: await page.screenshot(), contentType: 'image/png' });
});

test('Session: HUD sichtbar, Renderer aktiv, Draw-Calls über null', async ({ page }) => {
  const errs = [];
  attachErrors(errs, page);
  await startSession(page);
  const s = parseStatus(await waitForStatus(page));
  expect(s.ok, 'Statuszeile muss "3D OK" melden: ' + s.text).toBeTruthy();
  expect(s.draw, 'Es müssen Draw-Calls stattfinden: ' + s.text).toBeGreaterThan(0);
  expect(await canvasAlive(page, '#game'), 'WebGL-Kontext des Hauptspiels muss leben').toBeTruthy();
  await expect(page.locator('#ctxlost'), 'Kontextverlust-Overlay darf nicht erscheinen').toBeHidden();
  expect(errs).toEqual([]);
  await test.info().attach('screenshot-session', { body: await page.screenshot(), contentType: 'image/png' });
});

test('Fahrt: Beschleunigen und Ollie bewegen die Kamera, kein Fehler', async ({ page }) => {
  const errs = [];
  attachErrors(errs, page);
  await startSession(page);
  const s1 = parseStatus(await waitForStatus(page));
  expect(s1.ok).toBeTruthy();
  expect(s1.cam, 'Kameraposition muss lesbar sein: ' + s1.text).not.toBeNull();
  /* Pfeil hoch halten (Schub), nach 1,5 s ein Ollie (Leertaste) */
  await page.keyboard.down('ArrowUp');
  await page.waitForTimeout(1500);
  await page.keyboard.press('Space');
  await page.waitForTimeout(2500);
  await page.keyboard.up('ArrowUp');
  /* Mindestens eine Sekunde warten, damit die Statuszeile neu aufgebaut wurde */
  await page.waitForTimeout(1200);
  const s2 = parseStatus(await statusText(page));
  expect(s2.ok, 'Nach der Fahrt weiter "3D OK": ' + s2.text).toBeTruthy();
  expect(s2.draw, 'Spiel muss weiter zeichnen: ' + s2.text).toBeGreaterThan(0);
  expect(JSON.stringify(s2.cam), 'Kamera muss der Fahrt folgen (vorher: ' + JSON.stringify(s1.cam) + ', nachher: ' + JSON.stringify(s2.cam) + ')').not.toBe(JSON.stringify(s1.cam));
  expect(errs).toEqual([]);
});

test('Map Builder: öffnen und schließen, Haupt-3D läuft danach weiter', async ({ page }) => {
  const errs = [];
  attachErrors(errs, page);
  await startSession(page);
  const s1 = parseStatus(await waitForStatus(page));
  expect(s1.ok).toBeTruthy();
  /* Builder öffnen (identischer Codepfad wie der Startmenü-Button) */
  await page.evaluate(() => window.MB && window.MB.open());
  await expect(page.locator('#mbroot')).toBeVisible();
  await page.waitForTimeout(1500); /* Builder-Renderer hochfahren lassen */
  expect(await page.locator('#mbview canvas').count(), 'Builder braucht einen eigenen Canvas').toBeGreaterThan(0);
  expect(await canvasAlive(page, '#mbview canvas'), 'WebGL-Kontext des Builders muss leben').toBeTruthy();
  /* Schließen (identischer Codepfad wie der Close-Button): der Builder
     gibt seinen WebGL-Kontext sofort wieder frei */
  await page.evaluate(() => window.MB && window.MB.close());
  await expect(page.locator('#mbroot')).toBeHidden();
  await page.waitForTimeout(3000); /* eine volle Statusaktualisierung abwarten */
  const s2 = parseStatus(await statusText(page));
  expect(s2.ok, 'Hauptspiel muss nach dem Schließen weiter rendern (Kontext-Fix): ' + s2.text).toBeTruthy();
  expect(s2.draw, 'Draw-Calls nach Builder-Nutzung: ' + s2.text).toBeGreaterThan(0);
  await expect(page.locator('#ctxlost'), 'Kontextverlust-Overlay darf nicht erscheinen').toBeHidden();
  expect(errs).toEqual([]);
});
