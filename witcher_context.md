# Projet The Witcher — Contexte & État d'avancement

## Stack technique

| Couche    | Techno                                      |
|-----------|---------------------------------------------|
| Back      | Python + Flask + Flask-RESTX                |
| ORM       | SQLAlchemy + Flask-SQLAlchemy               |
| DB        | PostgreSQL + PostGIS (géométries carte)     |
| Auth      | Flask-JWT-Extended + Flask-Bcrypt           |
| Carte     | Leaflet (à intégrer côté front)             |
| Front     | Non décidé (React ou Svelte)                |

---

## Architecture du projet

```
backend/
├── app/
│   ├── __init__.py              ← create_app() + enregistrement namespaces
│   ├── facade.py                ← Orchestre les repositories, pas de db.session
│   │
│   ├── models/                  ← SQLAlchemy (héritent de BaseModel)
│   │   ├── basemodel.py         ← id, image_url, created_at, updated_at, save()
│   │   ├── user.py
│   │   ├── character.py
│   │   ├── character_organisation.py
│   │   ├── culture.py
│   │   ├── culture_type.py
│   │   ├── description.py       ← générique : entity_type + entity_id
│   │   ├── map_marker.py        ← géométrie POINT PostGIS (SRID=0)
│   │   ├── map_region.py        ← géométrie POLYGON PostGIS (SRID=0)
│   │   ├── object.py
│   │   ├── object_type.py
│   │   ├── organisation.py
│   │   ├── organisation_type.py
│   │   ├── place.py
│   │   ├── places_relation.py
│   │   ├── profession.py
│   │   ├── race.py
│   │   ├── race_trait.py
│   │   ├── race_type.py
│   │   └── relation_type.py
│   │
│   ├── persistence/             ← Repositories (tout db.session est ici)
│   │   ├── repository.py        ← Repository(ABC) + SQLAlchemyRepository
│   │   │                           méthodes : add, get, get_all, get_by_attribute,
│   │   │                                      update, delete
│   │   ├── user_repository.py   ← get_user_by_email, email_exists,
│   │   │                           get_all_admins, get_all_regular_users
│   │   ├── character_repository.py
│   │   │                        ← get_by_name, get_by_race, get_by_profession,
│   │   │                           get_by_culture, get_by_birth_place, get_alive
│   │   ├── character_organisation_repository.py
│   │   │                        ← get_by_character, get_by_organisation,
│   │   │                           get_link, get_by_role
│   │   ├── place_repository.py  ← get_by_title, get_by_type,
│   │   │                           get_children, get_root_places
│   │   ├── places_relation_repository.py
│   │   │                        ← RelationTypeRepository + PlacesRelationRepository
│   │   │                           get_by_place, get_by_related_place,
│   │   │                           get_all_for_place, get_by_relation_type
│   │   ├── race_repository.py   ← RaceTypeRepository + RaceRepository
│   │   │                           + RaceTraitRepository
│   │   ├── organisation_repository.py
│   │   │                        ← OrganisationTypeRepository + OrganisationRepository
│   │   ├── culture_repository.py
│   │   │                        ← CultureTypeRepository + CultureRepository
│   │   │                           get_children, get_root_cultures
│   │   ├── object_repository.py ← ObjectTypeRepository + ObjectRepository
│   │   ├── profession_repository.py
│   │   │                        ← get_by_name, name_exists
│   │   ├── description_repository.py
│   │   │                        ← get_by_entity (trié order_index),
│   │   │                           get_by_entity_and_order,
│   │   │                           delete_all_by_entity
│   │   └── map_repository.py    ← MapMarkerRepository + MapRegionRepository
│   │                               get_by_place, get_by_type, get_without_place
│   │
│   ├── services/                ← Logique métier spécifique
│   │   └── user_service.py      ← register, login, get_current_user,
│   │                               refresh_token
│   │
│   └── api/                     ← Namespaces Flask-RESTX
│       ├── ns_auth.py           ← /api/auth + décorateur admin_required
│       ├── ns_character.py      ← /api/characters
│       ├── ns_place.py          ← /api/places
│       ├── ns_race.py           ← /api/races
│       ├── ns_misc.py           ← /api/organisations /api/cultures
│       │                           /api/professions /api/objects
│       └── ns_map_description.py← /api/map + /api/descriptions
│
├── config.py
├── .env
├── .env.test
└── run.py
```

---

## Règles d'architecture

