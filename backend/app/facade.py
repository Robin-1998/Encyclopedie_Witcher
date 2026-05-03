"""
Facade principale du projet The Witcher.
Orchestre les repositories — ne touche jamais directement à db.session.
Toute la persistance est déléguée aux repositories spécialisés.
"""
from backend.app.models.character import Character
from backend.app.models.character_organisation import CharacterOrganisation
from backend.app.models.culture import Culture
from backend.app.models.culture_type import CultureType
from backend.app.models.description import Description
from backend.app.models.place_map.map_marker import MapMarker
from backend.app.models.place_map.map_region import MapRegion
from backend.app.models.object import Object
from backend.app.models.object_type import ObjectType
from backend.app.models.organisation import Organisation
from backend.app.models.organisation_type import OrganisationType
from backend.app.models.place_map.place import Place
from backend.app.models.place_map.place_relation import PlacesRelation
from backend.app.models.profession import Profession
from backend.app.models.race import Race
from backend.app.models.race.race_trait import RaceTrait
from backend.app.models.race.race_type import RaceType
from backend.app.models.place_map.relation_type import RelationType
from backend.app.models.user import User

from backend.app.persistence.user_repository import UserRepository
from backend.app.persistence.character_repository import CharacterRepository
from backend.app.persistence.character_organisation_repository import CharacterOrganisationRepository
from backend.app.persistence.culture_repository import CultureRepository, CultureTypeRepository
from backend.app.persistence.description_repository import DescriptionRepository
from backend.app.persistence.map_repository import MapMarkerRepository, MapRegionRepository
from backend.app.persistence.object_repository import ObjectRepository, ObjectTypeRepository
from backend.app.persistence.organisation_repository import OrganisationRepository, OrganisationTypeRepository
from backend.app.persistence.place_repository import PlaceRepository
from backend.app.persistence.places_relation_repository import PlacesRelationRepository, RelationTypeRepository
from backend.app.persistence.profession_repository import ProfessionRepository
from backend.app.persistence.race_repository import RaceRepository, RaceTypeRepository, RaceTraitRepository


