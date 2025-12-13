import json
from flask import Flask
from neo4j import GraphDatabase
import os

NEO4J_URI = os.environ.get("NEO4J_URI")
USER = os.environ.get("NEO4J_USER")
PASSWORD = os.environ.get("NEO4J_PASSWORD")

try:
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

@app.route('/', methods=['GET'])
def index():
    return open('index.html').read()

@app.route('/hello', methods=['GET'])
def hello_world():
    if not driver:
        return json.dumps({'error': 'Brak Neo4j'}), 500
    try:
        with driver.session(database="neo4j") as session:
            msg = session.run('RETURN "System rekomendacji książek działa!" AS m').single()['m']
        return json.dumps({'message': msg}), 200
    except Exception as e:
        return json.dumps({'error': str(e)}), 500

@app.route('/recommendations/<username>', methods=['GET'])
def recommendations(username):
    if not driver:
        return json.dumps({'error': 'Brak połączenia z Neo4j'}), 500
    
    try:
        with driver.session(database="neo4j") as session:
            # Zapytanie: Znajdź podobnych użytkowników i poleć książki
            result = session.run("""
                MATCH (me:User {username: $username})-[:READS]->(b:Book)<-[:READS]-(other:User)
                WHERE other <> me
                WITH other, COUNT(DISTINCT b) AS commonBooks
                ORDER BY commonBooks DESC
                LIMIT 5
                
                MATCH (other)-[r:READS]->(recBook:Book)
                WHERE NOT EXISTS {
                    MATCH (me:User {username: $username})-[:READS]->(recBook)
                }
                
                RETURN recBook.title AS title, 
                       recBook.isbn AS isbn,
                       AVG(r.rating) AS avgRating,
                       COUNT(other) AS recommenders
                ORDER BY avgRating DESC, recommenders DESC
                LIMIT 5
            """, username=username)
            
            recommendations = []
            for record in result:
                recommendations.append({
                    'title': record['title'],
                    'isbn': record['isbn'],
                    'avgRating': round(record['avgRating'], 2),
                    'recommenders': record['recommenders']
                })
            
            return json.dumps({
                'user': username,
                'recommendations': recommendations,
                'count': len(recommendations)
            }), 200
            
    except Exception as e:
        return json.dumps({'error': str(e)}), 500
