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
  expect(errs, 'Keine unbehandelten JS-Fehler im Startmenü erlaubt').toEqual([]);
});

test('Session: HUD sichtbar, Renderer aktiv, FPS und Draw-Calls über null', async ({ page }) => {
  const errs = [];
  attachErrors(errs, page);
  await page.goto('/pro-skater-99.html');
  await page.locator('#start').click();
  await expect(page.locator('#hud')).toBeVisible();
  const s = parseStatus(await waitForStatus(page));
  expect(s.ok, 'Statuszeile muss "3D OK" melden: ' + s.text).toBeTruthy();
  expect(s.fps, 'Mindestens 1 Frame pro Sekunde nötig: ' + s.text).toBeGreaterThan(0);
  expect(s.draw, 'Es müssen Draw-Calls stattfinden: ' + s.text).toBeGreaterThan(0);
  expect(await canvasAlive(page, '#game'), 'WebGL-Kontext des Hauptspiels muss leben').toBeTruthy();
  await expect(page.locator('#ctxlost'), 'Kontextverlust-Overlay darf nicht erscheinen').toBeHidden();
  expect(errs).toEqual([]);
  await test.info().attach('screenshot-session', { body: await page.screenshot(), contentType: 'image/png' });
});

test('Fahrt: Beschleunigen und Ollie bewegen die Kamera, kein Fehler', async ({ page }) => {
  const errs = [];
  attachErrors(errs, page);
  await page.goto('/pro-skater-99.html');
  await page.locator('#start').click();
  await expect(page.locator('#hud')).toBeVisible();
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
  expect(s2.fps, 'Spiel muss weiterlaufen: ' + s2.text).toBeGreaterThan(0);
  expect(JSON.stringify(s2.cam), 'Kamera muss der Fahrt folgen (vorher: ' + JSON.stringify(s1.cam) + ', nachher: ' + JSON.stringify(s2.cam) + ')').not.toBe(JSON.stringify(s1.cam));
  expect(errs).toEqual([]);
});

test('Map Builder: öffnen und schließen, Haupt-3D läuft danach weiter', async ({ page }) => {
  const errs = [];
  attachErrors(errs, page);
  await page.goto('/pro-skater-99.html');
  await page.locator('#start').click();
  await expect(page.locator('#hud')).toBeVisible();
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
  expect(s2.fps, 'FPS nach Builder-Nutzung: ' + s2.text).toBeGreaterThan(0);
  expect(s2.draw, 'Draw-Calls nach Builder-Nutzung: ' + s2.text).toBeGreaterThan(0);
  await expect(page.locator('#ctxlost'), 'Kontextverlust-Overlay darf nicht erscheinen').toBeHidden();
  expect(errs).toEqual([]);
});
