import os
import json
from flask import Flask, jsonify  # Dodajemy jsonify dla lepszych odpowiedzi
from neo4j import GraphDatabase
import sys, os

# --- 1. Konfiguracja (Render Użyje Zmiennych Środowiskowych) ---
# Te zmienne będą pobierane z ustawień Render.com
NEO4J_URI = os.environ.get("NEO4J_URI")
USER = os.environ.get("NEO4J_USER")
PASSWORD = os.environ.get("NEO4J_PASSWORD")

# --- 2. Inicjalizacja Neo4j ---
# Używamy najprostszej metody połączenia, która działa (URI + Auth)
try:
    driver = GraphDatabase.driver(
        NEO4J_URI,
        auth=(USER, PASSWORD)
        # Opcja "encrypted=True" jest zbędna i powodowała błąd.
    )
    # Weryfikacja połączenia
    driver.verify_connectivity()
    print("STATUS: Połączenie Neo4j gotowe.")
except Exception as e:
    print(f"FATAL ERROR: Błąd połączenia Neo4j. Sprawdź hasło/URI. Szczegóły: {e}")
    driver = None

# --- 3. Inicjalizacja Aplikacji Flask ---
app = Flask(__name__)


# --- 4. Definicja Endpointu /hello (Test Połączenia) ---
@app.route('/hello', methods=['GET'])
def hello_world():
    if not driver:
        return jsonify({'error': 'Połączenie z bazą danych nieudane.'}), 500

    try:
        with driver.session() as session:
            msg = session.run('RETURN "LOCAL CONNECTION SUCCESSFUL (Render)!" AS m').single()['m']

        return jsonify({'message': msg}), 200  # Używamy jsonify

    except Exception as e:
        # Ten błąd wskaże na zły login/hasło Neo4j, jeśli wszystko inne działa
        return jsonify({'error': f"Błąd bazy danych (Auth?): {str(e)}"}), 500

# Kod do uruchomienia serwera jest przekazywany przez Gunicorn (Render), więc usuwamy sekcję if __name__ == '__main__':