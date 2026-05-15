"""
Namespaces RESTX pour :
- Organisation + OrganisationType
- Culture + CultureType
- Profession
- Object + ObjectType

GET         → public
POST/PUT/DELETE → admin uniquement
"""
from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from backend.app.facade import Facade
from backend.app.api.ns_auth import admin_required

facade = Facade()

# ===========================================================================
# ORGANISATION
# ===========================================================================

organisation_api = Namespace('organisations', description='Organisations', path='/api/organisations')

org_type_model = organisation_api.model('OrganisationType', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(required=True),
    'image_url': fields.String(),
})

org_model = organisation_api.model('Organisation', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(required=True),
    'short_description': fields.String(),
    'image_url': fields.String(),
    'organisation_type_id': fields.Integer(required=True),
    'created_at': fields.String(readonly=True),
    'updated_at': fields.String(readonly=True),
})

org_input = organisation_api.model('OrganisationInput', {
    'name': fields.String(required=True),
    'short_description': fields.String(),
    'image_url': fields.String(),
    'organisation_type_id': fields.Integer(required=True),
})


@organisation_api.route('/types')
class OrgTypeList(Resource):
    @organisation_api.marshal_list_with(org_type_model)
    def get(self):
        """Retourne tous les types d'organisations. (public)"""
        return facade.get_all_organisation_types()

    @jwt_required()
    @admin_required
    @organisation_api.expect(org_type_model, validate=True)
    @organisation_api.marshal_with(org_type_model, code=201)
    def post(self):
        """Crée un type d'organisation. (admin)"""
        return facade.post_organisation_type(**request.get_json()), 201


@organisation_api.route('/types/<int:org_type_id>')
class OrgTypeDetail(Resource):
    @organisation_api.marshal_with(org_type_model)
    def get(self, org_type_id):
        """Retourne un type d'organisation. (public)"""
        ot = facade.get_organisation_type(org_type_id)
        if not ot:
            organisation_api.abort(404, 'Type introuvable')
        return ot

    @jwt_required()
    @admin_required
    def put(self, org_type_id):
        """Met à jour un type d'organisation. (admin)"""
        ot = facade.put_organisation_type(org_type_id, **request.get_json())
        if not ot:
            organisation_api.abort(404, 'Type introuvable')
        return ot.to_dict()

    @jwt_required()
    @admin_required
    def delete(self, org_type_id):
        """Supprime un type d'organisation. (admin)"""
        if not facade.delete_organisation_type(org_type_id):
            organisation_api.abort(404, 'Type introuvable')
        return '', 204


@organisation_api.route('/')
class OrganisationList(Resource):
    @organisation_api.marshal_list_with(org_model)
    def get(self):
        """Retourne toutes les organisations. Filtre optionnel : ?type_id=1 (public)"""
        type_id = request.args.get('type_id', type=int)
        if type_id:
            return facade.get_organisations_by_type(type_id)
        return facade.get_all_organisations()

    @jwt_required()
    @admin_required
    @organisation_api.expect(org_input, validate=True)
    @organisation_api.marshal_with(org_model, code=201)
    def post(self):
        """Crée une organisation. (admin)"""
        return facade.post_organisation(**request.get_json()), 201


@organisation_api.route('/<int:organisation_id>')
class OrganisationDetail(Resource):
    @organisation_api.marshal_with(org_model)
    def get(self, organisation_id):
        """Retourne une organisation. (public)"""
        org = facade.get_organisation(organisation_id)
        if not org:
            organisation_api.abort(404, 'Organisation introuvable')
        return org

    @jwt_required()
    @admin_required
    def put(self, organisation_id):
        """Met à jour une organisation. (admin)"""
        org = facade.put_organisation(organisation_id, **request.get_json())
        if not org:
            organisation_api.abort(404, 'Organisation introuvable')
        return org.to_dict()

    @jwt_required()
    @admin_required
    def delete(self, organisation_id):
        """Supprime une organisation. (admin)"""
        if not facade.delete_organisation(organisation_id):
            organisation_api.abort(404, 'Organisation introuvable')
        return '', 204


@organisation_api.route('/<int:organisation_id>/characters')
class OrganisationCharacters(Resource):
    def get(self, organisation_id):
        """Retourne tous les membres d'une organisation. (public)"""
        links = facade.get_characters_by_organisation(organisation_id)
        return [l.to_dict() for l in links]


# ===========================================================================
# CULTURE
# ===========================================================================

culture_api = Namespace('cultures', description='Cultures', path='/api/cultures')

