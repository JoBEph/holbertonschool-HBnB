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
                return {'UserNotFound': 'User not found'}, 400

        place_id = review_data.get('place_id')
        if place_id:
            place = facade.get_place(place_id)
            if not place:
                return {'PlaceNotFound': 'Place not found'}, 400
        
        rating = review_data.get('rating')
        if not (1 <= rating <= 5):
            return {'IvalidRating': 'Invalid rating. Choose between 1 and 5'}, 400
        
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

@app.route('/api/v1/reviews/', methods=['POST'])
@jwt_required()
def create_review():
    current_user = get_jwt_identity()
    data = request.get_json()
    
    place = Place.query.get(data["place_id"])
    if not place:
        return jsonify({"error": "Lieu non trouvé"}), 404
    
    if place.owner_id == current_user:
        return jsonify({"error": "Vous ne pouvez pas évaluer votre propre lieu"}), 403
    
    existing_review = Review.query.filter_by(user_id=current_user, place_id=place.id).first()
    if existing_review:
        return jsonify({"error": "Vous avez déjà évalué ce lieu"}), 400
    
    new_review = Review(user_id=current_user, place_id=place.id, text=data["text"])
    db.session.add(new_review)
    db.session.commit()

    return jsonify({"message": "Avis ajouté"}), 201

@app.route('/api/v1/reviews/<int:review_id>', methods=['PUT'])
@jwt_required()
def update_review(review_id):
    current_user = get_jwt_identity()
    review = Review.query.get(review_id)

    if not review or review.user_id != current_user:
        return jsonify({"error": "Non autorisé"}), 403

    data = request.get_json()
    review.text = data.get("text", review.text)
    db.session.commit()

    return jsonify({"message": "Avis mis à jour"})

@app.route('/api/v1/reviews/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    current_user = get_jwt_identity()
    review = Review.query.get(review_id)

    if not review or review.user_id != current_user:
        return jsonify({"error": "Non autorisé"}), 403

    db.session.delete(review)
    db.session.commit()

    return jsonify({"message": "Avis supprimé"})
