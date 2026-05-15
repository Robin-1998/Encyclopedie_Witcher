"""
Namespace RESTX pour l'authentification.
Routes : register, login, me, refresh.
Inclut aussi le décorateur admin_required réutilisable sur les autres namespaces.
"""
from functools import wraps
from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from backend.app.services.user_service import UserService

api = Namespace('auth', description='Authentification', path='/api/auth')

service = UserService()

# ---------------------------------------------------------------------------
# Modèles Swagger
# ---------------------------------------------------------------------------

register_input = api.model('RegisterInput', {
    'name': fields.String(required=True, description='Nom affiché'),
    'email': fields.String(required=True, description='Adresse email'),
    'password': fields.String(required=True, description='Mot de passe (min 8 caractères)'),
})

login_input = api.model('LoginInput', {
    'email': fields.String(required=True),
    'password': fields.String(required=True),
})

token_model = api.model('TokenResponse', {
    'access_token': fields.String(),
    'refresh_token': fields.String(),
    'user': fields.Raw(),
})

user_model = api.model('UserResponse', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(),
    'email': fields.String(),
    'is_admin': fields.Boolean(),
    'image_url': fields.String(),
    'created_at': fields.String(readonly=True),
})

# ---------------------------------------------------------------------------
# Décorateur admin_required
# Réutilisable dans les autres namespaces :
#   from backend.app.api.ns_auth import admin_required
#   @admin_required
# ---------------------------------------------------------------------------

def admin_required(fn):
    """
    Décorateur qui vérifie que l'utilisateur est connecté ET admin.
    À placer après @jwt_required() sur les routes protégées.

    Usage :
        @api.route('/sensitive')
        class SensitiveResource(Resource):
            @jwt_required()
            @admin_required
            def delete(self, ...):
                ...
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if not claims.get('is_admin', False):
            api.abort(403, "Accès réservé aux administrateurs.")
        return fn(*args, **kwargs)
    return wrapper


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@api.route('/register')
class Register(Resource):

    @api.expect(register_input, validate=True)
    @api.response(201, 'Compte créé')
    @api.response(400, 'Email déjà utilisé ou données invalides')
    def post(self):
        """Crée un nouveau compte utilisateur."""
        data = request.get_json()
        try:
            user = service.register(
                name=data['name'],
                email=data['email'],
                password=data['password']
            )
            return {'message': 'Compte créé avec succès.', 'user': user}, 201
        except ValueError as e:
            api.abort(400, str(e))


@api.route('/login')
class Login(Resource):

    @api.expect(login_input, validate=True)
    @api.marshal_with(token_model)
    @api.response(401, 'Identifiants incorrects')
    def post(self):
        """Connecte un utilisateur et retourne les tokens JWT."""
        data = request.get_json()
        try:
            result = service.login(
                email=data['email'],
                password=data['password']
            )
            return result
        except ValueError as e:
            api.abort(401, str(e))


@api.route('/me')
class Me(Resource):

    @jwt_required()
    @api.marshal_with(user_model)
    @api.response(401, 'Token manquant ou invalide')
    @api.response(404, 'Utilisateur introuvable')
    def get(self):
        """Retourne les infos de l'utilisateur connecté."""
        user_id = int(get_jwt_identity())
        user = service.get_current_user(user_id)
        if not user:
            api.abort(404, 'Utilisateur introuvable')
        return user


@api.route('/refresh')
class Refresh(Resource):

    @jwt_required(refresh=True)
    @api.response(200, 'Nouveau access token')
    @api.response(404, 'Utilisateur introuvable')
    def post(self):
        """Génère un nouvel access token depuis le refresh token."""
        user_id = int(get_jwt_identity())
        try:
            result = service.refresh_token(user_id)
            return result
        except ValueError as e:
            api.abort(404, str(e))
