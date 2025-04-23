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

# GET /users/:id/friends : Récupérer la liste des amis d'un utilisateur
# POST /users/:id/friends : Ajouter un ami (ID de l'ami dans le body)
# DELETE /users/:id/friends/:friendId : Supprimer un ami
# GET /users/:id/friends/:friendId : Vérifier si deux utilisateurs sont amis
# GET /users/:id/mutual-friends/:otherId : Récupérer les amis en commun