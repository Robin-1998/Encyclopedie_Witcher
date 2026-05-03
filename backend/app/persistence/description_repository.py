"""
Repository spécifique pour les descriptions.
Le système de descriptions est générique : une description
peut appartenir à n'importe quelle entité (character, place, race, etc.)
via entity_type + entity_id.
"""
from backend.app.models.description import Description
from backend.app.persistence.repository import SQLAlchemyRepository


class DescriptionRepository(SQLAlchemyRepository):

    def __init__(self):
        super().__init__(Description)

    def get_by_entity(self, entity_type: str, entity_id: int) -> list[Description]:
        """
        Retourne toutes les descriptions d'une entité, triées par order_index.
        Exemple : get_by_entity('character', 42)
        """
        return (
            self.model.query
            .filter_by(entity_type=entity_type, entity_id=entity_id)
            .order_by(Description.order_index)
            .all()
        )

    def get_by_entity_and_order(self, entity_type: str, entity_id: int, order_index: int) -> Description | None:
        """Récupère une section précise par sa position (contrainte UNIQUE en DB)."""
        return self.model.query.filter_by(
            entity_type=entity_type,
            entity_id=entity_id,
            order_index=order_index
        ).first()

    def delete_all_by_entity(self, entity_type: str, entity_id: int) -> int:
        """
        Supprime toutes les descriptions d'une entité.
        Retourne le nombre de lignes supprimées.
        À appeler depuis la Facade lors de la suppression d'une entité parente.
        """
        descriptions = self.get_by_entity(entity_type, entity_id)
        count = len(descriptions)
        for desc in descriptions:
            self._db.session.delete(desc)
        self._db.session.commit()
        return count
