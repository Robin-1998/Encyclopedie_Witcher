import os
from dotenv import load_dotenv
from datetime import timedelta

# permet de chager le .env
load_dotenv()

class Config:
    """ Configuration de base pour environnement flask"""
    # Clé secrète Flask (utile pour les sessions utilisateurs)
    SECRET_KEY = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError("La variable d'environnement SECRET_KEY doit être définie !")

    # Désactive le suvi des modification des modèles qui
    # consomment trop de mémoire
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # UTF-8 pour JSON (évite les caractères bizarres)
    JSON_AS_ASCII = False

    # durée de validité du token mis à une journée
    # ⚠️ à modifier plus tard pour un token qui se renouvelle
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)

class DevelopmentConfig(Config):
    """Configuration pour le développement local."""

    DEBUG = True # affiche les erreurs détaillés
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") # la donnée à utiliser
    SQLALCHEMY_ECHO = True  # afficher les requêtes SQL pour le debug

class ProductionConfig(Config):
    """ Configuration pour la production"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") # la donnée à utiliser

# Dictionnaire de configuration global pour Flask
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
