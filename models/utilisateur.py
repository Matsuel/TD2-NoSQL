from datetime import datetime
from py2neo import Node
from database.config import connect_to_neo4j

class Utilisateur:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.created_at = str(datetime.now())
        
    def save(self):
        utilisateur_node = Node("User",
                                name=self.name,
                                email=self.email,
                                created_at=self.created_at)
        
        graph = connect_to_neo4j()
        graph.merge(utilisateur_node, "User", "email")
        return utilisateur_node
    
    @staticmethod
    def get_all():
        graph = connect_to_neo4j()
        query = """
        MATCH (u:User)
        RETURN id(u) AS id, u.name AS name, u.email AS email, u.created_at AS created_at
        """
        return graph.run(query).data()
    
    @staticmethod
    def get_by_id(user_id):
        graph = connect_to_neo4j()
        query = """
        MATCH (u:User)
        WHERE id(u) = $user_id
        RETURN id(u) AS id, u.name AS name, u.email AS email, u.created_at AS created_at
        """
        result = graph.run(query, user_id=user_id).data()
        return result[0] if result else None
    
    @staticmethod
    def get_by_id_as_node(user_id):
        graph = connect_to_neo4j()
        query = """
        MATCH (u:User)
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
        MATCH (u:User)
        WHERE id(u) = $user_id
        DELETE u
        """
        graph.run(query, user_id=user_id)
        
    @staticmethod
    def update_user(user_id, name=None, email=None):
        graph = connect_to_neo4j()
        query = """
        MATCH (u:User)
        WHERE id(u) = $user_id
        SET u.name = $name, u.email = $email
        """
        graph.run(query, user_id=user_id, name=name, email=email)
        
    @staticmethod
    def get_friends(user_id):
        graph = connect_to_neo4j()
        query = """
        MATCH (u:User)-[:FRIENDS_WITH]->(f:User)
        WHERE id(u) = $user_id
        RETURN id(f) AS id, f.name AS name, f.email AS email
        """
        return graph.run(query, user_id=user_id).data()
    
    @staticmethod
    def add_friend(user_id, friend_id):
        graph = connect_to_neo4j()
        query = """
        MATCH (u:User)
        WHERE id(u) = $user_id
        MATCH (f:User)
        WHERE id(f) = $friend_id
        CREATE (u)-[:FRIENDS_WITH]->(f)
        """
        graph.run(query, user_id=user_id, friend_id=friend_id)
        
    @staticmethod
    def delete_friend(user_id, friend_id):
        graph = connect_to_neo4j()
        query = """
        MATCH (u:User)-[r:FRIENDS_WITH]->(f:User)
        WHERE id(u) = $user_id AND id(f) = $friend_id
        DELETE r
        """
        graph.run(query, user_id=user_id, friend_id=friend_id)
        
    @staticmethod
    def is_friend(user_id, friend_id):
        graph = connect_to_neo4j()
        query = """
        MATCH (u:User)-[r:FRIENDS_WITH]->(f:User)
        WHERE id(u) = $user_id AND id(f) = $friend_id
        RETURN count(r) > 0 AS is_friend
        """
        result = graph.run(query, user_id=user_id, friend_id=friend_id).data()
        return result[0]['is_friend'] if result else False
    
    @staticmethod
    def get_mutual_friends(user_id, other_id):
        graph = connect_to_neo4j()
        query = """
        MATCH (u:User)-[:FRIENDS_WITH]->(f:User)-[:FRIENDS_WITH]->(o:User)
        WHERE id(u) = $user_id AND id(o) = $other_id
        RETURN id(f) AS id, f.name AS name
        """
        return graph.run(query, user_id=user_id, other_id=other_id).data()
    
    
