"""
Classe modèle d'un user
"""

from backend.app import db, bcrypt
from backend.app.models.basemodel import BaseModel
from email_validator import validate_email, EmailNotValidError
from sqlalchemy.orm import validates
import re

class User(BaseModel):
    """
    Modèle réprésentant un utilisateur de l'application et hérite de base model
    """
    __tablename__ = "users"

    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # ---------------------
    # Validation des champs
    # ---------------------

    @validates('name')
    def validate_name(self, key, name):
        """Gère les conditions de validation du nom/pseudo"""
        if not isinstance(name, str):
            raise ValueError(f"{key} doit être une chaîne de caractères.")

        name = name.strip()

        if not name:
            raise ValueError(f"{key} ne peut pas être vide, merci de compléter.")
        
        if not (1 <= len(name) <= 50):
            raise ValueError(f"{key} doit contenir entre 1 et 50 caractères.")

        if not re.fullmatch(r"[a-zA-ZÀ-ÿ\s-]+", name):
            raise ValueError(
                f"{key} ne doit contenir que des lettres ou des tirets.")

        return name.title() # capitalisation (majuscules) automatique

    @validates('email')
    def validation_email(self, key, email):
        """
        Méthode de validation qui vérifie une bonne conformité
        d'adresse e-mail en utilisant la bibliothèque email-Validator
        """
        if not email:
            raise ValueError("L'email ne peut pas être vide, merci de renseigner votre adresse email")
        try: # on appelle la bibliothèque validate_email et on la valide
            valid = validate_email(email)
            return valid.normalized
        except EmailNotValidError as email_error:
            raise ValueError(f"Erreur, email invalide : {email_error}")

    def hash_password(self, password):
        """
        Pour le haching, utilisation de bcrypt car plus de contrôle de sécurité sur les mots de passe
        Hache le mot de passe avant de le stocker
        """
        if not password:
            raise ValueError("Le mot de passe ne peut être vide, merci de renseigner un mot de passe")
        if len(password) < 8:
            raise ValueError("Le mot de passe doit contenir au moins 8 caractères")
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """
        Vérifie si le mot de passe fourni correspond au mot de passe haché
        """
        if not password:
            return False
        return bcrypt.check_password_hash(self.password, password)

    def update_password(self, new_password):
        """
        Met à jour le mot de passe d'un user
        Rapelle `hash_password` pour appliquer les validations et le hachage
        """
        self.hash_password(new_password)
    
    @validates('is_admin')
    def validate_is_admin(self, key, is_admin):
        """
        Méthode de validation qui vérifie si l'utilisateur est un admin
        ou non. Par défaut is_admin = False
        """
    
    def to_dict(self):
        data = super().to_dict()
        data.update ({
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "is_admin": self.is_admin
        })
        return data
