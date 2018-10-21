import requests
import json
import os
import instance.log
from flask_restful import Resource
from models.game import GameModel
from instance.config import app_config
from repositories.gamerepository import GameRepository
from exceptions.repositoryexception import RepositoryException


class ImportList(Resource):
    def __init__(self):
        config_name = os.getenv('APP_SETTINGS')
        self.config = app_config[config_name]
        self.list_url = self.config.IMPORT_API_URL + "games"
        self.list_url = self.list_url + "?api_key={}".format(os.getenv('IMPORT_API_KEY'))
        self.list_url = self.list_url + "&format=json"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }
        self.page_size = 100
        self.logger = instance.log.setup_custom_logger(__name__)

    def get(self):
        games = []
        start_page = 0
        end_page = 2
        for i in range(start_page, end_page+1):
            offset = i*self.page_size
            url = self.list_url + "&offset={0}".format(offset)

            try:
                self.logger.debug("requesting {0}".format(url))
                result = requests.get(url, headers=self.headers)
            except e:
                self.logger.exception("unhandled exception during request")

            if result.ok:
                self.logger.debug("request successful")
                json_data = json.loads(result.content)['results']
                for item in json_data:
                    games.append(GameModel.as_game(item).json())
            else:
                self.logger.error("request failed with status code {0}".format(result.status_code))
                result.raise_for_status()

            if i % 50 == 0 or i == end_page:
                self.logger.debug("persisting games (count = {0})".format(len(games)))
                try:
                    with GameRepository() as game_repository:
                        game_repository.insert_many(games)
                except RepositoryException as e:
                    self.logger.exception("An error has occurred while persisting the games summary. \n {0}"
                                          .format(e.errors))
                games = []

