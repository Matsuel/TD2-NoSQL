# TP Neo4j

## Introduction

Ce projet est une application web basée sur Flask et Neo4j pour gérer des utilisateurs, des posts, des commentaires et leurs relations. Il utilise une architecture modulaire avec des routes, des modèles, des utilitaires et une configuration centralisée.

## Prérequis

- Python 3.10 ou supérieur
- Neo4j (via Docker ou installation locale)
- `pip` pour gérer les dépendances Python

## Installation

### 1. Clonez ce dépôt :
```bash
git clone https://github.com/Matsuel/TD2-NoSQL.git
cd TD2-NoSQL
python -m venv venv
source venv/bin/activate 
pip install -r requirements.txt
```
### 2. Démarrez le serveur Neo4j (si vous utilisez Docker) :

```bash
docker compose up -d --build
```

### 3. Démarrez l'application Flask :

```bash
python main.py
```

### 4. Testez l'application :
Utiliser la collection Postman pour tester les différentes routes de l'API
[Postman Collection](./TD2.postman_collection.json)

### 5. Routes disponibles :
#### Utilisateurs:
- Créer un utilisateur : POST /users
- Récupérer tous les utilisateurs : GET /users
- Récupérer un utilisateur par ID : GET /users/<user_id>
- Mettre à jour un utilisateur : PUT /users/<user_id>
- Supprimer un utilisateur : DELETE /users/<user_id>
- Gérer les amis :
    - Ajouter un ami : POST /users/<user_id>/friends
    - Supprimer un ami : DELETE /users/<user_id>/friends/<friend_id>
    - Vérifier une amitié : GET /users/<user_id>/friends/<friend_id>
    - Récupérer les amis communs : GET /users/<user_id>/mutual-friends/<other_id>

#### Posts:
- Créer un post : POST /users/<user_id>/posts
- Récupérer tous les posts : GET /posts
- Récupérer un post par ID : GET /posts/<post_id>
- Mettre à jour un post : PUT /posts/<post_id>
- Supprimer un post : DELETE /posts/<post_id>
- Gérer les likes :
    - Liker un post : POST /posts/<post_id>/like
    - Retirer un like : DELETE /posts/<post_id>/like

#### Commentaires:
- Créer un commentaire : POST /posts/<post_id>/comments
- Récupérer tous les commentaires d'un post : GET /posts/<post_id>/comments
- Récupérer un commentaire par ID : GET /comments/<comment_id>
- Mettre à jour un commentaire : PUT /comments/<comment_id>
- Supprimer un commentaire : DELETE /comments/<comment_id>
- Gérer les likes :
    - Liker un commentaire : POST /comments/<comment_id>/like
    - Retirer un like : DELETE /comments/<comment_id>/like

### 5. Accédez à l'interface utilisateur :
Ouvrez votre navigateur et accédez à `http://localhost:7474` pour accéder à l'interface de Neo4j Browser.

## Structure du projet

```
.
├── constantes/
│   ├── [node.py]         # Définitions des types de nœuds
│   ├── [relation.py]    # Définitions des types de relations
├── database/
│   ├── [config.py]      # Configuration de la connexion à Neo4j
├── models/
│   ├── [utilisateur.py]   # Modèle pour les utilisateurs
│   ├── [post.py]         # Modèle pour les posts
│   ├── [commentaire.py]  # Modèle pour les commentaires
├── routes/
│   ├── [users.py]      # Routes pour les utilisateurs
│   ├── [posts.py]      # Routes pour les posts
│   ├── [commentaires.py]  # Routes pour les commentaires
├── utils/
│   ├── [node.py]         # Fonctions utilitaires pour les nœuds
│   ├── [relations.py]     # Fonctions utilitaires pour les relations
│   ├── [format.py]        # Fonctions de formatage des données
├── [main.py]           # Point d'entrée de l'application Flask
├── [docker-compose.yml]   # Configuration Docker pour Neo4j
└── venv/                # Environnement virtuel Python
```