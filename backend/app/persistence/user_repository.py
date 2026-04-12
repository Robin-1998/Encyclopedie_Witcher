"""
Ce module définit le `UserRepository`, responsable de la gestion
des entités `User` (utilisateurs).

Il hérite de `SQLAlchemyRepository`, qui fournit les opérations CRUD de base,
et ajoute des méthodes spécifiques pour :
    - Récupérer un utilisateur par email,
    - Vérifier l'existence d'un email,
    - Récupérer tous les administrateurs,
    - Récupérer tous les utilisateurs réguliers.
"""
from backend.app.models.user import User
from backend.app.persistence.repository import SQLAlchemyRepository

class UserRepository(SQLAlchemyRepository):
    """
    Repository spécifique pour les utilisateurs.
    
    Fournit des méthodes de récupération ciblées pour les entités User :
    - par email,
    - par type d'utilisateur (admin ou régulier).
    """
    def __init__(self):
        """ Initialise le repository avec le modèle `User`."""
        super().__init__(User)

    def get_user_by_email(self, email):
        """ Récupère un utilisateur par son adresse email."""
        return self.model.query.filter_by(email=email).first()
    
    def email_exists(self, email):
        """
        Vérifie si un email existe déjà dans la base de données.
        """
        return self.get_user_by_email(email) is not None

    def get_all_admins(self):
        """
        Récupère tous les utilisateurs administrateurs.
        
        Returns:
            list: Liste des utilisateurs avec is_admin=True
        """
        return self.model.query.filter_by(is_admin=True).all()

    def get_all_regular_users(self):
        """
        Récupère tous les utilisateurs non-administrateurs.
        
        Returns:
            list: Liste des utilisateurs avec is_admin=False
        """
        return self.model.query.filter_by(is_admin=False).all()
