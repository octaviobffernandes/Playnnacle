import os
from dotenv import load_dotenv
from pathlib import Path
from flask import Flask
from flask_restful import Api
from instance.config import app_config
from resources.game import Game
from resources.game import Games
from resources.importlist import ImportList
from resources.importdetail import ImportDetail


vars_path = Path('.') / 'vars.env'
private_vars_path = Path('.') / 'private_vars.env'
load_dotenv(dotenv_path=vars_path)
load_dotenv(dotenv_path=private_vars_path)

config_name = os.getenv('APP_SETTINGS')
application = Flask(__name__)
application.config.from_object(app_config[config_name])
api = Api(application)
api.add_resource(Game, '/game/<string:name>')
api.add_resource(Games, '/games')
api.add_resource(ImportList, '/importsummary')
api.add_resource(ImportDetail, '/importdetail')

if __name__ == '__main__':
    application.run()