"""
Modèle pour les traits de race
Exemple : faiblesse, environnement...
"""
from backend.app import db
from backend.app.models.basemodel import BaseModel

class RaceTrait(BaseModel):
    __tablename__ = "race_traits"

    race_id = db.Column(db.BigInteger, db.ForeignKey("races.id"), nullable=False)
    trait = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50))

    # Relation ORM
    race = db.relationship("Race", back_populate="race_traits", nullable=False)

    def to_dict(self):
        data = super().to_dict()
        data.update ({
            "race_id": self.race_id,
            "trait": self.trait,
            "category": self.category
        })
        return data
