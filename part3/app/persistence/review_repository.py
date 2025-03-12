from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
"""
 test Defines the Reviews class and Base instance.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Review(Base):
    """Review class Base"""
    __tablename__ = 'Review'
    id =  Column(Integer, primary_key=True)
    text = Column(String)
    rating =  Column(Integer)
