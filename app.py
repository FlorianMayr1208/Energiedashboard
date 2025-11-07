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

# Historische Verbrauchsdaten für Vergleich
HISTORISCHE_DATEN_STROM = [
    {
        'zeitraum': '23.03.2022 - 06.03.2023',
        'verbrauch_kwh': 1448.00,
        'tage': 349,
        'durchschnitt_tag': 4.15
    },
    {
        'zeitraum': '07.03.2023 - 17.03.2024',
        'verbrauch_kwh': 1547.00,
        'tage': 377,
        'durchschnitt_tag': 4.10
    },
    {
        'zeitraum': '18.03.2024 - 17.03.2025',
        'verbrauch_kwh': 1591.01,
        'tage': 365,
        'durchschnitt_tag': 4.36
    }
]

# Historische Gasverbrauchsdaten (in kWh nach Umrechnung)
HISTORISCHE_DATEN_GAS = [
    {
        'zeitraum': '23.03.2022 - 06.03.2023',
        'verbrauch_kwh': 7391.00,
        'tage': 349,
        'durchschnitt_tag': 21.18
    },
    {
        'zeitraum': '07.03.2023 - 04.03.2024',
        'verbrauch_kwh': 7713.00,
        'tage': 364,
        'durchschnitt_tag': 21.19
    },
    {
        'zeitraum': '05.03.2024 - 03.03.2025',
        'verbrauch_kwh': 9719.00,
        'tage': 364,
        'durchschnitt_tag': 26.70
    }
]

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

    # Datum verwenden: entweder vom User oder aktuell
    if 'datum' in request.json and request.json['datum']:
        # Datum von datetime-local Input kommt im Format: 2023-03-17T14:30
        datum_str = request.json['datum']
        try:
            # Parse ISO format und konvertiere zu unserem Format
            datum_obj = datetime.fromisoformat(datum_str)
            datum_formatted = datum_obj.strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            # Falls Parsing fehlschlägt, verwende aktuelles Datum
            datum_formatted = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    else:
        # Kein Datum übergeben, verwende aktuelles
        datum_formatted = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    eintrag = {
        'datum': datum_formatted,
        'strom': float(request.json['strom']) if 'strom' in request.json and request.json['strom'] else None,
        'gas': float(request.json['gas']) if 'gas' in request.json and request.json['gas'] else None
    }

    data['eintraege'].append(eintrag)

    # Sortiere Einträge nach Datum (älteste zuerst)
    data['eintraege'].sort(key=lambda x: x['datum'])

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

@app.route('/api/vergleich')
def get_vergleich():
    """API Endpoint für Vergleich mit historischen Daten"""
    data = load_data()
    eintraege = data['eintraege']

    # Berechne aktuellen Stromverbrauch
    aktueller_verbrauch_strom = {
        'gesamt_kwh': 0,
        'tage': 0,
        'durchschnitt_tag': 0,
        'zeitraum': None
    }

    if len(eintraege) >= 2:
        # Finde erste und letzte Einträge mit Strom-Werten
        strom_eintraege = [e for e in eintraege if e.get('strom') is not None]

        if len(strom_eintraege) >= 2:
            erster = strom_eintraege[0]
            letzter = strom_eintraege[-1]

            # Parse Datum
            from datetime import datetime
            datum_erster = datetime.strptime(erster['datum'], '%Y-%m-%d %H:%M:%S')
            datum_letzter = datetime.strptime(letzter['datum'], '%Y-%m-%d %H:%M:%S')

            tage = (datum_letzter - datum_erster).days
            verbrauch = letzter['strom'] - erster['strom']

            if tage > 0:
                aktueller_verbrauch_strom = {
                    'gesamt_kwh': round(verbrauch, 2),
                    'tage': tage,
                    'durchschnitt_tag': round(verbrauch / tage, 2),
                    'zeitraum': f"{datum_erster.strftime('%d.%m.%Y')} - {datum_letzter.strftime('%d.%m.%Y')}"
                }

    # Berechne aktuellen Gasverbrauch (in kWh)
    aktueller_verbrauch_gas = {
        'gesamt_kwh': 0,
        'tage': 0,
        'durchschnitt_tag': 0,
        'zeitraum': None
    }

    if len(eintraege) >= 2:
        # Finde erste und letzte Einträge mit Gas-Werten
        gas_eintraege = [e for e in eintraege if e.get('gas') is not None]

        if len(gas_eintraege) >= 2:
            erster = gas_eintraege[0]
            letzter = gas_eintraege[-1]

            # Parse Datum
            from datetime import datetime
            datum_erster = datetime.strptime(erster['datum'], '%Y-%m-%d %H:%M:%S')
            datum_letzter = datetime.strptime(letzter['datum'], '%Y-%m-%d %H:%M:%S')

            tage = (datum_letzter - datum_erster).days
            verbrauch_m3 = letzter['gas'] - erster['gas']
            verbrauch_kwh = verbrauch_m3 * BRENNWERT * ZUSTANDSZAHL

            if tage > 0:
                aktueller_verbrauch_gas = {
                    'gesamt_kwh': round(verbrauch_kwh, 2),
                    'gesamt_m3': round(verbrauch_m3, 2),
                    'tage': tage,
                    'durchschnitt_tag': round(verbrauch_kwh / tage, 2),
                    'zeitraum': f"{datum_erster.strftime('%d.%m.%Y')} - {datum_letzter.strftime('%d.%m.%Y')}"
                }

    # Berechne historischen Durchschnitt Strom
    if HISTORISCHE_DATEN_STROM:
        hist_durchschnitt_strom = sum(d['durchschnitt_tag'] for d in HISTORISCHE_DATEN_STROM) / len(HISTORISCHE_DATEN_STROM)
    else:
        hist_durchschnitt_strom = 0

    # Berechne historischen Durchschnitt Gas
    if HISTORISCHE_DATEN_GAS:
        hist_durchschnitt_gas = sum(d['durchschnitt_tag'] for d in HISTORISCHE_DATEN_GAS) / len(HISTORISCHE_DATEN_GAS)
    else:
        hist_durchschnitt_gas = 0

    return jsonify({
        'strom': {
            'historisch': HISTORISCHE_DATEN_STROM,
            'historischer_durchschnitt': round(hist_durchschnitt_strom, 2),
            'aktuell': aktueller_verbrauch_strom
        },
        'gas': {
            'historisch': HISTORISCHE_DATEN_GAS,
            'historischer_durchschnitt': round(hist_durchschnitt_gas, 2),
            'aktuell': aktueller_verbrauch_gas
        }
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
