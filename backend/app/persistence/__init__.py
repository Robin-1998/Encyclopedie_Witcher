"""
Ce module gère la persistance des données dans l’application.
Les repositories encapsulent la logique CRUD (Create, Read, Update, Delete)
pour chaque entité, en respectant le principe de séparation des responsabilités :
    - La couche "repository" s’occupe des accès à la base de données.
    - La couche "service" (ou logique métier) utilise ces repositories pour manipuler les entités.

"""
from .repository import Repository, SQLAlchemyRepository
from .user_repository import UserRepository

__all__ = [
    'Repository',         # Interface abstraite commune à tous les dépôts
    'SQLAlchemyRepository',# Implémentation générique utilisant SQLAlchemy
    'UserRepository',     # Requêtes spécifiques aux utilisateurs
]
