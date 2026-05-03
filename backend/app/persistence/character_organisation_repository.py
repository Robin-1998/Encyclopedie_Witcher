"""
Repository spécifique pour la table d'association `character_organisations`.
Gère le lien entre un personnage et une organisation, avec son rôle.
"""
from backend.app.models.character_organisation import CharacterOrganisation
from backend.app.persistence.repository import SQLAlchemyRepository


class CharacterOrganisationRepository(SQLAlchemyRepository):

    def __init__(self):
        super().__init__(CharacterOrganisation)

    def get_by_character(self, character_id: int) -> list[CharacterOrganisation]:
        """Retourne toutes les organisations d'un personnage."""
        return self.model.query.filter_by(character_id=character_id).all()

    def get_by_organisation(self, organisation_id: int) -> list[CharacterOrganisation]:
        """Retourne tous les membres d'une organisation."""
        return self.model.query.filter_by(organisation_id=organisation_id).all()

    def get_link(self, character_id: int, organisation_id: int) -> CharacterOrganisation | None:
        """Retourne le lien exact entre un personnage et une organisation."""
        return self.model.query.filter_by(
            character_id=character_id,
            organisation_id=organisation_id
        ).first()

    def get_by_role(self, role: str) -> list[CharacterOrganisation]:
        """Retourne tous les liens correspondant à un rôle donné (ex: 'chef', 'membre')."""
        return self.model.query.filter_by(role=role).all()
