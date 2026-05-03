"""
Repositories pour les races et leurs sous-entités.
- RaceTypeRepository  : types de races (ex: humanoïdes, monstres...)
- RaceRepository      : les races elles-mêmes
- RaceTraitRepository : les traits associés à chaque race
"""
from backend.app.models.race_type import RaceType
from backend.app.models.race import Race
from backend.app.models.race_trait import RaceTrait
from backend.app.persistence.repository import SQLAlchemyRepository


class RaceTypeRepository(SQLAlchemyRepository):

    def __init__(self):
        super().__init__(RaceType)

    def get_by_name(self, name: str) -> RaceType | None:
        return self.model.query.filter_by(name=name).first()

    def get_children(self, parent_id: int) -> list[RaceType]:
        """Retourne les sous-types d'un type de race parent."""
        return self.model.query.filter_by(parent_id=parent_id).all()

    def get_root_types(self) -> list[RaceType]:
        """Retourne les types de race sans parent."""
        return self.model.query.filter(RaceType.parent_id.is_(None)).all()


class RaceRepository(SQLAlchemyRepository):

    def __init__(self):
        super().__init__(Race)

    def get_by_name(self, name: str) -> Race | None:
        return self.model.query.filter_by(name=name).first()

    def get_by_type(self, race_type_id: int) -> list[Race]:
        """Retourne toutes les races d'un type donné."""
        return self.model.query.filter_by(race_type_id=race_type_id).all()


class RaceTraitRepository(SQLAlchemyRepository):

    def __init__(self):
        super().__init__(RaceTrait)

    def get_by_race(self, race_id: int) -> list[RaceTrait]:
        """Retourne tous les traits d'une race."""
        return self.model.query.filter_by(race_id=race_id).all()

    def get_by_category(self, race_id: int, category: str) -> list[RaceTrait]:
        """Retourne les traits d'une race filtrés par catégorie."""
        return self.model.query.filter_by(race_id=race_id, category=category).all()
