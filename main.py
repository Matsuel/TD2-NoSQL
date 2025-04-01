from flask import Flask, jsonify, request
from py2neo import Relationship, Node
from models.utilisateur import Utilisateur
from models.post import Post
from database.config import connect_to_neo4j
from database.functions import create_relationship

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

@app.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.get_all()
    return jsonify(posts)

@app.route('/users/<int:user_id>/posts', methods=['POST'])
def create_post(user_id):
    data = request.get_json()
    new_post = Post(title=data['title'], content=data['content'])
    post_node = new_post.save()
    user = Utilisateur.get_by_id_as_node(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    # Assuming you want to create a relationship between the post and the user
    create_relationship(user, post_node, "CREATED")
    return jsonify({"message": "Post created successfully"}), 201

@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.get_by_id(post_id)
    if post:
        return jsonify(post)
    return jsonify({"message": "Post not found"}), 404

@app.route('/users/<int:user_id>/posts', methods=['GET'])
def get_user_posts(user_id):
    # Récupérer l'utilisateur en tant que Node
    user_node = Utilisateur.get_by_id_as_node(user_id)
    if not user_node:
        return jsonify({"message": "User not found"}), 404

    # Requête pour récupérer les posts liés à l'utilisateur via la relation CREATED
    graph = connect_to_neo4j()
    query = """
    MATCH (u:Utilisateur)-[:CREATED]->(p:Post)
    WHERE id(u) = $user_id
    RETURN id(p) AS id, p.title AS title, p.content AS content, p.created_at AS created_at
    """
    posts = graph.run(query, user_id=user_id).data()

    return jsonify(posts)

@app.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    data = request.get_json()
    post = Post.get_by_id(post_id)
    if post:
        Post.update_post(post_id, title=data['title'], content=data['content'])
        return jsonify({"message": "Post updated successfully"})
    return jsonify({"message": "Post not found"}), 404

@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = Post.get_by_id(post_id)
    if post:
        Post.delete_post(post_id)
        return jsonify({"message": "Post deleted successfully"})
    return jsonify({"message": "Post not found"}), 404

@app.route('/posts/<int:post_id>/like', methods=['POST'])
def like_post(post_id):
    data = request.get_json()
    user_id = data['user_id']
    post = Post.get_by_id(post_id)
    user = Utilisateur.get_by_id(user_id)
    if post and user:
        Post.like_post(post_id, user_id)
        return jsonify({"message": "Post liked successfully"})
    return jsonify({"message": "Post or User not found"}), 404

@app.route('/posts/<int:post_id>/like', methods=['DELETE'])
def unlike_post(post_id):
    data = request.get_json()
    user_id = data['user_id']
    post = Post.get_by_id(post_id)
    user = Utilisateur.get_by_id(user_id)
    if post and user:
        Post.unlike_post(post_id, user_id)
        return jsonify({"message": "Post unliked successfully"})
    return jsonify({"message": "Post or User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)