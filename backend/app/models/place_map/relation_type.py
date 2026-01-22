"""
Classe modèle pour les différents types de relations entre lieux
"""

from backend.app import db
from backend.app.models.basemodel import BaseModel

class RelationType(BaseModel):
    """
    Classe modèle pour les différents types de relations entre lieux.
    Chaque type est utilisé dans la table `places_relations` pour indiquer
    la nature de la relation entre deux lieux.
    """
    __tablename__ = "relation_types"

    name = db.Column(db.String(100), nullable=False, unique=True)

    place_relations = db.relationship("PlaceRelation", back_populates="relation_type", lazy='select')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }
