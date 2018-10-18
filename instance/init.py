from flask import Flask
from flask_restful import Api
from instance.config import app_config
from resources.game import Game
from resources.game import Games
from resources.importdata import ImportData

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    api = Api(app)
    api.add_resource(Game, '/game/<string:name>')
    api.add_resource(Games, '/games')
    api.add_resource(ImportData, '/import')

    return app
