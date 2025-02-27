from app.models.user import User
from app.persistence.repository import InMemoryRepository
from app.models.amenity import Amenity, name
from app import db

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
















def create_amenity(self, amenity_data):
    """Create new equipment"""
    new_amenity = Amenity(name=name)
    db.session.add(new_amenity)
    db.session.commit()
    return new_amenity

def get_amenity(self, amenity_id):
    """Retrieve equipment by its ID"""
    return Amenity.query.get(amenity_id)

def get_all_amenities(self):
    # Placeholder for logic to retrieve all amenities
    pass

def update_amenity(self, amenity_id, amenity_data):
    # Placeholder for logic to update an amenity
    pass