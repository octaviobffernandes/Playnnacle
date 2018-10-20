import datetime
import json
from flask import session


class GameModel:
    """This class represents the game entity."""

    def __init__(self, uid, name, release_date, deck, description, external_id, external_guid):
        """initialize with name."""
        self.uid = uid
        self.name = name
        self.deck = deck
        self.description = description
        self.external_guid = external_guid
        self.external_id = external_id
        self.release_date = release_date
        self.date_modified = datetime.datetime.now()
        self.platforms = []
        self.developers = []
        self.genres = []
        self.publishers = []
        self.similar_games = []

    @staticmethod
    def create_simple(name, external_id):
        return GameModel(None, name, None, None, None, external_id, None)

    def json(self):
        return {'_id': self.uid,
                'name': self.name, 'release_date': str(self.release_date),
                'deck': self.deck, 'description': self.deck, 'external_id': self.external_id,
                'external_guid': self.external_guid,
                'date_modified': str(self.date_modified),
                'platforms': [p.json() for p in self.platforms],
                'developers': [d.json() for d in self.developers],
                'genres': [g.json() for g in self.genres],
                'publishers': [p.json() for p in self.publishers],
                'similar_games': [g.simple_json() for g in self.similar_games]}

    def simple_json(self):
        return {'name': self.name, 'external_id': self.external_id}

    @staticmethod
    def as_game(item):
        gm = GameModel(item['name'], item['original_release_date'], item['deck'], item['description'], item['id'],
                       item['guid'])
        return gm

    def __repr__(self):
        return "<Game: {}>".format(self.name)
