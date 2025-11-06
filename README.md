# ⚡ Energiedashboard

Einfaches Dashboard zur Erfassung und Visualisierung deines Strom- und Gasverbrauchs auf dem Raspberry Pi.

## 🎯 Features

- ✅ **Super einfache Eingabe** - Nur zwei Zahlen eingeben, fertig!
- ✅ **Progressive Web App (PWA)** - Installierbar auf iOS & Android
- ✅ **Keine Datenbank** - Alles in einer einfachen JSON-Datei
- ✅ **Interaktive Charts** - Visualisierung deines Verbrauchs
- ✅ **Responsive Design** - Funktioniert auf allen Geräten

## 🚀 Installation auf Raspberry Pi

### 1. Abhängigkeiten installieren

```bash
# Python und pip updaten
sudo apt update
sudo apt install python3 python3-pip -y

# Projekt klonen oder Dateien hochladen
cd /home/pi
git clone <dein-repo>
cd Energiedashboard

# Python-Abhängigkeiten installieren
pip3 install -r requirements.txt
```

### 2. App starten

```bash
python3 app.py
```

Die App läuft jetzt auf: `http://localhost:5001`

### 3. Von anderen Geräten zugreifen

Finde die IP-Adresse deines Raspberry Pi:
```bash
hostname -I
```

Greife von deinem Handy zu: `http://192.168.x.x:5001`

## 📱 Als App auf dem Handy installieren

### iOS (Safari):
1. Öffne `http://deine-pi-ip:5001/eingabe` in Safari
2. Tippe auf den "Teilen"-Button
3. Scrolle runter und wähle "Zum Home-Bildschirm"
4. Bestätige mit "Hinzufügen"

### Android (Chrome):
1. Öffne `http://deine-pi-ip:5001/eingabe` in Chrome
2. Tippe auf die drei Punkte (Menü)
3. Wähle "App installieren" oder "Zum Startbildschirm hinzufügen"

## 🔧 Autostart einrichten (Optional)

Damit die App automatisch beim Raspberry Pi Start läuft:

```bash
# Systemd Service erstellen
sudo nano /etc/systemd/system/energiedashboard.service
```

Füge folgendes ein:

```ini
[Unit]
Description=Energiedashboard
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/Energiedashboard
ExecStart=/usr/bin/python3 /home/pi/Energiedashboard/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Aktivieren:
```bash
sudo systemctl enable energiedashboard.service
sudo systemctl start energiedashboard.service
```

Status prüfen:
```bash
sudo systemctl status energiedashboard.service
```

## 📊 Verwendung

1. **Eingabe**: Öffne `/eingabe` und gib deine Zählerstände ein
2. **Dashboard**: Öffne `/` um deine Statistiken und Verbrauchsgrafiken zu sehen

## 🗂️ Datenstruktur

Alle Daten werden in `data/verbrauch.json` gespeichert:

```json
{
  "eintraege": [
    {
      "datum": "2025-11-06 10:30:00",
      "strom": 12345.5,
      "gas": 6789.2
    }
  ]
}
```

## 🔒 Sicherheit

⚠️ **Wichtig**: Standardmäßig läuft die App im Debug-Modus und ist für jeden im Netzwerk zugänglich.

Für Produktivbetrieb:
- Setze `debug=False` in `app.py`
- Nutze einen WSGI Server wie Gunicorn
- Aktiviere HTTPS (z.B. mit Let's Encrypt)

## 🎨 Anpassungen

- **Design ändern**: Bearbeite die `<style>` Blöcke in den HTML-Dateien
- **Weitere Daten**: Erweitere die JSON-Struktur und Formulare
- **Kostenberechnung**: Füge Preise pro kWh/m³ hinzu

## 📝 Tipps

- Trage deine Zählerstände regelmäßig ein (z.B. wöchentlich)
- Die App berechnet automatisch den Verbrauch zwischen den Einträgen
- Backup deiner `data/verbrauch.json` nicht vergessen!

## 🐛 Probleme?

- **App nicht erreichbar?** Prüfe die Firewall: `sudo ufw allow 5001`
- **Fehler beim Start?** Prüfe die Logs: `python3 app.py`
- **Daten weg?** Schau in `data/verbrauch.json`

## 📦 Projektstruktur

```
Energiedashboard/
├── app.py                  # Flask App
├── requirements.txt        # Python Dependencies
├── data/
│   └── verbrauch.json     # Deine Daten
├── static/
│   ├── sw.js              # Service Worker für PWA
│   └── icon.svg           # App Icon
└── templates/
    ├── dashboard.html     # Dashboard Ansicht
    └── eingabe.html       # Eingabe-Formular
```

## 🚀 Nächste Schritte (Optional)

- [ ] Kosten-Rechner hinzufügen
- [ ] Export-Funktion (CSV Download)
- [ ] Benachrichtigungen bei hohem Verbrauch
- [ ] Vergleich mit Vorjahr
- [ ] Wetterintegration (Korrelation)

Viel Spaß mit deinem Energiedashboard! ⚡
