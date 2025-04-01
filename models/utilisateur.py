from datetime import datetime
from py2neo import Node
from database.config import connect_to_neo4j

class Utilisateur:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.created_at = str(datetime.now())
        
    def save(self):
        utilisateur_node = Node("Utilisateur",
                                name=self.name,
                                email=self.email,
                                created_at=self.created_at)
        
        graph = connect_to_neo4j()
        graph.merge(utilisateur_node, "Utilisateur", "email")
        return utilisateur_node
    
    @staticmethod
    def get_all():
        graph = connect_to_neo4j()
        query = """
        MATCH (u:Utilisateur)
        RETURN id(u) AS id, u.name AS name, u.email AS email, u.created_at AS created_at
        """
        return graph.run(query).data()
    
    @staticmethod
    def get_by_id(user_id):
        graph = connect_to_neo4j()
        query = """
        MATCH (u:Utilisateur)
        WHERE id(u) = $user_id
        RETURN id(u) AS id, u.name AS name, u.email AS email, u.created_at AS created_at
        """
        result = graph.run(query, user_id=user_id).data()
        return result[0] if result else None
    
    @staticmethod
    def get_by_id_as_node(user_id):
        graph = connect_to_neo4j()
        query = """
        MATCH (u:Utilisateur)
        WHERE id(u) = $user_id
        RETURN u
        """
        result = graph.run(query, user_id=user_id).evaluate()
        print(result)
        print(type(result))
        print(user_id)
        return result
    
    @staticmethod
    def delete_user(user_id):
        graph = connect_to_neo4j()
        query = """
        MATCH (u:Utilisateur)
        WHERE id(u) = $user_id
        DELETE u
        """
        graph.run(query, user_id=user_id)
        
    @staticmethod
    def update_user(user_id, name=None, email=None):
        graph = connect_to_neo4j()
        query = """
        MATCH (u:Utilisateur)
        WHERE id(u) = $user_id
        SET u.name = $name, u.email = $email
        """
        graph.run(query, user_id=user_id, name=name, email=email)