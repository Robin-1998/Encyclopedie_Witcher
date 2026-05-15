import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restx import Api
from dotenv import load_dotenv
from config import config
from flask_cors import CORS

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app(config_name=None):
    """Crée et configure l'application Flask selon l'environnement."""

    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    if config_name == "testing":
        env_path = os.path.join(os.path.dirname(__file__), "..", ".env.test")
    else:
        env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    load_dotenv(env_path)

    app = Flask(__name__)
    app.url_map.strict_slashes = False

    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:5173", "http://127.0.0.1:5173"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "expose_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })

    app.config.from_object(config[config_name])

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # -------------------------------------------------------------------------
    # Initialisation Flask-RESTX
    # -------------------------------------------------------------------------
    api = Api(
        app,
        version="1.0",
        title="Witcher API",
        description="Witcher Application API",
        doc="/api/v1/"
    )

    # -------------------------------------------------------------------------
    # Import des namespaces
    # Les imports sont ici (et non en haut du fichier) pour éviter les imports
    # circulaires : les namespaces importent db via la Facade et les modèles,
    # qui eux-mêmes importent db depuis ce fichier.
    # -------------------------------------------------------------------------
    from backend.app.api.ns_auth import api as ns_auth
    from backend.app.api.ns_character import api as ns_character
    from backend.app.api.ns_place import api as ns_place
    from backend.app.api.ns_race import api as ns_race
    from backend.app.api.ns_misc import (
        organisation_api as ns_organisation,
        culture_api as ns_culture,
        profession_api as ns_profession,
        object_api as ns_object,
    )
    from backend.app.api.ns_map_description import (
        map_api as ns_map,
        description_api as ns_description,
    )

    # -------------------------------------------------------------------------
    # Enregistrement des namespaces
    # -------------------------------------------------------------------------
    api.add_namespace(ns_auth)
    api.add_namespace(ns_character)
    api.add_namespace(ns_place)
    api.add_namespace(ns_race)
    api.add_namespace(ns_organisation)
    api.add_namespace(ns_culture)
    api.add_namespace(ns_profession)
    api.add_namespace(ns_object)
    api.add_namespace(ns_map)
    api.add_namespace(ns_description)

    return app
