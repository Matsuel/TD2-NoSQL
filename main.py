from flask import Flask
from routes.users import users_bp
from routes.posts import posts_bp
from routes.commentaires import commentaires_bp
from py2neo import Graph

app = Flask(__name__)

graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))

app.register_blueprint(users_bp)
app.register_blueprint(posts_bp)
app.register_blueprint(commentaires_bp)

# Ajouter préfix sur les routes
# Factoriser le code des routes

# Commentaires
# GET /posts/:id/comments : Récupérer les commentaires d'un post
# POST /posts/:id/comments : Ajouter un commentaire
# Lors de la création d'un commentaire, deux relations doivent être établies :
# Une relation CREATED entre l'utilisateur et le commentaire
# Une relation HAS_COMMENT entre le post et le commentaire
# DELETE /posts/:postId/comments/:commentId : Supprimer un commentaire
# GET /comments : Récupérer tous les commentaires
# GET /comments/:id : Récupérer un commentaire par son ID
# PUT /comments/:id : Mettre à jour un commentaire
# DELETE /comments/:id : Supprimer un commentaire
# POST /comments/:id/like : Ajouter un like à un commentaire (créer la relation LIKES entre un utilisateur et le
# commentaire)
# DELETE /comments/:id/like : Retirer un like d'un commentaire (supprimer la relation LIKES )


if __name__ == '__main__':
    app.run(debug=True)