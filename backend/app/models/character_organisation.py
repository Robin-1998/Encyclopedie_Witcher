"""
Classe Modèle représentation le type d'organisaion d'un personnage
"""

from backend.app import db
from backend.app.models.basemodel import BaseModel
from sqlalchemy.orm import validates

class CharacterOrganisation(BaseModel):
    """
    Class characterOrganisation lié un character
    """
    __tablename__ = "character_organisations"

    character_id = db.Column(db.BigInteger, db.ForeignKey('characters.id', ondelete='CASCADE'), nullable=False)
    organisation_id = db.Column(db.BigInteger, db.ForeignKey('organisations.id', ondelete='CASCADE'), nullable=False)
    role = db.Column(db.String(50))

    # ------------------------
    # Relations ORM
    # ------------------------

    character = db.relationship('Character', foreign_keys=[character_id])
    organisation = db.relationship('Organisation', foreign_keys=[organisation_id])

    @validates('role')
    def validate_text(self, _key, role):
        """ Vérifier que le role est une chaîne non vide d'une longueur maximale de 50 caractères. """
        if not isinstance(role, str):
            raise ValueError("Le nom doit être une chaîne de caractère")
        if not role:
            raise ValueError("Le role est requis.")
        if len(role) > 50:
            raise ValueError("Le role ne doit pas dépasser 50 caractères.")
        return role
    
    def to_dict(self):
        return {
            'id': self.id,
            'role': self.role,
            'character': self.character.to_dict() if self.character else None,
            'organisation': self.organisation.to_dict() if self.organisation else None,
        }

    """
    pour éviter les boucles infinis
    'character': {
        'id': self.character.id,
        'name': self.character.name
    } if self.character else None,
    """
