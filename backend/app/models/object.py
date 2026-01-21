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

    def to_dict(self):
        """
        Convertit l'objet Object en dictionnaire sérialisable

        Cette méthode va réutiliser BaseModel afin d'inclure les champs id,
        created_at, updated_at et image_url
        """
        data = super().to_dict()
        data.update ({
            "name": self.name.id,
            "short_description": self.short_description.id
        })
        return data
