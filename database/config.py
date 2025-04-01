from py2neo import Graph
from dotenv import load_dotenv

def connect_to_neo4j():
    load_dotenv()
    # Connexion à la base de données Neo4j
    graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))
    return graph