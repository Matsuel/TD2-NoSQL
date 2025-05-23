from py2neo import Graph
from constantes.node import NodeEnum

def node_exists(graph: Graph, node_id: int, node_type: NodeEnum):
    """
    Check if a node exists in the Neo4j database.

    :param graph: The Neo4j graph object.
    :param node_id: The ID of the node to check.
    :param node_type: The type of the node (e.g., NodeEnum.Post).
    :return: True if the node exists, False otherwise.
    """
    try:
        node = graph.nodes.get(node_id)
        if node and node.labels == {node_type.value}:
            return node
        return False
    except Exception as e:
        print(f"Error checking node existence: {e}")
        return False
        
def get_all_nodes(graph: Graph, node_type: NodeEnum):
    """
    Get all nodes of a specific type from the Neo4j database.

    :param graph: The Neo4j graph object.
    :param node_type: The type of the node (e.g., NodeEnum.Post).
    :return: A list of nodes of the specified type.
    """
    try:
        nodes = graph.nodes.match(node_type.value).all()
        return nodes
    except Exception as e:
        print(f"Error getting all nodes: {e}")
        return []