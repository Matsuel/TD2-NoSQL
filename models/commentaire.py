from datetime import datetime
from py2neo import Node, Graph
from database.config import connect_to_neo4j
from constantes.node import NodeEnum

class Commentaire:
    def __init__(self, content, graph: Graph):
        self.content = content
        self.created_at = str(datetime.now())
        self.graph = graph
        
    def create_comment(self):
        comment_node = Node(NodeEnum.Commentaire.value, content=self.content, created_at=self.created_at)
        self.graph.create(comment_node)
        return comment_node
