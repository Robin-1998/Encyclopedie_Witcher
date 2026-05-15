# L'encyclopédie sur l'univers de The Witcher

[![Flask](https://img.shields.io/badge/Flask-2.3+-blue.svg)](https://flask.palletsprojects.com/)
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://reactjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-316192.svg)](https://www.postgresql.org/)
[![PostGIS](https://img.shields.io/badge/PostGIS-3.0+-green.svg)](https://postgis.net/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Ceci est un projet personnel réalisé dans le but de faire découvrir cette univers par le biais d'un site web immersif et de rendre honneur à cette univers tellement fantastique

## Fonctionalités
Frontend : Svelte + Svelte kit + css + vite
backend : python + fastapi
Intelligence artificielle : Ollama

### 🗺️ Carte interactive
- Certaine page sur les lieux principaux regroupe des carte interactives qui permet d'avoir une visible plus fluide entre les différentes ville d'une région
- Affichage des points d'intérêts via des marqueurs

### 📚 Encyclopédie
- Vitrine des différents personnages, races, profession, culture, lieux.
- Possibilité d'avoir une description de chaque élément de la vitrine

# Structure du projet The Witcher

```
backend/
├── app/
│   ├── __init__.py                  ← create_app + enregistrement namespaces
│   │
│   ├── models/                      ← Modèles SQLAlchemy
│   │   ├── basemodel.py
│   │   ├── character.py
│   │   ├── character_organisation.py
│   │   ├── culture.py
│   │   ├── culture_type.py
│   │   ├── description.py
│   │   ├── map_marker.py
│   │   ├── map_region.py
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
│   │   ├── relation_type.py
│   │   └── user.py
│   │
│   ├── persistence/                 ← Repositories (accès DB)
│   │   ├── repository.py            ← Repository (ABC) + SQLAlchemyRepository
│   │   ├── user_repository.py
│   │   ├── character_repository.py
│   │   ├── character_organisation_repository.py
│   │   ├── place_repository.py
│   │   ├── places_relation_repository.py  ← RelationTypeRepository aussi
│   │   ├── race_repository.py             ← RaceType + RaceTrait aussi
│   │   ├── organisation_repository.py     ← OrganisationType aussi
│   │   ├── culture_repository.py          ← CultureType aussi
│   │   ├── object_repository.py           ← ObjectType aussi
│   │   ├── profession_repository.py
│   │   ├── description_repository.py
│   │   └── map_repository.py              ← MapMarker + MapRegion
│   │
│   ├── facade.py                    ← Facade (orchestre les repositories)
│   │
│   └── api/                         ← Namespaces Flask-RESTX
│       ├── ns_character.py          ← /api/characters
│       ├── ns_place.py              ← /api/places
│       ├── ns_race.py               ← /api/races + /api/races/types
│       ├── ns_misc.py               ← /api/organisations /api/cultures
│       │                                /api/professions /api/objects
│       ├── ns_map_description.py    ← /api/map + /api/descriptions
│       └── (ns_auth.py)             ← /api/auth  ← à créer (login/register)
│
├── config.py
├── .env
├── .env.test
└── run.py
```

## Résumé des routes disponibles

| Namespace        | Routes principales                                                  |
|------------------|---------------------------------------------------------------------|
| characters       | GET/POST /api/characters/                                           |
|                  | GET/PUT/DELETE /api/characters/<id>                                 |
|                  | GET /api/characters/race/<id>                                       |
|                  | GET /api/characters/profession/<id>                                 |
|                  | GET /api/characters/culture/<id>                                    |
|                  | GET/POST /api/characters/<id>/organisations                         |
|                  | PUT/DELETE /api/characters/<id>/organisations/<org_id>              |
| places           | GET/POST /api/places/                                               |
|                  | GET/PUT/DELETE /api/places/<id>                                     |
|                  | GET /api/places/roots                                               |
|                  | GET /api/places/<id>/children                                       |
|                  | GET/POST /api/places/<id>/relations                                 |
|                  | DELETE /api/places/relations/<id>                                   |
| races            | GET/POST /api/races/                                                |
|                  | GET/PUT/DELETE /api/races/<id>                                      |
|                  | GET/POST /api/races/<id>/traits                                     |
|                  | PUT/DELETE /api/races/traits/<id>                                   |
|                  | GET/POST /api/races/types                                           |
|                  | GET/PUT/DELETE /api/races/types/<id>                                |
| organisations    | GET/POST /api/organisations/                                        |
|                  | GET/PUT/DELETE /api/organisations/<id>                              |
|                  | GET /api/organisations/<id>/characters                              |
|                  | GET/POST/PUT/DELETE /api/organisations/types/...                    |
| cultures         | GET/POST /api/cultures/  (?type_id= ou ?parent_id=)                |
|                  | GET/PUT/DELETE /api/cultures/<id>                                   |
|                  | GET/POST/PUT/DELETE /api/cultures/types/...                         |
| professions      | GET/POST /api/professions/                                          |
|                  | GET/PUT/DELETE /api/professions/<id>                                |
| objects          | GET/POST /api/objects/  (?type_id=)                                 |
|                  | GET/PUT/DELETE /api/objects/<id>                                    |
|                  | GET/POST/PUT/DELETE /api/objects/types/...                          |
| map              | GET/POST /api/map/markers  (?type= ou ?place_id=)                  |
|                  | GET/PUT/DELETE /api/map/markers/<id>                                |
|                  | GET/POST /api/map/regions                                           |
|                  | GET/PUT/DELETE /api/map/regions/<id>                                |
| descriptions     | GET/POST/DELETE /api/descriptions/<entity_type>/<entity_id>        |
|                  | PUT/DELETE /api/descriptions/<id>                                   |
```