- **models/** → représentation des tables, `to_dict()`, validations `@validates`
- **persistence/** → tout `db.session` est ici, jamais ailleurs
- **services/** → logique métier qui ne rentre pas dans la Facade (auth, etc.)
- **facade.py** → instancie tous les repos dans `__init__`, délègue sans toucher à `db.session`
- **api/** → routes HTTP uniquement, appelle la Facade ou les Services

---

## Authentification

- `POST /api/auth/register` — public
- `POST /api/auth/login` — retourne `access_token` + `refresh_token`
- `GET  /api/auth/me` — `@jwt_required()`
- `POST /api/auth/refresh` — `@jwt_required(refresh=True)`

**Règle de protection des routes :**
```python
# GET → public (aucun décorateur)
# POST / PUT / DELETE → admin seulement
@jwt_required()   # toujours en premier
@admin_required   # lit les claims JWT, doit venir après
```
`admin_required` est défini dans `ns_auth.py` et importé dans tous les namespaces.

---

## Carte interactive

- Géométries stockées en PostGIS avec **SRID=0** (carte custom, pas de projection géo réelle)
- `MapMarker` → `GEOMETRY(POINT, 0)` — sérialisé en `{x, y}` via `geoalchemy2.shape.to_shape()`
- `MapRegion` → `GEOMETRY(POLYGON, 0)` — sérialisé en `[[x1,y1],[x2,y2],...]`
- Lib front retenue : **Leaflet**
- ⚠️ Leaflet attend `[lat, lng]` = `[y, x]` — inverser x/y côté front
- Les marqueurs/régions sont liés à `places` via `place_id`
- Cliquer un marqueur → appelle `GET /api/places/<id>` pour charger la fiche

**to_dict() à ajouter sur les modèles map :**
```python
# map_marker.py
from geoalchemy2.shape import to_shape

def to_dict(self):
    data = super().to_dict()
    point = to_shape(self.location)
    data.update({'name': self.name, 'type': self.type,
                 'place_id': self.place_id, 'x': point.x, 'y': point.y})
    return data

# map_region.py
def to_dict(self):
    data = super().to_dict()
    polygon = to_shape(self.shape_data)
    coordinates = [[x, y] for x, y in polygon.exterior.coords]
    data.update({'name': self.name, 'place_id': self.place_id,
                 'coordinates': coordinates})
    return data
```

---

## Routes disponibles

| Namespace      | Méthode | Route                                              | Auth     |
|----------------|---------|----------------------------------------------------|----------|
| auth           | POST    | /api/auth/register                                 | public   |
| auth           | POST    | /api/auth/login                                    | public   |
| auth           | GET     | /api/auth/me                                       | jwt      |
| auth           | POST    | /api/auth/refresh                                  | refresh  |
| characters     | GET     | /api/characters/                                   | public   |
| characters     | POST    | /api/characters/                                   | admin    |
| characters     | GET     | /api/characters/<id>                               | public   |
| characters     | PUT     | /api/characters/<id>                               | admin    |
| characters     | DELETE  | /api/characters/<id>                               | admin    |
| characters     | GET     | /api/characters/race/<id>                          | public   |
| characters     | GET     | /api/characters/profession/<id>                    | public   |
| characters     | GET     | /api/characters/culture/<id>                       | public   |
| characters     | GET     | /api/characters/<id>/organisations                 | public   |
| characters     | POST    | /api/characters/<id>/organisations                 | admin    |
| characters     | PUT     | /api/characters/<id>/organisations/<org_id>        | admin    |
| characters     | DELETE  | /api/characters/<id>/organisations/<org_id>        | admin    |
| places         | GET     | /api/places/ (?type=)                              | public   |
| places         | POST    | /api/places/                                       | admin    |
| places         | GET     | /api/places/roots                                  | public   |
| places         | GET     | /api/places/<id>                                   | public   |
| places         | PUT     | /api/places/<id>                                   | admin    |
| places         | DELETE  | /api/places/<id>                                   | admin    |
| places         | GET     | /api/places/<id>/children                          | public   |
| places         | GET     | /api/places/<id>/relations                         | public   |
| places         | POST    | /api/places/<id>/relations                         | admin    |
| places         | DELETE  | /api/places/relations/<id>                         | admin    |
| races          | GET     | /api/races/                                        | public   |
| races          | POST    | /api/races/                                        | admin    |
| races          | GET/PUT/DELETE | /api/races/<id>                             | —        |
| races          | GET     | /api/races/<id>/traits                             | public   |
| races          | POST    | /api/races/<id>/traits                             | admin    |
| races          | PUT/DELETE | /api/races/traits/<id>                          | admin    |
| races          | GET     | /api/races/types                                   | public   |
| races          | POST    | /api/races/types                                   | admin    |
| races          | GET/PUT/DELETE | /api/races/types/<id>                       | —        |
| organisations  | GET     | /api/organisations/ (?type_id=)                    | public   |
| organisations  | POST    | /api/organisations/                                | admin    |
| organisations  | GET/<id>/characters | /api/organisations/...                  | public   |
| cultures       | GET     | /api/cultures/ (?type_id= ?parent_id=)             | public   |
| cultures       | POST    | /api/cultures/                                     | admin    |
| professions    | GET     | /api/professions/                                  | public   |
| professions    | POST    | /api/professions/                                  | admin    |
| objects        | GET     | /api/objects/ (?type_id=)                          | public   |
| objects        | POST    | /api/objects/                                      | admin    |
| map            | GET     | /api/map/markers (?type= ?place_id=)               | public   |
| map            | POST    | /api/map/markers                                   | admin    |
| map            | GET     | /api/map/markers/<id>                              | public   |
| map            | PUT/DELETE | /api/map/markers/<id>                           | admin    |
| map            | GET     | /api/map/regions                                   | public   |
| map            | POST    | /api/map/regions                                   | admin    |
| map            | GET/PUT/DELETE | /api/map/regions/<id>                       | —        |
| descriptions   | GET     | /api/descriptions/<entity_type>/<entity_id>        | public   |
| descriptions   | POST    | /api/descriptions/<entity_type>/<entity_id>        | admin    |
| descriptions   | DELETE  | /api/descriptions/<entity_type>/<entity_id>        | admin    |
| descriptions   | PUT/DELETE | /api/descriptions/<id>                          | admin    |

---

## Ce qui reste à faire

- [ ] Choisir React ou Svelte pour le front
- [ ] Intégrer Leaflet avec carte custom (image du monde Witcher)
- [ ] Brancher les marqueurs/régions depuis l'API map
- [ ] Interface d'administration (formulaires pour ajouter personnages, lieux, etc.)
- [ ] Pagination sur les listes (get_all_characters, etc.) si le contenu grossit
- [ ] Tests unitaires sur les repositories et la Facade
