"""
Repositories pour les relations entre lieux.
- RelationTypeRepository : gère les types de relations (ex: 'borde', 'contient')
- PlacesRelationRepository : gère les liens entre lieux
"""
from backend.app.models.relation_type import RelationType
from backend.app.models.places_relation import PlacesRelation
from backend.app.persistence.repository import SQLAlchemyRepository


class RelationTypeRepository(SQLAlchemyRepository):

    def __init__(self):
        super().__init__(RelationType)

    def get_by_name(self, name: str) -> RelationType | None:
        """Récupère un type de relation par son nom."""
        return self.model.query.filter_by(name=name).first()


class PlacesRelationRepository(SQLAlchemyRepository):

    def __init__(self):
        super().__init__(PlacesRelation)

    def get_by_place(self, place_id: int) -> list[PlacesRelation]:
        """Retourne toutes les relations dont ce lieu est la source."""
        return self.model.query.filter_by(place_id=place_id).all()

    def get_by_related_place(self, related_place_id: int) -> list[PlacesRelation]:
        """Retourne toutes les relations dont ce lieu est la cible."""
        return self.model.query.filter_by(related_place_id=related_place_id).all()

    def get_all_for_place(self, place_id: int) -> list[PlacesRelation]:
        """
        Retourne toutes les relations impliquant ce lieu
        (source OU cible), utile pour un affichage bidirectionnel.
        """
        return self.model.query.filter(
            (PlacesRelation.place_id == place_id) |
            (PlacesRelation.related_place_id == place_id)
        ).all()

    def get_by_relation_type(self, relation_type_id: int) -> list[PlacesRelation]:
        """Retourne toutes les relations d'un type donné."""
        return self.model.query.filter_by(relation_type_id=relation_type_id).all()
