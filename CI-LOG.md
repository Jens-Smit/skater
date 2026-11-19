# E2E-Testlauf

- Commit: 4a84957
- Lauf: 14 (ID 44626173363)
- Zeit (UTC): 2026-11-19 22:18:12
- npm install: success
- Playwright-Installation: success
- Testlauf: success (Exit-Code: 0)

## Ausgaben

### npm-install.log

```

added 3 packages in 1s
```

### pw-install.log

```
Get:9 http://security.ubuntu.com/ubuntu noble-security/main amd64 Packages [1198 kB]
Get:3 http://us-east-2.ec2.archive.ubuntu.com/ubuntu noble-updates InRelease [126 kB]
Get:4 http://us-east-2.ec2.archive.ubuntu.com/ubuntu noble-backports InRelease [126 kB]
Get:10 http://us-east-2.ec2.archive.ubuntu.com/ubuntu noble-updates/main amd64 Packages [1475 kB]
Get:11 http://us-east-2.ec2.archive.ubuntu.com/ubuntu noble-updates/main Translation-en [319 kB]
Get:12 http://us-east-2.ec2.archive.ubuntu.com/ubuntu noble-updates/universe amd64 Packages [1716 kB]
Get:17 http://security.ubuntu.com/ubuntu noble-security/main Translation-en [239 kB]
Get:13 http://us-east-2.ec2.archive.ubuntu.com/ubuntu noble-updates/universe Translation-en [346 kB]
Get:18 http://security.ubuntu.com/ubuntu noble-security/universe amd64 Packages [1230 kB]
Get:19 http://security.ubuntu.com/ubuntu noble-security/universe Translation-en [248 kB]
Get:20 http://security.ubuntu.com/ubuntu noble-security/restricted amd64 Packages [1792 kB]
Get:21 http://security.ubuntu.com/ubuntu noble-security/restricted Translation-en [414 kB]
Get:22 http://security.ubuntu.com/ubuntu noble-security/multiverse Translation-en [12.7 kB]
Get:14 http://us-east-2.ec2.archive.ubuntu.com/ubuntu noble-updates/restricted amd64 Packages [1922 kB]
Get:15 http://us-east-2.ec2.archive.ubuntu.com/ubuntu noble-updates/restricted Translation-en [443 kB]
Get:16 http://us-east-2.ec2.archive.ubuntu.com/ubuntu noble-updates/multiverse Translation-en [14.6 kB]
Fetched 13.3 MB in 10s (1291 kB/s)
Reading package lists...
Reading package lists...
Building dependency tree...
Reading state information...
libasound2t64 is already the newest version (1.2.11-1ubuntu0.3).
libasound2t64 set to manually installed.
libatk-bridge2.0-0t64 is already the newest version (2.52.0-1build1).
libatk-bridge2.0-0t64 set to manually installed.
libatk1.0-0t64 is already the newest version (2.52.0-1build1).
libatk1.0-0t64 set to manually installed.
libatspi2.0-0t64 is already the newest version (2.52.0-1build1).
libatspi2.0-0t64 set to manually installed.
libcairo2 is already the newest version (1.18.0-3build1).
libcairo2 set to manually installed.
libcups2t64 is already the newest version (2.4.7-1.2ubuntu7.14).
libcups2t64 set to manually installed.
libdbus-1-3 is already the newest version (1.14.10-4ubuntu4.1).
libdbus-1-3 set to manually installed.
libdrm2 is already the newest version (2.4.125-1ubuntu0.1~24.04.2).
libdrm2 set to manually installed.
libglib2.0-0t64 is already the newest version (2.80.0-6ubuntu3.10).
libglib2.0-0t64 set to manually installed.
libnspr4 is already the newest version (2:4.35-1.1build1).
libnspr4 set to manually installed.
libnss3 is already the newest version (2:3.98-1ubuntu0.3).
libnss3 set to manually installed.
libpango-1.0-0 is already the newest version (1.52.1+ds-1build1).
libpango-1.0-0 set to manually installed.
libx11-6 is already the newest version (2:1.8.7-1ubuntu0.1).
libx11-6 set to manually installed.
libxcb1 is already the newest version (1.15-1ubuntu2).
libxcb1 set to manually installed.
libxcomposite1 is already the newest version (1:0.4.5-1build3).
libxcomposite1 set to manually installed.
libxdamage1 is already the newest version (1:1.1.6-1build1).
libxdamage1 set to manually installed.
libxext6 is already the newest version (2:1.3.4-1build2).
libxext6 set to manually installed.
libxfixes3 is already the newest version (1:6.0.0-2build1).
libxfixes3 set to manually installed.
libxkbcommon0 is already the newest version (1.6.0-1build1).
libxkbcommon0 set to manually installed.
libxrandr2 is already the newest version (2:1.5.2-2build1).
libxrandr2 set to manually installed.
xvfb is already the newest version (2:21.1.12-1ubuntu1.9).
fonts-noto-color-emoji is already the newest version (2.047-0ubuntu0.24.04.1).
libfontconfig1 is already the newest version (2.15.0-1.1ubuntu2).
libfontconfig1 set to manually installed.
libfreetype6 is already the newest version (2.13.2+dfsg-1ubuntu0.2).
libfreetype6 set to manually installed.
fonts-liberation is already the newest version (1:2.1.5-3).
fonts-liberation set to manually installed.
The following additional packages will be installed:
  libgl1-mesa-dri libglx-mesa0 mesa-libgallium xfonts-encodings xfonts-utils
Recommended packages:
  fonts-ipafont-mincho fonts-tlwg-loma
The following NEW packages will be installed:
  fonts-freefont-ttf fonts-ipafont-gothic fonts-tlwg-loma-otf fonts-unifont
  fonts-wqy-zenhei xfonts-cyrillic xfonts-encodings xfonts-scalable
  xfonts-utils
The following packages will be upgraded:
  libgbm1 libgl1-mesa-dri libglx-mesa0 mesa-libgallium
4 upgraded, 9 newly installed, 0 to remove and 46 not upgraded.
Need to get 32.1 MB of archives.
After this operation, 79.7 MB of additional disk space will be used.
Get:1 file:/etc/apt/apt-mirrors.txt Mirrorlist [152 B]
Get:2 http://us-east-2.ec2.archive.ubuntu.com/ubuntu noble/universe amd64 fonts-ipafont-gothic all 00303-21ubuntu1 [3513 kB]
Get:3 http://us-east-2.ec2.archive.ubuntu.com/ubuntu noble/main amd64 fonts-freefont-ttf all 20211204+svn4273-2 [5641 kB]
Get:4 http://us-east-2.ec2.archive.ubuntu.com/ubuntu noble/universe amd64 fonts-tlwg-loma-otf all 1:0.7.3-1 [107 kB]
Get:5 http://us-east-2.ec2.archive.ubuntu.com/ubuntu noble/universe amd64 fonts-unifont all 1:15.1.01-1build1 [2993 kB]
Get:6 http://us-east-2.ec2.archive.ubuntu.com/ubuntu noble/universe amd64 fonts-wqy-zenhei all 0.9.45-8 [7472 kB]
Get:7 http://us-east-2.ec2.archive.ubuntu.com/ubuntu noble-updates/main amd64 libgl1-mesa-dri amd64 25.2.8-0ubuntu0.24.04.5 [38.0 kB]
Get:8 http://us-east-2.ec2.archive.ubuntu.com/ubuntu noble-updates/main amd64 libglx-mesa0 amd64 25.2.8-0ubuntu0.24.04.5 [110 kB]
Get:9 http://us-east-2.ec2.archive.ubuntu.com/ubuntu noble-updates/main amd64 libgbm1 amd64 25.2.8-0ubuntu0.24.04.5 [34.2 kB]
Get:10 http://us-east-2.ec2.archive.ubuntu.com/ubuntu noble-updates/main amd64 mesa-libgallium amd64 25.2.8-0ubuntu0.24.04.5 [10.8 MB]
Get:11 http://us-east-2.ec2.archive.ubuntu.com/ubuntu noble/main amd64 xfonts-encodings all 1:1.0.5-0ubuntu2 [578 kB]
Get:12 http://us-east-2.ec2.archive.ubuntu.com/ubuntu noble/main amd64 xfonts-utils amd64 1:7.7+6build3 [94.4 kB]
Get:13 http://us-east-2.ec2.archive.ubuntu.com/ubuntu noble/universe amd64 xfonts-cyrillic all 1:1.0.5+nmu1 [384 kB]
Get:14 http://us-east-2.ec2.archive.ubuntu.com/ubuntu noble/main amd64 xfonts-scalable all 1:1.0.3-1.3 [304 kB]
Fetched 32.1 MB in 3min 1s (177 kB/s)
Selecting previously unselected package fonts-ipafont-gothic.
(Reading database ... (Reading database ... 5%(Reading database ... 10%(Reading database ... 15%(Reading database ... 20%(Reading database ... 25%(Reading database ... 30%(Reading database ... 35%(Reading database ... 40%(Reading database ... 45%(Reading database ... 50%(Reading database ... 55%(Reading database ... 60%(Reading database ... 65%(Reading database ... 70%(Reading database ... 75%(Reading database ... 80%(Reading database ... 85%(Reading database ... 90%(Reading database ... 95%(Reading database ... 100%(Reading database ... 216380 files and directories currently installed.)
Preparing to unpack .../00-fonts-ipafont-gothic_00303-21ubuntu1_all.deb ...
Unpacking fonts-ipafont-gothic (00303-21ubuntu1) ...
Selecting previously unselected package fonts-freefont-ttf.
Preparing to unpack .../01-fonts-freefont-ttf_20211204+svn4273-2_all.deb ...
Unpacking fonts-freefont-ttf (20211204+svn4273-2) ...
Selecting previously unselected package fonts-tlwg-loma-otf.
Preparing to unpack .../02-fonts-tlwg-loma-otf_1%3a0.7.3-1_all.deb ...
Unpacking fonts-tlwg-loma-otf (1:0.7.3-1) ...
Selecting previously unselected package fonts-unifont.
Preparing to unpack .../03-fonts-unifont_1%3a15.1.01-1build1_all.deb ...
Unpacking fonts-unifont (1:15.1.01-1build1) ...
Selecting previously unselected package fonts-wqy-zenhei.
Preparing to unpack .../04-fonts-wqy-zenhei_0.9.45-8_all.deb ...
Unpacking fonts-wqy-zenhei (0.9.45-8) ...
Preparing to unpack .../05-libgl1-mesa-dri_25.2.8-0ubuntu0.24.04.5_amd64.deb ...
Unpacking libgl1-mesa-dri:amd64 (25.2.8-0ubuntu0.24.04.5) over (25.2.8-0ubuntu0.24.04.4) ...
Preparing to unpack .../06-libglx-mesa0_25.2.8-0ubuntu0.24.04.5_amd64.deb ...
Unpacking libglx-mesa0:amd64 (25.2.8-0ubuntu0.24.04.5) over (25.2.8-0ubuntu0.24.04.4) ...
Preparing to unpack .../07-libgbm1_25.2.8-0ubuntu0.24.04.5_amd64.deb ...
Unpacking libgbm1:amd64 (25.2.8-0ubuntu0.24.04.5) over (25.2.8-0ubuntu0.24.04.4) ...
Preparing to unpack .../08-mesa-libgallium_25.2.8-0ubuntu0.24.04.5_amd64.deb ...
Unpacking mesa-libgallium:amd64 (25.2.8-0ubuntu0.24.04.5) over (25.2.8-0ubuntu0.24.04.4) ...
Selecting previously unselected package xfonts-encodings.
Preparing to unpack .../09-xfonts-encodings_1%3a1.0.5-0ubuntu2_all.deb ...
Unpacking xfonts-encodings (1:1.0.5-0ubuntu2) ...
Selecting previously unselected package xfonts-utils.
Preparing to unpack .../10-xfonts-utils_1%3a7.7+6build3_amd64.deb ...
Unpacking xfonts-utils (1:7.7+6build3) ...
Selecting previously unselected package xfonts-cyrillic.
Preparing to unpack .../11-xfonts-cyrillic_1%3a1.0.5+nmu1_all.deb ...
Unpacking xfonts-cyrillic (1:1.0.5+nmu1) ...
Selecting previously unselected package xfonts-scalable.
Preparing to unpack .../12-xfonts-scalable_1%3a1.0.3-1.3_all.deb ...
Unpacking xfonts-scalable (1:1.0.3-1.3) ...
Setting up mesa-libgallium:amd64 (25.2.8-0ubuntu0.24.04.5) ...
Setting up libgbm1:amd64 (25.2.8-0ubuntu0.24.04.5) ...
Setting up libgl1-mesa-dri:amd64 (25.2.8-0ubuntu0.24.04.5) ...
Setting up fonts-wqy-zenhei (0.9.45-8) ...
Setting up fonts-freefont-ttf (20211204+svn4273-2) ...
Setting up fonts-tlwg-loma-otf (1:0.7.3-1) ...
Setting up xfonts-encodings (1:1.0.5-0ubuntu2) ...
Setting up fonts-ipafont-gothic (00303-21ubuntu1) ...
update-alternatives: using /usr/share/fonts/opentype/ipafont-gothic/ipag.ttf to provide /usr/share/fonts/truetype/fonts-japanese-gothic.ttf (fonts-japanese-gothic.ttf) in auto mode
Setting up fonts-unifont (1:15.1.01-1build1) ...
Setting up libglx-mesa0:amd64 (25.2.8-0ubuntu0.24.04.5) ...
Setting up xfonts-utils (1:7.7+6build3) ...
Setting up xfonts-cyrillic (1:1.0.5+nmu1) ...
Setting up xfonts-scalable (1:1.0.3-1.3) ...
Processing triggers for libc-bin (2.39-0ubuntu8.9) ...
Processing triggers for man-db (2.12.0-4build2) ...
Not building database; man-db/auto-update is not 'true'.
Processing triggers for fontconfig (2.15.0-1.1ubuntu2) ...

Running kernel seems to be up-to-date.

No services need to be restarted.

No containers need to be restarted.

No user sessions are running outdated binaries.

No VM guests are running outdated hypervisor (qemu) binaries on this host.
Downloading Chromium 133.0.6943.16 (playwright build v1155) from https://cdn.playwright.dev/dbazure/download/playwright/builds/chromium/1155/chromium-linux.zip
|                                                                                |   0% of 163.5 MiB
|■■■■■■■■                                                                        |  10% of 163.5 MiB
|■■■■■■■■■■■■■■■■                                                                |  20% of 163.5 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■                                                        |  30% of 163.5 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■                                                |  40% of 163.5 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■                                        |  50% of 163.5 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■                                |  60% of 163.5 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■                        |  70% of 163.5 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■                |  80% of 163.5 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■        |  90% of 163.5 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■| 100% of 163.5 MiB
Chromium 133.0.6943.16 (playwright build v1155) downloaded to /home/runner/.cache/ms-playwright/chromium-1155
Downloading FFMPEG playwright build v1011 from https://cdn.playwright.dev/dbazure/download/playwright/builds/ffmpeg/1011/ffmpeg-linux.zip
|                                                                                |   0% of 2.3 MiB
|■■■■■■■■                                                                        |  10% of 2.3 MiB
|■■■■■■■■■■■■■■■■                                                                |  20% of 2.3 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■                                                        |  30% of 2.3 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■                                                |  40% of 2.3 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■                                        |  50% of 2.3 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■                                |  60% of 2.3 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■                        |  70% of 2.3 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■                |  80% of 2.3 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■        |  90% of 2.3 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■| 100% of 2.3 MiB
FFMPEG playwright build v1011 downloaded to /home/runner/.cache/ms-playwright/ffmpeg-1011
Downloading Chromium Headless Shell 133.0.6943.16 (playwright build v1155) from https://cdn.playwright.dev/dbazure/download/playwright/builds/chromium/1155/chromium-headless-shell-linux.zip
|                                                                                |   0% of 99.9 MiB
|■■■■■■■■                                                                        |  10% of 99.9 MiB
|■■■■■■■■■■■■■■■■                                                                |  20% of 99.9 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■                                                        |  30% of 99.9 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■                                                |  40% of 99.9 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■                                        |  50% of 99.9 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■                                |  60% of 99.9 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■                        |  70% of 99.9 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■                |  80% of 99.9 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■        |  90% of 99.9 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■| 100% of 99.9 MiB
Chromium Headless Shell 133.0.6943.16 (playwright build v1155) downloaded to /home/runner/.cache/ms-playwright/chromium_headless_shell-1155
```

