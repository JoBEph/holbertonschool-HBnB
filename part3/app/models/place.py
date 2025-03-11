import uuid
from datetime import datetime
from app.models.base_class import Baseclass
from app.models.user import User
from app.models.amenity import Amenity


"""
Création class Place
"""


class Place(Baseclass):
    """
    Création class Place
    """

    def __init__(self, title, price, latitude, longitude, owner, owner_id, description=""):
        super().__init__()
        self.place_id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.owner_id = owner_id
        self.reviews = []
        self.amenities = []

        if not isinstance(title, str) or len(title) > 100:
            raise ValueError("Titre trop long")
        if not isinstance(price, (float, int)) or price <= 0:
            raise ValueError("Le prix dois etre positif")
        if not isinstance(latitude,
                          (float, int)) or not (-90.0 <= latitude <= 90.0):
            raise ValueError("Error 404")
        if not isinstance(longitude,
                          (float, int)) or not (-180.0 <= longitude <= 180.0):
            raise ValueError("Error 404")
        if owner is not None and not isinstance(owner, User):
            raise TypeError("Owner inexistant")
        if not isinstance(owner_id, str):
            raise TypeError("L'ID du propriétaire est invalide")

        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def add_review(self, review):
        self.reviews.append(review)

    def add_amenity(self, amenity):
        self.amenities.append(amenity)

    def __str__(self):
        return f"Place: {self.title} (Owner: {self.owner() if self.owner else 'No Owner'})"
