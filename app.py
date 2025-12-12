import os
import json
from flask import Flask, jsonify
from neo4j import GraphDatabase


NEO4J_URI = os.environ.get("NEO4J_URI")
USER = os.environ.get("NEO4J_USER")
PASSWORD = os.environ.get("NEO4J_PASSWORD")


try:
    driver = GraphDatabase.driver(
        NEO4J_URI,
        auth=(USER, PASSWORD)
    )
    driver.verify_connectivity()
    print("STATUS: Połączenie Neo4j gotowe.")
except Exception as e:
    print(f"FATAL ERROR: Błąd połączenia Neo4j. Sprawdź hasło/URI. Szczegóły: {e}")
    driver = None

app = Flask(__name__)


@app.route('/hello', methods=['GET'])
def hello_world():
    if not driver:
        return jsonify({'error': 'Połączenie z bazą danych nieudane.'}), 500

    try:
        with driver.session() as session:
            msg = session.run('RETURN "LOCAL CONNECTION SUCCESSFUL (Render)!" AS m').single()['m']

        return jsonify({'message': msg}), 200

    except Exception as e:

        return jsonify({'error': f"Błąd bazy danych (Auth?): {str(e)}"}), 500



@app.route('/recommendations/<username>', methods=['GET'])
def get_recommendations(username):
    if not driver:
        return jsonify({'error': 'Połączenie z bazą danych nieudane.'}), 500


    cypher_query = """
    // Krok 1: Znajdź 5 najbardziej podobnych użytkowników
    MATCH (me:User {username: $username})-[:READS]->(b:Book)<-[:READS]->(other:User)
    WHERE other <> me
    WITH other, count(b) AS commonBooks
    ORDER BY commonBooks DESC
    LIMIT 5

    
    MATCH (other)-[:READS {rating: r}]->(recBook:Book)
    WHERE NOT EXISTS {
        MATCH (me)-[:READS]->(recBook)
    }
    
    RETURN recBook.title AS title,
           avg(r) AS avgRating
    ORDER BY avgRating DESC
    LIMIT 5
    """

    try:
        with driver.session() as session:

            result = session.run(cypher_query, username=username)
            recommendations = [{"title": record["title"], "avgRating": record["avgRating"]} for record in result]


        if not recommendations:
            return jsonify({
                               'message': f"Brak rekomendacji dla użytkownika {username}. Upewnij się, że użytkownik istnieje i ma relacje."}), 200

        return jsonify({'recommendations': recommendations}), 200

    except Exception as e:
        return jsonify({'error': f"Błąd wykonania zapytania: {str(e)}"}), 500

