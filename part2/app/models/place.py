import uuid
from datetime import datetime
from app.models.base_class import Baseclass
from app.models.user import User
"""
Création class Place
"""


class Place(Baseclass):
    """
    Création class Place
    """

    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner

        if not isinstance(title, str) or len(title) > 100:
            raise ValueError("Titre trop long")
        if not isinstance(price, (float, int)) or price <= 0:
            raise ValueError("Le prix dois etre une valeur positive")
        if not isinstance(latitude,
                          (float, int)) or not (-90.0 <= latitude <= 90.0):
            raise ValueError("Error 404")
        if not isinstance(longitude,
                          (float, int)) or not (-180.0 <= longitude <= 180.0):
            raise ValueError("Error 404")
        if owner is not None and not isinstance(owner, User):
            raise TypeError("Owner inexistant")

        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def __str__(self):
        return f"Place: {self.title} \
        (Owner: {self.owner.full_name() if self.owner else 'No Owner'})"
