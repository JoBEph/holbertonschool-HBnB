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
    """Collect all equipment"""
    return Amenity.query.all()

def update_amenity(self, amenity_id, amenity_data):
        """Update existing equipment"""
        amenity = Amenity.query.get(amenity_id)
        if not amenity:
            return None
        amenity.name = name
        db.session.commit()
        return amenity
