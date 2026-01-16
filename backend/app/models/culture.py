"""
Classe modèle pour les différentes cultures
"""
from backend.app import db
from backend.app.models.basemodel import BaseModel
from sqlalchemy.orm import validates

class Culture(BaseModel):
    """
    Classe culture en lecture seule

    Cette classe contient les attributs tels que :
    name, description
    """

    __tablename__ = "cultures"


    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)

    characters = db.relationship('Character', back_populates='culture', lazy='select')

    @validates('name')
    def validate_name(self, key, name):
        if not isinstance(name, str):
            raise ValueError("Le nom doit être une chaîne.")
        if not name.strip():
            raise ValueError("Le nom est requis.")
        return name

    def to_dict(self):
        """
        Convertit l'objet Culture en dictionnaire sérialisable

        Cette méthode va réutiliser BaseModel afin d'inclure les champs id,
        created_at, updated_at
        """
        data = super().to_dict() # récupère le dictionnaire du parent
        data.update ({
            "name": self.name,
            "description": self.description
        })
        return data
