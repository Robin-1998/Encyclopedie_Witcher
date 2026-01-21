"""
Classe modèle qui est en relation avec le modèle Obejct
"""

from backend.app import db
from backend.app.models.basemodel import BaseModel

class ObjectType(BaseModel):
    __tablename__ = "object_types"

    name = db.Column(db.String(100), nullable=False, unique=True)

    objects = db.relationship("Object", back_populates="object_type")

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "name": self.name
        })
        return data


