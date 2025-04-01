from py2neo import Relationship
from database.config import connect_to_neo4j

def create_relationship(node1, node2, relationship_type):
    graph = connect_to_neo4j()
    relationship = Relationship(node1, relationship_type, node2)
    graph.create(relationship)
    return relationship