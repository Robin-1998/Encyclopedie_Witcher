"""
Classe modèle pour les races
"""

from backend.app import db
from backend.app.models.basemodel import BaseModel

class Race(BaseModel):
    """
    Classe Race qui hérite de basemodel, en lecture seul
    """
    __tablename__ = "races"

    name = db.Column(db.String(100), nullable=False, unique=True)
    race_type_id = db.Column(db.BigInteger, db.ForeignKey("race_types.id"), nullable=False)
    short_description = db.Column(db.Text, nullable=False)
    citation = db.Column(db.String(400))

    # ------------------------
    # Relations ORM
    # ------------------------

    race_type = db.relationship("RaceType", back_populates="races")

    def to_dict(self):
        data = super().to_dict()
        data.update ({
            "name": self.name,
            "race_type_id": self.race_type.id,
            "short_description": self.short_description,
            "citation": self.citation
        })
        return data
