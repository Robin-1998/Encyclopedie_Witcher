"""
Repository spécifique pour les professions.
"""
from backend.app.models.profession import Profession
from backend.app.persistence.repository import SQLAlchemyRepository


class ProfessionRepository(SQLAlchemyRepository):

    def __init__(self):
        super().__init__(Profession)

    def get_by_name(self, name: str) -> Profession | None:
        """Récupère une profession par son nom exact."""
        return self.model.query.filter_by(name=name).first()

    def name_exists(self, name: str) -> bool:
        """Vérifie si une profession avec ce nom existe déjà."""
        return self.get_by_name(name) is not None
