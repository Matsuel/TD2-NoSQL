from flask import Blueprint, jsonify, request
from models.utilisateur import Utilisateur


users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['GET'])
def get_users():
    utilisateurs = Utilisateur.get_all()
    return jsonify(utilisateurs)

@users_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = Utilisateur(name=data['name'], email=data['email'])
    new_user.save()
    return jsonify({"message": "User created successfully"}), 201

@users_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = Utilisateur.get_by_id(user_id)
    if user:
        return jsonify(user)
    return jsonify({"message": "User not found"}), 404

@users_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = Utilisateur.get_by_id(user_id)
    if user:
        Utilisateur.update_user(user_id, name=data['name'], email=data['email'])
        return jsonify({"message": "User updated successfully"})
    return jsonify({"message": "User not found"}), 404

@users_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = Utilisateur.get_by_id(user_id)
    if user:
        Utilisateur.delete_user(user_id)
        return jsonify({"message": "User deleted successfully"})
    return jsonify({"message": "User not found"}), 404

@users_bp.route('/users/<int:user_id>/friends', methods=['GET'])
def get_friends(user_id):
    friends = Utilisateur.get_friends(user_id)
    return jsonify(friends)

@users_bp.route('/users/<int:user_id>/friends', methods=['POST'])
def add_friend(user_id):
    data = request.get_json()
    friend_id = data['friend_id']
    Utilisateur.add_friend(user_id, friend_id)
    return jsonify({"message": "Friend added successfully"})

@users_bp.route('/users/<int:user_id>/friends/<int:friendId>', methods=['DELETE'])
def delete_friend(user_id, friendId):
    Utilisateur.delete_friend(user_id, friendId)
    return jsonify({"message": "Friend deleted successfully"})

@users_bp.route('/users/<int:user_id>/friends/<int:friendId>', methods=['GET'])
def is_friend(user_id, friendId):
    is_friend1 = Utilisateur.is_friend(user_id, friendId)
    is_friend2 = Utilisateur.is_friend(friendId, user_id)
    return jsonify({"is_friend": is_friend1 and is_friend2})

@users_bp.route('/users/<int:user_id>/mutual-friends/<int:otherId>', methods=['GET'])
def get_mutual_friends(user_id, otherId):
    mutual_friends = Utilisateur.get_mutual_friends(user_id, otherId)
    return jsonify(mutual_friends)
