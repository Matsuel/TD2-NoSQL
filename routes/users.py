from flask import Blueprint, jsonify, request
from models.utilisateur import Utilisateur
from constantes.node import NodeEnum
from constantes.relation import RelationEnum
from database.config import graph
from utils.node import node_exists, get_all_nodes
from utils.relations import create_relation, delete_relation, get_all_relations, get_one_relation
from utils.format import format_user

users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['GET'])
def get_users():
    users = get_all_nodes(graph, NodeEnum.Utilisateur)
    users_list = []
    for user in users:
        users_list.append(format_user(user))
    return jsonify(users_list)

@users_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = Utilisateur(graph, name=data['name'], email=data['email'])
    user.create_user()
    return jsonify({"message": "User created successfully"}), 201

@users_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = node_exists(graph, user_id, NodeEnum.Utilisateur)
    if user:
        return jsonify(format_user(user))
    return jsonify({"message": "User not found"}), 404

@users_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = node_exists(graph, user_id, NodeEnum.Utilisateur)
    if user:
        user["name"] = data['name']
        user["email"] = data['email']
        graph.push(user)
        return jsonify({"message": "User updated successfully"})
    return jsonify({"message": "User not found"}), 404

@users_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = node_exists(graph, user_id, NodeEnum.Utilisateur)
    if user:
        graph.delete(user)
        return jsonify({"message": "User deleted successfully"})
    return jsonify({"message": "User not found"}), 404

@users_bp.route('/users/<int:user_id>/friends', methods=['GET'])
def get_friends(user_id):
    user = node_exists(graph, user_id, NodeEnum.Utilisateur)
    if user:
        friends = get_all_relations(user, None, RelationEnum.Friend, graph)
        friends_list = []
        for friend in friends:
            friends_list.append(format_user(friend.end_node))
        return jsonify(friends_list)
    return jsonify({"message": "User not found"}), 404


@users_bp.route('/users/<int:user_id>/friends', methods=['POST'])
def add_friend(user_id):
    data = request.get_json()
    friend_id = data['friend_id']
    user = node_exists(graph, user_id, NodeEnum.Utilisateur)
    friend = node_exists(graph, friend_id, NodeEnum.Utilisateur)
    if user and friend:
        create_relation(user, friend, RelationEnum.Friend, graph)
        return jsonify({"message": "Friend added successfully"}), 201
    return jsonify({"message": "User or Friend not found"}), 404

@users_bp.route('/users/<int:user_id>/friends/<int:friendId>', methods=['DELETE'])
def delete_friend(user_id, friendId):
    user = node_exists(graph, user_id, NodeEnum.Utilisateur)
    friend = node_exists(graph, friendId, NodeEnum.Utilisateur)
    if user and friend:
        friend_relation = delete_relation(user, friend, RelationEnum.Friend, graph)
        if friend_relation is not None:
            return jsonify({"message": "Friend deleted successfully"})
        return jsonify({"message": "Friend relation not found"}), 404
    return jsonify({"message": "User or Friend not found"}), 404

@users_bp.route('/users/<int:user_id>/friends/<int:friendId>', methods=['GET'])
def is_friend(user_id, friendId):
    user = node_exists(graph, user_id, NodeEnum.Utilisateur)
    friend = node_exists(graph, friendId, NodeEnum.Utilisateur)
    if user and friend:
        friend_relation1 = get_one_relation(user, friend, RelationEnum.Friend, graph)
        friend_relation2 = get_one_relation(friend, user, RelationEnum.Friend, graph)
        return jsonify({"is_friend": (friend_relation1 is not None) and (friend_relation2 is not None)})
    return jsonify({"message": "User or Friend not found"}), 404

@users_bp.route('/users/<int:user_id>/mutual-friends/<int:other_id>', methods=['GET'])
def get_mutual_friends(user_id, other_id):
    user = node_exists(graph, user_id, NodeEnum.Utilisateur)
    other = node_exists(graph, other_id, NodeEnum.Utilisateur)
    if user and other:
        user_friends = set(friend.end_node for friend in get_all_relations(user, None, RelationEnum.Friend, graph))
        other_friends = set(friend.end_node for friend in get_all_relations(other, None, RelationEnum.Friend, graph))
        mutual_friends = user_friends & other_friends
        return jsonify([format_user(friend) for friend in mutual_friends])
    return jsonify({"error": "User or other user not found"}), 404
