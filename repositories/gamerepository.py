from repositories.baserepository import BaseRepository
from exceptions.repositoryexception import RepositoryException


class GameRepository(BaseRepository):
    def insert_many(self, games):
        try:
            games_collection = self.db.Games
            games_collection.insert_many(games)
        except Exception as e:
            raise RepositoryException('error storing games', e.details)

    def get_many(self, limit, page):
        try:
            games_collection = self.db.Games
            result = games_collection.find().skip(page*limit).limit(limit)
            return result
        except Exception as e:
            raise RepositoryException('error retrieving games', e.details)

    def update(self, game):
        try:
            games_collection = self.db.Games
            result = games_collection.replace_one({'_id': game.uid}, game.json())
            return result
        except Exception as e:
            raise RepositoryException('error retrieving games', e.details)

