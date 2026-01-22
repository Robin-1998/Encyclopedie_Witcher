"""
Classe modèle pour le type de culture
"""

from backend.app import db
from backend.app.models.basemodel import BaseModel

class CultureType(BaseModel):
    __tablename__ = "culture_types"

    name = db.Column(db.String(100), nullable=False, unique=True)

    cultures = db.relationship("Culture", back_populates="culture_type", lazy="select")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "image_url": self.image_url
        }
