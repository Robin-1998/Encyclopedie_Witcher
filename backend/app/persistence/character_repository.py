"""
Repository spécifique pour les entités `Character`.
Hérite de SQLAlchemyRepository et ajoute des méthodes de filtrage
propres aux personnages (par race, profession, culture, lieu).
"""
from backend.app.models.character import Character
from backend.app.persistence.repository import SQLAlchemyRepository


class CharacterRepository(SQLAlchemyRepository):

    def __init__(self):
        super().__init__(Character)

    def get_by_name(self, name: str) -> Character | None:
        """Récupère un personnage par son nom exact."""
        return self.model.query.filter_by(name=name).first()

    def get_by_race(self, race_id: int) -> list[Character]:
        """Retourne tous les personnages d'une race donnée."""
        return self.model.query.filter_by(race_id=race_id).all()

    def get_by_profession(self, profession_id: int) -> list[Character]:
        """Retourne tous les personnages d'une profession donnée."""
        return self.model.query.filter_by(profession_id=profession_id).all()

    def get_by_culture(self, culture_id: int) -> list[Character]:
        """Retourne tous les personnages liés à une culture."""
        return self.model.query.filter_by(culture_id=culture_id).all()

    def get_by_birth_place(self, place_id: int) -> list[Character]:
        """Retourne tous les personnages nés dans un lieu donné."""
        return self.model.query.filter_by(birth_place_id=place_id).all()

    def get_alive(self) -> list[Character]:
        """Retourne tous les personnages sans date de mort (potentiellement vivants)."""
        return self.model.query.filter(Character.death_date.is_(None)).all()
