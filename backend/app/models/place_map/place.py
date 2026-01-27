"""
Classe place qui comprend tout les lieux, hérite de base model
Non affilié à un utilisateur

Chaque lieu peut-être visualisé sur une carte via des marqueurs en polygones
ou en point sur PostGIS
"""
from backend.app import db
from backend.app.models.basemodel import BaseModel

class Place(BaseModel):
    """
    Classe place en lecture seule

    Cette classe contient les attributs principaux :
    title, type_place, description, image_url, architecture parent

    Les lieux sont gérés pour les cartes interactive et sur la page dédié
    """

    __tablename__ = "places"

    title = db.Column(db.String(200), nullable=False, unique=True)
    type_place = db.Column(
        db.Enum(
            'royaume',
            'foret',
            'montagne',
            'forteresse',
            'village',
            'univers',
            'ville',
            'duché',
            'provinces', 'baronnies', 'principautés', 'region',
            'île', 'rivière', 'mer', 'taverne', 'multivers', 'special',
            'magique', 'ruine', 'capitale', 'port', 'monument', 'marais',
            'lac', 'château', 'manoir', 'temple', 'route', 'marché', 'monde',
            'grotte', 'mine', 'plan', 'tour', 'phare', 'quartier', 'default',
            name="place_enum", native_enum=False, create_type=False
        ),
        nullable=False
    )
    short_description = db.Column(db.Text, nullable=False)
    parent_id = db.Column(db.BigInteger, db.ForeignKey('places.id'), ondelete='SET NULL')
    # Relation hiérarchique
    parent = db.relationship('Place', remote_side='Place.id', backref='children')

    # relations ORM 

    map_regions = db.relationship('MapRegion', back_populates='place')
    map_markers = db.relationship('MapMarker', back_populates='place')

    def to_dict(self, include_geometry=False):
        data = super().to_dict()
        data.update ({
            "title":self.title,
            "type_place":self.type_place,
            "short_description":self.short_description,
            "parent_id": self.parent_id
        })

    # On inclut la géométrie si demandé
    # Le paramètre include_geometry est un booléen optionnel (par défaut False) 
    # qui permet de choisir si tu veux inclure ces données dans le dictionnaire.

        if include_geometry:
            data["markers"] = [marker.to_dict() for marker in self.map_markers]
            data["regions"] = [region.to_dict() for region in self.map_regions]
        
        return data
