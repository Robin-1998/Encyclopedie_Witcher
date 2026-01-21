"""
Classe modèle profession qui hérite de basemodel
Non affilié à un utilisateur
"""

from backend.app import db
from backend.app.models.basemodel import BaseModel

class Profession(BaseModel):
    """
    Classe profession en lecture seule

    Cette classe contient les attributs principaux :
        - name, short_description et les attributs hérités de basemodel
    """
    __tablename__ = "professions"

    name = db.Column(db.String(100), nullable=False)
    short_description = db.Column(db.Text)

    def to_dict(self):
        """
        Convertit l'objet Profession en dictionnaire sérialisable
        
        Cette méthode va réutiliser BaseModel afin d'inclure
        id, created_at, updated_at
        """
        data = super().to_dict()
        data.update ({
            "name": self.name,
            "short_description": self.short_description
        })
        return data
