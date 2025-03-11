from app.models.user import User
from app.models.review import Review
from app.models.place import Place
from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repository = InMemoryRepository()

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
    def delete_user(self, user_id):
        user = self.user_repo.get(user_id)
        self.user_repo.delete(user)
        return user

    # Review methods
    def create_review(self, review_data):
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')
        rating = review_data.get('rating')

        if not self.get_user(user_id):
            raise ValueError(f"User with ID {user_id} not found")
        if not self.get_place(place_id):
            raise ValueError(f"Place with ID {place_id} not found")
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")

        review = Review(**review_data)
        self.review_repo.add(review)
        return review
    
    def get_review(self, review_id):
        return self.review_repo.get(review_id)
    
    def get_all_reviews(self):
        return self.review_repo.get_all()
    
    def get_reviews_by_place(self, place_id):
        reviews = self.review_repo.get_all()
        return [review for review in reviews if review.place == place_id]
    
    def update_review(self, review_id, data):
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError(f"Review with ID {review_id} not found")
        user_id = data.get('user_id')
        place_id = data.get('place_id')
        rating = data.get('rating')
        if not self.get_user(user_id):
            raise ValueError(f"User with ID {user_id} not found")
        if not self.get_place(place_id):
            raise ValueError(f"Place with ID {place_id} not found")
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        
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
        owner_id = place_data.get('owner_id')
        if not owner_id:
            raise ValueError("Owner ID is required")
        owner = self.get_user(owner_id)
        if not owner:
            raise ValueError(f"User with ID {owner_id} not found")
        try:
            place = Place(
                title=place_data['title'],
                description=place_data.get('description', ''),
                price=place_data['price'],
                latitude=place_data['latitude'],
                longitude=place_data['longitude'],
                owner=owner,
                amenities=place_data['amenities']
            )
            self.place_repository.add(place)
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
