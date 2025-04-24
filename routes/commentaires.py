from flask import Blueprint, request, jsonify
from models.commentaire import Commentaire

commentaires_bp = Blueprint('commentaires', __name__)

@commentaires_bp.route('/posts/<int:post_id>/comments', methods=['POST'])
def create_comment(post_id):
    data = request.json
    content = data.get('content')
    user_id = data.get('user_id')
    comment = Commentaire(content, post_id)
    comment.save()
    comment.link_to_post(post_id)
    comment.link_to_user(user_id)
    return jsonify({"message": "Commentaire créé avec succès"}), 201


