from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import app, jwt_required, get_jwt_identity, Place, Review, db

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review created successfully')
    @api.response(400, 'Invalid data')
    @jwt_required()
    def post(self):
        """Register a new review"""
        review_data = api.payload
        if not review_data:
            return {'Error': 'Invalid data'}, 400

        user_id = review_data.get('user')
        if user_id:
            user = facade.get_user(user_id)
            if not user:
                return {'UserNotFound': 'User not found'}, 400

        place_id = review_data.get('place_id')
        if place_id:
            place = facade.get_place(place_id)
            if not place:
                return {'PlaceNotFound': 'Place not found'}, 400

        rating = review_data.get('rating')
        if not (1 <= rating <= 5):
            return {'InvalidRating': 'Invalid rating. Choose between 1 and 5'}, 400

        try:
            review = facade.create_review(review_data)
        except (ValueError, TypeError) as error:
            return {'Error': str(error)}, 400

        return jsonify(review), 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve the list of all reviews"""
        reviews = facade.get_all_reviews()
        return jsonify(reviews), 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get details of a review by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'Error': 'Review not found'}, 404
        return jsonify(review), 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid data')
    @jwt_required()
    def put(self, review_id):
        """Update a review"""
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)
        if not review or review.user_id != current_user:
            return jsonify({"error": "Unauthorized"}), 403

        data = request.get_json()
        updated_review = facade.update_review(review_id, data)
        if not updated_review:
            return {'Error': 'Review not found'}, 404
        return jsonify(updated_review), 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)

        if not review or review.user_id != current_user:
            return jsonify({"error": "Unauthorized"}), 403

        facade.delete_review(review_id)
        return jsonify({"Error": "Review deleted"}), 200
