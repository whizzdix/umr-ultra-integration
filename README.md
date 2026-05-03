# Unifi Mobile Router Ultra (UMR-Ultra) Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

Diese benutzerdefinierte Integration (Custom Component) verbindet den **Unifi Mobile Router Ultra (UMR-Ultra)** lokal mit deinem Home Assistant über die ubus REST-API. Sie ermöglicht das Auslesen der wichtigsten Betriebs- und Netzwerkdaten des Routers, um sie für Dashboards und Automatisierungen nutzbar zu machen.

## 🌟 Features

Die Integration stellt automatisch eine Vielzahl von Sensoren bereit, die im konfigurierten Intervall lokal vom Router abgerufen werden:

- **Netzwerk- & Verbindungsinformationen:** Öffentliche IP, IPv4-Adresse, Betreiber (Operator), APN, Verbundene Clients.
- **Empfang & Signal:** LTE-Modus, RSSI, RSRQ, RSRP, Signal Level.
- **Hardware & SIM:** ICCID, IMSI, CPU-Auslastung, Speicherauslastung, Latenz (Durchschnitt).
- **Datenverbrauch:** Download, Upload und Gesamtverbrauch (automatisch und lesbar in Megabyte (MB) umgerechnet).
- **Betriebszeit (Uptime):** Leicht lesbare Formatierung (z.B. "2 Tage, 4 Std., 12 Min.").
- **Nächstes Update:** Ein intelligenter Home Assistant Timestamp-Sensor, der als interaktiver, sekündlicher Live-Countdown ("in 45 Sekunden") in der Benutzeroberfläche gerendert wird, ohne die Datenbank zu belasten.
- **Geräteinformationen:** Die aktuelle Firmware-Version wird nahtlos in den nativen Home Assistant Geräteinformationen verlinkt.

## 🚀 Installation

### Option 1: Über HACS (Empfohlen)
Da diese Integration noch nicht im Standard-HACS-Verzeichnis ist, kannst du sie als benutzerdefiniertes Repository hinzufügen:
1. Öffne Home Assistant und gehe zu **HACS** -> **Integrationen**.
2. Klicke oben rechts auf das Drei-Punkte-Menü und wähle **Benutzerdefinierte Repositories (Custom repositories)**.
3. Füge die URL dieses GitHub-Repositories ein und wähle als Kategorie **Integration**.
4. Suche nun in HACS nach `UMR-Ultra` und klicke auf Herunterladen/Installieren.
5. Starte Home Assistant neu.

### Option 2: Manuelle Installation
1. Lade dir dieses Repository als ZIP-Datei herunter.
2. Kopiere den gesamten Ordner `custom_components/umr_ultra` in das Verzeichnis `custom_components/` in deiner Home Assistant Installation (erstelle den Ordner `custom_components`, falls er nicht existiert).
3. Starte Home Assistant neu.

## ⚙️ Konfiguration

Die Einrichtung erfolgt vollständig über die Home Assistant Benutzeroberfläche (Config Flow). Du musst keine YAML-Dateien anpassen!

1. Gehe in Home Assistant zu **Einstellungen** -> **Geräte & Dienste**.
2. Klicke unten rechts auf **Integration hinzufügen**.
3. Suche nach **UMR-Ultra**.
4. Gib die Verbindungsdaten deines Routers ein:
   - **IP-Adresse:** (Standard: `192.168.105.1`)
   - **Benutzername:** Dein Router-Login (häufig `ui` oder `root`)
   - **Passwort:** Dein Router-Passwort
   - **Aktualisierungsintervall:** Zeit in Sekunden, in der die Daten neu abgerufen werden sollen (Standard: `60` Sekunden).

Sobald die Zugangsdaten geprüft wurden, wird das Gerät angelegt und die Sensoren stehen sofort zur Verfügung!

---
*Hinweis: Dies ist eine inoffizielle Integration und steht in keiner direkten Verbindung zu Ubiquiti Inc.*
