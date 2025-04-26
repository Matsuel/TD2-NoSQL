from flask import Blueprint, jsonify, request
from models.utilisateur import Utilisateur
from constantes.node import NodeEnum
from constantes.relation import RelationEnum
from py2neo import Relationship
from database.config import graph

users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['GET'])
def get_users():
    users = graph.nodes.match(NodeEnum.Utilisateur.value).all()
    users_list = []
    for user in users:
        user_data = {
            "id": user.identity,
            "name": user["name"],
            "email": user["email"],
            "created_at": user["created_at"]
        }
        users_list.append(user_data)
    return jsonify(users_list)

@users_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = Utilisateur(graph, name=data['name'], email=data['email'])
    user.create_user()
    return jsonify({"message": "User created successfully"}), 201

@users_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = graph.nodes.get(user_id)
    if user:
        user_data = {
            "id": user.identity,
            "name": user["name"],
            "email": user["email"],
            "created_at": user["created_at"]
        }
        return jsonify(user_data)
    return jsonify({"message": "User not found"}), 404

@users_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = graph.nodes.get(user_id)
    if user:
        user["name"] = data['name']
        user["email"] = data['email']
        graph.push(user)
        return jsonify({"message": "User updated successfully"})
    return jsonify({"message": "User not found"}), 404

@users_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = graph.nodes.get(user_id)
    if user:
        graph.delete(user)
        return jsonify({"message": "User deleted successfully"})
    return jsonify({"message": "User not found"}), 404

@users_bp.route('/users/<int:user_id>/friends', methods=['GET'])
def get_friends(user_id):
    user = graph.nodes.get(user_id)
    if user:
        friends = graph.match((user,), r_type=RelationEnum.Friend.value).all()
        friends_list = []
        for friend in friends:
            friend_data = {
                "id": friend.end_node.identity,
                "name": friend.end_node["name"],
                "email": friend.end_node["email"],
                "created_at": friend.end_node["created_at"]
            }
            friends_list.append(friend_data)
        return jsonify(friends_list)
    return jsonify({"message": "User not found"}), 404


@users_bp.route('/users/<int:user_id>/friends', methods=['POST'])
def add_friend(user_id):
    data = request.get_json()
    friend_id = data['friend_id']
    user = graph.nodes.get(user_id)
    friend = graph.nodes.get(friend_id)
    if user and friend:
        friend_relation = Relationship(user, RelationEnum.Friend.value, friend)
        graph.create(friend_relation)
        return jsonify({"message": "Friend added successfully"}), 201
    return jsonify({"message": "User or Friend not found"}), 404

@users_bp.route('/users/<int:user_id>/friends/<int:friendId>', methods=['DELETE'])
def delete_friend(user_id, friendId):
    user = graph.nodes.get(user_id)
    friend = graph.nodes.get(friendId)
    if user and friend:
        friend_relation = graph.match_one((user, friend), r_type=RelationEnum.Friend.value)
        if friend_relation is not None:
            graph.separate(friend_relation)
            return jsonify({"message": "Friend deleted successfully"})
        return jsonify({"message": "Friend relation not found"}), 404
    return jsonify({"message": "User or Friend not found"}), 404

@users_bp.route('/users/<int:user_id>/friends/<int:friendId>', methods=['GET'])
def is_friend(user_id, friendId):
    user = graph.nodes.get(user_id)
    friend = graph.nodes.get(friendId)
    if user and friend:
        friend_relation1 = graph.match_one((user, friend), r_type=RelationEnum.Friend.value)
        friend_relation2 = graph.match_one((friend, user), r_type=RelationEnum.Friend.value)
        if (friend_relation1 is not None) and (friend_relation2 is not None):
            return jsonify({"is_friend": True})
        return jsonify({"is_friend": False})
    return jsonify({"message": "User or Friend not found"}), 404

@users_bp.route('/users/<int:user_id>/mutual-friends/<int:other_id>', methods=['GET'])
def get_mutual_friends(user_id, other_id):
    # TODO: Réparer
    user = graph.nodes.get(user_id)
    other = graph.nodes.get(other_id)
    if user and other:
        user_friends = set(friend.end_node for friend in graph.match((user,), r_type=RelationEnum.Friend.value))
        other_friends = set(friend.end_node for friend in graph.match((other,), r_type=RelationEnum.Friend.value))
        mutual_friends = user_friends & other_friends
        return jsonify([{"id": friend.identity, "name": friend["name"]} for friend in mutual_friends])
    return jsonify({"error": "User or other user not found"}), 404
