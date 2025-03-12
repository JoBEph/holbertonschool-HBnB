#!/usr/bin/python3
from app.models.base_class import Baseclass


class Amenity(Baseclass):
    """
    Amenity class that defines attributes and methods for amenities.
    Inherits from Base_class which provides common attributes.
    """
    name = ""

    def __init__(self, *args, **kwargs):
        """Initialize an Amenity instance."""
        super().__init__(*args, **kwargs)
#!/usr/bin/python3
"""This module for the Class Amenity"""
from datetime import datetime
import uuid

from app.models.base_class import Baseclass



class Amenity(Baseclass):
    """To create attibutes for the Class"""
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not name or not isinstance(name, str):
            raise ValueError("The name of the amenity is required and must be a string")
        if len(name) > 50:
            raise ValueError("The name of the amenity cannot exceed 50 characters")

        self.id = str(uuid.uuid4())

        self.name = name
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        self.places = []

    def add_place(self, place):
        from app.models.place import Place

        if not isinstance(place, Place):
            raise ValueError("Place must be a Place instance")

        if place not in self.places:
            self.places.append(place)
            if self not in place.amenities:
                place.add_amenity(self)

    def remove_place(self, place):
        if place in self.places:
            self.places.remove(place)
            if self in place.amenities:
                place.remove_amenity(self)

    def update_timestamp(self):
        self.updated_at = datetime.now()
