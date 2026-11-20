# PRO SKATER 99 - Warehouse Sessions Pro

Skateboard-Spiel (three.js) als eigenstaendige HTML-Datei mit Neigungsphysik, Tricks, Vert-Rampen, Bowls, eingebettetem Map Builder und E2E-Tests. Der Skater wird als echtes 3D-Charaktermodell angezeigt (Mixamo-Charakter "Remy", siehe unten).

## Spielen

`pro-skater-99.html` herunterladen oder raw oeffnen und im Browser starten. Kein Build, keine Installation; three.js ist eingebettet. Das Spiel laedt die Spielfigur und optionale Assets beim Start nach (Internetverbindung noetig, sonst greift der stilisierte Fallback-Skater). Am zuverlaessigsten ist die Raw-URL:

    https://raw.githubusercontent.com/Jens-Smit/skater/main/pro-skater-99.html

Fahrtrichtung und Blickrichtung sind entkoppelt: Nach einem 180er (fakie/switch) dreht sich die Figur weich um weitere 180 Grad zur Fahrtrichtung (`switchYaw`-Daempfung), waehrend das Board weiter rueckwaerts rollt.

## Dateien

- `pro-skater-99.html`: das vollstaendige Spiel (Skatepark, Physik, Tricks, Map Builder im Startmenue)
- `mapbuilder.html`: eigenstaendige Version des Map Builders (der aktuellste Builder ist in pro-skater-99.html eingebettet)
- `assets/remy/`: Spielfigur "Remy" als reine Textfragmente (glTF-JSON + Base64-Bloecke), im Spiel zusammengesetzt
- `tests/`, `playwright.config.js`, `package.json`: Playwright-E2E-Tests
- `.github/workflows/e2e.yml`: GitHub-Actions-Workflow

## Animationen und der Animations-Viewer

Die Figur hat 14 Clips im glTF: `ride`, `ride2` (Schwanken), `jump`, `flip`, `shove`, `grab`, `grind`, `manual`, `nmanual` (Nose-Manual), `land`, `fall` sowie die drei unveraenderten Original-Clips `orig_ride`, `orig_ride2`, `orig_jump` als Referenz.

`anim-viewer.html` ist ein eigenstaendiger Viewer im Repo: im Browser oeffnen (Raw-URL oder lokale Datei neben dem Repo-Ordner), er laedt dieselben `assets/remy`-Fragmente wie das Spiel (inklusive Byte-Laengen-Pruefung) und zeigt pro Clip einen Play/Pause-Knopf, Tempo-Regler, Licht-Drehung und Kamera-Presets (Iso, Seite, Hinten, Orbit). Einmal-Aktionen wie `jump` oder `flip` laufen als LoopOnce und frieren am Ende ein.

    https://raw.githubusercontent.com/Jens-Smit/skater/main/anim-viewer.html

Der gleiche Tricknamen-Mechanismus wie im Spiel: Der Viewer listet Clips automatisch aus `gltf.animations`, neue Clips erscheinen also ohne Anpassung als Knopf.

## Animationen und Tricks erweitern (tools/anims)

Alle Autorenskripte liegen in `tools/anims/` und sind Pfad-unabhaengig (relativ zur Repo-Wurzel). Pipeline:

1. `python3 tools/anims/author_full2.py`
   Erzeugt `frames2.pkl`: pro Clip eine Pose-Liste (Keyframes fuer alle 52 Rotations-Kanaele). Hier neue Clips als Funktionen ergaenzen; Vorlagen sind die bestehenden Clip-Funktionen (z.B. `pose_grab`). Clips werden in `NEW_ORDER` registriert.
2. `python3 tools/anims/encode2.py`
   Schreibt `frames2.pkl` in `assets/remy/` zurueck: erweitert `remy.gltf.json` (neue Animationen, Translation-Kanaele fuer Hips und Kopf) und haengt die neuen Quaternion-Samples als Base64 an `f7.txt` an. Die Funktion druckt danach eine Roundtrip-Validierung (Quaternionen normiert, Hips-Diff-Check, Kopf-Werte).
3. Validation/Render: `python3 tools/anims/render_skin.py <clip> [t] [side|back] [out.png]` rendert die echte gemeshte Silhouette als PNG (reine numpy-Berechnung, kein Browser noetig). Fuer saubere Vergleichsgrafiken gibt es zusaetzlich `verify_render.py` (helle Renders, vorher/nachher).

Kopf-Korrektur: Remy hat kein messbares Genick (mixamorigNeck ist ein Nullswert-Knoten), deshalb tragen alle von uns erzeugten Clips eine konstante Kopf-Translation (die Konstanten `HEAD_DY = 70` und `HEAD_DZ = -29` stehen in `encode2.py`), damit der Kopf in jeder Pose frei ueber dem Kragen steht. Beim Aendern beide Dateien konsistent halten und die Roundtrip-Zeile `KopfY`/`KopfZ` pruefen.

Basis fuer die Pipeline ist `tools/anims/original/remy.gltf.json`, der unveraenderte Mixamo-Export (4 Clips). Die Bufferdateien `f0..f6.txt` werden direkt aus `assets/remy/` gelesen (identisch mit dem Original), nur `f7.txt` wird neu erzeugt.

Im Spiel selbst den neuen Clip nur registrieren: Er ist nach dem Push automatisch in `gltf.animations` enthalten; fuer Steuerung/Ausloesung eine Zeile im Trick-Handling ergaenzen (Suchpunkt: `playClip` bzw. `action.play()`-Stellen in pro-skater-99.html).

Wichtige Randbedingungen:

- Das Spiel laedt Assets raw-first (GitHub-Raw vor jsdelivr) mit Byte-Laengen-Pruefung; nach einem Push genuegt ein Hard-Reload der Raw-URL.
- `remy.gltf.json` muss minifiziert bleiben (Trennzeichen `(',',':'`)).
- Commit-Meldungen auf Deutsch, direkte Pushes auf `main` sind in diesem Repo etabliert.

Requirements fuer die Pipeline: Python 3 mit `numpy`, `scipy`, `matplotlib`.

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
- Mixamo (Adobe): Charakter "Remy" samt Animationen (Skateboarding, Jumping Up, Falling to Landing), mit eigenem Adobe-Konto heruntergeladen, offline konvertiert und als Teil des Spiels integriert. Da Adobe-Mixamo-Inhalte nicht eigenstaendig weitergegeben werden duerfen, liegen sie nur in Spielform (konvertierte Fragmente in `assets/remy/`) vor; Quell-FBX-Dateien sind bewusst nicht Teil des Repos.
