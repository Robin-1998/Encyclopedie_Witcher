"""
Repositories pour les entités géographiques de la carte interactive.
- MapMarkerRepository : points sur la carte (villes, lieux clés...)
- MapRegionRepository : zones polygonales (royaumes, régions...)
Les géométries utilisent GeoAlchemy2 avec SRID=0 (carte custom sans projection).
"""
from backend.app.models.place_map.map_marker import MapMarker
from backend.app.models.place_map.map_region import MapRegion
from backend.app.persistence.repository import SQLAlchemyRepository


class MapMarkerRepository(SQLAlchemyRepository):

    def __init__(self):
        super().__init__(MapMarker)

    def get_by_name(self, name: str) -> MapMarker | None:
        return self.model.query.filter_by(name=name).first()

    def get_by_place(self, place_id: int) -> list[MapMarker]:
        """Retourne tous les marqueurs liés à un lieu donné."""
        return self.model.query.filter_by(place_id=place_id).all()

    def get_by_type(self, marker_type: str) -> list[MapMarker]:
        """
        Filtre les marqueurs par type (ex: 'ville', 'château', 'forteresse').
        Les valeurs valides correspondent à l'enum marker_type en DB.
        """
        return self.model.query.filter_by(type=marker_type).all()

    def get_without_place(self) -> list[MapMarker]:
        """Retourne les marqueurs non encore liés à un lieu (place_id NULL)."""
        return self.model.query.filter(MapMarker.place_id.is_(None)).all()


class MapRegionRepository(SQLAlchemyRepository):

    def __init__(self):
        super().__init__(MapRegion)

    def get_by_name(self, name: str) -> MapRegion | None:
        return self.model.query.filter_by(name=name).first()

    def get_by_place(self, place_id: int) -> list[MapRegion]:
        """Retourne toutes les régions liées à un lieu."""
        return self.model.query.filter_by(place_id=place_id).all()

    def get_without_place(self) -> list[MapRegion]:
        """Retourne les régions non encore liées à un lieu (place_id NULL)."""
        return self.model.query.filter(MapRegion.place_id.is_(None)).all()
