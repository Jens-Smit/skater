/* E2E-Tests: Map Builder, eigenständige Version (mapbuilder.html)
   Prüft, dass der Builder vollständig initialisiert: Renderer mit
   eigenem Canvas, lebender WebGL-Kontext, Demo-Karte aufgebaut. */
const { test, expect } = require('@playwright/test');

const JS_ERROR_NOISE = /swiftshader|groupmarker|automatic fallback|falling back to/i;

function attachErrors(collector, page) {
  page.on('pageerror', e => collector.push('pageerror: ' + (e.message || e)));
  page.on('console', m => {
    if (m.type() === 'error' && !JS_ERROR_NOISE.test(m.text())) collector.push('console: ' + m.text());
  });
}

test('Standalone-Builder: lädt, rendert und zeigt die Demo-Karte an', async ({ page }) => {
  const errs = [];
  attachErrors(errs, page);
  await page.goto('/mapbuilder.html');
  /* Beim Laden erzeugt der Builder seinen Renderer und damit einen Canvas in #view */
  await page.waitForSelector('#view canvas', { timeout: 30000 });
  /* WebGL-Kontext des Builder-Canvas lebt */
  const alive = await page.evaluate(() => {
    const c = document.querySelector('#view canvas');
    if (!c) return false;
    const gl = c.getContext('webgl2') || c.getContext('webgl') || c.getContext('experimental-webgl');
    return !!gl && !gl.isContextLost();
  });
  expect(alive, 'WebGL-Kontext des Builders muss leben').toBeTruthy();
  /* Demo-Karte wurde aufgebaut: Objektzähler in der Statusleiste */
  await expect(page.locator('#stCount')).toHaveText(/[1-9]\d*/, { timeout: 15000 });
  expect(errs, 'Keine unbehandelten JS-Fehler im Builder erlaubt').toEqual([]);
  await test.info().attach('screenshot-mapbuilder', { body: await page.screenshot(), contentType: 'image/png' });
});
