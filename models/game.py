import datetime
import json
from flask import session


class GameModel:
    """This class represents the game entity."""

    def __init__(self, name, release_date, deck, description, external_id, external_guid):
        """initialize with name."""
        self.name = name
        self.deck = deck
        self.description = description
        self.external_guid = external_guid
        self.external_id = external_id
        self.release_date = release_date
        self.date_modified = datetime.datetime.now()

    def save(self):
        games = session.get("games")
        if games is None:
            games = {}
        games[self.name] = self.__dict__
        session["games"] = games

    @staticmethod
    def get(name):
        games = session.get("games")
        if games:
            game = games.get(name)
            if game:
                return json.loads(json.dumps(game, indent=4, sort_keys=True, default=str),
                                  object_hook=GameModel.as_game)

    @staticmethod
    def get_all():
        games = session.get("games")
        if games is None:
            games = {}

        game_list = [json.loads(json.dumps(g, indent=4, sort_keys=True, default=str),
                                object_hook=GameModel.as_game)
                     for g in games.values()]
        return game_list

    def delete(self):
        games = session.get("games")
        if games:
            games.pop(self.name)
        session["games"] = games

    def json(self):
        return {'name': self.name, 'release_date': str(self.release_date),
                'deck': self.deck, 'description': self.deck, 'external_id': self.external_id,
                'external_guid': self.external_guid,
                'date_modified': str(self.date_modified)}

    @staticmethod
    def as_game(item):
        gm = GameModel(item['name'], item['original_release_date'], item['deck'], item['description'], item['id'],
                       item['guid'])
        return gm

    def __repr__(self):
        return "<Game: {}>".format(self.name)
