"""
Repository spécifique pour les entités `Place`.
Ajoute des méthodes de filtrage par type, hiérarchie parent/enfant.
"""
from backend.app.models.place_map.place import Place
from backend.app.persistence.repository import SQLAlchemyRepository


class PlaceRepository(SQLAlchemyRepository):

    def __init__(self):
        super().__init__(Place)

    def get_by_title(self, title: str) -> Place | None:
        """Récupère un lieu par son titre exact."""
        return self.model.query.filter_by(title=title).first()

    def get_by_type(self, type_place: str) -> list[Place]:
        """Retourne tous les lieux d'un type donné (ex: 'royaume', 'ville')."""
        return self.model.query.filter_by(type_place=type_place).all()

    def get_children(self, parent_id: int) -> list[Place]:
        """Retourne tous les lieux enfants d'un lieu parent."""
        return self.model.query.filter_by(parent_id=parent_id).all()

    def get_root_places(self) -> list[Place]:
        """Retourne tous les lieux racines (sans parent), ex: les univers/mondes."""
        return self.model.query.filter(Place.parent_id.is_(None)).all()
