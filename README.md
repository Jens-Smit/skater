# PRO SKATER 99 - Warehouse Sessions Pro

Skateboard-Spiel (three.js) als eigenstaendige HTML-Datei mit Neigungsphysik, Tricks, Vert-Rampen, Bowls, eingebettetem Map Builder und E2E-Tests. Der Skater wird als echtes 3D-Charaktermodell angezeigt (Mixamo-Charakter \"Remy\", siehe unten).

## Spielen

`pro-skater-99.html` herunterladen oder raw oeffnen und im Browser starten. Kein Build, keine Installation; three.js ist eingebettet. Das Spiel laedt die Spielfigur und optionale Assets beim Start nach (Internetverbindung noetig, sonst greift der stilisierte Fallback-Skater).

## Dateien

- `pro-skater-99.html`: das vollstaendige Spiel (Skatepark, Physik, Tricks, Map Builder im Startmenue)
- `mapbuilder.html`: eigenstaendige Version des Map Builders (der aktuellste Builder ist in pro-skater-99.html eingebettet)
- `assets/remy/`: Spielfigur \"Remy\" als reine Textfragmente (glTF-JSON + Base64-Bloecke), im Spiel zusammengesetzt
- `tests/`, `playwright.config.js`, `package.json`: Playwright-E2E-Tests
- `.github/workflows/e2e.yml`: GitHub-Actions-Workflow

## E2E-Tests

Die Tests laufen mit Playwright in GitHub Actions (headless Chromium, WebGL ueber SwiftShader) bei jedem Push auf `main`. Der vollstaendige Report mit Screenshots liegt als Artefakt `playwright-report` beim jeweiligen Lauf (14 Tage Aufbewahrung); das Repository selbst bleibt sauber.

Lokal ausfuehren:

    npm install
    npx playwright install chromium
    npm test

## Lizenzen und Drittanbieter-Assets

- Spielcode und Map Builder: MIT (siehe LICENSE)
- three.js: MIT, eingebettet in den HTML-Dateien
- Quaternius Universal Mannequin + Universal Animation Library (CC0): Fallback-Charakter als Fallback, wird per CDN geladen
- Kenney-Assets (CC0): eingebaute Park- und Requisitenmodelle
- Mixamo (Adobe): Charakter \"Remy\" samt Animationen (Skateboarding, Jumping Up, Falling to Landing), mit eigenem Adobe-Konto heruntergeladen, offline konvertiert und als Teil des Spiels integriert. Da Adobe-Mixamo-Inhalte nicht eigenstaendig weitergegeben werden duerfen, liegen sie nur in Spielform (konvertierte Fragmente in `assets/remy/`) vor; Quell-FBX-Dateien sind bewusst nicht Teil des Repos.
