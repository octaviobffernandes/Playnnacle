from repositories.baserepository import BaseRepository
from exceptions.storeexception import StoreException


class GameRepository(BaseRepository):
    def insert_many(self, games):
        try:
            games_collection = self.db.Games
            games_collection.insert_many(games)
        except Exception as e:
            raise StoreException('error storing games', e.details)


