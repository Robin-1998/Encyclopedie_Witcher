"""
Repositories pour les organisations.
- OrganisationTypeRepository : types d'organisations (guilde, ordre, etc.)
- OrganisationRepository     : les organisations elles-mêmes
"""
from backend.app.models.organisation_type import OrganisationType
from backend.app.models.organisation import Organisation
from backend.app.persistence.repository import SQLAlchemyRepository


class OrganisationTypeRepository(SQLAlchemyRepository):

    def __init__(self):
        super().__init__(OrganisationType)

    def get_by_name(self, name: str) -> OrganisationType | None:
        return self.model.query.filter_by(name=name).first()


class OrganisationRepository(SQLAlchemyRepository):

    def __init__(self):
        super().__init__(Organisation)

    def get_by_name(self, name: str) -> Organisation | None:
        return self.model.query.filter_by(name=name).first()

    def get_by_type(self, organisation_type_id: int) -> list[Organisation]:
        """Retourne toutes les organisations d'un type donné."""
        return self.model.query.filter_by(organisation_type_id=organisation_type_id).all()
