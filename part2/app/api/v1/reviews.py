from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from app.services import facade

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
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        review_data = api.payload
        if not review_data:
            return {'Error': 'Invalid input data'}, 400

        user_id = review_data.get('user')
        if user_id:
            user = facade.get_user(user_id)
            if not user:
                return {'Error': 'User not found'}, 400

        # place_id = review_data.get('place_id')
        # if place_id:
        #     place = facade.get_place(place_id)
        #     if not place:
        #         return {'Error': 'Place not found'}, 400
        try:
            review = facade.create_review(review_data)
        except (ValueError, TypeError) as error:
            return {'Error': str(error)}, 400


        return jsonify(review), 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return jsonify(reviews), 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'Error': 'Review not found'}, 404
        return jsonify(review), 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        data = request.get_json()
        if not data:
            return {'Error': 'Invalid input data'}, 400
        updated_review = facade.update_review(review_id, data)
        if not updated_review:
            return {'Error': 'Review not found'}, 404
        return jsonify(updated_review), 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        deleted = facade.delete_review(review_id)
        if not deleted:
            return {'Error': 'Review not found'}, 404
        return jsonify({"Error": "Review deleted"}), 200

# @api.route('/places/<place_id>/reviews')
# class PlaceReviewList(Resource):
#     @api.response(200, 'List of reviews for the place retrieved successfully')
#     @api.response(404, 'Place not found')
#     def get(self, place_id):
#         """Get all reviews for a specific place"""
#         reviews = facade.get_reviews_by_place(place_id)
#         if not reviews:
#             return {'Error': 'Place not found or no reviews for this place'}, 404
#         return jsonify(reviews), 200
