from app.models.user import User
from app.models.review import Review
from app.models.place import Place
from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    # User methods
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        list_users = self.user_repo.get_all()
        return [user.display() for user in list_users]

    def update_user(self, user_id, user_data):
        self.user_repo.update(user_id, user_data)
        return self.user_repo.get(user_id)

    # Review methods
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

   # Amenity methods
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        self.amenity_repo.update(amenity_id, amenity_data)
        return self.amenity_repo.get(amenity_id)

    def delete_amenity(self, amenity_id):
        amenity = self.amenity_repo.get(amenity_id)
        self.amenity_repo.delete(amenity)
        return amenity

    # Place methods
    def create_place(self, place_data):
        try:
            place = Place(
                title=place_data['title'],
                description=place_data.get('description', ''),
                price=place_data['price'],
                latitude=place_data['latitude'],
                longitude=place_data['longitude'],
                owner_id=place_data['owner_id'],
                amenities=place_data['amenities']
            )
            self.place_repository.save(place)
            return place
        except Exception as e:
            raise ValueError(f"Error creation place: {e}")
        
    def get_place(self, place_id):
    # Placeholder for logic to retrieve a place by ID, including associated owner and amenities
        return self.place_repository.get_all()

    def get_all_places(self):
    # Placeholder for logic to retrieve all places
        return self.place_repository.get_all()

    def update_place(self, place_id, place_data):
    # Placeholder for logic to update a place
        place = self.place_repository.get_by_id(place_id)
        if not place:
            raise ValueError(f"Place avec ID {place_id} pas trouvé")

    def get_place_by_id(self, place_id):
        place = self.place_repository.get_by_id(place_id)
        if not place:
            raise ValueError(f"Place avec ID {place_id} pas trouvé")
        return place
