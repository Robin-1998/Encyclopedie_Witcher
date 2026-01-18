"""
Modèle représentant les organsations
hérite de basemodel
"""

from backend.app import db
from backend.app.models.basemodel import BaseModel

class Organisation(BaseModel):
    """
    Classe qui représente une organisation
    """
    __tablename__ = "organisations"

    name = db.Column(db.String(100), nullable=False)
    short_description = db.Column(db.Text)
    organisation_type_id = db.Column(db.BigInteger, db.ForeignKey('organisation_types.id', ondelete='RESTRICT'))

    #Relation ORM
    organisation_type = db.relationship("OrganisationType", back_populates="organisations", passive_deletes=True)

    def to_dict(self):
        """
        Convertit l'objet Organisation en dictionnaire sérialisable

        Cette méthode va réutiliser BaseModel afin d'inclure les champs id,
        created_at, updated_at
        """
        data = super().to_dict() # récupère le dictionnaire du parent
        data.update ({
            "name": self.name,
            "short_description": self.short_description,
            "organisation_type": self.organisation_type.id,
        })
        return data
