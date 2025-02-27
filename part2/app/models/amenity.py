#!/usr/bin/python3
from datetime import datetime
import uuid

Base_class = __import__("base_class").Baseclass


class Amenity(Base_class):
    def __init__(self, name, *args, **kwargs):
        """
        Initialize a new instance of Amenity with the necessary attributes.

        Args:
            name (str): The name of amenity (required, maximum 50 characters)

    Generates a unique identifier for amenity, records the creation update
    timestamps, and initializes the list of locations associated with amenity.
        """
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
        """
    Add a place to the equipment and establish the bidirectional relationship.

        Args:
            place (Place): Place instance to add
        """
        from app.models.place import Place

        if not isinstance(place, Place):
            raise ValueError("Place must be a Place instance")

        if place not in self.places:
            self.places.append(place)
            if self not in place.amenities:
                place.add_amenity(self)

    def remove_place(self, place):
        """
   Remove place from equipment and establish reverse bidirectional relationship

        Args:
            place (Place): Place instance to remove
        """
        if place in self.places:
            self.places.remove(place)
            if self in place.amenities:
                place.remove_amenity(self)

    def update_timestamp(self):
        """
        Update the `updated_at` timestamp when equipment is modified.
        """
        self.updated_at = datetime.now()
