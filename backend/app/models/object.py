"""
Classe modèle object qui hérite de basemodel
Non affilié à un utilisateur
Est lié au modèle object_type
"""

from backend.app import db
from backend.app.models.basemodel import BaseModel

class Object(BaseModel):
    """
    Class object qui hérite de basemodel
    """

    __tablename__ = "objects"

    name = db.Column(db.String(100), nullable=False)
    short_description = db.Column(db.Text)

    object_type_id = db.Column(db.BigInteger,db.ForeignKey("object_types.id"),nullable=False)

    object_type = db.relationship("ObjectType",back_populates="objects")

    def to_dict(self):
        """
        Convertit l'objet Object en dictionnaire sérialisable

        Cette méthode va réutiliser BaseModel afin d'inclure les champs id,
        created_at, updated_at et image_url
        """
        data = super().to_dict()
        data.update ({
            "name": self.name,
            "short_description": self.short_description
            "object_type_id": self.object_type_id
        })
        return data
