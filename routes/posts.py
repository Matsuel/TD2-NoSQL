from flask import Blueprint, jsonify, request
from models.post import Post
from database.config import connect_to_neo4j
from database.functions import create_relationship
from models.utilisateur import Utilisateur

posts_bp = Blueprint('posts', __name__)

@posts_bp.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.get_all()
    return jsonify(posts)


@posts_bp.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.get_by_id(post_id)
    if post:
        return jsonify(post)
    return jsonify({"message": "Post not found"}), 404

@posts_bp.route('/users/<int:user_id>/posts', methods=['GET'])
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

@posts_bp.route('/users/<int:user_id>/posts', methods=['POST'])
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

@posts_bp.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    data = request.get_json()
    post = Post.get_by_id(post_id)
    if post:
        Post.update_post(post_id, title=data['title'], content=data['content'])
        return jsonify({"message": "Post updated successfully"})
    return jsonify({"message": "Post not found"}), 404

@posts_bp.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = Post.get_by_id(post_id)
    if post:
        Post.delete_post(post_id)
        return jsonify({"message": "Post deleted successfully"})
    return jsonify({"message": "Post not found"}), 404

@posts_bp.route('/posts/<int:post_id>/like', methods=['POST'])
def like_post(post_id):
    data = request.get_json()
    user_id = data['user_id']
    post = Post.get_by_id(post_id)
    user = Utilisateur.get_by_id(user_id)
    if post and user:
        Post.like_post(post_id, user_id)
        return jsonify({"message": "Post liked successfully"})
    return jsonify({"message": "Post or User not found"}), 404

@posts_bp.route('/posts/<int:post_id>/like', methods=['DELETE'])
def unlike_post(post_id):
    data = request.get_json()
    user_id = data['user_id']
    post = Post.get_by_id(post_id)
    user = Utilisateur.get_by_id(user_id)
    if post and user:
        Post.unlike_post(post_id, user_id)
        return jsonify({"message": "Post unliked successfully"})
    return jsonify({"message": "Post or User not found"}), 404