from flask_restful import Resource
import requests
import json
from models.game import GameModel
from pymongo import MongoClient
from instance.config import app_config
import os


class ImportData(Resource):
    def get(self):
        config_name = os.getenv('APP_SETTINGS')
        config = app_config[config_name]
        url = "https://www.giantbomb.com/api/games?api_key=87ea21d55cc157899bc6c64372bf0d4fd215f930&format=json&offset=0"
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        result = requests.get(url, headers=headers)

        print(result.status_code)

        if result.ok:
            json_data = json.loads(result.content)['results']
            games = []
            for item in json_data:
                games.append(GameModel.as_game(item).json())

            client = MongoClient(config.MONGODB_CONNSTR)
            db = client[config.CATALOG_NAME]
            games_collection = db.Games
            insert_result = games_collection.insert_many(games)
            print(insert_result)
        else:
            result.raise_for_status()
