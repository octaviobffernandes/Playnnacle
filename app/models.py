import datetime
import json
from collections import namedtuple
from flask import session


class Game:
    """This class represents the game entity."""

    def __init__(self, name, genre, year):
        """initialize with name."""
        self.name = name
        self.genre = genre
        self.year = year
        self.date_modified = datetime.datetime.now()

    def save(self):
        session[self.name] = self.__dict__

    @staticmethod
    def get(name):
        # TODO: find a more efficient way of getting the element from session and converting to object
        print("searching for ", name)
        data = session.get(name)
        js = json.dumps(data, indent=4, sort_keys=True, default=str)
        return json.loads(js, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

    @staticmethod
    def get_all():
        # TODO: implement get all method
        return 1

    def delete(self):
        # TODO: implement delete method
        self.name= 1+1

    def __repr__(self):
        return "<Game: {}>".format(self.name)
