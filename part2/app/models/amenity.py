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
