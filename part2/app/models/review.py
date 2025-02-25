import uuid
from datetime import datetime


class Review:
    def __init__(self, text, rating, place, user):
        self.id = str(uuid.uuid4())
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.validate()

    def validate(self):
        if not self.text:
            raise ValueError('Error: Text is empty.')
        if not (1 <= self.rating <= 5):
            raise ValueError('Error: Choose beetween 1 and 5')
        if not self.place:
            raise ValueError('Error: Place does not exist.')
        if not self.user:
            raise ValueError('Error: User does not exist.')

    def place_exist(self, place):

        print(f'Place {place} exists')
        return True

    def user_exist(self, user):
        print(f'User {user} exists')
        return True

    def update_text(self, text):
        if self.text != text:
            self.text = text
            self.updated_at = datetime.now()
            self.validate()

    def update_rating(self, rating):
        if self.rating != rating:
            self.rating = rating
            self.updated_at = datetime.now()
            self.validate()
