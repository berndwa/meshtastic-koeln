# Koeln · Meshtastic über Funk

Kleine, moderne und mobilfreundliche Informationsseite für den öffentlichen Meshtastic-Channel **Koeln** in Köln und Umgebung. Unabhängige Einladung ohne behauptete offizielle Zugehörigkeit zu Meshtastic, der Stadt Köln oder einer lokalen Community.

**Fertig für GitHub Pages:** reines HTML/CSS mit einer kleinen optionalen Kopierfunktion. Kein Build, kein Paketmanager, keine Laufzeitabhängigkeiten, keine externen Fonts, keine Analysewerkzeuge und kein externer QR-Dienst. Alle wesentlichen Inhalte und die Einladung funktionieren ohne JavaScript.

## Veröffentlichen mit GitHub Pages

1. Auf GitHub ein neues **öffentliches** Repository erstellen, z. B. `meshtastic-koeln`. Für den folgenden Git-Weg beim Erstellen keine README hinzufügen: Diese Dateien bringen bereits eine mit.
2. Den **Inhalt dieses Ordners** hochladen, sodass `index.html` direkt im Repository-Hauptverzeichnis liegt, zusammen mit `styles.css`, `script.js`, `assets/`, `config/`, `docs/`, `tools/` und der leeren Datei `.nojekyll`. Es darf kein zusätzlicher Ordner `meshtastic-koeln/` darüber liegen.
3. Unter **Settings → Pages → Build and deployment** bei **Source** die Option **Deploy from a branch** wählen.
4. **Branch: `main`**, Ordner **`/ (root)`**, dann **Save**.
5. Nach der Veröffentlichung unter Pages auf **Visit site** klicken. Bei einem Projekt-Repository lautet die Adresse üblicherweise `https://DEIN-NAME.github.io/meshtastic-koeln/`. Die erstmalige Veröffentlichung kann einige Minuten dauern.

Es ist kein eigener GitHub-Actions-Workflow nötig. `.nojekyll` lässt die Dateien ohne Jekyll-Verarbeitung ausliefern. Alle Ressourcenpfade sind relativ und funktionieren auch unter einem Repository-Unterpfad. HTTPS unter Pages aktivieren, sofern verfügbar.

### Alternativ per Git hochladen

Im entpackten Projektordner ausführen. Die Platzhalteradresse durch dein eigenes neues, leeres Repository ersetzen:

```sh
git init -b main
git add .
git commit -m "Add public Koeln Meshtastic channel page"
git remote add origin https://github.com/DEIN-NAME/meshtastic-koeln.git
git push -u origin main
```

Falls der Ordner bereits als Git-Repository initialisiert ist, den ersten Befehl weglassen. Anschließend Pages wie oben aktivieren. Aktualisierungen werden nach einem Push auf `main` erneut veröffentlicht.

Offizielle Anleitung: [GitHub Pages erstellen](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site).

## Lokal ansehen

`index.html` direkt im Browser öffnen oder im Projektordner einen lokalen Server starten:

```sh
python3 -m http.server 8080
```

