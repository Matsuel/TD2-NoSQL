from flask import Blueprint, jsonify, request
from models.post import Post
from constantes.node import NodeEnum
from constantes.relation import RelationEnum
from database.config import graph
from utils.relations import create_relation, delete_relation, get_all_relations
from utils.node import node_exists, get_all_nodes
from utils.format import format_post

posts_bp = Blueprint('posts', __name__)

@posts_bp.route('/posts', methods=['GET'])
def get_posts():
    posts = get_all_nodes(graph, NodeEnum.Post)
    posts_list = []
    for post in posts:
        posts_list.append(format_post(post))
    return jsonify(posts_list)


@posts_bp.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = node_exists(graph, post_id, NodeEnum.Post)
    if post:
        return jsonify(format_post(post))
    return jsonify({"message": "Post not found"}), 404

@posts_bp.route('/users/<int:user_id>/posts', methods=['GET'])
def get_user_posts(user_id):
    user = node_exists(graph, user_id, NodeEnum.Utilisateur)
    if user:
        posts = get_all_relations(user, None, RelationEnum.Created, graph)
        posts_list = []
        for post in posts:
            posts_list.append(format_post(post.end_node))
        return jsonify(posts_list)
    return jsonify({"message": "User not found"}), 404

@posts_bp.route('/users/<int:user_id>/posts', methods=['POST'])
def create_post(user_id):
    data = request.get_json()
    title = data['title']
    content = data['content']
    user = node_exists(graph, user_id, NodeEnum.Utilisateur)
    if user:
        post = Post(title=title, content=content, graph=graph)
        post_node = post.create_post()
        create_relation(user, post_node, RelationEnum.Created, graph)
        return jsonify({"message": "Post created successfully"}), 201
    return jsonify({"message": "User not found"}), 404

@posts_bp.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    data = request.get_json()
    title = data['title']
    content = data['content']
    post = node_exists(graph, post_id, NodeEnum.Post)
    if post:
        post["title"] = title
        post["content"] = content
        graph.push(post)
        return jsonify({"message": "Post updated successfully"})
    return jsonify({"message": "Post not found"}), 404

@posts_bp.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = node_exists(graph, post_id, NodeEnum.Post)
    if post:
        graph.delete(post)
        return jsonify({"message": "Post deleted successfully"})
    return jsonify({"message": "Post not found"}), 404

@posts_bp.route('/posts/<int:post_id>/like', methods=['POST'])
def like_post(post_id):
    data = request.get_json()
    user_id = data['user_id']
    post = node_exists(graph, post_id, NodeEnum.Post)
    user = node_exists(graph, user_id, NodeEnum.Utilisateur)
    if post and user:
        create_relation(user, post, RelationEnum.Likes, graph)
        return jsonify({"message": "Post liked successfully"}), 201
    return jsonify({"message": "Post or User not found"}), 404

@posts_bp.route('/posts/<int:post_id>/like', methods=['DELETE'])
def unlike_post(post_id):
    data = request.get_json()
    user_id = data['user_id']
    post = node_exists(graph, post_id, NodeEnum.Post)
    user = node_exists(graph, user_id, NodeEnum.Utilisateur)
    if post and user:
        if delete_relation(user, post, RelationEnum.Likes, graph):
            return jsonify({"message": "Post unliked successfully"}), 200
        return jsonify({"message": "Like relation not found"}), 404
    return jsonify({"message": "Post or User not found"}), 404