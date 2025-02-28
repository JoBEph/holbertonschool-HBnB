#!/usr/bin/python3
"""
This file provide an user class
"""
import re
from .base_class import Baseclass


class User(Baseclass):
    """
    This class represent an user
    """
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.place = []

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise TypeError("first name must be a string")
        if not value:
            raise TypeError("first name is required")
        if len(value) > 50:
            raise ValueError("first name is too long")
        self._first_name = value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if not isinstance(value, str):
            raise TypeError("last name must be a string")
        if not value:
            raise TypeError("last name is required")
        if len(value) > 50:
            raise ValueError("last name is too long")
        self._last_name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        pattern = r"^[a-zA-Z0-9_.-]+@[a-zA-Z-_]+\.[a-zA-Z]{2,}$"
        if not isinstance(value, str):
            raise TypeError("Email must be a string")
        if not value:
            raise TypeError("Email is required")
        if not re.match(pattern, value):
            raise ValueError("Email is not valid")
        self._email = value

    @property
    def is_admin(self):
        return self._is_admin

    @is_admin.setter
    def is_admin(self, value):
        if not isinstance(value, bool):
            raise TypeError("Admin must be True or False")
        self._is_admin = value

    @property
    def place(self):
        return self._place

    @place.setter
    def add_place(self, value):
        self._place.append(value)

    def display(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }