import requests
import json
import os
import instance.log
from flask_restful import Resource
from models.game import GameModel
from instance.config import app_config
from repositories.gamerepository import GameRepository
from exceptions.repositoryexception import RepositoryException
from collections import Iterable
from models.platform import PlatformModel
from models.developer import DeveloperModel
from models.genre import GenreModel
from models.publisher import PublisherModel
import threading


class ImportDetail(Resource):
    def __init__(self):
        config_name = os.getenv('APP_SETTINGS')
        self.config = app_config[config_name]
        self.detail_url = self.config.IMPORT_API_URL + "game/{0}"
        self.detail_url = self.detail_url + "?api_key={}".format(os.getenv('IMPORT_API_KEY'))
        self.detail_url = self.detail_url + "&format=json"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }
        self.logger = instance.log.setup_custom_logger(__name__)

    def get(self):
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        batch_size = 200
        batch_page = 10
        while batch_page > -1:
            game_batch = self.get_batch(batch_page, batch_size)

            if game_batch is not None and isinstance(game_batch, Iterable):
                i = 1
                for item in game_batch:
                    self.logger.debug("processing game {0} of {1} - page {2}".format(i, batch_size, batch_page))
                    game_model = GameModel(item['_id'], item['name'], item['release_date'],
                                           item['deck'], item['description'],
                                           item['external_id'], item['external_id'])

                    url = self.detail_url.format(game_model.external_guid)
                    try:
                        self.logger.debug("requesting {0}".format(url))
                        result = requests.get(url, headers=self.headers)
                    except e:
                        self.logger.exception("unhandled exception during request")

                    if result.ok:
                        json_data = json.loads(result.content)['results']
                        self.load_game_detail(json_data, game_model)
                        self.persist_game(game_model)
                    else:
                        self.logger.error("request failed with status code {0}".format(result.status_code))
                        result.raise_for_status()
                    i = i + 1
                batch_page = batch_page + 1
            else:
                self.logger.debug("no games retrieved")
                batch_page = -1

    def get_batch(self, batch_page, batch_size):
        try:
            with GameRepository() as game_repository:
                self.logger.debug("retrieving {0} games from database (page {1})".format(batch_size, batch_page))
                return game_repository.get_many(batch_size, batch_page)
        except RepositoryException as e:
            self.logger.exception("An error has occurred while retrieving the game batch. \n {0}".format(e.errors))

    @staticmethod
    def load_game_detail(json_data, game_model):
        if 'platforms' in json_data and isinstance(json_data["platforms"], Iterable):
            for p in json_data["platforms"]:
                game_model.platforms.append(PlatformModel(p['name'], p['abbreviation']))

        if 'developers' in json_data and isinstance(json_data["developers"], Iterable):
            for d in json_data["developers"]:
                game_model.developers.append(DeveloperModel(d['name']))

        if 'genres' in json_data and isinstance(json_data["genres"], Iterable):
            for g in json_data["genres"]:
                game_model.genres.append(GenreModel(g['name']))

        if 'publishers' in json_data and isinstance(json_data["publishers"], Iterable):
            for p in json_data["publishers"]:
                game_model.publishers.append(PublisherModel(p['name']))

        if 'similar_games' in json_data and isinstance(json_data["similar_games"], Iterable):
            for s in json_data["similar_games"]:
                game_model.similar_games.append(GameModel.create_simple(s['name'], s['id']))

    def persist_game(self, game_model):
        self.logger.debug("persisting game in database")

        try:
            with GameRepository() as game_repository:
                return game_repository.update(game_model)
        except RepositoryException as e:
            self.logger.exception(
                "An error has occurred while persisting the game details. \n {0}".format(e.errors))
