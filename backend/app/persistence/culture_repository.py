"""
Repositories pour les cultures.
- CultureTypeRepository : types de cultures (magie, religion, etc.)
- CultureRepository     : les cultures avec leur hiérarchie parent/enfant
"""
from backend.app.models.culture_type import CultureType
from backend.app.models.culture import Culture
from backend.app.persistence.repository import SQLAlchemyRepository


class CultureTypeRepository(SQLAlchemyRepository):

    def __init__(self):
        super().__init__(CultureType)

    def get_by_name(self, name: str) -> CultureType | None:
        return self.model.query.filter_by(name=name).first()


class CultureRepository(SQLAlchemyRepository):

    def __init__(self):
        super().__init__(Culture)

    def get_by_name(self, name: str) -> Culture | None:
        return self.model.query.filter_by(name=name).first()

    def get_by_type(self, culture_type_id: int) -> list[Culture]:
        """Retourne toutes les cultures d'un type donné."""
        return self.model.query.filter_by(culture_type_id=culture_type_id).all()

    def get_children(self, parent_culture_id: int) -> list[Culture]:
        """Retourne les sous-cultures d'une culture parente."""
        return self.model.query.filter_by(parent_culture_id=parent_culture_id).all()

    def get_root_cultures(self) -> list[Culture]:
        """Retourne les cultures sans parent (niveau racine)."""
        return self.model.query.filter(Culture.parent_culture_id.is_(None)).all()
