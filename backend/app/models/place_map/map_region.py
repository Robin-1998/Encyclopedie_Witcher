"""
Modèle contenant les régions géographiques

Ce modèle représente chaque région ou zone importante sur la carte.
Chaque région est stockée sous forme géométrique (de type polygon)
"""

from backend.app import db
from backend.app.models.basemodel import BaseModel
from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape
from shapely.geometry import mapping

class MapRegion(BaseModel):
    """
    La class région permet de définir des zones larges avec les polygons.
    Ils peuvent êtres associé à des lieux.
    Une région est souvent le parent de plusieurs petites villes ou autre entité
    ex : Rédanie -> Novigrad -> Auberge du thym et romarin
    """
    __tablename__="map_region"

    name = db.Column(db.String(100), nullable=False, unique=True)
    shape_data = db.Column(Geometry('POLYGON', srid=0), nullable=False)

    place_id = db.Column(db.BigInteger, db.ForeignKey('places.id'))
    place = db.relationship('Place', back_populates='map_regions')

    def to_dict(self):
        """
        Convertit la région en dictionnaire JSON-sérialisable.

        Cette méthode extrait les coordonnées du polygone (via Shapely)
        pour fournir une structure compatible avec le format GeoJSON,
        utilisable directement par le frontend (ex: Leaflet, Mapbox).

        arg -> mapping(geom) sert exactement à traduire une forme géographique Python (Shapely)
        en un objet GeoJSON standard, compréhensible par le frontend.
        """
        geography = to_shape(self.shape_data)
        return {
            "id": self.id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "name": self.name,
            "place_id": self.place_id,
            "geometry": mapping(geography)
        }
