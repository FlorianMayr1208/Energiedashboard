# 📱 PWA Installation - Energiedashboard

Dein Energiedashboard ist jetzt eine vollständige **Progressive Web App (PWA)**!

## ✨ Was bedeutet das?

Du kannst die App auf deinem Smartphone **wie eine native App** installieren:
- ✅ Eigenes App-Icon auf dem Homescreen
- ✅ Läuft ohne Browser-UI (Vollbild)
- ✅ Schnellerer Start durch Caching
- ✅ Funktioniert teilweise offline
- ✅ iOS & Android kompatibel

## 📱 Installation auf Android / Chrome

1. Öffne `http://deine-pi-ip:5001` in **Chrome**
2. Tippe auf die **drei Punkte** (⋮) oben rechts
3. Wähle **"App installieren"** oder **"Zum Startbildschirm hinzufügen"**
4. Bestätige mit **"Installieren"**
5. Das App-Icon erscheint auf deinem Homescreen! 🎉

### Alternative: Install-Button im Dashboard
- Wenn verfügbar, erscheint ein Button **"📱 Als App installieren"** im Dashboard
- Einfach draufklicken und Installation bestätigen

## 🍎 Installation auf iOS / Safari

Apple erlaubt nur manuelle Installation:

1. Öffne `http://deine-pi-ip:5001` in **Safari** (nicht Chrome!)
2. Tippe auf das **Teilen-Symbol** (□↑) unten in der Mitte
3. Scrolle runter und wähle **"Zum Home-Bildschirm"**
4. Gib einen Namen ein (z.B. "Energie")
5. Tippe auf **"Hinzufügen"**
6. Das App-Icon erscheint auf deinem Homescreen! 🎉

### iOS-Besonderheiten
- ⚠️ Muss in **Safari** geöffnet werden (Chrome funktioniert nicht)
- ⚠️ Automatischer Install-Prompt nicht verfügbar (nur manuell)
- ⚠️ Cache wird nach 7 Tagen Inaktivität gelöscht
- ✅ Deine Daten sind trotzdem sicher (auf dem Pi gespeichert!)

## 🔍 Überprüfen ob installiert

**Android:**
- App erscheint in der App-Liste
- Beim Öffnen: Kein Browser-UI sichtbar

**iOS:**
- App erscheint auf Homescreen mit Icon
- Beim Öffnen: Läuft im Vollbild

## 🚀 Nach der Installation

Die installierte App:
- ✅ Lädt schneller (gecachte Dateien)
- ✅ Funktioniert teilweise offline (gecachte Seiten)
- ✅ Sieht aus wie eine native App
- ✅ Kann direkt vom Homescreen gestartet werden

## 💾 Was wird gecacht?

Der Service Worker cached automatisch:
- Eingabe-Seite
- Dashboard
- App-Icons
- Chart.js Bibliothek

**Wichtig:** Deine Zählerstände werden auf dem **Raspberry Pi gespeichert**,
nicht im Browser-Cache!

## 🔄 App-Updates

**Android:**
- Service Worker updated automatisch
- Einfach App neu öffnen

**iOS:**
- App muss neu installiert werden für Updates
- Alte Version vom Homescreen löschen und neu installieren

## ⚠️ Troubleshooting

**"App installieren" Button erscheint nicht:**
- Android: Warte kurz oder lade Seite neu
- iOS: Nutze manuelle Installation (siehe oben)

**App lädt nicht:**
- Überprüfe WLAN-Verbindung
- Raspberry Pi muss laufen
- Port 5001 muss erreichbar sein

**Icons werden nicht angezeigt:**
- Icons wurden generiert in `static/icon-192.png` und `icon-512.png`
- Bei Problemen: `python3 generate_icons.py` neu ausführen

## 🛠️ Technische Details

**PWA Features:**
- ✅ Web App Manifest (`/manifest.json`)
- ✅ Service Worker mit Offline-Caching (`static/sw.js`)
- ✅ App Icons (192x192 und 512x512)
- ✅ Theme Color & Splash Screen
- ✅ Standalone Display Mode

**Caching-Strategie:**
- **Network-First:** Versucht zuerst Server, dann Cache
- Gut für dynamische Daten (deine Zählerstände)
- Fallback auf gecachte Version bei Offline

## 📊 PWA vs. Native App

| Feature | PWA | Native App |
|---------|-----|------------|
| Installation | Einfach (Browser) | App Store nötig |
| Updates | Automatisch | App Store |
| Größe | ~100 KB | 5-50 MB |
| Plattformen | iOS & Android | Separate Entwicklung |
| Offline | Teilweise | Vollständig |
| Push-Notifications | Android: Ja, iOS: Nein | Beide: Ja |

## 🎯 Fazit

Deine PWA bietet:
- ✅ **90% native App Feeling**
- ✅ **Funktioniert auf iOS & Android**
- ✅ **Keine App Store Abhängigkeit**
- ✅ **Automatische Updates** (außer iOS)
- ✅ **Klein & schnell**

Perfekt für dein Energiedashboard! ⚡

---

Bei Fragen: Siehe `README.md` für weitere Informationen.
