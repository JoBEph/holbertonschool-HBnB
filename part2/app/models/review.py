from app.models.base_class import BaseClass
from place import Place
from user import User


class Review(BaseClass):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
        self.validate()

    def validate(self):
        if not self.text:
            raise ValueError('Error: Text is empty.')
        if not (1 <= self.rating <= 5):
            raise ValueError('Error: Choose between 1 and 5')
        if not isinstance(self.place, Place):
            raise ValueError('Error: Place does not exist.')
        if not isinstance(self.user, User):
            raise ValueError('Error: User does not exist.')
        
    
    def place_exist(self, obj_id):
        place = place._storage.get(obj_id)
        if place is None:
            print(f'Place {obj_id} does not exist')
            return False
        else:
            print(f'Place {obj_id} exist')
            return True

    def user_exist(self, obj_id):
        user = user._storage.get(obj_id)
        if user is None:
            print(f'User {obj_id} does not exist')
            return False
        else:
            print(f'User {obj_id} exist')
        return True

    def update_text(self, text):
        if self.text != text:
            self.text = text
            self.updated_at = BaseClass.datetime.now()
            self.validate()

    def update_rating(self, rating):
        if self.rating != rating:
            self.rating = rating
            self.updated_at = BaseClass.datetime.now()
            self.validate()

    def __str__(self):
        return (
            f'Review: (id={self.id}, text={self.text}, rating={self.rating}, '
            f'place={self.place}, user={self.user})'
        )
