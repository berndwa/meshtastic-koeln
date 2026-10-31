# Technische Prüfung

Geprüft am 31.10.2026 anhand der offiziellen Dokumentation und Protobuf-Definitionen von Meshtastic. Dieser Text dokumentiert die konkrete Einladung, keine offizielle Bestätigung eines lokalen Funknetzes.

## 1. Vorgegebenen Link decodiert

Der Base64url-Teil nach `#` decodiert zu 50 Bytes:

```text
0a3012204cd9c9c43aec02055043271010ea30c31b988b4a29d2412dbfbeb7782212069f1a054b6f656c6e25020000003a00
```

Nach [`apponly.proto`](https://github.com/meshtastic/protobufs/blob/master/meshtastic/apponly.proto) und [`channel.proto`](https://github.com/meshtastic/protobufs/blob/master/meshtastic/channel.proto):

| Objekt / Feld | Ergebnis |
| --- | --- |
| `ChannelSet.settings` (Feld 1) | Ein Eintrag |
| `ChannelSet.lora_config` (Feld 2) | Nicht enthalten |
| `ChannelSettings.psk` (Feld 2) | 32 Byte; Base64 `TNnJxDrsAgVQQycQEOowwxuYi0op0kEtv763eCISBp8=` |
| `ChannelSettings.name` (Feld 3) | `Koeln` |
| `ChannelSettings.id` (Feld 4, fixed32) | `2` |
| `uplink_enabled` (Feld 5) | Nicht gesetzt → false im Protobuf-Datenmodell |
| `downlink_enabled` (Feld 6) | Nicht gesetzt → false im Protobuf-Datenmodell |
| `module_settings` (Feld 7) | Enthalten, aber leer |

**Wichtig: `id = 2` ist keine Rolle.** Die Rolle `SECONDARY = 2` gehört zum getrennten `Channel`-Objekt, das hier nicht serialisiert wird. Der Link enthält ChannelSettings, keine Channel-Objekte mit Rolle und lokalem Index. Eine Ein-Eintrag-ChannelSet-Liste darf deshalb nicht ungeprüft als Ersatz für die bestehende Konfiguration benutzt werden. Der explizite Add-Modus soll das ergänzende Einrichten steuern.

Die Query `?add=true` ist außerhalb des Protobuf-Fragments. Auf der Seite bleibt der vorgegebene Link unverändert. Das tatsächliche Importverhalten hängt vom Client und dessen Version ab; Nutzer prüfen den Add-Dialog und das gespeicherte Ergebnis. Weil keine LoRaConfig vorhanden ist, kann aus diesem Payload weder die Region EU_868 noch das Preset SHORT_SLOW abgeleitet werden. Beides ist die vom Auftraggeber vorgegebene Gerätekonfiguration und wird ausdrücklich separat erläutert. Das globale MQTT-Modul ist ebenfalls nicht Teil der Einladung. Nicht gesetzte Uplink-/Downlink-Felder sind kein Nachweis über den Zustand eines konkreten Zielgeräts nach dem Import.

## 2. Short Slow und Secondary auseinanderhalten

Die [Channel-Dokumentation](https://meshtastic.org/docs/configuration/radio/channels/) trennt Nachrichtengruppen mit Name/Schlüssel von den geräteweit identischen Modemparametern. Die [LoRa-Dokumentation](https://meshtastic.org/docs/configuration/radio/lora/) fordert passende Region, Modemeinstellungen und Frequenz für die Funkkommunikation.

Laut [offizieller Preset-Tabelle](https://meshtastic.org/docs/overview/radio-settings/) hat Short Slow **250 kHz Bandbreite, SF8 und Coding Rate 4/5**. „Slow“ ist hier Teil des Presetnamens; daraus folgt keine pauschal größere Reichweite als bei Long Fast. Es werden bewusst keine Kilometerangaben oder lokale Abdeckungsversprechen gemacht. Geräte mit unterschiedlichen Presets können nicht durch Hinzufügen eines Secondary auf demselben üblichen Ein-Radio-Gerät parallel verbunden werden.

Für EU_868 definiert die [Firmware in `RadioInterface.cpp`](https://github.com/meshtastic/firmware/blob/master/src/mesh/RadioInterface.cpp) den Bereich 869,4–869,65 MHz. Die Anzahl der Frequenzslots ist der abgerundete Quotient aus Bandbreite der Region und Kanalbreite einschließlich Abstand. Bei 250 kHz ohne zusätzlichen Abstand ergibt das einen Slot. Die Mittenfrequenz ist 869,4 + 0,125 = **869,525 MHz**. Dies ist aus der Firmwareformel abgeleitet, gilt für das genannte Preset ohne Frequenzüberschreibung und ist kein neuer Parameter im vorhandenen Einladungslink.

Die allgemeine Warnung, dass unterschiedliche Primary-Namen bei automatischer Auswahl verschiedene Frequenzslots ergeben können, gilt in Regionen/Presetkombinationen mit mehreren Slots. Bei dieser EU_868/250-kHz-Kombination gibt es nur einen. Der lokale Channelindex bleibt davon unabhängig.

## 3. Öffentlich trotz AES-256

32 Byte PSK entsprechen nach `channel.proto` AES-256. Der Schlüssel wird im öffentlichen Link und zusätzlich auf der Seite geteilt. Damit ist die Kommunikation dieser Gruppe gegenüber Personen mit dem Schlüssel nicht vertraulich. Eine starke Schlüssellänge oder ein Verschlüsselungssymbol in der App belegt hier keine exklusive Mitgliedschaft.

Die Seite fordert auf, sensible Inhalte sowie präzise Standortdaten zu vermeiden und Positions-/Telemetrieeinstellungen des gesamten Geräts und aller Channels zu prüfen. Aktuelle Firmware kann Positionsfreigaben je Channel beeinflussen; die Rolle Secondary allein schließt Standortübertragung nicht aus. Siehe [Meshtastic Configuration Tips](https://meshtastic.org/docs/configuration/tips/).

## 4. MQTT aus

Vorgabe sind **MQTT-Modul aus** und **Uplink/Downlink für Koeln aus**. Laut [MQTT-Dokumentation](https://meshtastic.org/docs/configuration/module/mqtt/) spielen Modul und Channel-Schalter zusammen. Die Seite behauptet keine netzweite Weitergabesperre. Auch ohne eigenes MQTT können andere Empfangende Inhalte veröffentlichen. „OK to MQTT“ ist deshalb nicht als universeller Schutz für diesen eigenen, öffentlich geteilten Schlüssel dargestellt.

## 5. Clients und Grenzen der Prüfung

Die [Apple-Channel-Dokumentation](https://meshtastic.org/docs/software/apple/user/messages/) beschreibt die Auswahl zwischen Add und Replace. Die Webseite nennt keine unbestätigten exakten Menüpositionen für jede Version. Für Clients ohne passenden Import gibt es Name und PSK zur manuellen Einrichtung. Der [Web-Client](https://meshtastic.org/docs/software/web-client/) benötigt eine unterstützte Transportart und Browserfunktion; die Seite verspricht keine Bluetooth-/USB-Unterstützung auf jedem iPhone oder in jedem Browser.

Der QR-Code wird lokal mit Project Nayukis QR-Encoder erzeugt. Die Prüfung vergleicht den Link, den decodierten Payload, die sichtbaren Schlüsseldaten und die reproduzierbaren QR-Dateien. Eine erfolgreiche Desktop- oder QR-Prüfung beweist **nicht** den Import auf einem realen iPhone, die tatsächlichen Radioeinstellungen oder erreichbare Funkpartner. Diese Schritte müssen am Gerät geprüft werden.

Bei der Erstellung bestanden: Offline-Prüfung mit `tools/verify.py`, JavaScript-Syntaxprüfung, HTTP-Abruf unter einem Projekt-Unterpfad, Bilddarstellung, Kopierfunktion und Browserprüfung bei 320, 390, 768 und 1280 CSS-Pixeln Breite ohne horizontalen Seitenüberlauf. Der PNG-QR-Code wurde zusätzlich mit dem unabhängigen Decoder jsQR 1.4.0 zurückgelesen; das Ergebnis stimmt exakt mit dem vorgegebenen Link einschließlich Query und Fragment überein. Es gab keine JavaScript-Warnungen oder -Fehler im geprüften Browserablauf. Reale iOS-/Android-Importe und Funkkommunikation wurden nicht getestet.
