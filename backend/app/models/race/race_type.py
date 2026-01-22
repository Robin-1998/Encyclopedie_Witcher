"""
Classe modèle pour les type de race
exemple : Vampire, Goule, Vampire originel
"""
from backend.app import db
from backend.app.models.basemodel import BaseModel

class RaceType(BaseModel):
    __tablename__ = "race_types"

    name = db.Column(db.String(100), nullable=False)
    short_description = db.Column(db.Text)
    citation = db.Column(db.String)

    parent_race_type_id = db.Column(db.BigInteger, db.ForeignKey("race_types.id", ondelete="RESTRICT"), nullable=True)
    parent_race_type = db.Column(
        db.relationship("RaceType", remote_side="RaceType.id", back_populates="children")
    )
    children = db.relationship("RaceType", back_populates="parent_race_type", lazy="select")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "short_description": self.short_description,
            "citation": self.citation,
            "image_url": self.image_url,
            "parent_race_type_id": self.parent_race_type.id
        }
