"""
Namespace RESTX pour les races, types de races et traits.
GET         → public
POST/PUT/DELETE → admin uniquement
"""
from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from backend.app.facade import Facade
from backend.app.api.ns_auth import admin_required

api = Namespace('races', description='Opérations sur les races', path='/api/races')

facade = Facade()

# ---------------------------------------------------------------------------
# Modèles Swagger
# ---------------------------------------------------------------------------

race_model = api.model('Race', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(required=True),
    'short_description': fields.String(required=True),
    'citation': fields.String(),
    'image_url': fields.String(),
    'race_type_id': fields.Integer(required=True),
    'created_at': fields.String(readonly=True),
    'updated_at': fields.String(readonly=True),
})

race_input = api.model('RaceInput', {
    'name': fields.String(required=True),
    'short_description': fields.String(required=True),
    'citation': fields.String(),
    'image_url': fields.String(),
    'race_type_id': fields.Integer(required=True),
})

race_type_model = api.model('RaceType', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(required=True),
    'short_description': fields.String(),
    'citation': fields.String(),
    'image_url': fields.String(),
    'parent_id': fields.Integer(),
})

race_type_input = api.model('RaceTypeInput', {
    'name': fields.String(required=True),
    'short_description': fields.String(),
    'citation': fields.String(),
    'image_url': fields.String(),
    'parent_id': fields.Integer(),
})

race_trait_model = api.model('RaceTrait', {
    'id': fields.Integer(readonly=True),
    'trait': fields.String(required=True),
    'category': fields.String(),
    'image_url': fields.String(),
    'race_id': fields.Integer(readonly=True),
})

race_trait_input = api.model('RaceTraitInput', {
    'trait': fields.String(required=True),
    'category': fields.String(),
    'image_url': fields.String(),
})

# ---------------------------------------------------------------------------
# Routes Race
# ---------------------------------------------------------------------------

@api.route('/')
class RaceList(Resource):

    @api.marshal_list_with(race_model)
    def get(self):
        """Retourne toutes les races. (public)"""
        return facade.get_all_races()

    @jwt_required()
    @admin_required
    @api.expect(race_input, validate=True)
    @api.marshal_with(race_model, code=201)
    def post(self):
        """Crée une nouvelle race. (admin)"""
        return facade.post_race(**request.get_json()), 201


@api.route('/<int:race_id>')
class RaceDetail(Resource):

    @api.marshal_with(race_model)
    @api.response(404, 'Race introuvable')
    def get(self, race_id):
        """Retourne une race par son id. (public)"""
        race = facade.get_race(race_id)
        if not race:
            api.abort(404, 'Race introuvable')
        return race

    @jwt_required()
    @admin_required
    @api.expect(race_input)
    @api.marshal_with(race_model)
    def put(self, race_id):
        """Met à jour une race. (admin)"""
        race = facade.put_race(race_id, **request.get_json())
        if not race:
            api.abort(404, 'Race introuvable')
        return race

    @jwt_required()
    @admin_required
    @api.response(204, 'Race supprimée')
    def delete(self, race_id):
        """Supprime une race. (admin)"""
        if not facade.delete_race(race_id):
            api.abort(404, 'Race introuvable')
        return '', 204


@api.route('/<int:race_id>/traits')
class RaceTraits(Resource):

    @api.marshal_list_with(race_trait_model)
    def get(self, race_id):
        """Retourne tous les traits d'une race. (public)"""
        return facade.get_traits_by_race(race_id)

    @jwt_required()
    @admin_required
    @api.expect(race_trait_input, validate=True)
    @api.marshal_with(race_trait_model, code=201)
    def post(self, race_id):
        """Ajoute un trait à une race. (admin)"""
        return facade.post_race_trait(race_id=race_id, **request.get_json()), 201


@api.route('/traits/<int:trait_id>')
class RaceTraitDetail(Resource):

    @jwt_required()
    @admin_required
    @api.expect(race_trait_input)
    @api.marshal_with(race_trait_model)
    def put(self, trait_id):
        """Met à jour un trait. (admin)"""
        trait = facade.put_race_trait(trait_id, **request.get_json())
        if not trait:
            api.abort(404, 'Trait introuvable')
        return trait

    @jwt_required()
    @admin_required
    @api.response(204, 'Trait supprimé')
    def delete(self, trait_id):
        """Supprime un trait. (admin)"""
        if not facade.delete_race_trait(trait_id):
            api.abort(404, 'Trait introuvable')
        return '', 204


# ---------------------------------------------------------------------------
# Routes Race Type
# ---------------------------------------------------------------------------

@api.route('/types')
class RaceTypeList(Resource):

    @api.marshal_list_with(race_type_model)
    def get(self):
        """Retourne tous les types de races. (public)"""
        return facade.get_all_race_types()

    @jwt_required()
    @admin_required
    @api.expect(race_type_input, validate=True)
    @api.marshal_with(race_type_model, code=201)
    def post(self):
        """Crée un nouveau type de race. (admin)"""
        return facade.post_race_type(**request.get_json()), 201


@api.route('/types/<int:race_type_id>')
class RaceTypeDetail(Resource):

    @api.marshal_with(race_type_model)
    @api.response(404, 'Type de race introuvable')
    def get(self, race_type_id):
        """Retourne un type de race. (public)"""
        race_type = facade.get_race_type(race_type_id)
        if not race_type:
            api.abort(404, 'Type de race introuvable')
        return race_type

    @jwt_required()
    @admin_required
    @api.expect(race_type_input)
    @api.marshal_with(race_type_model)
    def put(self, race_type_id):
        """Met à jour un type de race. (admin)"""
        race_type = facade.put_race_type(race_type_id, **request.get_json())
        if not race_type:
            api.abort(404, 'Type de race introuvable')
        return race_type

    @jwt_required()
    @admin_required
    @api.response(204, 'Type supprimé')
    def delete(self, race_type_id):
        """Supprime un type de race. (admin)"""
        if not facade.delete_race_type(race_type_id):
            api.abort(404, 'Type de race introuvable')
        return '', 204
