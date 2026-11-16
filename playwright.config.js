/* Playwright-Konfiguration für die E2E-Tests.
   In der CI läuft headless Chromium; WebGL wird dort über SwiftShader
   (Software-Rendering) bereitgestellt. */
const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './tests',
  timeout: 120000,
  /* SwiftShader rechnet auf der CPU: Tests sequenziell ausführen,
     damit sich die Renderlast nicht gegenseitig aushungert. */
  workers: 1,
  retries: process.env.CI ? 1 : 0,
  reporter: [
    ['list'],
    ['html', { outputFolder: 'playwright-report', open: 'never' }]
  ],
  use: {
    baseURL: 'http://127.0.0.1:8099',
    actionTimeout: 45000,
    navigationTimeout: 30000,
    screenshot: 'only-on-failure',
    launchOptions: {
      args: [
        '--enable-unsafe-swiftshader',
        '--use-gl=angle',
        '--use-angle=swiftshader',
        '--disable-dev-shm-usage'
      ]
    }
  },
  webServer: {
    /* Statischer Server für pro-skater-99.html und mapbuilder.html */
    command: 'python3 -m http.server 8099 --bind 127.0.0.1',
    url: 'http://127.0.0.1:8099/',
    reuseExistingServer: !process.env.CI,
    timeout: 20000
  },
  projects: [{ name: 'chromium', use: { browserName: 'chromium' } }]
});
