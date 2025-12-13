import json
from flask import Flask
from neo4j import GraphDatabase
import os

NEO4J_URI = os.environ.get("NEO4J_URI")
USER = os.environ.get("NEO4J_USER")
PASSWORD = os.environ.get("NEO4J_PASSWORD")

try:
    # ZMIANA: dodaj max_connection_lifetime=0 dla AuraDB Free
    driver = GraphDatabase.driver(
        NEO4J_URI, 
        auth=(USER, PASSWORD),
        max_connection_lifetime=0
    )
    driver.verify_connectivity()
    print(" Neo4j OK")
except Exception as e:
    print(f" Neo4j: {e}")
    driver = None

app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def hello_world():
    if not driver:
        return json.dumps({'error': 'Brak Neo4j'}), 500
    try:
        with driver.session(database="neo4j") as session:
            msg = session.run('RETURN "DZIAŁA NA RENDER!" AS m').single()['m']
        return json.dumps({'message': msg}), 200
    except Exception as e:
        return json.dumps({'error': str(e)}), 500
