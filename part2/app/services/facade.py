from app.models.user import User
from app.models.review import Review
from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def create_review(self, review_data):
        review = Review(**review_data)
        self.review_repo.add(review)
        return review
    
    def get_review(self, review_id):
        return self.review_repo.get(review_id)
    
    def get_all_reviews(self):
        return self.review_repo.get_all()
    
    def get_reviews_by_place(self, place_id):
        return self.review_repo.get_by_attribute('place', place_id)
    
    def update_review(self, review_id, data):
        review = self.review_repo.get(review_id)
        review.update(data)
        return review
    
    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        self.review_repo.delete(review)
        return review
