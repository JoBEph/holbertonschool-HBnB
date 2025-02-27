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
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._is_admin = is_admin
        self._place = []

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if re.match(r"^[A-Za-z][a-zA-Z]{2,49}+$", value, re.UNICODE) \
              is not None:
            self._first_name = value
        else:
            raise ValueError("Wrong input !")

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if re.match(r"^[A-Za-z][a-zA-Z]{2,49}+$", value, re.UNICODE):
            self._last_name = value
        else:
            raise ValueError("Wrong input !")

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        pattern = r"^[a-zA-Z0-9_.-]+@[a-zA-Z-_]+\.[a-zA-Z]{2,}$"
        if re.match(pattern, value) is not None:
            self._email = value
        else:
            raise ValueError("The format is wrong !")

    @property
    def is_admin(self):
        return self._is_admin

    @is_admin.setter
    def is_admin(self, value):
        if value == True or value == False:
            self._is_admin = value

    @property
    def place(self):
        return self._place

    @place.setter
    def add_place(self, value):
        self._place.append(value)