culture_type_model = culture_api.model('CultureType', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(required=True),
    'image_url': fields.String(),
})

culture_model = culture_api.model('Culture', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(required=True),
    'short_description': fields.String(),
    'image_url': fields.String(),
    'culture_type_id': fields.Integer(required=True),
    'parent_culture_id': fields.Integer(),
    'created_at': fields.String(readonly=True),
    'updated_at': fields.String(readonly=True),
})

culture_input = culture_api.model('CultureInput', {
    'name': fields.String(required=True),
    'short_description': fields.String(),
    'image_url': fields.String(),
    'culture_type_id': fields.Integer(required=True),
    'parent_culture_id': fields.Integer(),
})


@culture_api.route('/types')
class CultureTypeList(Resource):
    @culture_api.marshal_list_with(culture_type_model)
    def get(self):
        """Retourne tous les types de cultures. (public)"""
        return facade.get_all_culture_types()

    @jwt_required()
    @admin_required
    @culture_api.expect(culture_type_model, validate=True)
    @culture_api.marshal_with(culture_type_model, code=201)
    def post(self):
        """Crée un type de culture. (admin)"""
        return facade.post_culture_type(**request.get_json()), 201


@culture_api.route('/types/<int:culture_type_id>')
class CultureTypeDetail(Resource):
    @culture_api.marshal_with(culture_type_model)
    def get(self, culture_type_id):
        """Retourne un type de culture. (public)"""
        ct = facade.get_culture_type(culture_type_id)
        if not ct:
            culture_api.abort(404, 'Type introuvable')
        return ct

    @jwt_required()
    @admin_required
    def put(self, culture_type_id):
        """Met à jour un type de culture. (admin)"""
        ct = facade.put_culture_type(culture_type_id, **request.get_json())
        if not ct:
            culture_api.abort(404, 'Type introuvable')
        return ct.to_dict()

    @jwt_required()
    @admin_required
    def delete(self, culture_type_id):
        """Supprime un type de culture. (admin)"""
        if not facade.delete_culture_type(culture_type_id):
            culture_api.abort(404, 'Type introuvable')
        return '', 204


@culture_api.route('/')
class CultureList(Resource):
    @culture_api.marshal_list_with(culture_model)
    def get(self):
        """Retourne toutes les cultures. Filtres : ?type_id=1 ou ?parent_id=2 (public)"""
        type_id = request.args.get('type_id', type=int)
        parent_id = request.args.get('parent_id', type=int)
        if type_id:
            return facade.get_cultures_by_type(type_id)
        if parent_id:
            return facade.get_culture_children(parent_id)
        return facade.get_all_cultures()

    @jwt_required()
    @admin_required
    @culture_api.expect(culture_input, validate=True)
    @culture_api.marshal_with(culture_model, code=201)
    def post(self):
        """Crée une culture. (admin)"""
        return facade.post_culture(**request.get_json()), 201


@culture_api.route('/<int:culture_id>')
class CultureDetail(Resource):
    @culture_api.marshal_with(culture_model)
    def get(self, culture_id):
        """Retourne une culture. (public)"""
        culture = facade.get_culture(culture_id)
        if not culture:
            culture_api.abort(404, 'Culture introuvable')
        return culture

    @jwt_required()
    @admin_required
    def put(self, culture_id):
        """Met à jour une culture. (admin)"""
        culture = facade.put_culture(culture_id, **request.get_json())
        if not culture:
            culture_api.abort(404, 'Culture introuvable')
        return culture.to_dict()

    @jwt_required()
    @admin_required
    def delete(self, culture_id):
        """Supprime une culture. (admin)"""
        if not facade.delete_culture(culture_id):
            culture_api.abort(404, 'Culture introuvable')
        return '', 204


# ===========================================================================
# PROFESSION
# ===========================================================================

profession_api = Namespace('professions', description='Professions', path='/api/professions')

profession_model = profession_api.model('Profession', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(required=True),
    'short_description': fields.String(),
    'image_url': fields.String(),
    'created_at': fields.String(readonly=True),
    'updated_at': fields.String(readonly=True),
})

profession_input = profession_api.model('ProfessionInput', {
    'name': fields.String(required=True),
    'short_description': fields.String(),
    'image_url': fields.String(),
})


@profession_api.route('/')
class ProfessionList(Resource):
    @profession_api.marshal_list_with(profession_model)
    def get(self):
        """Retourne toutes les professions. (public)"""
        return facade.get_all_professions()

    @jwt_required()
    @admin_required
    @profession_api.expect(profession_input, validate=True)
    @profession_api.marshal_with(profession_model, code=201)
    def post(self):
        """Crée une profession. (admin)"""
        return facade.post_profession(**request.get_json()), 201


@profession_api.route('/<int:profession_id>')
class ProfessionDetail(Resource):
    @profession_api.marshal_with(profession_model)
    def get(self, profession_id):
        """Retourne une profession. (public)"""
        p = facade.get_profession(profession_id)
        if not p:
            profession_api.abort(404, 'Profession introuvable')
        return p

    @jwt_required()
    @admin_required
    def put(self, profession_id):
        """Met à jour une profession. (admin)"""
        p = facade.put_profession(profession_id, **request.get_json())
        if not p:
            profession_api.abort(404, 'Profession introuvable')
        return p.to_dict()

    @jwt_required()
    @admin_required
    def delete(self, profession_id):
        """Supprime une profession. (admin)"""
        if not facade.delete_profession(profession_id):
            profession_api.abort(404, 'Profession introuvable')
        return '', 204


# ===========================================================================
# OBJECT
# ===========================================================================

object_api = Namespace('objects', description='Objets', path='/api/objects')

object_type_model = object_api.model('ObjectType', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(required=True),
    'image_url': fields.String(),
})

object_model = object_api.model('Object', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(required=True),
    'short_description': fields.String(),
    'image_url': fields.String(),
    'object_type_id': fields.Integer(required=True),
    'created_at': fields.String(readonly=True),
    'updated_at': fields.String(readonly=True),
})

object_input = object_api.model('ObjectInput', {
    'name': fields.String(required=True),
    'short_description': fields.String(),
    'image_url': fields.String(),
    'object_type_id': fields.Integer(required=True),
})


@object_api.route('/types')
class ObjectTypeList(Resource):
    @object_api.marshal_list_with(object_type_model)
    def get(self):
        """Retourne tous les types d'objets. (public)"""
        return facade.get_all_object_types()

    @jwt_required()
    @admin_required
    @object_api.expect(object_type_model, validate=True)
    @object_api.marshal_with(object_type_model, code=201)
    def post(self):
        """Crée un type d'objet. (admin)"""
        return facade.post_object_type(**request.get_json()), 201


@object_api.route('/types/<int:object_type_id>')
class ObjectTypeDetail(Resource):
    @object_api.marshal_with(object_type_model)
    def get(self, object_type_id):
        """Retourne un type d'objet. (public)"""
        ot = facade.get_object_type(object_type_id)
        if not ot:
            object_api.abort(404, 'Type introuvable')
        return ot

    @jwt_required()
    @admin_required
    def put(self, object_type_id):
        """Met à jour un type d'objet. (admin)"""
        ot = facade.put_object_type(object_type_id, **request.get_json())
        if not ot:
            object_api.abort(404, 'Type introuvable')
        return ot.to_dict()

    @jwt_required()
    @admin_required
    def delete(self, object_type_id):
        """Supprime un type d'objet. (admin)"""
        if not facade.delete_object_type(object_type_id):
            object_api.abort(404, 'Type introuvable')
        return '', 204


@object_api.route('/')
class ObjectList(Resource):
    @object_api.marshal_list_with(object_model)
    def get(self):
        """Retourne tous les objets. Filtre optionnel : ?type_id=1 (public)"""
        type_id = request.args.get('type_id', type=int)
        if type_id:
            return facade.get_objects_by_type(type_id)
        return facade.get_all_objects()

    @jwt_required()
    @admin_required
    @object_api.expect(object_input, validate=True)
    @object_api.marshal_with(object_model, code=201)
    def post(self):
        """Crée un objet. (admin)"""
        return facade.post_object(**request.get_json()), 201


@object_api.route('/<int:object_id>')
class ObjectDetail(Resource):
    @object_api.marshal_with(object_model)
    def get(self, object_id):
        """Retourne un objet. (public)"""
        obj = facade.get_object(object_id)
        if not obj:
            object_api.abort(404, 'Objet introuvable')
        return obj

    @jwt_required()
    @admin_required
    def put(self, object_id):
        """Met à jour un objet. (admin)"""
        obj = facade.put_object(object_id, **request.get_json())
        if not obj:
            object_api.abort(404, 'Objet introuvable')
        return obj.to_dict()

    @jwt_required()
    @admin_required
    def delete(self, object_id):
        """Supprime un objet. (admin)"""
        if not facade.delete_object(object_id):
            object_api.abort(404, 'Objet introuvable')
        return '', 204
