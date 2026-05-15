"""
Service d'authentification.
Gère l'inscription, la connexion et la récupération de l'utilisateur courant.
Séparé de la Facade car l'auth a ses propres responsabilités :
hashage des mots de passe, génération et vérification des tokens JWT.
"""
from flask_jwt_extended import create_access_token, create_refresh_token
from backend.app import bcrypt
from backend.app.models.user import User
from backend.app.persistence.user_repository import UserRepository


class UserService:

    def __init__(self):
        self.user_repo = UserRepository()

    # -------------------------------------------------------------------------
    # Register
    # -------------------------------------------------------------------------

    def register(self, name: str, email: str, password: str) -> dict:
        """
        Inscrit un nouvel utilisateur.
        Raises:
            ValueError: si l'email est déjà utilisé ou les champs invalides.
        """
        if not name or not email or not password:
            raise ValueError("Tous les champs sont requis.")

        if self.user_repo.email_exists(email):
            raise ValueError("Cet email est déjà utilisé.")

        if len(password) < 8:
            raise ValueError("Le mot de passe doit contenir au moins 8 caractères.")

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        user = User(
            name=name,
            email=email,
            password=hashed_password
        )
        self.user_repo.add(user)
        return user.to_dict()

    # -------------------------------------------------------------------------
    # Login
    # -------------------------------------------------------------------------

    def login(self, email: str, password: str) -> dict:
        """
        Authentifie un utilisateur et retourne les tokens JWT.
        Raises:
            ValueError: si les identifiants sont incorrects.
        """
        if not email or not password:
            raise ValueError("Email et mot de passe requis.")

        user = self.user_repo.get_user_by_email(email)

        if not user or not bcrypt.check_password_hash(user.password, password):
            raise ValueError("Email ou mot de passe incorrect.")

        # On stocke l'id dans le token (identity) + infos utiles en claims
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={
                'is_admin': user.is_admin,
                'name': user.name
            }
        )
        refresh_token = create_refresh_token(identity=str(user.id))

        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        }

    # -------------------------------------------------------------------------
    # Get current user
    # -------------------------------------------------------------------------

    def get_current_user(self, user_id: int) -> dict | None:
        """Retourne les infos de l'utilisateur connecté depuis son id (extrait du JWT)."""
        user = self.user_repo.get(user_id)
        if not user:
            return None
        return user.to_dict()

    # -------------------------------------------------------------------------
    # Refresh token
    # -------------------------------------------------------------------------

    def refresh_token(self, user_id: int) -> dict:
        """Génère un nouvel access token depuis un refresh token valide."""
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("Utilisateur introuvable.")

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={
                'is_admin': user.is_admin,
                'name': user.name
            }
        )
        return {'access_token': access_token}
