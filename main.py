from flask import Flask, jsonify, request
from models.utilisateur import Utilisateur
app = Flask(__name__)


@app.route('/users', methods=['GET'])
def get_users():
    utilisateurs = Utilisateur.get_all()
    return jsonify(utilisateurs)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = Utilisateur.get_by_id(user_id)
    if user:
        return jsonify(user)
    return jsonify({"message": "User not found"}), 404

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = Utilisateur(name=data['name'], email=data['email'])
    new_user.save()
    return jsonify({"message": "User created successfully"}), 201

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = Utilisateur.get_by_id(user_id)
    if user:
        Utilisateur.delete_user(user_id)
        return jsonify({"message": "User deleted successfully"})
    return jsonify({"message": "User not found"}), 404

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = Utilisateur.get_by_id(user_id)
    if user:
        Utilisateur.update_user(user_id, name=data['name'], email=data['email'])
        return jsonify({"message": "User updated successfully"})
    return jsonify({"message": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)