from constantes.relation import RelationEnum
from py2neo import Graph, Node, Relationship

def create_relation(node1, node2, relation_type: RelationEnum, graph: Graph):
    """
    Create a relationship between two nodes in the graph database.
    
    :param node1: The first node (source) to create the relationship from.
    :param node2: The second node (target) to create the relationship to.
    :param relation_type: The type of relationship to create.
    :param graph: The graph database instance.
    """
    try:
        relation = Relationship(node1, relation_type.value, node2)
        graph.create(relation)
        return relation
    except Exception as e:
        print(f"Error creating relationship: {e}")
        return None

def delete_relation(node1, node2, relation_type: RelationEnum, graph: Graph):
    """
    Delete a relationship between two nodes in the graph database.
    
    :param node1: The first node (source) to delete the relationship from.
    :param node2: The second node (target) to delete the relationship to.
    :param relation_type: The type of relationship to delete.
    :param graph: The graph database instance.
    """
    try:
        relation = graph.match((node1, node2), r_type=relation_type.value).first()
        if relation is not None:
            graph.separate(relation)
            return True
        return False
    except Exception as e:
        print(f"Error deleting relationship: {e}")
        return False
    
def delete_all_relations(node1, node2, graph: Graph):
    """
    Delete all relationships of a node in the graph database.
    
    :param node1: The first node (source) to delete the relationships from.
    :param node2: The second node (target) to delete the relationships to.
    :param graph: The graph database instance.
    """
    try:
        relations = graph.match((node1, node2)).all()
        for relation in relations:
            graph.separate(relation)
        return True
    except Exception as e:
        print(f"Error deleting all relationships: {e}")
        return False