from flask import Flask
from routes.users import users_bp
from routes.posts import posts_bp
from routes.commentaires import commentaires_bp

app = Flask(__name__)

app.register_blueprint(users_bp)
app.register_blueprint(posts_bp)
app.register_blueprint(commentaires_bp)

# Ajouter préfix sur les routes
# Factoriser le code des routes

if __name__ == '__main__':
    app.run(debug=True)