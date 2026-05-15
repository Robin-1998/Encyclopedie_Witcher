"""
Namespace RESTX pour les personnages (characters).
GET         → public
POST/PUT/DELETE → admin uniquement
"""
from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from backend.app.facade import Facade
from backend.app.api.ns_auth import admin_required

api = Namespace('characters', description='Opérations sur les personnages', path='/api/characters')

facade = Facade()

# ---------------------------------------------------------------------------
# Modèles Swagger
# ---------------------------------------------------------------------------

character_model = api.model('Character', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(required=True),
    'gender': fields.String(),
    'birth_date': fields.Integer(),
    'death_date': fields.Integer(),
    'short_description': fields.String(required=True),
    'citation': fields.String(),
    'image_url': fields.String(),
    'race_id': fields.Integer(required=True),
    'profession_id': fields.Integer(required=True),
    'culture_id': fields.Integer(),
    'birth_place_id': fields.Integer(),
    'death_place_id': fields.Integer(),
    'created_at': fields.String(readonly=True),
    'updated_at': fields.String(readonly=True),
})

character_input = api.model('CharacterInput', {
    'name': fields.String(required=True),
    'gender': fields.String(),
    'birth_date': fields.Integer(),
    'death_date': fields.Integer(),
    'short_description': fields.String(required=True),
    'citation': fields.String(),
    'image_url': fields.String(),
    'race_id': fields.Integer(required=True),
    'profession_id': fields.Integer(required=True),
    'culture_id': fields.Integer(),
    'birth_place_id': fields.Integer(),
    'death_place_id': fields.Integer(),
})

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@api.route('/')
class CharacterList(Resource):

    @api.marshal_list_with(character_model)
    def get(self):
        """Retourne tous les personnages. (public)"""
        return facade.get_all_characters()

    @jwt_required()
    @admin_required
    @api.expect(character_input, validate=True)
    @api.marshal_with(character_model, code=201)
    def post(self):
        """Crée un nouveau personnage. (admin)"""
        return facade.post_character(**request.get_json()), 201


@api.route('/<int:character_id>')
class CharacterDetail(Resource):

    @api.marshal_with(character_model)
    @api.response(404, 'Personnage introuvable')
    def get(self, character_id):
        """Retourne un personnage par son id. (public)"""
        character = facade.get_character(character_id)
        if not character:
            api.abort(404, 'Personnage introuvable')
        return character

    @jwt_required()
    @admin_required
    @api.expect(character_input)
    @api.marshal_with(character_model)
    @api.response(404, 'Personnage introuvable')
    def put(self, character_id):
        """Met à jour un personnage. (admin)"""
        character = facade.put_character(character_id, **request.get_json())
        if not character:
            api.abort(404, 'Personnage introuvable')
        return character

    @jwt_required()
    @admin_required
    @api.response(204, 'Personnage supprimé')
    @api.response(404, 'Personnage introuvable')
    def delete(self, character_id):
        """Supprime un personnage. (admin)"""
        if not facade.delete_character(character_id):
            api.abort(404, 'Personnage introuvable')
        return '', 204


@api.route('/race/<int:race_id>')
class CharactersByRace(Resource):
    @api.marshal_list_with(character_model)
    def get(self, race_id):
        """Retourne tous les personnages d'une race. (public)"""
        return facade.get_characters_by_race(race_id)


@api.route('/profession/<int:profession_id>')
class CharactersByProfession(Resource):
    @api.marshal_list_with(character_model)
    def get(self, profession_id):
        """Retourne tous les personnages d'une profession. (public)"""
        return facade.get_characters_by_profession(profession_id)


@api.route('/culture/<int:culture_id>')
class CharactersByCulture(Resource):
    @api.marshal_list_with(character_model)
    def get(self, culture_id):
        """Retourne tous les personnages d'une culture. (public)"""
        return facade.get_characters_by_culture(culture_id)


@api.route('/<int:character_id>/organisations')
class CharacterOrganisations(Resource):

    def get(self, character_id):
        """Retourne toutes les organisations d'un personnage. (public)"""
        return [l.to_dict() for l in facade.get_organisations_by_character(character_id)]

    @jwt_required()
    @admin_required
    def post(self, character_id):
        """Ajoute un personnage à une organisation. (admin)"""
        data = request.get_json()
        link = facade.add_character_to_organisation(
            character_id=character_id,
            organisation_id=data['organisation_id'],
            role=data.get('role')
        )
        return link.to_dict(), 201


@api.route('/<int:character_id>/organisations/<int:organisation_id>')
class CharacterOrganisationDetail(Resource):

    @jwt_required()
    @admin_required
    def put(self, character_id, organisation_id):
        """Met à jour le rôle d'un personnage dans une organisation. (admin)"""
        link = facade.update_character_role_in_organisation(
            character_id, organisation_id, request.get_json().get('role')
        )
        if not link:
            api.abort(404, 'Lien introuvable')
        return link.to_dict()

    @jwt_required()
    @admin_required
    def delete(self, character_id, organisation_id):
        """Retire un personnage d'une organisation. (admin)"""
        if not facade.remove_character_from_organisation(character_id, organisation_id):
            api.abort(404, 'Lien introuvable')
        return '', 204
