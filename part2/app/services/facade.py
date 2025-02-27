from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # Placeholder method for creating a user
    def create_user(self, user_data):
        # Logic will be implemented in later tasks
        pass

    # Placeholder method for fetching a place by ID
    def get_place(self, place_id):
        # Logic will be implemented in later tasks
        pass

    def create_review(self, review_data):
        # Placeholder for logic to create a review, including validation for user_id, place_id, and rating
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')
        rating = review_data.get('rating')

        if not user_id or not place_id or not rating:
            raise ValueError('user_id, place_id, and rating not found in review data')
        if not 1 <= rating <= 5:
            raise ValueError('rating must be between 1 and 5')
        
        review = {user_id: user_id, place_id: place_id, rating: rating}

        self.database.save('reviews', review)
    
    def get_review(self, review_id):
    # Placeholder for logic to retrieve a review by ID
        review = review_data.get('review_id')
    

    def get_all_reviews(self):
    # Placeholder for logic to retrieve all reviews
        pass

    def get_reviews_by_place(self, place_id):
    # Placeholder for logic to retrieve all reviews for a specific place
        pass

    def update_review(self, review_id, review_data):
    # Placeholder for logic to update a review
        pass

    def delete_review(self, review_id):
    # Placeholder for logic to delete a review
        pass