Dann [http://localhost:8080](http://localhost:8080) öffnen. Die Kopierfunktion braucht einen sicheren Browserkontext und Clipboard-Berechtigung; falls sie nicht verfügbar ist, wird der Text zur manuellen Übernahme markiert.

## Konfiguration und wichtige Grenzen

| Einstellung | Vorgabe |
| --- | --- |
| Channelname | `Koeln` (exakte Schreibweise) |
| Funkregion des Geräts | `EU_868` |
| Modem-Preset des Geräts | `SHORT_SLOW` / Short Slow; `use_preset = true` |
| Channelrolle | `SECONDARY`, als zusätzlicher Channel |
| PSK | 32 Byte / AES-256, bewusst öffentlich geteilt |
| MQTT-Modul | Aus, am Gerät separat prüfen |
| Channel-Uplink und -Downlink | Aus |

Einladung:

<https://meshtastic.org/e/?add=true#CjASIEzZycQ67AIFUEMnEBDqMMMbmItKKdJBLb--t3giEgafGgVLb2VsbiUCAAAAOgA>

Öffentlicher PSK (Standard-Base64):

```text
TNnJxDrsAgVQQycQEOowwxuYi0op0kEtv763eCISBp8=
```

Der vorgegebene Link wurde decodiert: Er enthält **genau ein `ChannelSettings`-Objekt ohne `LoRaConfig`**. Er stellt EU_868 und Short Slow daher nicht ein. Auch die Rolle ist kein Feld dieses eingebetteten Settings-Objekts. `?add=true` signalisiert den Hinzufügen-Modus; der Importdialog und das gespeicherte Ergebnis sind in jedem Client zu prüfen. „Ersetzen“ kann bestehende Channels überschreiben.

**Short Slow ist eine Geräteeinstellung.** Alle Channels desselben üblichen Funkgeräts verwenden dasselbe LoRa-Profil. Ein zusätzlicher Channel ermöglicht keine gleichzeitige Teilnahme an einem Long-Fast-Funknetz. Ein Channel namens „LongFast“ kann auch auf einem anders eingestellten Gerät stehen; der Name setzt nicht das Modem-Preset.

Short Slow verwendet 250 kHz Bandbreite, SF8 und CR 4/5. In EU_868 ergibt das ohne Frequenzüberschreibung einen Frequenzslot (Slot 1, 869,525 MHz). Automatische Auswahl mit Slot 0 führt hier zum gleichen Slot. Ein Channelplatz (z. B. Index 1 für einen Secondary) ist kein Funkfrequenzslot. Andere Regionen oder Presets können mehrere Frequenzslots haben.

Der 256-Bit-Schlüssel bietet **keine Vertraulichkeit gegenüber Personen mit dieser öffentlichen Einladung**. Keine sensiblen Inhalte oder präzisen Standortdaten teilen. Positionsfreigabe und Telemetrie für das gesamte Gerät und alle Channels prüfen. MQTT aus am eigenen Gerät verhindert nicht, dass andere Empfangende Inhalte speichern, weitergeben oder ins Internet übertragen. Es werden weder Funkabdeckung noch Reichweite, aktive Mitglieder oder eine Antwort zugesichert.

Die vollständigen Prüfnotizen einschließlich der Bedeutung von `id = 2` stehen in [docs/technical-notes.md](docs/technical-notes.md).

## Inhalt ändern und QR-Code erneuern

- Texte/Links: `index.html`
- Darstellung: `styles.css`
- Kopierbuttons: `script.js`
- Referenzkonfiguration: `config/channel.json` (**keine universelle Importdatei**)
- Lokale Illustration und QR-Dateien: `assets/`

Der QR-Code enthält exakt denselben vollständigen Einladungslink, einschließlich `?add=true` und Fragment. Er hat einen weißen Rand von vier QR-Modulen, schwarze Module ohne Logo und ist als SVG und PNG vorhanden.

Falls der Link geändert wird: `config/channel.json`, beide Einladungsbuttons, das Linkfeld und gegebenenfalls das PSK-Feld in `index.html` konsistent ändern; anschließend die QR-Dateien erneuern und prüfen:

```sh
python3 tools/generate_qr.py
python3 tools/verify.py
node --check script.js
```

Diese Erzeugung und Prüfung arbeiten offline mit Python 3.9+ ohne Installation weiterer Pakete. Der QR-Encoder von Project Nayuki liegt samt MIT-Lizenz unter `tools/vendor/`; im Browser wird nur das fertige Bild geladen. `verify.py` prüft den konkreten vorgegebenen Payload bewusst streng. Bei einer neuen Einladung die erwarteten Payload-Felder ebenfalls überprüfen und den Prüfer anpassen.

## Prüfung vor und nach der Veröffentlichung

- Lokal: Payload, Name, 32-Byte-PSK, Add-Modus, relative Ressourcen, Sprungmarken und reproduzierbare QR-Dateien mit `tools/verify.py` prüfen.
- Browser: Seite schmal und breit ansehen; Kopierbuttons, Downloadlinks und aufklappbare Hinweise ausprobieren. Mit Tastatur und ohne JavaScript prüfen.
- Reales iPhone/Android: Einladung oder QR-Code in Meshtastic öffnen, **Add** wählen und anschließend **Secondary, EU_868, Short Slow und MQTT aus** kontrollieren. Ein QR-Scan allein ersetzt diesen Gerätetest nicht.
- Nach GitHub-Deployment: Projekt-Unterpfad, Bilder, QR-Download und HTTPS prüfen. In der Seite werden technische Verbindungsdaten des Hostings erwähnt; vor einer eigenen Veröffentlichung gegebenenfalls eigene erforderliche Betreiberangaben ergänzen.

## Dateistruktur

```text
index.html
styles.css
script.js
.nojekyll
.gitignore
assets/
  favicon.svg
  koeln-mesh.svg
  koeln-qr.svg
  koeln-qr.png
config/channel.json
docs/technical-notes.md
tools/
  generate_qr.py
  verify.py
  vendor/qrcodegen.py
  vendor/README.md
README.md
```

Technischer Stand: **31. Oktober 2026**. App-Menüs, Importfunktionen und Firmware können sich ändern; die Seite verspricht deshalb keinen unbestätigten automatischen Konfigurationswechsel.
