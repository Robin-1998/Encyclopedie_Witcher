"""
Modèle pour le nom d'un type d'une organisation, en lien avec le modèle Organisation
"""
from backend.app import db
from backend.app.models.basemodel import BaseModel

class OrganisationType(BaseModel):
    __tablename__ = "organisation_types"

    name = db.Column(db.String(150), nullable=False)

    organisations = db.relationship("Organisation", back_populates="organisation_type")

def to_dict(self):
    return {
        'id': self.id,
        'name': self.name
    }
