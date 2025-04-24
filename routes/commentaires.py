from flask import Blueprint, request, jsonify
from models.commentaire import Commentaire

commentaires_bp = Blueprint('commentaires', __name__)



