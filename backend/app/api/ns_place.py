"""
Namespace RESTX pour les lieux (places).
GET         → public
POST/PUT/DELETE → admin uniquement
"""
from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from backend.app.facade import Facade
from backend.app.api.ns_auth import admin_required

api = Namespace('places', description='Opérations sur les lieux', path='/api/places')

facade = Facade()

# ---------------------------------------------------------------------------
# Modèles Swagger
# ---------------------------------------------------------------------------

place_model = api.model('Place', {
    'id': fields.Integer(readonly=True),
    'title': fields.String(required=True),
    'type_place': fields.String(required=True),
    'short_description': fields.String(required=True),
    'image_url': fields.String(),
    'parent_id': fields.Integer(),
    'created_at': fields.String(readonly=True),
    'updated_at': fields.String(readonly=True),
})

place_input = api.model('PlaceInput', {
    'title': fields.String(required=True),
    'type_place': fields.String(required=True),
    'short_description': fields.String(required=True),
    'image_url': fields.String(),
    'parent_id': fields.Integer(),
})

place_relation_input = api.model('PlaceRelationInput', {
    'related_place_id': fields.Integer(required=True),
    'relation_type_id': fields.Integer(required=True),
})

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@api.route('/')
class PlaceList(Resource):

    @api.marshal_list_with(place_model)
    def get(self):
        """Retourne tous les lieux. Filtre optionnel : ?type=royaume (public)"""
        type_filter = request.args.get('type')
        if type_filter:
            return facade.get_places_by_type(type_filter)
        return facade.get_all_places()

    @jwt_required()
    @admin_required
    @api.expect(place_input, validate=True)
    @api.marshal_with(place_model, code=201)
    def post(self):
        """Crée un nouveau lieu. (admin)"""
        return facade.post_place(**request.get_json()), 201


@api.route('/roots')
class RootPlaces(Resource):
    @api.marshal_list_with(place_model)
    def get(self):
        """Retourne les lieux racines (sans parent). (public)"""
        return facade.get_root_places()


@api.route('/<int:place_id>')
class PlaceDetail(Resource):

    @api.marshal_with(place_model)
    @api.response(404, 'Lieu introuvable')
    def get(self, place_id):
        """Retourne un lieu par son id. (public)"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, 'Lieu introuvable')
        return place

    @jwt_required()
    @admin_required
    @api.expect(place_input)
    @api.marshal_with(place_model)
    def put(self, place_id):
        """Met à jour un lieu. (admin)"""
        place = facade.put_place(place_id, **request.get_json())
        if not place:
            api.abort(404, 'Lieu introuvable')
        return place

    @jwt_required()
    @admin_required
    @api.response(204, 'Lieu supprimé')
    def delete(self, place_id):
        """Supprime un lieu. (admin)"""
        if not facade.delete_place(place_id):
            api.abort(404, 'Lieu introuvable')
        return '', 204


@api.route('/<int:place_id>/children')
class PlaceChildren(Resource):
    @api.marshal_list_with(place_model)
    def get(self, place_id):
        """Retourne les lieux enfants. (public)"""
        return facade.get_children_places(place_id)


@api.route('/<int:place_id>/relations')
class PlaceRelations(Resource):

    def get(self, place_id):
        """Retourne toutes les relations d'un lieu. (public)"""
        return [r.to_dict() for r in facade.get_relations_by_place(place_id)]

    @jwt_required()
    @admin_required
    @api.expect(place_relation_input, validate=True)
    def post(self, place_id):
        """Crée une relation entre deux lieux. (admin)"""
        data = request.get_json()
        relation = facade.post_place_relation(
            place_id=place_id,
            related_place_id=data['related_place_id'],
            relation_type_id=data['relation_type_id']
        )
        return relation.to_dict(), 201


@api.route('/relations/<int:relation_id>')
class PlaceRelationDetail(Resource):

    @jwt_required()
    @admin_required
    @api.response(204, 'Relation supprimée')
    def delete(self, relation_id):
        """Supprime une relation entre deux lieux. (admin)"""
        if not facade.delete_place_relation(relation_id):
            api.abort(404, 'Relation introuvable')
        return '', 204