class Facade:
    """
    Facade pour le projet The Witcher.
    Instancie tous les repositories et expose les opérations métier.
    """

    def __init__(self):
        self.character_repo = CharacterRepository()
        self.character_org_repo = CharacterOrganisationRepository()
        self.culture_repo = CultureRepository()
        self.culture_type_repo = CultureTypeRepository()
        self.description_repo = DescriptionRepository()
        self.map_marker_repo = MapMarkerRepository()
        self.map_region_repo = MapRegionRepository()
        self.object_repo = ObjectRepository()
        self.object_type_repo = ObjectTypeRepository()
        self.organisation_repo = OrganisationRepository()
        self.organisation_type_repo = OrganisationTypeRepository()
        self.place_repo = PlaceRepository()
        self.places_relation_repo = PlacesRelationRepository()
        self.profession_repo = ProfessionRepository()
        self.race_repo = RaceRepository()
        self.race_type_repo = RaceTypeRepository()
        self.race_trait_repo = RaceTraitRepository()
        self.relation_type_repo = RelationTypeRepository()
        self.user_repo = UserRepository()

    # =========================================================================
    # PROFESSION
    # =========================================================================

    def post_profession(self, name: str, short_description: str = None, image_url: str = None) -> Profession:
        profession = Profession(name=name, short_description=short_description, image_url=image_url)
        self.profession_repo.add(profession)
        return profession

    def get_profession(self, profession_id: int) -> Profession | None:
        return self.profession_repo.get(profession_id)

    def get_all_professions(self) -> list[Profession]:
        return self.profession_repo.get_all()

    def put_profession(self, profession_id: int, **kwargs) -> Profession | None:
        return self.profession_repo.update(profession_id, kwargs)

    def delete_profession(self, profession_id: int) -> bool:
        return self.profession_repo.delete(profession_id)

    # =========================================================================
    # CULTURE TYPE
    # =========================================================================

    def post_culture_type(self, name: str, image_url: str = None) -> CultureType:
        culture_type = CultureType(name=name, image_url=image_url)
        self.culture_type_repo.add(culture_type)
        return culture_type

    def get_culture_type(self, culture_type_id: int) -> CultureType | None:
        return self.culture_type_repo.get(culture_type_id)

    def get_all_culture_types(self) -> list[CultureType]:
        return self.culture_type_repo.get_all()

    def put_culture_type(self, culture_type_id: int, **kwargs) -> CultureType | None:
        return self.culture_type_repo.update(culture_type_id, kwargs)

    def delete_culture_type(self, culture_type_id: int) -> bool:
        return self.culture_type_repo.delete(culture_type_id)

    # =========================================================================
    # CULTURE
    # =========================================================================

    def post_culture(
        self,
        name: str,
        culture_type_id: int,
        short_description: str = None,
        image_url: str = None,
        parent_culture_id: int = None
    ) -> Culture:
        culture = Culture(
            name=name,
            culture_type_id=culture_type_id,
            short_description=short_description,
            image_url=image_url,
            parent_culture_id=parent_culture_id
        )
        self.culture_repo.add(culture)
        return culture

    def get_culture(self, culture_id: int) -> Culture | None:
        return self.culture_repo.get(culture_id)

    def get_all_cultures(self) -> list[Culture]:
        return self.culture_repo.get_all()

    def get_cultures_by_type(self, culture_type_id: int) -> list[Culture]:
        return self.culture_repo.get_by_type(culture_type_id)

    def get_culture_children(self, parent_culture_id: int) -> list[Culture]:
        return self.culture_repo.get_children(parent_culture_id)

    def put_culture(self, culture_id: int, **kwargs) -> Culture | None:
        return self.culture_repo.update(culture_id, kwargs)

    def delete_culture(self, culture_id: int) -> bool:
        return self.culture_repo.delete(culture_id)

    # =========================================================================
    # ORGANISATION TYPE
    # =========================================================================

    def post_organisation_type(self, name: str, image_url: str = None) -> OrganisationType:
        org_type = OrganisationType(name=name, image_url=image_url)
        self.organisation_type_repo.add(org_type)
        return org_type

    def get_organisation_type(self, org_type_id: int) -> OrganisationType | None:
        return self.organisation_type_repo.get(org_type_id)

    def get_all_organisation_types(self) -> list[OrganisationType]:
        return self.organisation_type_repo.get_all()

    def put_organisation_type(self, org_type_id: int, **kwargs) -> OrganisationType | None:
        return self.organisation_type_repo.update(org_type_id, kwargs)

    def delete_organisation_type(self, org_type_id: int) -> bool:
        return self.organisation_type_repo.delete(org_type_id)

    # =========================================================================
    # ORGANISATION
    # =========================================================================

    def post_organisation(
        self,
        name: str,
        organisation_type_id: int,
        short_description: str = None,
        image_url: str = None
    ) -> Organisation:
        organisation = Organisation(
            name=name,
            organisation_type_id=organisation_type_id,
            short_description=short_description,
            image_url=image_url
        )
        self.organisation_repo.add(organisation)
        return organisation

    def get_organisation(self, organisation_id: int) -> Organisation | None:
        return self.organisation_repo.get(organisation_id)

    def get_all_organisations(self) -> list[Organisation]:
        return self.organisation_repo.get_all()

    def get_organisations_by_type(self, organisation_type_id: int) -> list[Organisation]:
        return self.organisation_repo.get_by_type(organisation_type_id)

    def put_organisation(self, organisation_id: int, **kwargs) -> Organisation | None:
        return self.organisation_repo.update(organisation_id, kwargs)

    def delete_organisation(self, organisation_id: int) -> bool:
        return self.organisation_repo.delete(organisation_id)

    # =========================================================================
    # OBJECT TYPE
    # =========================================================================

    def post_object_type(self, name: str, image_url: str = None) -> ObjectType:
        obj_type = ObjectType(name=name, image_url=image_url)
        self.object_type_repo.add(obj_type)
        return obj_type

    def get_object_type(self, object_type_id: int) -> ObjectType | None:
        return self.object_type_repo.get(object_type_id)

    def get_all_object_types(self) -> list[ObjectType]:
        return self.object_type_repo.get_all()

    def put_object_type(self, object_type_id: int, **kwargs) -> ObjectType | None:
        return self.object_type_repo.update(object_type_id, kwargs)

    def delete_object_type(self, object_type_id: int) -> bool:
        return self.object_type_repo.delete(object_type_id)

    # =========================================================================
    # OBJECT
    # =========================================================================

    def post_object(
        self,
        name: str,
        object_type_id: int,
        short_description: str = None,
        image_url: str = None
    ) -> Object:
        obj = Object(name=name, object_type_id=object_type_id, short_description=short_description, image_url=image_url)
        self.object_repo.add(obj)
        return obj

    def get_object(self, object_id: int) -> Object | None:
        return self.object_repo.get(object_id)

    def get_all_objects(self) -> list[Object]:
        return self.object_repo.get_all()

    def get_objects_by_type(self, object_type_id: int) -> list[Object]:
        return self.object_repo.get_by_type(object_type_id)

    def put_object(self, object_id: int, **kwargs) -> Object | None:
        return self.object_repo.update(object_id, kwargs)

    def delete_object(self, object_id: int) -> bool:
        return self.object_repo.delete(object_id)

    # =========================================================================
    # RACE TYPE
    # =========================================================================

    def post_race_type(
        self,
        name: str,
        short_description: str = None,
        citation: str = None,
        image_url: str = None,
        parent_id: int = None
    ) -> RaceType:
        race_type = RaceType(
            name=name, short_description=short_description,
            citation=citation, image_url=image_url, parent_id=parent_id
        )
        self.race_type_repo.add(race_type)
        return race_type

    def get_race_type(self, race_type_id: int) -> RaceType | None:
        return self.race_type_repo.get(race_type_id)

    def get_all_race_types(self) -> list[RaceType]:
        return self.race_type_repo.get_all()

    def put_race_type(self, race_type_id: int, **kwargs) -> RaceType | None:
        return self.race_type_repo.update(race_type_id, kwargs)

    def delete_race_type(self, race_type_id: int) -> bool:
        return self.race_type_repo.delete(race_type_id)

    # =========================================================================
    # RACE
    # =========================================================================

    def post_race(
        self,
        name: str,
        race_type_id: int,
        short_description: str,
        citation: str = None,
        image_url: str = None
    ) -> Race:
        race = Race(
            name=name, race_type_id=race_type_id,
            short_description=short_description, citation=citation, image_url=image_url
        )
        self.race_repo.add(race)
        return race

    def get_race(self, race_id: int) -> Race | None:
        return self.race_repo.get(race_id)

    def get_all_races(self) -> list[Race]:
        return self.race_repo.get_all()

    def get_races_by_type(self, race_type_id: int) -> list[Race]:
        return self.race_repo.get_by_type(race_type_id)

    def put_race(self, race_id: int, **kwargs) -> Race | None:
        return self.race_repo.update(race_id, kwargs)

    def delete_race(self, race_id: int) -> bool:
        return self.race_repo.delete(race_id)

    # =========================================================================
    # RACE TRAIT
    # =========================================================================

    def post_race_trait(
        self,
        race_id: int,
        trait: str,
        category: str = None,
        image_url: str = None
    ) -> RaceTrait:
        race_trait = RaceTrait(race_id=race_id, trait=trait, category=category, image_url=image_url)
        self.race_trait_repo.add(race_trait)
        return race_trait

    def get_race_trait(self, race_trait_id: int) -> RaceTrait | None:
        return self.race_trait_repo.get(race_trait_id)

    def get_traits_by_race(self, race_id: int) -> list[RaceTrait]:
        return self.race_trait_repo.get_by_race(race_id)

    def put_race_trait(self, race_trait_id: int, **kwargs) -> RaceTrait | None:
        return self.race_trait_repo.update(race_trait_id, kwargs)

    def delete_race_trait(self, race_trait_id: int) -> bool:
        return self.race_trait_repo.delete(race_trait_id)

    # =========================================================================
    # PLACE
    # =========================================================================

    def post_place(
        self,
        title: str,
        type_place: str,
        short_description: str,
        image_url: str = None,
        parent_id: int = None
    ) -> Place:
        place = Place(
            title=title, type_place=type_place,
            short_description=short_description, image_url=image_url, parent_id=parent_id
        )
        self.place_repo.add(place)
        return place

    def get_place(self, place_id: int) -> Place | None:
        return self.place_repo.get(place_id)

    def get_all_places(self) -> list[Place]:
        return self.place_repo.get_all()

    def get_places_by_type(self, type_place: str) -> list[Place]:
        return self.place_repo.get_by_type(type_place)

    def get_children_places(self, parent_id: int) -> list[Place]:
        return self.place_repo.get_children(parent_id)

    def get_root_places(self) -> list[Place]:
        return self.place_repo.get_root_places()

    def put_place(self, place_id: int, **kwargs) -> Place | None:
        return self.place_repo.update(place_id, kwargs)

    def delete_place(self, place_id: int) -> bool:
        return self.place_repo.delete(place_id)

    # =========================================================================
    # RELATION TYPE
    # =========================================================================

    def post_relation_type(self, name: str) -> RelationType:
        relation_type = RelationType(name=name)
        self.relation_type_repo.add(relation_type)
        return relation_type

    def get_relation_type(self, relation_type_id: int) -> RelationType | None:
        return self.relation_type_repo.get(relation_type_id)

    def get_all_relation_types(self) -> list[RelationType]:
        return self.relation_type_repo.get_all()

    def delete_relation_type(self, relation_type_id: int) -> bool:
        return self.relation_type_repo.delete(relation_type_id)

    # =========================================================================
    # PLACES RELATIONS
    # =========================================================================

    def post_place_relation(
        self,
        place_id: int,
        related_place_id: int,
        relation_type_id: int
    ) -> PlacesRelation:
        place_relation = PlacesRelation(
            place_id=place_id,
            related_place_id=related_place_id,
            relation_type_id=relation_type_id
        )
        self.places_relation_repo.add(place_relation)
        return place_relation

    def get_relations_by_place(self, place_id: int) -> list[PlacesRelation]:
        return self.places_relation_repo.get_all_for_place(place_id)

    def delete_place_relation(self, place_relation_id: int) -> bool:
        return self.places_relation_repo.delete(place_relation_id)

    # =========================================================================
    # MAP MARKER
    # =========================================================================

    def post_map_marker(self, name: str, location, marker_type: str = 'default', place_id: int = None) -> MapMarker:
        """
        location = WKTElement('POINT(x y)', srid=0) via geoalchemy2
        """
        marker = MapMarker(name=name, location=location, type=marker_type, place_id=place_id)
        self.map_marker_repo.add(marker)
        return marker

    def get_map_marker(self, marker_id: int) -> MapMarker | None:
        return self.map_marker_repo.get(marker_id)

    def get_all_map_markers(self) -> list[MapMarker]:
        return self.map_marker_repo.get_all()

    def get_markers_by_place(self, place_id: int) -> list[MapMarker]:
        return self.map_marker_repo.get_by_place(place_id)

    def put_map_marker(self, marker_id: int, **kwargs) -> MapMarker | None:
        return self.map_marker_repo.update(marker_id, kwargs)

    def delete_map_marker(self, marker_id: int) -> bool:
        return self.map_marker_repo.delete(marker_id)

    # =========================================================================
    # MAP REGION
    # =========================================================================

    def post_map_region(self, name: str, shape_data, place_id: int = None) -> MapRegion:
        """
        shape_data = WKTElement('POLYGON((x1 y1, x2 y2, ...))', srid=0) via geoalchemy2
        """
        region = MapRegion(name=name, shape_data=shape_data, place_id=place_id)
        self.map_region_repo.add(region)
        return region

    def get_map_region(self, region_id: int) -> MapRegion | None:
        return self.map_region_repo.get(region_id)

    def get_all_map_regions(self) -> list[MapRegion]:
        return self.map_region_repo.get_all()

    def put_map_region(self, region_id: int, **kwargs) -> MapRegion | None:
        return self.map_region_repo.update(region_id, kwargs)

    def delete_map_region(self, region_id: int) -> bool:
        return self.map_region_repo.delete(region_id)

    # =========================================================================
    # DESCRIPTION
    # =========================================================================

    def post_description(
        self,
        entity_type: str,
        entity_id: int,
        content: str,
        title: str = None,
        order_index: int = 0,
        image_url: str = None
    ) -> Description:
        description = Description(
            entity_type=entity_type,
            entity_id=entity_id,
            content=content,
            title=title,
            order_index=order_index,
            image_url=image_url
        )
        self.description_repo.add(description)
        return description

    def get_description(self, description_id: int) -> Description | None:
        return self.description_repo.get(description_id)

    def get_descriptions_by_entity(self, entity_type: str, entity_id: int) -> list[Description]:
        return self.description_repo.get_by_entity(entity_type, entity_id)

    def put_description(self, description_id: int, **kwargs) -> Description | None:
        return self.description_repo.update(description_id, kwargs)

    def delete_description(self, description_id: int) -> bool:
        return self.description_repo.delete(description_id)

    def delete_all_descriptions_for_entity(self, entity_type: str, entity_id: int) -> int:
        return self.description_repo.delete_all_by_entity(entity_type, entity_id)

    # =========================================================================
    # CHARACTER
    # =========================================================================

    def post_character(
        self,
        name: str,
        short_description: str,
        race_id: int,
        profession_id: int,
        gender: str = None,
        birth_date: int = None,
        death_date: int = None,
        birth_place_id: int = None,
        death_place_id: int = None,
        culture_id: int = None,
        citation: str = None,
        image_url: str = None
    ) -> Character:
        character = Character(
            name=name,
            short_description=short_description,
            race_id=race_id,
            profession_id=profession_id,
            gender=gender,
            birth_date=birth_date,
            death_date=death_date,
            birth_place_id=birth_place_id,
            death_place_id=death_place_id,
            culture_id=culture_id,
            citation=citation,
            image_url=image_url
        )
        self.character_repo.add(character)
        return character

    def get_character(self, character_id: int) -> Character | None:
        return self.character_repo.get(character_id)

    def get_all_characters(self) -> list[Character]:
        return self.character_repo.get_all()

    def get_characters_by_race(self, race_id: int) -> list[Character]:
        return self.character_repo.get_by_race(race_id)

    def get_characters_by_profession(self, profession_id: int) -> list[Character]:
        return self.character_repo.get_by_profession(profession_id)

    def get_characters_by_culture(self, culture_id: int) -> list[Character]:
        return self.character_repo.get_by_culture(culture_id)

    def put_character(self, character_id: int, **kwargs) -> Character | None:
        return self.character_repo.update(character_id, kwargs)

    def delete_character(self, character_id: int) -> bool:
        return self.character_repo.delete(character_id)

    # =========================================================================
    # CHARACTER <-> ORGANISATION
    # =========================================================================

    def add_character_to_organisation(
        self,
        character_id: int,
        organisation_id: int,
        role: str = None
    ) -> CharacterOrganisation:
        link = CharacterOrganisation(
            character_id=character_id,
            organisation_id=organisation_id,
            role=role
        )
        self.character_org_repo.add(link)
        return link

    def get_organisations_by_character(self, character_id: int) -> list[CharacterOrganisation]:
        return self.character_org_repo.get_by_character(character_id)

    def get_characters_by_organisation(self, organisation_id: int) -> list[CharacterOrganisation]:
        return self.character_org_repo.get_by_organisation(organisation_id)

    def update_character_role_in_organisation(
        self,
        character_id: int,
        organisation_id: int,
        new_role: str
    ) -> CharacterOrganisation | None:
        link = self.character_org_repo.get_link(character_id, organisation_id)
        if not link:
            return None
        return self.character_org_repo.update(link.id, {'role': new_role})

    def remove_character_from_organisation(self, character_id: int, organisation_id: int) -> bool:
        link = self.character_org_repo.get_link(character_id, organisation_id)
        if not link:
            return False
        return self.character_org_repo.delete(link.id)

