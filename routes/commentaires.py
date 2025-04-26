from flask import Blueprint, request, jsonify
from models.commentaire import Commentaire
from constantes.node import NodeEnum
from constantes.relation import RelationEnum
from database.config import graph
from utils.node import node_exists
from utils.relations import create_relation, delete_all_relations, delete_relation

commentaires_bp = Blueprint('commentaires', __name__)

@commentaires_bp.route('/posts/<int:post_id>/comments', methods=['GET'])
def get_comments(post_id):
    post = node_exists(graph, post_id, NodeEnum.Post)
    if post:
        comments = graph.match((post, None), r_type=RelationEnum.HasComment.value).all()
        comments_list = []
        for comment in comments:
            comment_data = {
                "id": comment.end_node.identity,
                "content": comment.end_node["content"],
                "created_at": comment.end_node["created_at"]
            }
            comments_list.append(comment_data)
        return jsonify(comments_list)
    return jsonify({"message": "Post not found"}), 404

@commentaires_bp.route('/posts/<int:post_id>/comments', methods=['POST'])
def create_comment(post_id):
    data = request.get_json()
    content = data['content']
    user_id = data['user_id']
    post = node_exists(graph, post_id, NodeEnum.Post)
    user = node_exists(graph, user_id, NodeEnum.Utilisateur)
    if post and user:
        comment = Commentaire(content, graph)
        comment_node = comment.create_comment()
        create_relation(user, comment_node, RelationEnum.Created, graph)
        create_relation(post, comment_node, RelationEnum.HasComment, graph)
        return jsonify({"message": "Comment created", "comment_id": comment_node.identity}), 201
    return jsonify({"message": "Post or user not found"}), 404

@commentaires_bp.route('/posts/<int:post_id>/comments/<int:comment_id>', methods=['DELETE'])
def delete_post_comment(post_id, comment_id):
    post = node_exists(graph, post_id, NodeEnum.Post)
    comment = node_exists(graph, comment_id, NodeEnum.Commentaire)
    if post and comment:
        delete_all_relations(None, comment, graph)
        graph.delete(comment)
        return jsonify({"message": "Comment deleted"}), 200
    return jsonify({"message": "Post or comment not found"}), 404

@commentaires_bp.route('/comments', methods=['GET'])
def get_all_comments():
    comments = graph.nodes.match(NodeEnum.Commentaire.value).all()
    comments_list = []
    for comment in comments:
        comment_data = {
            "id": comment.identity,
            "content": comment["content"],
            "created_at": comment["created_at"]
        }
        comments_list.append(comment_data)
    return jsonify(comments_list)

@commentaires_bp.route('/comments/<int:comment_id>', methods=['GET'])
def get_comment(comment_id):
    comment = node_exists(graph, comment_id, NodeEnum.Commentaire)
    if comment:
        comment_data = {
            "id": comment.identity,
            "content": comment["content"],
            "created_at": comment["created_at"]
        }
        return jsonify(comment_data)
    return jsonify({"message": "Comment not found"}), 404

@commentaires_bp.route('/comments/<int:comment_id>', methods=['PUT'])
def update_comment(comment_id):
    data = request.get_json()
    content = data['content']
    comment = node_exists(graph, comment_id, NodeEnum.Commentaire)
    if comment:
        comment["content"] = content
        graph.push(comment)
        return jsonify({"message": "Comment updated successfully"}), 200
    return jsonify({"message": "Comment not found"}), 404

@commentaires_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    comment = node_exists(graph, comment_id, NodeEnum.Commentaire)
    if comment:
        delete_all_relations(None, comment, graph)
        graph.delete(comment)
        return jsonify({"message": "Comment deleted successfully"}), 200
    return jsonify({"message": "Comment not found"}), 404

@commentaires_bp.route('/comments/<int:comment_id>/like', methods=['POST'])
def like_comment(comment_id):
    data = request.get_json()
    user_id = data['user_id']
    comment = node_exists(graph, comment_id, NodeEnum.Commentaire)
    user = node_exists(graph, user_id, NodeEnum.Utilisateur)
    if comment and user:
        create_relation(user, comment, RelationEnum.Likes, graph)
        return jsonify({"message": "Comment liked successfully"}), 201
    return jsonify({"message": "Comment or user not found"}), 404  

@commentaires_bp.route('/comments/<int:comment_id>/like', methods=['DELETE'])
def unlike_comment(comment_id):
    data = request.get_json()
    user_id = data['user_id']
    comment = node_exists(graph, comment_id, NodeEnum.Commentaire)
    user = node_exists(graph, user_id, NodeEnum.Utilisateur)
    if comment and user:
        like_relation = delete_relation(user, comment, RelationEnum.Likes, graph)
        if like_relation is not None:
            return jsonify({"message": "Comment unliked successfully"}), 200
        return jsonify({"message": "Like relation not found"}), 404
    return jsonify({"message": "Comment or user not found"}), 404     