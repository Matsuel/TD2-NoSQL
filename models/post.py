from datetime import datetime
from py2neo import Node, Graph
from constantes.node import NodeEnum

class Post:
    def __init__(self, title, content, graph: Graph):
        self.title = title
        self.content = content
        self.created_at = str(datetime.now())
        self.graph = graph
        
    def create_post(self):
        post_node = Node(NodeEnum.Post.value, title=self.title, content=self.content, created_at=self.created_at)
        self.graph.create(post_node)
        return post_node
        
    