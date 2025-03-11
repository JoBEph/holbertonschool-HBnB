from flask_restx import Namespace, Resource, fields
from app.services import facade
import re

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
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        if not user_data["first_name"] or not user_data["last_name"] or not user_data["email"]:
            api.abort(400, "invalid input data")

        if not user_data['first_name'] or not isinstance(user_data['first_name'], str):
            api.abort(400, "first name must be a non-empty string")
        
        if not user_data['last_name'] or not isinstance(user_data['last_name'], str):
            api.abort(400, "last name must be a non-empty string")

        if not user_data['email'] or not isinstance(user_data['email'], str):
            api.abort(400, "email is required")

        if not isinstance(user_data['email'], str):
            api.abort(400, "email must be a string")

        email_pattern = r"^[a-zA-Z0-9_.-]+@[a-zA-Z-_]+\.[a-zA-Z]{2,}$"
        if not re.match(email_pattern, user_data['email']):
            api.abort(400, "Invalid input data: email format is incorrect")

        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            api.abort(400, "Email already registred")

        try:
            new_user = facade.create_user(user_data)
        except (ValueError, TypeError) as e:
            api.abort(400, str(e))
        
        return new_user.display(), 201

    @api.response(200, "Successfully retrieved list")
    def get(self):
        list_users = facade.get_all_users()
        return list_users

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        return {'id': user.id, 'first_name':
                user.first_name, 'last_name':
                user.last_name, 'email': user.email}, 200

    @api.expect(user_model)
    @api.response(201, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """Update user"""
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
            api.abort(400, f"error: {str(e)}")

        return updated_user.display(), 201

    @api.response(204, 'User successfully deleted')
    @api.response(404, 'User not found')
    def delete(self, user_id):
        user = facade.get_user(user_id)
        print(f"Tentative de suppression de l'utilisateur : {user}")
        if not user:
            return {'error': 'User not found'}, 404

        facade.delete_user(user_id)
        return '', 204