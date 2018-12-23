import os
from dotenv import load_dotenv
from pathlib import Path
from flask import Flask
from flask_restful import Api
from .instance.config import app_config
from .resources import Game, Games, PersonResource, CountryResource
from mongoengine import connect
from flask_restful_swagger import swagger

vars_path = Path('.') / 'vars.env'
private_vars_path = Path('.') / 'private_vars.env'
load_dotenv(dotenv_path=vars_path)
load_dotenv(dotenv_path=private_vars_path)

config_name = os.getenv('APP_SETTINGS')
application = Flask(__name__)
application.config.from_object(app_config[config_name])
api = swagger.docs(Api(application), apiVersion='0.1')
api.add_resource(Game, '/games/<string:name>')
api.add_resource(Games, '/games')
# api.add_resource(ImportList, '/importsummary')
# api.add_resource(ImportDetail, '/importdetail')
api.add_resource(PersonResource, '/people')
api.add_resource(CountryResource, '/countries')


connect(host=app_config[config_name].MONGODB_CONNSTR.format(os.getenv('MONGODB_USER'), os.getenv('MONGODB_PASSWORD')))

if __name__ == '__main__':
    application.run()
