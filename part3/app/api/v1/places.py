from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    #'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place created successfully')
    @api.response(400, 'Invalid data')
    @jwt_required()
    def post(self):
        """Register a new place"""
        place_data = api.payload
        try:
            place = facade.create_place(place_data)
            return place, 201
        except ValueError as e:
            return {'Error': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve the list of all places"""
        places = facade.get_all_places()
        return places, 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get details of a place by ID"""
        try:
            place = facade.get_place_by_id(place_id)
            return place, 200
        except ValueError:
            return {'message': 'Place not found'}, 404

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid data')
    @jwt_required()
    def put(self, place_id):
        """Update a place"""
        current_user = get_jwt_identity()
        place = facade.get_place_by_id(place_id)

        if not place or place.owner_id != current_user:
            return {'error': 'Unauthorized'}, 403

        place_data = api.payload
        try:
            updated_place = facade.update_place(place_id, place_data)
            return updated_place, 200
        except ValueError as e:
            return {'Error': str(e)}, 400

    @api.response(204, 'Place deleted successfully')
    @api.response(404, 'Place not found')
    @jwt_required()
    def delete(self, place_id):
        """Delete a place"""
        current_user = get_jwt_identity()
        place = facade.get_place_by_id(place_id)

        if not place or place.owner_id != current_user:
            return {'error': 'Unauthorized'}, 403

        facade.delete_place(place_id)
        return '', 204
