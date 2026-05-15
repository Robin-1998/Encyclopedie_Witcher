"""
Namespaces RESTX pour :
- Carte interactive (map_marker, map_region)
- Descriptions génériques

GET         → public
POST/PUT/DELETE → admin uniquement
"""
from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from geoalchemy2.elements import WKTElement
from backend.app.facade import Facade
from backend.app.api.ns_auth import admin_required

facade = Facade()

# ===========================================================================
# MAP
# ===========================================================================

map_api = Namespace('map', description='Carte interactive', path='/api/map')

marker_model = map_api.model('MapMarker', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(required=True),
    'type': fields.String(),
    'place_id': fields.Integer(),
    'x': fields.Float(description='Coordonnée X sur la carte'),
    'y': fields.Float(description='Coordonnée Y sur la carte'),
    'created_at': fields.String(readonly=True),
    'updated_at': fields.String(readonly=True),
})

marker_input = map_api.model('MapMarkerInput', {
    'name': fields.String(required=True),
    'type': fields.String(),
    'place_id': fields.Integer(),
    'x': fields.Float(required=True),
    'y': fields.Float(required=True),
})

region_input = map_api.model('MapRegionInput', {
    'name': fields.String(required=True),
    'place_id': fields.Integer(),
    'coordinates': fields.List(
        fields.List(fields.Float),
        required=True,
        description='[[x1,y1],[x2,y2],...] polygone fermé'
    ),
})


def _to_point(x: float, y: float) -> WKTElement:
    return WKTElement(f'POINT({x} {y})', srid=0)


def _to_polygon(coordinates: list) -> WKTElement:
    points = ', '.join(f'{c[0]} {c[1]}' for c in coordinates)
    return WKTElement(f'POLYGON(({points}))', srid=0)


@map_api.route('/markers')
class MapMarkerList(Resource):

    def get(self):
        """Retourne tous les marqueurs. Filtres : ?type=ville ou ?place_id=3 (public)"""
        type_filter = request.args.get('type')
        place_id = request.args.get('place_id', type=int)
        if place_id:
            markers = facade.get_markers_by_place(place_id)
        elif type_filter:
            markers = facade.map_marker_repo.get_by_type(type_filter)
        else:
            markers = facade.get_all_map_markers()
        return [m.to_dict() for m in markers]

    @jwt_required()
    @admin_required
    @map_api.expect(marker_input, validate=True)
    def post(self):
        """Crée un marqueur sur la carte. (admin)"""
        data = request.get_json()
        location = _to_point(data.pop('x'), data.pop('y'))
        marker = facade.post_map_marker(location=location, **data)
        return marker.to_dict(), 201


@map_api.route('/markers/<int:marker_id>')
class MapMarkerDetail(Resource):

    def get(self, marker_id):
        """Retourne un marqueur. (public)"""
        marker = facade.get_map_marker(marker_id)
        if not marker:
            map_api.abort(404, 'Marqueur introuvable')
        return marker.to_dict()

    @jwt_required()
    @admin_required
    def put(self, marker_id):
        """Met à jour un marqueur. (admin)"""
        data = request.get_json()
        if 'x' in data and 'y' in data:
            data['location'] = _to_point(data.pop('x'), data.pop('y'))
        marker = facade.put_map_marker(marker_id, **data)
        if not marker:
            map_api.abort(404, 'Marqueur introuvable')
        return marker.to_dict()

    @jwt_required()
    @admin_required
    @map_api.response(204, 'Marqueur supprimé')
    def delete(self, marker_id):
        """Supprime un marqueur. (admin)"""
        if not facade.delete_map_marker(marker_id):
            map_api.abort(404, 'Marqueur introuvable')
        return '', 204


@map_api.route('/regions')
class MapRegionList(Resource):

    def get(self):
        """Retourne toutes les régions. (public)"""
        return [r.to_dict() for r in facade.get_all_map_regions()]

    @jwt_required()
    @admin_required
    @map_api.expect(region_input, validate=True)
    def post(self):
        """Crée une région polygonale. (admin)"""
        data = request.get_json()
        shape_data = _to_polygon(data.pop('coordinates'))
        region = facade.post_map_region(shape_data=shape_data, **data)
        return region.to_dict(), 201


@map_api.route('/regions/<int:region_id>')
class MapRegionDetail(Resource):

    def get(self, region_id):
        """Retourne une région. (public)"""
        region = facade.get_map_region(region_id)
        if not region:
            map_api.abort(404, 'Région introuvable')
        return region.to_dict()

    @jwt_required()
    @admin_required
    def put(self, region_id):
        """Met à jour une région. (admin)"""
        data = request.get_json()
        if 'coordinates' in data:
            data['shape_data'] = _to_polygon(data.pop('coordinates'))
        region = facade.put_map_region(region_id, **data)
        if not region:
            map_api.abort(404, 'Région introuvable')
        return region.to_dict()

    @jwt_required()
    @admin_required
    @map_api.response(204, 'Région supprimée')
    def delete(self, region_id):
        """Supprime une région. (admin)"""
        if not facade.delete_map_region(region_id):
            map_api.abort(404, 'Région introuvable')
        return '', 204


# ===========================================================================
# DESCRIPTION
# ===========================================================================

description_api = Namespace('descriptions', description='Descriptions par entité', path='/api/descriptions')

description_model = description_api.model('Description', {
    'id': fields.Integer(readonly=True),
    'entity_type': fields.String(required=True),
    'entity_id': fields.Integer(required=True),
    'title': fields.String(),
    'content': fields.String(required=True),
    'order_index': fields.Integer(),
    'image_url': fields.String(),
    'created_at': fields.String(readonly=True),
    'updated_at': fields.String(readonly=True),
})

description_input = description_api.model('DescriptionInput', {
    'title': fields.String(),
    'content': fields.String(required=True),
    'order_index': fields.Integer(),
    'image_url': fields.String(),
})


@description_api.route('/<string:entity_type>/<int:entity_id>')
class DescriptionsByEntity(Resource):

    @description_api.marshal_list_with(description_model)
    def get(self, entity_type, entity_id):
        """Retourne toutes les descriptions d'une entité triées par order_index. (public)"""
        return facade.get_descriptions_by_entity(entity_type, entity_id)

    @jwt_required()
    @admin_required
    @description_api.expect(description_input, validate=True)
    @description_api.marshal_with(description_model, code=201)
    def post(self, entity_type, entity_id):
        """Ajoute une section de description à une entité. (admin)"""
        return facade.post_description(
            entity_type=entity_type,
            entity_id=entity_id,
            **request.get_json()
        ), 201

    @jwt_required()
    @admin_required
    @description_api.response(204, 'Toutes les descriptions supprimées')
    def delete(self, entity_type, entity_id):
        """Supprime toutes les descriptions d'une entité. (admin)"""
        facade.delete_all_descriptions_for_entity(entity_type, entity_id)
        return '', 204


@description_api.route('/<int:description_id>')
class DescriptionDetail(Resource):

    @jwt_required()
    @admin_required
    @description_api.expect(description_input)
    @description_api.marshal_with(description_model)
    def put(self, description_id):
        """Met à jour une description. (admin)"""
        description = facade.put_description(description_id, **request.get_json())
        if not description:
            description_api.abort(404, 'Description introuvable')
        return description

    @jwt_required()
    @admin_required
    @description_api.response(204, 'Description supprimée')
    def delete(self, description_id):
        """Supprime une description. (admin)"""
        if not facade.delete_description(description_id):
            description_api.abort(404, 'Description introuvable')
        return '', 204
