from flask_restx import Namespace, Resource, fields
from app.services import facade
import re
from flask_jwt_extended import app, jwt_required, get_jwt_identity, Place, Review, db, jsonify, User, request

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True,
                                description='First name of the user'),
    'last_name': fields.String(required=True,
                               description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User created successfully')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new user"""
        user_data = api.payload

        if not user_data["first_name"] or not user_data["last_name"] or not user_data["email"]:
            api.abort(400, "Invalid data")

        if not user_data['first_name'] or not isinstance(user_data['first_name'], str):
            api.abort(400, "First name must be a non-empty string")
        
        if not user_data['last_name'] or not isinstance(user_data['last_name'], str):
            api.abort(400, "Last name must be a non-empty string")

        if not user_data['email'] or not isinstance(user_data['email'], str):
            api.abort(400, "Email is required")

        email_pattern = r"^[a-zA-Z0-9_.-]+@[a-zA-Z-_]+\.[a-zA-Z]{2,}$"
        if not re.match(email_pattern, user_data['email']):
            api.abort(400, "Invalid email format")

        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            api.abort(400, "Email already registered")

        try:
            new_user = facade.create_user(user_data)
        except (ValueError, TypeError) as e:
            api.abort(400, str(e))

        return new_user.display(), 201

    @api.response(200, "List of users retrieved successfully")
    def get(self):
        list_users = facade.get_all_users()
        return list_users

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get details of a user by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200

    @api.expect(user_model)
    @api.response(201, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid data')
    @jwt_required()
    def put(self, user_id):
        """Update a user"""
        current_user = get_jwt_identity()
        if current_user != user_id:
            return {'error': 'Unauthorized'}, 403

        user_data = api.payload
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        if "email" in user_data:
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user and existing_user.id != user.id:
                api.abort(400, "Email already registered by another user")

        try:
            user.update(user_data)
            updated_user = facade.update_user(user_id, user.display())
        except (ValueError, TypeError) as e:
            api.abort(400, f"Error: {str(e)}")

        return updated_user.display(), 201

    @api.response(204, 'User deleted successfully')
    @api.response(404, 'User not found')
    @jwt_required()
    def delete(self, user_id):
        current_user = get_jwt_identity()
        if current_user != user_id:
            return {'error': 'Unauthorized'}, 403

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        facade.delete_user(user_id)
        return '', 204
