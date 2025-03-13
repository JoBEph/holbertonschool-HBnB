from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base_class import Baseclass
from app.models.place import Place
from app.models.user import User
from app import db, bcrypt
from flask_sqlalchemy import SQLAlchemy


class Review(Baseclass):
    
    db = SQLAlchemy()

    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.Integer, ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)

    place = relationship('Place', backref='reviews')
    user = relationship('User', backref='reviews')

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
        if Place.query.get(self.place_id) is None:
            raise ValueError('Error: Place does not exist')
        if User.query.get(self.user_id) is None:
            raise ValueError('Error: User does not exist')

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
            f'place={self.place}, user={self.user})'
        )
