import os
from dotenv import load_dotenv
from pathlib import Path
from flask import Flask
from flask_restful import Api
from .instance.config import app_config
from .resources import Game, Games
# from resources.importlist import ImportList
# from resources.importdetail import ImportDetail
from .resources import PersonResource
from mongoengine import connect



vars_path = Path('.') / 'app/vars.env'
private_vars_path = Path('.') / 'app/private_vars.env'
load_dotenv(dotenv_path=vars_path)
load_dotenv(dotenv_path=private_vars_path)

config_name = os.getenv('APP_SETTINGS')
application = Flask(__name__)
application.config.from_object(app_config[config_name])
api = Api(application)
api.add_resource(Game, '/games/<string:name>')
api.add_resource(Games, '/games')
# api.add_resource(ImportList, '/importsummary')
# api.add_resource(ImportDetail, '/importdetail')
api.add_resource(PersonResource, '/persons')
connect(host='mongodb://<USERNAME>:<PASSWORD>@cluster0-shard-00-00-uu4dq.mongodb.net:27017,cluster0-shard-00-01-uu4dq.mongodb.net:27017,cluster0-shard-00-02-uu4dq.mongodb.net:27017/TestDb?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true')

if __name__ == '__main__':
    application.run()
