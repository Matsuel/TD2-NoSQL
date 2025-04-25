from datetime import datetime
from py2neo import Graph, Node
from constantes.node import NodeEnum

class Utilisateur:
    def __init__(self, graph: Graph, name: str, email: str):
        self.graph = graph
        self.name = name
        self.email = email
        self.created_at = str(datetime.now())
        
    def create_user(self):
        user_node = Node(NodeEnum.Utilisateur.value, name=self.name, email=self.email, created_at=self.created_at)
        self.graph.create(user_node)
        return user_node

