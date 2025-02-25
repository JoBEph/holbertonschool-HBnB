Base_class = __import__("base_class").Baseclass

class Amenity(Base_class):
    """
    Amenity class that defines attributes and methods for amenities.
    Inherits from Base_class which provides common attributes like id, created_at, and updated_at.
    """
    name = ""

    def __init__(self, *args, **kwargs):
        """Initialize an Amenity instance."""
        super().__init__(*args, **kwargs)
