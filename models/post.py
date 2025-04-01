from datetime import datetime
from py2neo import Node
from database.config import connect_to_neo4j

class Post:
    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.created_at = str(datetime.now())
        
    def save(self):
        post_node = Node("Post",
                         title=self.title,
                         content=self.content,
                         created_at=self.created_at)
        
        graph = connect_to_neo4j()
        graph.merge(post_node, "Post", "title")
        return post_node
    
    def get_all():
        graph = connect_to_neo4j()
        query = """
        MATCH (p:Post)
        RETURN id(p) AS id, p.title AS title, p.content AS content, p.created_at AS created_at
        """
        return graph.run(query).data()
    
    @staticmethod
    def get_by_id(post_id):
        graph = connect_to_neo4j()
        query = """
        MATCH (p:Post)
        WHERE id(p) = $post_id
        RETURN id(p) AS id, p.title AS title, p.content AS content, p.created_at AS created_at
        """
        result = graph.run(query, post_id=post_id).data()
        return result[0] if result else None
    
    @staticmethod
    def update_post(post_id, title=None, content=None):
        graph = connect_to_neo4j()
        query = """
        MATCH (p:Post)
        WHERE id(p) = $post_id
        SET p.title = $title, p.content = $content
        """
        graph.run(query, post_id=post_id, title=title, content=content)
        
    @staticmethod
    def delete_post(post):
        graph = connect_to_neo4j()
        graph.delete(post)