# -------------------- Authentification de l'utilisateur --------------------

    def create_user(self, user_data):
        """
        Crée un nouvel utilisateur et le sauvegarde dans la base de données.
        Code Erreur:
            ValueError: Si l'email existe déjà, si le mot de passe est manquant
                        ou si une erreur survient lors de la création.
        """
        # Vérifie si l'email existe déjà
        existing_user = self.user_repo.get_user_by_email(user_data.get('email'))
        if existing_user:
            raise ValueError(f"Un utilisateur avec l'email {user_data['email']} existe déjà.")
        # Si l'email n'existe pas, on créé un utilisateur
        if not user_data.get('password'):
            raise ValueError("Le mot de passe est requis pour la création de l'utilisateur.")
        # Si l'email n'existe pas, on créé un utilisateur
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def login_user(self, email, password):
        """
        Authentifie un utilisateur avec son email et mot de passe.

        Code Erreur:
            ValueError: Si l'email ou le mot de passe est incorrect ou manquant.
        """
        try:
            # Validation des paramètres
            if not email or not password:
                raise ValueError("Email et mot de passe sont requis.")
            # Recherche l'utilisateur
            user = self.user_repo.get_user_by_email(email)
            if not user:
                raise ValueError("Email ou mot de passe incorrect.")
            # Vérifie le mot de passe
            if not user.verify_password(password):
                raise ValueError("Email ou mot de passe incorrect.")
            return user

        except ValueError:
            raise

        except Exception as e:
            raise ValueError(f"Erreur lors de la connexion : {str(e)}")

    def get_users(self, user_id):
        """
        On retourne un utilisateur par son ID
        Code Erreur:
            ValueError: Si aucun utilisateur n'est trouvé avec l'ID fourni.
        """
        try:
            user = self.user_repo.get(user_id)
            if not user:
                raise ValueError(f"Aucun utilisateur trouvé avec l'ID {user_id}.")
            return user

        except ValueError:
            raise

        except Exception as e:
            raise ValueError(f"Erreur lors de la récupération de l'utilisateur : {str(e)}")

    def get_user_by_email(self, email):
        """ 
        Récupère un utilisateur à partir de son email.
        Code Erreur:
            ValueError: Si l'email est vide ou aucun utilisateur n'est trouvé.
        """
        try:
            if not email:
                raise ValueError("L'email ne peut pas être vide.")
            user = self.user_repo.get_user_by_email(email)
            if not user:
                raise ValueError(f"Aucun utilisateur trouvé avec l'email {email}.")
            return user
        except ValueError:
            raise

        except Exception as e:
            raise ValueError(f"Erreur lors de la recherche par email : {str(e)}")

    def get_user_by_id(self, user_id):
        """Récupère un utilisateur par son identifiant unique"""
        try:
            if not user_id:
                raise ValueError("L'identifiant utilisateur est requis.")
            user = self.user_repo.get_by_attribute('id', user_id)
            if not user:
                raise ValueError(f"Aucun utilisateur trouvé avec l'id {user_id}.")
            return user
        except ValueError:
            raise
        except Exception as e:
            raise ValueError(f"Erreur lors de la recherche par ID : {str(e)}")
