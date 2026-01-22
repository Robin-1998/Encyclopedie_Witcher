"""
Classe modèle pour représenter les relations entre différents lieux.
Chaque instance relie un lieu à un autre lieu et indique le type de relation.
"""

from backend.app import db
from backend.app.models.basemodel import BaseModel

class PlaceRelation(BaseModel):
    __tablename__ = "place_relations"

    relation_type_id = db.Column(db.BigInteger, db.ForeignKey('relation_types.id'), nullable=False)
    place_id = db.Column(db.BigInteger, db.ForeignKey('places.id'), nullable=False)
    related_place_id = db.Column(db.BigInteger, db.ForeignKey('places.id'), nullable=False)
    
    # relation ORM

    relation_type = db.relationship("RelationType", back_populates="place_relations")
    place = db.relationship("Place", foreign_keys=[place_id], back_populates="relations")
    related_place = db.relationship("Place", foreign_keys=[related_place_id])

    def to_dict(self):
        return {
            "id": self.id,
            "place_id": self.place_id,
            "related_place_id": self.related_place_id,
            "relation_type_id": self.relation_type_id
            # "relation_type_name": self.relation_type.name if self.relation_type else None
        }
