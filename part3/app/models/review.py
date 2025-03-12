from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base_class import Baseclass
from app.models.place import Place
from app.models.user import User


class Review(Baseclass):

    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    text = Column(String)
    rating = Column(Integer)
    place_id = Column(Integer)
    user_id = Column(Integer)

    def __init__(self, text, rating, place_id, user_id):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id
        self.validate()

    def validate(self):
        if not self.text:
            raise ValueError('Error: Text is empty.')
        if not (1 <= self.rating <= 5):
            raise ValueError('Error: Choose between 1 and 5')

    def update(self, text=None, rating=None, place_id=None, user_id=None):
        if text is not None:
            self.text = text
        if rating is not None:
            self.rating = rating
        if place_id is not None:
            self.place_id = place_id
        if user_id is not None:
            self.user_id = user_id
        self.updated_at = Baseclass.datetime.now()
        self.validate()

    def __str__(self):
        return (
            f'Review: (id={self.id}, text={self.text}, rating={self.rating}, '
            f'place_id={self.place_id}, user_id={self.user_id})'
        )
