from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

# Pfad zur JSON-Datei
DATA_FILE = 'data/verbrauch.json'

# Gas-Umrechnung: m³ → kWh
BRENNWERT = 11.493  # kWh/m³
ZUSTANDSZAHL = 0.947

def init_data_file():
    """Erstellt die JSON-Datei, falls sie nicht existiert"""
    os.makedirs('data', exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump({"eintraege": []}, f)

def load_data():
    """Lädt die Daten aus der JSON-Datei"""
    init_data_file()
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    """Speichert Daten in die JSON-Datei"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def index():
    """Hauptseite - Dashboard"""
    return render_template('dashboard.html')

@app.route('/eingabe')
def eingabe():
    """Eingabe-Seite für neue Zählerstände"""
    return render_template('eingabe.html')

@app.route('/api/speichern', methods=['POST'])
def speichern():
    """API Endpoint zum Speichern neuer Zählerstände"""
    data = load_data()

    eintrag = {
        'datum': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'strom': float(request.json['strom']) if 'strom' in request.json and request.json['strom'] else None,
        'gas': float(request.json['gas']) if 'gas' in request.json and request.json['gas'] else None
    }

    data['eintraege'].append(eintrag)
    save_data(data)

    return jsonify({'status': 'success', 'message': 'Daten gespeichert!'})

@app.route('/api/daten')
def get_daten():
    """API Endpoint zum Abrufen aller Daten"""
    data = load_data()

    # Berechne Verbrauch zwischen Einträgen
    eintraege = data['eintraege']

    # Rechne Gas m³ in kWh um (nur wenn Gas-Wert vorhanden)
    for i, eintrag in enumerate(eintraege):
        if eintrag.get('gas') is not None:
            eintrag['gas_kwh'] = round(eintrag['gas'] * BRENNWERT * ZUSTANDSZAHL, 2)
        else:
            eintrag['gas_kwh'] = None

        # Füge Index hinzu für Lösch-Funktion
        eintrag['index'] = i

    if len(eintraege) > 1:
        for i in range(len(eintraege)-1, 0, -1):
            # Strom-Verbrauch berechnen (nur wenn beide Werte vorhanden)
            if eintraege[i].get('strom') is not None and eintraege[i-1].get('strom') is not None:
                eintraege[i]['strom_verbrauch'] = round(
                    eintraege[i]['strom'] - eintraege[i-1]['strom'], 2
                )
            else:
                eintraege[i]['strom_verbrauch'] = None

            # Gas-Verbrauch berechnen (nur wenn beide Werte vorhanden)
            if eintraege[i].get('gas') is not None and eintraege[i-1].get('gas') is not None:
                eintraege[i]['gas_verbrauch_m3'] = round(
                    eintraege[i]['gas'] - eintraege[i-1]['gas'], 2
                )
                eintraege[i]['gas_verbrauch_kwh'] = round(
                    eintraege[i]['gas_verbrauch_m3'] * BRENNWERT * ZUSTANDSZAHL, 2
                )
            else:
                eintraege[i]['gas_verbrauch_m3'] = None
                eintraege[i]['gas_verbrauch_kwh'] = None

    return jsonify(data)

@app.route('/api/loeschen/<int:index>', methods=['DELETE'])
def loeschen(index):
    """API Endpoint zum Löschen eines Eintrags"""
    data = load_data()

    if 0 <= index < len(data['eintraege']):
        geloeschter_eintrag = data['eintraege'].pop(index)
        save_data(data)
        return jsonify({'status': 'success', 'message': 'Eintrag gelöscht!', 'geloescht': geloeschter_eintrag})
    else:
        return jsonify({'status': 'error', 'message': 'Ungültiger Index'}), 400

@app.route('/api/config')
def get_config():
    """API Endpoint für Konfigurationswerte"""
    return jsonify({
        'brennwert': BRENNWERT,
        'zustandszahl': ZUSTANDSZAHL
    })

@app.route('/manifest.json')
def manifest():
    """PWA Manifest"""
    return jsonify({
        "name": "Energiedashboard",
        "short_name": "Energie",
        "description": "Strom & Gas Verbrauch tracken",
        "start_url": "/eingabe",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#4CAF50",
        "icons": [
            {
                "src": "/static/icon-192.png",
                "sizes": "192x192",
                "type": "image/png"
            },
            {
                "src": "/static/icon-512.png",
                "sizes": "512x512",
                "type": "image/png"
            }
        ]
    })

if __name__ == '__main__':
    init_data_file()
    app.run(host='0.0.0.0', port=5001, debug=True)
