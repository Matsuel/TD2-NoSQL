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
│   ├── [functions.py]    # Fonctions utilitaires pour Neo4j
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