### test-output.log

```
[WebServer] 127.0.0.1 - - [19/Nov/2026 22:15:28] "GET / HTTP/1.1" 200 -

Running 13 tests using 1 worker

[WebServer] 127.0.0.1 - - [19/Nov/2026 22:15:29] "GET /pro-skater-99.html HTTP/1.1" 200 -
  ✓  1 [chromium] › tests/game.spec.js:68:1 › Startmenü: Seite lädt ohne JS-Fehler, 3D-Grafik wird bereit (4.8s)
[WebServer] 127.0.0.1 - - [19/Nov/2026 22:15:35] "GET /pro-skater-99.html HTTP/1.1" 200 -
  ✓  2 [chromium] › tests/game.spec.js:84:1 › Layout: Spiel-Canvas ist im Dokument sichtbar platziert (Regression 0x0-Leinwand) (6.7s)
[WebServer] 127.0.0.1 - - [19/Nov/2026 22:15:42] "GET /pro-skater-99.html HTTP/1.1" 200 -
  ✓  3 [chromium] › tests/game.spec.js:124:1 › Karte lädt und ist sichtbar: Szene rendert, kein schwarzer Bildschirm (18.6s)
[WebServer] 127.0.0.1 - - [19/Nov/2026 22:16:01] "GET /pro-skater-99.html HTTP/1.1" 200 -
  ✓  4 [chromium] › tests/game.spec.js:195:1 › Session: HUD sichtbar, Renderer aktiv, Draw-Calls über null (12.5s)
[WebServer] 127.0.0.1 - - [19/Nov/2026 22:16:14] "GET /pro-skater-99.html HTTP/1.1" 200 -
  ✓  5 [chromium] › tests/game.spec.js:208:1 › Fahrt: Beschleunigen und Ollie bewegen die Kamera, kein Fehler (14.3s)
[WebServer] 127.0.0.1 - - [19/Nov/2026 22:16:28] "GET /pro-skater-99.html HTTP/1.1" 200 -
  ✓  6 [chromium] › tests/game.spec.js:230:1 › Map Builder: öffnen und schließen, Haupt-3D läuft danach weiter (19.3s)
[WebServer] 127.0.0.1 - - [19/Nov/2026 22:16:48] "GET /mapbuilder.html HTTP/1.1" 200 -
  ✓  7 [chromium] › tests/mapbuilder.spec.js:15:1 › Standalone-Builder: lädt, rendert und zeigt die Demo-Karte an (4.5s)
[WebServer] 127.0.0.1 - - [19/Nov/2026 22:16:50] "GET /pro-skater-99.html HTTP/1.1" 200 -
KARTEN-SCREENSHOT tutorial: {"datei":"ci-screenshots/tutorial.png","bytes":83818,"breite":480,"hoehe":270,"meanLum":205.1,"darkFraction":0,"colorBins":208}
  ✓  8 [chromium] › tests/screenshots.spec.js:178:3 › Karte tutorial laedt und ist sichtbar (Screenshot als Beleg) (12.7s)
[WebServer] 127.0.0.1 - - [19/Nov/2026 22:17:05] "GET /pro-skater-99.html HTTP/1.1" 200 -
KARTEN-SCREENSHOT warehouse: {"datei":"ci-screenshots/warehouse.png","bytes":66990,"breite":480,"hoehe":270,"meanLum":238.7,"darkFraction":0,"colorBins":177}
  ✓  9 [chromium] › tests/screenshots.spec.js:178:3 › Karte warehouse laedt und ist sichtbar (Screenshot als Beleg) (16.8s)
[WebServer] 127.0.0.1 - - [19/Nov/2026 22:17:23] "GET /pro-skater-99.html HTTP/1.1" 200 -
KARTEN-SCREENSHOT school: {"datei":"ci-screenshots/school.png","bytes":102989,"breite":480,"hoehe":270,"meanLum":213.9,"darkFraction":0,"colorBins":217}
  ✓  10 [chromium] › tests/screenshots.spec.js:178:3 › Karte school laedt und ist sichtbar (Screenshot als Beleg) (15.3s)
[WebServer] 127.0.0.1 - - [19/Nov/2026 22:17:36] "GET /pro-skater-99.html HTTP/1.1" 200 -
KARTEN-SCREENSHOT minipark: {"datei":"ci-screenshots/minipark.png","bytes":87392,"breite":480,"hoehe":270,"meanLum":213.7,"darkFraction":0.002,"colorBins":277}
  ✓  11 [chromium] › tests/screenshots.spec.js:178:3 › Karte minipark laedt und ist sichtbar (Screenshot als Beleg) (14.1s)
[WebServer] 127.0.0.1 - - [19/Nov/2026 22:17:51] "GET /pro-skater-99.html HTTP/1.1" 200 -
KARTEN-SCREENSHOT funpark: {"datei":"ci-screenshots/funpark.png","bytes":94663,"breite":480,"hoehe":270,"meanLum":202.6,"darkFraction":0,"colorBins":295}
  ✓  12 [chromium] › tests/screenshots.spec.js:178:3 › Karte funpark laedt und ist sichtbar (Screenshot als Beleg) (16.0s)
[WebServer] 127.0.0.1 - - [19/Nov/2026 22:18:08] "GET /mapbuilder.html HTTP/1.1" 200 -
KARTEN-SCREENSHOT builder-demo: {"datei":"ci-screenshots/builder-demo.png","bytes":36775,"breite":480,"hoehe":270,"meanLum":189.1,"darkFraction":0,"colorBins":91}
KARTEN-SCREENSHOTS: [{"datei":"ci-screenshots/tutorial.png","bytes":83818,"breite":480,"hoehe":270,"meanLum":205.1,"darkFraction":0,"colorBins":208},{"datei":"ci-screenshots/warehouse.png","bytes":66990,"breite":480,"hoehe":270,"meanLum":238.7,"darkFraction":0,"colorBins":177},{"datei":"ci-screenshots/school.png","bytes":102989,"breite":480,"hoehe":270,"meanLum":213.9,"darkFraction":0,"colorBins":217},{"datei":"ci-screenshots/minipark.png","bytes":87392,"breite":480,"hoehe":270,"meanLum":213.7,"darkFraction":0.002,"colorBins":277},{"datei":"ci-screenshots/funpark.png","bytes":94663,"breite":480,"hoehe":270,"meanLum":202.6,"darkFraction":0,"colorBins":295},{"datei":"ci-screenshots/builder-demo.png","bytes":36775,"breite":480,"hoehe":270,"meanLum":189.1,"darkFraction":0,"colorBins":91}]
  ✓  13 [chromium] › tests/screenshots.spec.js:204:1 › Map-Builder-Demo-Karte laedt und ist sichtbar (Screenshot als Beleg) (5.6s)

  Slow test file: [chromium] › tests/screenshots.spec.js (1.3m)
  Slow test file: [chromium] › tests/game.spec.js (1.3m)
  Consider running tests from slow files in parallel, see https://playwright.dev/docs/test-parallel.
  13 passed (2.7m)
```

## Karten-Screenshots

- [builder-demo.png](ci-screenshots/builder-demo.png) (36775 Bytes)
- [funpark.png](ci-screenshots/funpark.png) (94663 Bytes)
- [minipark.png](ci-screenshots/minipark.png) (87392 Bytes)
- [school.png](ci-screenshots/school.png) (102989 Bytes)
- [tutorial.png](ci-screenshots/tutorial.png) (83818 Bytes)
- [warehouse.png](ci-screenshots/warehouse.png) (66990 Bytes)
