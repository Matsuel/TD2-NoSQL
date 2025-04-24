from datetime import datetime
from py2neo import Node
from database.config import connect_to_neo4j

class Commentaire:
    def __init__(self, content, post_id):
        self.content = content
        self.post_id = post_id
        self.created_at = str(datetime.now())
        self.comment_id = None
        
    def save(self):
        graph = connect_to_neo4j()
        comment_node = Node("Comment",
                            content=self.content,
                            created_at=self.created_at)
        graph.merge(comment_node, "Comment", "content")
        self.comment_id = comment_node.identity
        return comment_node
    
    def link_to_post(self, post_id):
        graph = connect_to_neo4j()
        query = """
        MATCH (p:Post), (c:Comment)
        WHERE id(p) = $post_id AND id(c) = $comment_id
        CREATE (p)-[:HAS_COMMENT]->(c)
        """
        graph.run(query, post_id=post_id, comment_id=self.comment_id)
        
    def link_to_user(self, user_id):
        graph = connect_to_neo4j()
        query = """
        MATCH (u:User), (c:Comment)
        WHERE id(u) = $user_id AND id(c) = $comment_id
        CREATE (u)-[:CREATED]->(c)
        """
        graph.run(query, user_id=user_id, comment_id=self.comment_id)
