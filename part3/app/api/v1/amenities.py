from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity created successfully')
    @api.response(400, 'Invalid data')
    @jwt_required()
    def post(self):
        """Create a new amenity"""
        amenity_data = api.payload
        try:
            amenity = facade.create_amenity(amenity_data)
            return amenity, 201
        except ValueError as e:
            return {'Error': str(e)}, 400

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve the list of all amenities"""
        amenities = facade.get_all_amenities()
        return amenities, 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get details of an amenity by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return amenity, 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @jwt_required()
    def put(self, amenity_id):
        """Update an amenity"""
        current_user = get_jwt_identity()
        amenity = facade.get_amenity(amenity_id)
        
        if not amenity:
            return {'error': 'Amenity not found'}, 404

        # Additional checks (if needed for ownership) can go here
        amenity_data = api.payload
        updated_amenity = facade.update_amenity(amenity_id, amenity_data)
        return updated_amenity, 200

    @api.response(204, 'Amenity deleted successfully')
    @api.response(404, 'Amenity not found')
    @jwt_required()
    def delete(self, amenity_id):
        """Delete an amenity"""
        facade.delete_amenity(amenity_id)
        return '', 204
