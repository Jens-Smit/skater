# skater

PRO SKATER 99: Warehouse Sessions Pro. Skateboard-Spiel mit three.js als eigenständige HTML-Datei, plus separater Map Builder.

## Dateien

- `pro-skater-99.html`: das vollständige Spiel (Skatepark, Fahrphysik, Tricks, eingebetteter Map Builder über den Startmenü-Button)
- `mapbuilder.html`: eigenständige Version des Map Builders (nutzt dieselbe Kartenbibliothek wie das Spiel)

Beide Dateien sind autark: three.js ist eingebettet, es werden keine externen Ressourcen geladen.

## E2E-Tests

Die Tests laufen mit Playwright in GitHub Actions (headless Chromium, WebGL über SwiftShader) automatisch bei jedem Push auf `main`. Workflow: `.github/workflows/e2e.yml`, Testfälle: `tests/`.

Nach jedem Lauf committet die CI das Protokoll als `CI-LOG.md` ins Repository: Ergebnis und die letzten 300 Zeilen der Playwright-Ausgabe. Der vollständige HTML-Report mit Screenshots liegt als Artefakt `playwright-report` beim jeweiligen Lauf.

Lokal ausführen:

    npm install
    npx playwright install chromium
    npm test

Getestet wird:

- Laden beider Seiten ohne unbehandelte JS-Fehler
- Startmenü mit initialisiertem WebGL (Start-Button wird erst nach dem 3D-Laden aktiv)
- Karte lädt und ist sichtbar: die Szene rendert mit messbarem Bildinhalt, kein schwarzer Bildschirm
- Session-Start: HUD sichtbar, Draw-Calls über null
- Fahrt mit Tastatur: Kamera folgt dem Skater
- Map Builder im Spiel: öffnen und schließen, danach rendert das Hauptspiel weiter (WebGL-Kontext-Fix)
- Eigenständiger Builder: Renderer aktiv, Demo-Karte aufgebaut
