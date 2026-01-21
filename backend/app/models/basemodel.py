"""
Classe parente qui sert aux autres modèles pour fournir des fonctionalités
principales réutilisés 
"""
from backend.app import db
from datetime import datetime, timezone

class BaseModel(db.Model):
    """
    Note:
        Cette classe est abstraite (__abstract__ = True) et ne créera pas
        de table en base de données. Elle sert uniquement de modèle parent.
    """

    __abstract__ = True

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    image_url = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                          onupdate=lambda: datetime.now(timezone.utc))

    def save(self):
        """
        sauvegarde de l'objet en base de données

        Cette méthode simplifie le processus de sauvegarde en encapsulant
        les opérations db.session.add() et db.session.commit(). Elle met
        également à jour automatiquement le champ updated_at.
        """
        self.updated_at = datetime.now(timezone.utc)
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        """
        Convertit l'objet en dictionnaire de base.

        Cette méthode de base retourne uniquement les champs communs (id, timestamps).
        Elle DOIT être surchargée dans les classes enfants pour inclure leurs
        attributs spécifiques.
        Returns:
            dict: Dictionnaire avec id, created_at, updated_at

        Note:
        Les dates sont converties au format ISO 8601 (ex: "2024-01-15T10:30:00")
        pour faciliter la sérialisation JSON et l'interopérabilité.
        """
        return {
            'id': self.id,
            'image_url': self.image_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
