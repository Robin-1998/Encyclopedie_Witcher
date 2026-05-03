"""
Repositories pour les objets.
- ObjectTypeRepository : types d'objets (arme, artefact, etc.)
- ObjectRepository     : les objets eux-mêmes
"""
from backend.app.models.object_type import ObjectType
from backend.app.models.object import Object
from backend.app.persistence.repository import SQLAlchemyRepository


class ObjectTypeRepository(SQLAlchemyRepository):

    def __init__(self):
        super().__init__(ObjectType)

    def get_by_name(self, name: str) -> ObjectType | None:
        return self.model.query.filter_by(name=name).first()


class ObjectRepository(SQLAlchemyRepository):

    def __init__(self):
        super().__init__(Object)

    def get_by_name(self, name: str) -> Object | None:
        return self.model.query.filter_by(name=name).first()

    def get_by_type(self, object_type_id: int) -> list[Object]:
        """Retourne tous les objets d'un type donné."""
        return self.model.query.filter_by(object_type_id=object_type_id).all()
