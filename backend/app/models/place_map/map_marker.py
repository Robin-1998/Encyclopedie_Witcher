"""
Modèle contenant les marqueur de lieu géographiques

Ce modèle représente chaque marqueur sur une carte.
Chaque région est stockée sous forme géométrique (de type polygon)
"""
from backend.app.models.basemodel import BaseModel
from backend.app import db
from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape
from shapely.geometry import mapping
from sqlalchemy import Enum
import enum

# Définir l'ENUM Python pour correspondre à l'ENUM PostgreSQL
class MarkerTypeEnum(enum.Enum):
    """
    Énumération des types de marqueurs disponibles sur la carte.

    IMPORTANT :
    - Les valeurs (à droite) doivent correspondre EXACTEMENT
      aux valeurs de l'ENUM PostgreSQL `marker_type`.
    - Les clés Python (à gauche) sont sans accents pour rester valides en Python.
    - Toute désynchronisation avec la base provoquera une erreur SQL.
    """
    royaume = 'royaume'
    foret = 'foret'
    montagne = 'montagne'
    forteresse = 'forteresse'
    village = 'village'
    ville = 'ville'
    duche = 'duché'
    provinces = 'provinces'
    baronnies = 'baronnies'
    principautes = 'principautés'
    ile = 'île'
    riviere = 'rivière'
    mer = 'mer'
    taverne = 'taverne'
    special = 'special'
    magique = 'magique'
    ruine = 'ruine'
    capitale = 'capitale'
    port = 'port'
    monument = 'monument'
    marais = 'marais'
    lac = 'lac'
    chateau = 'château'
    manoir = 'manoir'
    temple = 'temple'
    route = 'route'
    marche = 'marché'
    grotte = 'grotte'
    mine = 'mine'
    plan = 'plan'
    tour = 'tour'
    phare = 'phare'
    default = 'default'

class MapMarker(BaseModel):
    """
    Modèle représentant un marqueur de lieu sur la carte.

    Un marqueur correspond à un point précis (coordonnées X/Y),
    associé à :
    - un nom
    - un type (ENUM)
    - éventuellement un lieu parent (Place)
    """
    __tablename__ = "map_marker"

    name = db.Column(db.String(100), nullable=False, unique=True)
    # Coordonnées géographiques (PostGIS POINT)
    location = db.Column(Geometry('POINT', srid=0), nullable=False)

    # Type du marqueur (ville, ruine, port, etc.)
    # Relié directement à l'ENUM PostgreSQL marker_type    type = db.Column(Enum(MarkerTypeEnum, name='marker_type', native_enum=True), nullable=False, default=MarkerTypeEnum.default)
    place_id = db.Column(db.BigInteger, db.ForeignKey('places.id'))
    place = db.relationship('Place', back_populates='map_markers')

    def to_dict(self):
        """
        Conversion en dictionnaire avec coordonnées
        Le frontend utilisera ces données pour afficher le marqueur
        - La géométrie PostGIS est convertie en objet Shapely (`to_shape`)
        - L'objet Shapely est transformé en GeoJSON via `mapping`
        """
        geom = to_shape(self.location)
        return {
            "id": self.id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "name": self.name,
            "type": self.type.value if self.type else 'default',
            "place_id": self.place_id,
            "geometry": mapping(geom)
        }
